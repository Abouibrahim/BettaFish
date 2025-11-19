#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Chinese to English translation script for MindSpider module
Translates all Chinese text in Python files to English
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Translation dictionary for common terms
TRANSLATIONS = {
    # Module/Component names
    "database": "database",
    "initialize": "initialize/initialization",
    "configuration": "configuration",
    "connection": "connection",
    "main program": "main program",
    "工作流程": "workflow",
    "topic extraction": "topic extraction",
    "sentiment crawling": "sentiment crawling",
    "deep crawling": "deep crawling",
    "news": "news",
    "keyword": "keywords",
    "总结": "summary",

    # Status/Result terms
    "success": "successful/success",
    "failed": "failed/failure",
    "error": "error",
    "warning": "warning",
    "normal": "normal",
    "exception": "error/exception",
    "completed": "completed",
    "execute": "execute/execution",

    # Data terms
    "data": "data",
    "table": "table",
    "record": "record(s)",
    "statistics": "statistics",
    "query": "query",
    "save": "save",
    "delete": "delete",
    "update": "update",

    # Actions
    "run": "run/running",
    "check": "check/checking",
    "show": "show/display",
    "get": "get/obtain",
    "设置": "setup/setting",
    "cleanup": "cleanup",
    "collect": "collect/collection",
    "extract": "extract/extraction",
    "crawl": "crawl/crawling",

    # Platform names (keep original)
    "Xiaohongshu": "Xiaohongshu",
    "Douyin": "Douyin",
    "Kuaishou": "Kuaishou",
    "Weibo": "Weibo",
    "Tieba": "Tieba",
    "Zhihu": "Zhihu",
    "Bilibili": "Bilibili",
    "Bilibili": "Bilibili",

    # Common phrases
    "请check": "please check",
    "please ensure": "please ensure",
    "unable to": "unable to",
    "not found": "not found",
    "does not exist": "does not exist",
    "need": "need/required",
    "missing": "missing",
    "missing": "missing",
}

