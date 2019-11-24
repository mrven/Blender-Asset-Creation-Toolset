bl_info = {
	"name": "Asset Creation Toolset",
	"description": "Toolset for easy create assets for Unity 3D/3D Stocks/etc.",
	"author": "Ivan 'mrven' Vostrikov",
	"version": (2, 5, 0),
	"blender": (2, 81, 0),
	"location": "3D View > Toolbox",
	"category": "Object",
}

import bpy
import os
import subprocess
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
		apply_rotation_object_list = []

		act.export_dir = ""

		if act.fbx_export_mode == '1':
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

			if act.delete_mats_before_export:
				for o in current_selected_obj:
					if o.type == 'MESH' and len(o.data.materials) > 0:
						for q in reversed(range(len(o.data.materials))):
							bpy.context.object.active_material_index = q
							o.data.materials.pop(index = q)
			
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
			
			#Apply Scale
			if act.apply_scale:
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
				bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

			#Rotation Fix. Rotate X -90, Apply, Rotate X 90
			if act.apply_rot:
				bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
				#Operate only with higher level parents 
				for x in current_selected_obj:
					bpy.ops.object.select_all(action='DESELECT')
					if x.parent == None:
						x.select_set(True)
						bpy.context.view_layer.objects.active = x

						child_rotated = False
						bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
						for y in bpy.context.selected_objects:
							if abs(y.rotation_euler.x) + abs(y.rotation_euler.y) + abs(y.rotation_euler.z) > 0.017:
								child_rotated = True

						print(x.name)
						print(child_rotated)

						bpy.ops.object.select_all(action='DESELECT')
						x.select_set(True)

						# X-rotation fix
						if act.apply_rot_rotated or (not act.apply_rot_rotated and not child_rotated) or not act.fbx_export_mode == '2':
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							bpy.ops.transform.rotate(value= (math.pi * -90 / 180), orient_axis='X', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_type='GLOBAL', constraint_axis=(True, False, False), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)						
							bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
							
							for n in bpy.context.selected_objects:
								apply_rotation_object_list.append(n)
							
							bpy.ops.object.select_all(action='DESELECT')
							x.select_set(True)
							bpy.ops.transform.rotate(value= (math.pi * 90 / 180), orient_axis='X', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_type='GLOBAL', constraint_axis=(True, False, False), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.object.select_all(action='DESELECT')
			for x in current_selected_obj:
				if x.type == 'MESH' or x.type == 'EMPTY' or x.type == 'ARMATURE':
					x.select_set(True)

			#Export All as one fbx
			if act.fbx_export_mode == '1':
				if act.set_custom_fbx_name:
					name = act.custom_fbx_name
				
				#Export FBX
				bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')

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
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					
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
					bpy.ops.export_scene.fbx(filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					
					bpy.ops.object.select_all(action='DESELECT')
					x.select_set(True)
					
					#Restore Object Location
					if act.apply_loc:
						bpy.context.scene.cursor.location = object_loc
						bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
			
			#Export by Collection
			if act.fbx_export_mode == '3':

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
					bpy.ops.export_scene.fbx(filepath=str(path + c + '.fbx'), use_selection=True, apply_scale_options = 'FBX_SCALE_ALL')
					
				bpy.ops.object.select_all(action='DESELECT')


			#Apply Rotation
			if act.apply_rot:
				bpy.ops.object.select_all(action='DESELECT')
				
				if act.apply_rot_rotated or not act.fbx_export_mode == '2':
					for i in start_selected_obj:
						i.select_set(True)
				else:		
					for i in apply_rotation_object_list:
						i.select_set(True)

				bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
				bpy.ops.object.select_all(action='DESELECT')
			

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

			#save export dir
			act.export_dir = path
		
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
		#Check Render Engine
		if bpy.context.scene.render.engine != 'CYCLES':
			self.report({'INFO'}, 'Select Cycles Render Engine')
			return {'FINISHED'};

		#check opened image editor window
		IE_area = 0
		flag_exist_area = False
		for area in range(len(bpy.context.screen.areas)):
			if bpy.context.screen.areas[area].type == 'IMAGE_EDITOR':
				IE_area = area
				flag_exist_area = True
				bpy.context.screen.areas[area].type = 'CONSOLE'

		# get selected MESH objects and get active object name
		start_active_obj = bpy.context.active_object
		start_selected_obj = bpy.context.selected_objects
		current_objects = []
		for selected_mesh in bpy.context.selected_objects:
			if selected_mesh.type == 'MESH' and len(selected_mesh.data.materials) > 0:
				current_objects.append(selected_mesh)
				# remove empty material slots
				for q in reversed(range(len(selected_mesh.data.materials))):
					if selected_mesh.data.materials[q] == None:
						bpy.context.object.active_material_index = q
						# unlink empty slots
						selected_mesh.data.materials.pop(index = q)
						
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
			palette_back_color.diffuse_color = 0.8, 0.8, 0.8, 1.0

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

		# set materials to plane's polygons
		bpy.ops.object.mode_set(mode = 'OBJECT')
		ob = bpy.context.object

		for poly in ob.data.polygons:   
			if (poly.index + 1) < palette_mat_len:
				poly.material_index = poly.index + 1

		#BAKING!!!!!
		#ob - plane with materials (source)

		#create another plane (destination for baking)
		bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
		bake_plane = bpy.context.object
		bake_plane.name = 'Palette_Bake_Plane'

		bpy.ops.object.mode_set(mode = 'OBJECT')

		# check exist material for Baking
		flag_exist_bake_mat = False
		for a in range(len(bpy.data.materials)):
			if bpy.data.materials[a].name == 'Palette_Bake':
				bpy.data.materials.remove(bpy.data.materials[a])
				

		# create or not palette bake material
		if flag_exist_bake_mat == False:
			palette_bake_mat = bpy.data.materials.new('Palette_Bake')

		#Setup material for baking
		bake_plane.data.materials.append(palette_bake_mat)
		palette_bake_mat.use_nodes = True
		Nodes = palette_bake_mat.node_tree.nodes
		TexNode = Nodes.new('ShaderNodeTexImage')
		TexNode.location = (-500,0)
		TexNode.image = bpy.data.images['Palette_' + add_name_palette]

		#Bake Action
		ob.select_set(True)
		bpy.context.scene.cycles.bake_type = 'DIFFUSE'
		bpy.context.scene.render.bake.use_pass_direct = False
		bpy.context.scene.render.bake.use_pass_indirect = False
		bpy.context.scene.render.bake.use_pass_color = True
		bpy.context.scene.render.bake.use_selected_to_active = True
		bpy.ops.object.bake(type='DIFFUSE')

		#Delete Bake Plane
		bpy.ops.object.select_all(action='DESELECT')
		bake_plane.select_set(True)
		bpy.ops.object.delete()
		ob.select_set(True)
		bpy.context.view_layer.objects.active = ob

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

			if bpy.context.space_data.mode != 'UV':
				bpy.context.space_data.mode = 'UV'
			
			bpy.ops.uv.select_all(action='SELECT')
			bpy.ops.uv.snap_cursor(target='SELECTED')

			# get coord center poly
			x_loc = bpy.context.area.spaces[0].cursor_location[0]
			y_loc = bpy.context.area.spaces[0].cursor_location[1]
			mat_coll_list = [mat_name, x_loc, y_loc]
			mat_coll_array.append(mat_coll_list)
			
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.area.type = 'VIEW_3D'

		for r in current_objects:   
			bpy.ops.object.select_all(action='DESELECT')
			r.select_set(True)
			# unwrap selected objects and add palette texture
			bpy.context.view_layer.objects.active = r	
			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.uv.smart_project(angle_limit=89, island_margin=0.01, user_area_weight=0, use_aspect=True)
			
			bpy.ops.mesh.select_all(action='DESELECT')
			# select poly with 1 material 
			r_mats = r.data.materials
			r_mats_len = len(r_mats)
			r_mat_index = 0

			for r_mat_index in range(r_mats_len):
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.context.object.active_material_index = r_mat_index
				r_mat_name = bpy.context.object.data.materials[r_mat_index].name
				bpy.ops.object.material_slot_select()
				bpy.ops.uv.select_all(action = 'SELECT')
				
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
				bpy.ops.transform.resize(value=(0, 0, 1), orient_type ='GLOBAL', orient_matrix_type='GLOBAL', \
						 mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, \
						 					use_proportional_connected=False, use_proportional_projected=False)
						  
			bpy.ops.object.mode_set(mode = 'OBJECT')

		# Delete Palette Plane
		bpy.ops.object.select_all(action='DESELECT')
		ob.select_set(True)
		bpy.ops.object.delete()
		
		# Select again objects
		for j in start_selected_obj:
			j.select_set(True)	

		bpy.context.view_layer.objects.active = start_active_obj	
			
		bpy.context.area.type = current_area

		if flag_exist_area == True:
			bpy.context.screen.areas[IE_area].type = 'IMAGE_EDITOR'

		#Connect Texture to Shader Base Color and rename
		palette_bake_mat.node_tree.links.new(TexNode.outputs['Color'], palette_bake_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
		palette_bake_mat.name = 'Palette_' + add_name_palette

		#Delete Temp Material
		bpy.data.materials.remove(bpy.data.materials['Palette_background'])

		return {'FINISHED'}

#-------------------------------------------------------
#Open Export Directory
class OpenExportDir(Operator):
	"""Open Export Directory in OS"""
	bl_idname = "object.open_export_dir"
	bl_label = "Open Export Directory in OS"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act

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
			if x.type == 'MESH':
				if len(x.data.uv_layers) > 0:
					if uv_index < len(x.data.uv_layers):
						x.data.uv_layers[uv_index].name = uv_name	
		return {'FINISHED'}

#-------------------------------------------------------
#Rename bones
class RenameBones(Operator):
	"""Rename bones"""
	bl_idname = "object.rename_bones"
	bl_label = "Rename bones"
	bl_options = {'REGISTER', 'UNDO'}
	
	Value: StringProperty()

	def execute(self, context):
		selected_bones = bpy.context.selected_bones	
		for x in selected_bones:
			x.name = x.name + self.Value

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
			if act.nums_method == '0' or act.nums_method == '3' or act.nums_method == '4':
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
					
			if act.nums_method == '4':
				bpy.data.objects[objects_list[y][0]].name = ob_name;
			else:
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
#Assign Materials in MultiEdit
class AssignMultieditMaterials(Operator):
	"""Assign Materials for some objects in MultiEdit Mode"""
	bl_idname = "object.assign_multiedit_materials"
	bl_label = "Assign Materials for some objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		active_mat = bpy.context.active_object.active_material.name_full

		bpy.ops.object.mode_set(mode = 'OBJECT')

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				append_mat = True
				mat_index = 0		
				for m in range(0, len(x.data.materials)):
					if not x.data.materials[m] == None:
						if x.data.materials[m].name_full == active_mat:
							append_mat = False
				if append_mat:
					x.data.materials.append(bpy.data.materials[active_mat])
				for n in range(0, len(x.data.materials)):
					if not x.data.materials[n] == None:
						if x.data.materials[n].name_full == active_mat:
							mat_index = n

				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.context.active_object.active_material_index = mat_index
				bpy.ops.object.material_slot_assign()
				bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj
		bpy.ops.object.mode_set(mode = 'EDIT')

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
			
			elif context.mode == 'EDIT_ARMATURE':
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				row.operator("object.rename_bones", text="Add .L").Value=".L"
				split = split.split()
				c = split.column()
				row.operator("object.rename_bones", text="Add .R").Value=".R"
				#----

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
				
				layout.prop(act, "apply_rot", text="Rotation")

				if act.apply_rot and act.fbx_export_mode == '2':
						#Split row
						row = layout.row()
						c = row.column()
						row = c.row()
						split = row.split(factor=0.05, align=True)
						c = split.column()
						c.label(text="")
						split = split.split()
						c = split.column()
						c.prop(act, "apply_rot_rotated")
						#----

				layout.prop(act, "apply_scale", text="Scale")
				
				if act.fbx_export_mode == '0' or act.fbx_export_mode == '2':
					layout.prop(act, "apply_loc", text="Location")
				
				row = layout.row()
				layout.prop(act, "delete_mats_before_export", text="Delete All Materials")

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

				if len(act.export_dir) > 0:
					row = layout.row()
					row.operator("object.open_export_dir", text="Open Export Directory")
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
				row.operator("object.palette_creator", text="Create Palette Texture")
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
		
def Material_Menu_Panel(self, context):
	if context.object is not None:
			if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
				layout = self.layout
				row = layout.row()		
				row.operator("object.assign_multiedit_materials", text="Active Material -> Selected")

class ACTAddonProps(PropertyGroup):
	old_text: StringProperty(
		name="",
		description="Text for search",
		default="")
	
	new_text: StringProperty(
		name="",
		description="Text for replace",
		default="")

	export_dir: StringProperty(
		name="",
		description="Export Directory",
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
	
	nums_method_items = (('0','Along X',''),('1','Along Y',''), ('2','Along Z',''), ('3','Simple',''), ('4','None',''))
	nums_method: EnumProperty(name="", items = nums_method_items)
	
	nums_format_items = (('0','_X, _XX, _XXX',''),('1','_0X, _XX, _XXX',''), ('2','_00X, _0XX, _XXX',''))
	nums_format: EnumProperty(name="", items = nums_format_items)
	
	axis_items = (('0','X',''),('1','Y',''), ('2','Z',''))
	axis_select: EnumProperty(name="Axis", items = axis_items)
	
	rename_menu_items = (('0','Add Pre/Postfix',''),('1','Replace',''), ('2','New name',''))
	rename_select: EnumProperty(name="", items = rename_menu_items)
	
	orientation_menu_items = (('0','GLOBAL',''),('1','LOCAL',''))
	orientation_select: EnumProperty(name="", items = orientation_menu_items)

	fbx_export_mode_menu_items = (('0','1 Obj->1 FBX',''),('1','All->One FBX',''),('2','By Parent',''),('3','By Collection',''))
	fbx_export_mode: EnumProperty(name="", items = fbx_export_mode_menu_items)
	
	uv_move_factor_items = (('1','2',''),('2','4',''), ('3','8',''), ('4','16',''), ('5','32',''))
	uv_move_factor: EnumProperty(name="", items = uv_move_factor_items, default = '3')
	
	apply_rot: BoolProperty(
		name="Apply Rotation",
		description="Apply Rotation for Exported Models",
		default = True)

	apply_rot_rotated: BoolProperty(
		name="Apply for Rotated Objects",
		description="Apply Rotation for Objects with not 0,0,0 rotation",
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

	delete_mats_before_export: BoolProperty(
		name="Delete Materials",
		description="Delete Materials before Export",
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
	OpenExportDir,
	PaletteCreate,
	ClearNormals,
	CalcNormals,
	ImportFBXOBJ,
	RenameUV,
	RenameBones,
	Numbering,
	UVremove,
	AlignMin,
	AlignMax,
	AlignCur,
	AlignCo,
	SetOriginToSelect,
	ObjNameToMeshName,
	ClearVertexColors,
	UV_Mover,
	AssignMultieditMaterials,
)	  
	
#-------------------------------------------------------		
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
		
	bpy.types.Scene.act = PointerProperty(type=ACTAddonProps)

	bpy.types.CYCLES_PT_context_material.prepend(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.prepend(Material_Menu_Panel)
	
def unregister():
	bpy.types.CYCLES_PT_context_material.remove(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.remove(Material_Menu_Panel)

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		
	del bpy.types.Scene.act

if __name__ == "__main__":
	register()
