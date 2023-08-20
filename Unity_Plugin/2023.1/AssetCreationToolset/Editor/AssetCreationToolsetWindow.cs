using UnityEngine;
using UnityEditor;

// Asset Creation Toolset 2023.1
public class AssetCreationToolsetWindow : EditorWindow
{
    private bool _postProcessorEnabled;
    private int _applyIfContains;
    private string _triggerString;
    
    public string[] _selStrings = new string[] {"For All Models", "If Name Contains"};

    private void OnEnable()
    {
        _postProcessorEnabled = EditorPrefs.GetBool(AssetCreationToolsetEditor.Prefs.PostProcessorEnabled);
        _applyIfContains = EditorPrefs.GetInt(AssetCreationToolsetEditor.Prefs.ApplyIfContains);
        _triggerString = EditorPrefs.GetString(AssetCreationToolsetEditor.Prefs.TriggerString);

        if (_triggerString == "")
            _triggerString = "_ACT";
    }

    private void OnGUI()
    {
        float windowWidth = position.width - 20;

        EditorGUILayout.BeginHorizontal(GUILayout.Width(windowWidth));
        EditorGUILayout.LabelField("Asset Creation Toolset v.2023.1", EditorStyles.boldLabel, GUILayout.Width(windowWidth));
        EditorGUILayout.EndHorizontal();
        
        EditorGUILayout.Space();
        
        EditorGUILayout.BeginHorizontal(GUILayout.Width(windowWidth));
        _postProcessorEnabled = GUILayout.Toggle(_postProcessorEnabled, " Enable Models Postprocessor", GUILayout.Width(windowWidth));
        EditorGUILayout.EndHorizontal();

        EditorGUILayout.Space();
        EditorGUILayout.Space();
        
        if (_postProcessorEnabled)
        {
            EditorGUILayout.Space();
            EditorGUILayout.Space();
            _applyIfContains = GUI.SelectionGrid(new Rect(15, 50, 270, 35), _applyIfContains, _selStrings, 2);

            if (_applyIfContains > 0)
            {
                EditorGUILayout.Space();
                EditorGUILayout.Space();
                EditorGUILayout.Space();
                EditorGUILayout.BeginHorizontal(GUILayout.Width(windowWidth));
                EditorGUILayout.LabelField(" ", EditorStyles.boldLabel, GUILayout.Width(windowWidth * 0.05f));
                EditorGUILayout.LabelField("Apply if model's name contains:", EditorStyles.boldLabel, GUILayout.Width(windowWidth * 0.9f));
                EditorGUILayout.EndHorizontal();
                EditorGUILayout.BeginHorizontal(GUILayout.Width(windowWidth));
                EditorGUILayout.LabelField(" ", EditorStyles.boldLabel, GUILayout.Width(windowWidth * 0.05f));
                _triggerString = GUILayout.TextField(_triggerString, GUILayout.Width(windowWidth * 0.9f));
                EditorGUILayout.EndHorizontal();
            }
        }
        
    }

    private void OnInspectorUpdate()
    {
        UpdateEditorPrefs();
        Repaint();
    }

    private void UpdateEditorPrefs()
    {
        EditorPrefs.SetBool(AssetCreationToolsetEditor.Prefs.PostProcessorEnabled, _postProcessorEnabled);
        EditorPrefs.SetInt(AssetCreationToolsetEditor.Prefs.ApplyIfContains, _applyIfContains);
        EditorPrefs.SetString(AssetCreationToolsetEditor.Prefs.TriggerString, _triggerString);
    }
}
