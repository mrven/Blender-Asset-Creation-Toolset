# Blender Addon: Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[Russian README](/README_ru.md)**

**Asset Creation Toolset** is Many Tools for Game Asset Creation (Batch Import/Export FBXs, Origin Aligment Tool, Renaming, Low-Poly Art workflow tools, etc.) for Blender 2.79 and 2.8.

***Download latest version:***

* ***[Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***
* ***[Blender 2.80](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_5_0_280.zip)***
* ***[Blender 2.81](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_281.zip)***

If you want to support me you can buy this addon:
* ***[Gumroad (Pay what you want)](https://gumroad.com/l/hPXIh)***


***[Watch Features Overview (Youtube Playlist)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRr_UOQp3TapOVyEqbzZ0MkL)***



#### Origin Align Tool
Aligment Origin Point to:
* Max/Min point of object for X, Y or Z axis
* 3D Cursor (Separate Axis)
* Coordinates (Separate Axis)

![Origin Align](/images/gifs/01_Origin_Align.gif)


#### Set Origin to Selected (Edit Mode)
Set Origin Point to Selected Element(s)

![Origin To Selected](/images/gifs/13_OriginToSelected.gif)


#### UV Tools
* Batch Renaming UV by Index (example, Lightmap - second uv channel)
* Batch Add UV with custom name
* Batch Remove UV by Index
* Set Active UV Layer for Selected Objects in 3D View and Image/UV Editor by UV Index

![Rename UV](/images/gifs/02_RenameUV.gif)
![UV Tools](/images/pngs/02_UV_Tools.png)


#### Quick Select Texture from Active material in UV Editor

![Quick Select Texture](/images/pngs/03_Quick_Select_Texture.png)


#### Numbering Objects
Delete Blender's default numbering and add new numbering by Axis and with pattern:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

![Numbering Objects](/images/gifs/03_Numbering.gif)


#### Clear Custom Normals
Clear Custom Normals and set Autosmooth to 180 degrees for Selected Objects.

![Clear Custom Normals](/images/gifs/10_ClearCustomNormals.gif)


#### Flip/Calculate Normals
Flip or Recalculate Normals for Selected Objects in Object Mode.

![Flip Calculate Normals](/images/gifs/11_CalcNormals.gif)


#### Export FBX to Unity/UE4
Batch Export Selected Objects for Unity or UE4 (Fix Scale and Rotation). Available some modes:
* Export All Selected Object into One FBX
* Export Each Object into Individual FBX
* Batch Objects by Parent
* Batch Objects by Collection

![Export FBXs](/images/gifs/04_ExportFBX.gif)


#### Import FBXs/OBJs
Batch Import FBX and OBJ files with default parameters.

![Import FBXs OBJs](/images/gifs/05_ImportFBX.gif)


#### Create Palette Texture
Create Palette Texture (32x32px) for Selected Objects painted with colored materials. In one palette texture can be up to 256 colors (materials).
**Note: for Blender 2.79 uses Blender Render, for Blender 2.8 uses Cycles Render**

![Create Palette Texture](/images/gifs/06_PaletteTexture.gif)


#### Clear UV Maps/Clear Vertex Color
Just remove all UV Maps or all Vertex Colors from selected objects.

![Clear UV Maps](/images/gifs/08_ClearUVandVC.gif)


#### Obj Name -> Mesh Name
Copy Object Name to Mesh(Data-Block) Name.

![Copy Name](/images/gifs/09_ObjToMeshName.gif)


#### UV Mover (UV Image Editor)
Tool for easier Atlas Packing.

![UV Mover](/images/gifs/15_UVMover.gif)


#### Material -> Viewport Color
Transfer Material Base Color to Viewport Color for Solid View Mode.

![Material To Viewport](/images/gifs/07_MaterialToViewport.gif)


#### Delete Unused Materials
Delete from selected objects unused materials (not applyed to faces) and unused material slots.

![Delete Unused Materials](/images/gifs/12_DeleteUnusedMats.gif)


#### Add .L or .R suffix to Bones
Quick add suffix .L or .R to Selected Bones.

![Suffix Bones](/images/gifs/16_BonesSuffix.gif)


#### Merge Bones Tool
Tool For Easy Simplifying Armature: Delete (or Dissolve) Selected Bones (Exclude Active) and Transfer Vertex Weights to Active Bone.

![Merge Bones](/images/gifs/17_MergeBones.gif)


#### Active Material -> Selected
Assign active material to selected faces in MultiEdit Mode.

![Active Material To Selected](/images/gifs/14_ActiveMatToSelected.gif)


#### Addon Preferences
* Show/Hide UI Panels via Addon Preferences
* Changing Category for each Panel from Preferences

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)