"""
バリューオブジェクト: メールアドレス
"""
import re
from typing import Optional


class EmailAddress:
    """メールアドレスのバリューオブジェクト"""
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, address: Optional[str]):
        if address and not self._is_valid(address):
            raise ValueError(f"Invalid email address: {address}")
        self._address = address
    
    @staticmethod
    def _is_valid(address: str) -> bool:
        """メールアドレスのバリデーション"""
        return bool(EmailAddress.EMAIL_PATTERN.match(address))
    
    @property
    def value(self) -> Optional[str]:
        """メールアドレス文字列を取得"""
        return self._address
    
    def __str__(self) -> str:
        return self._address or ""
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, EmailAddress):
            return False
        return self._address == other._address
    
    def __hash__(self) -> int:
        return hash(self._address)
