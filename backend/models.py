"""
SQLAlchemyモデル定義
ER図に基づいたデータベースモデル
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# 多対多の中間テーブル
program_personalities = Table(
    "program_personalities",
    Base.metadata,
    Column("program_id", Integer, ForeignKey("programs.id"), primary_key=True),
    Column("personality_id", Integer, ForeignKey("personalities.id"), primary_key=True),
)


class User(Base):
    """ユーザーモデル"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    # リレーション
    profiles: Mapped[List["Profile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    programs: Mapped[List["Program"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    personalities: Mapped[List["Personality"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    memos: Mapped[List["Memo"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    """プロフィール（投稿用署名）モデル"""
    __tablename__ = "profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))  # 管理用名称
    radio_name: Mapped[str] = mapped_column(String(100))  # ラジオネーム
    real_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 本名
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # 住所
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 電話番号
    
    # リレーション
    user: Mapped["User"] = relationship(back_populates="profiles")
    programs: Mapped[List["Program"]] = relationship(back_populates="default_profile")


class Personality(Base):
    """パーソナリティモデル"""
    __tablename__ = "personalities"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100), index=True)  # 名前
    nickname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 愛称
    
    # リレーション
    user: Mapped["User"] = relationship(back_populates="personalities")
    programs: Mapped[List["Program"]] = relationship(
        secondary=program_personalities,
        back_populates="personalities"
    )


class Program(Base):
    """番組モデル"""
    __tablename__ = "programs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    default_profile_id: Mapped[Optional[int]] = mapped_column(ForeignKey("profiles.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), index=True)  # 番組名
    email_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # 投稿先メアド
    broadcast_schedule: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # 放送日時
    
    # リレーション
    user: Mapped["User"] = relationship(back_populates="programs")
    default_profile: Mapped[Optional["Profile"]] = relationship(back_populates="programs")
    corners: Mapped[List["Corner"]] = relationship(back_populates="program", cascade="all, delete-orphan")
    personalities: Mapped[List["Personality"]] = relationship(
        secondary=program_personalities,
        back_populates="programs"
    )


class Corner(Base):
    """コーナーモデル"""
    __tablename__ = "corners"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"))
    title: Mapped[str] = mapped_column(String(255))  # コーナー名
    description_for_llm: Mapped[str] = mapped_column(Text)  # LLM用コーナー説明
    
    # リレーション
    program: Mapped["Program"] = relationship(back_populates="corners")
    mails: Mapped[List["Mail"]] = relationship(back_populates="corner", cascade="all, delete-orphan")


class Memo(Base):
    """メモモデル"""
    __tablename__ = "memos"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)  # メモ内容
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # リレーション
    user: Mapped["User"] = relationship(back_populates="memos")
    mails: Mapped[List["Mail"]] = relationship(back_populates="memo")


class Mail(Base):
    """メールモデル"""
    __tablename__ = "mails"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    corner_id: Mapped[int] = mapped_column(ForeignKey("corners.id"))
    memo_id: Mapped[Optional[int]] = mapped_column(ForeignKey("memos.id"), nullable=True)
    subject: Mapped[str] = mapped_column(String(255))  # 件名
    body: Mapped[str] = mapped_column(Text)  # 本文
    status: Mapped[str] = mapped_column(String(20), default="下書き")  # ステータス
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # リレーション
    corner: Mapped["Corner"] = relationship(back_populates="mails")
    memo: Mapped[Optional["Memo"]] = relationship(back_populates="mails")
