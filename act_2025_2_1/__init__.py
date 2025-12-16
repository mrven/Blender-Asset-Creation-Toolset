bl_info = {
	"name": "ACT: Game Asset Creation Toolset",
	"description": "Tools for easy create and export low-poly game assets",
	"author": "Ivan 'mrven' Vostrikov,  Felipe Torrents, mokalux, Oxicid, ani-kun",
	"wiki_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"tracker_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset/issues",
	"doc_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"version": (2025, 2, 1),
	"blender": (3, 0, 0),
	"location": "3D View > Toolbox > ACT",
	"category": "Object",
}

import importlib
import bpy
from bpy.app.handlers import persistent
from bpy.app import timers

from .common import config_json

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

def deferred_initialize():
	config_json.load_or_initialize_prefs()
	config_json.saving_enabled = True
	config_json.copy_prefs_to_props()

	return None


@persistent
def on_load_post(_):
	config_json.load_or_initialize_prefs()
	config_json.copy_prefs_to_props()


def register():
	config_json.saving_enabled = False
	for m in modules:
		if hasattr(m, "register"):
			m.register()

	timers.register(deferred_initialize, first_interval=0.1)

	if on_load_post not in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.append(on_load_post)


def unregister():
	if on_load_post in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.remove(on_load_post)

	for m in reversed(modules):
		if hasattr(m, "unregister"):
			m.unregister()