bl_info = {
	"name": "Asset Creation Toolset",
	"description": "Toolset for easy create assets for Unity 3D/3D Stocks/etc.",
	"author": "Ivan 'mrven' Vostrikov",
	"version": (2, 4, 1),
	"blender": (2, 80, 0),
	"location": "3D View > Toolbox",
	"category": "Object",
}

import bpy
import os
import bmesh
import math
from bpy_extras.io_utils import ImportHelper

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
		OperatorFileListElement,
        )
		
from bpy.props import (
        BoolProperty,
        PointerProperty,
		StringProperty, 
		CollectionProperty,
		FloatProperty,
		EnumProperty,
		IntProperty,
        )


#-------------------------------------------------------
#FBX-Export
class Multi_FBX_export(Operator):
	"""Export FBXs to Unity"""
	bl_idname = "object.multi_fbx_export"
	bl_label = "Export FBXs to Unity"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		blend_not_saved = False
		
		#check saved blend file
		if len(bpy.data.filepath) == 0:
			self.report({'INFO'}, 'Objects don\'t export, because Blend file is not saved')
			blend_not_saved = True
		if blend_not_saved == False:	
			path = bpy.path.abspath('//FBXs/')
			if act.custom_export_path:
				if not os.path.exists(os.path.realpath(bpy.path.abspath(act.export_path))):
					self.report({'INFO'}, 'Directory for export not exist. Objects will be export to \'FBXs\' folder')
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
			
			#Export All as one fbx
			if act.fbx_export_mode == '1':
		
				if act.set_custom_fbx_name:
					name = act.custom_fbx_name
				
				#Export FBX
				bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), ui_tab='MAIN', use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')

			#Individual Export
			if act.fbx_export_mode == '0':
				for x in current_selected_obj:
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
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), ui_tab='MAIN', use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					
					#Restore Object Location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			#Export By Parents
			if act.fbx_export_mode == '2':
				bpy.ops.object.select_all(action='DESELECT')
				for x in current_selected_obj:
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
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), ui_tab='MAIN', use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					
					#Restore Object Location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			
			#Select again objects and set active object
			bpy.ops.object.select_all(action='DESELECT')
			for j in start_selected_obj:
				j.select_set(True)
	
			bpy.context.view_layer.objects.active = start_active_obj

			#Restore "Pivot Point Align" option
			bpy.context.scene.tool_settings.use_transform_pivot_point_align = current_pivot_point_align

			#Restore Cursor Location and Pivot Point Mode
			bpy.context.scene.cursor.location = saved_cursor_loc
			bpy.context.scene.tool_settings.transform_pivot_point = current_pivot_point
		
		return {'FINISHED'}

#-------------------------------------------------------
#Palette Texture Creator
class PaletteCreate(Operator):
	"""Palette Texture Creator"""
	bl_idname = "object.palette_creator"
	bl_label = "Palette Texture Creator"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#Yet NOT AVAILABLE
		return {'FINISHED'}

#-------------------------------------------------------
#Quick Bake Vertex Colors from Texture
class BakeVC(Operator):
	"""Quick Bake Vertex Colors from Texture"""
	bl_idname = "object.bake_vc"
	bl_label = "Quick Bake Vertex Colors from Texture"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#Yet NOT AVAILABLE					
		return {'FINISHED'}

#-------------------------------------------------------
#Clear Custom Split Normals
class ClearNormals(Operator):
	"""Clear Custom Split Normals"""
	bl_idname = "object.clear_normals"
	bl_label = "Clear Custom Split Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.mesh.customdata_custom_splitnormals_clear()
				bpy.context.object.data.auto_smooth_angle = 3.14159
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj					
		return {'FINISHED'}		
		
#-------------------------------------------------------
#Recalculate Normals
class CalcNormals(Operator):
	"""Recalculate Normals"""
	bl_idname = "object.calc_normals"
	bl_label = "Flip/Calculate Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				if act.calc_normals_en == False:
					bpy.ops.mesh.flip_normals()
				else:
					bpy.ops.mesh.normals_make_consistent(inside=act.normals_inside)
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.ops.object.mode_set(mode='OBJECT')
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj
		return {'FINISHED'}
		
