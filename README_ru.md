# Blender Addon: ACT: Game Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[English README](/README.md)**

**ACT** аддон для Blender, который содержит в себе набор инструментов, помогающих при создании низкополигональных ассетов для Blender.

[<img src="https://api.gitsponsors.com/api/badge/img?id=190054403" height="50">](https://api.gitsponsors.com/api/badge/link?p=R7W5zpiWrH5vKtok3kziskOzBnSDKorI5wOcmiIPBzz9i28hZmWFBXmcyJL/atWR9JoicfSKTaNSfh+Mfp0bcA==)

***Скачать последнюю версию:***

* ***[(2024.2) Blender 4.2+ (с Blender Extensions)](https://extensions.blender.org/add-ons/act-game-asset-creation-toolset/)***
* ***[(2024.2) Blender 4.1+](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2024_2_Bl410.zip)***
* ***[(2023.2) Blender 4.0+](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2023_2_Bl400.zip)***
* ***[(2023.1) Blender 3.6+](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2023_1_Bl361.zip)***
* ***[ACT Unity Editor Скрипт (для ACT 2023.1+)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Unity_Plugin/Releases/ACT_2023_1_Unity_Plugin.unitypackage)***
-----------------------------------------------------
* ***[(3.3) Blender 3.4+](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_3_341.zip)***
* ***[(3.1.5) Blender 2.90 - 3.0](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_5_290.zip)***
* ***[(3.1.2) Blender 2.83](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_3_1_2_283.zip)***
* ***[(2.4.1) Blender 2.79](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/Asset_Creation_Toolset_2_4_1_279.zip)***

Если вы хотите поддержать меня, то можете купить аддон на следующих площадках:
* ***[Blender Market](https://blendermarket.com/products/asset-creation-toolset-2024)***


***[Смотреть обзор всех функций (плейлист Youtube)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRpLoJD79MC6AQf_phyXP62b)***

# Функции
## Origin Tools

[![Origin Tools Overview](https://img.youtube.com/vi/cxcSM-HvMH8/0.jpg)](https://www.youtube.com/watch?v=cxcSM-HvMH8)

### Origin Align Tool
Выравнивание Origin Point объекта. Позволяет выровнять Origin по заданной оси по максимальной/минимальной/средней точки объекта, 3D-курсору или заданной координате.

### Set Origin to Selected (Edit Mode)
Выравнивание Origin по выделенным элементам. Является автоматизацией шагов: перемещение 3D-курсора к выделенному, переключение в объектный режим, установка Origin по 3D-курсору и возврат в режим редактирования.

### Numbering Objects
Удаляет стандартную нумерацию блендера и добавляет свою собственную нумерацию вдоль оси или по порядку аутлайнера:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

### Add .L or .R suffix to Bones
Быстрое добавление суффикса .L или .R к выделенным костям.


## UV Tools

[![UV Tools Overview](https://img.youtube.com/vi/ble4bwOJwjQ/0.jpg)](https://www.youtube.com/watch?v=ble4bwOJwjQ)

* Переименовывание UV-развёртку выделенных объектов по заданному индексу (каналу) развёртки. Например, у объектов, импортированных из 3Ds Max название развёртки UVChannel_1, а у объектов, созданных в Blender UVMap. Таким образом при объединении объектов вместо объединения развёрток они разбросаются по двум каналам. Также удобно задавать имя для канала Lightmap и т.п.
* Добавление нового UV-канала c заданным именем на выделенные объекты (с копированием UV  активного канала или автоматической развёрткой (Smart/Lightmap))
* Удаление UV-канала по индексу с выделенных объектов
* Выбор активного UV-канала в 3D View и Image/UV Editor по индексу

### UV Mover (UV Image Editor)
Инструмент, облегчающий масштабирование и перемещение островов с заданным шагом при паковке текстурных атласов.


## Export Tools

[![Export Tools Overview](https://img.youtube.com/vi/XTyvRZLvVUg/0.jpg)](https://www.youtube.com/watch?v=XTyvRZLvVUg)

### Export OBJ/FBX/GLTF to Unity/UE/Godot
Пакетный экспорт выделенных объектов в FBX/OBJ/GLTF с корректным масштабом и поворотом. Рядом с файлом .Blend будет создана папка, в которую будут экспортированы объекты. Каждый объект/группа/коллекция будет экспортирован(а) в отдельный файл.

#### Алгоритм экспорта в Unity
Теперь у ACT два разных алгоритма для экспорта FBXs в Unity: ***"Unity"*** и ***"Unity (Legacy)"***.\
![Target_Engine](/images/pngs/2023/01_Target.png)

#### Профиль экспорта "Unity"
Этот профиль поддерживает объекты с Linked Data, более точная работа с ригами, анимациями, углами и осями. ***Но этот профиль требует дополнительных манипуляций с моделями при импорте в Unity.*** Вы должны установить в параметрах импорта модели "Scale Factor" в 100 и включить опцию "Bake Axis Conversion".\
![Import_Settings](/images/pngs/2023/02_Import_Settings.png)

Для автоматизации этих шагов я сделал ***Unity Editor скрипт*** и с помощью него можно установить эти параметры следующими способами:
1. Выбрать модели -> RMB -> ACT/Fix Models Transform.
![Fix_Transforms](/images/pngs/2023/03_Fix_Transforms.png)
2. Открыть окно ACT Settings (Window -> ACT -> Settings) и включить Models Postprocessor. Постпроцессор будет автоматически устанавливать параметры для любой импортируемой модели (или для моделей, которые содержат заданную строку или символ).
![ACT_Settings_1](/images/pngs/2023/04_ACT_Settings_1.png)\
![ACT_Settings_2](/images/pngs/2023/05_ACT_Settings_2.png)\
![ACT_Settings_3](/images/pngs/2023/06_ACT_Settings_3.png)\
Unity editor ACT скрипт поставляется вместе с ACT Blender add-on.

#### Профиль экспорта "Unity (Legacy)"
Но вы до сих пор можете использовать предыдущий алгоритм экспорта: Этот алгоритм не требует дополнительных манипуляций в Unity, а также этот алгоритм позволяет сохранить обратную совместимость с уже существующими моделями.\
![Old_Algorithm](/images/pngs/2023/07_Old_Algorithm.png)


## Material/Texture Tools

[![Material Tools Overview](https://img.youtube.com/vi/WY9vJja1nqw/0.jpg)](https://www.youtube.com/watch?v=WY9vJja1nqw)

### Material -> Viewport Color / Random Material Viewport Colors
Копирование Base Color материала в Viewport Color для режима отображения Solid View. Или назначение случайных цветов для материалов во Viewport.

### Clear UV Maps/Clear Vertex Colors
Удаление всех UV-развёрток или vertex color с выделенных объектов.

### Delete Unused Materials
Удаление с выделенных объектов неиспользуемых материалов и слотов.

### Create Palette Textures (Albedo, Roughness, Metallic, Opacity and Emission)
Создание текстуры-палитры для выделенных объектов, раскрашенных разными материалами. С объектов индексируются Diffuse цвета (или PBR сет) материалов и распределяются на текстуре 32 пикселя (одна палитра может содержать до 256 цветов). Затем на объектах создаётся UV-развёртка, в которой полигоны, имеющие один материал сводятся в точку и размещаются на палитре в соответсвующее место.

### Быстрый выбор текстуры из активного материала в Image/UV Editor

### Active Material -> Selected
Назначить активный материал на выделенные полигоны в режиме MultiEdit.


## Other Tools

[![Other Tools Overview](https://img.youtube.com/vi/n8ZBI3KZ47Y/0.jpg)](https://www.youtube.com/watch?v=n8ZBI3KZ47Y)

### Obj Name -> Data Name
Назначение имени меша/шрифта и т.п. по имени объекта.

### Collection Name -> Obj Name
Переносит имя коллекции в имя объекта. Вы можете использовать разные пути для этого:
1. Добавлени имени коллекции перед или после текущего имени объекта. Например, ***"CollectionName_ObjectName"*** или ***"ObjectName_CollectionName"***
2. Замена имени объекта на "Collection Name + Type + Numbering", Например, ***"CollectionName_Mesh_001"*** или ***"CollectionName_MESH_001"***. Спасибо @Oxicid за имплементацию!\
![Col_To_Name](/images/pngs/2023/09_Col_To_Name.png)

### Clear Custom Normals
Удаляет с выделенных объектов объектов информацию о кастомных нормалях и устанавливает автосглаживание (AutoSmooth) на 180 градусов.

### Flip/Calculate Normals
Перевернуть/пересчитать нормали в объектном режиме для выделенных объектов.

### Merge Bones Tool
Инструмент для упрощения скелета: Удаление выделенных костей (кроме активной) и перенос весов на активную кость.


## Addon Preferences
* Возможность включать/отключать через настройки аддона видимость панелей
* Возможность изменять категорию для каждой панели через настройки аддона

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)
