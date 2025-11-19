#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BroadTopicExtraction模块 - database管理器
只负责newsdata和topic分析的存储和query
"""

import sys
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from loguru import logger

# Add project root directory to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import config
except ImportError:
    raise ImportError("unable to导入config.pyconfiguration文件")

from config import settings


class DatabaseManager:
    """database管理器"""

    def __init__(self):
        """initializedatabase管理器"""
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
            logger.info(f"successconnection到database: {settings.DB_NAME}")
        except ModuleNotFoundError as e:
            missing: str = str(e)
            if "psycopg" in missing:
                logger.error(
                    "databaseconnectionfailed: 未安装PostgreSQL驱动 psycopg。请安装: psycopg[binary]。参考指令：uv pip install psycopg[binary]")
            elif "pymysql" in missing:
                logger.error("databaseconnectionfailed: 未安装MySQL驱动 pymysql。请安装: pymysql。参考指令：uv pip install pymysql")
            else:
                logger.error(f"databaseconnectionfailed(missing驱动): {e}")
            raise
        except Exception as e:
            logger.exception(f"databaseconnectionfailed: {e}")
            raise

    def close(self):
        """关闭databaseconnection"""
        if self.engine:
            self.engine.dispose()
            logger.info("databaseconnection已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ==================== newsdata操作 ====================

    def save_daily_news(self, news_data: List[Dict], crawl_date: date = None) -> int:
        """
        save每日newsdata，如果当天已有data则覆盖

        Args:
            news_data: newsdata列table
            crawl_date: crawl日期，default为今天

        Returns:
            save的news数量
        """
        if not crawl_date:
            crawl_date = date.today()

        current_timestamp = int(datetime.now().timestamp())

        try:
            saved_count = 0
            # 先独立事务executedelete，防止后续插入failed导致unable tocleanup
            with self.engine.begin() as conn:
                deleted = conn.execute(text("DELETE FROM daily_news WHERE crawl_date = :d"), {"d": crawl_date}).rowcount
                if deleted and deleted > 0:
                    logger.info(f"覆盖模式：delete了当天已有的 {deleted} newsrecord")

            # 逐条插入，单条failed不影响后续（每条独立事务）
            for news_item in news_data:
                try:
                    # news_item.get('id') 已经是完整的 news_id（格式：source_item_id）
                    # 为了支持同一条news在不同日期出现，将 crawl_date 加入到 news_id 中
                    base_news_id = news_item.get(
                        'id') or f"{news_item.get('source', 'unknown')}_rank_{news_item.get('rank', 0)}"
                    # 将日期格式化为字符串并加入到 news_id 中，确保全局唯一性
                    news_id = f"{base_news_id}_{crawl_date.strftime('%Y%m%d')}"

                    title_val = (news_item.get("title", "") or "")
                    if len(title_val) > 500:
                        title_val = title_val[:500]
                    with self.engine.begin() as conn:
                        conn.execute(
                            text(
                                """
                                INSERT INTO daily_news (
                                    news_id, source_platform, title, url, crawl_date,
                                    rank_position, add_ts, last_modify_ts
                                ) VALUES (:news_id, :source_platform, :title, :url, :crawl_date, :rank_position, :add_ts, :last_modify_ts)
                                """
                            ),
                            {
                                "news_id": news_id,
                                "source_platform": news_item.get("source", "unknown"),
                                "title": title_val,
                                "url": news_item.get("url", ""),
                                "crawl_date": crawl_date,
                                "rank_position": news_item.get("rank", None),
                                "add_ts": current_timestamp,
                                "last_modify_ts": current_timestamp,
                            },
                        )
                    saved_count += 1
                except Exception as e:
                    logger.exception(f"save单条newsfailed: {e}")
                    continue
            logger.info(f"successsave {saved_count} newsrecord")
            return saved_count
        except Exception as e:
            logger.exception(f"savenewsdatafailed: {e}")
            return 0

    def get_daily_news(self, crawl_date: date = None) -> List[Dict]:
        """
        get每日newsdata

        Args:
            crawl_date: crawl日期，default为今天

        Returns:
            news列table
        """
        if not crawl_date:
            crawl_date = date.today()

        query = (
            "SELECT * FROM daily_news WHERE crawl_date = :d ORDER BY rank_position ASC"
        )
        with self.engine.connect() as conn:
            result = conn.execute(text(query), {"d": crawl_date})
            rows = result.mappings().all()
        return rows

    # ==================== topicdata操作 ====================

    def save_daily_topics(self, keywords: List[str], summary: str, extract_date: date = None) -> bool:
        """
        save每日topic分析

        Args:
            keywords: topickeyword列table
            summary: news分析总结
            extract_date: extract日期，default为今天

        Returns:
            是否savesuccess
        """
        if not extract_date:
            extract_date = date.today()

        current_timestamp = int(datetime.now().timestamp())

        try:
            keywords_json = json.dumps(keywords, ensure_ascii=False)
            # 为了支持外键引用，topic_id need全局唯一，所以将日期加入到 topic_id 中
            topic_id = f"summary_{extract_date.strftime('%Y%m%d')}"

            with self.engine.begin() as conn:
                check = conn.execute(
                    text("SELECT id FROM daily_topics WHERE extract_date = :d AND topic_id = :tid"),
                    {"d": extract_date, "tid": topic_id},
                ).first()
                if check:
                    conn.execute(
                        text(
                            "UPDATE daily_topics SET keywords = :k, topic_description = :s, add_ts = :ts, last_modify_ts = :lmt, topic_name = :tn WHERE extract_date = :d AND topic_id = :tid"
                        ),
                        {"k": keywords_json, "s": summary, "ts": current_timestamp, "lmt": current_timestamp,
                         "d": extract_date, "tid": topic_id, "tn": "每日news分析"},
                    )
                    logger.info(f"update了 {extract_date} 的topic分析")
                else:
                    conn.execute(
                        text(
                            "INSERT INTO daily_topics (extract_date, topic_id, topic_name, keywords, topic_description, add_ts, last_modify_ts) VALUES (:d, :tid, :tn, :k, :s, :ts, :lmt)"
                        ),
                        {"d": extract_date, "tid": topic_id, "tn": "每日news分析", "k": keywords_json, "s": summary,
                         "ts": current_timestamp, "lmt": current_timestamp},
                    )
                    logger.info(f"save了 {extract_date} 的topic分析")
            return True
        except Exception as e:
            logger.exception(f"savetopic分析failed: {e}")
            return False

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
                result = conn.execute(text("SELECT * FROM daily_topics WHERE extract_date = :d"),
                                      {"d": extract_date}).mappings().first()
                if result:
                    result = dict(result)  # 转为可变dict以支持item赋值
                    result["keywords"] = json.loads(result["keywords"]) if result.get("keywords") else []
                    return result
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
                for r in results:
                    r["keywords"] = json.loads(r["keywords"]) if r.get("keywords") else []
                return results
        except Exception as e:
            logger.exception(f"get最近topic分析failed: {e}")
            return []

    # ==================== statisticsquery ====================

    def get_summary_stats(self, days: int = 7) -> Dict:
        """getstatistics摘要"""
        try:
            start_date = date.today() - timedelta(days=days)
            with self.engine.connect() as conn:
                news_stats = conn.execute(
                    text(
                        """
                        SELECT crawl_date, COUNT(*) as news_count, COUNT(DISTINCT source_platform) as platforms_count
                        FROM daily_news 
                        WHERE crawl_date >= :start_date
                        GROUP BY crawl_date
                        ORDER BY crawl_date DESC
                        """
                    ),
                    {"start_date": start_date},
                ).all()
                topics_stats = conn.execute(
                    text(
                        """
                        SELECT extract_date, keywords, CHAR_LENGTH(topic_description) as summary_length
                        FROM daily_topics 
                        WHERE extract_date >= :start_date
                        ORDER BY extract_date DESC
                        """
                    ),
                    {"start_date": start_date},
                ).all()
                return {"news_stats": news_stats, "topics_stats": topics_stats}
        except Exception as e:
            logger.exception(f"getstatistics摘要failed: {e}")
            return {"news_stats": [], "topics_stats": []}


if __name__ == "__main__":
    # 测试database管理器
    with DatabaseManager() as db:
        # 测试getnews
        news = db.get_daily_news()
        logger.info(f"今日news数量: {len(news)}")

        # 测试gettopic
        topics = db.get_daily_topics()
        if topics:
            logger.info(f"今日topickeyword: {topics['keywords']}")
        else:
            logger.info("今日暂无topic分析")

        logger.info("简化database管理器测试completed！")
