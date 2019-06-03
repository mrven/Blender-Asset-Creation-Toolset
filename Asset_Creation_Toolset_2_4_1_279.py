bl_info = {
	"name": "Asset Creation Toolset",
	"description": "Toolset for easy create assets for Unity 3D/3D Stocks/etc.",
	"author": "Ivan 'mrven' Vostrikov",
	"version": (2, 4, 1),
	"blender": (2, 7, 9),
	"location": "3D View > Object Mode > Toolshelf > Asset Creation Toolset",
	"warning": "For use tool 'Texture to Vertex Colors' requires enabled 'Bake UV-Texture to Vertex Colors' Add-on",
	"category": "Object",
}

import bpy
import os
import bmesh
import math
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement


#-------------------------------------------------------
#FBX-Export
class Multi_FBX_export(bpy.types.Operator):
	"""Export FBXs to Unity"""
	bl_idname = "object.multi_fbx_export"
	bl_label = "Export FBXs to Unity"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		blend_not_saved = False
		#check saved blend file
		if len(bpy.data.filepath) == 0:
			self.report({'INFO'}, 'Objects don\'t export, because Blend file is not saved')
			blend_not_saved = True
		if blend_not_saved == False:
			
			path = bpy.path.abspath('//FBXs/')
			if context.scene.custom_export_path:
				if not os.path.exists(context.scene.export_path):
					self.report({'INFO'}, 'Directory for export not exist. Objects will be export to \'FBXs\' folder')
				else:
					path = context.scene.export_path
			
			#Create export folder
			if not os.path.exists(path):
				os.makedirs(path)
			
			# Save selected objects and active object
			start_selected_obj = bpy.context.selected_objects
			start_active_obj = bpy.context.active_object
			current_selected_obj = bpy.context.selected_objects
			#Save unit system settings
			current_unit_system = bpy.context.scene.unit_settings.system
			current_scale_length = bpy.context.scene.unit_settings.scale_length
			#Set own unit system
			bpy.context.scene.unit_settings.system = 'METRIC'
			bpy.context.scene.unit_settings.scale_length = 1
			#Check "Pivot Point Align" option and disable it
			current_pivot_point_align = bpy.context.space_data.use_pivot_point_align
			if current_pivot_point_align:
				bpy.context.space_data.use_pivot_point_align = False
			#Save Cursor Location and Pivot Point Mode
			saved_cursor_loc = bpy.context.scene.cursor_location.copy()
			current_pivot_point = bpy.context.space_data.pivot_point
			
			#Name for FBX
			name = bpy.context.active_object.name
			
			#Filtering Selected Objects. Exclude All not meshes, empties and armatures
			bpy.ops.object.select_all(action='DESELECT')
			for x in current_selected_obj:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE':
					x.select = True
			current_selected_obj = bpy.context.selected_objects
			
			#Rotation Fix. Rotate X -90, Apply, Rotate X 90. Operate only with higher level parents
			if context.scene.apply_rot:
				bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
				#Operate only with higher level parents 
				for x in current_selected_obj:
					bpy.ops.object.select_all(action='DESELECT')
					if x.parent == None:
						x.select = True
						bpy.context.scene.objects.active = x
						# X-rotation fix
						bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
						bpy.ops.transform.rotate(value = -1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
						bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
						bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
						bpy.ops.object.select_all(action='DESELECT')
						x.select = True
						bpy.ops.transform.rotate(value = 1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
						
			#Export All as one fbx
			if bpy.context.scene.fbx_export_mode == '1':
				#Scale Fix. Scale 100, Apply, Scale 0.01. Operate with all objects
				#Move Cursor to Center and Set Transform around Cursor
				if context.scene.set_custom_fbx_name:
					name = context.scene.custom_fbx_name
				
				if context.scene.apply_scale:
					bpy.context.scene.unit_settings.scale_length = 0.01
					bpy.ops.view3d.snap_cursor_to_center()
					bpy.context.space_data.pivot_point = 'CURSOR'
					#Select All Objects
					bpy.ops.object.select_all(action='DESELECT')
					for x in current_selected_obj:
						x.select = True
					bpy.ops.transform.resize(value=(100, 100, 100))
					bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
				#Export FBX
				bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), version='BIN7400', ui_tab='MAIN', use_selection=True, global_scale=1, apply_unit_scale=True)
				#Scale down to normal size
				if context.scene.apply_scale:
					bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
			
			#Individual Export
			if bpy.context.scene.fbx_export_mode == '0':
				for x in current_selected_obj:
					bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')
					x.select = True
					bpy.context.scene.objects.active = x

					if context.scene.apply_loc:
						#Copy Object Location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor_location.copy()
						#Move Object to Center
						bpy.ops.object.location_clear(clear_delta=False)
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.space_data.pivot_point = 'CURSOR'
					name = x.name
					#Scale Fix
					if context.scene.apply_scale:
						bpy.context.scene.unit_settings.scale_length = 0.01
						bpy.ops.transform.resize(value=(100, 100, 100))
						bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
					#Export FBX
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), version='BIN7400', ui_tab='MAIN', use_selection=True, global_scale=1, apply_unit_scale=True)
					#Scale down to normal size
					if context.scene.apply_scale:
						if context.scene.apply_loc:
							bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
						else:
							bpy.ops.view3d.snap_cursor_to_center()
							bpy.context.space_data.pivot_point = 'CURSOR'
						bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
						bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
					
					#Restore Object Location
					if context.scene.apply_loc:
						bpy.context.scene.cursor_location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			#Export By Parents
			if bpy.context.scene.fbx_export_mode == '2':
				bpy.ops.object.select_all(action='DESELECT')
				for x in current_selected_obj:
					if x.parent == None:
						x.select = True
				parent_obj = bpy.context.selected_objects
				bpy.ops.object.select_all(action='DESELECT')
				for x in parent_obj:
					bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
					# Select only current object
					bpy.ops.object.select_all(action='DESELECT')
					x.select = True
					bpy.context.scene.objects.active = x

					if context.scene.apply_loc:
						#Copy Object Location
						bpy.ops.view3d.snap_cursor_to_selected()
						object_loc = bpy.context.scene.cursor_location.copy()
						#Move Object to Center
						bpy.ops.object.location_clear(clear_delta=False)
					else:
						bpy.ops.view3d.snap_cursor_to_center()
						bpy.context.space_data.pivot_point = 'CURSOR'
					name = x.name
					bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
					
					#Scale Fix
					if context.scene.apply_scale:
						bpy.context.scene.unit_settings.scale_length = 0.01
						bpy.ops.transform.resize(value=(100, 100, 100))
						bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
					
					#Export FBX
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), version='BIN7400', ui_tab='MAIN', use_selection=True, global_scale=1, apply_unit_scale=True)
					
					#Scale down to normal size
					if context.scene.apply_scale:
						if context.scene.apply_loc:
							bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
						else:
							bpy.ops.view3d.snap_cursor_to_center()
							bpy.context.space_data.pivot_point = 'CURSOR'
						bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
						bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
					
					bpy.ops.object.select_all(action='DESELECT')
					x.select = True
					
					#Restore Object Location
					if context.scene.apply_loc:
						bpy.context.scene.cursor_location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
				
			
			#Apply rotation and scale
			if context.scene.apply_scale:
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
			
			if context.scene.apply_rot:
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
			
			
			#Select again objects and set active object
			bpy.ops.object.select_all(action='DESELECT')
			for j in start_selected_obj:
				j.select = True;
			bpy.context.scene.objects.active = start_active_obj
			#Restore Unit System and "Pivot Point Align" option
			bpy.context.scene.unit_settings.scale_length = current_scale_length
			bpy.context.scene.unit_settings.system = current_unit_system
			bpy.context.space_data.use_pivot_point_align = current_pivot_point_align
			#Restore Cursor Location and Pivot Point Mode
			bpy.context.scene.cursor_location = saved_cursor_loc
			bpy.context.space_data.pivot_point = current_pivot_point
		
		return {'FINISHED'}

