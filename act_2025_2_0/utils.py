import re
import collections
from collections import defaultdict
import bpy
import bmesh

from datetime import datetime


# Find min and max vertex coordinates
def find_min_max_verts(obj, coord_index):
	bpy.ops.mesh.reveal()

	# Get bmesh from active object
	bm = bmesh.from_edit_mesh(obj.data)
	bm.verts.ensure_lookup_table()

	if len(bm.verts) == 0:
		result = None
	else:
		min_co = (obj.matrix_world @ bm.verts[0].co)[coord_index]
		max_co = (obj.matrix_world @ bm.verts[0].co)[coord_index]

		for v in bm.verts:
			if (obj.matrix_world @ v.co)[coord_index] < min_co:
				min_co = (obj.matrix_world @ v.co)[coord_index]
			if (obj.matrix_world @ v.co)[coord_index] > max_co:
				max_co = (obj.matrix_world @ v.co)[coord_index]

		result = (min_co, max_co)

	return result


# Check string is a number
def str_is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


# Message Box
def show_message_box(message="", title="Message Box", icon='INFO'):
	def draw(self, context):
		self.layout.label(text=message)

	bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# Prefilter Export Name
def prefilter_export_name(name):
	result = re.sub("[#%&{}<>\\\*?/'\":`|]", "_", name)

	return result


# Export Model
def export_model(path, name):
	act = bpy.context.scene.act

	if act.export_custom_options:
		# Scale Defaults
		apply_scale_options_value = 'FBX_SCALE_NONE'
		global_scale_value = 1.0
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY':
			apply_scale_options_value = 'FBX_SCALE_ALL'
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY2023':
			global_scale_value = 0.01

		# Custom Scale Option
		if act.use_custom_export_scale:
			apply_scale_options_value = 'FBX_SCALE_CUSTOM'
			global_scale_value = act.custom_export_scale_value

		# Axes Defaults
		forward_axis = '-Z'
		up_axis = 'Y'
		use_transform = True
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY2023':
			forward_axis = '-Y'
			up_axis = 'Z'
			use_transform = False
		if act.export_format == 'OBJ':
			forward_axis = 'NEGATIVE_Z'

		# Custom Axes Option
		if act.use_custom_export_axes:
			forward_axis = act.custom_export_forward_axis
			up_axis = act.custom_export_up_axis
			use_transform = False
			if act.export_format == 'OBJ':
				forward_axis = forward_axis.replace('-', 'NEGATIVE_')
				up_axis = up_axis.replace('-', 'NEGATIVE_')

		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					use_space_transform=use_transform)
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					use_space_transform=use_transform)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					use_space_transform=use_transform)

		if act.export_format == 'OBJ':
			bpy.ops.wm.obj_export(
				filepath=str(path + name + '.obj'), export_selected_objects=True, apply_modifiers=True,
				export_smooth_groups=act.obj_export_smooth_groups, export_normals=True, export_uv=True,
				export_materials=True, export_triangulated_mesh=act.triangulate_before_export,
				export_object_groups=True, export_material_groups=act.obj_separate_by_materials,
				global_scale=global_scale_value, path_mode='AUTO', forward_axis=forward_axis, up_axis=up_axis)

		if act.export_format == 'GLTF':
			bpy.ops.export_scene.gltf(
				filepath=str(path + name + '.glb'), check_existing=False,
				export_image_format=act.gltf_export_image_format,
				export_tangents=act.gltf_export_tangents, export_attributes=act.gltf_export_attributes,
				use_selection=True, export_extras=act.gltf_export_custom_properties,
				export_def_bones=act.gltf_export_deform_bones_only)
	else:
		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_ALL', add_leaf_bones=False, colors_type='LINEAR',
					use_custom_props=True)
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True,
					add_leaf_bones=False, colors_type='LINEAR', use_custom_props=True)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options='FBX_SCALE_NONE',
					global_scale=0.01, colors_type='LINEAR', axis_forward='-Y', axis_up='Z',
					add_leaf_bones=False,
					use_custom_props=True, use_space_transform=False)

		if act.export_format == 'OBJ':
			bpy.ops.wm.obj_export(
				filepath=str(path + name + '.obj'), export_selected_objects=True, apply_modifiers=True,
				export_smooth_groups=True, export_normals=True, export_uv=True,
				export_materials=True, export_triangulated_mesh=act.triangulate_before_export,
				export_object_groups=True, export_material_groups=True,
				global_scale=1, path_mode='AUTO', forward_axis='NEGATIVE_Z', up_axis='Y')

		if act.export_format == 'GLTF':
			bpy.ops.export_scene.gltf(
				filepath=str(path + name + '.glb'), check_existing=False, export_image_format='AUTO',
				export_tangents=False, export_attributes=False,
				use_selection=True, export_extras=True, export_def_bones=False)


# Execution Time
def print_execution_time(function_name, start_time):
	act = bpy.context.scene.act

	if act.debug:
		finish_time = datetime.now()
		execution_time = finish_time - start_time
		seconds = (execution_time.total_seconds())
		milliseconds = round(seconds * 1000)
		print(function_name + " finished in " + str(seconds) + "s (" + str(milliseconds) + "ms)")


# Exclude unnecessary objects
def selected_obj_with_unique_data(obj_type='MESH'):
	objs_with_instances = collections.defaultdict(list)

	for obj in bpy.context.selected_objects:
		if obj.type == obj_type:
			objs_with_instances[obj.data].append(obj)
	return [objs[0] for objs in objs_with_instances.values()]


# Check Cycles Addon is Enabled or Not
def cycles_is_enabled():
	is_cycles_enabled = False

	for module_name in bpy.context.preferences.addons.keys():
		if module_name == 'cycles':
			is_cycles_enabled = True

	return is_cycles_enabled


# Get Mesh Selection
def get_mesh_selection(obj):
	selection = []
	start_object_mode = bpy.context.object.mode
	bpy.ops.object.mode_set(mode='OBJECT')
	if bpy.context.scene.tool_settings.mesh_select_mode[2]:
		selection_source = obj.data.polygons
	elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
		selection_source = obj.data.edges
	else:
		selection_source = obj.data.vertices

	for i in range(len(selection_source)):
		if selection_source[i].select:
			selection.append(i)
	bpy.ops.object.mode_set(mode=start_object_mode)

	return selection


# Set Mesh Selection
def set_mesh_selection(obj, selection):
	start_object_mode = bpy.context.object.mode
	bpy.ops.object.mode_set(mode='OBJECT')
	if bpy.context.scene.tool_settings.mesh_select_mode[2]:
		for item in selection:
			obj.data.polygons[item].select = True
	elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
		for item in selection:
			obj.data.edges[item].select = True
	else:
		for item in selection:
			obj.data.vertices[item].select = True
	bpy.ops.object.mode_set(mode=start_object_mode)


# Object name to data name
def obj_name_to_data_name():
	obj_dict = defaultdict(list)

	for obj in bpy.context.selected_objects:
		if obj.type != 'EMPTY':
			obj_dict[obj.data].append(obj)

	for mesh, objects in obj_dict.items():
		for enum, object_mesh in enumerate(objects):
			# Skip instances
			if enum == 0:
				object_mesh.data.name = object_mesh.name
			else:
				break