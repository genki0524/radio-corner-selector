"""
番組リポジトリ実装
Repository Interfaceの具体的な実装
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Program, Personality, program_personalities
from domain.repositories.program_repository import ProgramRepositoryInterface
from domain.entities.program_entity import ProgramEntity
from domain.value_objects.email_address import EmailAddress


class ProgramRepositoryImpl(ProgramRepositoryInterface):
    """番組リポジトリの実装クラス"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def find_by_id(self, program_id: int) -> Optional[ProgramEntity]:
        """IDで番組を取得"""
        db_program = self._db.query(Program).filter(Program.id == program_id).first()
        if not db_program:
            return None
        return self._to_entity(db_program)
    
    def find_by_user_id(
        self,
        user_id: int,
        personality_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[ProgramEntity]:
        """ユーザーIDで番組一覧を取得"""
        query = self._db.query(Program).filter(Program.user_id == user_id)
        
        if personality_id:
            query = query.join(
                program_personalities,
                Program.id == program_personalities.c.program_id
            ).filter(program_personalities.c.personality_id == personality_id)
        
        if search:
            query = query.filter(Program.title.contains(search))
        
        db_programs = query.all()
        return [self._to_entity(program) for program in db_programs]
    
    def save(self, program: ProgramEntity) -> ProgramEntity:
        """番組を保存（新規作成または更新）"""
        db_program = self._db.query(Program).filter(Program.id == program.id).first()
        
        email_value = program.email_address.value if program.email_address else None
        
        if db_program:
            # 更新
            db_program.title = program.title
            db_program.email_address = email_value
            db_program.broadcast_schedule = program.broadcast_schedule
            db_program.default_profile_id = program.default_profile_id
        else:
            # 新規作成
            db_program = Program(
                id=program.id,
                user_id=program.user_id,
                title=program.title,
                email_address=email_value,
                broadcast_schedule=program.broadcast_schedule,
                default_profile_id=program.default_profile_id
            )
            self._db.add(db_program)
        
        self._db.commit()
        self._db.refresh(db_program)
        return self._to_entity(db_program)
    
    def delete(self, program_id: int) -> bool:
        """番組を削除"""
        db_program = self._db.query(Program).filter(Program.id == program_id).first()
        if not db_program:
            return False
        
        self._db.delete(db_program)
        self._db.commit()
        return True
    
    def create_from_dict(
        self,
        program_data: dict,
        personality_ids: List[int],
        corners_data: Optional[List[dict]] = None
    ) -> Program:
        """辞書から番組を作成（後方互換性のため）"""
        from models import Corner
        
        db_program = Program(**program_data)
        self._db.add(db_program)
        self._db.flush()
        
        # パーソナリティの関連付け
        if personality_ids:
            personalities = (
                self._db.query(Personality)
                .filter(Personality.id.in_(personality_ids))
                .all()
            )
            db_program.personalities = personalities
        
        # コーナーの作成
        if corners_data:
            for corner_data in corners_data:
                corner_data['program_id'] = db_program.id
                db_corner = Corner(**corner_data)
                self._db.add(db_corner)
        
        self._db.commit()
        self._db.refresh(db_program)
        return db_program
    
    def update_from_dict(
        self,
        program_id: int,
        program_data: dict,
        personality_ids: Optional[List[int]] = None
    ) -> Optional[Program]:
        """辞書で番組を更新（後方互換性のため）"""
        db_program = self._db.query(Program).filter(Program.id == program_id).first()
        if not db_program:
            return None
        
        for key, value in program_data.items():
            setattr(db_program, key, value)
        
        # パーソナリティの更新
        if personality_ids is not None:
            personalities = (
                self._db.query(Personality)
                .filter(Personality.id.in_(personality_ids))
                .all()
            )
            db_program.personalities = personalities
        
        self._db.commit()
        self._db.refresh(db_program)
        return db_program
    
    def get_by_id(self, program_id: int) -> Optional[Program]:
        """IDで番組を取得（後方互換性のため）"""
        return self._db.query(Program).filter(Program.id == program_id).first()
    
    def get_by_user_id(
        self,
        user_id: int,
        personality_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Program]:
        """ユーザーIDで番組一覧を取得（後方互換性のため）"""
        query = self._db.query(Program).filter(Program.user_id == user_id)
        
        if personality_id:
            query = query.join(
                program_personalities,
                Program.id == program_personalities.c.program_id
            ).filter(program_personalities.c.personality_id == personality_id)
        
        if search:
            query = query.filter(Program.title.contains(search))
        
        return query.all()
    
    @staticmethod
    def _to_entity(db_program: Program) -> ProgramEntity:
        """DBモデルをエンティティに変換"""
        email_addr = None
        if db_program.email_address:
            email_addr = EmailAddress(db_program.email_address)
        
        return ProgramEntity(
            id=db_program.id,
            user_id=db_program.user_id,
            title=db_program.title,
            email_address=email_addr,
            broadcast_schedule=db_program.broadcast_schedule,
            default_profile_id=db_program.default_profile_id
        )
