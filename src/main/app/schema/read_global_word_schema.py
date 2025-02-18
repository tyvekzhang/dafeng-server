"""GlobalWord schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class GlobalWordPage(BaseModel):
    """
    阅读词库分页信息
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = 0
    # 创建时间
    createTime: Optional[datetime] = None

class GlobalWordQuery(PageBase):
    """
    阅读词库查询参数
    """
    # 主键
    id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = None
    # 创建时间
    createTime: Optional[datetime] = None

class GlobalWordCreate(BaseModel):
    """
    阅读词库新增
    """
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = 0
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class GlobalWordModify(BaseModel):
    """
    阅读词库更新
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = 0

class GlobalWordBatchModify(BaseModel):
    """
    阅读词库批量更新
    """
    ids: List[int]
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = 0

class GlobalWordDetail(BaseModel):
    """
    阅读词库详情
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 国际音标
    pronunciation: Optional[str] = None
    # 美式音标
    pronunciationUs: Optional[str] = None
    # 定义
    definition: Optional[str] = None
    # 例句
    example: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 单词音频
    wordSrc: Optional[str] = None
    # 美式音频
    wordSrcUs: Optional[str] = None
    # 例句音频
    exampleSrc: Optional[str] = None
    # 复数
    pluralForm: Optional[str] = None
    # 人称单数
    thirdPersonSingular: Optional[str] = None
    # 进行时
    presentTenseContinuous: Optional[str] = None
    # 过去式
    pastTense: Optional[str] = None
    # 过去分词
    pastParticiple: Optional[str] = None
    # 等级
    level: Optional[int] = None
    # 版本
    version: Optional[str] = None
    # 标签
    tag: Optional[str] = None
    # 状态
    status: Optional[int] = 0
    # 创建时间
    createTime: Optional[datetime] = None