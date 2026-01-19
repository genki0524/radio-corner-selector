# レイヤードアーキテクチャ + ドメイン駆動設計（DDD）

## アーキテクチャ概要

このアプリケーションは、ドメイン駆動設計（DDD）を取り入れた4層のレイヤードアーキテクチャを採用しています。

```
┌─────────────────────────────────────────┐
│         Router層 (routers/)              │
│   HTTPリクエスト/レスポンス処理          │
│   - パラメータ検証                        │
│   - HTTPステータスコード管理              │
│   - エラーハンドリング                    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Service層 (services/)             │
│      アプリケーションロジック             │
│   - ユースケース実装                      │
│   - トランザクション管理                  │
│   - Domain層の組み立て                    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Domain層 (domain/)   ★NEW★       │
│      ビジネスロジック・ドメイン知識       │
│   - Entities（エンティティ）              │
│   - Value Objects（バリューオブジェクト） │
│   - Domain Services（ドメインサービス）   │
│   - Repository Interfaces                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         CRUD層 (cruds/)                  │
│       データアクセス処理                  │
│   - SQLクエリ実行                         │
│   - モデル操作                            │
│   - Repository実装                        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Database層                      │
│   SQLite / SQLAlchemy ORM                │
└─────────────────────────────────────────┘
```

## 各層の責務

### Router層 (`routers/`)
- HTTPリクエストの受付とレスポンス返却
- リクエストパラメータのバリデーション
- HTTPステータスコードの設定
- エラーハンドリング（404, 400など）
- **Service層のメソッドを呼び出す（下位層を直接呼ばない）**

### Service層 (`services/`)
- アプリケーションのユースケース実装
- トランザクション管理
- Domain層のエンティティやサービスを組み立て
- CRUD層を呼び出してデータ永続化
- **Domain層とCRUD層の橋渡し**

### Domain層 (`domain/`) ★NEW★
- **Entities**: ビジネスロジックを持つリッチなドメインオブジェクト
- **Value Objects**: 不変で値による等価性を持つオブジェクト
- **Domain Services**: 複数エンティティにまたがるビジネスロジック
- **Repository Interfaces**: データアクセスの抽象化
- **インフラ層への依存を持たない純粋なビジネスロジック**

### CRUD層 (`cruds/`)
- データベースへの直接アクセス
- SQLクエリの実行
- ORMモデルの操作
- Repository Interfaceの実装
- データの永続化処理

## ファイル構成

```
backend/
├── routers/              # Router層
│   ├── __init__.py
│   ├── analyze.py        # LLM解析API
│   ├── corners.py        # コーナー管理API
│   ├── mails.py          # メール管理API
│   ├── memos.py          # メモ管理API
│   ├── personalities.py  # パーソナリティ管理API
│   ├── profiles.py       # プロフィール管理API
│   └── programs.py       # 番組管理API
│
├── services/             # Service層
│   ├── __init__.py
│   ├── analyze_service.py       # LLM解析サービス
│   ├── corner_service.py        # コーナーサービス
│   ├── mail_service.py          # メールサービス
│   ├── memo_service.py          # メモサービス
│   ├── personality_service.py   # パーソナリティサービス
│   ├── profile_service.py       # プロフィールサービス
│   └── program_service.py       # 番組サービス
│
├── domain/               # Domain層 ★NEW★
│   ├── entities/         # エンティティ
│   │   ├── memo_entity.py
│   │   ├── mail_entity.py
│   │   ├── corner_entity.py
│   │   └── program_entity.py
│   ├── value_objects/    # バリューオブジェクト
│   │   ├── mail_status.py
│   │   ├── email_address.py
│   │   └── recommendation_score.py
│   ├── services/         # ドメインサービス
│   │   ├── mail_creation_service.py
│   │   ├── corner_recommendation_service.py
│   │   └── mail_statistics_service.py
│   └── repositories/     # リポジトリIF
│       ├── memo_repository.py
│       ├── mail_repository.py
│       ├── corner_repository.py
│       └── program_repository.py
│
└── cruds/                # CRUD層
    ├── __init__.py
    ├── analyze.py        # LLM解析CRUD
    ├── corners.py        # コーナーCRUD
    ├── mails.py          # メールCRUD
    ├── memos.py          # メモCRUD
    ├── personalities.py  # パーソナリティCRUD
    ├── profiles.py       # プロフィールCRUD
    └── programs.py       # 番組CRUD
```

