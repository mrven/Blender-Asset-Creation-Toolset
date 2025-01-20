# Blender Addon: ACT: Game Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[Russian README](/README_ru.md)**

**ACT** is Many Tools for Game Asset Creation (Batch Export FBXs/GLTF for Unity/UE/Godot, Origin Aligment Tool, Renaming, UV Tools, Low-Poly Art workflow tools, etc.) for Blender.

# Download
* ***[(2025.1) Blender 4.2+ (from Blender Extensions)](https://extensions.blender.org/add-ons/act-game-asset-creation-toolset/)***
* ***[(2025.1) Blender 4.2+ (from GitHub)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/ACT_2025_1_Bl420.zip)***
* ***[ACT Unity Editor Script (for Unity 2022+)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Unity_Plugin/Releases/ACT_Unity_Plugin.unitypackage)***
-----------------------------------------------
* ***[Previous Releases](/Previous_Releases.md)***

# Documentation
[![ACT Playlist](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRpLoJD79MC6AQf_phyXP62b)

# Sponsorship
If you want to support me you can buy this addon on **[Blender Market](https://blendermarket.com/products/asset-creation-toolset-2024)**

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mrven)

# Features
## What's new in ACT 2025?
[NEW] Add/Remove LOD to Name \
[NEW] Assign Seams from UV \
[NEW] Export Tool: Custom Scale and Axes for FBX/OBJ \
[NEW] Cleanup Duplicated Materials \
[NEW] Select Objects with Negative Scale \
[NEW] Cleanup Empties \
[NEW] Dissolve Checker Loops \
[NEW] Collapse Checker Edges \
[FIX] Fix addon installation error if Cycles is disabled \
[FIX] Clear Custom Normals apply on meshes with custom normal data only \
[IMPROVEMENT] Rename UV: Set Default name for UV when "Name" Field is empty \

## Origin Tools
![Origin Tools](/images/pngs/2025/01_Origin_Tools.png)\
[![Origin Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=cxcSM-HvMH8)

### Origin Align Tool
Aligment Origin Point to:
* Max/Min/Middle point of object for X, Y or Z axis
* 3D Cursor (Separate Axis)
* Coordinates (Separate Axis)

### Set Origin to Selected (Edit Mode)
Set Origin Point to Selected Element(s)


## Renaming Tools
![Renaming Tools](/images/pngs/2025/02_Renaming_Tools.png)\
[![Renaming Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=pqz-mSK8n90)

### Numbering Objects
Delete Blender's default numbering and add new numbering by Axis/Outliner order with pattern:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

### Add/Remove LOD to Name
Add/replace/remove postfix \_LOD\* with a selected LOD level.

### Add .L or .R suffix to Bones
Quick add suffix .L or .R to Selected Bones.


## UV Tools
![UV Tools](/images/pngs/2025/03_UV_Tools.png)\
[![UV Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=ble4bwOJwjQ)

* Batch Renaming UV by Index (example, Lightmap - second uv channel)
* Batch Add UV with custom name (copy UV from active, smart projection or lightmap uv)
* Batch Remove UV by Index
* Set Active UV Layer for Selected Objects in 3D View and Image/UV Editor by UV Index

### Assign Seams from UV
Batch assignment of UV seams to models directly from Object Mode.

### UV Mover (UV Image Editor)
Tool for easier Atlas Packing.
* Scale UV with power of 2
* Move UV with steps


## Export Tools
![Export Tools](/images/pngs/2025/04_Export.png)\
[![Export Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=XTyvRZLvVUg)

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
![Export Tools](/images/pngs/2025/05_Material_Tools.png)\
[![Material Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=WY9vJja1nqw)

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

### Cleanup Duplicated Materials
Remove duplicate materials (by name). Useful when importing many models with the same materials but from different files. In this case, Blender creates many copies of the materials. This function allows you to find and assign the original materials to all models.


## Other Tools
![Export Tools](/images/pngs/2025/06_Other_Tools.png)\
[![Other Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=n8ZBI3KZ47Y)

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

### Select Objects with Negative Scale
In game development, objects with negative scale should be avoided (especially colliders or other physical objects). This tool allows you to find such objects.

### Cleanup Empties
Removing empty spaces under which there are no objects and meshes without geometry.


## Geometry Tools
![Geometry Tools](/images/pngs/2025/07_Geometry_Tools.png)\

### Dissolve Checker Loops
Remove stitches one by one (starting from the selected edge). Perfect for simplifying cylindrical geometry.

### Collapse Checker Edges
Collapses edges one by one (along the loop). Perfect for simplifying spherical geometry.


## Addon Preferences
* Show/Hide UI Panels via Addon Preferences
* Changing Category for each Panel from Preferences

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)

[<img src="https://api.gitsponsors.com/api/badge/img?id=190054403" height="20">](https://api.gitsponsors.com/api/badge/link?p=R7W5zpiWrH5vKtok3kzishcHSm+vXLZUisxg1E+mz6+XIavgMaeedIgSiO/Pg8qJqY/tYxmwupuzjsP75azNlSy4YbYlJdL3ENeRkPjkRrmotBAe8wjwLaG/9IT0ejm234ouL7ohak0h8SewxjZpPA==)