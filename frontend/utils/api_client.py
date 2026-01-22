"""
バックエンドAPI通信クライアント
"""
import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime


class APIClient:
    """バックエンドAPIとの通信を管理するクライアント"""
    
    def __init__(self, base_url: str = None):
        if base_url is None:
            base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.user_id = 1  # デフォルトユーザーID（認証実装後に変更）
    
    def _handle_response(self, response: requests.Response) -> Any:
        """レスポンスを処理"""
        if response.status_code >= 400:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        return response.json()
    
    # ========== メモ ==========
    def get_memos(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """メモ一覧を取得"""
        response = requests.get(
            f"{self.api_base}/memos",
            params={"user_id": self.user_id, "skip": skip, "limit": limit}
        )
        return self._handle_response(response)
    
    def get_memo(self, memo_id: int) -> Dict[str, Any]:
        """メモを取得"""
        response = requests.get(f"{self.api_base}/memos/{memo_id}")
        return self._handle_response(response)
    
    def create_memo(self, content: str) -> Dict[str, Any]:
        """メモを作成"""
        response = requests.post(
            f"{self.api_base}/memos",
            json={"content": content, "user_id": self.user_id}
        )
        return self._handle_response(response)
    
    def update_memo(self, memo_id: int, content: str) -> Dict[str, Any]:
        """メモを更新"""
        response = requests.put(
            f"{self.api_base}/memos/{memo_id}",
            json={"content": content}
        )
        return self._handle_response(response)
    
    def delete_memo(self, memo_id: int) -> None:
        """メモを削除"""
        response = requests.delete(f"{self.api_base}/memos/{memo_id}")
        if response.status_code != 204:
            raise Exception(f"Failed to delete memo: {response.status_code}")
    
    # ========== プロフィール ==========
    def get_profiles(self) -> List[Dict[str, Any]]:
        """プロフィール一覧を取得"""
        response = requests.get(
            f"{self.api_base}/profiles",
            params={"user_id": self.user_id}
        )
        return self._handle_response(response)
    
    def get_profile(self, profile_id: int) -> Dict[str, Any]:
        """プロフィールを取得"""
        response = requests.get(f"{self.api_base}/profiles/{profile_id}")
        return self._handle_response(response)
    
    def create_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """プロフィールを作成"""
        data["user_id"] = self.user_id
        response = requests.post(f"{self.api_base}/profiles", json=data)
        return self._handle_response(response)
    
    def update_profile(self, profile_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """プロフィールを更新"""
        response = requests.put(f"{self.api_base}/profiles/{profile_id}", json=data)
        return self._handle_response(response)
    
    def delete_profile(self, profile_id: int) -> None:
        """プロフィールを削除"""
        response = requests.delete(f"{self.api_base}/profiles/{profile_id}")
        if response.status_code != 204:
            raise Exception(f"Failed to delete profile: {response.status_code}")
    
    # ========== パーソナリティ ==========
    def get_personalities(self) -> List[Dict[str, Any]]:
        """パーソナリティ一覧を取得"""
        response = requests.get(
            f"{self.api_base}/personalities",
            params={"user_id": self.user_id}
        )
        return self._handle_response(response)
    
    def get_personality(self, personality_id: int) -> Dict[str, Any]:
        """パーソナリティを取得"""
        response = requests.get(f"{self.api_base}/personalities/{personality_id}")
        return self._handle_response(response)
    
    def create_personality(self, name: str, nickname: Optional[str] = None) -> Dict[str, Any]:
        """パーソナリティを作成"""
        data = {"name": name, "nickname": nickname, "user_id": self.user_id}
        response = requests.post(f"{self.api_base}/personalities", json=data)
        return self._handle_response(response)
    
    def update_personality(self, personality_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """パーソナリティを更新"""
        response = requests.put(f"{self.api_base}/personalities/{personality_id}", json=data)
        return self._handle_response(response)
    
    def delete_personality(self, personality_id: int) -> None:
        """パーソナリティを削除"""
        response = requests.delete(f"{self.api_base}/personalities/{personality_id}")
        if response.status_code != 204:
            raise Exception(f"Failed to delete personality: {response.status_code}")
    
    # ========== 番組 ==========
    def get_programs(
        self,
        personality_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """番組一覧を取得"""
        params = {"user_id": self.user_id}
        if personality_id:
            params["personality_id"] = personality_id
        if search:
            params["search"] = search
        
        response = requests.get(f"{self.api_base}/programs", params=params)
        return self._handle_response(response)
    
    def get_program(self, program_id: int) -> Dict[str, Any]:
        """番組を取得"""
        response = requests.get(f"{self.api_base}/programs/{program_id}")
        return self._handle_response(response)
    
    def create_program(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """番組を作成"""
        data["user_id"] = self.user_id
        response = requests.post(f"{self.api_base}/programs", json=data)
        return self._handle_response(response)
    
    def update_program(self, program_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """番組を更新"""
        response = requests.put(f"{self.api_base}/programs/{program_id}", json=data)
        return self._handle_response(response)
    
    def delete_program(self, program_id: int) -> None:
        """番組を削除"""
        response = requests.delete(f"{self.api_base}/programs/{program_id}")
        if response.status_code != 204:
            raise Exception(f"Failed to delete program: {response.status_code}")
    
    # ========== コーナー ==========
    def get_corners(self, program_id: int) -> List[Dict[str, Any]]:
        """コーナー一覧を取得"""
        response = requests.get(
            f"{self.api_base}/corners",
            params={"program_id": program_id}
        )
        return self._handle_response(response)
    
    def create_corner(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """コーナーを作成"""
        response = requests.post(f"{self.api_base}/corners", json=data)
        return self._handle_response(response)
    
    # ========== メール ==========
    def get_mails(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """メール一覧を取得"""
        params = {"user_id": self.user_id}
        if status_filter:
            params["status_filter"] = status_filter
        
        response = requests.get(f"{self.api_base}/mails", params=params)
        return self._handle_response(response)
    
    def get_mail_stats(self) -> Dict[str, int]:
        """メール統計を取得"""
        response = requests.get(
            f"{self.api_base}/mails/stats",
            params={"user_id": self.user_id}
        )
        return self._handle_response(response)
    
    def create_mail(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """メールを作成"""
        response = requests.post(f"{self.api_base}/mails", json=data)
        return self._handle_response(response)
    
    def update_mail(self, mail_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """メールを更新"""
        response = requests.put(f"{self.api_base}/mails/{mail_id}", json=data)
        return self._handle_response(response)
    
    # ========== LLM解析 ==========
    def analyze_memo(self, memo_id: int) -> Dict[str, Any]:
        """メモを解析して推奨コーナーを取得"""
        response = requests.post(
            f"{self.api_base}/analyze",
            json={"memo_id": memo_id, "user_id": self.user_id}
        )
        return self._handle_response(response)


# シングルトンインスタンス
api_client = APIClient()
