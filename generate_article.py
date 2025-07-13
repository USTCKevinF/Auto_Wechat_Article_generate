#!/usr/bin/env python3
"""
微信公众号文章HTML生成器
将结构化的访谈数据转换为微信公众号文章格式的HTML
"""

import html
import re
import json
import os
from datetime import datetime


def process_text_with_emphasis(text):
    """
    处理文本中的加粗标记
    将需要强调的文本转换为加粗格式
    """
    # 需要加粗的关键短语列表
    emphasis_patterns = [
    ]
    
    # 应用加粗标记
    for pattern in emphasis_patterns:
        if pattern in text and f'<span textstyle="" style="font-weight: bold;">{pattern}</span>' not in text:
            text = text.replace(pattern, f'<span textstyle="" style="font-weight: bold;">{pattern}</span>')
    
    return text


def escape_html(text):
    """安全地转义HTML特殊字符"""
    return html.escape(text)


def format_guest_intro(intro_text):
    """格式化嘉宾介绍，保留换行"""
    return intro_text.replace('\n', '<br>')


def generate_topics_summary(topics):
    """生成主题摘要HTML"""
    summary_items = []
    for topic in topics:
        summary_items.append(f'• {topic}')
    return '<br>'.join(summary_items)


def generate_section_html(section, data):
    """生成单个章节的HTML"""
    section_html = f'''
                    <section
                        style="padding-right: 20px;padding-left: 20px;outline: 0px;caret-color: rgba(0, 0, 0, 0.9);font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;font-size: 17px;letter-spacing: 0.544px;line-height: 0.8;visibility: visible;">
                        <section
                            style="outline: 0px;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);font-size: 16px;color: rgb(62, 62, 62);text-align: center;text-indent: 0em;line-height: 1.6em;margin-top: 8px;margin-bottom: 24px;">
                            <span
                                style="outline: 0px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;color: rgb(44, 42, 143);font-size: 24px;font-weight: 700;text-decoration: underline;letter-spacing: 0.5px;"><span
                                    leaf="">{section['id']} &nbsp;{section['title']}</span></span></section>'''
    
    # 如果有副标题，添加副标题部分
    if section.get('sub_sections'):
        first_subtitle = section['sub_sections'][0].get('subtitle', '')
        if first_subtitle:
            section_html += f'''
                        <section
                            style="outline: 0px;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);font-size: 16px;color: rgb(62, 62, 62);text-align: center;text-indent: 0em;line-height: 1.6em;margin-top: 8px;margin-bottom: 24px;">
                            <span
                                style="outline: 0px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;font-size: 20px;font-weight: 700;letter-spacing: 0.5px;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;text-indent: 0em;"><span
                                    leaf="">"{first_subtitle}"</span></span></section>'''
    
    section_html += '''
                    </section>'''
    
    # 格式化章节HTML
    section_html = section_html.format(
        section_id=section['id'],
        section_title=section['title']
    )
    
    # 生成问答内容
    qa_html = ''
    for sub_section in section['sub_sections']:
        # 问题
        question_html = f'''
                    <section
                        style="margin-bottom: 24px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;letter-spacing: 0.578px;visibility: visible;margin-top: 8px;">
                        <span leaf=""
                            style="outline: 0px;font-size: 15px;text-indent: 0em;color: rgb(0, 0, 0);letter-spacing: 0.5px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;"><span
                                textstyle=""
                                style="color: rgb(171, 25, 66);font-weight: bold;">蜗壳进阶联盟：{sub_section['question']}</span></span>
                    </section>'''
        
        qa_html += question_html
        
        # 回答（处理多段落）
        answer_paragraphs = sub_section['answer'].split('\n')
        para = answer_paragraphs[0]
        if para.strip():
            # 处理带有说话人的段落
            speaker = f"{data['guest_name']}："
            content = process_text_with_emphasis(para)
            
            answer_html = f'''
            <section
                style="box-sizing: border-box;font-style: normal;font-weight: 400;text-align: justify;font-size: 16px;color: rgb(62, 62, 62);"
                data-pm-slice="0 0 []">
                <section style="color: rgb(0, 0, 0);font-size: 15px;box-sizing: border-box;">
                    <p style="white-space: normal;margin: 8px 0px 24px;padding: 0px;box-sizing: border-box;">
                        <strong style="box-sizing: border-box;"><span leaf="">{speaker}</span></strong><span
                            leaf="">{content}</span>
                    </p>
                </section>
            </section>'''
            qa_html += answer_html
        for para in answer_paragraphs[1:]:
            content = process_text_with_emphasis(para)
            answer_html = f'''
            <section
                style="box-sizing: border-box;font-style: normal;font-weight: 400;text-align: justify;font-size: 16px;color: rgb(62, 62, 62);"
                data-pm-slice="0 0 []">
                <section style="color: rgb(0, 0, 0);font-size: 15px;box-sizing: border-box;">
                    <p style="white-space: normal;margin: 8px 0px 24px;padding: 0px;box-sizing: border-box;">
                        <span leaf="">{content}</span>
                    </p>
                </section>
            </section>'''
            qa_html += answer_html

    return section_html + qa_html