#-------------------------------------------------------
#Batch Import FBX and OBJ
class ImportFBXOBJ(Operator, ImportHelper):
	"""Batch Import FBX and OBJ"""
	bl_idname = "object.import_fbxobj"
	bl_label = "Import FBXs/OBJs"
	bl_options = {'REGISTER', 'UNDO'}
	files: CollectionProperty(name="File Path", type=OperatorFileListElement)
	directory: StringProperty(subtype="DIR_PATH")
	
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
#Rename object(s)
class RenameObject(Operator):
	"""Rename object(s)"""
	bl_idname = "object.rename_object"
	bl_label = "Rename object(s)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		old_str = act.old_text
		new_str = act.new_text
		new_name_glob = act.new_name
		prefix = act.prefix
		postfix = act.postfix
		selected_obj = bpy.context.selected_objects
		
		#New name
		if act.rename_select == '2':
			for x in selected_obj:
				x.name = new_name_glob
		
		#Add Pre/Postfix
		if act.rename_select == '0':
			for x in selected_obj:
				ob_name = x.name
				#Preprocess Delete Blender Numbers
				if act.delete_nums:
					if StrIsInt(ob_name[-3:]):
						dot_pos = len(ob_name) - 4
						if ob_name[dot_pos] == '.':
							ob_name = ob_name[:-4]
				new_name = prefix + ob_name + postfix
				x.name = new_name
				
		#Replace
		if act.rename_select == '1':
			for x in selected_obj:
				if x.name.find(old_str) > -1:
					ob_name = x.name
					new_name = ob_name.replace(old_str, new_str)
					x.name = new_name			
		return {'FINISHED'}

#Rename UV(s)
class RenameUV(Operator):
	"""Rename UV(s)"""
	bl_idname = "object.uv_rename"
	bl_label = "Rename UV(s)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects	
		uv_index = act.uv_layer_index
		uv_name = act.uv_name
		
		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].name = uv_name	
		return {'FINISHED'}

#-------------------------------------------------------		
#Numbering
class Numbering(Operator):
	"""Numbering of Objects"""
	bl_idname = "object.numbering"
	bl_label = "Numbering of Objects"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects	
		objects_list = []
		
		for x in selected_obj:
			#List of Objects
			if act.nums_method == '0' or act.nums_method == '3':
				object_class = [x.name, x.location.x]
			if act.nums_method == '1':
				object_class = [x.name, x.location.y]
			if act.nums_method == '2':
				object_class = [x.name, x.location.z]
			
			objects_list.append(object_class)
			
		#Sort List
		if act.nums_method != '3':
			objects_list.sort(key=lambda object: object[1])
		
		#Preprocess Delete Blender Numbers and add new numbers
		for y in range(len(objects_list)):
			current_obj = bpy.data.objects[objects_list[y][0]]
			
			#Delete Blender Numbers
			ob_name = current_obj.name
			if StrIsInt(ob_name[-3:]):
				dot_pos = len(ob_name) - 4
				if ob_name[dot_pos] == '.':
					ob_name = ob_name[:-4]
						
			#Delete Previous Numbers
			if act.delete_prev_nums:
				if StrIsInt(ob_name[-1:]):
					unds_pos = len(ob_name) - 2
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-2]
						
				if StrIsInt(ob_name[-2:]):
					unds_pos = len(ob_name) - 3
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-3]
						
				if StrIsInt(ob_name[-3:]):
					unds_pos = len(ob_name) - 4
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-4]
						
			#Format for Numbers
			num_str = ''
			
			#_X, _XX, _XXX
			if act.nums_format == '0': 
				num_str = str(y+1)
			
			#_0X, _XX, _XXX
			if act.nums_format == '1':
				if (y <= 8):
					num_str = '0' + str(y+1)
				else:
					num_str = str(y+1)
			
			#_00X, _0XX, _XXX
			if act.nums_format == '2':
				if (y <= 8):
					num_str = '00' + str(y+1)
				elif (y >= 9) and (y <= 98):
					num_str = '0' + str(y+1)
				else:
					num_str = str(y+1)
			bpy.data.objects[objects_list[y][0]].name = ob_name + '_' + num_str;
		return {'FINISHED'}

