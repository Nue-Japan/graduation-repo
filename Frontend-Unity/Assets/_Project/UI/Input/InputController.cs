using UnityEngine;
using UnityEngine.UIElements;
using MyARPlatform.API; // AnalysisDataLoaderを呼ぶため

namespace MyARPlatform.UI
{
    public class InputController : MonoBehaviour
    {
        [Header("連携設定")]
        [SerializeField] private AnalysisDataLoader _dataLoader;

        private UIDocument _uiDocument;
        private TextField _inputField;
        private Button _sendButton;

        void OnEnable()
        {
            _uiDocument = GetComponent<UIDocument>();
            var root = _uiDocument.rootVisualElement;

            // UIパーツ取得
            _inputField = root.Q<TextField>("AnalysisInput");
            _sendButton = root.Q<Button>("SendButton");

            // ボタンイベント登録
            if (_sendButton != null)
            {
                _sendButton.clicked += OnSendClicked;
            }
        }

        private void OnSendClicked()
        {
            if (_inputField == null || _dataLoader == null) return;

            string text = _inputField.value;

            if (string.IsNullOrEmpty(text))
            {
                Debug.LogWarning("テキストが空です");
                return;
            }

            
            // API通信開始！
            _dataLoader.AnalyzeText(text);
        }
    }
}