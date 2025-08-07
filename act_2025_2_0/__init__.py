bl_info = {
	"name": "ACT: Game Asset Creation Toolset",
	"description": "Tools for easy create and export low-poly game assets",
	"author": "Ivan 'mrven' Vostrikov,  Felipe Torrents, mokalux, Oxicid, ani-kun",
	"wiki_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"tracker_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset/issues",
	"doc_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"version": (2025, 2, 0),
	"blender": (3, 0, 0),
	"location": "3D View > Toolbox > ACT",
	"category": "Object",
}

from . import props
from . import preferences
from . import origin_tools
from . import rename_tools
from . import uv_tools
from . import import_export_tools
from . import material_tools
from . import other_tools
from . import geometry_tools

modules_names = (
	props,
	origin_tools,
	rename_tools,
	uv_tools,
	import_export_tools,
	material_tools,
	other_tools,
	geometry_tools,
	preferences
)

def register():
	for module_name in modules_names:
		module_name.register()


def unregister():
	for module_name in reversed(modules_names):
		module_name.unregister()