#-------------------------------------------------------
#UV-Remover
class UVremove(Operator):
	"""Remove UV layer"""
	bl_idname = "object.uv_remove"
	bl_label = "Remove UV layer"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				for a in range(len(x.data.uv_layers)):
					bpy.ops.mesh.uv_texture_remove()			
		
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
			
		bpy.context.view_layer.objects.active = active_obj

		return {'FINISHED'}

#------------------Align Origin To Min-------------------------------
class AlignMin(Operator):
	"""Origin To Min """
	bl_idname = "object.align_min"
	bl_label = "Origin To Min"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			bpy.context.view_layer.objects.active = x
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy() 
			if x.type == 'MESH':
				bpy.ops.object.mode_set(mode = 'EDIT')
				
				if self.TypeAlign == 'X':
					MinCo = FindMinMaxVerts(x, 0, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[0]
				if self.TypeAlign == 'Y':
					MinCo = FindMinMaxVerts(x, 1, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[1]
				if self.TypeAlign == 'Z':
					MinCo = FindMinMaxVerts(x, 2, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[2]
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor.location = [MinCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], MinCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], MinCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor.location = saved_cursor_loc
				
				if act.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MinCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MinCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MinCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
			
		bpy.context.view_layer.objects.active = current_active_obj

		return {'FINISHED'}
	
#------------------Align Origin To Max-------------------------------
class AlignMax(Operator):
	"""Origin To Max """
	bl_idname = "object.align_max"
	bl_label = "Origin To Max"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			bpy.context.view_layer.objects.active = x
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy() 
			if x.type == 'MESH':
				bpy.ops.object.mode_set(mode = 'EDIT')
				
				if self.TypeAlign == 'X':
					MaxCo = FindMinMaxVerts(x, 0, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[0]
				if self.TypeAlign == 'Y':
					MaxCo = FindMinMaxVerts(x, 1, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[1]
				if self.TypeAlign == 'Z':
					MaxCo = FindMinMaxVerts(x, 2, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[2]
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor.location = [MaxCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], MaxCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], MaxCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor.location = saved_cursor_loc
				
				if act.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MaxCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MaxCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MaxCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
			
		bpy.context.view_layer.objects.active = current_active_obj

		return {'FINISHED'}
	
#------------------Align Cursor------------------
class AlignCur(Operator):
	"""Origin Align To Cursor"""
	bl_idname = "object.align_cur"
	bl_label = "Origin To Cursor"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy()
			#Align to 3D Cursor
			if self.TypeAlign == 'X':
				bpy.context.scene.cursor.location = [saved_cursor_loc[0], saved_origin_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Y':
				bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_cursor_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Z':
				bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], saved_cursor_loc[2]] 
			# Apply origin to Cursor position
			if act.align_geom_to_orig == False:
				bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
			else:
				if self.TypeAlign == 'X':
					Difference = saved_cursor_loc[0] - saved_origin_loc[0]
					bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Y':
					Difference = saved_cursor_loc[1] - saved_origin_loc[1]
					bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Z':
					Difference = saved_cursor_loc[2] - saved_origin_loc[2]
					bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			# Reset 3D Cursor position  
			bpy.context.scene.cursor.location = saved_cursor_loc
		
		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
		
		return {'FINISHED'}

#------------------Align Coordinate------------------ 
class AlignCo(Operator):
	"""Origin Align To Spec Coordinate"""
	bl_idname = "object.align_co"
	bl_label = "Origin Align To Spec Coordinate"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: StringProperty()

	def execute(self, context):
		act = context.scene.act

		wrong_align_co = False
		#Check coordinate if check tgis option
		try:
			align_coordinate = float(act.align_co)
		except:
			self.report({'INFO'}, 'Coordinate is wrong')
			wrong_align_co = True   
		
		if wrong_align_co == False:
			# Save selected objects and current position of 3D Cursor
			current_selected_obj = bpy.context.selected_objects
			saved_cursor_loc = bpy.context.scene.cursor.location.copy()
			bpy.ops.object.mode_set(mode = 'OBJECT')
			# Change individual origin point
			for x in current_selected_obj:
				# Select only current object (for setting origin)
				bpy.ops.object.select_all(action='DESELECT')
				x.select_set(True);
				# Save current origin and relocate 3D Cursor
				saved_origin_loc = x.location.copy()
				
				#Align to Coordinate
				if self.TypeAlign == 'X':
					bpy.context.scene.cursor.location = [align_coordinate, saved_origin_loc[1], saved_origin_loc[2]] 
				if self.TypeAlign == 'Y':
					bpy.context.scene.cursor.location = [saved_origin_loc[0], align_coordinate, saved_origin_loc[2]] 
				if self.TypeAlign == 'Z':
					bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], align_coordinate] 
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
				else:
					if self.TypeAlign == 'X':
						Difference = align_coordinate - saved_origin_loc[0]
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						Difference = align_coordinate - saved_origin_loc[1]
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						Difference = align_coordinate - saved_origin_loc[2]
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				# Reset 3D Cursor position  
				bpy.context.scene.cursor.location = saved_cursor_loc
			
			# Select again objects
			for j in current_selected_obj:
				j.select_set(True);
			
		return {'FINISHED'}

#-------------------------------------------------------
#OriginRotate
class OriginRotate(Operator):
	"""Rotate Origin"""
	bl_idname = "object.origin_rotate"
	bl_label = "Rotate Origin"
	bl_options = {'REGISTER', 'UNDO'}
	TypeRot: StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		wrong_angle = False
		#Check value if check this option
		try:
			RotValue = float(act.origin_rotate_value)
		except:
			self.report({'INFO'}, 'Angle is wrong')
			wrong_angle = True   
		
		if act.orientation_select == '0':
			Ori_Constaraint = 'GLOBAL'
		if act.orientation_select == '1':
			Ori_Constaraint = 'LOCAL'
		
		if wrong_angle == False:
			active_obj = bpy.context.active_object
			bpy.ops.object.select_all(action='DESELECT')
			active_obj.select_set(True)
			if active_obj.type == 'MESH':
				bpy.ops.object.duplicate()
				dupli_object = bpy.context.active_object
				if self.TypeRot == 'X+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), orient_axis='X', orient_type=Ori_Constaraint, constraint_axis=(True, False, False), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'X-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), orient_axis='X', orient_type=Ori_Constaraint, constraint_axis=(True, False, False), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Y+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), orient_axis='Y', orient_type=Ori_Constaraint, constraint_axis=(False, True, False), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Y-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), orient_axis='Y', orient_type=Ori_Constaraint, constraint_axis=(False, True, False), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Z+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), orient_axis='Z', orient_type=Ori_Constaraint, constraint_axis=(False, False, True), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Z-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), orient_axis='Z', orient_type=Ori_Constaraint, constraint_axis=(False, False, True), orient_matrix_type=Ori_Constaraint, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)	
				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				bpy.ops.mesh.delete()
				bpy.ops.object.mode_set(mode = 'OBJECT')
				active_obj.select_set(True)
				name = active_obj.name
				geo_name = active_obj.data.name 
				bpy.ops.object.join()
				bpy.context.active_object.name = name
				bpy.context.active_object.data.name = geo_name
		return {'FINISHED'}
		
