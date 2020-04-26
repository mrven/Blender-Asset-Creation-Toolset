import bpy
import os
import subprocess
import math
from bpy_extras.io_utils import ImportHelper

#-------------------------------------------------------
#FBX-Export
class Multi_FBX_Export(bpy.types.Operator):
	"""Export FBXs to Unity"""
	bl_idname = "object.multi_fbx_export"
	bl_label = "Export FBXs"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		act.export_dir = ""

		#FBX Export Scale Mode depends selected Target Engine
		fbx_scale_mode = 'FBX_SCALE_ALL'
		if act.export_target_engine == 'UNREAL':
			fbx_scale_mode = 'FBX_SCALE_NONE'

		if act.fbx_export_mode == 'ALL':
			if act.set_custom_fbx_name:
				if len(act.custom_fbx_name) == 0:
					self.report({'INFO'}, 'Custom Name can\'t be empty')
					return {'CANCELLED'}

		#check saved blend file
		if len(bpy.data.filepath) == 0 and not act.custom_export_path:
			self.report({'INFO'}, 'Blend file is not saved. Try use Custom Export Path')
			return {'CANCELLED'}

		if len(bpy.data.filepath) > 0 or act.custom_export_path:	

			if len(bpy.data.filepath) > 0:
				path = bpy.path.abspath('//FBXs/')
			
			if act.custom_export_path:
				if len(act.export_path) == 0:
					self.report({'INFO'}, 'Export Path can\'t be empty')
					return {'CANCELLED'}

				if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_path))):
					self.report({'INFO'}, 'Directory for export not exist')
					return {'CANCELLED'}
				else:
					path = os.path.realpath(bpy.path.abspath(act.export_path)) + '/'
		
			#Create export folder
			if not os.path.exists(path):
				os.makedirs(path)
			
			# Save selected objects and active object
			start_selected_obj = bpy.context.selected_objects
			start_active_obj = bpy.context.active_object
			current_selected_obj = bpy.context.selected_objects

			#Check "Pivot Point Align" option and disable it
			current_pivot_point_align = bpy.context.scene.tool_settings.use_transform_pivot_point_align
			if current_pivot_point_align:
				bpy.context.scene.tool_settings.use_transform_pivot_point_align = False
			
			#Save Cursor Location and Pivot Point Mode
			saved_cursor_loc = bpy.context.scene.cursor.location.copy()
			current_pivot_point = bpy.context.scene.tool_settings.transform_pivot_point

			#Name for FBX
			name = bpy.context.active_object.name

			#Filtering Selected Objects. Exclude All not meshes, empties and armatures
			bpy.ops.object.select_all(action='DESELECT')
			for x in current_selected_obj:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE':
					x.select_set(True)
			current_selected_obj = bpy.context.selected_objects

			for obj in current_selected_obj:
				obj.name += "_ex"
				obj.data.name += "_ex"

			bpy.ops.object.duplicate()
			exp_objects = bpy.context.selected_objects

			bpy.ops.object.convert(target='MESH')
			bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

			for obj in exp_objects:
				obj.name = obj.name[:-7]
				obj.data.name = obj.name
			
			if act.delete_mats_before_export:
				for o in exp_objects:
					if o.type == 'MESH' and len(o.data.materials) > 0:
						for q in reversed(range(len(o.data.materials))):
							bpy.context.object.active_material_index = q
							o.data.materials.pop(index = q)	

			#Apply Scale
			if act.apply_scale:
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
			
			#Rotation Fix. Rotate X -90, Apply, Rotate X 90
			if act.apply_rot:
				bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
				#Operate only with higher level parents 
				for x in exp_objects:
					bpy.ops.object.select_all(action='DESELECT')
					if x.parent == None:
						x.select_set(True)
						bpy.context.view_layer.objects.active = x

						child_rotated = False
						bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
						for y in bpy.context.selected_objects:
							if abs(y.rotation_euler.x) + abs(y.rotation_euler.y) + abs(y.rotation_euler.z) > 0.017:
								child_rotated = True

						bpy.ops.object.select_all(action='DESELECT')
						x.select_set(True)

						# X-rotation fix
						if act.apply_rot_rotated or (not act.apply_rot_rotated and not child_rotated) or not act.fbx_export_mode == 'PARENT':
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							bpy.ops.transform.rotate(value= (math.pi * -90 / 180), orient_axis='X', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_type='GLOBAL', constraint_axis=(True, False, False), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)						
							bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							
							bpy.ops.object.select_all(action='DESELECT')
							x.select_set(True)
							bpy.ops.transform.rotate(value= (math.pi * 90 / 180), orient_axis='X', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_type='GLOBAL', constraint_axis=(True, False, False), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.object.select_all(action='DESELECT')

			for x in exp_objects:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE':
					x.select_set(True)

			#Export All as one fbx
			if act.fbx_export_mode == 'ALL':
				if act.set_custom_fbx_name:
					name = act.custom_fbx_name
				
				#Export FBX
				if act.export_custom_options:
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = fbx_scale_mode, 
							use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing, 
								use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
				else:
					if act.export_target_engine == 'UNITY':
						bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					else:
						bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True)

			#Individual Export
			if act.fbx_export_mode == 'INDIVIDUAL':
				for x in exp_objects:
					bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					bpy.context.view_layer.objects.active = x

					if act.apply_loc:
						#Copy Object Location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor.location.copy()
						#Move Object to Center
						bpy.ops.object.location_clear(clear_delta=False)
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
					name = x.name

					#Export FBX
					if act.export_custom_options:
						bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = fbx_scale_mode, 
							use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing, 
								use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
					else:
						if act.export_target_engine == 'UNITY':
							bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
						else:
							bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True)
					
					#Restore Object Location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			#Export By Parents
			if act.fbx_export_mode == 'PARENT':
				bpy.ops.object.select_all(action='DESELECT')
				for x in exp_objects:
					if x.parent == None:
						x.select_set(True)
				parent_obj = bpy.context.selected_objects
				bpy.ops.object.select_all(action='DESELECT')
				for x in parent_obj:
					bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					bpy.context.view_layer.objects.active = x

					if act.apply_loc:
						#Copy Object Location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor.location.copy()
						#Move Object to Center
						bpy.ops.object.location_clear(clear_delta=False)
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
					name = x.name
					bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
					
					#Export FBX
					if act.export_custom_options:
						bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = fbx_scale_mode, 
							use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing, 
								use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
					else:
						if act.export_target_engine == 'UNITY':
							bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
						else:
							bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True)
					
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					
					#Restore Object Location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			#Export by Collection
			if act.fbx_export_mode == 'COLLECTION':

				#Collect used collections
				used_collections = []

				for x in current_selected_obj:  
					collection_in_list = False
				    
					for c in used_collections:
						if x.users_collection[0].name == c:
							collection_in_list = True
				            
					if collection_in_list == False:
						used_collections.append(x.users_collection[0].name) 

				for c in used_collections:
					bpy.ops.object.select_all(action='DESELECT')
					for x in current_selected_obj:
						if x.users_collection[0].name == c:
							x.select_set(True)
				            
					#Export FBX
					if act.export_custom_options:
						bpy.ops.export_scene.fbx(filepath=str(path + c + '.fbx'), use_selection=True, apply_scale_options = fbx_scale_mode, 
							use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing, 
								use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
					else:
						if act.export_target_engine == 'UNITY':
							bpy.ops.export_scene.fbx(filepath=str(path + c + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
						else:
							bpy.ops.export_scene.fbx(filepath=str(path + c + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True)
					
				bpy.ops.object.select_all(action='DESELECT')


			bpy.ops.object.select_all(action='DESELECT')
			for obj in exp_objects:
				obj.select_set(True)

			bpy.ops.object.delete()			

			#Select again objects and set active object
			bpy.ops.object.select_all(action='DESELECT')
			
			for j in start_selected_obj:
				j.name = j.name[:-3]
				j.data.name = j.data.name[:-3]
				j.select_set(True)
	
			bpy.context.view_layer.objects.active = start_active_obj

			#Restore "Pivot Point Align" option
			bpy.context.scene.tool_settings.use_transform_pivot_point_align = current_pivot_point_align

			#Restore Cursor Location and Pivot Point Mode
			bpy.context.scene.cursor.location = saved_cursor_loc
			bpy.context.scene.tool_settings.transform_pivot_point = current_pivot_point

			#save export dir
			act.export_dir = path
		
		return {'FINISHED'}


#-------------------------------------------------------
#Open Export Directory
class Open_Export_Dir(bpy.types.Operator):
	"""Open Export Directory in OS"""
	bl_idname = "object.open_export_dir"
	bl_label = "Open Export Directory in OS"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act

		if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_path))):
			act.export_dir = "";
			self.report({'INFO'}, 'Directory not exist')

			return {'CANCELLED'}

		if len(act.export_dir) > 0:
			try:
				os.startfile(act.export_dir)
			except:
				subprocess.Popen(['xdg-open', act.export_dir])
		else:
			self.report({'INFO'}, 'Export FBX\'s before')
			return {'FINISHED'}

		return {'FINISHED'}


#-------------------------------------------------------
#Batch Import FBX and OBJ
class Import_FBX_OBJ(bpy.types.Operator, ImportHelper):
	"""Batch Import FBX and OBJ"""
	bl_idname = "object.import_fbxobj"
	bl_label = "Import FBXs/OBJs"
	bl_options = {'REGISTER', 'UNDO'}
	files: bpy.props.CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)
	directory: bpy.props.StringProperty(subtype="DIR_PATH")
	
	def execute(self, context):
		directory = self.directory
		for f in self.files:
			filepath = os.path.join(directory, f.name)
			extension = (os.path.splitext(f.name)[1])[1:]
			if extension == "fbx" or extension == "FBX":
				bpy.ops.import_scene.fbx(filepath = filepath)
			if extension == "obj" or extension == "OBJ":
				bpy.ops.import_scene.obj(filepath = filepath)	
		return {'FINISHED'}