#-------------------------------------------------------
#Palette Texture Creator
class PaletteCreate(bpy.types.Operator):
	"""Palette Texture Creator"""
	bl_idname = "object.palette_creator"
	bl_label = "Palette Texture Creator"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#check opened image editor window
		IE_area = 0
		flag_exist_area = False
		for area in range(len(bpy.context.screen.areas)):
			if bpy.context.screen.areas[area].type == 'IMAGE_EDITOR':
				IE_area = area
				flag_exist_area = True
				bpy.context.screen.areas[area].type = 'CONSOLE'

		# get selected MESH objects and get active object name
		current_objects = []
		for selected_mesh in bpy.context.selected_objects:
			if selected_mesh.type == 'MESH':
				current_objects.append(selected_mesh)
				# remove empty material slots
				for q in reversed(range(len(selected_mesh.data.materials))):
					if selected_mesh.data.materials[q] == None:
						bpy.context.object.active_material_index = q
						# unlink empty slots
						selected_mesh.data.materials.pop(q, update_data=True)
						
		add_name_palette = bpy.context.active_object.name

		# set tool setting for uv editor
		bpy.context.scene.tool_settings.use_uv_select_sync = False
		bpy.context.scene.tool_settings.uv_select_mode = 'FACE'

		# get materials from selected objects
		me = []
		for x in current_objects:
			me += x.data.materials

		# check exist material Palette_background
		flag_exist_mat = False
		for a in range(len(bpy.data.materials)):
			if bpy.data.materials[a].name == 'Palette_background':
				flag_exist_mat = True
				palette_back_color = bpy.data.materials[a]

		# create or not palette background material
		if flag_exist_mat == False:
			palette_back_color = bpy.data.materials.new('Palette_background')
			palette_back_color.diffuse_color = 0.8, 0.8, 0.8

		# check exist palette plane
		flag_exist_obj = False
		for o in range(len(bpy.data.objects)):
			if bpy.data.objects[o].name == ('Palette_' + add_name_palette):
				flag_exist_obj = True

		if flag_exist_obj == True:
			bpy.ops.object.select_all(action='DESELECT')
			bpy.data.objects['Palette_' + add_name_palette].select = True
			bpy.ops.object.delete()
				
		bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
		pln = bpy.context.object
		pln.name = 'Palette_' + add_name_palette

		# Add palette background material to palette plane
		pln.data.materials.append(palette_back_color)

		# Add materials to palette plane
		mat_offset = len(me)
		i = 0
		for i in range(mat_offset):
			flag_non = False
			palette_mat = pln.data.materials
			palette_mat_len = len(palette_mat)
			j = 0
			
			for j in range(palette_mat_len):
				if palette_mat[j] == me[i]:
					flag_non = True
					
			if flag_non == False:
				pln.data.materials.append(me[i])
				
		# compute number of subdivide palette plane from number of materials
		palette_mat = pln.data.materials
		palette_mat_len = len(palette_mat)
		palette_mat_wobg = palette_mat_len - 1
		number_of_subdiv = 0
		if palette_mat_wobg > 1 and palette_mat_wobg <= 4:
			number_of_subdiv = 1
			
		if palette_mat_wobg > 4 and palette_mat_wobg <= 16:
			number_of_subdiv = 2

		if palette_mat_wobg > 16 and palette_mat_wobg <= 64:
			number_of_subdiv = 3

		if palette_mat_wobg > 64 and palette_mat_wobg <= 256:
			number_of_subdiv = 4
			
		# subdivide palette plane
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
		n = 0
		for n in range(number_of_subdiv):
			bpy.ops.mesh.subdivide(smoothness=0)

		#TEST check exist texture image

		# create texture and unwrap
		bpy.ops.mesh.select_all(action='SELECT')

		#TEST check exist texture image
		flag_exist_texture = False
		for t in range(len(bpy.data.images)):
			if bpy.data.images[t].name == ('Palette_' + add_name_palette):
				flag_exist_texture = True
				
		# create or not texture
		if flag_exist_texture == False:
			bpy.ops.image.new( name='Palette_' + add_name_palette, width = 32, height = 32)

		bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
		bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['Palette_' + add_name_palette]


		# set materials to plane's polygons
		bpy.ops.object.mode_set(mode = 'OBJECT')
		ob = bpy.context.object

		for poly in ob.data.polygons:   
			if (poly.index + 1) < palette_mat_len:
				poly.material_index = poly.index + 1

		# bake palette texture
		bpy.context.scene.render.bake_type = 'TEXTURE' 
		bpy.ops.object.bake_image()

		# Create collection materials with (mat_name, uv_x_mat, uv_y_mat)
		mat_coll_array = []
		collect_uv_mat = 1
		current_area = bpy.context.area.type

		for collect_uv_mat in range(palette_mat_len - 1):

			# select polygon
			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action='DESELECT')
			bpy.ops.object.mode_set(mode = 'OBJECT')
			ob.data.polygons[collect_uv_mat].select = True
			bpy.ops.object.mode_set(mode = 'EDIT')

			# get mat_name
			mat_index = ob.data.polygons[collect_uv_mat].material_index
			mat_name = ob.data.materials[mat_index].name

			bpy.context.area.type = 'IMAGE_EDITOR'
			
			if bpy.context.area.spaces[0].image != None:
				if bpy.context.area.spaces[0].image.name == 'Render Result':
					bpy.context.area.spaces[0].image = None
			
			bpy.ops.uv.snap_cursor(target='SELECTED')

			# get coord center poly
			x_loc = (1/256)*bpy.context.area.spaces[0].cursor_location[0]
			y_loc = (1/256)*bpy.context.area.spaces[0].cursor_location[1]
			mat_coll_list = [mat_name, x_loc, y_loc]
			mat_coll_array.append(mat_coll_list)
			
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.area.type = 'VIEW_3D'
			
		for r in current_objects:   
			bpy.ops.object.select_all(action='DESELECT')
			r.select = True
			# unwrap selected objects and add palette texture
			bpy.context.scene.objects.active = r	
			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.uv.smart_project(angle_limit=89, island_margin=0.01, user_area_weight=0, use_aspect=True)
			bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['Palette_' + add_name_palette]
			
			bpy.ops.mesh.select_all(action='DESELECT')
			# select poly with 1 material 
			r_mats = r.data.materials
			r_mats_len = len(r_mats)
			r_mat_index = 0
			print(r_mats, r_mats_len)
			for r_mat_index in range(r_mats_len):
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.context.object.active_material_index = r_mat_index
				r_mat_name = bpy.context.object.data.materials[r_mat_index].name
				bpy.ops.object.material_slot_select()
				bpy.ops.uv.select_all(action = 'SELECT')
				print(r_mat_index)
				# get XY material on UV
				h = 0
				r_mat_x = 0
				r_mat_y = 0
				for h in range (len(mat_coll_array)):
					if (r_mat_name == mat_coll_array[h][0]):
						r_mat_x = mat_coll_array[h][1]
						r_mat_y = mat_coll_array[h][2]
				
				# scale uv to color on palette texture
				bpy.context.area.type = 'IMAGE_EDITOR'
				bpy.ops.uv.cursor_set(location = (r_mat_x, r_mat_y))
				bpy.context.space_data.pivot_point = 'CURSOR'
				bpy.ops.transform.resize(value=(0, 0, 1),\
					 constraint_axis=(False, False, False),\
					  constraint_orientation='GLOBAL', mirror=False,\
					   proportional='DISABLED', proportional_edit_falloff='SMOOTH',\
						proportional_size=1, snap=False, snap_target='CLOSEST',\
						 snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0),\
						  texture_space=False, release_confirm=False)
						  
			bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# Delete Palette Plane
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Palette_' + add_name_palette].select = True
		bpy.ops.object.delete()
		
		# Select again objects
		for j in current_objects:
			j.select = True;		
			
		bpy.context.area.type = current_area

		if flag_exist_area == True:
			bpy.context.screen.areas[IE_area].type = 'IMAGE_EDITOR'

		return {'FINISHED'}

