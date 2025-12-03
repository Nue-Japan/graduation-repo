using System;

namespace MyARPlatform.Data
{
    // Backendの共通レスポンス型に合わせます
    [Serializable]
    public class APIResponse
    {
        public string status;   // "success" or "error"
        public string message;  // "System is healthy" など
    }

    // ヘルスチェックの "data" の中身
    [Serializable]
    public class HealthData
    {
        public string database;
        public string api;
    }

    // APIResponseの中にHealthDataが入っている形
    [Serializable]
    public class HealthResponse : APIResponse
    {
        public HealthData data;
    }
}