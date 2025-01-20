# Blender Addon: ACT: Game Asset Creation Toolset

![Header](/images/headers/ACT_Header_1920.png)

**[English README](/README.md)**

**ACT** аддон для Blender, который содержит в себе набор инструментов, помогающих при создании низкополигональных ассетов для Blender.


# Загрузка
* ***[(2025.1) Blender 4.2+ (с Blender Extensions)](https://extensions.blender.org/add-ons/act-game-asset-creation-toolset/)***
* ***[(2025.1) Blender 4.2+ (с GitHub)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Releases/ACT_2025_1_Bl420.zip)***
* ***[ACT Unity Editor Script (для Unity 2022+)](https://github.com/mrven/Blender-Asset-Creation-Toolset/raw/master/Unity_Plugin/Releases/ACT_Unity_Plugin.unitypackage)***
-----------------------------------------------
* ***[Предыдущие версии](/Previous_Releases.md)***

# Документация
[![ACT Playlist](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/playlist?list=PLmXnsUZu0CRpLoJD79MC6AQf_phyXP62b)

# Спонсорство
Если вы хотите поддержать меня, то можете купить аддон на **[Blender Market](https://blendermarket.com/products/act)**

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mrven)

# Функции
## Что нового в ACT 2025?
[NEW] Добавление/замена/удаление постфикса \_LOD\* с заданным уровнем LOD'а \
[NEW] Пакетное назначение швов развёртки на модели по UV непосредственно из Object Mode \
[NEW] Export Tool: Возможность задавать пользовательские масштаб и оси при экспорте FBX или OBJ \
[NEW] Удаление дубликатов материалов \
[NEW] Выделение объектов с отрицательным масштабом \
[NEW] Удаление пустышек, под которыми нет объектов и мешей без геометрии \
[NEW] Удаление лупов через один (начиная с выделенной грани) \
[NEW] Схлопывание граней по одному (по длине лупа) \
[FIX] Исправлена ошибка установки аддона, если отключен Cycles \
[FIX] Clear Custom Normals применяется только к объектам, у которых есть custom normal data \
[IMPROVEMENT] Устанавливать дефолтное имя для UV когда поле "Name" пустое

## Origin Tools
![Origin Tools](/images/pngs/2025/01_Origin_Tools.png)\
[![Origin Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=cxcSM-HvMH8)

### Origin Align Tool
Выравнивание Origin Point объекта. Позволяет выровнять Origin по заданной оси по максимальной/минимальной/средней точки объекта, 3D-курсору или заданной координате.

### Set Origin to Selected (Edit Mode)
Выравнивание Origin по выделенным элементам. Является автоматизацией шагов: перемещение 3D-курсора к выделенному, переключение в объектный режим, установка Origin по 3D-курсору и возврат в режим редактирования.

## Renaming Tools
![Renaming Tools](/images/pngs/2025/02_Renaming_Tools.png)\
[![Renaming Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=pqz-mSK8n90)

### Numbering Objects
Удаляет стандартную нумерацию блендера и добавляет свою собственную нумерацию вдоль оси или по порядку аутлайнера:
* xxx_1, xxx_10, xxx_100
* xxx_01, xxx_10, xxx_100
* xxx_001, xxx_010, xxx_100

### Add/Remove LOD to Name
Добавление/замена/удаление постфикса \_LOD\* с заданным уровнем LOD'а.

### Add .L or .R suffix to Bones
Быстрое добавление суффикса .L или .R к выделенным костям.


## UV Tools
![UV Tools](/images/pngs/2025/03_UV_Tools.png)\
[![UV Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=ble4bwOJwjQ)

* Переименовывание UV-развёртку выделенных объектов по заданному индексу (каналу) развёртки. Например, у объектов, импортированных из 3Ds Max название развёртки UVChannel_1, а у объектов, созданных в Blender UVMap. Таким образом при объединении объектов вместо объединения развёрток они разбросаются по двум каналам. Также удобно задавать имя для канала Lightmap и т.п.
* Добавление нового UV-канала c заданным именем на выделенные объекты (с копированием UV  активного канала или автоматической развёрткой (Smart/Lightmap))
* Удаление UV-канала по индексу с выделенных объектов
* Выбор активного UV-канала в 3D View и Image/UV Editor по индексу

### Assign Seams from UV
Пакетное назначение швов развёртки на модели по UV непосредственно из Object Mode.

### UV Mover (UV Image Editor)
Инструмент, облегчающий масштабирование и перемещение островов с заданным шагом при паковке текстурных атласов.


## Export Tools
![Export Tools](/images/pngs/2025/04_Export.png)\
[![Export Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=XTyvRZLvVUg)

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
![Material Tools](/images/pngs/2025/05_Material_Tools.png)\
[![Material Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=WY9vJja1nqw)

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

### Cleanup Duplicated Materials
Удаление дубликатов материалов (по имени). Полезно, когда импортируется много моделей с одинаковыми материалами, но из разных файлов. В этом случае Blender создаёт множество копий материалов. Данная функция позволяет найти и назначить исходные материалы на все модели.


## Other Tools
![Other Tools](/images/pngs/2025/06_Other_Tools.png)\
[![Other Tools Overview](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=n8ZBI3KZ47Y)

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

### Select Objects with Negative Scale
Функция выделения объектов с отрицательным масштабом. В игровой разработке следует избегать объекты с отрицательным масштабом (особенно если это касается коллайдеров и других физических объектов). Данный инструмент позволяет найти такие объекты.

### Cleanup Empties
Удаление пустышек, под которыми нет объектов и мешей без геометрии.


## Geometry Tools
![Geometry Tools](/images/pngs/2025/07_Geometry_Tools.png)

### Dissolve Checker Loops
Удаление лупов через один (начиная с выделенной грани). Идеально для упрощения цилиндрических моделей.

### Collapse Checker Edges
Схлопывание граней по одному (по длине лупа). Идеально для упрощения сферических объектов.


## Addon Preferences
* Возможность включать/отключать через настройки аддона видимость панелей
* Возможность изменять категорию для каждой панели через настройки аддона

![Addon Preferences](/images/pngs/01_Addon_Prefs.png)

[<img src="https://api.gitsponsors.com/api/badge/img?id=190054403" height="20">](https://api.gitsponsors.com/api/badge/link?p=R7W5zpiWrH5vKtok3kzishcHSm+vXLZUisxg1E+mz6+XIavgMaeedIgSiO/Pg8qJqY/tYxmwupuzjsP75azNlSy4YbYlJdL3ENeRkPjkRrmotBAe8wjwLaG/9IT0ejm234ouL7ohak0h8SewxjZpPA==)