#-------------------------------------------------------
#Quick Bake Vertex Colors from Texture
class BakeVC(bpy.types.Operator):
	"""Quick Bake Vertex Colors from Texture"""
	bl_idname = "object.bake_vc"
	bl_label = "Quick Bake Vertex Colors from Texture"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			if x.type == 'MESH':
				if len(x.data.uv_layers) > 0:
					bpy.context.scene.objects.active = x
					bpy.ops.paint.vertex_paint_toggle()
					bpy.context.object.data.use_paint_mask = True
					bpy.ops.paint.face_select_all(action='SELECT')
					bpy.ops.uv.bake_texture_to_vcols()
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.ops.mesh.uv_texture_remove()
			
		# Select again objects
		for j in selected_obj:
			j.select = True;
		
		bpy.context.scene.objects.active = active_obj
							
		return {'FINISHED'}

#-------------------------------------------------------
#Clear Custom Split Normals
class ClearNormals(bpy.types.Operator):
	"""Clear Custom Split Normals"""
	bl_idname = "object.clear_normals"
	bl_label = "Clear Custom Split Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			if x.type == 'MESH':
				bpy.context.scene.objects.active = x
				bpy.ops.mesh.customdata_custom_splitnormals_clear()
				bpy.context.object.data.auto_smooth_angle = 3.14159
				
		# Select again objects
		for j in selected_obj:
			j.select = True;
		
		bpy.context.scene.objects.active = active_obj
							
		return {'FINISHED'}		
		
#-------------------------------------------------------
#Recalculate Normals
class CalcNormals(bpy.types.Operator):
	"""Recalculate Normals"""
	bl_idname = "object.calc_normals"
	bl_label = "Flip/Calculate Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			if x.type == 'MESH':
				bpy.context.scene.objects.active = x
				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				if context.scene.calc_normals_en == False:
					bpy.ops.mesh.flip_normals()
				else:
					bpy.ops.mesh.normals_make_consistent(inside=context.scene.normals_inside)
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.ops.object.mode_set(mode='OBJECT')
				
		# Select again objects
		for j in selected_obj:
			j.select = True;
		
		bpy.context.scene.objects.active = active_obj
							
		return {'FINISHED'}
		
