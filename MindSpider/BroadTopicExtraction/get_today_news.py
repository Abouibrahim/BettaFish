#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BroadTopicExtraction模块 - newsget和collect
整合newsAPI调用和database存储功能
"""

import sys
import asyncio
import httpx
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from BroadTopicExtraction.database_manager import DatabaseManager
except ImportError as e:
    raise ImportError(f"导入模块failed: {e}")

# newsAPI基础URL
BASE_URL = "https://newsnow.busiyi.world"

# news源中文名称映射
SOURCE_NAMES = {
    "weibo": "Weibo热搜",
    "zhihu": "Zhihu热榜",
    "bilibili-hot-search": "Bilibili热搜",
    "toutiao": "今日头条",
    "douyin": "Douyin热榜",
    "github-trending-today": "GitHub趋势",
    "coolapk": "酷安热榜",
    "tieba": "百度Tieba",
    "wallstreetcn": "华尔街见闻",
    "thepaper": "澎湃news",
    "cls-hot": "财联社",
    "xueqiu": "雪球热榜"
}

class NewsCollector:
    """newscollect器 - 整合API调用和database存储"""
    
    def __init__(self):
        """initializenewscollect器"""
        self.db_manager = DatabaseManager()
        self.supported_sources = list(SOURCE_NAMES.keys())
    
    def close(self):
        """关闭资源"""
        if self.db_manager:
            self.db_manager.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # ==================== newsAPI调用 ====================
    
    async def fetch_news(self, source: str) -> dict:
        """从指定源get最新news"""
        url = f"{BASE_URL}/api/s?id={source}&latest"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Referer": BASE_URL,
            "Connection": "keep-alive",
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                # 解析JSON响应
                data = response.json()
                return {
                    "source": source,
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
        except httpx.TimeoutException:
            return {
                "source": source,
                "status": "timeout",
                "error": f"请求超时: {source}({url})",
                "timestamp": datetime.now().isoformat()
            }
        except httpx.HTTPStatusError as e:
            return {
                "source": source,
                "status": "http_error",
                "error": f"HTTPerror: {source}({url}) - {e.response.status_code}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "source": source,
                "status": "error",
                "error": f"未知error: {source}({url}) - {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_popular_news(self, sources: List[str] = None) -> List[dict]:
        """get热门news"""
        if sources is None:
            sources = list(SOURCE_NAMES.keys())
        
        logger.info(f"正在get {len(sources)} news源的最新content...")
        logger.info("=" * 80)
        
        results = []
        for source in sources:
            source_name = SOURCE_NAMES.get(source, source)
            logger.info(f"正在get {source_name} 的news...")
            result = await self.fetch_news(source)
            results.append(result)
            
            if result["status"] == "success":
                data = result["data"]
                if 'items' in data and isinstance(data['items'], list):
                    count = len(data['items'])
                    logger.info(f"✓ {source_name}: getsuccess，共 {count} news")
                else:
                    logger.info(f"✓ {source_name}: getsuccess")
            else:
                logger.error(f"✗ {source_name}: {result.get('error', 'getfailed')}")
            
            # 避免请求过快
            await asyncio.sleep(0.5)
        
        return results
    
    # ==================== data处理和存储 ====================
    
    async def collect_and_save_news(self, sources: Optional[List[str]] = None) -> Dict:
        """
        collect并save每日热点news
        
        Args:
            sources: 指定的news源列table，Nonetable示使用all支持的源
            
        Returns:
            包含collect结果的字典
        """
        collection_summary_message = ""
        collection_summary_message += "\n开始collect每日热点news...\n"
        collection_summary_message += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        # 选择news源
        if sources is None:
            # 使用all支持的news源
            sources = list(SOURCE_NAMES.keys())
        
        collection_summary_message += f"将从 {len(sources)} news源collectdata:\n"
        for source in sources:
            source_name = SOURCE_NAMES.get(source, source)
            collection_summary_message += f"  - {source_name}\n"
        
        logger.info(collection_summary_message)
        
        try:
            # getnewsdata
            results = await self.get_popular_news(sources)
            
            # 处理结果
            processed_data = self._process_news_results(results)
            
            # save到database（覆盖模式）
            if processed_data['news_list']:
                saved_count = self.db_manager.save_daily_news(
                    processed_data['news_list'], 
                    date.today()
                )
                processed_data['saved_count'] = saved_count
            
            # 打印statistics信息
            self._print_collection_summary(processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.exception(f"collectnewsfailed: {e}")
            return {
                'success': False,
                'error': str(e),
                'news_list': [],
                'total_news': 0
            }
    
    def _process_news_results(self, results: List[Dict]) -> Dict:
        """处理newsget结果"""
        news_list = []
        successful_sources = 0
        total_news = 0
        
        for result in results:
            source = result['source']
            status = result['status']
            
            if status == 'success':
                successful_sources += 1
                data = result['data']
                
                if 'items' in data and isinstance(data['items'], list):
                    source_news_count = len(data['items'])
                    total_news += source_news_count
                    
                    # 处理该源的news
                    for i, item in enumerate(data['items'], 1):
                        processed_news = self._process_news_item(item, source, i)
                        if processed_news:
                            news_list.append(processed_news)
        
        return {
            'success': True,
            'news_list': news_list,
            'successful_sources': successful_sources,
            'total_sources': len(results),
            'total_news': total_news,
            'collection_time': datetime.now().isoformat()
        }
    
    def _process_news_item(self, item: Dict, source: str, rank: int) -> Optional[Dict]:
        """处理单条news"""
        try:
            if isinstance(item, dict):
                title = item.get('title', '无标题').strip()
                url = item.get('url', '')
                
                # 生成newsID
                news_id = f"{source}_{item.get('id', f'rank_{rank}')}"
                
                return {
                    'id': news_id,
                    'title': title,
                    'url': url,
                    'source': source,
                    'rank': rank
                }
            else:
                # 处理字符串类型的news
                title = str(item)[:100] if len(str(item)) > 100 else str(item)
                return {
                    'id': f"{source}_rank_{rank}",
                    'title': title,
                    'url': '',
                    'source': source,
                    'rank': rank
                }
                
        except Exception as e:
            logger.exception(f"处理news项failed: {e}")
            return None
    
    def _print_collection_summary(self, data: Dict):
        """打印collect摘要"""
        collection_summary_message = ""
        collection_summary_message += f"\n总news源: {data['total_sources']}\n"
        collection_summary_message += f"success源数: {data['successful_sources']}\n"
        collection_summary_message += f"总news数: {data['total_news']}\n"
        if 'saved_count' in data:
            collection_summary_message += f"已save数: {data['saved_count']}\n"
        logger.info(collection_summary_message)
    
    def get_today_news(self) -> List[Dict]:
        """get今天的news"""
        try:
            return self.db_manager.get_daily_news(date.today())
        except Exception as e:
            logger.exception(f"get今日newsfailed: {e}")
            return []

async def main():
    """测试newscollect器"""
    logger.info("测试newscollect器...")
    
    async with NewsCollector() as collector:
        # collectnews
        result = await collector.collect_and_save_news(
            sources=["weibo", "zhihu"]  # 测试用，只使用两个源
        )
        
        if result['success']:
            logger.info(f"collectsuccess！共get {result['total_news']} news")
        else:
            logger.error(f"collectfailed: {result.get('error', '未知error')}")

if __name__ == "__main__":
    asyncio.run(main())
