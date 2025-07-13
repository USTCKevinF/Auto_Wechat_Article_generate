#!/usr/bin/env python3
"""
录音稿处理Pipeline
输入录音稿txt -> 生成逐字稿 -> 转换为JSON -> 生成HTML文章
"""

import os
import json
import yaml
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from generate_article import generate_wechat_article_html

def load_config():
    """加载环境配置"""
    load_dotenv()
    
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('BASE_URL')
    model_name = os.getenv('MODEL_NAME')
    
    if not api_key:
        raise ValueError("请在.env文件中设置API_KEY")
    
    return {
        'api_key': api_key,
        'base_url': base_url,
        'model_name': model_name
    }

def load_prompts():
    """加载prompt配置"""
    with open('prompt.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config['prompts']

def call_llm(client, prompt, content, model_name):
    """调用大语言模型"""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        raise

def step1_transcript_to_verbatim(txt_path, config, prompts):
    """步骤1: 录音稿转逐字稿"""
    print("🎯 步骤1: 录音稿转逐字稿...")
    
    # 读取录音稿
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
    except Exception as e:
        print(f"❌ 无法读取录音稿文件: {e}")
        raise
    
    # 调用大模型
    client = OpenAI(api_key=config['api_key'], base_url=config['base_url'])
    prompt = prompts['transcript_to_verbatim']['content']
    
    verbatim = call_llm(client, prompt, transcript, config['model_name'])
    
    # 保存逐字稿
    verbatim_path = txt_path.replace('.txt', '_verbatim.txt')
    with open(verbatim_path, 'w', encoding='utf-8') as f:
        f.write(verbatim)
    
    print(f"✅ 逐字稿已保存: {verbatim_path}")
    return verbatim, verbatim_path

def step2_verbatim_to_json(verbatim, config, prompts):
    """步骤2: 逐字稿转JSON"""
    print("🎯 步骤2: 逐字稿转JSON...")
    
    # 调用大模型
    client = OpenAI(api_key=config['api_key'], base_url=config['base_url'])
    prompt = prompts['verbatim_to_json']['content']
    
    json_content = call_llm(client, prompt, verbatim, config['model_name'])
    
    # 解析JSON
    try:
        # 提取JSON内容（如果模型返回了额外的文本）
        json_start = json_content.find('{')
        json_end = json_content.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_content = json_content[json_start:json_end]
        
        data = json.loads(json_content)
    except Exception as e:
        print(f"❌ JSON解析失败: {e}")
        print("原始返回内容:")
        print(json_content)
        raise
    
    # 保存JSON
    json_path = 'interview_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON数据已保存: {json_path}")
    return data, json_path

def step3_json_to_html(data):
    """步骤3: JSON转HTML"""
    print("🎯 步骤3: JSON转HTML...")
    
    # 生成HTML
    html_content = generate_wechat_article_html(data)
    
    # 保存HTML
    html_path = 'interview_article.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML文章已生成: {html_path}")
    return html_path

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python pipeline.py <录音稿txt文件路径>")
        sys.exit(1)
    
    txt_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(txt_path):
        print(f"❌ 文件不存在: {txt_path}")
        sys.exit(1)
    
    print("🚀 开始处理pipeline...")
    print(f"📁 输入文件: {txt_path}")
    
    try:
        # 加载配置
        config = load_config()
        prompts = load_prompts()
        
        # 步骤1: 录音稿转逐字稿
        verbatim, verbatim_path = step1_transcript_to_verbatim(txt_path, config, prompts)
        
        # 步骤2: 逐字稿转JSON
        data, json_path = step2_verbatim_to_json(verbatim, config, prompts)
        
        # 步骤3: JSON转HTML
        html_path = step3_json_to_html(data)
        
        print("\n🎉 Pipeline执行完成!")
        print(f"📝 逐字稿: {verbatim_path}")
        print(f"📋 JSON数据: {json_path}")
        print(f"🌐 HTML文章: {html_path}")
        
        # 显示文章信息
        print(f"\n📊 文章信息:")
        print(f"   - 嘉宾: {data.get('guest_name', 'N/A')}")
        print(f"   - 字数: {data.get('word_count', 'N/A')}")
        print(f"   - 预计阅读时间: {data.get('reading_time', 'N/A')}分钟")
        print(f"   - 章节数: {len(data.get('main_sections', []))}")
        
    except Exception as e:
        print(f"❌ Pipeline执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()