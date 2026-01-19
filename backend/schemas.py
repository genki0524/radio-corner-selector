"""
Pydanticスキーマ定義
リクエスト/レスポンス用のデータバリデーション
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ========== User ==========
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== Profile ==========
class ProfileBase(BaseModel):
    name: str = Field(..., max_length=100)
    radio_name: str = Field(..., max_length=100)
    real_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True


# ========== Personality ==========
class PersonalityBase(BaseModel):
    name: str = Field(..., max_length=100)
    nickname: Optional[str] = Field(None, max_length=100)


class PersonalityCreate(PersonalityBase):
    user_id: int


class PersonalityUpdate(PersonalityBase):
    pass


class PersonalityResponse(PersonalityBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True


# ========== Corner ==========
class CornerBase(BaseModel):
    title: str = Field(..., max_length=255)
    description_for_llm: str


class CornerCreate(CornerBase):
    program_id: int


class CornerUpdate(CornerBase):
    pass


class CornerResponse(CornerBase):
    id: int
    program_id: int
    
    class Config:
        from_attributes = True


# ========== Program ==========
class ProgramBase(BaseModel):
    title: str = Field(..., max_length=255)
    email_address: Optional[str] = Field(None, max_length=255)
    broadcast_schedule: Optional[str] = Field(None, max_length=255)
    default_profile_id: Optional[int] = None


class ProgramCreate(ProgramBase):
    user_id: int
    personality_ids: List[int] = Field(default_factory=list)
    corners: List[CornerBase] = Field(default_factory=list)


class ProgramUpdate(ProgramBase):
    personality_ids: Optional[List[int]] = None


class ProgramResponse(ProgramBase):
    id: int
    user_id: int
    corners: List[CornerResponse] = []
    personalities: List[PersonalityResponse] = []
    
    class Config:
        from_attributes = True


# ========== Memo ==========
class MemoBase(BaseModel):
    content: str


class MemoCreate(MemoBase):
    user_id: int


class MemoUpdate(MemoBase):
    pass


class MemoResponse(MemoBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Mail ==========
class MailBase(BaseModel):
    subject: str = Field(..., max_length=255)
    body: str
    status: str = Field(default="下書き", pattern="^(下書き|送信済み|採用|不採用)$")


class MailCreate(MailBase):
    corner_id: int
    memo_id: Optional[int] = None


class MailUpdate(BaseModel):
    subject: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(下書き|送信済み|採用|不採用)$")
    sent_at: Optional[datetime] = None


class MailResponse(MailBase):
    id: int
    corner_id: int
    memo_id: Optional[int]
    sent_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== LLM Analysis ==========
class AnalyzeRequest(BaseModel):
    """メモ解析リクエスト"""
    memo_id: int
    user_id: int


class CornerRecommendation(BaseModel):
    """コーナー推奨結果"""
    corner_id: int
    corner_title: str
    program_id: int
    program_title: str
    score: float = Field(..., ge=0.0, le=1.0, description="一致度スコア (0.0-1.0)")
    reason: str = Field(..., description="推奨理由")


class AnalyzeResponse(BaseModel):
    """メモ解析レスポンス"""
    memo_id: int
    recommendations: List[CornerRecommendation]
    
    class Config:
        from_attributes = True


# ========== Statistics ==========
class MailStatsResponse(BaseModel):
    """メール統計レスポンス"""
    total: int
    draft: int
    sent: int
    accepted: int
    rejected: int
