using System.Collections;
using System.Text; // 文字コード変換に必要
using UnityEngine;
using UnityEngine.Networking;
using MyARPlatform.Data;
using MyARPlatform.Visualization;
using MyARPlatform.UI;

namespace MyARPlatform.API
{
    public class AnalysisDataLoader : MonoBehaviour
    {
        [Header("通信設定")]
        [SerializeField] private string _baseUrl = "http://localhost:8000"; 

        [Header("連携設定")]
        [SerializeField] private GraphVisualizer _visualizer; 
        [SerializeField] private DashboardController _dashboard; 

        // テスト用にInspectorから文章を変えられるようにする
        [Header("デバッグ入力")]
        [TextArea(3, 10)] 
        public string TestInputText = "今月の店舗ごとの売上は、渋谷店が120万円、新宿店が95万円、池袋店が110万円、横浜店が80万円でした。横浜店だけ目標未達です。";

        void Start()
        {
            // 起動時に、Inspectorに入力されたテキストでAI分析を実行！
            StartCoroutine(PostAnalysisRequest(TestInputText));
        }

        // 外部（音声入力やキーボード）から呼べるように public にしておく
        public void AnalyzeText(string text)
        {
            StartCoroutine(PostAnalysisRequest(text));
        }

        private IEnumerator PostAnalysisRequest(string textInput)
        {
            string url = $"{_baseUrl}/api/analysis/generate";
            Debug.Log($"【AI分析開始】送信テキスト: {textInput}");

            // 1. 送信データの作成 (JSON化)
            AnalysisRequest reqData = new AnalysisRequest();
            reqData.raw_text = textInput;
            string jsonBody = JsonUtility.ToJson(reqData);

            // 2. POSTリクエストの作成 (UnityWebRequestの特殊な書き方)
            using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonBody);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                
                // ヘッダー設定 (これを忘れるとBackendでエラーになる)
                request.SetRequestHeader("Content-Type", "application/json");

                // 3. 送信！
                yield return request.SendWebRequest();

                if (request.result != UnityWebRequest.Result.Success)
                {
                    Debug.LogError($"【通信エラー】: {request.error}\nResponse: {request.downloadHandler.text}");
                }
                else
                {
                    // 4. 受信データの処理
                    string responseJson = request.downloadHandler.text;
                    Debug.Log($"【AI応答あり】: {responseJson}");

                    try 
                    {
                        AnalysisResponse data = JsonUtility.FromJson<AnalysisResponse>(responseJson);

                        // UI更新
                        if (_dashboard != null) _dashboard.UpdateDashboard(data);
                        
                        // グラフ描画
                        if (_visualizer != null) _visualizer.RenderGraph(data);
                    }
                    catch (System.Exception e)
                    {
                        Debug.LogError($"データ処理エラー: {e.Message}");
                    }
                }
            }
        }
    }
}