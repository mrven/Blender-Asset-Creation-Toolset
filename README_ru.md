# Blender Addon: Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[English README](/README.md)**

**Asset Creation Toolset** аддон для Blender, который содержит в себе набор инструментов, помогающих при создании низкополигональных ассетов для Blender 2.79 и 2.8 (и выше).

***Скачать последнюю версию:***

* ***[(3.2) Blender 3.1 и выше](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_2_310.zip)***
* ***[(3.1.5) Blender 2.90 - 3.0](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_5_290.zip)***
* ***[(3.1.2) Blender 2.83](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_2_283.zip)***
* ***[(2.4.1) Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***

Если вы хотите поддержать меня, то можете купить аддон на следующих площадках:
* ***[Gumroad (Свободная цена)](https://gumroad.com/l/hPXIh)***

***[Смотреть обзор всех функций (плейлист Youtube)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRr_UOQp3TapOVyEqbzZ0MkL)***

#### Origin Align Tool
Выравнивание Origin Point объекта. Позволяет выровнять Origin по заданной оси по максимальной/минимальной точки объекта, 3D-курсору или заданной координате.

![Origin Align](/images/gifs/01_Origin_Align.gif)


#### Set Origin to Selected (Edit Mode)
Выравнивание Origin по выделенным элементам. Является автоматизацией шагов: перемещение 3D-курсора к выделенному, переключение в объектный режим, установка Origin по 3D-курсору и возврат в режим редактирования.

![Origin To Selected](/images/gifs/13_OriginToSelected.gif)


#### UV Tools
* Переименовывание UV-развёртку выделенных объектов по заданному индексу (каналу) развёртки. Например, у объектов, импортированных из 3Ds Max название развёртки UVChannel_1, а у объектов, созданных в Blender UVMap. Таким образом при объединении объектов вместо объединения развёрток они разбросаются по двум каналам. Также удобно задавать имя для канала Lightmap и т.п.
* Добавление нового UV-канала c заданным именем на выделенные объекты
* Удаление UV-канала по индексу с выделенных объектов
* Выбор активного UV-канала в 3D View и Image/UV Editor по индексу

![Rename UV](/images/gifs/02_RenameUV.gif)
![UV Tools](/images/pngs/02_UV_Tools.png)


#### Быстрый выбор текстуры из активного материала в Image/UV Editor

![Quick Select Texture](/images/pngs/03_Quick_Select_Texture.png)


#### Numbering Objects
Удаляет стандартную нумерацию блендера и добавляет свою собственную нумерацию:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

![Numbering Objects](/images/gifs/03_Numbering.gif)


#### Clear Custom Normals
Удаляет с выделенных объектов объектов информацию о кастомных нормалях и устанавливает автосглаживание (AutoSmooth) на 180 градусов.

![Clear Custom Normals](/images/gifs/10_ClearCustomNormals.gif)


#### Flip/Calculate Normals
Перевернуть/пересчитать нормали в объектном режиме для выделенных объектов.

![Flip Calculate Normals](/images/gifs/11_CalcNormals.gif)


#### Export OBJ или FBX to Unity/UE4
Пакетный экспорт выделенных объектов в FBX/OBJ с корректным масштабом и поворотом. Рядом с файлом .Blend будет создана папка “FBXs” или "OBJs", в которую будут экспортированы объекты. Каждый объект будет экспортирован в отдельный FBX/OBJ. Работает только со статичными мешами. Также обратите внимание, что у объектов в сцене перед экспортом применяются масштабы и поворот.

![Export FBXs](/images/gifs/04_ExportFBX.gif)


#### Import FBXs/OBJs
Пакетный импорт FBX и OBJ файлов.

![Import FBXs OBJs](/images/gifs/05_ImportFBX.gif)


#### Create Palette Textures (Albedo, Roughness, Metallic, Opacity and Emission)
Создание текстуры-палитры для выделенных объектов, раскрашенных разными материалами. С объектов индексируются Diffuse цвета (или PBR сет) материалов и распределяются на текстуре 32 пикселя (одна палитра может содержать до 256 цветов). Затем на объектах создаётся UV-развёртка, в которой полигоны, имеющие один материал сводятся в точку и размещаются на палитре в соответсвующее место.
**Примечание: для Blender 2.79 используется Blender Render, а для Blender 2.8 используется Cycles Render**

![Create Palette Texture](/images/gifs/06_PaletteTexture.gif)


#### Clear UV Maps/Clear Vertex Colors
Удаление всех UV-развёрток или vertex color с выделенных объектов.

![Clear UV Maps](/images/gifs/08_ClearUVandVC.gif)


#### Obj Name -> Data Name
Назначение имени меша/шрифта и т.п. по имени объекта.

![Copy Name](/images/gifs/09_ObjToMeshName.gif)


#### UV Mover (UV Image Editor)
Инструмент, облегчающий масштабирование и перемещение островов с заданным шагом при паковке текстурных атласов.

![UV Mover](/images/gifs/15_UVMover.gif)


#### Material -> Viewport Color
Копирование Base Color материала в Viewport Color для режима отображения Solid View.

![Material To Viewport](/images/gifs/07_MaterialToViewport.gif)


#### Delete Unused Materials
Удаление с выделенных объектов неиспользуемых материалов и слотов.

![Delete Unused Materials](/images/gifs/12_DeleteUnusedMats.gif)


#### Add .L or .R suffix to Bones
Быстрое добавление суффикса .L или .R к выделенным костям.

![Suffix Bones](/images/gifs/16_BonesSuffix.gif)


#### Merge Bones Tool
Инструмент для упрощения скелета: Удаление выделенных костей (кроме активной) и перенос весов на активную кость.

![Merge Bones](/images/gifs/17_MergeBones.gif)

#### Active Material -> Selected
Назначить активный материал на выделенные полигоны в режиме MultiEdit.

![Active Material To Selected](/images/gifs/14_ActiveMatToSelected.gif)


#### Addon Preferences
* Возможность включать/отключать через настройки аддона видимость панелей
* Возможность изменять категорию для каждой панели через настройки аддона

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)