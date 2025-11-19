# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标platform的使用条款和robots.txt规则。
# 3. 不得进行大规模crawl或对platform造成运营干扰。
# 4. 应合理控制请求频率，避免给目标platform带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即table示您同意遵守上述原则和LICENSE中的all条款。

# 基础configuration
PLATFORM = "bili"  # platform，xhs | dy | ks | bili | wb | tieba | zhihu
KEYWORDS = "电影鬼灭之刃,亲属想侵吞3姐妹亡父赔偿款,网警斩断侵害未成年人网络黑色产业链,2007年后出生的人不能在马尔代夫吸烟,沈月,是公主也是自己的骑士,以军虐囚视频,唐朝诡事录,广州地铁回应APP乘车码频繁弹窗广告,全红婵的减肥计划精确到克"  # keyword搜索configuration，以英文逗号分隔
LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = ""
CRAWLER_TYPE = "search"  # crawl类型，search(keyword搜索) | detail(帖子详情)| creator(创作者主页data)

# 是否开启 IP 代理
ENABLE_IP_PROXY = False

# 代理IP池数量
IP_PROXY_POOL_COUNT = 2

# 代理IP提供商名称
IP_PROXY_PROVIDER_NAME = "kuaidaili"  # kuaidaili | wandouhttp

# 设置为True不会打开浏览器（无头浏览器）
# 设置False会打开一个浏览器
# Xiaohongshu如果一直扫码登录不通过，打开浏览器手动过一下滑动验证码
# Douyin如果一直提示failed，打开浏览器看下是否扫码登录之后出现了手机号验证，如果出现了手动过一下再试。
HEADLESS = True

# 是否save登录状态
SAVE_LOGIN_STATE = True

# ==================== CDP (Chrome DevTools Protocol) configuration ====================
# 是否启用CDP模式 - 使用user现有的Chrome/Edge浏览器进行crawl，提供更好的反检测能力
# 启用后将自动检测并启动user的Chrome/Edge浏览器，通过CDP协议进行控制
# 这种方式使用真实的浏览器环境，包括user的扩展、Cookie和设置，大大降低被检测的风险
ENABLE_CDP_MODE = True

# CDP调试端口，用于与浏览器通信
# 如果端口被占用，系统会自动尝试下一个可用端口
CDP_DEBUG_PORT = 9222

# 自定义浏览器路径（optional）
# 如果为空，系统会自动检测Chrome/Edge的安装路径
# Windows示例: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# macOS示例: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CUSTOM_BROWSER_PATH = ""

# CDP模式下是否启用无头模式
# 注意：即使设置为True，某些反检测功能在无头模式下可能效果不佳
CDP_HEADLESS = False

# 浏览器启动超时时间（秒）
BROWSER_LAUNCH_TIMEOUT = 30

# 是否在程序结束时自动关闭浏览器
# 设置为False可以保持浏览器run，便于调试
AUTO_CLOSE_BROWSER = True

# datasave类型选项configuration,支持五种类型：csv、db、json、sqlite、postgresql, 最好save到DB，有排重的功能。
SAVE_DATA_OPTION = "postgresql"  # csv or db or json or sqlite or postgresql

# user浏览器缓存的浏览器文件configuration
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# crawl开始页数 default从第一页开始
START_PAGE = 1

# crawl视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = 5

# 并发爬虫数量控制
MAX_CONCURRENCY_NUM = 1

# 是否开启爬媒体模式（包含图片或视频资源），default不开启爬媒体
ENABLE_GET_MEIDAS = False

# 是否开启爬comment模式, default开启爬comment
ENABLE_GET_COMMENTS = True

# crawl一级comment的数量控制(单视频/帖子)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20

# 是否开启爬二级comment模式, default不开启爬二级comment
# 老版本项目使用了 db, 则需参考 schema/tables.sql line 287 增加table字段
ENABLE_GET_SUB_COMMENTS = False

# 词云相关
# 是否开启生成comment词云图
ENABLE_GET_WORDCLOUD = False
# 自定义词语及其分组
# 添加规则：xx:yy 其中xx为自定义添加的词组，yy为将xx该词组分到的组名。
CUSTOM_WORDS = {
    "零几": "年份",  # 将“零几”识别为一个整体
    "高频词": "专业术语",  # 示例自定义词
}

# 停用(禁用)词文件路径
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# 中文字体文件路径
FONT_PATH = "./docs/STZHONGS.TTF"

# crawl间隔时间
CRAWLER_MAX_SLEEP_SEC = 2

from .bilibili_config import *
from .xhs_config import *
from .dy_config import *
from .ks_config import *
from .weibo_config import *
from .tieba_config import *
from .zhihu_config import *
