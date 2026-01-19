# Repository パターンの実装

## 概要

Repository パターンを導入し、Domain層のRepository Interfaceを通じてデータアクセスを抽象化しました。これにより、テスタビリティと保守性が大幅に向上しています。

## アーキテクチャ

```
┌─────────────────────────────────────────┐
│         Router層 (routers/)              │
│   HTTPリクエスト/レスポンス処理          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Service層 (services/)             │
│   - Repository Interface経由でアクセス   │
│   - _get_repository()でDI                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Domain層 Repository Interfaces          │
│  (domain/repositories/)                  │
│   - MemoRepositoryInterface              │
│   - MailRepositoryInterface              │
│   - CornerRepositoryInterface            │
│   - ProgramRepositoryInterface           │
└─────────────────┬───────────────────────┘
                  │ implements
                  ▼
┌─────────────────────────────────────────┐
│  CRUD層 Repository実装                   │
│  (cruds/*_repository_impl.py)            │
│   - MemoRepositoryImpl                   │
│   - MailRepositoryImpl                   │
│   - CornerRepositoryImpl                 │
│   - ProgramRepositoryImpl                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Database層                      │
│   SQLite / SQLAlchemy ORM                │
└─────────────────────────────────────────┘
```

## ファイル構成

```
backend/
├── domain/
│   └── repositories/              # Repository Interfaces
│       ├── memo_repository.py
│       ├── mail_repository.py
│       ├── corner_repository.py
│       └── program_repository.py
│
├── cruds/                         # Repository実装
│   ├── memo_repository_impl.py    # MemoRepositoryInterface実装
│   ├── mail_repository_impl.py    # MailRepositoryInterface実装
│   ├── corner_repository_impl.py  # CornerRepositoryInterface実装
│   ├── program_repository_impl.py # ProgramRepositoryInterface実装
│   ├── memos.py                   # 後方互換ラッパー
│   ├── mails.py                   # 後方互換ラッパー
│   ├── corners.py                 # 後方互換ラッパー
│   └── programs.py                # 後方互換ラッパー
│
└── services/                      # Service層
    ├── memo_service.py            # Repository経由でアクセス
    ├── mail_service.py
    ├── corner_service.py
    └── program_service.py
```

## Repository Interface（抽象化）

### 例: MemoRepositoryInterface

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.memo_entity import MemoEntity