def generate_wechat_article_html(data):
    """
    主函数：根据结构化数据生成微信公众号文章HTML
    
    Args:
        data: 包含文章信息的字典
    
    Returns:
        str: 生成的HTML字符串
    """
    
    # HTML模板开头部分（保持原有的样式和结构）
    html_template = '''<div class="rich_media_content js_underline_content autoTypeSetting24psection fix_apple_default_style" id="js_content"
    style="">
    <section
        style="margin-bottom: 0px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;letter-spacing: 0.578px;font-size: 16px;visibility: visible;"
        data-pm-slice="0 0 []">
        <section style="padding-right: 10px;padding-left: 10px;outline: 0px;line-height: 1.6;visibility: visible;">
            <section style="outline: 0px;visibility: visible;">
                <section style="margin-top: 8px;outline: 0px;visibility: visible;margin-bottom: 24px;">
                    <section
                        style="margin-top: 10px;margin-bottom: 10px;outline: 0px;text-align: left;justify-content: flex-start;display: flex;flex-flow: row;visibility: visible;">
                        <section
                            style="outline: 0px;display: inline-block;vertical-align: bottom;width: 100.438px;flex: 0 0 auto;height: auto;align-self: flex-end;visibility: visible;">
                            <section
                                style="outline: 0px;line-height: 0;transform: translate3d(10px, 0px, 0px);visibility: visible;">
                                <span leaf="" style="visibility: visible;"><br style="visibility: visible;"></span>
                                <section
                                    style="outline: 0px;vertical-align: middle;display: inline-block;line-height: 0;width: 74.3203px;height: auto;border-top-left-radius: 647px;border-top-right-radius: 647px;border-bottom-left-radius: 647px;overflow: hidden;visibility: visible;"
                                    nodeleaf=""><img
                                        data-src="https://mmbiz.qpic.cn/mmbiz_png/twW3euR3BMLsyBeyHbW3q5Uc4FG2ktl4MtsRbfzMks2ZYWELA3KH47IV3Xod2f6obGoGyTsI64U1vUiaUgK1VibQ/640?wx_fmt=other&amp;from=appmsg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1"
                                        class="rich_pages wxw-img" data-ratio="1.0046296296296295" data-s="300,640"
                                        data-type="png" data-w="1080"
                                        style="outline: 0px; vertical-align: middle; width: 74.3125px !important; visibility: visible !important; height: auto !important;"
                                        data-cropselx1="0" data-cropselx2="75" data-cropsely1="0" data-cropsely2="75"
                                        data-backw="74" data-backh="75" data-imgfileid="100000981"
                                        data-original-style="outline: 0px;vertical-align: middle;width: 74.3125px !important;visibility: visible !important;height: auto !important;"
                                        data-index="1"
                                        src="https://mmbiz.qpic.cn/mmbiz_png/twW3euR3BMLsyBeyHbW3q5Uc4FG2ktl4MtsRbfzMks2ZYWELA3KH47IV3Xod2f6obGoGyTsI64U1vUiaUgK1VibQ/640?wx_fmt=other&amp;from=appmsg&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1&amp;tp=webp"
                                        _width="74.3125px" alt="Image" data-report-img-idx="5" data-fail="0"></section>
                            </section>
                        </section>
                        <section
                            style="outline: 0px;display: inline-block;vertical-align: bottom;width: auto;align-self: flex-end;flex: 100 100 0%;height: auto;visibility: visible;">
                            <section
                                style="outline: 0px;text-align: justify;font-size: 12px;color: rgb(141, 141, 141);visibility: visible;">
                                <p style="outline: 0px;visibility: visible;"><span
                                        style="outline: 0px;letter-spacing: 0.5px;visibility: visible;"><strong
                                            style="outline: 0px;visibility: visible;"><span leaf=""
                                                style="visibility: visible;">专注打破大学信息差</span></strong></span></p>
                            </section>
                            <section style="margin-top: 3px;margin-bottom: 3px;outline: 0px;visibility: visible;">
                                <section
                                    style="outline: 0px;background-color: rgb(141, 141, 141);height: 1px;visibility: visible;">
                                    <svg viewBox="0 0 1 1"
                                        style="float: left;line-height: 0;width: 0px;vertical-align: top;visibility: visible;"></svg>
                                </section>
                            </section>
                            <section
                                style="margin-top: 7px;margin-bottom: 7px;outline: 0px;justify-content: flex-start;display: flex;flex-flow: row;visibility: visible;">
                                <section
                                    style="padding-right: 4px;padding-left: 4px;outline: 0px;display: inline-block;vertical-align: bottom;width: auto;align-self: flex-end;flex: 0 0 auto;background-color: rgb(92, 170, 233);min-width: 5%;height: auto;visibility: visible;">
                                    <section style="outline: 0px;text-align: center;visibility: visible;">
                                        <section
                                            style="outline: 0px;font-size: 17px;color: rgb(255, 255, 255);visibility: visible;">
                                            <p style="outline: 0px;visibility: visible;"><span
                                                    style="outline: 0px;letter-spacing: 0.5px;visibility: visible;"><strong
                                                        style="outline: 0px;visibility: visible;"><span leaf=""
                                                            style="visibility: visible;">点击蓝字</span></strong></span></p>
                                        </section>
                                    </section>
                                </section>
                                <section
                                    style="padding-left: 5px;outline: 0px;display: inline-block;vertical-align: bottom;width: auto;min-width: 5%;flex: 0 0 auto;height: auto;align-self: flex-end;visibility: visible;">
                                    <section style="outline: 0px;visibility: visible;">
                                        <section style="outline: 0px;font-size: 17px;visibility: visible;">
                                            <p style="outline: 0px;visibility: visible;"><span
                                                    style="outline: 0px;letter-spacing: 0.5px;visibility: visible;"><strong
                                                        style="outline: 0px;visibility: visible;"><span leaf=""
                                                            style="visibility: visible;">关注我们</span></strong></span></p>
                                        </section>
                                    </section>
                                </section>
                            </section>
                        </section>
                    </section>
                </section>
                <section style="text-align: center; margin-bottom: 24px; visibility: visible;"><span leaf=""
                        style="visibility: visible;"><img
                            data-src="https://mmbiz.qpic.cn/mmbiz_png/twW3euR3BMIlU2KI3CgvzhkAYcwQw5ctw8IvZAq0l1Nl1QQyHcMSAKDqgduNY2TqO1YJd41YrHTfMTU9C1Pw3A/640?wx_fmt=png&amp;from=appmsg"
                            class="rich_pages wxw-img" data-ratio="0.512962962962963" data-s="300,640" data-type="png"
                            data-w="1080"
                            style="vertical-align: middle; max-width: 100%; width: 657px !important; box-sizing: border-box; height: auto !important; visibility: visible !important;"
                            data-imgfileid="100001361"
                            data-original-style="vertical-align: middle;max-width: 100%;width: 100%;box-sizing: border-box;height: auto !important;"
                            data-index="2"
                            src="https://mmbiz.qpic.cn/mmbiz_png/twW3euR3BMIlU2KI3CgvzhkAYcwQw5ctw8IvZAq0l1Nl1QQyHcMSAKDqgduNY2TqO1YJd41YrHTfMTU9C1Pw3A/640?wx_fmt=png&amp;from=appmsg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1"
                            _width="100%" alt="Image" data-report-img-idx="4" data-fail="0"></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: left;text-indent: 0em;line-height: 1.6em;visibility: visible;margin-bottom: 24px;">
                    <span style="outline: 0px;letter-spacing: 0.5px;visibility: visible;"><span
                            style="outline: 0px;color: rgb(106, 106, 106);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;font-size: 14px;visibility: visible;"><span
                                leaf="" style="visibility: visible;">长文预警，本文共</span></span><span
                            style="outline: 0px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;font-size: 14px;color: rgb(44, 42, 143);visibility: visible;"><strong
                                style="outline: 0px;visibility: visible;"><span leaf=""
                                    style="visibility: visible;">{word_count}</span></strong></span><span
                            style="outline: 0px;color: rgb(106, 106, 106);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;font-size: 14px;visibility: visible;"><span
                                leaf="" style="visibility: visible;">字，预计阅读时间</span></span><span
                            style="outline: 0px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;font-size: 14px;color: rgb(44, 42, 143);visibility: visible;"><strong
                                style="outline: 0px;visibility: visible;"><span leaf=""
                                    style="visibility: visible;">{reading_time}</span></strong></span><span
                            style="outline: 0px;color: rgb(106, 106, 106);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;font-size: 14px;visibility: visible;"><span
                                leaf="" style="visibility: visible;">分钟</span></span></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: normal;white-space-collapse: preserve;orphans: 4;caret-color: rgb(0, 122, 255);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;text-align: start;text-indent: 0em;line-height: 1.75em;visibility: visible;margin-bottom: 24px;">
                    <span
                        style="outline: 0px;color: rgb(106, 106, 106);letter-spacing: 0.5px;font-size: 15px;visibility: visible;"><span
                            leaf=""
                            style="visibility: visible;">「对话」是蜗壳进阶联盟推出的系列深度访谈栏目，我们邀请并采访了科大的优秀前辈，他们在科大的大学生活当中走过了弯路，品尝过挫折，获得过成就。我们希望通过深度对话的方式展现他们人生生涯当中的种种历程与个人选择，希望通过这种对话的方式，前辈们的经历可以为科大的后辈们照亮更多的前路。</span></span>
                </section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: normal;white-space-collapse: preserve;orphans: 4;caret-color: rgb(0, 122, 255);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;text-align: start;text-indent: 0em;line-height: 1.75em;visibility: visible;margin-bottom: 24px;">
                    <span
                        style="outline: 0px;color: rgb(106, 106, 106);letter-spacing: 0.5px;font-size: 15px;visibility: visible;"><span
                            leaf="">{guest_intro}</span></span>
                </section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: left;text-indent: 0em;line-height: 1.6em;margin-bottom: 24px;">
                    <span style="outline: 0px;letter-spacing: 0.5px;"><strong
                            style="outline: 0px;color: rgb(171, 25, 66);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;font-size: 14px;letter-spacing: normal;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;"><span
                                leaf="">本文由蜗壳进阶联盟原创 未经允许 不得转载</span></strong></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;">
                    <span leaf=""><br></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;">
                    <span leaf=""><br></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;">
                    <span style="outline: 0px;letter-spacing: 0.5px;"><strong style="outline: 0px;"><span leaf="">采访、编辑
                                | {interviewer}</span></strong></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;">
                    <span style="outline: 0px;letter-spacing: 0.5px;"><strong style="outline: 0px;"><span leaf="">线下承办 |
                                {proofreader}</span></strong></span></section>
                <section
                    style="margin-top: 8px;outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;">
                    <span style="outline: 0px;letter-spacing: 0.5px;"><strong style="outline: 0px;"><span
                                leaf=""><br></span></strong></span></section>
                <p
                    style="outline: 0px;letter-spacing: 0.578px;text-align: right;text-indent: 0em;line-height: 1.6em;margin-top: 8px;">
                    <span style="outline: 0px;letter-spacing: 0.5px;"><strong style="outline: 0px;"><span
                                leaf=""><br></span></strong></span></p>
            </section>
            <p
                style="outline: 0px;color: rgb(62, 62, 62);background-color: rgb(255, 255, 255);visibility: visible;margin-top: 8px;">
                <span leaf=""><br></span></p>
            <p
                style="margin-bottom: 8px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;text-indent: 0em;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);color: rgb(62, 62, 62);text-align: center;line-height: 1.6em;margin-top: 8px;">
                <span
                    style="outline: 0px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;color: rgb(44, 42, 143);font-size: 24px;font-weight: 700;text-decoration: underline;letter-spacing: 0.5px;"><span
                        leaf="">&nbsp;主题摘要&nbsp;</span></span></p>
            <p
                style="margin-bottom: 8px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;text-indent: 0em;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);color: rgb(62, 62, 62);text-align: center;line-height: 1.6em;margin-top: 8px;">
                <span leaf=""><br></span></p>
            <section
                style="margin-bottom: 16px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;text-indent: 0em;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);color: rgb(62, 62, 62);text-align: center;line-height: 1.6em;margin-top: 8px;">
                <span leaf=""><span textstyle="" style="font-weight: bold;">{topics_summary}</span></span></section>
            <p
                style="margin-top: 8px;margin-bottom: 16px;outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;text-indent: 0em;letter-spacing: 0.578px;background-color: rgb(255, 255, 255);color: rgb(62, 62, 62);text-align: center;line-height: 1.6em;">
                <strong style="outline: 0px;"><span leaf="">...</span></strong></p>
            <section
                style="outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;letter-spacing: 0.544px;visibility: visible;">
                <section powered-by="xiumi.us" style="outline: 0px;visibility: visible;">
                    <section
                        style="outline: 0px;font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;letter-spacing: 0.578px;visibility: visible;margin-top: 8px;margin-bottom: 24px;">
                        <span leaf=""
                            style="outline: 0px;font-size: 15px;text-indent: 0em;color: rgb(0, 0, 0);letter-spacing: 0.5px;font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);white-space-collapse: preserve;"><br></span>
                    </section>'''
    
    # 处理数据
    guest_intro_html = format_guest_intro(data['guest_intro'])
    topics_summary = generate_topics_summary(data['topics'])
    
    # 填充基础信息
    html_content = html_template.format(
        word_count=data['word_count'],
        reading_time=data['reading_time'],
        guest_intro=guest_intro_html,
        interviewer=data['interviewer'],
        proofreader=data['proofreader'],
        topics_summary=topics_summary
    )
    
    # 生成各章节内容
    for section in data['main_sections']:
        html_content += generate_section_html(section, data)
    
    # HTML结尾部分
    html_footer = '''
                </section>
            </section>
        </section>
        <section style="padding-right: 10px;padding-left: 10px;outline: 0px;line-height: 1.6;visibility: visible;">
            <section style="outline: 0px;visibility: visible;">
                <p
                    style="margin: 8px 8px 24px;outline: 0px;letter-spacing: 0.578px;text-indent: 0em;line-height: 1.6em;">
                    <span leaf=""><br></span></p>
                <p
                    style="margin: 8px 8px 24px;outline: 0px;letter-spacing: 0.578px;text-indent: 0em;line-height: 1.6em;">
                    <span
                        style="outline: 0px;font-size: 15px;text-indent: 0em;white-space-collapse: preserve;letter-spacing: 0.5px;color: rgb(0, 0, 0);font-family: &quot;Open Sans&quot;, &quot;Clear Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, &quot;Segoe UI Emoji&quot;, sans-serif;orphans: 4;caret-color: rgb(0, 122, 255);"><strong
                            style="outline: 0px;color: rgb(171, 25, 66);background-color: rgb(255, 255, 255);"><span
                                leaf=""><img
                                    data-src="https://mmbiz.qpic.cn/mmbiz_jpg/twW3euR3BMJaBWaicHQq4icagaiageoklRIx6gcXphTa66cohxibYDMvuWfJArLV6HTFoKT4Aibqia0QcnZbnqhaHF5g/640?wx_fmt=jpeg"
                                    class="rich_pages wxw-img js_img_placeholder wx_img_placeholder"
                                    data-ratio="0.44722222222222224" data-s="300,640" data-type="png" data-w="1080"
                                    style="caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); font-weight: 400; letter-spacing: normal; text-align: start; white-space-collapse: collapse; outline: 0px; visibility: visible !important; width: 579px !important; height: 258.942px !important;"
                                    data-croporisrc="https://mmbiz.qpic.cn/mmbiz_png/twW3euR3BMIMkk15K4JCJKHQWSxSeEqicOju9uRCAvQ8C9aMibgKt4VE48VDHMTYjhoOOM4ciaMOLzDCZyEsytSjg/640?wx_fmt=other&amp;from=appmsg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1"
                                    data-cropx2="1080" data-cropy2="483.1088082901554" data-imgfileid="100000983"
                                    data-original-style="caret-color: rgb(0, 0, 0);color: rgb(0, 0, 0);font-weight: 400;letter-spacing: normal;text-align: start;white-space-collapse: collapse;outline: 0px;width: 579px;visibility: visible !important;height: auto !important;"
                                    data-index="7"
                                    src="data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E"
                                    _width="579px" alt="Image"></span></strong></span></p>
                <p><span leaf=""><br></span></p>
            </section>
        </section>
    </section>
    <p style="display: none;"><mp-style-type data-value="3"></mp-style-type></p>
</div>'''
    
    html_content += html_footer
    
    return html_content


