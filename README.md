# bangumi-tag-for-nfo
给 nas-tools 通过 TMDB 刮削的动漫加上来自 Bangumi 的 Meta tags

## 依赖的 python 库：

```
lxml
requests
```

## 基础使用方法

命令行在媒体目录下使用，由于 nas-tools 链接过去的名字不一定能直接用，所以没设置自动找媒体名字的方法

```
python /<path>/main.py --token xxx --keyword <搜索用的关键字>
```

其它选项：
1. `--write_path`: 指定要写入的 nfo 文件，否则在运行目录下寻找 `movie.nfo` 或 `tvshow.nfo`
2. `--direct`: 很自信设定的关键词一定能找对，使用这个可以选择第一个动画候选
3. `--no_write`: 不进行写，只搜索

## 效果

![使用前](https://github.com/user-attachments/assets/5d864c61-cb02-4231-93dc-de3d7eb6a16e)

![使用](https://github.com/user-attachments/assets/5ac14a01-f717-4be7-b64c-42346a1981f3)

![使用后](https://github.com/user-attachments/assets/ececdbc0-4fdb-4d56-ac17-0f24c09c344b)