class MemoRepositoryInterface(ABC):
    """メモリポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        """IDでメモを取得"""
        pass
    
    @abstractmethod
    def find_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MemoEntity]:
        """ユーザーIDでメモ一覧を取得"""
        pass
    
    @abstractmethod
    def save(self, memo: MemoEntity) -> MemoEntity:
        """メモを保存"""
        pass
    
    @abstractmethod
    def delete(self, memo_id: int) -> bool:
        """メモを削除"""
        pass
```

## Repository実装

### 例: MemoRepositoryImpl

```python
from cruds.memo_repository_impl import MemoRepositoryImpl
from domain.repositories.memo_repository import MemoRepositoryInterface

class MemoRepositoryImpl(MemoRepositoryInterface):
    """メモリポジトリの実装クラス"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        """IDでメモを取得"""
        db_memo = self._db.query(Memo).filter(Memo.id == memo_id).first()
        if not db_memo:
            return None
        return self._to_entity(db_memo)
    
    # ... 他のメソッド実装
    
    @staticmethod
    def _to_entity(db_memo: Memo) -> MemoEntity:
        """DBモデルをエンティティに変換"""
        return MemoEntity(
            id=db_memo.id,
            user_id=db_memo.user_id,
            content=db_memo.content,
            created_at=db_memo.created_at
        )
```

## Service層での使用

### 依存性注入（DI）パターン

```python
from domain.repositories.memo_repository import MemoRepositoryInterface
from cruds.memo_repository_impl import MemoRepositoryImpl

def _get_repository(db: Session) -> MemoRepositoryInterface:
    """Repositoryインスタンスを取得（DI用）"""
    return MemoRepositoryImpl(db)

def get_memo(db: Session, memo_id: int) -> Optional[MemoResponse]:
    """メモを取得"""
    repo = _get_repository(db)  # Interface経由でアクセス
    return repo.get_by_id(memo_id)
```

### 利点

1. **テスタビリティ**: `_get_repository()`をモックに差し替え可能
2. **柔軟性**: 実装を切り替えやすい（例: Redis実装への変更）
3. **依存関係の明確化**: インターフェースへの依存のみ

## 後方互換性

既存のCRUDファイル（`cruds/memos.py`など）は後方互換ラッパーとして機能します。

```python
# cruds/memos.py
from cruds.memo_repository_impl import MemoRepositoryImpl

def get_memo(db: Session, memo_id: int) -> Optional[Memo]:
    """メモを取得（後方互換）"""
    repo = MemoRepositoryImpl(db)
    return repo.get_by_id(memo_id)
```

これにより、既存コードを壊さずに段階的な移行が可能です。

## エンティティ変換

Repository実装では、DBモデルとDomainエンティティ間の変換を行います。

```python
@staticmethod
def _to_entity(db_mail: Mail) -> MailEntity:
    """DBモデルをエンティティに変換"""
    return MailEntity(
        id=db_mail.id,
        corner_id=db_mail.corner_id,
        subject=db_mail.subject,
        body=db_mail.body,
        status=MailStatus.from_string(db_mail.status),  # Value Object変換
        sent_at=db_mail.sent_at,
        created_at=db_mail.created_at,
        updated_at=db_mail.updated_at
    )
```

## 実装済みRepository

| Interface | 実装クラス | 主な責務 |
|-----------|----------|---------|
| MemoRepositoryInterface | MemoRepositoryImpl | メモのCRUD |
| MailRepositoryInterface | MailRepositoryImpl | メールのCRUD・統計 |
| CornerRepositoryInterface | CornerRepositoryImpl | コーナーのCRUD |
| ProgramRepositoryInterface | ProgramRepositoryImpl | 番組のCRUD・関連付け |

## 今後の拡張

### 1. キャッシュリポジトリ実装

```python
class CachedMemoRepositoryImpl(MemoRepositoryInterface):
    """キャッシュ付きメモリポジトリ"""
    
    def __init__(self, db: Session, cache: Cache):
        self._db = db
        self._cache = cache
    
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        # キャッシュから取得を試みる
        cached = self._cache.get(f"memo:{memo_id}")
        if cached:
            return cached
        
        # DBから取得してキャッシュ
        memo = self._db.query(Memo).filter(Memo.id == memo_id).first()
        if memo:
            entity = self._to_entity(memo)
            self._cache.set(f"memo:{memo_id}", entity)
            return entity
        return None
```

### 2. テスト用インメモリ実装

```python
class InMemoryMemoRepository(MemoRepositoryInterface):
    """テスト用インメモリリポジトリ"""
    
    def __init__(self):
        self._memos = {}
    
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        return self._memos.get(memo_id)
    
    def save(self, memo: MemoEntity) -> MemoEntity:
        self._memos[memo.id] = memo
        return memo
```

### 3. 異なるデータストアへの対応

- PostgreSQL実装
- MongoDB実装
- Redis実装

Interfaceは変更せず、実装クラスのみ追加すればOK！

## 設計原則

1. **依存性逆転の原則（DIP）**: 上位層は抽象に依存
2. **単一責任の原則（SRP）**: Repositoryはデータアクセスのみ
3. **開放閉鎖の原則（OCP）**: 拡張に開いて、修正に閉じている
4. **リスコフの置換原則（LSP）**: 実装クラスは自由に置換可能

## まとめ

Repository パターンの導入により：

✅ **テスタビリティ向上**: モック・スタブの作成が容易
✅ **保守性向上**: データアクセスロジックが集約
✅ **柔軟性向上**: 実装の切り替えが容易
✅ **Domain層の独立性**: インフラ層への依存がゼロ

DDDの原則に忠実な、堅牢なアーキテクチャが完成しました！
