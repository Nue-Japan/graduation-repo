using System;
using System.Collections.Generic;

namespace MyARPlatform.Data
{
    [Serializable]
    public class DataPoint
    {
        public string label;
        public float value;
    }

    [Serializable]
    public class AnalysisResponse
    {
        public string recommended_graph_type;
        public string title;
        public string summary;
        
        public string advice;
        public List<string> key_points; 
        
        public List<DataPoint> data_points;
    }
}