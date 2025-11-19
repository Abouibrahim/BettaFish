# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标platform的使用条款和robots.txt规则。  
# 3. 不得进行大规模crawl或对platform造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标platform带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即table示您同意遵守上述原则和LICENSE中的all条款。  


# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class ZhihuContent(BaseModel):
    """
    Zhihucontent（回答、文章、视频）
    """
    content_id: str = Field(default="", description="contentID")
    content_type: str = Field(default="", description="content类型(article | answer | zvideo)")
    content_text: str = Field(default="", description="content文本, 如果是视频类型这里为空")
    content_url: str = Field(default="", description="content落地链接")
    question_id: str = Field(default="", description="问题ID, type为answer时有值")
    title: str = Field(default="", description="content标题")
    desc: str = Field(default="", description="content描述")
    created_time: int = Field(default=0, description="创建时间")
    updated_time: int = Field(default=0, description="update时间")
    voteup_count: int = Field(default=0, description="赞同人数")
    comment_count: int = Field(default=0, description="comment数量")
    source_keyword: str = Field(default="", description="来源keyword")

    user_id: str = Field(default="", description="userID")
    user_link: str = Field(default="", description="user主页链接")
    user_nickname: str = Field(default="", description="user昵称")
    user_avatar: str = Field(default="", description="user头像地址")
    user_url_token: str = Field(default="", description="userurl_token")


class ZhihuComment(BaseModel):
    """
    Zhihucomment
    """

    comment_id: str = Field(default="", description="commentID")
    parent_comment_id: str = Field(default="", description="父commentID")
    content: str = Field(default="", description="commentcontent")
    publish_time: int = Field(default=0, description="发布时间")
    ip_location: Optional[str] = Field(default="", description="IP地理位置")
    sub_comment_count: int = Field(default=0, description="子comment数")
    like_count: int = Field(default=0, description="点赞数")
    dislike_count: int = Field(default=0, description="踩数")
    content_id: str = Field(default="", description="contentID")
    content_type: str = Field(default="", description="content类型(article | answer | zvideo)")

    user_id: str = Field(default="", description="userID")
    user_link: str = Field(default="", description="user主页链接")
    user_nickname: str = Field(default="", description="user昵称")
    user_avatar: str = Field(default="", description="user头像地址")


class ZhihuCreator(BaseModel):
    """
    Zhihu创作者
    """
    user_id: str = Field(default="", description="userID")
    user_link: str = Field(default="", description="user主页链接")
    user_nickname: str = Field(default="", description="user昵称")
    user_avatar: str = Field(default="", description="user头像地址")
    url_token: str = Field(default="", description="userurl_token")
    gender: str = Field(default="", description="user性别")
    ip_location: Optional[str] = Field(default="", description="IP地理位置")
    follows: int = Field(default=0, description="关注数")
    fans: int = Field(default=0, description="粉丝数")
    anwser_count: int = Field(default=0, description="回答数")
    video_count: int = Field(default=0, description="视频数")
    question_count: int = Field(default=0, description="提问数")
    article_count: int = Field(default=0, description="文章数")
    column_count: int = Field(default=0, description="专栏数")
    get_voteup_count: int = Field(default=0, description="获得的赞同数")

