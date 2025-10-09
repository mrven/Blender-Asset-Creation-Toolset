import bpy
import os
import subprocess
import math
from datetime import datetime

from ..common import utils as common_utils
from . import utils

package_name = __package__.split('.')[0]

# FBX/OBJ/GLTF export
class ACTExport(bpy.types.Operator):
	"""Export FBXs/OBJs/GLTFs to Unity/UE/Godot"""
	bl_idname = "act.export"
	bl_label = "Export FBXs/OBJs/GLTFs"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		act.export_dir = ""
		incorrect_names = []

		# Prepare for export
		# Save selected objects and active object
		start_active_obj = context.active_object
		current_selected_obj = context.selected_objects
		name = context.active_object.name

		# Check custom name
		if act.export_mode == 'ALL' and act.set_custom_fbx_name and not act.custom_fbx_name:
			common_utils.show_message_box("Custom Name can't be empty", 'Saving Error', 'ERROR')
			return {'CANCELLED'}

		if not bpy.data.filepath and not act.custom_export_path:
			common_utils.show_message_box('Blend file is not saved. Try use Custom Export Path',
								   'Saving Error', 'ERROR')
			return {'CANCELLED'}

		if act.custom_export_path:
			if not act.export_path:
				common_utils.show_message_box("Export Path can't be empty",
				                              'Saving Error', 'ERROR')
				return {'CANCELLED'}

			export_path = os.path.realpath(bpy.path.abspath(act.export_path))

			if not os.path.exists(export_path):
				common_utils.show_message_box('Directory for export not exist',
				                              'Saving Error', 'ERROR')
				return {'CANCELLED'}

			path = export_path + os.sep
		else:
			path = bpy.path.abspath(f'//{act.export_format}s/')

		os.makedirs(path, exist_ok=True)

		# Filtering selected objects. Exclude all not meshes, empties, armatures, curves and text
		for x in current_selected_obj:
			if x.type not in {'MESH', 'EMPTY', 'ARMATURE', 'CURVE', 'FONT'}:
				x.select_set(False)
		current_selected_obj = context.selected_objects

		bpy.ops.ed.undo_push(message="FBX Bridge Export Prepare")

		# Undoable operations
		allow_multi_users = (act.export_format == 'FBX' and act.export_target_engine == 'UNITY'
		                     and not act.export_combine_meshes and not act.export_mode == 'INDIVIDUAL')

		if not allow_multi_users:
			bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

		bpy.ops.object.select_all(action='DESELECT')

		# Preparing transforms
		for obj in current_selected_obj:
			obj.select_set(True)
			context.view_layer.objects.active = obj

			if obj.type == 'EMPTY':
				continue

			# Remove all materials (optional)
			if act.delete_mats_before_export:
				if obj.type == 'MESH' and obj.data.materials:
					obj.data.materials.clear()

			# Triangulate with adding modifier (optional)
			if act.triangulate_before_export and obj.type in {'MESH', 'CURVE', 'FONT'}:
				bpy.ops.object.modifier_add(type='TRIANGULATE')

			# Remove disabled modifiers
			for modifier in reversed(obj.modifiers):
				if not (modifier.show_viewport and modifier.show_render):
					obj.modifiers.remove(modifier)

			# Apply modifiers (except Armature) and convert to mesh
			if obj.type == 'MESH' and obj.data.users < 2 and not obj.data.shape_keys:
				for modifier in obj.modifiers:
					if modifier.type == 'ARMATURE':
						continue
					try:
						bpy.ops.object.modifier_apply(modifier=modifier.name)
					except Exception as err:
						print(f"Can't apply modifier: {modifier.name} on {obj.name}", err)
						bpy.ops.object.modifier_remove(modifier=modifier.name)
			else:
				bpy.ops.object.convert(target='MESH')

			# Apply Scale and Rotation for UNITY Export or GLTF
			# Processing only objects without linked data
			if (act.export_format == 'FBX' and act.export_target_engine == 'UNITY') or act.export_format == 'GLTF':
				if not (obj.type == 'MESH' and obj.data.users > 1):
						bpy.ops.object.transform_apply(location=False, rotation=act.apply_rot, scale=act.apply_scale)
			else:
				# Apply scale
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=act.apply_scale)
				# Rotation Fix. Rotate X -90, Apply, Rotate X 90
				if act.apply_rot:
					context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

					if obj.parent is None:
						# Check object has any rotation
						# for option "Apply for Rotated Objects"
						child_rotated = False
						bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
						for x in context.selected_objects:
							if abs(x.rotation_euler.x) + abs(x.rotation_euler.y) + abs(x.rotation_euler.z) > 0.017:
								child_rotated = True

						bpy.ops.object.select_all(action='DESELECT')
						obj.select_set(True)

						rotate_params = dict(value=(math.pi * -90 / 180), orient_axis='X',
						                     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
						                     orient_type='GLOBAL', constraint_axis=(True, False, False),
						                     orient_matrix_type='GLOBAL', mirror=False,
						                     use_proportional_edit=False)

						# X-rotation fix
						if act.export_format == 'FBX' and (act.apply_rot_rotated
						                                   or (not act.apply_rot_rotated and not child_rotated)
						                                   or not act.export_mode == 'PARENT'):
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							bpy.ops.transform.rotate(**rotate_params)
							bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							bpy.ops.object.select_all(action='DESELECT')
							obj.select_set(True)
							rotate_params['value'] = (math.pi * 90 / 180)
							bpy.ops.transform.rotate(**rotate_params)

			obj.select_set(False)

		# Export Stage
		for obj in current_selected_obj:
			obj.select_set(True)

		if act.export_mode == 'ALL':
			# Combine All Meshes (Optional)
			if act.export_combine_meshes:
				# If parent object is mesh
				# combine all children to parent object
				if start_active_obj.type == 'MESH':
					context.view_layer.objects.active = start_active_obj
					bpy.ops.object.join()
				# If  parent is empty
				else:
					current_active = context.view_layer.objects.active
					# Combine all child meshes to first in list
					for obj in current_selected_obj:
						if obj.type == 'MESH':
							context.view_layer.objects.active = obj
					bpy.ops.object.join()
					context.view_layer.objects.active = current_active

				current_selected_obj = context.selected_objects

			# Set custom fbx/obj name (Optional)
			prefilter_name = act.custom_fbx_name if act.set_custom_fbx_name else name

			# Replace invalid chars
			name = common_utils.prefilter_export_name(prefilter_name)

			if name != prefilter_name:
				incorrect_names.append(prefilter_name)

			# Export FBX/OBJ/GLTF
			utils.export_model(path, name)

		# Export by parents
		if act.export_mode in {'PARENT', 'INDIVIDUAL'}:
			if act.export_mode == 'INDIVIDUAL':
				bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

			bpy.ops.object.select_all(action='DESELECT')

			for obj in current_selected_obj:
				if not obj.parent:
					obj.select_set(True)

			current_selected_obj = context.selected_objects

			for obj in current_selected_obj:
				bpy.ops.object.select_all(action='DESELECT')
				context.view_layer.objects.active = obj
				obj.select_set(True)

				# Combine All Meshes (Optional)
				if act.export_combine_meshes:
					# If parent object is mesh
					# combine all children to parent object
					if obj.type == 'MESH':
						bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
						bpy.ops.object.join()

						# CleanUp Empties without Children
						selected_objects_for_cleanup = context.selected_objects
						for x in selected_objects_for_cleanup:
							if x.type == "EMPTY" and len(x.children) == 0:
								bpy.data.objects.remove(x, do_unlink=True)

					# If  parent is not Mesh
					else:
						current_active = context.view_layer.objects.active
						parent_loc = current_active.location.copy()
						parent_name = current_active.name

						# Select all children
						bpy.ops.object.select_grouped(extend=False, type='CHILDREN_RECURSIVE')
						group_selected_objects = context.selected_objects

						# Combine all child meshes to first in list
						for x in group_selected_objects:
							if x.type == 'MESH':
								context.view_layer.objects.active = x
						bpy.ops.object.join()

						context.view_layer.objects.active.name = parent_name + '_Mesh'

						# Parent Combined mesh back
						current_active.select_set(True)
						context.view_layer.objects.active = current_active
						bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

						selected_objects_for_cleanup = context.selected_objects

						# Move Origin to Parent
						context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
						context.scene.cursor.location = parent_loc
						bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

						# CleanUp Empties without Children
						for x in selected_objects_for_cleanup:
							if x.type == "EMPTY" and len(x.children) == 0:
								bpy.data.objects.remove(x, do_unlink=True)

						context.view_layer.objects.active = current_active

				current_parent = context.view_layer.objects.active

				# Select only current object
				bpy.ops.object.select_all(action='DESELECT')

				current_parent.select_set(True)
				context.view_layer.objects.active = current_parent

				object_loc = obj.location.copy()

				if act.apply_loc:
					# Move object to center
					obj.location = (0, 0, 0)

				# Name is name of parent
				prefilter_name = current_parent.name
				name = common_utils.prefilter_export_name(prefilter_name)

				# Select Parent and his children
				bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')

				if name != prefilter_name:
					incorrect_names.append(prefilter_name)

				# Export FBX/OBJ/GLTF
				utils.export_model(path, name)

				if act.apply_loc:
					obj.location = object_loc

		# Export by collection
		if act.export_mode == 'COLLECTION':
			used_collections = []
			origin_loc = (0.0, 0.0, 0.0)
			context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
			obj_col_dict = {}
			# Collect used collections for selected objects
			for obj in current_selected_obj:
				collection_in_list = False

				for c in used_collections:
					if obj.users_collection[0].name == c:
						collection_in_list = True

				if not collection_in_list:
					used_collections.append(obj.users_collection[0].name)

				obj_col_dict[obj] = obj.users_collection[0].name

			# Select objects by collection and export
			for c in used_collections:
				bpy.ops.object.select_all(action='DESELECT')

				# Select Objects in Collection
				set_active_mesh = False
				for obj, col_name in obj_col_dict.items():
					if col_name == c:
						obj.select_set(True)
						if obj.type == 'MESH' and not set_active_mesh:
							context.view_layer.objects.active = obj
							if act.export_combine_meshes:
								obj.name = c
							set_active_mesh = True

				if act.export_combine_meshes and set_active_mesh:
					bpy.ops.object.join()

					# Move Origin to Parent
					context.scene.cursor.location = origin_loc
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

					# CleanUp Empties without Children
					selected_objects_for_cleanup = context.selected_objects
					for obj in selected_objects_for_cleanup:
						if obj.type == "EMPTY" and len(obj.children) == 0:
							bpy.data.objects.remove(obj, do_unlink=True)

				# Replace invalid chars
				name = common_utils.prefilter_export_name(c)

				if name != c:
					incorrect_names.append(c)

				# Export FBX/OBJ/GLTF
				utils.export_model(path, name)

			bpy.ops.object.select_all(action='DESELECT')

		# Show message about incorrect names
		if len(incorrect_names) > 0:
			common_utils.show_message_box(
				"Object(s) has invalid characters in name. Some chars in export name have been replaced",
				"Incorrect Export Names")

		bpy.ops.ed.undo_push(message="")
		bpy.ops.ed.undo()
		bpy.ops.ed.undo_push(message="ACT Export")

		context.scene.act.export_dir = path

		common_utils.print_execution_time("FBX/OBJ/GLTF Export", start_time)
		return {'FINISHED'}


# Open Export Directory
class OpenExportDir(bpy.types.Operator):
	"""Open Export Directory in OS"""
	bl_idname = "act.open_export_dir"
	bl_label = "Open Export Directory"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act

		if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_dir))):
			act.export_dir = ""
			common_utils.show_message_box('Directory not exist',
								   'Wrong Path',
								   'ERROR')

			return {'CANCELLED'}

		# Try open export dir in OS
		if len(act.export_dir) > 0:
			try:
				os.startfile(act.export_dir)
			except Exception:
				subprocess.Popen(['xdg-open', act.export_dir])
		else:
			common_utils.show_message_box('Export FBX\'s before',
								   'Info')
			return {'FINISHED'}

		common_utils.print_execution_time("Open Export Directory", start_time)
		return {'FINISHED'}


classes = (
	ACTExport,
	OpenExportDir,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)