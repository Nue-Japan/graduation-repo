using UnityEngine;
using UnityEngine.UIElements; // UI Toolkitを使うおまじない
using MyARPlatform.Data;

namespace MyARPlatform.UI
{
    public class DashboardController : MonoBehaviour
    {
        private UIDocument _uiDocument;
        private Label _titleLabel;
        private Label _summaryLabel;
        private Label _adviceLabel;

        void OnEnable()
        {
            // UI Documentコンポーネントを取得
            _uiDocument = GetComponent<UIDocument>();
            
            // UIパーツの参照を取得 (UXMLでつけた "name" で探す)
            var root = _uiDocument.rootVisualElement;
            _titleLabel = root.Q<Label>("TitleLabel");
            _summaryLabel = root.Q<Label>("SummaryLabel");
            _adviceLabel = root.Q<Label>("AdviceLabel");
        }

        // 外部からデータを渡されて表示を更新する関数
        public void UpdateDashboard(AnalysisResponse data)
        {
            if (data == null) return;

            // スレッドセーフにするためメインスレッドで実行
            // (UnityWebRequestのコールバック等は別スレッド扱いになることがあるため念の為)
            if (_titleLabel != null) _titleLabel.text = data.title;
            if (_summaryLabel != null) _summaryLabel.text = data.summary;
            if (_adviceLabel != null) _adviceLabel.text = data.advice;

            Debug.Log("<color=cyan>UIパネル更新完了</color>");
        }
    }
}