#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSentimentCrawling模块 - platform爬虫管理器
负责configuration和调用MediaCrawler进行多platformcrawl
"""

import os
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json
from loguru import logger

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import config
except ImportError:
    raise ImportError("unable to导入config.pyconfiguration文件")

class PlatformCrawler:
    """platform爬虫管理器"""
    
    def __init__(self):
        """initializeplatform爬虫管理器"""
        self.mediacrawler_path = Path(__file__).parent / "MediaCrawler"
        self.supported_platforms = ['xhs', 'dy', 'ks', 'bili', 'wb', 'tieba', 'zhihu']
        self.crawl_stats = {}
        
        # 确保MediaCrawler目录存在
        if not self.mediacrawler_path.exists():
            raise FileNotFoundError(f"MediaCrawler目录does not exist: {self.mediacrawler_path}")
        
        logger.info(f"initializeplatform爬虫管理器，MediaCrawler路径: {self.mediacrawler_path}")
    
    def configure_mediacrawler_db(self):
        """configurationMediaCrawler使用我们的database（MySQL或PostgreSQL）"""
        try:
            # 判断database类型
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            is_postgresql = db_dialect in ("postgresql", "postgres")
            
            # 修改MediaCrawler的databaseconfiguration
            db_config_path = self.mediacrawler_path / "config" / "db_config.py"
            
            # 读取原始configuration
            with open(db_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # PostgreSQLconfiguration值：如果使用PostgreSQL则使用MindSpiderconfiguration，否则使用default值或环境变量
            pg_password = config.settings.DB_PASSWORD if is_postgresql else "bettafish"
            pg_user = config.settings.DB_USER if is_postgresql else "bettafish"
            pg_host = config.settings.DB_HOST if is_postgresql else "127.0.0.1"
            pg_port = config.settings.DB_PORT if is_postgresql else 5432
            pg_db_name = config.settings.DB_NAME if is_postgresql else "bettafish"
            
            # 替换databaseconfiguration - 使用MindSpider的databaseconfiguration
            new_config = f'''# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标platform的使用条款和robots.txt规则。  
# 3. 不得进行大规模crawl或对platform造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标platform带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即table示您同意遵守上述原则和LICENSE中的all条款。  


import os

# mysql config - 使用MindSpider的databaseconfiguration
MYSQL_DB_PWD = "{config.settings.DB_PASSWORD}"
MYSQL_DB_USER = "{config.settings.DB_USER}"
MYSQL_DB_HOST = "{config.settings.DB_HOST}"
MYSQL_DB_PORT = {config.settings.DB_PORT}
MYSQL_DB_NAME = "{config.settings.DB_NAME}"

mysql_db_config = {{
    "user": MYSQL_DB_USER,
    "password": MYSQL_DB_PWD,
    "host": MYSQL_DB_HOST,
    "port": MYSQL_DB_PORT,
    "db_name": MYSQL_DB_NAME,
}}


# redis config
REDIS_DB_HOST = "127.0.0.1"  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password
REDIS_DB_PORT = os.getenv("REDIS_DB_PORT", 6379)  # your redis port
REDIS_DB_NUM = os.getenv("REDIS_DB_NUM", 0)  # your redis db num

# cache type
CACHE_TYPE_REDIS = "redis"
CACHE_TYPE_MEMORY = "memory"

# sqlite config
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "sqlite_tables.db")

sqlite_db_config = {{
    "db_path": SQLITE_DB_PATH
}}

# postgresql config - 使用MindSpider的databaseconfiguration（如果DB_DIALECT是postgresql）或环境变量
POSTGRESQL_DB_PWD = os.getenv("POSTGRESQL_DB_PWD", "{pg_password}")
POSTGRESQL_DB_USER = os.getenv("POSTGRESQL_DB_USER", "{pg_user}")
POSTGRESQL_DB_HOST = os.getenv("POSTGRESQL_DB_HOST", "{pg_host}")
POSTGRESQL_DB_PORT = os.getenv("POSTGRESQL_DB_PORT", "{pg_port}")
POSTGRESQL_DB_NAME = os.getenv("POSTGRESQL_DB_NAME", "{pg_db_name}")

postgresql_db_config = {{
    "user": POSTGRESQL_DB_USER,
    "password": POSTGRESQL_DB_PWD,
    "host": POSTGRESQL_DB_HOST,
    "port": POSTGRESQL_DB_PORT,
    "db_name": POSTGRESQL_DB_NAME,
}}

'''
            
            # 写入新configuration
            with open(db_config_path, 'w', encoding='utf-8') as f:
                f.write(new_config)
            
            db_type = "PostgreSQL" if is_postgresql else "MySQL"
            logger.info(f"已configurationMediaCrawler使用MindSpider {db_type}database")
            return True
            
        except Exception as e:
            logger.exception(f"configurationMediaCrawlerdatabasefailed: {e}")
            return False
    
    def create_base_config(self, platform: str, keywords: List[str], 
                          crawler_type: str = "search", max_notes: int = 50) -> bool:
        """
        创建MediaCrawler的基础configuration
        
        Args:
            platform: platform名称
            keywords: keyword列table
            crawler_type: crawl类型
            max_notes: maximumcrawl数量
        
        Returns:
            是否configurationsuccess
        """
        try:
            # 判断database类型，确定 SAVE_DATA_OPTION
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            is_postgresql = db_dialect in ("postgresql", "postgres")
            save_data_option = "postgresql" if is_postgresql else "db"
            
            base_config_path = self.mediacrawler_path / "config" / "base_config.py"
            
            # 将keyword列table转换为逗号分隔的字符串
            keywords_str = ",".join(keywords)
            
            # 读取原始configuration文件
            with open(base_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修改关键configuration项
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                if line.startswith('PLATFORM = '):
                    new_lines.append(f'PLATFORM = "{platform}"  # platform，xhs | dy | ks | bili | wb | tieba | zhihu')
                elif line.startswith('KEYWORDS = '):
                    new_lines.append(f'KEYWORDS = "{keywords_str}"  # keyword搜索configuration，以英文逗号分隔')
                elif line.startswith('CRAWLER_TYPE = '):
                    new_lines.append(f'CRAWLER_TYPE = "{crawler_type}"  # crawl类型，search(keyword搜索) | detail(帖子详情)| creator(创作者主页data)')
                elif line.startswith('SAVE_DATA_OPTION = '):
                    new_lines.append(f'SAVE_DATA_OPTION = "{save_data_option}"  # csv or db or json or sqlite or postgresql')
                elif line.startswith('CRAWLER_MAX_NOTES_COUNT = '):
                    new_lines.append(f'CRAWLER_MAX_NOTES_COUNT = {max_notes}')
                elif line.startswith('ENABLE_GET_COMMENTS = '):
                    new_lines.append('ENABLE_GET_COMMENTS = True')
                elif line.startswith('CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = '):
                    new_lines.append('CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20')
                elif line.startswith('HEADLESS = '):
                    new_lines.append('HEADLESS = True')  # 使用无头模式
                else:
                    new_lines.append(line)
            
            # 写入新configuration
            with open(base_config_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            logger.info(f"已configuration {platform} platform，crawl类型: {crawler_type}，keyword数量: {len(keywords)}，maximumcrawl数量: {max_notes}，savedata方式: {save_data_option}")
            return True
            
        except Exception as e:
            logger.exception(f"创建基础configurationfailed: {e}")
            return False
    
    def run_crawler(self, platform: str, keywords: List[str], 
                   login_type: str = "qrcode", max_notes: int = 50) -> Dict:
        """
        run爬虫
        
        Args:
            platform: platform名称
            keywords: keyword列table
            login_type: 登录方式
            max_notes: maximumcrawl数量
        
        Returns:
            crawl结果statistics
        """
        if platform not in self.supported_platforms:
            raise ValueError(f"不支持的platform: {platform}")
        
        if not keywords:
            raise ValueError("keyword列table不能为空")
        
        start_message = f"\n开始crawlplatform: {platform}"
        start_message += f"\nkeyword: {keywords[:5]}{'...' if len(keywords) > 5 else ''} (共{len(keywords)}个)"
        logger.info(start_message)
        
        start_time = datetime.now()
        
        try:
            # configurationdatabase
            if not self.configure_mediacrawler_db():
                return {"success": False, "error": "databaseconfigurationfailed"}
            
            # 创建基础configuration
            if not self.create_base_config(platform, keywords, "search", max_notes):
                return {"success": False, "error": "基础configuration创建failed"}
            
            # 判断database类型，确定 save_data_option
            db_dialect = (config.settings.DB_DIALECT or "mysql").lower()
            is_postgresql = db_dialect in ("postgresql", "postgres")
            save_data_option = "postgresql" if is_postgresql else "db"
            
            # 构建命令
            cmd = [
                sys.executable, "main.py",
                "--platform", platform,
                "--lt", login_type,
                "--type", "search",
                "--save_data_option", save_data_option
            ]
            
            logger.info(f"execute命令: {' '.join(cmd)}")
            
            # 切换到MediaCrawler目录并execute
            result = subprocess.run(
                cmd,
                cwd=self.mediacrawler_path,
                timeout=3600  # 60分钟超时
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 创建statistics信息
            crawl_stats = {
                "platform": platform,
                "keywords_count": len(keywords),
                "duration_seconds": duration,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "return_code": result.returncode,
                "success": result.returncode == 0,
                "notes_count": 0,
                "comments_count": 0,
                "errors_count": 0
            }
            
            # savestatistics信息
            self.crawl_stats[platform] = crawl_stats
            
            if result.returncode == 0:
                logger.info(f"✅ {platform} crawlcompleted，耗时: {duration:.1f}秒")
            else:
                logger.error(f"❌ {platform} crawlfailed，返回码: {result.returncode}")
            
            return crawl_stats
            
        except subprocess.TimeoutExpired:
            logger.exception(f"❌ {platform} crawl超时")
            return {"success": False, "error": "crawl超时", "platform": platform}
        except Exception as e:
            logger.exception(f"❌ {platform} crawlexception: {e}")
            return {"success": False, "error": str(e), "platform": platform}
    
    def _parse_crawl_output(self, output_lines: List[str], error_lines: List[str]) -> Dict:
        """解析crawl输出，extractstatistics信息"""
        stats = {
            "notes_count": 0,
            "comments_count": 0,
            "errors_count": 0,
            "login_required": False
        }
        
        # 解析输出行
        for line in output_lines:
            if "条笔记" in line or "条content" in line:
                try:
                    # extract数字
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        stats["notes_count"] = int(numbers[0])
                except:
                    pass
            elif "条comment" in line:
                try:
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        stats["comments_count"] = int(numbers[0])
                except:
                    pass
            elif "登录" in line or "扫码" in line:
                stats["login_required"] = True
        
        # 解析error行
        for line in error_lines:
            if "error" in line.lower() or "exception" in line:
                stats["errors_count"] += 1
        
        return stats
    
    def run_multi_platform_crawl_by_keywords(self, keywords: List[str], platforms: List[str],
                                            login_type: str = "qrcode", max_notes_per_keyword: int = 50) -> Dict:
        """
        基于keyword的多platformcrawl - 每个keyword在allplatform上都进行crawl
        
        Args:
            keywords: keyword列table
            platforms: platform列table
            login_type: 登录方式
            max_notes_per_keyword: 每个keyword在每个platform的maximumcrawl数量
        
        Returns:
            总体crawlstatistics
        """
        
        start_message = f"\n🚀 开始全platformkeywordcrawl"
        start_message += f"\n   keyword数量: {len(keywords)}"
        start_message += f"\n   platform数量: {len(platforms)}"
        start_message += f"\n   登录方式: {login_type}"
        start_message += f"\n   每个keyword在每个platform的maximumcrawl数量: {max_notes_per_keyword}"
        start_message += f"\n   总crawltask: {len(keywords)} × {len(platforms)} = {len(keywords) * len(platforms)}"
        logger.info(start_message)
        
        total_stats = {
            "total_keywords": len(keywords),
            "total_platforms": len(platforms),
            "total_tasks": len(keywords) * len(platforms),
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_notes": 0,
            "total_comments": 0,
            "keyword_results": {},
            "platform_summary": {}
        }
        
        # initializeplatformstatistics
        for platform in platforms:
            total_stats["platform_summary"][platform] = {
                "successful_keywords": 0,
                "failed_keywords": 0,
                "total_notes": 0,
                "total_comments": 0
            }
        
        # 对每个platform一次性crawlallkeyword
        for platform in platforms:
            logger.info(f"\n📝 在 {platform} platformcrawlallkeyword")
            logger.info(f"   keyword: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
            
            try:
                # 一次性传递allkeyword给platform
                result = self.run_crawler(platform, keywords, login_type, max_notes_per_keyword)
                
                if result.get("success"):
                    total_stats["successful_tasks"] += len(keywords)
                    total_stats["platform_summary"][platform]["successful_keywords"] = len(keywords)
                    
                    notes_count = result.get("notes_count", 0)
                    comments_count = result.get("comments_count", 0)
                    
                    total_stats["total_notes"] += notes_count
                    total_stats["total_comments"] += comments_count
                    total_stats["platform_summary"][platform]["total_notes"] = notes_count
                    total_stats["platform_summary"][platform]["total_comments"] = comments_count
                    
                    # 为每个keywordrecord结果
                    for keyword in keywords:
                        if keyword not in total_stats["keyword_results"]:
                            total_stats["keyword_results"][keyword] = {}
                        total_stats["keyword_results"][keyword][platform] = result
                    
                    logger.info(f"   ✅ success: {notes_count} content, {comments_count} comment")
                else:
                    total_stats["failed_tasks"] += len(keywords)
                    total_stats["platform_summary"][platform]["failed_keywords"] = len(keywords)
                    
                    # 为每个keywordrecordfailed结果
                    for keyword in keywords:
                        if keyword not in total_stats["keyword_results"]:
                            total_stats["keyword_results"][keyword] = {}
                        total_stats["keyword_results"][keyword][platform] = result
                    
                    logger.error(f"   ❌ failed: {result.get('error', '未知error')}")
            
            except Exception as e:
                total_stats["failed_tasks"] += len(keywords)
                total_stats["platform_summary"][platform]["failed_keywords"] = len(keywords)
                error_result = {"success": False, "error": str(e)}
                
                # 为每个keywordrecordexception结果
                for keyword in keywords:
                    if keyword not in total_stats["keyword_results"]:
                        total_stats["keyword_results"][keyword] = {}
                    total_stats["keyword_results"][keyword][platform] = error_result
                
                logger.error(f"   ❌ exception: {e}")
        
        # 打印详细statistics
        finish_message = f"\n📊 全platformkeywordcrawlcompleted!"
        finish_message += f"\n   总task: {total_stats['total_tasks']}"
        finish_message += f"\n   success: {total_stats['successful_tasks']}"
        finish_message += f"\n   failed: {total_stats['failed_tasks']}"
        finish_message += f"\n   success率: {total_stats['successful_tasks']/total_stats['total_tasks']*100:.1f}%"
        finish_message += f"\n   总content: {total_stats['total_notes']} "
        finish_message += f"\n   总comment: {total_stats['total_comments']} "
        logger.info(finish_message)
        
        platform_summary_message = f"\n� 各platformstatistics:"
        for platform, stats in total_stats["platform_summary"].items():
            success_rate = stats["successful_keywords"] / len(keywords) * 100 if keywords else 0
            platform_summary_message += f"\n   {platform}: {stats['successful_keywords']}/{len(keywords)} keywordsuccess ({success_rate:.1f}%), "
            platform_summary_message += f"{stats['total_notes']} content"
        logger.info(platform_summary_message)
        
        return total_stats
    
    def get_crawl_statistics(self) -> Dict:
        """getcrawlstatistics信息"""
        return {
            "platforms_crawled": list(self.crawl_stats.keys()),
            "total_platforms": len(self.crawl_stats),
            "detailed_stats": self.crawl_stats
        }
    
    def save_crawl_log(self, log_path: str = None):
        """savecrawl日志"""
        if not log_path:
            log_path = f"crawl_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(self.crawl_stats, f, ensure_ascii=False, indent=2)
            logger.info(f"crawl日志已save到: {log_path}")
        except Exception as e:
            logger.exception(f"savecrawl日志failed: {e}")

if __name__ == "__main__":
    # 测试platform爬虫管理器
    crawler = PlatformCrawler()
    
    # 测试configuration
    test_keywords = ["科技", "AI", "编程"]
    result = crawler.run_crawler("xhs", test_keywords, max_notes=5)
    
    logger.info(f"测试结果: {result}")
    logger.info("platform爬虫管理器测试completed！")
