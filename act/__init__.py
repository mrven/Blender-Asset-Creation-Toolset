bl_info = {
	"name": "ACT: Game Asset Creation Toolset",
	"description": "Tools for easy create and export low-poly game assets",
	"author": "Ivan 'mrven' Vostrikov,  Felipe Torrents, mokalux, Oxicid, ani-kun",
	"wiki_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"tracker_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset/issues",
	"doc_url": "https://github.com/mrven/Blender-Asset-Creation-Toolset#readme",
	"version": (2026, 1, 0),
	"blender": (3, 0, 0),
	"location": "3D View > Toolbox > ACT",
	"category": "Object",
}

_needs_reload = "bpy" in locals()

import bpy
from bpy.app.handlers import persistent
from bpy.app import timers

from .common import (
	constants,
	config_json,
	utils as common_utils,
	props,
	preferences,
)
from .support import operators as support_operators, ui as support_ui
from .origin import utils as origin_utils, operators as origin_operators, ui as origin_ui
from .rename import utils as rename_utils, operators as rename_operators, ui as rename_ui
from .uv import utils as uv_utils, operators as uv_operators, ui as uv_ui
from .geometry import operators as geometry_operators, ui as geometry_ui
from .import_export import (
	utils as import_export_utils,
	operators as import_export_operators,
	ui as import_export_ui,
)
from .material import operators as material_operators, ui as material_ui
from .other import utils as other_utils, operators as other_operators, ui as other_ui

_reload_modules = (
	constants,
	common_utils,
	config_json,
	props,
	preferences,
	support_operators,
	support_ui,
	origin_utils,
	origin_operators,
	origin_ui,
	rename_utils,
	rename_operators,
	rename_ui,
	uv_utils,
	uv_operators,
	uv_ui,
	geometry_operators,
	geometry_ui,
	import_export_utils,
	import_export_operators,
	import_export_ui,
	material_operators,
	material_ui,
	other_utils,
	other_operators,
	other_ui,
)

if _needs_reload:
	import importlib

	for module in _reload_modules:
		importlib.reload(module)


_modules = (
	props,
	preferences,
	support_operators,
	support_ui,
	origin_operators,
	origin_ui,
	rename_operators,
	rename_ui,
	uv_operators,
	uv_ui,
	geometry_operators,
	geometry_ui,
	import_export_operators,
	import_export_ui,
	material_operators,
	material_ui,
	other_operators,
	other_ui,
)

def deferred_initialize():
	config_json.load_or_initialize_prefs()
	config_json.saving_enabled = True
	config_json.copy_prefs_to_props(force=_needs_reload)

	return None


@persistent
def on_load_post(_):
	config_json.load_or_initialize_prefs()
	config_json.copy_prefs_to_props()


def register():
	config_json.saving_enabled = False
	for module in _modules:
		if hasattr(module, "register"):
			module.register()

	timers.register(deferred_initialize, first_interval=0.1)

	if on_load_post not in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.append(on_load_post)


def unregister():
	if on_load_post in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.remove(on_load_post)

	for module in reversed(_modules):
		if hasattr(module, "unregister"):
			module.unregister()