#-------------------------------------------------------
#FUNCTIONS
#Find Min and Max Vertex Coordinates
def FindMinMaxVerts(obj, CoordIndex, MinOrMax):
	
	bpy.ops.mesh.reveal()
	
	#get bmesh from active object
	bm = bmesh.from_edit_mesh(obj.data)
	bm.verts.ensure_lookup_table()
	
	if len(bm.verts) == 0:
		result = None
	else:
		min_co = (obj.matrix_world @ bm.verts[0].co)[CoordIndex]
		max_co = (obj.matrix_world @ bm.verts[0].co)[CoordIndex]
		
		for v in bm.verts:
			if (obj.matrix_world @ v.co)[CoordIndex] < min_co:
				min_co = (obj.matrix_world @ v.co)[CoordIndex]
			if (obj.matrix_world @ v.co)[CoordIndex] > max_co:
				max_co = (obj.matrix_world @ v.co)[CoordIndex]
		
		if MinOrMax == 0:
			result = min_co
		else:
			result = max_co
		
	return result	

#Check String is a Number
def StrIsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
	
#-------------------------------------------------------
#Set Origin To Selection
class SetOriginToSelect(Operator):
	"""Set Origin To Selection"""
	bl_idname = "object.set_origin_to_select"
	bl_label = "Set Origin To Selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Apply origin to Cursor position
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		# Reset 3D Cursor position  
		bpy.context.scene.cursor.location = saved_cursor_loc
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		return {'FINISHED'} 

