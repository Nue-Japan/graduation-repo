using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using MyARPlatform.Data;          // データ型 (AnalysisResponse)
using MyARPlatform.Visualization; // 3Dグラフ描画用
using MyARPlatform.UI;            // UIパネル表示用

namespace MyARPlatform.API
{
    public class AnalysisDataLoader : MonoBehaviour
    {
        [Header("通信設定")]
        // 開発環境(Windows)なら localhost, エミュレータなら 10.0.2.2
        [SerializeField] private string _baseUrl = "http://localhost:8000"; 

        [Header("連携設定")]
        [SerializeField, Tooltip("グラフを描画するコンポーネント")]
        private GraphVisualizer _visualizer; 

        [SerializeField, Tooltip("★追加: 情報を表示するUIパネル")]
        private DashboardController _dashboard; 

        void Start()
        {
            // 起動時にデータを取得開始
            StartCoroutine(FetchAnalysisData());
        }

        private IEnumerator FetchAnalysisData()
        {
            string url = $"{_baseUrl}/api/analysis/mock";
            Debug.Log($"【通信開始】Requesting to: {url}");

            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                // 通信待機
                yield return request.SendWebRequest();

                // エラーチェック
                if (request.result == UnityWebRequest.Result.ConnectionError || 
                    request.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.LogError($"【通信エラー】: {request.error}");
                }
                else
                {
                    // 通信成功
                    string json = request.downloadHandler.text;
                    
                    try 
                    {
                        // JSONをC#クラスに変換
                        AnalysisResponse data = JsonUtility.FromJson<AnalysisResponse>(json);

                        // --- ログ出力 (確認用) ---
                        Debug.Log("============== データ受信成功 ==============");
                        Debug.Log($"タイトル: {data.title}");
                        Debug.Log($"推奨グラフ: {data.recommended_graph_type}");
                        Debug.Log($"AIアドバイス: {data.advice}");
                        Debug.Log("==========================================");

                        // --- 1. 3Dグラフの描画 ---
                        if (_visualizer != null)
                        {
                            _visualizer.RenderGraph(data);
                        }
                        else
                        {
                            Debug.LogWarning("Visualizer (グラフ描画) がセットされていません。");
                        }

                        if (_dashboard != null)
                        {
                            _dashboard.UpdateDashboard(data);
                        }
                        else
                        {
                            Debug.LogWarning("Dashboard (UIパネル) がセットされていません。");
                        }
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