#-------------------------------------------------------
#Import Export UI Panel
class VIEW3D_Import_Export_Tools_Panel(bpy.types.Panel):
	bl_label = "Import/Export Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is None or (context.object is not None and context.object.mode == 'OBJECT')) and preferences['export_import_enable']

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				#Export Mode
				row = layout.row(align=True)
				row.label(text="Export Mode:")
				row.prop(act, 'fbx_export_mode', expand=False)
				
				#Target Engine
				row = layout.row(align=True)
				row.label(text="Target Engine:")
				row.prop(act, "export_target_engine", expand=False)
				
				#Apply Transforms
				box = layout.box()
				row = box.row()
				row.label(text="Apply:")
				
				row = box.row(align=True)
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

				if act.apply_rot and act.fbx_export_mode == 'PARENT':
					row = box.row()
					row.prop(act, "apply_rot_rotated")
						
				row = layout.row()
				row.prop(act, "delete_mats_before_export", text="Delete All Materials")
				if act.fbx_export_mode == 'ALL':
					row = layout.row()
					row.prop(act, "set_custom_fbx_name", text="Custom Name for FBX")
					if act.set_custom_fbx_name:
						row = layout.row(align=True)
						row.label(text="FBX Name:")
						row.prop(act, "custom_fbx_name")

				box = layout.box()
				row = box.row()
				row.prop(act, "export_custom_options", text="Custom Export Options")
				if act.export_custom_options:
					row = box.row(align=True)
					row.label(text=" Smoothing:")
					row.prop(act, "export_smoothing", expand=False)
					
					row = box.row(align=True)
					row.label(text=" Loose Edges")
					row.prop(act, "export_loose_edges",text="")
					
					row = box.row(align=True)
					row.label(text=" Tangent Space")
					row.prop(act, "export_tangent_space", text="")

				box = layout.box()
				row = box.row()
				row.prop(act, "custom_export_path", text="Custom Export Path")
				if act.custom_export_path:
					row = box.row(align=True)
					row.label(text="Export Path:")
					row.prop(act, "export_path")

				row = layout.row()
				if act.export_target_engine == 'UNITY':
					row.operator("object.multi_fbx_export", text="Export FBX to Unity")
				else:
					row.operator("object.multi_fbx_export", text="Export FBX to Unreal")

				if len(act.export_dir) > 0:
					row.operator("object.open_export_dir", text="Open Export Directory")
				
				row = layout.row()
				row.operator("object.import_fbxobj", text="Import FBXs/OBJs")

		else:
			row = layout.row()
			row.label(text=" ")


classes = (
	Multi_FBX_Export,
	Open_Export_Dir,
	Import_FBX_OBJ,
	VIEW3D_Import_Export_Tools_Panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