#-------------------------------------------------------
#Clear Custom Orientations
class ClearCustomOri(Operator):
	"""Clear Custom Orientations"""
	bl_idname = "object.clear_custom_ori"
	bl_label = "Clear Custom Orientations"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):

		return {'FINISHED'} 			

#-------------------------------------------------------
#Obj Name to Mesh Name
class ObjNameToMeshName(Operator):
	"""Obj Name to Mesh Name"""
	bl_idname = "object.objname_to_meshname"
	bl_label = "Obj Name to Mesh Name"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		current_selected_obj = bpy.context.selected_objects
		
		for x in current_selected_obj:
			if x.type == 'MESH':
				x.data.name = x.name
		return {'FINISHED'} 			

#-------------------------------------------------------
#Clear Vertex Colors
class ClearVertexColors(Operator):
	"""# Clear Vertex Colors"""
	bl_idname = "object.clear_vc"
	bl_label = "# Clear Vertex Colors"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		
		for x in current_selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				for y in x.data.vertex_colors:
					bpy.ops.mesh.vertex_color_remove()
				bpy.ops.mesh.vertex_color_remove()
				
		for x in current_selected_obj:
			x.select_set(True)
		bpy.context.view_layer.objects.active = current_active_obj

		return {'FINISHED'} 			

