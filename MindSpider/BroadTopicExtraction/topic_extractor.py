#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BroadTopicExtraction模块 - topic extraction器
基于DeepSeek直接extractkeyword和生成news总结
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from openai import OpenAI

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import config
    from config import settings
except ImportError:
    raise ImportError("unable to导入settings.pyconfiguration文件")

class TopicExtractor:
    """topic extraction器"""

    def __init__(self):
        """initializetopic extraction器"""
        self.client = OpenAI(
            api_key=settings.MINDSPIDER_API_KEY,
            base_url=settings.MINDSPIDER_BASE_URL
        )
        self.model = settings.MINDSPIDER_MODEL_NAME
    
    def extract_keywords_and_summary(self, news_list: List[Dict], max_keywords: int = 100) -> Tuple[List[str], str]:
        """
        从news列table中extractkeyword和生成总结
        
        Args:
            news_list: news列table
            max_keywords: maximumkeyword数量
            
        Returns:
            (keyword列table, news分析总结)
        """
        if not news_list:
            return [], "今日暂无热点news"
        
        # 构建news摘要文本
        news_text = self._build_news_summary(news_list)
        
        # 构建提示词
        prompt = self._build_analysis_prompt(news_text, max_keywords)
        
        try:
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的news分析师，擅长从热点news中extractkeyword和撰写分析总结。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # 解析返回结果
            result_text = response.choices[0].message.content
            keywords, summary = self._parse_analysis_result(result_text)
            
            print(f"successextract {len(keywords)} keyword并生成news总结")
            return keywords[:max_keywords], summary
            
        except Exception as e:
            print(f"topic extractionfailed: {e}")
            # 返回简单的fallback结果
            fallback_keywords = self._extract_simple_keywords(news_list)
            fallback_summary = f"今日共collect到 {len(news_list)} 热点news，涵盖多个platform的热门topic。"
            return fallback_keywords[:max_keywords], fallback_summary
    
    def _build_news_summary(self, news_list: List[Dict]) -> str:
        """构建news摘要文本"""
        news_items = []
        
        for i, news in enumerate(news_list, 1):
            title = news.get('title', '无标题')
            source = news.get('source_platform', news.get('source', '未知'))
            
            # cleanup标题中的特殊字符
            title = re.sub(r'[#@]', '', title).strip()
            
            news_items.append(f"{i}. 【{source}】{title}")
        
        return "\n".join(news_items)
    
    def _build_analysis_prompt(self, news_text: str, max_keywords: int) -> str:
        """构建分析提示词"""
        news_count = len(news_text.split('\n'))
        
        prompt = f"""
请分析以下{news_count}条今日热点news，completed两个task：

news列table：
{news_text}

task1：extractkeyword（最多{max_keywords}个）
- extract能代table今日热点topic的keyword
- keyword应该适合用于社交媒体platform搜索
- 优先选择热度高、讨论量大的topic
- 避免过于宽泛或过于具体的词汇

task2：撰写news分析总结（150-300字）
- 简要概括今日热点news的主要content
- 指出当前社会关注的重点topic方向
- 分析这些热点反映的社会现象或趋势
- 语言简洁明了，客观中性

请严格按照以下JSON格式输出：
```json
{{
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "summary": "今日news分析总结content..."
}}
```

请直接输出JSON格式的结果，不要包含其他文字说明。
"""
        return prompt
    
    def _parse_analysis_result(self, result_text: str) -> Tuple[List[str], str]:
        """解析分析结果"""
        try:
            # 尝试extractJSON部分
            json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                # 如果没有代码块，尝试直接解析
                json_text = result_text.strip()
            
            # 解析JSON
            data = json.loads(json_text)
            
            keywords = data.get('keywords', [])
            summary = data.get('summary', '')
            
            # 验证和cleanupkeyword
            clean_keywords = []
            for keyword in keywords:
                keyword = str(keyword).strip()
                if keyword and len(keyword) > 1 and keyword not in clean_keywords:
                    clean_keywords.append(keyword)
            
            # 验证总结
            if not summary or len(summary.strip()) < 10:
                summary = "今日热点news涵盖多个领域，反映了当前社会的多元化关注点。"
            
            return clean_keywords, summary.strip()
            
        except json.JSONDecodeError as e:
            print(f"解析JSONfailed: {e}")
            print(f"原始返回: {result_text}")
            
            # 尝试手动解析
            return self._manual_parse_result(result_text)
        
        except Exception as e:
            print(f"处理分析结果failed: {e}")
            return [], "分析结果处理failed，请稍后重试。"
    
    def _manual_parse_result(self, text: str) -> Tuple[List[str], str]:
        """手动解析结果（当JSON解析failed时的后备方案）"""
        print("尝试手动解析结果...")
        
        keywords = []
        summary = ""
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 寻找keyword
            if 'keyword' in line or 'keywords' in line.lower():
                # extractkeyword
                keyword_match = re.findall(r'[""](.*?)["""]', line)
                if keyword_match:
                    keywords.extend(keyword_match)
                else:
                    # 尝试其他分隔符
                    parts = re.split(r'[,，、]', line)
                    for part in parts:
                        clean_part = re.sub(r'[keyword：:keywords\[\]"]', '', part).strip()
                        if clean_part and len(clean_part) > 1:
                            keywords.append(clean_part)
            
            # 寻找总结
            elif '总结' in line or '分析' in line or 'summary' in line.lower():
                if '：' in line or ':' in line:
                    summary = line.split('：')[-1].split(':')[-1].strip()
            
            # 如果这一行看起来像总结content
            elif len(line) > 50 and ('今日' in line or '热点' in line or 'news' in line):
                if not summary:
                    summary = line
        
        # cleanupkeyword
        clean_keywords = []
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and len(keyword) > 1 and keyword not in clean_keywords:
                clean_keywords.append(keyword)
        
        # 如果没有找到总结，生成一个简单的
        if not summary:
            summary = "今日热点newscontent丰富，涵盖了社会各个层面的关注点。"
        
        return clean_keywords[:max_keywords], summary
    
    def _extract_simple_keywords(self, news_list: List[Dict]) -> List[str]:
        """简单keywordextract（fallback方案）"""
        keywords = []
        
        for news in news_list:
            title = news.get('title', '')
            
            # 简单的keywordextract
            # 移除常见的无意义词汇
            title_clean = re.sub(r'[#@【】\[\]()（）]', ' ', title)
            words = title_clean.split()
            
            for word in words:
                word = word.strip()
                if (len(word) > 1 and 
                    word not in ['的', '了', '在', '和', '与', '或', '但', '是', '有', '被', '将', '已', '正在'] and
                    word not in keywords):
                    keywords.append(word)
        
        return keywords[:10]
    
    def get_search_keywords(self, keywords: List[str], limit: int = 10) -> List[str]:
        """
        get用于搜索的keyword
        
        Args:
            keywords: keyword列table
            limit: 限制数量
            
        Returns:
            适合搜索的keyword列table
        """
        # 过滤和优化keyword
        search_keywords = []
        
        for keyword in keywords:
            keyword = str(keyword).strip()
            
            # 过滤条件
            if (len(keyword) > 1 and 
                len(keyword) < 20 and  # 不能太长
                keyword not in search_keywords and
                not keyword.isdigit() and  # 不是纯数字
                not re.match(r'^[a-zA-Z]+$', keyword)):  # 不是纯英文（除非是专有名词）
                
                search_keywords.append(keyword)
        
        return search_keywords[:limit]

if __name__ == "__main__":
    # 测试topic extraction器
    extractor = TopicExtractor()
    
    # 模拟newsdata
    test_news = [
        {"title": "AI技术发展迅速", "source_platform": "科技news"},
        {"title": "股市行情分析", "source_platform": "财经news"},
        {"title": "明星最新动态", "source_platform": "娱乐news"}
    ]
    
    keywords, summary = extractor.extract_keywords_and_summary(test_news)
    
    print(f"extract的keyword: {keywords}")
    print(f"news总结: {summary}")
    
    search_keywords = extractor.get_search_keywords(keywords)
    print(f"搜索keyword: {search_keywords}")
