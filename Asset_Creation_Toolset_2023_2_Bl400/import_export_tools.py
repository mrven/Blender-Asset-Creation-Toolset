import bpy
import os
import subprocess
import math
from bpy_extras.io_utils import ImportHelper
from . import utils
from datetime import datetime

# FBX and OBJ export
class Multi_FBX_Export(bpy.types.Operator):
	"""Export FBXs to Unity"""
	bl_idname = "object.multi_fbx_export"
	bl_label = "Export FBXs"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		act.export_dir = ""
		incorrect_names = []

		# Check custom name
		if act.fbx_export_mode == 'ALL':
			if act.set_custom_fbx_name:
				if len(act.custom_fbx_name) == 0:
					self.report({'INFO'}, 'Custom Name can\'t be empty')
					return {'CANCELLED'}

		# Check saved blend file
		if len(bpy.data.filepath) == 0 and not act.custom_export_path:
			self.report({'INFO'}, 'Blend file is not saved. Try use Custom Export Path')
			return {'CANCELLED'}

		if len(bpy.data.filepath) > 0 or act.custom_export_path:
			path = ""

			# Check export path
			if len(bpy.data.filepath) > 0:
				if act.export_format == 'FBX':
					path = bpy.path.abspath('//FBXs/')
				if act.export_format == 'OBJ':
					path = bpy.path.abspath('//OBJs/')

			if act.custom_export_path:
				if len(act.export_path) == 0:
					self.report({'INFO'}, 'Export Path can\'t be empty')
					return {'CANCELLED'}

				if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_path))):
					self.report({'INFO'}, 'Directory for export not exist')
					return {'CANCELLED'}
				else:
					path = os.path.realpath(bpy.path.abspath(act.export_path)) + '/'

			# Create export folder (if this need)
			if not os.path.exists(path):
				os.makedirs(path)

			# Save selected objects and active object
			start_selected_obj = bpy.context.selected_objects
			start_active_obj = bpy.context.active_object
			current_selected_obj = bpy.context.selected_objects

			# Check "Pivot Point Align" option, save start state and disable it
			current_pivot_point_align = bpy.context.scene.tool_settings.use_transform_pivot_point_align
			if current_pivot_point_align:
				bpy.context.scene.tool_settings.use_transform_pivot_point_align = False

			# Save cursor location and pivot point mode
			saved_cursor_loc = bpy.context.scene.cursor.location.copy()
			current_pivot_point = bpy.context.scene.tool_settings.transform_pivot_point

			# Name for FBX is active object name (by default)
			name = bpy.context.active_object.name

			# Filtering selected objects. Exclude all not meshes, empties, armatures, curves and text
			bpy.ops.object.select_all(action='DESELECT')
			for x in current_selected_obj:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE' or x.type == 'CURVE' or x.type == 'FONT':
					x.select_set(True)
			current_selected_obj = bpy.context.selected_objects

			# Added suffix _ex to all selected objects. Also add _ex to mesh data and armature name
			for obj in current_selected_obj:
				obj.name += "_ex"
				if obj.type == 'MESH' or obj.type == 'ARMATURE':
					obj.data.name += "_ex"

			# Make copies. These copies will be exported
			bpy.ops.object.duplicate()
			exp_objects = bpy.context.selected_objects

			if act.export_target_engine == 'UNITY2023' and act.export_format == 'FBX':
				if act.export_combine_meshes:
					bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
			else:
				bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

			# Convert all non-mesh objects to mesh (except empties)
			for obj in exp_objects:
				bpy.ops.object.select_all(action='DESELECT')
				obj.select_set(True)
				bpy.context.view_layer.objects.active = obj

				# Remove disabled modifiers
				if obj.type != 'EMPTY':
					for modifier in reversed(obj.modifiers):
						if not (modifier.show_viewport and modifier.show_render):
							obj.modifiers.remove(modifier)

				# Apply modifiers (except Armature)
				if act.export_target_engine == 'UNITY2023' and act.export_format == 'FBX':
					# Pocessing only objects without linked data or for all of enabled option combine meshes
					if ((obj.type == 'MESH' and obj.data.users < 2) or (act.fbx_export_mode != 'INDIVIDUAL' and act.export_combine_meshes)):
						for modifier in obj.modifiers:
							if modifier.type != 'ARMATURE':
								try:
									bpy.ops.object.modifier_apply(modifier=modifier.name)
								except:
									bpy.ops.object.modifier_remove(modifier=modifier.name)
					elif obj.type != 'EMPTY':
						bpy.ops.object.convert(target='MESH')
				else:
					if obj.type == 'MESH':
						for modifier in obj.modifiers:
							if modifier.type != 'ARMATURE':
								try:
									bpy.ops.object.modifier_apply(modifier=modifier.name)
								except:
									bpy.ops.object.modifier_remove(modifier=modifier.name)
					elif obj.type != 'EMPTY':
						bpy.ops.object.convert(target='MESH')
			# Delete _ex.001 suffix from object names.
			# Mesh name and armature name is object name
			for obj in exp_objects:
				obj.name = obj.name[:-7]
				if obj.type == 'MESH' or obj.type == 'ARMATURE':
					obj.data.name = obj.name

			# Delete all materials (Optional)
			if act.delete_mats_before_export:
				for o in exp_objects:
					if o.type == 'MESH' and len(o.data.materials) > 0:
						for q in reversed(range(len(o.data.materials))):
							bpy.context.object.active_material_index = q
							o.data.materials.pop(index=q)

			# Triangulate meshes (Optional)
			if act.triangulate_before_export:
				for o in exp_objects:
					if o.type == 'MESH':
						bpy.ops.object.select_all(action='DESELECT')
						o.select_set(True)
						bpy.context.view_layer.objects.active = o
						bpy.ops.object.mode_set(mode='EDIT')
						bpy.ops.mesh.reveal()
						bpy.ops.mesh.select_all(action='SELECT')
						bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
						bpy.ops.mesh.select_all(action='DESELECT')
						bpy.ops.object.mode_set(mode='OBJECT')

			# Select all exported objects
			for obj in exp_objects:
				obj.select_set(True)

			# Apply Scale and Rotation for UNITY2023 Export
			# Pocessing only objects without linked data
			if act.export_target_engine == 'UNITY2023' and act.export_format == 'FBX':
				current_active = bpy.context.view_layer.objects.active
				bpy.ops.object.select_all(action='DESELECT')
				for x in exp_objects:
					if (x.type == 'MESH' and x.data.users < 2) or x.type != 'MESH':
						bpy.context.view_layer.objects.active = x
						x.select_set(True)
				bpy.ops.object.transform_apply(location=False, rotation=act.apply_rot, scale=act.apply_scale)
				bpy.context.view_layer.objects.active = current_active
			else:
				# Apply scale
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=act.apply_scale)
				# Rotation Fix. Rotate X -90, Apply, Rotate X 90
				if act.apply_rot:
					bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

					# Operate only with higher level parents
					for x in exp_objects:
						bpy.ops.object.select_all(action='DESELECT')

						if x.parent is None:
							x.select_set(True)
							bpy.context.view_layer.objects.active = x

							# Check object has any rotation
							# for option "Apply for Rotated Objects"
							child_rotated = False
							bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
							for y in bpy.context.selected_objects:
								if abs(y.rotation_euler.x) + abs(y.rotation_euler.y) + abs(y.rotation_euler.z) > 0.017:
									child_rotated = True

							bpy.ops.object.select_all(action='DESELECT')
							x.select_set(True)

							# X-rotation fix
							if  act.export_format == 'FBX' and (act.apply_rot_rotated
																or (not act.apply_rot_rotated and not child_rotated)
																or not act.fbx_export_mode == 'PARENT'):
								bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
								bpy.ops.transform.rotate(
									value=(math.pi * -90 / 180), orient_axis='X',
									orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
									orient_type='GLOBAL', constraint_axis=(True, False, False),
									orient_matrix_type='GLOBAL', mirror=False,
									use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
									proportional_size=1)
								bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
								bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
								bpy.ops.object.select_all(action='DESELECT')
								x.select_set(True)
								bpy.ops.transform.rotate(
									value=(math.pi * 90 / 180), orient_axis='X',
									orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
									orient_type='GLOBAL', constraint_axis=(True, False, False),
									orient_matrix_type='GLOBAL', mirror=False,
									use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
									proportional_size=1)

			bpy.ops.object.select_all(action='DESELECT')

			# Select exported objects
			for x in exp_objects:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE':
					x.select_set(True)

			# Store duplicated data for cleanUp
			duplicated_data = []
			for obj in exp_objects:
				if obj.type == 'MESH':
					duplicated_data.append(obj.data.name)

			# Export all as one fbx
			if act.fbx_export_mode == 'ALL':
				# Combine All Meshes (Optional)
				if act.export_combine_meshes:
					# If parent object is mesh
					# combine all children to parent object
					if bpy.data.objects[name].type == 'MESH':
						bpy.context.view_layer.objects.active = bpy.data.objects[name]
						bpy.ops.object.join()
					# If  parent is empty
					else:
						current_active = bpy.context.view_layer.objects.active
						# Combine all child meshes to first in list
						for obj in exp_objects:
							if obj.type == 'MESH':
								bpy.context.view_layer.objects.active = obj
						bpy.ops.object.join()
						bpy.context.view_layer.objects.active = current_active

					exp_objects = bpy.context.selected_objects

				# Set custom fbx/obj name (Optional)
				if act.set_custom_fbx_name:
					prefilter_name = act.custom_fbx_name
				else:
					prefilter_name = name

				# Replace invalid chars
				name = utils.Prefilter_Export_Name(prefilter_name)

				if name != prefilter_name:
					incorrect_names.append(prefilter_name)

				# Export FBX/OBJ
				utils.Export_Model(path, name)

			# Individual Export
			if act.fbx_export_mode == 'INDIVIDUAL':
				for x in exp_objects:
					object_loc = (0.0, 0.0, 0.0)
					bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					bpy.context.view_layer.objects.active = x

					# Apply Location - Center of fbx is origin of object (Optional)
					if act.apply_loc:
						# Copy object location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor.location.copy()
						# Move object to center of world
						bpy.ops.object.location_clear(clear_delta=False)
					# Center of fbx is center of the world
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
					prefilter_name = x.name

					# Replace invalid chars
					name = utils.Prefilter_Export_Name(prefilter_name)

					if name != prefilter_name:
						incorrect_names.append(prefilter_name)

					# Export FBX/OBJ
					utils.Export_Model(path, name)

					# Restore object location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)

			combined_meshes = []

			# Export by parents
			if act.fbx_export_mode == 'PARENT':
				bpy.ops.object.select_all(action='DESELECT')

				# Select only top level parents
				for x in exp_objects:
					if x.parent is None:
						x.select_set(True)

				parent_objs = bpy.context.selected_objects

				for x in parent_objs:
					bpy.ops.object.select_all(action='DESELECT')
					bpy.context.view_layer.objects.active = x
					x.select_set(True)
					# Combine All Meshes (Optional)
					if act.export_combine_meshes:
						# If parent object is mesh
						# combine all children to parent object
						if x.type == 'MESH':
							bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
							bpy.ops.object.join()

							# CleanUp Empties without Children
							selected_objects_for_cleanup = bpy.context.selected_objects
							for obj in selected_objects_for_cleanup:
								if obj.type == "EMPTY" and len(obj.children) == 0:
									bpy.data.objects.remove(obj, do_unlink=True)

						# If  parent is not Mesh
						else:
							current_active = bpy.context.view_layer.objects.active
							parent_loc = current_active.location.copy()
							parent_name = current_active.name

							# Select all children
							bpy.ops.object.select_grouped(extend=False, type='CHILDREN_RECURSIVE')
							group_selected_objects = bpy.context.selected_objects

							# Combine all child meshes to first in list
							for obj in group_selected_objects:
								if obj.type == 'MESH':
									bpy.context.view_layer.objects.active = obj
							bpy.ops.object.join()

							bpy.context.view_layer.objects.active.name = parent_name + '_Mesh'

							# Parent Combined mesh back
							current_active.select_set(True)
							bpy.context.view_layer.objects.active = current_active
							bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

							selected_objects_for_cleanup = bpy.context.selected_objects

							# Move Origin to Parent
							bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
							bpy.context.scene.cursor.location = parent_loc
							bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

							# CleanUp Empties without Children
							for obj in selected_objects_for_cleanup:
								if obj.type == "EMPTY" and len(obj.children) == 0:
									bpy.data.objects.remove(obj, do_unlink=True)

							bpy.context.view_layer.objects.active = current_active

					current_parent = bpy.context.view_layer.objects.active

					object_loc = (0.0, 0.0, 0.0)
					bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')

					current_parent.select_set(True)
					bpy.context.view_layer.objects.active = current_parent

					if act.apply_loc:
						# Copy object location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor.location.copy()
						# Move object to center
						bpy.ops.object.location_clear(clear_delta=False)
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

					# Name is name of parent
					prefilter_name = current_parent.name
					# Select Parent and his children
					bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')

					# Replace invalid chars
					name = utils.Prefilter_Export_Name(prefilter_name)

					if name != prefilter_name:
						incorrect_names.append(prefilter_name)

					# Store objects after combine for future cleanup
					if act.export_combine_meshes:
						for obj in bpy.context.selected_objects:
							combined_meshes.append(obj)

					# Export FBX/OBJ
					utils.Export_Model(path, name)
					bpy.ops.object.select_all(action='DESELECT')
					current_parent.select_set(True)

					# Restore object location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)

			# Export by collection
			if act.fbx_export_mode == 'COLLECTION':
				used_collections = []
				origin_loc = (0.0, 0.0, 0.0)
				bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
				obj_col_dict = {}
				# Collect used collections for selected objects
				for x in exp_objects:
					collection_in_list = False

					for c in used_collections:
						if x.users_collection[0].name == c:
							collection_in_list = True

					if collection_in_list is False:
						used_collections.append(x.users_collection[0].name)

					obj_col_dict[x.name] = x.users_collection[0].name

				# Select objects by collection and export
				for c in used_collections:
					bpy.ops.object.select_all(action='DESELECT')

					# Select Objects in Collection
					set_active_mesh = False
					for obj_name, col_name in obj_col_dict.items():
						if col_name == c:
							bpy.data.objects[obj_name].select_set(True)
							if bpy.data.objects[obj_name].type == 'MESH' and not set_active_mesh:
								bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
								if act.export_combine_meshes:
									bpy.data.objects[obj_name].name = c
								set_active_mesh = True

					if act.export_combine_meshes and set_active_mesh:
						bpy.ops.object.join()

						# Move Origin to Parent
						bpy.context.scene.cursor.location = origin_loc
						bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

						# CleanUp Empties without Children
						selected_objects_for_cleanup = bpy.context.selected_objects
						for obj in selected_objects_for_cleanup:
							if obj.type == "EMPTY" and len(obj.children) == 0:
								bpy.data.objects.remove(obj, do_unlink=True)

					# Replace invalid chars
					name = utils.Prefilter_Export_Name(c)

					if name != c:
						incorrect_names.append(c)

					# Store objects after combine for future cleanup
					if act.export_combine_meshes:
						for obj in bpy.context.selected_objects:
							combined_meshes.append(obj)

					# Export FBX/OBJ
					utils.Export_Model(path, name)

				bpy.ops.object.select_all(action='DESELECT')

			if act.export_combine_meshes and (act.fbx_export_mode == 'PARENT' or act.fbx_export_mode == 'COLLECTION'):
				exp_objects = combined_meshes

			bpy.ops.object.select_all(action='DESELECT')

			for obj in exp_objects:
				obj.select_set(True)

			# Delete duplicates and cleanup
			bpy.ops.object.delete()

			for data_name in duplicated_data:
				try:
					bpy.data.meshes.remove(bpy.data.meshes[data_name])
				except:
					continue

			# Select again original objects and set active object
			bpy.ops.object.select_all(action='DESELECT')

			# Restore names of objects (remove "_ex" from name)
			for j in current_selected_obj:
				j.name = j.name[:-3]
				if j.type == 'MESH' or j.type == 'ARMATURE':
					j.data.name = j.data.name[:-3]

			for i in start_selected_obj:
				i.select_set(True)

			bpy.context.view_layer.objects.active = start_active_obj

			# Restore "Pivot point align" option
			bpy.context.scene.tool_settings.use_transform_pivot_point_align = current_pivot_point_align

			# Restore cursor location and pivot point mode
			bpy.context.scene.cursor.location = saved_cursor_loc
			bpy.context.scene.tool_settings.transform_pivot_point = current_pivot_point

			# Save export dir path for option "Open export dir"
			act.export_dir = path

		# Show message about incorrect names
		if len(incorrect_names) > 0:
			utils.Show_Message_Box("Object(s) has invalid characters in name. Some chars in export name have been replaced", "Invalid Export Names")

		utils.Print_Execution_Time("FBX/OBJ Export", start_time)
		return {'FINISHED'}


