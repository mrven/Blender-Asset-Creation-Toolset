# Blender Addon: Asset Creation Toolset

![Header](/images/header.png)

**[English README](/README.md)**

**Asset Creation Toolset** аддон для Blender, который содержит в себе набор инструментов, помогающих при создании низкополигональных ассетов для Blender 2.79 и 2.8.

***Скачать последнюю версию:***

* ***[Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***
* ***[Blender 2.80](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_280.zip)***

### Категория "Origin Tools"
Инструменты для работы с Origin (Pivot) Point объекта.


#### Origin Rotation
Поворот Origin Point объекта без поворота геометрии.

![Origin Rotate](/images/origin_rotate.gif)


#### Origin Align
Выравнивание Origin Point объекта. Позволяет выровнять Origin по заданной оси по максимальной/минимальной точки объекта, 3D-курсору или заданной координате.

![Origin Align](/images/origin_align.gif)


#### Set Origin to Selected (Edit Mode)
Выравнивание Origin по выделенным элементам. Является автоматизацией шагов: перемещение 3D-курсора к выделенному, переключение в объектный режим, установка Origin по 3D-курсору и возврат в режим редактирования.

![Origin To Selected](/images/origin_to_selected.gif)


### Категория "Rename Tools"
Инструменты для переименовывания объектов и UV-развёрток.


#### Rename UV
Позволяет переименовать UV-развёртку выделенных объектов по заданному индексу (каналу) развёртки. Например, у объектов, импортированных из 3Ds Max название развёртки UVChannel_1, а у объектов, созданных в Blender UVMap. Таким образом при объединении объектов вместо объединения развёрток они разбросаются по двум каналам. Также удобно задавать имя для канала Lightmap и т.п.

![Rename UV](/images/rename_uv.gif)


#### Rename Objects
Инструмент для группового переименовывания объектов. Доступны следующие функция переименовывания: Add preffix (добавить преффикс), Add postffix (добавить постфикс), Replace (найти и заменить строку) и New Name (задать новое имя).

![Rename Objects](/images/rename_objects.gif)


#### Numbering Objects
Удаляет стандартную нумерацию блендера и добавляет свою собственную нумерацию:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100


### Категория "Import/Export Tools"
Инструменты для импорта/экспорта объектов и работы с нормалями.


#### Clear Custom Normals
Удаляет с выделенных объектов объектов информацию о кастомных нормалях и устанавливает автосглаживание (AutoSmooth) на 180 градусов.

![Clear Custom Normals](/images/clear_custom_normals.gif)


#### Flip/Calculate Normals
Перевернуть/пересчитать нормали в объектном режиме для выделенных объектов.

![Flip Calculate Normals](/images/recalc_normals.gif)


#### Export FBX to Unity
Пакетный экспорт выделенных объектов в FBX с корректным масштабом и поворотом. Рядом с файлом .Blend будет создана папка “FBXs”, в которую будут экспортированы объекты. Каждый объект будет экспортирован в отдельный FBX. Работает только со статичными мешами. Также обратите внимание, что у объектов в сцене перед экспортом применяются масштабы и поворот.

![Export FBXs](/images/export_fbxs.gif)


#### Import FBXs/OBJs
Пакетный импорт FBX и OBJ файлов.

![Import FBXs OBJs](/images/batch_import.gif)


### Категория "Low Poly Art Tools"
Инструменты для подготовки ассетов в Low Poly Art стилистике.


#### Create Palette Texture
Создание текстуры-палитры для выделенных объектов, раскрашенных разными материалами. Инструмент работает только с Blender Render. С объектов индексируются Diffuse цвета материалов и распределяются на текстуре 32 пикселя (одна палитра может содержать до 256 цветов). Затем на объектах создаётся UV-развёртка, в которой полигоны, имеющие один материал сводятся в точку и размещаются на палитре в соответсвующее место.
**Примечание: для Blender 2.79 используется Blender Render, а для Blender 2.8 используется Cycles Render**

![Create Palette Texture](/images/create_palette.gif)


#### Texture to Vertex Color (ONLY 2.79)
Автоматизация для аддона Bake Vertex Color. Позволяет запекать текстуру в Vertex Color пакетно из объектного режима.

![Texture to Vertex Color](/images/vertex_colors.gif)


#### Clear UV Maps
Удаление всех UV-развёрток с выделенных объектов.

![Clear UV Maps](/images/clear_uv.gif)


#### Clear Vertex Colors
Удаление vertex color с выделенных объектов


### Категория "Other Tools"


#### Copy Texture Assignment (ONLY 2.79)
Копирует с активного объекта на выделенные текстуру, назначенную через UV/Image Editor.

![Copy Texture Assignment](/images/copy_texture.gif)


#### Clear Custom Orientations (ONLY 2.79)
Функция удаления всех кастомных ориентаций

![Clear Custom Orientations](/images/clear_custom_ori.gif)


#### Obj Name -> Mesh Name
Назначение имени меша по имени объекта.

![Copy Name](/images/mesh_name.gif)


#### UV Mover (UV Image Editor)
Инструмент, облегчающий масштабирование и перемещение островов с заданным шагом при паковке текстурных атласов.

![UV Mover](/images/uv_mover.gif)