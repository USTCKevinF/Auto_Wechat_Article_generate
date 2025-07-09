# 微信公众号文章生成器

将结构化的访谈数据转换为微信公众号文章格式的HTML。

## 功能特点

- 支持访谈文章的结构化数据转换
- 自动生成微信公众号文章格式的HTML
- 处理文本加粗、段落分割、问答格式等
- 保持原有的样式和排版结构

## 使用方法

1. 准备访谈数据，用llm（最好是gemini 2.5 pro）格式化整理成指定格式的结构化数据，参考data_example.json
2. 运行脚本生成HTML文件：
3. 将生成的html文件粘贴到 https://quaily.com/tools/markdown-to-wx/ 中，然后复制右边的内容粘贴到公众号后台即可

```bash
python generate_article.py
```


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