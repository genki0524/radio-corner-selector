"""
LangChainを使用した埋め込みとLLM推論サービス
"""
from typing import List, Dict, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from config import settings


class EmbeddingService:
    """埋め込みベクトル生成サービス"""
    
    def __init__(self):
        """HuggingFace埋め込みモデルを初期化"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def embed_text(self, text: str) -> List[float]:
        """
        テキストを埋め込みベクトルに変換
        
        Args:
            text: 埋め込み対象のテキスト
            
        Returns:
            埋め込みベクトル
        """
        return self.embeddings.embed_query(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        複数テキストを埋め込みベクトルに変換
        
        Args:
            texts: 埋め込み対象のテキストリスト
            
        Returns:
            埋め込みベクトルのリスト
        """
        return self.embeddings.embed_documents(texts)


class LLMReasoningService:
    """LLM推論サービス"""
    
    def __init__(self):
        """Ollama LLMを初期化"""
        self.llm = OllamaLLM(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=settings.ollama_temperature
        )
    
    def recommend_corner(
        self,
        memo_content: str,
        candidate_corners: List[Dict],
        max_candidates: int = 5
    ) -> Dict:
        """
        メモ内容から最適なコーナーを推薦
        
        Args:
            memo_content: メモの内容
            candidate_corners: ベクトル検索で見つかった候補コーナー
            max_candidates: 推論に使用する最大候補数
            
        Returns:
            推薦結果（corner_id, score, reasoning）
        """
        # 候補を制限
        candidates = candidate_corners[:max_candidates]
        
        # プロンプトテンプレートを作成
        template = """あなたはラジオ番組のコーナー選択アシスタントです。
以下のメモ内容に最も適したラジオコーナーを選択し、理由を説明してください。

メモ内容:
{memo_content}

候補コーナー:
{corners_info}

タスク:
1. メモ内容を分析し、適切なコーナーを1つ選択
2. 選択理由を簡潔に説明（2-3文）
3. 適合度を0.0-1.0のスコアで評価

以下の形式で回答してください:
推薦コーナーID: [corner_id]
スコア: [0.0-1.0]
理由: [選択理由]
"""
        
        # コーナー情報をフォーマット
        corners_info = self._format_corners_info(candidates)
        
        # プロンプトを作成
        prompt = PromptTemplate(
            input_variables=["memo_content", "corners_info"],
            template=template
        )
        
        # LLM推論を実行（LCEL使用）
        chain = prompt | self.llm
        result = chain.invoke({
            "memo_content": memo_content,
            "corners_info": corners_info
        })
        
        # 結果をパース
        return self._parse_llm_response(result, candidates)
    
    def _format_corners_info(self, corners: List[Dict]) -> str:
        """コーナー情報を整形"""
        formatted = []
        for i, corner in enumerate(corners, 1):
            formatted.append(
                f"{i}. ID: {corner['id']}\n"
                f"   タイトル: {corner['title']}\n"
                f"   説明: {corner['description_for_llm']}\n"
                f"   類似度: {corner.get('similarity', 0.0):.3f}"
            )
        return "\n\n".join(formatted)
    
    def _parse_llm_response(
        self,
        response: str,
        candidates: List[Dict]
    ) -> Dict:
        """LLMのレスポンスをパース"""
        lines = response.strip().split('\n')
        
        corner_id = None
        score = 0.5  # デフォルトスコア
        reasoning = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("推薦コーナーID:") or line.startswith("推奨コーナーID:"):
                try:
                    corner_id = int(line.split(":")[-1].strip())
                except ValueError:
                    pass
            elif line.startswith("スコア:"):
                try:
                    score_str = line.split(":")[-1].strip()
                    score = float(score_str)
                    score = max(0.0, min(1.0, score))  # 0-1に制限
                except ValueError:
                    pass
            elif line.startswith("理由:"):
                reasoning = line.split(":", 1)[-1].strip()
        
        # corner_idが取得できない場合は最初の候補を使用
        if corner_id is None and candidates:
            corner_id = candidates[0]["id"]
        
        # 理由が取得できない場合はデフォルトメッセージ
        if not reasoning:
            reasoning = "ベクトル類似度に基づく推薦です。"
        
        return {
            "corner_id": corner_id,
            "score": score,
            "reasoning": reasoning
        }
    
    def analyze_memo_for_corners(
        self,
        memo_content: str,
        all_corners: List[Dict]
    ) -> List[Dict]:
        """
        メモ内容を分析し、各コーナーとの適合度を評価
        
        Args:
            memo_content: メモの内容
            all_corners: 全コーナーのリスト
            
        Returns:
            各コーナーの評価結果リスト
        """
        template = """あなたはラジオ番組のコーナー選択アシスタントです。
以下のメモ内容が各コーナーにどの程度適しているか評価してください。

メモ内容:
{memo_content}

コーナー一覧:
{corners_list}

各コーナーについて、0.0-1.0のスコアで適合度を評価してください。
以下の形式で回答:
コーナーID [id]: スコア [score]
"""
        
        corners_list = "\n".join([
            f"- ID: {c['id']}, タイトル: {c['title']}, 説明: {c['description_for_llm']}"
            for c in all_corners
        ])
        
        prompt = PromptTemplate(
            input_variables=["memo_content", "corners_list"],
            template=template
        )
        
        # LLM推論を実行（LCEL使用）
        chain = prompt | self.llm
        result = chain.invoke({
            "memo_content": memo_content,
            "corners_list": corners_list
        })
        
        # 結果をパースして各コーナーのスコアを抽出
        return self._parse_multiple_scores(result, all_corners)
    
    def _parse_multiple_scores(
        self,
        response: str,
        corners: List[Dict]
    ) -> List[Dict]:
        """複数コーナーのスコアをパース"""
        scores = {}
        lines = response.strip().split('\n')
        
        for line in lines:
            if ":" in line:
                try:
                    parts = line.split(":")
                    if "コーナーID" in parts[0] or "ID" in parts[0]:
                        # ID部分を抽出
                        id_part = parts[0].split()[-1]
                        corner_id = int(id_part)
                        # スコア部分を抽出
                        score_part = parts[-1].strip()
                        score = float(score_part)
                        score = max(0.0, min(1.0, score))
                        scores[corner_id] = score
                except (ValueError, IndexError):
                    continue
        
        # 結果を構築
        results = []
        for corner in corners:
            results.append({
                **corner,
                "llm_score": scores.get(corner["id"], 0.5)
            })
        
        return results


# シングルトンインスタンス
_embedding_service: Optional[EmbeddingService] = None
_llm_service: Optional[LLMReasoningService] = None


def get_embedding_service() -> EmbeddingService:
    """埋め込みサービスのシングルトンインスタンスを取得"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def get_llm_service() -> LLMReasoningService:
    """LLMサービスのシングルトンインスタンスを取得"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMReasoningService()
    return _llm_service
