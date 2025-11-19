#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSentimentCrawling模块 - keyword管理器
从BroadTopicExtraction模块getkeyword并分配给不同platform进行crawl
"""

import sys
import json
from datetime import date, timedelta, datetime
from pathlib import Path
from typing import List, Dict, Optional
import random
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import config
except ImportError:
    raise ImportError("unable to导入config.pyconfiguration文件")

from config import settings
from loguru import logger

class KeywordManager:
    """keyword管理器"""
    
    def __init__(self):
        """initializekeyword管理器"""
        self.engine: Engine = None
        self.connect()
    
    def connect(self):
        """connectiondatabase"""
        try:
            dialect = (settings.DB_DIALECT or "mysql").lower()
            if dialect in ("postgresql", "postgres"):
                url = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            else:
                url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset={settings.DB_CHARSET}"
            self.engine = create_engine(url, future=True)
            logger.info(f"keyword管理器successconnection到database: {settings.DB_NAME}")
        except ModuleNotFoundError as e:
            missing: str = str(e)
            if "psycopg" in missing:
                logger.error("databaseconnectionfailed: 未安装PostgreSQL驱动 psycopg。请安装: psycopg[binary]。参考指令：uv pip install psycopg[binary]")
            elif "pymysql" in missing:
                logger.error("databaseconnectionfailed: 未安装MySQL驱动 pymysql。请安装: pymysql。参考指令：uv pip install pymysql")
            else:
                logger.error(f"databaseconnectionfailed(missing驱动): {e}")
            raise
        except Exception as e:
            logger.exception(f"keyword管理器databaseconnectionfailed: {e}")
            raise
    
    def get_latest_keywords(self, target_date: date = None, max_keywords: int = 100) -> List[str]:
        """
        get最新的keyword列table
        
        Args:
            target_date: 目标日期，default为今天
            max_keywords: maximumkeyword数量
        
        Returns:
            keyword列table
        """
        if not target_date:
            target_date = date.today()
        
        logger.info(f"正在get {target_date} 的keyword...")
        
        # 首先尝试get指定日期的keyword
        topics_data = self.get_daily_topics(target_date)
        
        if topics_data and topics_data.get('keywords'):
            keywords = topics_data['keywords']
            logger.info(f"successget {target_date} 的 {len(keywords)} keyword")
            
            # 如果keyword太多，随机选择指定数量
            if len(keywords) > max_keywords:
                keywords = random.sample(keywords, max_keywords)
                logger.info(f"随机选择了 {max_keywords} keyword")
            
            return keywords
        
        # 如果没有当天的keyword，尝试get最近几天的
        logger.info(f"{target_date} 没有keyworddata，尝试get最近的keyword...")
        recent_topics = self.get_recent_topics(days=7)
        
        if recent_topics:
            # 合并最近几天的keyword
            all_keywords = []
            for topic in recent_topics:
                if topic.get('keywords'):
                    all_keywords.extend(topic['keywords'])
            
            # 去重并限制数量
            unique_keywords = list(set(all_keywords))
            if len(unique_keywords) > max_keywords:
                unique_keywords = random.sample(unique_keywords, max_keywords)
            
            logger.info(f"从最近7天的data中get到 {len(unique_keywords)} keyword")
            return unique_keywords
        
        # 如果都没有，返回defaultkeyword
        logger.info("没有找到任何keyworddata，使用defaultkeyword")
        return self._get_default_keywords()
    
    def get_daily_topics(self, extract_date: date = None) -> Optional[Dict]:
        """
        get每日topic分析
        
        Args:
            extract_date: extract日期，default为今天
        
        Returns:
            topic分析data，如果does not exist返回None
        """
        if not extract_date:
            extract_date = date.today()
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM daily_topics WHERE extract_date = :d"),
                    {"d": extract_date},
                ).mappings().first()
            
            if result:
                # 转为可变dict再赋值
                result = dict(result)
                result['keywords'] = json.loads(result['keywords']) if result.get('keywords') else []
                return result
            else:
                return None
                
        except Exception as e:
            logger.exception(f"gettopic分析failed: {e}")
            return None
    
    def get_recent_topics(self, days: int = 7) -> List[Dict]:
        """
        get最近几天的topic分析
        
        Args:
            days: days数
        
        Returns:
            topic分析列table
        """
        try:
            start_date = date.today() - timedelta(days=days)
            with self.engine.connect() as conn:
                results = conn.execute(
                    text(
                        """
                        SELECT * FROM daily_topics 
                        WHERE extract_date >= :start_date
                        ORDER BY extract_date DESC
                        """
                    ),
                    {"start_date": start_date},
                ).mappings().all()
            
            # 转为可变dict列table再处理
            results = [dict(r) for r in results]
            for result in results:
                result['keywords'] = json.loads(result['keywords']) if result.get('keywords') else []
            
            return results
            
        except Exception as e:
            logger.exception(f"get最近topic分析failed: {e}")
            return []
    
    def _get_default_keywords(self) -> List[str]:
        """getdefaultkeyword列table"""
        return [
            "科技", "人工智能", "AI", "编程", "互联网",
            "创业", "投资", "理财", "股市", "经济",
            "教育", "学习", "考试", "大学", "就业",
            "健康", "养生", "运动", "美食", "旅游",
            "时尚", "美妆", "购物", "生活", "家居",
            "电影", "音乐", "游戏", "娱乐", "明星",
            "news", "热点", "社会", "政策", "环保"
        ]
    
    def get_all_keywords_for_platforms(self, platforms: List[str], target_date: date = None, 
                                      max_keywords: int = 100) -> List[str]:
        """
        为allplatformget相同的keyword列table
        
        Args:
            platforms: platform列table
            target_date: 目标日期
            max_keywords: maximumkeyword数量
        
        Returns:
            keyword列table（allplatform共用）
        """
        keywords = self.get_latest_keywords(target_date, max_keywords)
        
        if keywords:
            logger.info(f"为 {len(platforms)} platform准备了相同的 {len(keywords)} keyword")
            logger.info(f"每个keyword将在allplatform上进行crawl")
        
        return keywords
    
    def get_keywords_for_platform(self, platform: str, target_date: date = None, 
                                max_keywords: int = 50) -> List[str]:
        """
        为特定platformgetkeyword（现在allplatform使用相同keyword）
        
        Args:
            platform: platform名称
            target_date: 目标日期
            max_keywords: maximumkeyword数量
        
        Returns:
            keyword列table（与其他platform相同）
        """
        keywords = self.get_latest_keywords(target_date, max_keywords)
        
        logger.info(f"为platform {platform} 准备了 {len(keywords)} keyword（与其他platform相同）")
        return keywords
    
    def _filter_keywords_by_platform(self, keywords: List[str], platform: str) -> List[str]:
        """
        根据platform特性过滤keyword
        
        Args:
            keywords: 原始keyword列table
            platform: platform名称
        
        Returns:
            过滤后的keyword列table
        """
        # platform特性keyword映射（可以根据need调整）
        platform_preferences = {
            'xhs': ['美妆', '时尚', '生活', '美食', '旅游', '购物', '健康', '养生'],
            'dy': ['娱乐', '音乐', '舞蹈', '搞笑', '美食', '生活', '科技', '教育'],
            'ks': ['生活', '搞笑', '农村', '美食', '手工', '音乐', '娱乐'],
            'bili': ['科技', '游戏', '动漫', '学习', '编程', '数码', '科普'],
            'wb': ['热点', 'news', '娱乐', '明星', '社会', '时事', '科技'],
            'tieba': ['游戏', '动漫', '学习', '生活', '兴趣', '讨论'],
            'zhihu': ['知识', '学习', '科技', '职场', '投资', '教育', '思考']
        }
        
        # 如果platform有特定偏好，优先选择相关keyword
        preferred_keywords = platform_preferences.get(platform, [])
        
        if preferred_keywords:
            # 先选择platform偏好的keyword
            filtered = []
            remaining = []
            
            for keyword in keywords:
                if any(pref in keyword for pref in preferred_keywords):
                    filtered.append(keyword)
                else:
                    remaining.append(keyword)
            
            # 如果偏好keyword不够，补充其他keyword
            if len(filtered) < len(keywords) // 2:
                filtered.extend(remaining[:len(keywords) - len(filtered)])
            
            return filtered
        
        # 如果没有特定偏好，返回原keyword
        return keywords
    
    def get_crawling_summary(self, target_date: date = None) -> Dict:
        """
        getcrawltask摘要
        
        Args:
            target_date: 目标日期
        
        Returns:
            crawl摘要信息
        """
        if not target_date:
            target_date = date.today()
        
        topics_data = self.get_daily_topics(target_date)
        
        if topics_data:
            return {
                'date': target_date,
                'keywords_count': len(topics_data.get('keywords', [])),
                'summary': topics_data.get('summary', ''),
                'has_data': True
            }
        else:
            return {
                'date': target_date,
                'keywords_count': 0,
                'summary': '暂无data',
                'has_data': False
            }
    
    def close(self):
        """关闭databaseconnection"""
        if self.engine:
            self.engine.dispose()
            logger.info("keyword管理器databaseconnection已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    # 测试keyword管理器
    with KeywordManager() as km:
        # 测试getkeyword
        keywords = km.get_latest_keywords(max_keywords=20)
        logger.info(f"get到的keyword: {keywords}")
        
        # 测试platform分配
        platforms = ['xhs', 'dy', 'bili']
        distribution = km.distribute_keywords_by_platform(keywords, platforms)
        for platform, kws in distribution.items():
            logger.info(f"{platform}: {kws}")
        
        # 测试crawl摘要
        summary = km.get_crawling_summary()
        logger.info(f"crawl摘要: {summary}")
        
        logger.info("keyword管理器测试completed！")
