# -*- coding: utf-8 -*-
# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标platform的使用条款和robots.txt规则。
# 3. 不得进行大规模crawl或对platform造成运营干扰。
# 4. 应合理控制请求频率，避免给目标platform带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即table示您同意遵守上述原则和LICENSE中的all条款。
# bilili platformconfiguration

# 每天crawl视频/帖子的数量控制
MAX_NOTES_PER_DAY = 1

# 指定Bilibili视频URL列table (支持完整URL或BV号)
# 示例:
# - 完整URL: "https://www.bilibili.com/video/BV1dwuKzmE26/?spm_id_from=333.1387.homepage.video_card.click"
# - BV号: "BV1d54y1g7db"
BILI_SPECIFIED_ID_LIST = [
    "https://www.bilibili.com/video/BV1dwuKzmE26/?spm_id_from=333.1387.homepage.video_card.click",
    "BV1Sz4y1U77N",
    "BV14Q4y1n7jz",
    # ........................
]

# 指定Bilibili创作者URL列table (支持完整URL或UID)
# 示例:
# - 完整URL: "https://space.bilibili.com/434377496?spm_id_from=333.1007.0.0"
# - UID: "20813884"
BILI_CREATOR_ID_LIST = [
    "https://space.bilibili.com/434377496?spm_id_from=333.1007.0.0",
    "20813884",
    # ........................
]

# 指定时间范围
START_DAY = "2024-01-01"
END_DAY = "2024-01-01"

# 搜索模式
BILI_SEARCH_MODE = "normal"

# 视频清晰度（qn）configuration，常见取值：
# 16=360p, 32=480p, 64=720p, 80=1080p, 112=1080p高码率, 116=1080p60, 120=4K
# 注意：更高清晰度need账号/视频本身支持
BILI_QN = 80

# 是否crawluser信息
CREATOR_MODE = True

# 开始crawluser信息页码
START_CONTACTS_PAGE = 1

# 单个视频/帖子maximumcrawlcomment数
CRAWLER_MAX_CONTACTS_COUNT_SINGLENOTES = 100

# 单个视频/帖子maximumcrawl动态数
CRAWLER_MAX_DYNAMICS_COUNT_SINGLENOTES = 50
