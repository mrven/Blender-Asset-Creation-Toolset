# Blender Addon: Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[Russian README](/README_ru.md)**

**Asset Creation Toolset** is Many Tools for Game Asset Creation (Batch Export FBXs/GLTF for Unity/UE/Godot, Origin Aligment Tool, Renaming, UV Tools, Low-Poly Art workflow tools, etc.) for Blender.

***Download latest version:***

* ***[(2024.2) Blender 4.1 and higher](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2024_2_Bl410.zip)***
* ***[(2023.2) Blender 4.0 and higher](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2023_2_Bl400.zip)***
* ***[(2023.1) Blender 3.6 and higher](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2023_1_Bl361.zip)***
* ***[ACT Unity Editor Script (for ACT 2023.1 and higher)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Unity_Plugin/Releases/ACT_2023_1_Unity_Plugin.unitypackage)***
* -----------------------------------------------------
* ***[(3.3) Blender 3.4 and higher](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_3_341.zip)***
* ***[(3.1.5) Blender 2.90 - 3.0](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_5_290.zip)***
* ***[(3.1.2) Blender 2.83](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_2_283.zip)***
* ***[(2.4.1) Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***

If you want to support me you can buy this addon:
* ***[Gumroad (Pay what you want)](https://gumroad.com/l/hPXIh)***


***[Watch Features Overview (Youtube Playlist)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRr_UOQp3TapOVyEqbzZ0MkL)***

## New in Asset Creation Toolset 2024
### New GLTF Export for GODOT
![GLTF_Export](/images/pngs/2024/01_GLTF_Export.png)

### "Add UV" has option for generating Smart UV or Lightmap UV
![Add_UV_Packing](/images/pngs/2024/02_Add_UV_Packing.png)

### Export FBX now supports Custom Properties


## Features
### Origin Align Tool
Aligment Origin Point to:
* Max/Min/Middle point of object for X, Y or Z axis
* 3D Cursor (Separate Axis)
* Coordinates (Separate Axis)

![Origin Align](/images/gifs/01_Origin_Align.gif)


### Set Origin to Selected (Edit Mode)
Set Origin Point to Selected Element(s)

![Origin To Selected](/images/gifs/13_OriginToSelected.gif)


### Numbering Objects
Delete Blender's default numbering and add new numbering by Axis/Outliner order with pattern:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

![Numbering Objects](/images/gifs/03_Numbering.gif)


### Add .L or .R suffix to Bones
Quick add suffix .L or .R to Selected Bones.

![Suffix Bones](/images/gifs/16_BonesSuffix.gif)


### UV Tools
* Batch Renaming UV by Index (example, Lightmap - second uv channel)
* Batch Add UV with custom name (copy UV from active, smart projection or lightmap uv)
* Batch Remove UV by Index
* Set Active UV Layer for Selected Objects in 3D View and Image/UV Editor by UV Index

![Rename UV](/images/gifs/02_RenameUV.gif)
![UV Tools](/images/pngs/02_UV_Tools.png)


### UV Mover (UV Image Editor)
Tool for easier Atlas Packing.
* Scale UV with power of 2
* Move UV with steps

![UV Mover](/images/gifs/15_UVMover.gif)


### Export OBJ/FBX/GLTF to Unity/UE/Godot
Batch Export Selected Objects for Unity, UE or Godot. Available some modes:
* Export All Selected Object into One file
* Export Each Object into Individual file
* Batch Objects by Parent
* Batch Objects by Collection

![Export FBXs](/images/gifs/04_ExportFBX.gif)

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


### Material -> Viewport Color / Random Material Viewport Colors
Transfer Material Base Color to Viewport Color for Solid View Mode. Or Generate Random Colors for Materials for Viewport.

![Material To Viewport](/images/gifs/07_MaterialToViewport.gif)


### Clear UV Maps/Clear Vertex Color
Just remove all UV Maps or all Vertex Colors from selected objects.

![Clear UV Maps](/images/gifs/08_ClearUVandVC.gif)


### Delete Unused Materials
Delete from selected objects unused materials (not applyed to faces) and unused material slots.

![Delete Unused Materials](/images/gifs/12_DeleteUnusedMats.gif)


### Create Palette Textures (Albedo, Roughness, Metallic, Opacity and Emission)
Create Palette Textures (32x32px) for Selected Objects painted with colored materials. In one palette texture can be up to 256 colors (materials).

![Create Palette Texture](/images/gifs/06_PaletteTexture.gif)


### Quick Select Texture from Active material in UV Editor

![Quick Select Texture](/images/pngs/03_Quick_Select_Texture.png)


### Active Material -> Selected
Assign active material to selected faces in MultiEdit Mode.

![Active Material To Selected](/images/gifs/14_ActiveMatToSelected.gif)


### Obj Name -> Data Name
Copy Object Name to Mesh/Font/Etc.(Data-Block) Name.

![Copy Name](/images/gifs/09_ObjToMeshName.gif)


### Collection Name -> Obj Name
Transfer Collection Name to Object Name. You can use dirrernt ways for that:
1. Added Collection name before or after current object name. For example, ***"CollectionName_ObjectName"*** or ***"ObjectName_CollectionName"***
2. Replace Object Name to "Collection Name + Type + Numbering", For example, ***"CollectionName_Mesh_001"*** or ***"CollectionName_MESH_001"***. Thanks @Oxicid for implementation!\
![Col_To_Name](/images/pngs/2023/09_Col_To_Name.png)


### Clear Custom Normals
Clear Custom Normals and set Autosmooth to 180 degrees for Selected Objects.

![Clear Custom Normals](/images/gifs/10_ClearCustomNormals.gif)


### Flip/Calculate Normals
Flip or Recalculate Normals for Selected Objects in Object Mode.

![Flip Calculate Normals](/images/gifs/11_CalcNormals.gif)


### Merge Bones Tool
Tool For Easy Simplifying Armature: Delete (or Dissolve) Selected Bones (Exclude Active) and Transfer Vertex Weights to Active Bone.

![Merge Bones](/images/gifs/17_MergeBones.gif)


### Addon Preferences
* Show/Hide UI Panels via Addon Preferences
* Changing Category for each Panel from Preferences

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)