# Open Export Directory
class Open_Export_Dir(bpy.types.Operator):
	"""Open Export Directory in OS"""
	bl_idname = "object.open_export_dir"
	bl_label = "Open Export Directory in OS"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act

		if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_path))):
			act.export_dir = ""
			self.report({'INFO'}, 'Directory not exist')

			return {'CANCELLED'}

		# Try open export dir in OS
		if len(act.export_dir) > 0:
			try:
				os.startfile(act.export_dir)
			except:
				subprocess.Popen(['xdg-open', act.export_dir])
		else:
			self.report({'INFO'}, 'Export FBX\'s before')
			return {'FINISHED'}

		utils.Print_Execution_Time("Open Export Directory", start_time)
		return {'FINISHED'}


# Batch Import FBX and OBJ
class Import_FBX_OBJ(bpy.types.Operator, ImportHelper):
	"""Batch Import FBX and OBJ"""
	bl_idname = "object.import_fbxobj"
	bl_label = "Import FBXs/OBJs"
	bl_options = {'REGISTER', 'UNDO'}
	files: bpy.props.CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)
	directory: bpy.props.StringProperty(subtype="DIR_PATH")

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act

		# Import selected files from inspector
		directory = self.directory
		for f in self.files:
			# Get path and extension
			filepath = os.path.join(directory, f.name)
			extension = (os.path.splitext(f.name)[1])[1:]
			# export fbx
			if extension == "fbx" or extension == "FBX":
				if act.import_custom_options:
					bpy.ops.import_scene.fbx(
						filepath=filepath, use_custom_normals=act.import_normals,
						use_anim=act.import_animation,
						automatic_bone_orientation=act.import_automatic_bone_orientation,
						ignore_leaf_bones=act.import_ignore_leaf_bones)
				else:
					bpy.ops.import_scene.fbx(filepath=filepath)

			# Or export OBJ
			if extension == "obj" or extension == "OBJ":
				if act.import_custom_options:
					bpy.ops.import_scene.obj(filepath=filepath, use_smooth_groups=act.import_normals)
				else:
					bpy.ops.import_scene.obj(filepath=filepath)

		utils.Print_Execution_Time("Import FBX/OBJ", start_time)
		return {'FINISHED'}