# Specific translations for complete phrases/sentences
PHRASE_TRANSLATIONS = {
    # Error messages
    "error：unable to导入config.pyconfiguration文件": "Error: Unable to import config.py configuration file",
    "please ensure项目根目录下存在config.py文件，并包含database和APIconfiguration信息": "Please ensure config.py file exists in project root directory and contains database and API configuration",
    "error：not founddatabaseinitialize脚本": "Error: Database initialization script not found",
    "error：not foundMediaCrawler目录": "Error: MediaCrawler directory not found",
    "error：日期格式不正确，请使用 YYYY-MM-DD 格式": "Error: Incorrect date format, please use YYYY-MM-DD format",
    "error: unable to导入config.pyconfiguration文件": "Error: Unable to import config.py configuration file",

    # Info messages
    "MindSpider AIcrawler project": "MindSpider AI Crawler Project",
    "MindSpider AI爬虫 - 每日topic extraction": "MindSpider AI Crawler - Daily Topic Extraction",
    "databaseconnectionnormal": "Database connection successful",
    "databaseconnectionfailed": "Database connection failed",
    "databaseinitializesuccess": "Database initialization successful",
    "databaseinitializefailed": "Database initialization failed",
    "基础configurationcheck通过": "Basic configuration check passed",
    "依赖环境check通过": "Dependencies check passed",
    "databasetablecheck通过": "Database tables check passed",
    "MindSpider项目initializecompleted！": "MindSpider project initialization completed!",
    "完整工作流程executesuccess！": "Complete workflow executed successfully!",
    "topic extractionfailed，终止流程": "Topic extraction failed, terminating workflow",
    "sentiment crawlingfailed，但topic extraction已completed": "Sentiment crawling failed, but topic extraction completed",
    "项目设置completed，可以开始使用MindSpider！": "Project setup completed, ready to use MindSpider!",
    "项目设置failed，请checkconfiguration和环境": "Project setup failed, please check configuration and environment",
    "user中断操作": "User interrupted operation",

    # Database messages
    "successconnection到database": "Successfully connected to database",
    "database中没有table": "No tables in database",
    "missingdatabasetable": "Missing database tables",
    "needinitializedatabasetable...": "Database tables need initialization...",

    # Module execution
    "BroadTopicExtraction模块executesuccess": "BroadTopicExtraction module executed successfully",
    "BroadTopicExtraction模块executefailed，返回码": "BroadTopicExtraction module execution failed, return code",
    "BroadTopicExtraction模块execute超时": "BroadTopicExtraction module execution timeout",
    "BroadTopicExtraction模块executeexception": "BroadTopicExtraction module execution exception",
    "DeepSentimentCrawling模块executesuccess": "DeepSentimentCrawling module executed successfully",
    "DeepSentimentCrawling模块executefailed，返回码": "DeepSentimentCrawling module execution failed, return code",
    "DeepSentimentCrawling模块execute超时": "DeepSentimentCrawling module execution timeout",
    "DeepSentimentCrawling模块executeexception": "DeepSentimentCrawling module execution exception",

    # Status messages
    "开始MindSpider项目initialize...": "Starting MindSpider project initialization...",
    "开始完整的MindSpider工作流程": "Starting complete MindSpider workflow",
    "run完整MindSpider工作流程...": "Running complete MindSpider workflow...",
    "每日topic extraction流程completed!": "Daily topic extraction workflow completed!",

    # Log/comment headers
    "添加项目根目录到路径": "Add project root directory to path",
    "check基础configuration...": "Checking basic configuration...",
    "checkdatabaseconnection...": "Checking database connection...",
    "checkdatabasetable...": "Checking database tables...",
    "check依赖环境...": "Checking dependencies...",
    "initializedatabase...": "Initializing database...",
    "runBroadTopicExtraction模块...": "Running BroadTopicExtraction module...",
    "runDeepSentimentCrawling模块...": "Running DeepSentimentCrawling module...",
    "execute命令": "Executing command",

    # Help/argument descriptions
    "initialize项目设置": "Initialize project setup",
    "show项目状态": "Show project status",
    "initializedatabase": "Initialize database",
    "只runtopic extraction模块": "Run only topic extraction module",
    "只runsentiment crawling模块": "Run only sentiment crawling module",
    "run完整工作流程": "Run complete workflow",
    "目标日期 (YYYY-MM-DD)，default为今天": "Target date (YYYY-MM-DD), defaults to today",
    "指定crawlplatform": "Specify crawling platforms",
    "topic extraction的keyword数量": "Number of keywords for topic extraction",
    "每个platformmaximumkeyword数量": "Maximum keywords per platform",
    "每个keywordmaximumcrawlcontent数量": "Maximum content items to crawl per keyword",
    "测试模式（少量data）": "Test mode (small data)",

    # Comments
    "default使用 mysql 异步驱动 asyncmy": "Use mysql async driver asyncmy by default",
    "rundatabaseinitialize脚本": "Run database initialization script",
    "checkPython包": "Check Python packages",
    "checkMediaCrawler依赖": "Check MediaCrawler dependencies",
    "checksettingsconfiguration项": "Check settings configuration items",
    "30分钟超时": "30-minute timeout",
    "60分钟超时": "60-minute timeout",
    "第一步：topic extraction": "Step 1: Topic Extraction",
    "第二步：sentiment crawling": "Step 2: Sentiment Crawling",
    "=== 第一步：topic extraction ===": "=== Step 1: Topic Extraction ===",
    "=== 第二步：sentiment crawling ===": "=== Step 2: Sentiment Crawling ===",

    # Other
    "all支持的platform": "All supported platforms",
    "是": "Yes",
    "否": "No",
    "存在": "Exists",
    "missing": "Missing",
    "请run: pip install -r requirements.txt": "Please run: pip install -r requirements.txt",
    "missingPython包": "Missing Python packages",
}

def translate_file_summary(filepath: Path) -> None:
    """
    Print translation summary for a file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count Chinese characters
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_matches = chinese_pattern.findall(content)

        if chinese_matches:
            print(f"\n{filepath}:")
            print(f"  Found {len(chinese_matches)} Chinese text instances")
            print(f"  Sample: {chinese_matches[0] if chinese_matches else 'N/A'}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    """Main function to scan and report on files needing translation"""
    mindspider_root = Path("/home/user/BettaFish/MindSpider")

    # Find all Python files with Chinese text
    python_files = list(mindspider_root.rglob("*.py"))

    print(f"Scanning {len(python_files)} Python files in MindSpider module...")
    print("=" * 70)

    files_with_chinese = []
    total_instances = 0

    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
            chinese_matches = chinese_pattern.findall(content)

            if chinese_matches:
                files_with_chinese.append((py_file, len(chinese_matches)))
                total_instances += len(chinese_matches)
        except Exception as e:
            print(f"Error reading {py_file}: {e}")

    print(f"\nSummary:")
    print(f"  Total files with Chinese: {len(files_with_chinese)}")
    print(f"  Total Chinese text instances: {total_instances}")
    print("\nTop 10 files by Chinese text count:")

    sorted_files = sorted(files_with_chinese, key=lambda x: x[1], reverse=True)
    for filepath, count in sorted_files[:10]:
        rel_path = filepath.relative_to(mindspider_root)
        print(f"  {rel_path}: {count} instances")

    print("\nTranslation dictionary contains:")
    print(f"  {len(TRANSLATIONS)} term translations")
    print(f"  {len(PHRASE_TRANSLATIONS)} phrase translations")

if __name__ == "__main__":
    main()
