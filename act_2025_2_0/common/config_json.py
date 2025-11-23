import os
import json
import bpy
from bpy.utils import user_resource

from ..common import utils as common_utils

saving_enabled = False
package_name = common_utils.get_package_name()

def get_prefs_path():
	config_dir = user_resource('CONFIG', path='act', create=True)
	os.makedirs(config_dir, exist_ok=True)
	return os.path.join(config_dir, 'preferences.json')


def save_addon_prefs():
	prefs = bpy.context.preferences.addons[package_name].preferences
	data = {}
	for prop in prefs.bl_rna.properties:
		key = prop.identifier
		if key == "rna_type":
			continue
		value = getattr(prefs, key)
		data[key] = value
	with open(get_prefs_path(), 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=4)


def load_or_initialize_prefs():
	prefs = bpy.context.preferences.addons[package_name].preferences
	path = get_prefs_path()

	if os.path.exists(path):
		try:
			with open(path, 'r', encoding='utf-8') as f:
				data = json.load(f)

			for k, v in data.items():
				if hasattr(prefs, k):
					setattr(prefs, k, v)
		except Exception as e:
			print(f"[ACT Prefs] Failed to load: {e}")
	else:
		print(f"[ACT Prefs] No preferences file found at {path}")
		save_addon_prefs()


def copy_prefs_to_props(force = False):
	props = getattr(bpy.context.scene, "act", None)

	if props is None:
		return

	prefs = bpy.context.preferences.addons[package_name].preferences

	if not getattr(props, "initialized", False) or force:
		# Export
		props.export_mode = prefs.export_mode
		props.export_format = prefs.export_format
		props.obj_separate_by_materials = prefs.obj_separate_by_materials
		props.obj_export_smooth_groups = prefs.obj_export_smooth_groups
		props.gltf_export_image_format = prefs.gltf_export_image_format
		props.gltf_export_attributes = prefs.gltf_export_attributes
		props.apply_rot = prefs.apply_rot
		props.apply_rot_rotated = prefs.apply_rot_rotated
		props.apply_scale = prefs.apply_scale
		props.apply_loc = prefs.apply_loc
		props.set_custom_fbx_name = prefs.set_custom_fbx_name
		props.custom_fbx_name = prefs.custom_fbx_name
		props.delete_mats_before_export = prefs.delete_mats_before_export
		props.triangulate_before_export = prefs.triangulate_before_export
		props.custom_export_path = prefs.custom_export_path
		props.export_path = prefs.export_path
		props.export_target_engine = prefs.export_target_engine
		props.export_custom_options = prefs.export_custom_options
		props.export_loose_edges = prefs.export_loose_edges
		props.export_tangent_space = prefs.export_tangent_space
		props.export_smoothing = prefs.export_smoothing
		props.export_custom_props = prefs.export_custom_props
		props.export_combine_meshes = prefs.export_combine_meshes
		props.export_only_deform_bones = prefs.export_only_deform_bones
		props.export_add_leaf_bones = prefs.export_add_leaf_bones
		props.export_vc_color_space = prefs.export_vc_color_space
		props.use_custom_export_scale = prefs.use_custom_export_scale
		props.custom_export_scale_value = prefs.custom_export_scale_value
		props.use_custom_export_axes = prefs.use_custom_export_axes
		props.custom_export_forward_axis = prefs.custom_export_forward_axis
		props.custom_export_up_axis = prefs.custom_export_up_axis

		props.initialized = True


def load_default_prefs():
	default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default_prefs.json")
	try:
		with open(default_path, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception as e:
		print(f"[ACT Prefs] Failed to load default prefs: {e}")
		return {}


def apply_defaults_from_file():
	prefs = bpy.context.preferences.addons[package_name].preferences
	defaults = load_default_prefs()
	if not defaults:
		return False

	for key, value in defaults.items():
		try:
			prop_type = type(getattr(prefs, key))
			setattr(prefs, key, prop_type(value))
		except Exception as e:
			print(f"[ACT Prefs] Failed to apply {key}: {e}")
	return True