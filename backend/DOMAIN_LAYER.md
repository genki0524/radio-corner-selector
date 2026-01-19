# Domain層（ドメイン駆動設計）

## 概要

Domain層は、ビジネスロジックとドメイン知識を集約した層です。ドメイン駆動設計（DDD）の原則に基づき、以下の要素で構成されています。

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
│      アプリケーションロジック             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Domain層 (domain/)                │
│      ビジネスロジック・ドメイン知識       │
│  ┌─────────────────────────────────┐   │
│  │ Entities (エンティティ)          │   │
│  │ - MemoEntity                     │   │
│  │ - MailEntity                     │   │
│  │ - CornerEntity                   │   │
│  │ - ProgramEntity                  │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Value Objects (バリューオブジェクト)│   │
│  │ - MailStatus                     │   │
│  │ - EmailAddress                   │   │
│  │ - RecommendationScore            │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Domain Services                  │   │
│  │ - MailCreationService            │   │
│  │ - CornerRecommendationService    │   │
│  │ - MailStatisticsService          │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Repository Interfaces            │   │
│  │ - MemoRepositoryInterface        │   │
│  │ - MailRepositoryInterface        │   │
│  │ - CornerRepositoryInterface      │   │
│  │ - ProgramRepositoryInterface     │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         CRUD層 (cruds/)                  │
│   Repository実装・データアクセス         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Database層                      │
│   SQLite / SQLAlchemy ORM                │
└─────────────────────────────────────────┘
```

## Domain層の構成要素

### 1. Entities（エンティティ）

**責務**: ビジネスロジックを持つリッチなドメインオブジェクト

```python
# domain/entities/
├── memo_entity.py          # メモエンティティ
├── mail_entity.py          # メールエンティティ
├── corner_entity.py        # コーナーエンティティ
└── program_entity.py       # 番組エンティティ
```

**特徴**:
- 一意な識別子（ID）を持つ
- ビジネスルールを持つメソッドを実装
- 状態の変更を内部でカプセル化

**例**:
```python
class MailEntity:
    def change_status(self, new_status: MailStatus) -> None:
        """ステータス変更時のビジネスルールを実装"""
        if not self._status.can_transition_to(new_status):
            raise ValueError("Invalid status transition")
        self._status = new_status
```

### 2. Value Objects（バリューオブジェクト）

**責務**: 不変で値による等価性を持つオブジェクト

```python
# domain/value_objects/
├── mail_status.py           # メールステータス
├── email_address.py         # メールアドレス
└── recommendation_score.py  # 推奨スコア
```

**特徴**:
- 不変（immutable）
- 値による等価性判定
- バリデーションロジックを内包

**例**:
```python
class MailStatus(str, Enum):
    DRAFT = "下書き"
    SENT = "送信済み"
    
    def can_transition_to(self, new_status: "MailStatus") -> bool:
        """ステータス遷移ルール"""
        transitions = {
            self.DRAFT: [self.SENT],
            self.SENT: [self.ACCEPTED, self.REJECTED],
        }
        return new_status in transitions.get(self, [])
```

### 3. Domain Services（ドメインサービス）

**責務**: 複数エンティティにまたがるビジネスロジック

```python
# domain/services/
├── mail_creation_service.py       # メール作成ロジック
├── corner_recommendation_service.py  # コーナー推奨ロジック
└── mail_statistics_service.py     # メール統計ロジック
```

**特徴**:
- ステートレス（状態を持たない）
- 複数のエンティティを組み合わせた処理
- ドメインロジックを純粋に表現

**例**:
```python
class MailCreationService:
    @staticmethod
    def create_mail_draft_from_memo(
        memo: MemoEntity,
        corner: CornerEntity,
        program: ProgramEntity
    ) -> dict:
        """メモから下書きを生成するドメインロジック"""
        # ビジネスルールに基づいた件名・本文生成
        subject = f"{program.title} - {corner.title}への投稿"
        return {"subject": subject, "body": memo.content}
```

### 4. Repository Interfaces（リポジトリインターフェース）

**責務**: データアクセスの抽象化

```python
# domain/repositories/
├── memo_repository.py      # メモリポジトリIF
├── mail_repository.py      # メールリポジトリIF
├── corner_repository.py    # コーナーリポジトリIF
└── program_repository.py   # 番組リポジトリIF
```

**特徴**:
- 抽象基底クラス（ABC）で定義
- CRUD層がこのインターフェースを実装
- Domain層がインフラ層に依存しない

**例**:
```python
class MemoRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, memo_id: int) -> Optional[MemoEntity]:
        """IDでメモを取得"""
        pass
```

## ディレクトリ構造

```
backend/domain/
├── __init__.py
├── entities/                    # エンティティ
│   ├── __init__.py
│   ├── memo_entity.py
│   ├── mail_entity.py
│   ├── corner_entity.py
│   └── program_entity.py
├── value_objects/               # バリューオブジェクト
│   ├── __init__.py
│   ├── mail_status.py
│   ├── email_address.py
│   └── recommendation_score.py
├── services/                    # ドメインサービス
│   ├── __init__.py
│   ├── mail_creation_service.py
│   ├── corner_recommendation_service.py
│   └── mail_statistics_service.py
└── repositories/                # リポジトリIF
    ├── __init__.py
    ├── memo_repository.py
    ├── mail_repository.py
    ├── corner_repository.py
    └── program_repository.py
```

## DDDの主要な利点

### 1. ビジネスロジックの明確化
- ドメイン知識がコードに直接表現される
- ビジネスルールの変更箇所が明確

### 2. テスタビリティ
- ドメインロジックを独立してテスト可能
- インフラ層への依存がない

### 3. 保守性
- 責務が明確で変更の影響範囲が限定的
- ビジネスロジックとデータアクセスの分離

### 4. 再利用性
- ドメインロジックを複数の層から利用可能
- インフラの実装を変更してもドメインは不変

## ビジネスルールの例

### メールステータス遷移
```
下書き → 送信済み → 採用/不採用
```
- `MailStatus`バリューオブジェクトで実装
- 不正な遷移を防止

### メール作成ルール
- メモの内容から件名・本文を生成
- 番組にメールアドレスが設定されていない場合はエラー
- `MailCreationService`で実装

### コーナー推奨ルール
- スコア0.8以上: 高信頼度
- スコア0.3以下: 低信頼度（警告表示）
- `CornerRecommendationService`で実装

## 設計原則

1. **ドメインモデルの独立性**: インフラ層への依存を排除
2. **ユビキタス言語**: ビジネス用語をそのままコードに反映
3. **エンティティの自律性**: ビジネスルールはエンティティ内に実装
4. **不変性**: バリューオブジェクトは不変
5. **インターフェース分離**: リポジトリはインターフェースで抽象化

## 今後の拡張

- ドメインイベント（Domain Events）の追加
- 集約（Aggregate）の明確化
- 仕様パターン（Specification Pattern）の導入
- ファクトリーパターンの追加
