using System.Collections.Generic;
using UnityEngine;
using TMPro; // ★重要: 文字を扱うためのライブラリ
using MyARPlatform.Data;

namespace MyARPlatform.Visualization
{
    public class GraphVisualizer : MonoBehaviour
    {
        [Header("設定")]
        [SerializeField] private Transform _graphContainer;
        [SerializeField] private float _spacing = 0.3f;
        [SerializeField] private float _heightMultiplier = 0.05f;

        [Header("グラフ素材")]
        [SerializeField] private GameObject _barPrefab;     // 棒 (Cube)
        [SerializeField] private GameObject _pointPrefab;   // 点 (Sphere)
        [SerializeField] private GameObject _labelPrefab;   // ★追加: 文字 (GraphLabel)

        [Header("カラー設定")]
        [SerializeField] private Color _minColor = Color.blue; // 低い値の色
        [SerializeField] private Color _maxColor = Color.red;  // 高い値の色

        private List<GameObject> _spawnedObjects = new List<GameObject>();

        public void RenderGraph(AnalysisResponse data)
        {
            ClearGraph();

            if (data == null || data.data_points == null) return;
            Transform parent = _graphContainer != null ? _graphContainer : this.transform;

            string graphType = data.recommended_graph_type?.ToLower() ?? "bar";
            
            // 色を決めるために、データの中の最大値を探す
            float maxValue = 0f;
            foreach(var p in data.data_points) if(p.value > maxValue) maxValue = p.value;

            for (int i = 0; i < data.data_points.Count; i++)
            {
                var point = data.data_points[i];
                float xPos = i * _spacing;

                // --- 1. グラフ本体（棒 or 点）の生成 ---
                GameObject graphObj = null;

                if (graphType == "scatter")
                {
                    // 散布図 (Sphere)
                    graphObj = Instantiate(_pointPrefab, parent);
                    float yPos = point.value * _heightMultiplier;
                    graphObj.transform.localPosition = new Vector3(xPos, yPos, 0);
                    graphObj.transform.localScale = Vector3.one * 0.15f; // 点は小さく
                }
                else
                {
                    // 棒グラフ (Cube)
                    graphObj = Instantiate(_barPrefab, parent);
                    graphObj.transform.localPosition = new Vector3(xPos, 0, 0);
                    float h = point.value * _heightMultiplier;
                    
                    // 棒の現在の太さを維持しつつ、高さ(Y)だけ変える
                    Vector3 currentScale = graphObj.transform.localScale;
                    graphObj.transform.localScale = new Vector3(currentScale.x, h, currentScale.z);
                }

                // --- 2. 色の適用 (グラデーション) ---
                if (graphObj != null)
                {
                    // 値の大きさ(0.0 ~ 1.0)を計算
                    float ratio = (maxValue > 0) ? (point.value / maxValue) : 0;
                    // 青→赤 に色を変化させる
                    Color targetColor = Color.Lerp(_minColor, _maxColor, ratio);
                    
                    var renderer = graphObj.GetComponent<Renderer>();
                    if (renderer != null) renderer.material.color = targetColor;

                    _spawnedObjects.Add(graphObj);
                }

                // --- 3. ラベル(文字)の生成 ---
                if (_labelPrefab != null)
                {
                    GameObject labelObj = Instantiate(_labelPrefab, parent);
                    // グラフの少し下(-0.2)に配置
                    labelObj.transform.localPosition = new Vector3(xPos, -0.2f, -0.2f); 
                    
                    // 文字の内容を書き換える
                    TMP_Text tmp = labelObj.GetComponent<TMP_Text>();
                    if (tmp != null)
                    {
                        tmp.text = point.label; // "10代" など
                        tmp.fontSize = 2f;      // 文字サイズ調整
                    }

                    _spawnedObjects.Add(labelObj);
                }
            }
        }

        private void ClearGraph()
        {
            foreach (var obj in _spawnedObjects)
            {
                if (obj != null) Destroy(obj);
            }
            _spawnedObjects.Clear();
        }
    }
}