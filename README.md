# Blender Addon: Asset Creation Toolset

![Header](/images/header.png)

**[Russian README](/README_ru.md)**

**Asset Creation Toolset** is Many Tools for Game Asset Creation (Batch Import/Export FBXs, Origin Aligment Tool, Renaming, Low-Poly Art workflow tools, etc.) for Blender 2.79 and 2.8.

***Download latest version:***

* ***[Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***
* ***[Blender 2.80](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_5_0_280.zip)***

If you want to support me you can buy this addon:
* ***[Gumroad (Pay what you want)](https://gumroad.com/l/hPXIh)***

### "Origin Tools" Group
Tools fof operations with Origin Point.


#### Origin Rotation
Tool for Rotation Origin Point without rotating geometry.

![Origin Rotate](/images/origin_rotate.gif)


#### Origin Align
Aligment Origin Point: 
* Max/Min point of object for X, Y or Z axis
* 3D Cursor (Separate Axis)
* Coordinates

![Origin Align](/images/origin_align.gif)


#### Set Origin to Selected (Edit Mode)
Set Origin Point to Selected Element(s)

![Origin To Selected](/images/origin_to_selected.gif)


### "Rename Tools" Group
Tools fof renaming objects and uv maps.


#### Rename UV
Tool for Batch Renaming UV by Index (example, Lightmap - second uv channel).

![Rename UV](/images/rename_uv.gif)


#### Rename Objects
Tool for Batch Renaming Objects. Available next functions: Add prefix , Add postfix, Replace String and Set New Name.

![Rename Objects](/images/rename_objects.gif)


#### Numbering Objects
Delete Blender's default numbering and add new numbering by Axis and with pattern:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100


### "Import/Export Tools" Group
Tools fof Batch Import/Export Objects.


#### Clear Custom Normals
Clear Custom Normals and set Autosmooth to 180 degrees for Selected Objects.

![Clear Custom Normals](/images/clear_custom_normals.gif)


#### Flip/Calculate Normals
Flip or Recalculate Normals for Selected Objects.

![Flip Calculate Normals](/images/recalc_normals.gif)


#### Export FBX to Unity
Batch Export Selected Objects for Unity (Fix Scale and Rotation). Available some modes:
* Export All Selected Object into One FBX
* Export Each Object into Individual FBX
* Batch Objects by Parent

![Export FBXs](/images/export_fbxs.gif)


#### Import FBXs/OBJs
Batch Import FBX and OBJ files.

![Import FBXs OBJs](/images/batch_import.gif)


### "Low Poly Art Tools" Group
Tools fof Low Poly Art Style Models.


#### Create Palette Texture
Create Palette Texture (32x32px) for Selected Objects painted with colored materials. In one palette texture can be up to 256 colors (materials).
**Note: for Blender 2.79 uses Blender Render, for Blender 2.8 uses Cycles Render**

![Create Palette Texture](/images/create_palette.gif)


#### Texture to Vertex Color (ONLY 2.79)
With this function you can bake created palette texture to vertex color. For using this function you need enable addon "Bake UV-Texture to Vertex Color".

![Texture to Vertex Color](/images/vertex_colors.gif)


#### Clear UV Maps
Just remove all UV Maps from selected objects.

![Clear UV Maps](/images/clear_uv.gif)


#### Clear Vertex Colors
Clear All Vertex Colors from Selected Objects.


### "Other Tools" Group


#### Copy Texture Assignment (ONLY 2.79)
Copy Texture Assignment in UV/Image Editor from Active to Selected Objects. With this Function you can Fast Assign Grid or Base Color Texture for Selected Objects.

![Copy Texture Assignment](/images/copy_texture.gif)


#### Clear Custom Orientations (ONLY 2.79)
Delete All Custom Orientations.

![Clear Custom Orientations](/images/clear_custom_ori.gif)


#### Obj Name -> Mesh Name
Copy Object Name to Mesh(Data-Block) Name.

![Copy Name](/images/mesh_name.gif)


#### UV Mover (UV Image Editor)
Tool for easier Atlas Packing.

![UV Mover](/images/uv_mover.gif)