# Import Export UI Panel
class VIEW3D_PT_Import_Export_Tools_Panel(bpy.types.Panel):
	bl_label = "Import/Export Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		# If this panel not hidden in preferences
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is None or (
					context.object is not None and context.mode == 'OBJECT')) and preferences.export_import_enable

	def draw(self, context):
		act = bpy.context.scene.act
		layout = self.layout

		if context.object is not None:
			if context.mode == 'OBJECT':
				# Export Mode
				row = layout.row(align=True)
				row.label(text="Export Mode:")
				row.prop(act, 'fbx_export_mode', expand=False)

				# Export Format (FBX or OBJ)
				row = layout.row(align=True)
				row.label(text="File Format:")
				row.prop(act, "export_format", expand=False)

				if act.export_format == 'FBX':
					# Target Engine
					row = layout.row(align=True)
					row.label(text="Target Engine:")
					row.prop(act, "export_target_engine", expand=False)

				if not (act.export_format == 'OBJ' and (act.fbx_export_mode == 'ALL' or act.fbx_export_mode == 'COLLECTION')):
					# Apply Transforms
					box = layout.box()
					row = box.row()
					row.label(text="Apply:")

					row = box.row(align=True)
					if act.export_format == 'FBX':
						if act.apply_rot:
							row.prop(act, "apply_rot", text="Rotation", icon="CHECKBOX_HLT")
						else:
							row.prop(act, "apply_rot", text="Rotation", icon="CHECKBOX_DEHLT")
						if act.apply_scale:
							row.prop(act, "apply_scale", text="Scale", icon="CHECKBOX_HLT")
						else:
							row.prop(act, "apply_scale", text="Scale", icon="CHECKBOX_DEHLT")

					if act.fbx_export_mode == 'INDIVIDUAL' or act.fbx_export_mode == 'PARENT':
						if act.apply_loc:
							row.prop(act, "apply_loc", text="Location", icon="CHECKBOX_HLT")
						else:
							row.prop(act, "apply_loc", text="Location", icon="CHECKBOX_DEHLT")

					if act.export_format == 'FBX':
						if act.apply_rot and act.fbx_export_mode == 'PARENT' and act.export_target_engine != 'UNITY2023':
							row = box.row()
							row.prop(act, "apply_rot_rotated")

				row = layout.row()
				row.prop(act, "delete_mats_before_export", text="Delete All Materials")

				if act.fbx_export_mode != 'INDIVIDUAL':
					row = layout.row()
					row.prop(act, "export_combine_meshes", text="Combine All Meshes")

				row = layout.row()
				row.prop(act, "triangulate_before_export", text="Triangulate Meshes")

				if act.fbx_export_mode == 'ALL':
					box = layout.box()
					row = box.row()
					row.prop(act, "set_custom_fbx_name", text="Custom Name for File")
					if act.set_custom_fbx_name:
						row = box.row(align=True)
						row.label(text="File Name:")
						row.prop(act, "custom_fbx_name")

				box = layout.box()
				row = box.row()
				row.prop(act, "export_custom_options", text="Custom Export Options")
				if act.export_custom_options:
					if act.export_format == 'FBX':
						row = box.row(align=True)
						row.label(text=" Smoothing")
						row.prop(act, "export_smoothing", expand=False)

						row = box.row(align=True)
						row.label(text=" Loose Edges")
						row.prop(act, "export_loose_edges", text="")

						row = box.row(align=True)
						row.label(text=" Tangent Space")
						row.prop(act, "export_tangent_space", text="")

						row = box.row(align=True)
						row.label(text=" Add Leaf Bones")
						row.prop(act, "export_add_leaf_bones", text="")

						row = box.row(align=True)
						row.label(text=" VC color space")
						row.prop(act, "export_vc_color_space", expand=False)

					if act.export_format == 'OBJ':
						row = box.row(align=True)
						row.label(text=" Separate By Mats")
						row.prop(act, "obj_separate_by_materials", text="")

						row = box.row(align=True)
						row.label(text=" Smooth Groups")
						row.prop(act, "obj_export_smooth_groups", text="")

				box = layout.box()
				row = box.row()
				row.prop(act, "custom_export_path", text="Custom Export Path")
				if act.custom_export_path:
					row = box.row(align=True)
					row.label(text="Export Path:")
					row.prop(act, "export_path")

				row = layout.row()
				if act.export_format == 'FBX':
					if act.export_target_engine == 'UNITY' or act.export_target_engine == 'UNITY2023':
						row.operator("object.multi_fbx_export", text="Export FBX to Unity")
					else:
						row.operator("object.multi_fbx_export", text="Export FBX to Unreal")
				if act.export_format == 'OBJ':
					row.operator("object.multi_fbx_export", text="Export OBJ")

				if len(act.export_dir) > 0:
					row = layout.row()
					row.operator("object.open_export_dir", text="Open Export Directory")

		if context.mode == 'OBJECT':
			box = layout.box()
			row = box.row()
			row.operator("object.import_fbxobj", text="Import FBXs/OBJs")

			row = box.row()
			row.prop(act, "import_custom_options", text="Custom Import Options")
			if act.import_custom_options:
				row = box.row(align=True)
				row.label(text=" Import Normals")
				row.prop(act, "import_normals", text="")

				row = box.row(align=True)
				row.label(text=" Import Animation")
				row.prop(act, "import_animation", text="")

				row = box.row(align=True)
				row.label(text=" Auto Bone Orientation")
				row.prop(act, "import_automatic_bone_orientation", text="")

				row = box.row(align=True)
				row.label(text=" Ignore Leaf Bones")
				row.prop(act, "import_ignore_leaf_bones", text="")

		else:
			row = layout.row()
			row.label(text=" ")


classes = (
	Multi_FBX_Export,
	Open_Export_Dir,
	Import_FBX_OBJ,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
