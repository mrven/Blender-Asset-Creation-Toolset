[<< Return to README](../README.md#documentation)

# Export Tools

## Export OBJ/FBX/GLTF to Unity/UE/Godot
Batch Export Selected Objects for Unity, UE or Godot. Available some modes:
* Export All Selected Object into One file
* Export Each Object into Individual file
* Batch Objects by Parent
* Batch Objects by Collection

### Export Algorithm for Unity
Now ACT has two different algorithms for export FBXs to Unity: ***"Unity"*** and ***"Unity (Legacy)"***.\
![Target_Engine](./docs/images/pngs/2023/01_Target.png)

### "Unity" Export Profile
This profile supports Objects with Linked Data, more acurate for rigs, animations, angles and axis. ***But this export profile requires additional steps with models in Unity.*** You have to set in model import settings "Scale Factor" to 100 and check in option "Bake Axis Conversion".\
![Import_Settings](./docs/images/pngs/2023/02_Import_Settings.png)

For automatization this steps I created ***Unity Editor Script*** and you can use this different ways:
1. Select Models -> RMB -> ACT/Fix Models Transform.
![Fix_Transforms](./docs/images/pngs/2023/03_Fix_Transforms.png)
2. Open ACT Settings Window (Window -> ACT -> Settings) and enable Models Postprocessor. It automatically set import settings for each model (or for models whose names contain the specified string or character).
![ACT_Settings_1](./docs/images/pngs/2023/04_ACT_Settings_1.png)\
![ACT_Settings_2](./docs/images/pngs/2023/05_ACT_Settings_2.png)\
![ACT_Settings_3](./docs/images/pngs/2023/06_ACT_Settings_3.png)\
The Unity editor ACT script is distributed with the ACT Blender add-on.

### "Unity (Legacy)" Export Profile
But you can also use previous algorithm: This algorithm doesn't require additional actions in Unity and this Export Profile provide back-compatibility with already existing models.\
![Old_Algorithm](./docs/images/pngs/2023/07_Old_Algorithm.png)