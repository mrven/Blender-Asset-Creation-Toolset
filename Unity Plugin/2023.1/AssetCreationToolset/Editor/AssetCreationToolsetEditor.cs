using UnityEngine;
using UnityEditor;

// Asset Creation Toolset 2023.1
public class AssetCreationToolsetEditor : Editor
{
    public static class Prefs
    {
        public static readonly string PostProcessorEnabled = "PostprocessEnabled";
        public static readonly string ApplyIfContains = "ApplyIfContains";
        public static readonly string TriggerString = "TriggerString";
    }
    
    [MenuItem("Window/ACT/Settings")]
    private static void OpenACTSettings()
    {
        var actSettingsWindow = EditorWindow.GetWindow(typeof(AssetCreationToolsetWindow));
        actSettingsWindow.position = new Rect(Screen.width, Screen.height * 0.5f, 600, 600);
        actSettingsWindow.minSize = new Vector2(300, 200);
        actSettingsWindow.maxSize = new Vector2(300, 200);
        actSettingsWindow.Show();
        GUIContent actSettingsWindowTitle = new GUIContent("ACT Settings");
        actSettingsWindow.titleContent = actSettingsWindowTitle;
    }

    [MenuItem("Assets/ACT/Fix Models Transforms")]
    private static void FixModelsTransforms()
    {
        var selected = Selection.objects;

        foreach (Object obj in selected)
        {
            string assetPath = AssetDatabase.GetAssetPath(obj);
            
            if (assetPath.ToLower().EndsWith(".fbx"))
            {
                var assetImporter = AssetImporter.GetAtPath(assetPath);
                ModelImporter modelImporter = assetImporter as ModelImporter;
                
                modelImporter.globalScale = 100f;
                modelImporter.bakeAxisConversion = true;
                modelImporter.SaveAndReimport();
            }
        }
    }
}

public class ACTModelsPostprocessor : AssetPostprocessor
{
    void OnPostprocessModel(GameObject g)
    {
        Apply(g);
    }

    void Apply(GameObject g)
    {
        bool postprocessEnabled = EditorPrefs.GetBool(AssetCreationToolsetEditor.Prefs.PostProcessorEnabled);
        int applyIfContains = EditorPrefs.GetInt(AssetCreationToolsetEditor.Prefs.ApplyIfContains);
        string triggerString = EditorPrefs.GetString(AssetCreationToolsetEditor.Prefs.TriggerString);
        
        if (postprocessEnabled && assetPath.ToLower().Contains(".fbx"))
        {
            if (applyIfContains == 0 || (applyIfContains > 0 && g.name.Contains(triggerString)))
            {
                    ModelImporter modelImporter = (ModelImporter)assetImporter;
                    modelImporter.globalScale = 100f;
                    modelImporter.bakeAxisConversion = true;
                    modelImporter.SaveAndReimport();
            }
        }
    }
}
