
import os, time, requests, argparse
from lxml import etree as ET
from pathlib import Path

# MY_BANGUMI_TOKEN = "xxx"
BANGUMI_SEARCH_URL = "https://api.bgm.tv/search/subject/"
BANGUMI_SUBJECT_URL = "https://api.bgm.tv/v0/subjects/"


def search_anime(token, keyword, limit=5):
    cookies = {"chii_searchDateLine": str(int(time.time()))}
    url = BANGUMI_SEARCH_URL + keyword
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "trim21/bangumi-episode-ics (https://github.com/Trim21/bangumi-episode-calendar)",
    }
    resp = requests.get(
        url, params={"max_results": limit}, headers=headers, cookies=cookies, timeout=10
    ).json()
    return [
        (item["id"], item["type"], item["name_cn"] or item["name"])
        for item in resp["list"]
    ]


def get_detail(token, id):
    url = BANGUMI_SUBJECT_URL + str(id)
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "trim21/bangumi-episode-ics (https://github.com/Trim21/bangumi-episode-calendar)",
    }
    detail = requests.get(url, headers=headers, timeout=10).json()
    return detail


def get_direct_subject_id(items):
    for item in enumerate(items):
        if item[1] == 2:
            return item[0]
    return None


def select_subject_id(items):
    for i, item in enumerate(items):
        typestr = None
        if item[1] == 1:
            typestr = "书籍"
        elif item[1] == 2:
            typestr = "动画"
        elif item[1] == 3:
            typestr = "音乐"
        elif item[1] == 4:
            typestr = "游戏"
        elif item[1] == 6:
            typestr = "三次元"
        else:
            typestr = "其它"
        print(f"{i + 1}. {typestr:<4} {item[2]}")
    index = int(input("选择动画序号:")) - 1
    try_times = 5
    while try_times:
        if index >= 0 or index < len(items):
            break
        try_times -= 1
        print("输入错误")
    if try_times == 0:
        return None
    return items[index][0]


def write_tags_to_nfo(nfo_path: Path, tags: list[str]):
    if nfo_path.exists():
        tree = ET.parse(nfo_path)
        root = tree.getroot()
    else:
        root = ET.Element("tvshow")
        tree = ET.ElementTree(root)

    # 删除旧 tag，避免重复
    for t in root.findall("tag"):
        root.remove(t)

    for tag in tags:
        ET.SubElement(root, "tag").text = tag

    # pretty print (3.9+)
    ET.indent(tree, space="  ")
    tree.write(
        nfo_path,
        encoding="utf-8",
        xml_declaration=True,
        standalone=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", nargs="?", help="Bangumi Access Token")
    parser.add_argument("--keyword", nargs="?", help="搜索关键词")
    parser.add_argument("--write_path", nargs="?", help="写入文件")
    parser.add_argument(
        "--direct", action="store_true", help="是否直接使用第一个动画结果"
    )
    parser.add_argument("--no_write", action="store_true", help="是否不写入文件")
    args = parser.parse_args()

    token = args.token or input("输入 Token:")
    keyword = args.keyword or input("输入关键词:")

    items = search_anime(token, keyword)
    if not items:
        print("没有找到相关动画")
        return
    subject_id = None
    if args.direct:
        subject_id = get_direct_subject_id(items)
    else:
        subject_id = select_subject_id(items)

    if subject_id is None:
        print("没有找到相关动画")
        return

    detail = get_detail(token, subject_id)

    print(f"动画名称: {detail['name_cn'] or detail['name']}")
    print(f"tags: {', '.join(detail['meta_tags'])}")

    if args.no_write:
        return

    if args.write_path:
        nfo_file = Path(args.write_path)
    else:
        cwd = Path.cwd()
        candidates = [cwd / "movie.nfo", cwd / "tvshow.nfo"]
        for p in candidates:
            if p.exists():
                nfo_file = p
                break
        else:
            nfo_file = cwd / "tvshow.nfo"

    write_tags_to_nfo(nfo_file, detail["meta_tags"])

    return


if __name__ == "__main__":
    main()
