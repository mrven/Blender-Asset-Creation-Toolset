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

import importlib

modules_order = (
	"common",
	"support",
	"origin",
	"rename",
	"uv",
	"geometry",
	"import_export",
	"material",
	"other",
)

modules = [importlib.import_module(f".{name}", __package__) for name in modules_order]

def register():
	for m in modules:
		if hasattr(m, "register"):
			m.register()


def unregister():
	for m in reversed(modules):
		if hasattr(m, "unregister"):
			m.unregister()