#-------------------------------------------------------
#UV Mover
class UV_Mover(Operator):
	"""UV Mover"""
	bl_idname = "uv.uv_mover"
	bl_label = "Move and Scale UV islands"
	bl_options = {'REGISTER', 'UNDO'}
	Value: StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		Start_Pivot_Mode = bpy.context.space_data.pivot_point
		bpy.context.space_data.pivot_point = 'CURSOR'
		move_step = 1/2**int(act.uv_move_factor)
		if self.Value == "TL":
			bpy.ops.uv.cursor_set(location=(0, 1))
		if self.Value == "TR":
			bpy.ops.uv.cursor_set(location=(1, 1))
		if self.Value == "BL":
			bpy.ops.uv.cursor_set(location=(0, 0))
		if self.Value == "BR":
			bpy.ops.uv.cursor_set(location=(1, 0))
			
		if self.Value == "MINUS":
			bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "PLUS":
			bpy.ops.transform.resize(value=(2, 2, 2), constraint_axis=(False, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "RIGHT":
			bpy.ops.transform.translate(value=(move_step, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "LEFT":
			bpy.ops.transform.translate(value=(-1 * move_step, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "UP":
			bpy.ops.transform.translate(value=(0, move_step, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "DOWN":
			bpy.ops.transform.translate(value=(0, -1 * move_step, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)	
		
		bpy.context.space_data.pivot_point = Start_Pivot_Mode

		return {'FINISHED'}
		
#-------------------------------------------------------
#Panels
class VIEW3D_PT_Origin_Tools_panel(Panel):
	bl_label = "Origin Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.label(text="Origin Rotation")
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.label(text="Orientation:")
				split = split.split()
				c = split.column()
				c.prop(act, 'orientation_select', expand=False)
				#----
				row = layout.row()
				row.prop(act, "origin_rotate_value", text="Angle")
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.origin_rotate", text="X-").TypeRot = 'X-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="X+").TypeRot = 'X+'
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.origin_rotate", text="Y-").TypeRot = 'Y-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="Y+").TypeRot = 'Y+'
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.origin_rotate", text="Z-").TypeRot = 'Z-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="Z+").TypeRot = 'Z+'
				layout.separator()
				
				row = layout.row()
				row.label(text="Origin Align")
				row = layout.row()
				row.prop(act, "align_co", text="Coordinate")
				row = layout.row()
				row.prop(act, "align_geom_to_orig", text="Geometry To Origin")
				
				#--Aligner Labels----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.label(text="X")
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.label(text="Y")
				split = split.split()
				c = split.column()
				c.label(text="Z")
				
				#--Aligner Min Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Z'
				
				#--Aligner Max Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Z'
				
				#--Aligner Cursor Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Z'
				
				#--Aligner Coordinates Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='Z'
				
		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
				row.operator("object.set_origin_to_select", text="Set Origin To Selected")
				layout.separator()

		else:
			row = layout.row()
			row.label(text=" ")

class VIEW3D_PT_Rename_Tools_panel(Panel):
	bl_label = "Rename Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				layout.label(text="Rename UV")
				row = layout.row()
				row.prop(act, "uv_layer_index", text="UV Index")
				
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.4, align=True)
				c = split.column()
				c.label(text="UV Name:")
				split = split.split()
				c = split.column()
				c.prop(act, "uv_name")
				#----

				row = layout.row()
				row.operator("object.uv_rename", text="Rename UV(s)")
				layout.separator()
				
				layout.label(text="Rename Objects")
				row = layout.row()
				row.prop(act, 'rename_select', expand=False)
				row = layout.row()
				if act.rename_select == '0':	
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.3, align=True)
					c = split.column()
					c.label(text="Prefix:")
					split = split.split()
					c = split.column()
					c.prop(act, "prefix")
					#----
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.3, align=True)
					c = split.column()
					c.label(text="Postfix:")
					split = split.split()
					c = split.column()
					c.prop(act, "postfix")
					#----	

				if act.rename_select == '1':
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.4, align=True)
					c = split.column()
					c.label(text="Old Text:")
					split = split.split()
					c = split.column()
					c.prop(act, "old_text")
					#----
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.4, align=True)
					c = split.column()
					c.label(text="New Text:")
					split = split.split()
					c = split.column()
					c.prop(act, "new_text")
					#----	

				if act.rename_select == '2':
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.5, align=True)
					c = split.column()
					c.label(text="New Name:")
					split = split.split()
					c = split.column()
					c.prop(act, "new_name")
					#----

				if act.rename_select == '0':
					layout.prop(act, "delete_nums", text="Delete Blender Nums")
					row = layout.row()

				row = layout.row()
				row.operator("object.rename_object", text="Rename Object(s)")
				
				layout.separator()
				layout.label(text="Numbering Objects")
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Method:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_method', expand=False)
				#----
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Format:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_format', expand=False)
				#----
				
				row = layout.row()
				row.prop(act, "delete_prev_nums", text="Delete Previous Nums")
				row = layout.row()
				row.operator("object.numbering", text="Set Numbering")
			else:
				row = layout.row()
				row.label(text=" ")

		else:
			row = layout.row()
			row.label(text=" ")
				
class VIEW3D_PT_ImportExport_Tools_panel(Panel):
	bl_label = "Import/Export Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				layout.label(text="Export Mode:")
				row = layout.row()
				row.prop(act, 'fbx_export_mode', expand=False)
				row = layout.row()
				layout.label(text="Apply:")
				
				layout.label(text="--Rotation & Scale yet not work--")
				#layout.prop(act, "apply_rot", text="Rotation")
				#layout.prop(act, "apply_scale", text="Scale")
				
				if act.fbx_export_mode == '0' or act.fbx_export_mode == '2':
					layout.prop(act, "apply_loc", text="Location")
				row = layout.row()
				if act.fbx_export_mode == '1':
					layout.prop(act, "set_custom_fbx_name", text="Custom Name for FBX")
					if act.set_custom_fbx_name:
						#Split row
						row = layout.row()
						c = row.column()
						row = c.row()
						split = row.split(factor=0.5, align=True)
						c = split.column()
						c.label(text="FBX Name:")
						split = split.split()
						c = split.column()
						c.prop(act, "custom_fbx_name")
						#----

				row = layout.row()
				layout.prop(act, "custom_export_path", text="Custom Export Path")
				if act.custom_export_path:
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.5, align=True)
					c = split.column()
					c.label(text="Export Path:")
					split = split.split()
					c = split.column()
					c.prop(act, "export_path")
					#----

				row = layout.row()
				row.operator("object.multi_fbx_export", text="Export FBX to Unity")
				row = layout.row()
			
		
		if context.mode == 'OBJECT':
			row = layout.row()
			row.operator("object.import_fbxobj", text="Import FBXs/OBJs")

		else:
			row = layout.row()
			row.label(text=" ")
				
class VIEW3D_PT_LowPolyArt_Tools_panel(Panel):
	bl_label = "Low Poly Art Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.enabled = False
				row.operator("object.palette_creator", text="Create Palette Texture")
				layout.separator()
			
			if context.mode == 'OBJECT':
				row = layout.row()
				row.enabled = False
				row.operator("object.bake_vc", text="Texture to Vertex Colors")
				layout.separator()
			
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.uv_remove", text="Clear UV Maps")
				row = layout.row()
				row.operator("object.clear_vc", text="Clear Vertex Colors")
				layout.separator()
			
			else:
				row = layout.row()
				row.label(text=" ")
		else:
			row = layout.row()
			row.label(text=" ")
		
class VIEW3D_PT_Other_Tools_panel(Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		row = layout.row()
		row.enabled = False
		row.operator("object.clear_custom_ori", text="Clear Custom Orientations")
		row = layout.row()		
		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
		
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()	
				row.operator("object.objname_to_meshname", text="Obj Name -> Mesh Name")
				layout.separator()
				row = layout.row()
				row.operator("object.clear_normals", text="Clear Custom Normals")
				row = layout.row()
				row.operator("object.calc_normals", text="Flip/Calculate Normals")
				layout.prop(act, "calc_normals_en", text="Recalc Normals")
				if act.calc_normals_en:
					layout.prop(act, "normals_inside", text="Inside")
				layout.separator()

		else:
			row = layout.row()
			row.label(text=" ")

class VIEW3D_PT_Uv_Mover_panel(Panel):
	bl_label = "UV Mover"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object.mode == 'EDIT' and context.area.ui_type == 'UV':
			layout.label(text="Set Cursor To Corner:")
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Top Left").Value="TL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Top Right").Value="TR"
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Left").Value="BL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Right").Value="BR"
			
			layout.separator()
			row = layout.row()
			
			#--Aligner Buttons----
			layout.label(text="Scale and Move:")
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.33, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Scale-").Value="MINUS"
			split = split.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="UP").Value="UP"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Scale+").Value="PLUS"
				
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.33, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="LEFT").Value="LEFT"
			split = split.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="DOWN").Value="DOWN"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="RIGHT").Value="RIGHT"
			
			layout.separator()
			
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.label(text="Move Step   1/")
			split = split.split()
			c = split.column()
			c.prop(act, 'uv_move_factor', expand=False)

		else:
			row = layout.row()
			row.label(text=" ")
		