#-------------------------------------------------------
#Batch Import FBX and OBJ
class ImportFBXOBJ(bpy.types.Operator, ImportHelper):
	"""Batch Import FBX and OBJ"""
	bl_idname = "object.import_fbxobj"
	bl_label = "Import FBXs/OBJs"
	bl_options = {'REGISTER', 'UNDO'}
	files = CollectionProperty(name="File Path", type=OperatorFileListElement)
	directory = StringProperty(subtype="DIR_PATH")
	
	def execute(self, context):
		directory = self.directory
		for f in self.files:
			filepath = os.path.join(directory, f.name)
			extension = (os.path.splitext(f.name)[1])[1:]
			#print(filepath)
			#print(extension)
			if extension == "fbx" or extension == "FBX":
				bpy.ops.import_scene.fbx(filepath = filepath)
			if extension == "obj" or extension == "OBJ":
				bpy.ops.import_scene.obj(filepath = filepath)
			
		return {'FINISHED'}

#-------------------------------------------------------
#Rename object(s)
class RenameObject(bpy.types.Operator):
	"""Rename object(s)"""
	bl_idname = "object.rename_object"
	bl_label = "Rename object(s)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		old_str = context.scene.old_text
		new_str = context.scene.new_text
		new_name_glob = context.scene.new_name
		prefix = context.scene.prefix
		postfix = context.scene.postfix
		selected_obj = bpy.context.selected_objects
		
		#New name
		if bpy.context.scene.rename_select == '2':
			for x in selected_obj:
				x.name = new_name_glob
		
		#Add Pre/Postfix
		if bpy.context.scene.rename_select == '0':
			for x in selected_obj:
				ob_name = x.name
				#Preprocess Delete Blender Numbers
				if context.scene.delete_nums:
					if StrIsInt(ob_name[-3:]):
						dot_pos = len(ob_name) - 4
						if ob_name[dot_pos] == '.':
							ob_name = ob_name[:-4]
				new_name = prefix + ob_name + postfix
				x.name = new_name
				
		#Replace
		if bpy.context.scene.rename_select == '1':
			for x in selected_obj:
				if x.name.find(old_str) > -1:
					ob_name = x.name
					new_name = ob_name.replace(old_str, new_str)
					x.name = new_name
					
		return {'FINISHED'}

#Rename UV(s)
class RenameUV(bpy.types.Operator):
	"""Rename UV(s)"""
	bl_idname = "object.uv_rename"
	bl_label = "Rename UV(s)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects	
		uv_index = bpy.context.scene.uv_layer_index
		uv_name = bpy.context.scene.uv_name
		
		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].name = uv_name
				
		return {'FINISHED'}

#-------------------------------------------------------		
#Numbering
class Numbering(bpy.types.Operator):
	"""Rename UV(s)"""
	bl_idname = "object.numbering"
	bl_label = "Numbering of Objects"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects	
		objects_list = []
		
		for x in selected_obj:
			#List of Objects
			if bpy.context.scene.nums_method == '0' or bpy.context.scene.nums_method == '3':
				object_class = [x.name, x.location.x]
			if bpy.context.scene.nums_method == '1':
				object_class = [x.name, x.location.y]
			if bpy.context.scene.nums_method == '2':
				object_class = [x.name, x.location.z]
			
			objects_list.append(object_class)
			
		#Sort List
		if bpy.context.scene.nums_method != '3':
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
			if context.scene.delete_prev_nums:
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
			if bpy.context.scene.nums_format == '0': 
				num_str = str(y+1)
			
			#_0X, _XX, _XXX
			if bpy.context.scene.nums_format == '1':
				if (y <= 8):
					num_str = '0' + str(y+1)
				else:
					num_str = str(y+1)
			
			#_00X, _0XX, _XXX
			if bpy.context.scene.nums_format == '2':
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
class UVremove(bpy.types.Operator):
	"""Remove UV layer"""
	bl_idname = "object.uv_remove"
	bl_label = "Remove UV layer"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			bpy.context.scene.objects.active = x
			if x.type == 'MESH':
				for a in range(len(x.data.uv_layers)):
					bpy.ops.mesh.uv_texture_remove()			
		
		# Select again objects
		for j in selected_obj:
			j.select = True;
			
		bpy.context.scene.objects.active = active_obj
		
		return {'FINISHED'}

