bl_info = {
	"name": "Asset Creation Toolset",
	"description": "Tools for easy create and export low-poly assets for games",
	"author": "Ivan 'mrven' Vostrikov,  Felipe Torrents, mokalux, Oxicid, ani-kun",
	"wiki_url": "https://gum.co/hPXIh",
	"tracker_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset/issues",
	"doc_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"version": (2024, 3, 1),
	"blender": (4, 1, 0),
	"location": "3D View > Toolbox > ACT",
	"category": "Object",
}

from . import props
from . import preferences
from . import utils
from . import origin_tools
from . import rename_tools
from . import uv_tools
from . import import_export_tools
from . import material_tools
from . import other_tools

modules_names = (
	props,
	origin_tools,
	rename_tools,
	uv_tools,
	import_export_tools,
	material_tools,
	other_tools,
	preferences
)

def register():
	for module_name in modules_names:
		module_name.register()

def unregister():
	for module_name in reversed(modules_names):
		module_name.unregister()