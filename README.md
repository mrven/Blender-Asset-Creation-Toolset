# Blender Addon: ACT: Game Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[Russian README](/README_ru.md)**

**ACT** is Many Tools for Game Asset Creation (Batch Export FBXs/GLTF for Unity/UE/Godot, Origin Aligment Tool, Renaming, UV Tools, Low-Poly Art workflow tools, etc.) for Blender.

# Download
* ***[(2025.1) Blender 4.2+ (from Blender Extensions)](https://extensions.blender.org/add-ons/act-game-asset-creation-toolset/)***
* ***[(2025.1) Blender 4.2+ (from GitHub)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/ACT_2025_1_Bl420.zip)***
* ***[ACT Unity Editor Script (for Unity 2022+)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Unity_Plugin/Releases/ACT_Unity_Plugin.unitypackage)***

# Documentation
***[Watch Features Overview (Youtube Playlist)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRpLoJD79MC6AQf_phyXP62b)***

# Sponsorship
If you want to support me you can buy this addon on **[Blender Market](https://blendermarket.com/products/asset-creation-toolset-2024)**
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mrven)

# Features
## Origin Tools

[![Origin Tools Overview](https://img.youtube.com/vi/cxcSM-HvMH8/0.jpg)](https://www.youtube.com/watch?v=cxcSM-HvMH8)

### Origin Align Tool
Aligment Origin Point to:
* Max/Min/Middle point of object for X, Y or Z axis
* 3D Cursor (Separate Axis)
* Coordinates (Separate Axis)

### Set Origin to Selected (Edit Mode)
Set Origin Point to Selected Element(s)


## Renaming Tools

[![Renaming Tools Overview](https://img.youtube.com/vi/pqz-mSK8n90/0.jpg)](https://www.youtube.com/watch?v=pqz-mSK8n90)

### Numbering Objects
Delete Blender's default numbering and add new numbering by Axis/Outliner order with pattern:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

### Add .L or .R suffix to Bones
Quick add suffix .L or .R to Selected Bones.


## UV Tools

[![UV Tools Overview](https://img.youtube.com/vi/ble4bwOJwjQ/0.jpg)](https://www.youtube.com/watch?v=ble4bwOJwjQ)

* Batch Renaming UV by Index (example, Lightmap - second uv channel)
* Batch Add UV with custom name (copy UV from active, smart projection or lightmap uv)
* Batch Remove UV by Index
* Set Active UV Layer for Selected Objects in 3D View and Image/UV Editor by UV Index

### UV Mover (UV Image Editor)
Tool for easier Atlas Packing.
* Scale UV with power of 2
* Move UV with steps


## Export Tools

[![Export Tools Overview](https://img.youtube.com/vi/XTyvRZLvVUg/0.jpg)](https://www.youtube.com/watch?v=XTyvRZLvVUg)

### Export OBJ/FBX/GLTF to Unity/UE/Godot
Batch Export Selected Objects for Unity, UE or Godot. Available some modes:
* Export All Selected Object into One file
* Export Each Object into Individual file
* Batch Objects by Parent
* Batch Objects by Collection

#### Export Algorithm for Unity
Now ACT has two different algorithms for export FBXs to Unity: ***"Unity"*** and ***"Unity (Legacy)"***.\
![Target_Engine](/images/pngs/2023/01_Target.png)

#### "Unity" Export Profile
This profile supports Objects with Linked Data, more acurate for rigs, animations, angles and axis. ***But this export profile requires additional steps with models in Unity.*** You have to set in model import settings "Scale Factor" to 100 and check in option "Bake Axis Conversion".\
![Import_Settings](/images/pngs/2023/02_Import_Settings.png)

For automatization this steps I created ***Unity Editor Script*** and you can use this different ways:
1. Select Models -> RMB -> ACT/Fix Models Transform.
![Fix_Transforms](/images/pngs/2023/03_Fix_Transforms.png)
2. Open ACT Settings Window (Window -> ACT -> Settings) and enable Models Postprocessor. It automatically set import settings for each model (or for models whose names contain the specified string or character).
![ACT_Settings_1](/images/pngs/2023/04_ACT_Settings_1.png)\
![ACT_Settings_2](/images/pngs/2023/05_ACT_Settings_2.png)\
![ACT_Settings_3](/images/pngs/2023/06_ACT_Settings_3.png)\
The Unity editor ACT script is distributed with the ACT Blender add-on.

#### "Unity (Legacy)" Export Profile
But you can also use previous algorithm: This algorithm doesn't require additional actions in Unity and this Export Profile provide back-compatibility with already existing models.\
![Old_Algorithm](/images/pngs/2023/07_Old_Algorithm.png)


## Material/Texture Tools

[![Material Tools Overview](https://img.youtube.com/vi/WY9vJja1nqw/0.jpg)](https://www.youtube.com/watch?v=WY9vJja1nqw)

### Material -> Viewport Color / Random Material Viewport Colors
Transfer Material Base Color to Viewport Color for Solid View Mode. Or Generate Random Colors for Materials for Viewport.

### Clear UV Maps/Clear Vertex Color
Just remove all UV Maps or all Vertex Colors from selected objects.

### Delete Unused Materials
Delete from selected objects unused materials (not applyed to faces) and unused material slots.

### Create Palette Textures (Albedo, Roughness, Metallic, Opacity and Emission)
Create Palette Textures (32x32px) for Selected Objects painted with colored materials. In one palette texture can be up to 256 colors (materials).

### Quick Select Texture from Active material in UV Editor

### Active Material -> Selected
Assign active material to selected faces in MultiEdit Mode.


## Other Tools

[![Other Tools Overview](https://img.youtube.com/vi/n8ZBI3KZ47Y/0.jpg)](https://www.youtube.com/watch?v=n8ZBI3KZ47Y)

### Obj Name -> Data Name
Copy Object Name to Mesh/Font/Etc.(Data-Block) Name.

### Collection Name -> Obj Name
Transfer Collection Name to Object Name. You can use dirrernt ways for that:
1. Added Collection name before or after current object name. For example, ***"CollectionName_ObjectName"*** or ***"ObjectName_CollectionName"***
2. Replace Object Name to "Collection Name + Type + Numbering", For example, ***"CollectionName_Mesh_001"*** or ***"CollectionName_MESH_001"***. Thanks @Oxicid for implementation!\
![Col_To_Name](/images/pngs/2023/09_Col_To_Name.png)

### Clear Custom Normals
Clear Custom Normals and set Autosmooth to 180 degrees for Selected Objects.

### Flip/Calculate Normals
Flip or Recalculate Normals for Selected Objects in Object Mode.

### Merge Bones Tool
Tool For Easy Simplifying Armature: Delete (or Dissolve) Selected Bones (Exclude Active) and Transfer Vertex Weights to Active Bone.

## Addon Preferences
* Show/Hide UI Panels via Addon Preferences
* Changing Category for each Panel from Preferences

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)

[<img src="https://api.gitsponsors.com/api/badge/img?id=190054403" height="20">](https://api.gitsponsors.com/api/badge/link?p=R7W5zpiWrH5vKtok3kziskOzBnSDKorI5wOcmiIPBzz9i28hZmWFBXmcyJL/atWR9JoicfSKTaNSfh+Mfp0bcA==)