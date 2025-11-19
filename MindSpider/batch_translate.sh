#!/bin/bash
# Batch translation script for MindSpider module
# Translates common Chinese phrases to English across all Python files

cd /home/user/BettaFish/MindSpider

# Common translations - apply to all .py files in MindSpider
find . -name "*.py" -type f -exec sed -i '
# Module/file docstrings
s/爬虫项目/crawler project/g
s/主程序/main program/g
s/数据库管理工具/database management tool/g
s/话题提取/topic extraction/g
s/情感爬取/sentiment crawling/g
s/深度爬取/deep crawling/g

# Common actions
s/初始化/initialize/g
s/配置/configuration/g
s/检查/check/g
s/连接/connection/g
s/运行/run/g
s/执行/execute/g
s/显示/show/g
s/获取/get/g
s/保存/save/g
s/删除/delete/g
s/清理/cleanup/g
s/收集/collect/g
s/提取/extract/g
s/爬取/crawl/g
s/更新/update/g
s/查询/query/g

# Status terms
s/成功/success/g
s/失败/failed/g
s/完成/completed/g
s/错误/error/g
s/警告/warning/g
s/正常/normal/g
s/异常/exception/g

# Data terms
s/数据库/database/g
s/数据/data/g
s/表/table/g
s/记录/record/g
s/统计/statistics/g
s/新闻/news/g
s/话题/topic/g
s/关键词/keyword/g
s/平台/platform/g
s/任务/task/g
s/内容/content/g
s/评论/comment/g
s/用户/user/g

# Quantifiers
s/ 个/ /g
s/ 条/ /g
s/ 天/ days/g
s/ 次/ times/g

# Common phrases
s/请检查/please check/g
s/请确保/please ensure/g
s/无法/unable to/g
s/找不到/not found/g
s/不存在/does not exist/g
s/需要/need/g
s/缺少/missing/g
s/缺失/missing/g
s/所有/all/g
s/最大/maximum/g
s/最小/minimum/g
s/默认/default/g
s/可选/optional/g

# Platform names (keep original pinyin)
s/小红书/Xiaohongshu/g
s/抖音/Douyin/g
s/快手/Kuaishou/g
s/微博/Weibo/g
s/贴吧/Tieba/g
s/知乎/Zhihu/g
s/哔哩哔哩/Bilibili/g
s/B站/Bilibili/g

# Comments
s/# 添加项目根目录到路径/# Add project root directory to path/g
s/# 导入/# Import/g
s/# 检查/# Check/g
s/# 运行/# Run/g
s/# 初始化/# Initialize/g

' {} \;

echo "Batch translation completed!"
echo "Translated common Chinese terms to English across all Python files."
