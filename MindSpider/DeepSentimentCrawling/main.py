#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSentimentCrawling模块 - 主工作流程
基于BroadTopicExtractionextract的topic进行全platformkeywordcrawl
"""

import sys
import argparse
from datetime import date, datetime
from pathlib import Path
from typing import List, Dict

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from keyword_manager import KeywordManager
from platform_crawler import PlatformCrawler

class DeepSentimentCrawling:
    """深度sentiment crawling主工作流程"""
    
    def __init__(self):
        """initialize深度sentiment crawling"""
        self.keyword_manager = KeywordManager()
        self.platform_crawler = PlatformCrawler()
        self.supported_platforms = ['xhs', 'dy', 'ks', 'bili', 'wb', 'tieba', 'zhihu']
    
    def run_daily_crawling(self, target_date: date = None, platforms: List[str] = None, 
                          max_keywords_per_platform: int = 50, 
                          max_notes_per_platform: int = 50,
                          login_type: str = "qrcode") -> Dict:
        """
        execute每日crawltask
        
        Args:
            target_date: 目标日期，default为今天
            platforms: 要crawl的platform列table，default为all支持的platform
            max_keywords_per_platform: 每个platformmaximumkeyword数量
            max_notes_per_platform: 每个platformmaximumcrawlcontent数量
            login_type: 登录方式
        
        Returns:
            crawl结果statistics
        """
        if not target_date:
            target_date = date.today()
        
        if not platforms:
            platforms = self.supported_platforms
        
        print(f"🚀 开始execute {target_date} 的深度sentiment crawlingtask")
        print(f"目标platform: {platforms}")
        
        # 1. getkeyword摘要
        summary = self.keyword_manager.get_crawling_summary(target_date)
        print(f"📊 keyword摘要: {summary}")
        
        if not summary['has_data']:
            print("⚠️ 没有找到topicdata，unable to进行crawl")
            return {"success": False, "error": "没有topicdata"}
        
        # 2. getkeyword（不分配，allplatform使用相同keyword）
        print(f"\n📝 getkeyword...")
        keywords = self.keyword_manager.get_latest_keywords(target_date, max_keywords_per_platform)
        
        if not keywords:
            print("⚠️ 没有找到keyword，unable to进行crawl")
            return {"success": False, "error": "没有keyword"}
        
        print(f"   get到 {len(keywords)} keyword")
        print(f"   将在 {len(platforms)} platform上crawl每个keyword")
        print(f"   总crawltask: {len(keywords)} × {len(platforms)} = {len(keywords) * len(platforms)}")
        
        # 3. execute全platformkeywordcrawl
        print(f"\n🔄 开始全platformkeywordcrawl...")
        crawl_results = self.platform_crawler.run_multi_platform_crawl_by_keywords(
            keywords, platforms, login_type, max_notes_per_platform
        )
        
        # 4. 生成最终报告
        final_report = {
            "date": target_date.isoformat(),
            "summary": summary,
            "crawl_results": crawl_results,
            "success": crawl_results["successful_tasks"] > 0
        }
        
        print(f"\n✅ 深度sentiment crawlingtaskcompleted!")
        print(f"   日期: {target_date}")
        print(f"   successtask: {crawl_results['successful_tasks']}/{crawl_results['total_tasks']}")
        print(f"   总keyword: {crawl_results['total_keywords']} ")
        print(f"   总platform: {crawl_results['total_platforms']} ")
        print(f"   总content: {crawl_results['total_notes']} ")
        
        return final_report
    
    def run_platform_crawling(self, platform: str, target_date: date = None,
                             max_keywords: int = 50, max_notes: int = 50,
                             login_type: str = "qrcode") -> Dict:
        """
        execute单个platform的crawltask
        
        Args:
            platform: platform名称
            target_date: 目标日期
            max_keywords: maximumkeyword数量
            max_notes: maximumcrawlcontent数量
            login_type: 登录方式
        
        Returns:
            crawl结果
        """
        if platform not in self.supported_platforms:
            raise ValueError(f"不支持的platform: {platform}")
        
        if not target_date:
            target_date = date.today()
        
        print(f"🎯 开始execute {platform} platform的crawltask ({target_date})")
        
        # getkeyword
        keywords = self.keyword_manager.get_keywords_for_platform(
            platform, target_date, max_keywords
        )
        
        if not keywords:
            print(f"⚠️ 没有找到 {platform} platform的keyword")
            return {"success": False, "error": "没有keyword"}
        
        print(f"📝 准备crawl {len(keywords)} keyword")
        
        # executecrawl
        result = self.platform_crawler.run_crawler(
            platform, keywords, login_type, max_notes
        )
        
        return result
    
    def list_available_topics(self, days: int = 7):
        """列出最近可用的topic"""
        print(f"📋 最近 {days} days的topicdata:")
        
        recent_topics = self.keyword_manager.db_manager.get_recent_topics(days)
        
        if not recent_topics:
            print("   暂无topicdata")
            return
        
        for topic in recent_topics:
            extract_date = topic['extract_date']
            keywords_count = len(topic.get('keywords', []))
            summary_preview = topic.get('summary', '')[:100] + "..." if len(topic.get('summary', '')) > 100 else topic.get('summary', '')
            
            print(f"   📅 {extract_date}: {keywords_count} keyword")
            print(f"      摘要: {summary_preview}")
            print()
    
    def show_platform_guide(self):
        """showplatform使用指南"""
        print("🔧 platformcrawl指南:")
        print()
        
        platform_info = {
            'xhs': 'Xiaohongshu - 美妆、生活、时尚content为主',
            'dy': 'Douyin - 短视频、娱乐、生活content',
            'ks': 'Kuaishou - 生活、娱乐、农村题材content',
            'bili': 'Bilibili - 科技、学习、游戏、动漫content',
            'wb': 'Weibo - 热点news、明星、社会topic',
            'tieba': '百度Tieba - 兴趣讨论、游戏、学习',
            'zhihu': 'Zhihu - 知识问答、深度讨论'
        }
        
        for platform, desc in platform_info.items():
            print(f"   {platform}: {desc}")
        
        print()
        print("💡 使用建议:")
        print("   1. 首次使用need扫码登录各platform")
        print("   2. 建议先测试单个platform，确认登录normal")
        print("   3. crawl数量不宜过大，避免被限制")
        print("   4. 可以使用 --test 模式进行小规模测试")
    
    def close(self):
        """关闭资源"""
        if self.keyword_manager:
            self.keyword_manager.close()

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="DeepSentimentCrawling - 基于topic的深度sentiment crawling")
    
    # 基本参数
    parser.add_argument("--date", type=str, help="目标日期 (YYYY-MM-DD)，default为今天")
    parser.add_argument("--platform", type=str, choices=['xhs', 'dy', 'ks', 'bili', 'wb', 'tieba', 'zhihu'], 
                       help="指定单个platform进行crawl")
    parser.add_argument("--platforms", type=str, nargs='+', 
                       choices=['xhs', 'dy', 'ks', 'bili', 'wb', 'tieba', 'zhihu'],
                       help="指定多个platform进行crawl")
    
    # crawl参数
    parser.add_argument("--max-keywords", type=int, default=50, 
                       help="每个platformmaximumkeyword数量 (default: 50)")
    parser.add_argument("--max-notes", type=int, default=50,
                       help="每个platformmaximumcrawlcontent数量 (default: 50)")
    parser.add_argument("--login-type", type=str, choices=['qrcode', 'phone', 'cookie'], 
                       default='qrcode', help="登录方式 (default: qrcode)")
    
    # 功能参数
    parser.add_argument("--list-topics", action="store_true", help="列出最近的topicdata")
    parser.add_argument("--days", type=int, default=7, help="查看最近几天的topic (default: 7)")
    parser.add_argument("--guide", action="store_true", help="showplatform使用指南")
    parser.add_argument("--test", action="store_true", help="测试模式 (少量data)")
    
    args = parser.parse_args()
    
    # 解析日期
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("❌ 日期格式error，请使用 YYYY-MM-DD 格式")
            return
    
    # 创建crawl实例
    crawler = DeepSentimentCrawling()
    
    try:
        # show指南
        if args.guide:
            crawler.show_platform_guide()
            return
        
        # 列出topic
        if args.list_topics:
            crawler.list_available_topics(args.days)
            return
        
        # 测试模式调整参数
        if args.test:
            args.max_keywords = min(args.max_keywords, 10)
            args.max_notes = min(args.max_notes, 10)
            print("测试模式：限制keyword和content数量")
        
        # 单platformcrawl
        if args.platform:
            result = crawler.run_platform_crawling(
                args.platform, target_date, args.max_keywords, 
                args.max_notes, args.login_type
            )
            
            if result['success']:
                print(f"\n{args.platform} crawlsuccess！")
            else:
                print(f"\n{args.platform} crawlfailed: {result.get('error', '未知error')}")
            
            return
        
        # 多platformcrawl
        platforms = args.platforms if args.platforms else None
        result = crawler.run_daily_crawling(
            target_date, platforms, args.max_keywords, 
            args.max_notes, args.login_type
        )
        
        if result['success']:
            print(f"\n多platformcrawltaskcompleted！")
        else:
            print(f"\n多platformcrawlfailed: {result.get('error', '未知error')}")
    
    except KeyboardInterrupt:
        print("\nuser中断操作")
    except Exception as e:
        print(f"\nexecute出错: {e}")
    finally:
        crawler.close()

if __name__ == "__main__":
    main()
