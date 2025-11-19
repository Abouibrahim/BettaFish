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


class TiebaNote(BaseModel):
    """
    百度Tieba帖子
    """
    note_id: str = Field(..., description="帖子ID")
    title: str = Field(..., description="帖子标题")
    desc: str = Field(default="", description="帖子描述")
    note_url: str = Field(..., description="帖子链接")
    publish_time: str = Field(default="", description="发布时间")
    user_link: str = Field(default="", description="user主页链接")
    user_nickname: str = Field(default="", description="user昵称")
    user_avatar: str = Field(default="", description="user头像地址")
    tieba_name: str = Field(..., description="Tieba名称")
    tieba_link: str = Field(..., description="Tieba链接")
    total_replay_num: int = Field(default=0, description="回复总数")
    total_replay_page: int = Field(default=0, description="回复总页数")
    ip_location: Optional[str] = Field(default="", description="IP地理位置")
    source_keyword: str = Field(default="", description="来源keyword")


class TiebaComment(BaseModel):
    """
    百度Tiebacomment
    """

    comment_id: str = Field(..., description="commentID")
    parent_comment_id: str = Field(default="", description="父commentID")
    content: str = Field(..., description="commentcontent")
    user_link: str = Field(default="", description="user主页链接")
    user_nickname: str = Field(default="", description="user昵称")
    user_avatar: str = Field(default="", description="user头像地址")
    publish_time: str = Field(default="", description="发布时间")
    ip_location: Optional[str] = Field(default="", description="IP地理位置")
    sub_comment_count: int = Field(default=0, description="子comment数")
    note_id: str = Field(..., description="帖子ID")
    note_url: str = Field(..., description="帖子链接")
    tieba_id: str = Field(..., description="所属的TiebaID")
    tieba_name: str = Field(..., description="所属的Tieba名称")
    tieba_link: str = Field(..., description="Tieba链接")


class TiebaCreator(BaseModel):
    """
    百度Tieba创作者
    """
    user_id: str = Field(..., description="userID")
    user_name: str = Field(..., description="user名")
    nickname: str = Field(..., description="user昵称")
    gender: str = Field(default="", description="user性别")
    avatar: str = Field(..., description="user头像地址")
    ip_location: Optional[str] = Field(default="", description="IP地理位置")
    follows: int = Field(default=0, description="关注数")
    fans: int = Field(default=0, description="粉丝数")
    registration_duration: str = Field(default="", description="注册时长")
