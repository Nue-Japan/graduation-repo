import google.generativeai as genai
import os
import json
from app.schemas.analysis import AnalysisResponse

# Initialize Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API client
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY) 
    
# Function to generate insights using Gemini model
async def generate_insight(context: str, data_text: str, model_name: str = "gemini-2.5-flash") -> AnalysisResponse:
    if not GEMINI_API_KEY:
        return AnalysisResponse(advice="APIキーが見つかりません。サーバー設定を確認してください。", key_points=[])
    
    # Construct prompt and call Gemini model    
    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        以下の「会議コンテキスト」と「データ」を分析し、参加者へのアドバイスを生成してください。

        【会議コンテキスト】: {context}
        【データ内容】: {data_text}

        出力はMarkdownなどの装飾を含まず、以下の純粋なJSONフォーマットのみで出力してください。
        {{
            "advice": "全体的な分析コメント（150文字以内の日本語）",
            "key_points": ["重要なポイント1", "重要なポイント2", "重要なポイント3"]
        }}
        """
        
        # API call to Gemini model
        responce = model.generate_content(prompt=prompt)
        
        # Text extraction and JSON parsing
        raw_text = responce.text.replace("```json", "").replace("```", "").strip()
        
        # JSON parsing
        result_json = json.loads(raw_text)
        
        return AnalysisResponse(
            advice=result_json.get("advice","解析結果の取得に失敗しました"),
            key_points=result_json.get("key_points",[])
        )
        
    # Handle exceptions
    except Exception as e:
        print(f"Error during AI generation: {e}")
        return AnalysisResponse(
            advice="解析中にエラーが発生しました。後でもう一度お試しください。",
            key_points=["ERROR:" + str(e)]
        )