## Domain層の詳細

### 1. Entities（エンティティ）
ビジネスロジックを持つリッチなドメインオブジェクト

```python
# 例: MailEntity
class MailEntity:
    def change_status(self, new_status: MailStatus) -> None:
        """ステータス変更のビジネスルール"""
        if not self._status.can_transition_to(new_status):
            raise ValueError("Invalid status transition")
        self._status = new_status
```

### 2. Value Objects（バリューオブジェクト）
不変で値による等価性を持つオブジェクト

```python
# 例: MailStatus
class MailStatus(str, Enum):
    DRAFT = "下書き"
    SENT = "送信済み"
    ACCEPTED = "採用"
    REJECTED = "不採用"
    
    def can_transition_to(self, new_status) -> bool:
        """ステータス遷移ルール"""
        # ビジネスルールを実装
```

### 3. Domain Services（ドメインサービス）
複数エンティティにまたがるビジネスロジック

```python
# 例: MailCreationService
class MailCreationService:
    @staticmethod
    def create_mail_draft_from_memo(
        memo: MemoEntity,
        corner: CornerEntity,
        program: ProgramEntity
    ) -> dict:
        """メモから下書きを生成"""
        # 複数エンティティを使ったビジネスロジック
```

### 4. Repository Interfaces
データアクセスの抽象化

```python
# 例: MemoRepositoryInterface
class MemoRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        pass
```

## データフロー例

### メモ作成の例

1. **Router層** (`routers/memos.py`)
   ```python
   @router.post("", response_model=MemoResponse)
   def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
       return memo_service.create_memo(db, memo)
   ```

2. **Service層** (`services/memo_service.py`)
   ```python
   def create_memo(db: Session, memo: MemoCreate) -> MemoResponse:
       return memo_crud.create_memo(db, memo.model_dump())
   ```

3. **CRUD層** (`cruds/memos.py`)
   ```python
   def create_memo(db: Session, memo_data: dict) -> Memo:
       db_memo = Memo(**memo_data)
       db.add(db_memo)
       db.commit()
       return db_memo
   ```

### メールステータス変更の例（Domain層活用）

1. **Router層** → **Service層**
2. **Service層**:
   ```python
   # Domain層のエンティティを使用
   mail_entity = MailEntity(...)
   mail_entity.change_status(MailStatus.SENT)  # ビジネスルール適用
   ```
3. **CRUD層**: エンティティの状態を永続化

## 設計原則

1. **単一責任の原則**: 各層は明確な責務を持つ
2. **依存性の方向**: Router → Service → Domain → CRUD → Database の一方向
3. **ドメインの独立性**: Domain層はインフラ層に依存しない
4. **疎結合**: 各層はインターフェースを介して通信
5. **テスタビリティ**: 各層を独立してテスト可能

## DDDの利点

- **ビジネスロジックの明確化**: ドメイン知識がコードに直接表現される
- **変更容易性**: ビジネスルールの変更箇所が明確
- **テスタビリティ**: ドメインロジックを独立してテスト可能
- **保守性**: 責務が明確で影響範囲が限定的
- **再利用性**: ドメインロジックを複数の層から利用可能

## アーキテクチャの利点

- **保守性**: 責務が明確で変更箇所が特定しやすい
- **拡張性**: 新機能追加時に影響範囲が限定される
- **再利用性**: Service層・Domain層のロジックを複数箇所から利用可能
- **テスト容易性**: 各層を独立してモックやスタブでテスト可能
- **ビジネスロジックの明確化**: Domain層にビジネス知識が集約

## 参考ドキュメント

- **DOMAIN_LAYER.md**: Domain層の詳細設計とDDDの解説
- **README.md**: プロジェクト全体の概要
