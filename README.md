# Walinemoji 表情包下载与整理工具
> README由LLM生成，请注意鉴别

## 项目简介
本项目用于根据指定的**bilibili**平台表情包ID，从**bilibili**平台接口中自动下载、整理为waline可使用的表情包，包含表情图片、表情包图标、info.json 及 README.md，方便管理和在waline中使用。

## 主要功能
- 根据表情包 ID 自动查找并下载所有表情图片
- 自动下载表情包官方图标文件
- 自动生成包含表情包信息的 info.json 文件（使用预设图标）
- 自动生成带有预览和表格的 README.md 文件
- 支持批量处理多个表情包

## 生成的文件结构
每个下载的表情包会生成如下文件结构：
```
output/
└── {ID}_{表情包名称}/
    ├── {ID}_icon.png           # 表情包官方图标
    ├── {ID}_{表情名称}.png      # 各个表情图片
    ├── info.json               # 表情包信息文件
    └── README.md              # 表情包信息文档
```

## info.json 格式说明
生成的 info.json 文件格式如下：
```json
{
  "name": "表情包名称",
  "prefix": "ID_",
  "icon": "icon",
  "type": "png",
  "items": ["表情1", "表情2", "..."]
}
```

**重要更新**: 
- `icon` 字段现在使用统一的 "icon" 值，对应下载的 `{prefix}icon.png` 文件
- 这确保了与表情包官方图标的正确对应关系

**生成效果**
![](assets/image.png)

## 使用方法
1. clone本仓库以及子模块Bmoji

   ⚠️Bmoji数据文件在本项目中以子模块的方式导入，clone时请加上`--recursive`参数一同clone子模块，如果不使用子模块的方法可以使用-d参数自行指定`emoji_data.json`
   ```bash
   git clone --recursive https://github.com/DakoWang/bilibili_emoji.git
   cd bilibili_emoji
   ```
2. 运行主程序
   ```bash
   python run.py 表情包id
   ```
   或自定义调用 `download_emoji_package(target_id)` 函数
   爬出的表情包将保存在`output/id_name`文件夹中

3. 上传仓库
   参考文章[Waline表情包制作-上传仓库 · Textline博客](https://blog.textline.top/blogs/waline%E8%A1%A8%E6%83%85%E5%8C%85%E5%88%B6%E4%BD%9C/#%E4%B8%8A%E4%BC%A0%E4%BB%93%E5%BA%93)

本仓库爬好了`Mygo`和`Ave Mujica`两个表情包
在waline客户端中的emoji列表中分别加入即可使用
```
https://cdn.jsdelivr.net/gh/DakoWang/bilibili_emoji@v1.0.1/output/5390_Mygo%E8%A1%A8%E6%83%85%E5%8C%85
https://cdn.jsdelivr.net/gh/DakoWang/bilibili_emoji@v1.0.1/output/7961_Ave%20Mujica
```

## 目录结构
```
walinemoji/
├── run.py              # 主程序，包含下载与整理逻辑
├── Bmoji/
│   └── data/
│       └── emoji_data.json  # 表情包数据源
├── output/
│   └── {ID}_{表情包名称}/   # 自动生成的表情包文件夹
│       ├── {ID}_icon.png   # 表情包官方图标
│       ├── {ID}_{表情}.png # 各个表情图片
│       ├── info.json       # 表情包信息
│       └── README.md       # 表情包说明
└── README.md           # 项目说明文档
```

## 依赖说明
- Python 3.x
- requests

## 数据来源
本项目所用的 `emoji_data.json` 数据文件来源于项目：

> https://github.com/SakuraSenQwQ/Bmoji

该数据文件包含从 **bilibili** 平台爬取的表情包信息，包括表情包 ID、名称、图片 URL 等数据。项目会根据这些数据自动从 bilibili CDN (`https://i0.hdslb.com`) 下载对应的表情图片。

如需更新数据，请前往上述仓库获取最新版本。

## 致谢
感谢 Bmoji 项目及其贡献者提供的表情包数据支持。
Copilot

