import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.schemas.analysis import AnalysisResponse

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーの設定
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY が .env ファイルに設定されていません！")

genai.configure(api_key=API_KEY)

async def analyze_text_with_gemini(text_input: str) -> AnalysisResponse:
    """
    Geminiを使ってテキストデータを分析し、3Dグラフ用のJSONデータを生成する
    """
    
    # 使用するモデル (高速・軽量な Flash モデル推奨)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # AIへの命令書 (プロンプト)
    # ここで「JSONで返せ」「こういう構造にしろ」と厳しく指示します
    prompt = f"""
    あなたはプロのデータアナリストです。
    渡されたテキストデータを分析し、AR会議システムで表示するためのJSONデータを生成してください。

    【入力データ】
    {text_input}

    【制約事項】
    1. 出力は必ず正しいJSON形式であること。Markdown記法(```json ... ```)は不要。
    2. "recommended_graph_type" は、データの内容に応じて "bar" (棒グラフ) か "scatter" (散布図) のどちらか適切な方を選ぶこと。
    3. "data_points" の値は、入力データから抽出するか、文脈から妥当な数値を推定すること。
    4. 日本語で出力すること。

    【出力期待フォーマット (Pydantic Schema準拠)】
    {{
        "title": "分析タイトル",
        "summary": "短い要約",
        "advice": "具体的な改善アドバイス",
        "key_points": ["要点1", "要点2", "要点3"],
        "recommended_graph_type": "bar または scatter",
        "data_points": [
            {{ "label": "項目名", "value": 10.5 }}
        ]
    }}
    """

    try:
        # AIにリクエスト送信 (JSONモードを強制)
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 返ってきた文字列をPythonの辞書に変換
        result_json = json.loads(response.text)
        
        # Pydanticモデルに変換してバリデーション（形が合っているかチェック）
        return AnalysisResponse(**result_json)

    except Exception as e:
        print(f"AI Analysis Error: {e}")
        # エラー時はダミーデータを返してアプリが落ちないようにする（安全策）
        return AnalysisResponse(
            title="分析エラー",
            summary="AIによる解析に失敗しました。",
            advice="入力を確認して再試行してください。",
            key_points=[str(e)],
            recommended_graph_type="bar",
            data_points=[]
        )