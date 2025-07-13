# 录音稿处理Pipeline & 微信公众号文章生成器

将录音稿自动转换为微信公众号文章格式的HTML，支持全流程自动化处理。

## 功能特点

- **全自动化Pipeline**: 录音稿 -> 逐字稿 -> JSON -> HTML
- 支持访谈文章的结构化数据转换
- 自动生成微信公众号文章格式的HTML
- 处理文本加粗、段落分割、问答格式等
- 保持原有的样式和排版结构

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置设置

1. 复制 `.env` 文件并配置你的API信息：
   ```bash
   API_KEY=your_api_key_here
   BASE_URL=https://api.openai.com/v1
   MODEL_NAME=gpt-4o
   ```

## 使用方法

### 方法1: 全自动Pipeline（推荐）

直接从录音稿文件开始：

```bash
python pipeline.py 录音稿文件.txt
```

这将自动完成：
1. 录音稿转逐字稿
2. 逐字稿转JSON数据
3. JSON转HTML文章

### 方法2: 手动处理

如果你已有结构化JSON数据：

```bash
python generate_article.py
```

## 最后一步

将生成的HTML文件粘贴到 https://quaily.com/tools/markdown-to-wx/ 中，然后复制右边的内容粘贴到公众号后台即可。


## 数据结构

访谈数据需要包含以下字段：

- `guest_name`: 嘉宾姓名
- `guest_intro`: 嘉宾介绍
- `interviewer`: 采访者
- `proofreader`: 校对者
- `word_count`: 字数统计
- `reading_time`: 预计阅读时间
- `topics`: 主题摘要列表
- `main_sections`: 主要章节内容

## 输出文件

- `wechat_article_generated.html`: 生成的微信公众号文章HTML文件


## 技术特点

- 基于Python开发
- 支持HTML转义和安全处理
- 自动处理文本格式化和样式应用
- 模块化设计，易于扩展和维护