#------------------Align Origin To Min-------------------------------
class AlignMin(bpy.types.Operator):
	"""Origin To Min """
	bl_idname = "object.align_min"
	bl_label = "Origin To Min"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign = bpy.props.StringProperty()
	
	def execute(self, context):

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor_location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			bpy.context.scene.objects.active = x
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
				
				if context.scene.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor_location = [MinCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor_location = [saved_origin_loc[0], MinCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor_location = [saved_origin_loc[0], saved_origin_loc[1], MinCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor_location = saved_cursor_loc
				
				if context.scene.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MinCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MinCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MinCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select = True;
			
		bpy.context.scene.objects.active = current_active_obj
		
		return {'FINISHED'}
	
#------------------Align Origin To Max-------------------------------
class AlignMax(bpy.types.Operator):
	"""Origin To Max """
	bl_idname = "object.align_max"
	bl_label = "Origin To Max"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign = bpy.props.StringProperty()
	
	def execute(self, context):

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor_location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			bpy.context.scene.objects.active = x
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
				
				if context.scene.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor_location = [MaxCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor_location = [saved_origin_loc[0], MaxCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor_location = [saved_origin_loc[0], saved_origin_loc[1], MaxCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor_location = saved_cursor_loc
				
				if context.scene.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MaxCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MaxCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MaxCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select = True;
			
		bpy.context.scene.objects.active = current_active_obj
		
		return {'FINISHED'}
	
#------------------Align Cursor------------------
class AlignCur(bpy.types.Operator):
	"""Origin Align To Cursor"""
	bl_idname = "object.align_cur"
	bl_label = "Origin To Cursor"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign = bpy.props.StringProperty()
	
	def execute(self, context):

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		saved_cursor_loc = bpy.context.scene.cursor_location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy()
			#Align to 3D Cursor
			if self.TypeAlign == 'X':
				bpy.context.scene.cursor_location = [saved_cursor_loc[0], saved_origin_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Y':
				bpy.context.scene.cursor_location = [saved_origin_loc[0], saved_cursor_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Z':
				bpy.context.scene.cursor_location = [saved_origin_loc[0], saved_origin_loc[1], saved_cursor_loc[2]] 
			# Apply origin to Cursor position
			if context.scene.align_geom_to_orig == False:
				bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
			else:
				if self.TypeAlign == 'X':
					Difference = saved_cursor_loc[0] - saved_origin_loc[0]
					bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Y':
					Difference = saved_cursor_loc[1] - saved_origin_loc[1]
					bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Z':
					Difference = saved_cursor_loc[2] - saved_origin_loc[2]
					bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
			# Reset 3D Cursor position  
			bpy.context.scene.cursor_location = saved_cursor_loc
		
		# Select again objects
		for j in current_selected_obj:
			j.select = True;
		
		return {'FINISHED'}

#------------------Align Coordinate------------------ 
class AlignCo(bpy.types.Operator):
	"""Origin Align To Spec Coordinate"""
	bl_idname = "object.align_co"
	bl_label = "Origin Align To Spec Coordinate"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign = bpy.props.StringProperty()

	def execute(self, context):
		wrong_align_co = False
		#Check coordinate if check tgis option
		try:
			align_coordinate = float(context.scene.align_co)
		except:
			self.report({'INFO'}, 'Coordinate is wrong')
			wrong_align_co = True   
		
		if wrong_align_co == False:
			# Save selected objects and current position of 3D Cursor
			current_selected_obj = bpy.context.selected_objects
			saved_cursor_loc = bpy.context.scene.cursor_location.copy()
			bpy.ops.object.mode_set(mode = 'OBJECT')
			# Change individual origin point
			for x in current_selected_obj:
				# Select only current object (for setting origin)
				bpy.ops.object.select_all(action='DESELECT')
				x.select = True
				# Save current origin and relocate 3D Cursor
				saved_origin_loc = x.location.copy()
				
				#Align to Coordinate
				if self.TypeAlign == 'X':
					bpy.context.scene.cursor_location = [align_coordinate, saved_origin_loc[1], saved_origin_loc[2]] 
				if self.TypeAlign == 'Y':
					bpy.context.scene.cursor_location = [saved_origin_loc[0], align_coordinate, saved_origin_loc[2]] 
				if self.TypeAlign == 'Z':
					bpy.context.scene.cursor_location = [saved_origin_loc[0], saved_origin_loc[1], align_coordinate] 
				
				if context.scene.align_geom_to_orig == False:
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
				else:
					if self.TypeAlign == 'X':
						Difference = align_coordinate - saved_origin_loc[0]
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						Difference = align_coordinate - saved_origin_loc[1]
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						Difference = align_coordinate - saved_origin_loc[2]
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				# Reset 3D Cursor position  
				bpy.context.scene.cursor_location = saved_cursor_loc
			
			# Select again objects
			for j in current_selected_obj:
				j.select = True;
			
		return {'FINISHED'}

#-------------------------------------------------------
#OriginRotate
class OriginRotate(bpy.types.Operator):
	"""Rotate Origin"""
	bl_idname = "object.origin_rotate"
	bl_label = "Rotate Origin"
	bl_options = {'REGISTER', 'UNDO'}
	TypeRot = bpy.props.StringProperty()
	def execute(self, context):
		
		wrong_angle = False
		#Check value if check this option
		try:
			RotValue = float(context.scene.origin_rotate_value)
		except:
			self.report({'INFO'}, 'Angle is wrong')
			wrong_angle = True   
		
		if bpy.context.scene.orientation_select == '0':
			Ori_Constaraint = 'GLOBAL'
		if bpy.context.scene.orientation_select == '1':
			Ori_Constaraint = 'LOCAL'
		
		if wrong_angle == False:
			active_obj = bpy.context.active_object
			bpy.ops.object.select_all(action='DESELECT')
			active_obj.select = True
			if active_obj.type == 'MESH':
				bpy.ops.object.duplicate()
				dupli_object = bpy.context.active_object
				if self.TypeRot == 'X+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'X-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Y+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Y-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Z+':
					bpy.ops.transform.rotate(value= (math.pi * RotValue / 180), axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeRot == 'Z-':
					bpy.ops.transform.rotate(value= -(math.pi * RotValue / 180), axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation=Ori_Constaraint, mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)	
				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				bpy.ops.mesh.delete()
				bpy.ops.object.mode_set(mode = 'OBJECT')
				active_obj.select = True
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
		min_co = (obj.matrix_world*bm.verts[0].co)[CoordIndex]
		max_co = (obj.matrix_world*bm.verts[0].co)[CoordIndex]
		
		for v in bm.verts:
			if (obj.matrix_world*v.co)[CoordIndex] < min_co:
				min_co = (obj.matrix_world*v.co)[CoordIndex]
			if (obj.matrix_world*v.co)[CoordIndex] > max_co:
				max_co = (obj.matrix_world*v.co)[CoordIndex]
		
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
class SetOriginToSelect(bpy.types.Operator):
	"""Set Origin To Selection"""
	bl_idname = "object.set_origin_to_select"
	bl_label = "Set Origin To Selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		saved_cursor_loc = bpy.context.scene.cursor_location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Apply origin to Cursor position
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		# Reset 3D Cursor position  
		bpy.context.scene.cursor_location = saved_cursor_loc
		bpy.ops.object.mode_set(mode = 'EDIT')
		return {'FINISHED'} 	

#-------------------------------------------------------
#Copy Texture Assignment
class CopyTextAssign(bpy.types.Operator):
	"""Copy Texture Assignment"""
	bl_idname = "object.copy_text_assign"
	bl_label = "Copy Texture Assignment"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		if active_obj.type == 'MESH' and active_obj.data.uv_textures.active != -1:
			UVdata = active_obj.data.uv_textures.active.data[0]
			if UVdata.image != None:
				img = UVdata.image.name
				
			for x in selected_obj:
				bpy.ops.object.select_all(action='DESELECT')
				x.select = True
				if x.type == 'MESH':
					bpy.context.scene.objects.active = x
					bpy.ops.object.mode_set(mode = 'EDIT')
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					
					if x.data.uv_textures.active != -1:
						if UVdata.image != None:
							bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images[img]
						else:
							bpy.data.screens['UV Editing'].areas[1].spaces[0].image = None
					
					bpy.ops.mesh.select_all(action='DESELECT')
					bpy.ops.object.mode_set(mode='OBJECT')
					
		# Select again objects
		for j in selected_obj:
			j.select = True;
			
		bpy.context.scene.objects.active = active_obj
		UVdata = None
		img = None
		
		return {'FINISHED'}

#-------------------------------------------------------
#Clear Custom Orientations
class ClearCustomOri(bpy.types.Operator):
	"""Clear Custom Orientations"""
	bl_idname = "object.clear_custom_ori"
	bl_label = "Clear Custom Orientations"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		current_scene = bpy.context.scene
		for x in bpy.data.scenes[current_scene.name].orientations:
			name = x.name
			views = [area.spaces.active for area in bpy.context.screen.areas if area.type == 'VIEW_3D']
			if views:
				views[0].transform_orientation = name
			
			areas = [area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D']
			if areas:
				override = bpy.context.copy()
				override['area'] = areas[0]
				bpy.ops.transform.delete_orientation( override )
			
		return {'FINISHED'} 			

#-------------------------------------------------------
#Obj Name to Mesh Name
class ObjNameToMeshName(bpy.types.Operator):
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
class ClearVertexColors(bpy.types.Operator):
	"""# Clear Vertex Colors"""
	bl_idname = "object.clear_vc"
	bl_label = "# Clear Vertex Colors"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		for x in current_selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select = True
			bpy.context.scene.objects.active = x
			if x.type == 'MESH':
				for y in x.data.vertex_colors:
					bpy.ops.mesh.vertex_color_remove()
				bpy.ops.mesh.vertex_color_remove()
				
		for x in current_selected_obj:
			x.select = True
		bpy.context.scene.objects.active = current_active_obj
		return {'FINISHED'} 			

class UV_Mover(bpy.types.Operator):
	"""UV Mover"""
	bl_idname = "uv.uv_mover"
	bl_label = "Move and Scale UV islands"
	bl_options = {'REGISTER', 'UNDO'}
	Value = bpy.props.StringProperty()
	
	def execute(self, context):
		Start_Pivot_Mode = bpy.context.space_data.pivot_point
		bpy.context.space_data.pivot_point = 'CURSOR'
		move_step = 1/2**int(bpy.context.scene.uv_move_factor)
		if self.Value == "TL":
			bpy.ops.uv.cursor_set(location=(0, 1))
		if self.Value == "TR":
			bpy.ops.uv.cursor_set(location=(1, 1))
		if self.Value == "BL":
			bpy.ops.uv.cursor_set(location=(0, 0))
		if self.Value == "BR":
			bpy.ops.uv.cursor_set(location=(1, 0))
			
		if self.Value == "MINUS":
			bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "PLUS":
			bpy.ops.transform.resize(value=(2, 2, 2), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "RIGHT":
			bpy.ops.transform.translate(value=(move_step, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "LEFT":
			bpy.ops.transform.translate(value=(-1 * move_step, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "UP":
			bpy.ops.transform.translate(value=(0, move_step, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.Value == "DOWN":
			bpy.ops.transform.translate(value=(0, -1 * move_step, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)	
		
		bpy.context.space_data.pivot_point = Start_Pivot_Mode

		
		return {'FINISHED'}
		
#-------------------------------------------------------
#Panels
class VIEW3D_PT_Origin_Tools_panel(bpy.types.Panel):
	bl_label = "Origin Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.label("Origin Rotation")
				row = layout.row()
				row.prop(context.scene, 'orientation_select', expand=False)
				row = layout.row()
				row.prop(context.scene, "origin_rotate_value", text="Angle")
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.5)
				c = split.column()
				c.operator("object.origin_rotate", text="X-").TypeRot = 'X-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="X+").TypeRot = 'X+'
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.5)
				c = split.column()
				c.operator("object.origin_rotate", text="Y-").TypeRot = 'Y-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="Y+").TypeRot = 'Y+'
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.5)
				c = split.column()
				c.operator("object.origin_rotate", text="Z-").TypeRot = 'Z-'
				split = split.split()
				c = split.column()
				c.operator("object.origin_rotate", text="Z+").TypeRot = 'Z+'
				layout.separator()
				
				row = layout.row()
				row.label("Origin Align")
				row = layout.row()
				row.prop(context.scene, "align_co", text="Coordinate")
				row = layout.row()
				row.prop(context.scene, "align_geom_to_orig", text="Geometry To Origin")
				
				#--Aligner Labels----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.33)
				c = split.column()
				c.label("X")
				split = split.split(percentage=0.5)
				c = split.column()
				c.label("Y")
				split = split.split()
				c = split.column()
				c.label("Z")
				
				#--Aligner Min Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.33)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='X'
				split = split.split(percentage=0.5)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Z'
				
				#--Aligner Max Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.33)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='X'
				split = split.split(percentage=0.5)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Z'
				
				#--Aligner Cursor Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.33)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='X'
				split = split.split(percentage=0.5)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Z'
				
				#--Aligner Coordinates Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(percentage=0.33)
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='X'
				split = split.split(percentage=0.5)
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

class VIEW3D_PT_Rename_Tools_panel(bpy.types.Panel):
	bl_label = "Rename Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				layout.label("Rename UV")
				row = layout.row()
				row.prop(context.scene, "uv_layer_index", text="UV Index")
				row = layout.row()
				row.prop(context.scene, "uv_name")
				row = layout.row()
				row.operator("object.uv_rename", text="Rename UV(s)")
				layout.separator()
				
				layout.label("Rename Objects")
				row = layout.row()
				row.prop(context.scene, 'rename_select', expand=False)
				row = layout.row()
				if bpy.context.scene.rename_select == '0':
					row.prop(context.scene, "prefix")
					row = layout.row()
					row.prop(context.scene, "postfix")
					row = layout.row()
				if bpy.context.scene.rename_select == '1':
					row.prop(context.scene, "old_text")
					row = layout.row()
					row.prop(context.scene, "new_text")
					row = layout.row()
				if bpy.context.scene.rename_select == '2':
					row.prop(context.scene, "new_name")
					row = layout.row()
				if bpy.context.scene.rename_select == '0':
					layout.prop(context.scene, "delete_nums", text="Delete Blender Nums")
					row = layout.row()
				row.operator("object.rename_object", text="Rename Object(s)")
				
				layout.separator()
				layout.label("Numbering Objects")
				row = layout.row()
				row.prop(context.scene, 'nums_method', expand=False)
				row = layout.row()
				row.prop(context.scene, 'nums_format', expand=False)
				row = layout.row()
				row.prop(context.scene, "delete_prev_nums", text="Delete Previous Nums")
				row = layout.row()
				row.operator("object.numbering", text="Set Numbering")
				
class VIEW3D_PT_ImportExport_Tools_panel(bpy.types.Panel):
	bl_label = "Import/Export Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				layout.label("Export Mode:")
				row = layout.row()
				row.prop(context.scene, 'fbx_export_mode', expand=False)
				row = layout.row()
				layout.label("Apply:")
				layout.prop(context.scene, "apply_rot", text="Rotation")
				layout.prop(context.scene, "apply_scale", text="Scale")
				if bpy.context.scene.fbx_export_mode == '0' or bpy.context.scene.fbx_export_mode == '2':
					layout.prop(context.scene, "apply_loc", text="Location")
				row = layout.row()
				if bpy.context.scene.fbx_export_mode == '1':
					layout.prop(context.scene, "set_custom_fbx_name", text="Custom Name for FBX")
					if bpy.context.scene.set_custom_fbx_name:
						layout.prop(context.scene, "custom_fbx_name")
				row = layout.row()
				layout.prop(context.scene, "custom_export_path", text="Custom Export Path")
				if bpy.context.scene.custom_export_path:
					layout.prop(context.scene, 'export_path')
				row = layout.row()
				row.operator("object.multi_fbx_export", text="Export FBX to Unity")
				row = layout.row()
		
		if context.mode == 'OBJECT':
			row = layout.row()
			row.operator("object.import_fbxobj", text="Import FBXs/OBJs")
				
class VIEW3D_PT_LowPolyArt_Tools_panel(bpy.types.Panel):
	bl_label = "Low Poly Art Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.palette_creator", text="Create Palette Texture")
				layout.separator()
			
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.bake_vc", text="Texture to Vertex Colors")
				layout.separator()
			
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.uv_remove", text="Clear UV Maps")
				row = layout.row()
				row.operator("object.clear_vc", text="Clear Vertex Colors")
				layout.separator()
		
class VIEW3D_PT_tools_asset_toolset(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(self, context):
		return (True)

	def draw(self, context):
		layout = self.layout
		row = layout.row()	
		row.operator("object.clear_custom_ori", text="Clear Custom Orientations")
		row = layout.row()		
		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
		
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.copy_text_assign", text="Copy Texture Assignment")
				row = layout.row()		
				row.operator("object.objname_to_meshname", text="Obj Name -> Mesh Name")
				layout.separator()
				row = layout.row()
				row.operator("object.clear_normals", text="Clear Custom Normals")
				row = layout.row()
				row.operator("object.calc_normals", text="Flip/Calculate Normals")
				layout.prop(context.scene, "calc_normals_en", text="Recalc Normals")
				layout.prop(context.scene, "normals_inside", text="Inside")
				layout.separator()

class VIEW3D_PT_uv_mover_panel(bpy.types.Panel):
	bl_label = "UV Mover"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = 'TOOLS'

	def draw(self, context):
		layout = self.layout
		if context.object.mode == 'EDIT':
			layout.label("Set Cursor To Corner:")
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(percentage=0.5)
			c = split.column()
			c.operator("uv.uv_mover", text="Top Left").Value="TL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Top Right").Value="TR"
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(percentage=0.5)
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Left").Value="BL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Right").Value="BR"
			
			layout.separator()
			row = layout.row()
			
			#--Aligner Buttons----
			layout.label("Scale and Move:")
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(percentage=0.33)
			c = split.column()
			c.operator("uv.uv_mover", text="Scale-").Value="MINUS"
			split = split.split(percentage=0.5)
			c = split.column()
			c.operator("uv.uv_mover", text="UP").Value="UP"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Scale+").Value="PLUS"
				
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(percentage=0.33)
			c = split.column()
			c.operator("uv.uv_mover", text="LEFT").Value="LEFT"
			split = split.split(percentage=0.5)
			c = split.column()
			c.operator("uv.uv_mover", text="DOWN").Value="DOWN"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="RIGHT").Value="RIGHT"
			
			layout.separator()
			
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(percentage=0.5)
			c = split.column()
			c.label("Move Step   1/")
			split = split.split()
			c = split.column()
			c.prop(context.scene, 'uv_move_factor', expand=False)
		
#-------------------------------------------------------		
def register():
	bpy.utils.register_module(__name__)
	bpy.types.Scene.old_text = bpy.props.StringProperty(
		name="Find",
		description="Text for search",
		default="")
	
	bpy.types.Scene.new_text = bpy.props.StringProperty(
		name="Replace",
		description="Text for replace",
		default="")
		
	bpy.types.Scene.prefix = bpy.props.StringProperty(
		name="Prefix",
		description="Prefix Text",
		default="")
		
	bpy.types.Scene.postfix = bpy.props.StringProperty(
		name="Postfix",
		description="Postfix Text",
		default="")
	
	bpy.types.Scene.new_name = bpy.props.StringProperty(
		name="New Name",
		description="New Name for Objects",
		default="")
	
	bpy.types.Scene.delete_nums = bpy.props.BoolProperty(
		name="Delete Blender Nums",
		description="Delete Blender Numbers from Object Names",
		default = True)
	
	bpy.types.Scene.delete_prev_nums = bpy.props.BoolProperty(
		name="Delete Previous Nums",
		description="Delete Previous Numbers from Object Names",
		default = True)
	
	bpy.types.Scene.align_co = bpy.props.FloatProperty(
		name="",
		description="Coordinate",
		default=0.00,
		min = -9999,
        max = 9999,
		step = 50)
	
	nums_method_items = (('0','Along X',''),('1','Along Y',''), ('2','Along Z',''), ('3','Simple',''))
	bpy.types.Scene.nums_method = bpy.props.EnumProperty(name="Method", items = nums_method_items)
	
	nums_format_items = (('0','_X, _XX, _XXX',''),('1','_0X, _XX, _XXX',''), ('2','_00X, _0XX, _XXX',''))
	bpy.types.Scene.nums_format = bpy.props.EnumProperty(name="Format", items = nums_format_items)
	
	axis_items = (('0','X',''),('1','Y',''), ('2','Z',''))
	bpy.types.Scene.axis_select = bpy.props.EnumProperty(name="Axis", items = axis_items)
	
	rename_menu_items = (('0','Add Pre/Postfix',''),('1','Replace',''), ('2','New name',''))
	bpy.types.Scene.rename_select = bpy.props.EnumProperty(name="Rename function", items = rename_menu_items)
	
	orientation_menu_items = (('0','GLOBAL',''),('1','LOCAL',''))
	bpy.types.Scene.orientation_select = bpy.props.EnumProperty(name="Orientation", items = orientation_menu_items)

	fbx_export_mode_menu_items = (('0','1 Obj->1 FBX',''),('1','All->One FBX',''),('2','By Parent',''))
	bpy.types.Scene.fbx_export_mode = bpy.props.EnumProperty(name="", items = fbx_export_mode_menu_items)
	
	uv_move_factor_items = (('1','2',''),('2','4',''), ('3','8',''), ('4','16',''), ('5','32',''))
	bpy.types.Scene.uv_move_factor = bpy.props.EnumProperty(name="", items = uv_move_factor_items, default = '3')
	
	bpy.types.Scene.apply_rot = bpy.props.BoolProperty(
		name="Apply Rotation",
		description="Apply Rotation for Exported Models",
		default = True)
	bpy.types.Scene.apply_scale = bpy.props.BoolProperty(
		name="Apply Scale",
		description="Apply Scale for Exported Models",
		default = True)
	bpy.types.Scene.apply_loc = bpy.props.BoolProperty(
		name="Apply Location",
		description="Apply Location for Exported Models",
		default = True)
	bpy.types.Scene.set_custom_fbx_name = bpy.props.BoolProperty(
		name="Set Custom Name for FBX",
		description="Set Custom Name for FBX",
		default = False)
	bpy.types.Scene.custom_fbx_name = bpy.props.StringProperty(
		name="FBX Name",
		description="Custom Name for FBX",
		default="")
	
	bpy.types.Scene.custom_export_path = bpy.props.BoolProperty(
		name="Custom Export Path",
		description="Custom Export Path",
		default = False)
	
	bpy.types.Scene.normals_inside = bpy.props.BoolProperty(
		name="Inside Normals",
		description="Recalculate Normals Inside",
		default = False)
	
	bpy.types.Scene.calc_normals_en = bpy.props.BoolProperty(
		name="Recalc Normals",
		description="Recalculate Normals",
		default = False)

	bpy.types.Scene.align_geom_to_orig = bpy.props.BoolProperty(
		name="Geometry To Origin",
		description="Align Geometry To Origin",
		default = False)
	
	bpy.types.Scene.origin_rotate_value = bpy.props.FloatProperty(
		name="",
		description="Angle for Origin Rotate ",
		default=5.00,
		min = -1000,
        max = 1000,
		step = 50)
	
	bpy.types.Scene.uv_layer_index = bpy.props.IntProperty(
        name = "UV Index", 
        description = "UV Index",
		default = 0,
		min = 0,
        max = 10)
	
	bpy.types.Scene.uv_name = bpy.props.StringProperty(
		name="UV Name",
		description="UV Name",
		default="")
		
	bpy.types.Scene.export_path = bpy.props.StringProperty \
      (
      name = "Export Path",
      default = "",
      description = "Path for Export FBX",
      subtype = 'DIR_PATH'
      )
	
def unregister():
	bpy.utils.unregister_module(__name__)
	del bpy.types.Scene.old_text
	del bpy.types.Scene.new_text
	del bpy.types.Scene.prefix
	del bpy.types.Scene.postfix
	del bpy.types.Scene.new_name
	del bpy.types.Scene.delete_nums
	del bpy.types.Scene.delete_prev_nums
	del bpy.types.Scene.nums_method
	del bpy.types.Scene.nums_format
	del bpy.types.Scene.axis_select
	del bpy.types.Scene.normals_inside
	del bpy.types.Scene.calc_normals_en
	del bpy.types.Scene.align_co
	del bpy.types.Scene.align_geom_to_orig
	del bpy.types.Scene.orientation_select
	del bpy.types.Scene.uv_layer_index
	del bpy.types.Scene.fbx_export_mode
	del bpy.types.Scene.set_custom_fbx_name
	del bpy.types.Scene.custom_fbx_name
	del bpy.types.Scene.apply_loc
	del bpy.types.Scene.apply_rot
	del bpy.types.Scene.apply_scale
	del bpy.types.Scene.export_path
	del bpy.types.Scene.custom_export_path
	del bpy.types.Scene.uv_name
	del bpy.types.Scene.origin_rotate_value
	del bpy.types.Scene.rename_select
	del bpy.types.Scene.uv_move_factor
	

if __name__ == "__main__":
	register()
