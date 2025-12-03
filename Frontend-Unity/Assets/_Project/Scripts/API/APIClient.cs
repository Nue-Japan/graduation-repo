using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using MyARPlatform.Data; // さっき作ったクラスを使う

namespace MyARPlatform.API
{
    public class APIClient : MonoBehaviour
    {
        // 接続先URL (Windowsで動いているサーバー)
        private const string BASE_URL = "http://localhost:8000/api";

        // ゲーム開始時に自動で通信テストを行う
        void Start()
        {
            StartCoroutine(CheckServerHealth());
        }

        private IEnumerator CheckServerHealth()
        {
            string url = BASE_URL + "/system/health";
            Debug.Log($"[API] 接続試行中... : {url}");

            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                // 通信開始！完了するまで待機
                yield return request.SendWebRequest();

                // エラーチェック
                if (request.result == UnityWebRequest.Result.ConnectionError || 
                    request.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.LogError($"[API Error] 通信失敗: {request.error}");
                }
                else
                {
                    // 成功！サーバーからの返事を表示
                    string json = request.downloadHandler.text;
                    Debug.Log($"[API Success] 生データ: {json}");

                    // JSONをC#のクラスに変換
                    try 
                    {
                        HealthResponse res = JsonUtility.FromJson<HealthResponse>(json);
                        if (res.status == "success")
                        {
                            // 緑色の文字で成功を表示！
                            Debug.Log($"<color=green>★ サーバー接続成功！ ★</color> DB状態: {res.data.database}");
                        }
                    }
                    catch (System.Exception e)
                    {
                        Debug.LogError($"[JSON Parse Error] 変換失敗: {e.Message}");
                    }
                }
            }
        }
    }
}