class ACTAddonProps(PropertyGroup):
	old_text: StringProperty(
		name="",
		description="Text for search",
		default="")
	
	new_text: StringProperty(
		name="",
		description="Text for replace",
		default="")
		
	prefix: StringProperty(
		name="",
		description="Prefix Text",
		default="")
		
	postfix: StringProperty(
		name="",
		description="Postfix Text",
		default="")
	
	new_name: StringProperty(
		name="",
		description="New Name for Objects",
		default="")
	
	delete_nums: BoolProperty(
		name="Delete Blender Nums",
		description="Delete Blender Numbers from Object Names",
		default = True)
	
	delete_prev_nums: BoolProperty(
		name="Delete Previous Nums",
		description="Delete Previous Numbers from Object Names",
		default = True)
	
	align_co: FloatProperty(
		name="",
		description="Coordinate",
		default=0.00,
		min = -9999,
        max = 9999,
		step = 50)
	
	nums_method_items = (('0','Along X',''),('1','Along Y',''), ('2','Along Z',''), ('3','Simple',''))
	nums_method: EnumProperty(name="", items = nums_method_items)
	
	nums_format_items = (('0','_X, _XX, _XXX',''),('1','_0X, _XX, _XXX',''), ('2','_00X, _0XX, _XXX',''))
	nums_format: EnumProperty(name="", items = nums_format_items)
	
	axis_items = (('0','X',''),('1','Y',''), ('2','Z',''))
	axis_select: EnumProperty(name="Axis", items = axis_items)
	
	rename_menu_items = (('0','Add Pre/Postfix',''),('1','Replace',''), ('2','New name',''))
	rename_select: EnumProperty(name="", items = rename_menu_items)
	
	orientation_menu_items = (('0','GLOBAL',''),('1','LOCAL',''))
	orientation_select: EnumProperty(name="", items = orientation_menu_items)

	fbx_export_mode_menu_items = (('0','1 Obj->1 FBX',''),('1','All->One FBX',''),('2','By Parent',''))
	fbx_export_mode: EnumProperty(name="", items = fbx_export_mode_menu_items)
	
	uv_move_factor_items = (('1','2',''),('2','4',''), ('3','8',''), ('4','16',''), ('5','32',''))
	uv_move_factor: EnumProperty(name="", items = uv_move_factor_items, default = '3')
	
	apply_rot: BoolProperty(
		name="Apply Rotation",
		description="Apply Rotation for Exported Models",
		default = True)
		
	apply_scale: BoolProperty(
		name="Apply Scale",
		description="Apply Scale for Exported Models",
		default = True)
		
	apply_loc: BoolProperty(
		name="Apply Location",
		description="Apply Location for Exported Models",
		default = True)
		
	set_custom_fbx_name: BoolProperty(
		name="Set Custom Name for FBX",
		description="Set Custom Name for FBX",
		default = False)
		
	custom_fbx_name: StringProperty(
		name="",
		description="Custom Name for FBX",
		default="")
	
	custom_export_path: BoolProperty(
		name="Custom Export Path",
		description="Custom Export Path",
		default = False)
	
	normals_inside: BoolProperty(
		name="Inside Normals",
		description="Recalculate Normals Inside",
		default = False)
	
	calc_normals_en: BoolProperty(
		name="Recalc Normals",
		description="Recalculate Normals",
		default = False)

	align_geom_to_orig: BoolProperty(
		name="Geometry To Origin",
		description="Align Geometry To Origin",
		default = False)
	
	origin_rotate_value: FloatProperty(
		name="",
		description="Angle for Origin Rotate ",
		default=5.00,
		min = -1000,
        max = 1000,
		step = 50)
	
	uv_layer_index: IntProperty(
        name = "UV Index", 
        description = "UV Index",
		default = 0,
		min = 0,
        max = 10)
	
	uv_name: StringProperty(
		name="",
		description="UV Name",
		default="")
		
	export_path: StringProperty(
      name = "",
      default = "",
      description = "Path for Export FBX",
      subtype = 'DIR_PATH'
      )

classes = (
    ACTAddonProps,
	VIEW3D_PT_Origin_Tools_panel,
	VIEW3D_PT_Rename_Tools_panel,
	VIEW3D_PT_ImportExport_Tools_panel,
	VIEW3D_PT_LowPolyArt_Tools_panel,
	VIEW3D_PT_Other_Tools_panel,
	VIEW3D_PT_Uv_Mover_panel,
	Multi_FBX_export,
	PaletteCreate,
	BakeVC,
	ClearNormals,
	CalcNormals,
	ImportFBXOBJ,
	RenameObject,
	RenameUV,
	Numbering,
	UVremove,
	AlignMin,
	AlignMax,
	AlignCur,
	AlignCo,
	OriginRotate,
	SetOriginToSelect,
	ClearCustomOri,
	ObjNameToMeshName,
	ClearVertexColors,
	UV_Mover,
)	  
	
#-------------------------------------------------------		
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
		
	bpy.types.Scene.act = PointerProperty(type=ACTAddonProps)
	
def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		
	del bpy.types.Scene.act

if __name__ == "__main__":
	register()