def read_data_from_file(filename):
    """从文件读取数据"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # 简单解析 - 假设文件中有 simple_data = {...} 的格式
            if 'simple_data = {' in content:
                start = content.find('simple_data = {') + len('simple_data = ')
                # 找到对应的结束大括号
                brace_count = 0
                end = start
                for i in range(start, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                
                data_str = content[start:end]
                # 使用 ast.literal_eval 安全地解析Python字典
                import ast
                return ast.literal_eval(data_str)
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None


def main():
    """主函数"""
    simple_data = None
    # 新增逻辑：如果没有准备好simple_data，则读取json文件
    if not simple_data:
        try:
            with open('data_example.json', 'r', encoding='utf-8') as f:
                simple_data = json.load(f)
            print("已从 data_example.json 读取数据。")
        except Exception as e:
            print(f"❌ 无法读取 data_example.json: {e}")
            return

    if simple_data:
        print("正在生成微信公众号文章HTML...")
        html_output = generate_wechat_article_html(simple_data)
        
        # 保存到文件
        output_filename = 'wechat_article_generated.html'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✅ HTML文件已成功生成: {output_filename}")
        print(f"📊 文件大小: {len(html_output):,} 字符")
        print(f"📝 文章信息:")
        print(f"   - 嘉宾: {simple_data['guest_name']}")
        print(f"   - 字数: {simple_data['word_count']}")
        print(f"   - 预计阅读时间: {simple_data['reading_time']}分钟")
        print(f"   - 章节数: {len(simple_data['main_sections'])}")
    else:
        print("❌ 无法读取数据")


if __name__ == "__main__":
    main()