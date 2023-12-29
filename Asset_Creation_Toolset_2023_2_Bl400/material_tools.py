import bpy
import random
import colorsys
import os
import subprocess
from . import utils
from datetime import datetime

# Palette texture creator
class Palette_Create(bpy.types.Operator):
	"""Palette Texture Creator"""
	bl_idname = "object.palette_creator"
	bl_label = "Palette Texture Creator"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		act.export_dir = ""
		path = ""
		incorrect_names = []
		palette_back_color = (0.5, 0.5, 0.5, 1)
		# Bake PBR Palette Texture Set (Albedo, Roughness, Metallic, Opacity, Emission) or only Albedo
		pbr_mode = act.pbr_workflow
		# Store temporary data for cleanUp
		temp_meshes = []

		# Check blend file is saved and get export folder path
		if len(bpy.data.filepath) == 0 and not act.custom_save_path:
			self.report({'INFO'}, 'Blend file is not saved. Try use Custom Save Path')
			return {'CANCELLED'}

		if len(bpy.data.filepath) > 0 or act.custom_save_path:
			if len(bpy.data.filepath) > 0:
				path = bpy.path.abspath('//Textures/')
			
			if act.custom_save_path:
				if len(act.save_path) == 0:
					self.report({'INFO'}, 'Save Path can\'t be empty')
					return {'CANCELLED'}

				if not os.path.exists(os.path.realpath(bpy.path.abspath(act.save_path))):
					self.report({'INFO'}, 'Directory for saving not exist')
					return {'CANCELLED'}
				else:
					path = os.path.realpath(bpy.path.abspath(act.save_path)) + '/'
		
			# Create export folder
			if not os.path.exists(path):
				os.makedirs(path)

		# Check Render Engine (Save current and switch to Cycles render engine)
		current_engine = bpy.context.scene.render.engine
		bpy.context.scene.render.engine = 'CYCLES'

		# Check opened UV Editor window
		ie_areas = []
		flag_exist_area = False
		for area in range(len(bpy.context.screen.areas)):
			if bpy.context.screen.areas[area].type == 'IMAGE_EDITOR' and bpy.context.screen.areas[area].ui_type == 'UV':
				ie_areas.append(area)
				flag_exist_area = True

		# Switch UV Editors to Image Editors
		for ie_area in ie_areas:
			bpy.context.screen.areas[ie_area].ui_type = 'IMAGE_EDITOR'

		# Get selected MESH objects and get active object's name
		start_active_obj = bpy.context.active_object
		start_selected_obj = bpy.context.selected_objects
		current_objects = []

		for selected_mesh in bpy.context.selected_objects:
			if selected_mesh.type == 'MESH' and len(selected_mesh.data.materials) > 0:
				current_objects.append(selected_mesh)
				# Remove empty material slots
				for q in reversed(range(len(selected_mesh.data.materials))):
					if selected_mesh.data.materials[q] is None:
						bpy.context.object.active_material_index = q
						# Unlink empty slots
						selected_mesh.data.materials.pop(index=q)
						
		prefilter_add_name_palette = bpy.context.active_object.name

		# Replace invalid chars
		add_name_palette = utils.Prefilter_Export_Name(prefilter_add_name_palette)

		if add_name_palette != prefilter_add_name_palette:
			incorrect_names.append(prefilter_add_name_palette)

		# Set tool setting for UV Editor
		bpy.context.scene.tool_settings.use_uv_select_sync = False
		bpy.context.scene.tool_settings.uv_select_mode = 'FACE'

		# Get materials from selected objects
		me = []
		for x in current_objects:
			me += x.data.materials

		# Check exist material Palette_background
		flag_exist_mat = False
		for a in range(len(bpy.data.materials)):
			if bpy.data.materials[a].name == 'Palette_background':
				flag_exist_mat = True
				palette_back_color = bpy.data.materials[a]

		# Create palette background material
		if not flag_exist_mat:
			palette_back_color = bpy.data.materials.new('Palette_background')
			palette_back_color.diffuse_color = 0.8, 0.8, 0.8, 1.0

		# Check exist palette plane (for baking)
		flag_exist_obj = False
		for o in range(len(bpy.data.objects)):
			if bpy.data.objects[o].name == ('Palette_' + add_name_palette):
				flag_exist_obj = True

		# Delete plane
		if flag_exist_obj:
			bpy.ops.object.select_all(action='DESELECT')
			bpy.data.objects['Palette_' + add_name_palette].select = True
			bpy.ops.object.delete()

		# Create new plane
		bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
		pln = bpy.context.object
		pln.name = 'Palette_' + add_name_palette

		temp_meshes.append(pln.data.name)

		# Add palette background material to palette plane
		pln.data.materials.append(palette_back_color)

		# Names for textures
		albedo_texture_name = 'Palette_' + add_name_palette + '_Albedo'
		roughness_texture_name = 'Palette_' + add_name_palette + '_Roughness'
		metallic_texture_name = 'Palette_' + add_name_palette + '_Metallic'
		opacity_texture_name = 'Palette_' + add_name_palette + '_Opacity'
		emission_texture_name = 'Palette_' + add_name_palette + '_Emission'

		# Add materials to palette plane (only unique)
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
					
			if not flag_non:
				pln.data.materials.append(me[i])

		# Compute number of subdivide palette plane from number of materials
		palette_mat = pln.data.materials
		palette_mat_len = len(palette_mat)
		# Number of materials without background material
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

		# Subdivide palette plane
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

		for n in range(number_of_subdiv):
			bpy.ops.mesh.subdivide(smoothness=0)

		# Create texture and unwrap
		bpy.ops.mesh.select_all(action='SELECT')

		# Check exist albedo texture image
		flag_exist_texture_albedo = False
		for t in range(len(bpy.data.images)):
			if bpy.data.images[t].name == albedo_texture_name:
				flag_exist_texture_albedo = True

		# Create or not albedo texture
		if not flag_exist_texture_albedo:
			bpy.ops.image.new(name=albedo_texture_name, width=32, height=32)

		# Check exist of additional textures (if PBR workflow)
		if pbr_mode:
			# Roughness baking texture
			# Check exist roughness texture image
			flag_exist_texture_roughness = False
			for t in range(len(bpy.data.images)):
				if bpy.data.images[t].name == roughness_texture_name:
					flag_exist_texture_roughness = True

			# create or not roughness texture
			if not flag_exist_texture_roughness:
				bpy.ops.image.new(name=roughness_texture_name, width=32, height=32)
				bpy.data.images[roughness_texture_name].colorspace_settings.name = 'Non-Color'

			# Metallic baking texture
			# Check exist metallic texture image
			flag_exist_texture_metallic = False
			for t in range(len(bpy.data.images)):
				if bpy.data.images[t].name == metallic_texture_name:
					flag_exist_texture_metallic = True

			# Create or not metallic texture
			if not flag_exist_texture_metallic:
				bpy.ops.image.new(name=metallic_texture_name, width=32, height=32)
				bpy.data.images[metallic_texture_name].colorspace_settings.name = 'Non-Color'

			# Opacity baking texture
			# Check exist opacity texture image
			flag_exist_texture_opacity = False
			for t in range(len(bpy.data.images)):
				if bpy.data.images[t].name == opacity_texture_name:
					flag_exist_texture_opacity = True

			# Create or not opacity texture
			if not flag_exist_texture_opacity:
				bpy.ops.image.new(name=opacity_texture_name, width=32, height=32)
				bpy.data.images[opacity_texture_name].colorspace_settings.name = 'Non-Color'

			# Emission baking texture
			# Check exist emission texture image
			flag_exist_texture_emission = False
			for t in range(len(bpy.data.images)):
				if bpy.data.images[t].name == emission_texture_name:
					flag_exist_texture_emission = True

			# Create or not emission texture
			if not flag_exist_texture_emission:
				bpy.ops.image.new(name=emission_texture_name, width=32, height=32)

		# Set materials to plane's polygons (one material to one quad polygon)
		bpy.ops.object.mode_set(mode='OBJECT')
		ob = bpy.context.object

		for poly in ob.data.polygons:   
			if (poly.index + 1) < palette_mat_len:
				poly.material_index = poly.index + 1

		# Baking Albedo
		# ob is plane with materials (source)
		# Create another plane (destination for baking)
		bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
		bake_plane = bpy.context.object
		bake_plane.name = 'Palette_Bake_Plane'
		temp_meshes.append(bake_plane.data.name)
		bpy.ops.object.mode_set(mode='OBJECT')

		# Check exist material for baking
		for material in bpy.data.materials:
			if material.name == 'Palette_Bake':
				bpy.data.materials.remove(material)

		# Remove old material and create new
		palette_bake_mat = bpy.data.materials.new('Palette_Bake')

		# Setup material's nodes for baking
		bake_plane.data.materials.append(palette_bake_mat)
		palette_bake_mat.use_nodes = True
		nodes = palette_bake_mat.node_tree.nodes
		tex_node = nodes.new('ShaderNodeTexImage')
		tex_node.location = (-500, 500)
		tex_node.image = bpy.data.images[albedo_texture_name]

		# Save metallic value for each material
		# And set metallic to zero for all materials on the plane
		materials_metallic = []

		for mat in palette_mat:
			try:
				materials_metallic.append(mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value)
				mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0
			except:
				materials_metallic.append(0)
				continue

		materials_roughness = []

		# Also save roughness value for each material on the plane
		if pbr_mode:
			for mat in palette_mat:
				try:
					materials_roughness.append(mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value)
				except:
					materials_roughness.append(1)
					continue

		# Bake Albedo
		ob.select_set(True)
		bpy.context.scene.cycles.bake_type = 'DIFFUSE'
		bpy.context.scene.render.bake.use_pass_direct = False
		bpy.context.scene.render.bake.use_pass_indirect = False
		bpy.context.scene.render.bake.use_pass_color = True
		bpy.context.scene.render.bake.use_selected_to_active = True
		bpy.ops.object.bake(type='DIFFUSE')

		if pbr_mode:
			# Bake Roughness
			tex_node.image = bpy.data.images[roughness_texture_name]
			bpy.context.scene.cycles.bake_type = 'ROUGHNESS'
			bpy.ops.object.bake(type='ROUGHNESS')

			# Bake Metallic
			# Replace Roughness values to Metallic values
			# Because Blender do not bake metallic  channel
			# And Bake Roughness (but this is Metallic)
			tex_node.image = bpy.data.images[metallic_texture_name]

			for index in range(palette_mat_len):
				try:
					palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = materials_metallic[index]
				except:
					continue

			bpy.ops.object.bake(type='ROUGHNESS')

			# Bake Opacity
			# Also copy Alpha channel to Roughness
			# And Bake Roughness (but this is Opacity)
			tex_node.image = bpy.data.images[opacity_texture_name]

			for index in range(palette_mat_len):
				try:
					palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = \
						palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value
				except:
					continue

			bpy.ops.object.bake(type='ROUGHNESS')

			# Bake Emission
			tex_node.image = bpy.data.images[emission_texture_name]
			bpy.context.scene.cycles.bake_type = 'EMIT'
			bpy.ops.object.bake(type='EMIT')

		# Revert materials Metallic and Roughness values
		for index in range(palette_mat_len):
			try:
				palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = materials_metallic[index]
				palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = materials_roughness[index]
			except:
				continue

		# Delete Bake Plane
		bpy.ops.object.select_all(action='DESELECT')
		bake_plane.select_set(True)
		bpy.ops.object.delete()
		ob.select_set(True)
		bpy.context.view_layer.objects.active = ob

		# Create collection materials with (mat_name, uv_x_mat, uv_y_mat)
		# This is UV coordinates for baked materials
		mat_coll_array = []
		collect_uv_mat = 1
		current_area = bpy.context.area.type

		for collect_uv_mat in range(palette_mat_len - 1):
			# Select polygon on plane with materials
			bpy.ops.object.mode_set(mode='EDIT')
			bpy.ops.mesh.reveal()
			bpy.ops.mesh.select_all(action='DESELECT')
			bpy.ops.object.mode_set(mode='OBJECT')
			ob.data.polygons[collect_uv_mat].select = True
			bpy.ops.object.mode_set(mode='EDIT')

			# get material name and index from selected quad polygon
			mat_index = ob.data.polygons[collect_uv_mat].material_index
			mat_name = ob.data.materials[mat_index].name

			# Switch active area to Image Editor
			bpy.context.area.type = 'IMAGE_EDITOR'

			# If Image Editor has Render Result, Clean it
			if bpy.context.area.spaces[0].image is not None:
				if bpy.context.area.spaces[0].image.name == 'Render Result':
					bpy.context.area.spaces[0].image = None

			# Switch Image Editor to UV Editor
			if bpy.context.space_data.mode != 'UV':
				bpy.context.space_data.mode = 'UV'

			# Select current polygon in UV Editor and place cursor to center of this polygon
			bpy.ops.uv.select_all(action='SELECT')
			bpy.ops.uv.snap_cursor(target='SELECTED')

			# Get coordinates of center of polygon
			x_loc = bpy.context.area.spaces[0].cursor_location[0]
			y_loc = bpy.context.area.spaces[0].cursor_location[1]

			# And save these coordinates as material's UV coordinates
			mat_coll_list = [mat_name, x_loc, y_loc]
			mat_coll_array.append(mat_coll_list)
			
		bpy.ops.object.mode_set(mode='OBJECT')

		# Switch active area to 3D View
		bpy.context.area.type = 'VIEW_3D'

		# Create UV and transform it for using one palette instead of many colored materials
		for r in current_objects:
			bpy.ops.object.select_all(action='DESELECT')
			r.select_set(True)
			# Smart unwrap selected objects and add palette texture
			bpy.context.view_layer.objects.active = r	
			bpy.ops.object.mode_set(mode='EDIT')
			bpy.ops.mesh.reveal()
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.uv.smart_project(angle_limit=89, island_margin=0.01)
			bpy.ops.mesh.select_all(action='DESELECT')

			# Select polygons with 1 material
			r_mats = r.data.materials
			r_mats_len = len(r_mats)

			for r_mat_index in range(r_mats_len):
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.context.object.active_material_index = r_mat_index
				r_mat_name = bpy.context.object.data.materials[r_mat_index].name
				bpy.ops.object.material_slot_select()
				bpy.ops.uv.select_all(action='SELECT')
				
				# get UV coordinates for material from collection
				r_mat_x = 0
				r_mat_y = 0

				for h in range(len(mat_coll_array)):
					if r_mat_name == mat_coll_array[h][0]:
						r_mat_x = mat_coll_array[h][1]
						r_mat_y = mat_coll_array[h][2]
				
				# Scale object UV (for polygons with current material) to same material on palette texture
				bpy.context.area.type = 'IMAGE_EDITOR'
				bpy.ops.uv.cursor_set(location=(r_mat_x, r_mat_y))
				bpy.context.space_data.pivot_point = 'CURSOR'
				bpy.ops.transform.resize(
					value=(0, 0, 1), orient_type ='GLOBAL', orient_matrix_type='GLOBAL',
					mirror=False, use_proportional_edit=False,
					proportional_edit_falloff='SMOOTH', proportional_size=1,
					use_proportional_connected=False, use_proportional_projected=False)

			bpy.ops.object.mode_set(mode='OBJECT')

		# Delete Palette Plane
		bpy.ops.object.select_all(action='DESELECT')
		ob.select_set(True)
		bpy.ops.object.delete()

		# Switch active area to UV Editor
		bpy.context.area.type = 'IMAGE_EDITOR'

		# Save Palette Images
		current_image = bpy.context.area.spaces[0].image
		bpy.context.area.spaces[0].image = bpy.data.images[albedo_texture_name]
		bpy.ops.image.save_as(
			save_as_render=False, filepath=str(path + albedo_texture_name + '.png'),
			relative_path=True, show_multiview=False, use_multiview=False)
		if pbr_mode:
			bpy.context.area.spaces[0].image = bpy.data.images[roughness_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + roughness_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			bpy.context.area.spaces[0].image = bpy.data.images[metallic_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + metallic_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			bpy.context.area.spaces[0].image = bpy.data.images[opacity_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + opacity_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			bpy.context.area.spaces[0].image = bpy.data.images[emission_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + emission_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
		bpy.context.area.spaces[0].image = current_image

		# Save textures export dir
		act.save_dir = path

		# Switch active area to 3D View
		bpy.context.area.type = 'VIEW_3D'

		# Select again objects
		for j in start_selected_obj:
			j.select_set(True)	

		# Restore objects selection and areas
		bpy.context.view_layer.objects.active = start_active_obj
		bpy.context.area.type = current_area

		if flag_exist_area:
			for ie_area in ie_areas:
				bpy.context.screen.areas[ie_area].ui_type = 'UV'

		# Check palette atlas material exist and remove
		for material in bpy.data.materials:
			if material.name_full == 'Palette_' + add_name_palette:
				bpy.data.materials.remove(material)

		# Create palette atlas material and setup nodes for all baked textures
		palette_mat = bpy.data.materials.new('Palette_' + add_name_palette)
		palette_mat.use_nodes = True
		palette_node_tree = palette_mat.node_tree
		palette_nodes = palette_node_tree.nodes
		# Albedo
		albedo_tex_node = palette_nodes.new('ShaderNodeTexImage')
		albedo_tex_node.location = (-500, 500)
		albedo_tex_node.image = bpy.data.images[albedo_texture_name]
		bpy.data.images[albedo_texture_name].colorspace_settings.name = 'sRGB'
		palette_node_tree.links.new(
			albedo_tex_node.outputs['Color'],
			palette_node_tree.nodes['Principled BSDF'].inputs['Base Color'])

		if act.pbr_workflow:
			# Metallic
			metallic_tex_node = palette_nodes.new('ShaderNodeTexImage')
			metallic_tex_node.location = (-800, 250)
			metallic_tex_node.image = bpy.data.images[metallic_texture_name]
			bpy.data.images[metallic_texture_name].colorspace_settings.name = 'Non-Color'
			palette_node_tree.links.new(
				metallic_tex_node.outputs['Color'],
				palette_node_tree.nodes['Principled BSDF'].inputs['Metallic'])

			# Roughness
			roughness_tex_node = palette_nodes.new('ShaderNodeTexImage')
			roughness_tex_node.location = (-500, 0)
			roughness_tex_node.image = bpy.data.images[roughness_texture_name]
			bpy.data.images[roughness_texture_name].colorspace_settings.name = 'Non-Color'
			palette_node_tree.links.new(
				roughness_tex_node.outputs['Color'],
				palette_node_tree.nodes['Principled BSDF'].inputs['Roughness'])

			# Emission
			emission_tex_node = palette_nodes.new('ShaderNodeTexImage')
			emission_tex_node.location = (-800, -350)
			emission_tex_node.image = bpy.data.images[emission_texture_name]
			bpy.data.images[emission_texture_name].colorspace_settings.name = 'sRGB'
			palette_node_tree.links.new(
				emission_tex_node.outputs['Color'],
				palette_node_tree.nodes['Principled BSDF'].inputs['Emission Color'])
			palette_node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 1

			# Opacity
			opacity_tex_node = palette_nodes.new('ShaderNodeTexImage')
			opacity_tex_node.location = (-500, -500)
			opacity_tex_node.image = bpy.data.images[opacity_texture_name]
			bpy.data.images[opacity_texture_name].colorspace_settings.name = 'Non-Color'
			palette_node_tree.links.new(
				opacity_tex_node.outputs['Color'],
				palette_node_tree.nodes['Principled BSDF'].inputs['Alpha'])

			# Alpha Clip
			palette_mat.blend_method = 'CLIP'
			palette_mat.shadow_method = 'CLIP'

		# Delete temp materials and cleanup
		bpy.data.materials.remove(bpy.data.materials['Palette_background'])

		for mesh_name in temp_meshes:
			bpy.data.meshes.remove(bpy.data.meshes[mesh_name])

		for material in bpy.data.materials:
			if material.name == 'Palette_Bake':
				bpy.data.materials.remove(material)

		# Restore render engine
		bpy.context.scene.render.engine = current_engine

		utils.Print_Execution_Time("Create Palette Texture", start_time)

		# Show message about incorrect names
		if len(incorrect_names) > 0:
			utils.Show_Message_Box("Psllete name has invalid characters. Some chars have been replaced", "Invalid Palette Name")

		return {'FINISHED'}


# Open textures export directory
class Open_Save_Dir(bpy.types.Operator):
	"""Open Save Directory in OS"""
	bl_idname = "object.open_save_dir"
	bl_label = "Open Save Directory in OS"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act

		# Try open export directory in OS
		if not os.path.exists(os.path.realpath(bpy.path.abspath(act.save_path))):
			act.save_dir = ""
			self.report({'INFO'}, 'Directory not exist')

			return {'CANCELLED'}

		if len(act.save_dir) > 0:
			try:
				os.startfile(act.save_dir)
			except:
				subprocess.Popen(['xdg-open', act.save_dir])
		else:
			self.report({'INFO'}, 'Create Palette\'s before')
			return {'FINISHED'}

		utils.Print_Execution_Time("Open Textures Export Directory", start_time)
		return {'FINISHED'}


# Assign materials in multiEdit
class Assign_Multiedit_Materials(bpy.types.Operator):
	"""Assign Materials for some objects in MultiEdit Mode"""
	bl_idname = "object.assign_multiedit_materials"
	bl_label = "Assign Materials for some objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		active_mat = bpy.context.active_object.active_material.name_full

		bpy.ops.object.mode_set(mode='OBJECT')

		# Added active material to all selected objects
		# If these objects don't have slot with this material
		# But have selected polygons
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				append_mat = True
				mat_index = 0		
				for m in range(0, len(x.data.materials)):
					if not x.data.materials[m] is None:
						if x.data.materials[m].name_full == active_mat:
							append_mat = False

				selected_poly = False
				for p in x.data.polygons:
					if p.select:
						selected_poly = True

				if append_mat and selected_poly:
					x.data.materials.append(bpy.data.materials[active_mat])
				for n in range(0, len(x.data.materials)):
					if not x.data.materials[n] is None:
						if x.data.materials[n].name_full == active_mat:
							mat_index = n

				# Set active material for current object and assign to selected polygons
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.context.active_object.active_material_index = mat_index
				bpy.ops.object.material_slot_assign()
				bpy.ops.object.mode_set(mode='OBJECT')

		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj
		bpy.ops.object.mode_set(mode='EDIT')

		utils.Print_Execution_Time("Assign Material in Multi-Edit Mode", start_time)
		return {'FINISHED'}


# Clear vertex colors
class Clear_Vertex_Colors(bpy.types.Operator):
	"""Clear Vertex Colors"""
	bl_idname = "object.clear_vc"
	bl_label = "# Clear Vertex Colors"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		start_time = datetime.now()
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		
		for x in current_selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				for color_attribute in reversed(x.data.color_attributes):
					bpy.ops.geometry.color_attribute_remove()
				
		for x in current_selected_obj:
			x.select_set(True)
		bpy.context.view_layer.objects.active = current_active_obj

		utils.Print_Execution_Time("Clear Vertex Colors", start_time)
		return {'FINISHED'} 			


# Material color to viewport color
class Material_To_Viewport(bpy.types.Operator):
	"""Material Color to Viewport Color"""
	bl_idname = "object.material_to_viewport"
	bl_label = "Material Color to Viewport Color"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				for mat in x.data.materials:
					try:
						mat.diffuse_color = mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value
					except:
						print("Can\'t change viewport material color")
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Material Color to Viewport", start_time)
		return {'FINISHED'}


# Random material viewport color
class Random_Viewport_Color(bpy.types.Operator):
	"""Random Material Viewport Color"""
	bl_idname = "object.random_viewport_color"
	bl_label = "Random Material Viewport Color"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x

			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				for mat in x.data.materials:
					random_hue = random.randrange(0, 10, 1)/10
					random_value = random.randrange(2, 10, 1)/10
					random_saturation = random.randrange(7, 10, 1)/10
					color = colorsys.hsv_to_rgb(random_hue, random_saturation, random_value)
					color4 = (color[0], color[1], color[2], 1)
					try:
						mat.diffuse_color = color4
					except:
						print("Can\'t change viewport material color")
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Random Color to Viewport", start_time)
		return {'FINISHED'}


# Clear viewport color
class Clear_Viewport_Color(bpy.types.Operator):
	"""Clear Viewport Color"""
	bl_idname = "object.clear_viewport_color"
	bl_label = "Clear Viewport Color"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x

			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				for mat in x.data.materials:
					color = colorsys.hsv_to_rgb(0, 0, 0.906)
					color4 = (color[0], color[1], color[2], 1)
					try:
						mat.diffuse_color = color4
					except:
						print("Can\'t change viewport material color")
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Clear Viewport Color", start_time)
		return {'FINISHED'}


# Delete unused materials
class Delete_Unused_Materials(bpy.types.Operator):
	"""Delete from Objects Unused Materials and Slots"""
	bl_idname = "object.delete_unused_materials"
	bl_label = "Delete Unused Materials"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		# Delete Unused Materials
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x

			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				bpy.ops.object.material_slot_remove_unused()
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Delete Unused Materials", start_time)
		return {'FINISHED'}


# Select texture in UV Editor from active material (See Select_Texture_Menu)
class Texture_From_Active_Material(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "object.texture_from_material"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}
	texture_name: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		for area in bpy.context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				area.spaces[0].image = bpy.data.images[self.texture_name]

		utils.Print_Execution_Time("Select Texture in UV Editor", start_time)
		return {'FINISHED'}		


# Menu for select texture In UV Editor from active material
class Select_Texture_Menu(bpy.types.Menu):
	bl_idname = "OBJECT_MT_select_texture_menu"
	bl_label = "Select Texture"

	def draw(self, context):
		layout = self.layout
		texture_list = []

		# If now window has Image Editor area
		has_opened_image_editor = False
		for area in bpy.context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				has_opened_image_editor = True

		if has_opened_image_editor:
			# If active object is mesh and has material slots
			if bpy.context.active_object.type == 'MESH':
				if len(bpy.context.active_object.data.materials) > 0:
					has_textures = False

					# Collect all textures from active material to list
					for node in bpy.context.active_object.active_material.node_tree.nodes:
						if node.type == 'TEX_IMAGE':
							texture_name = node.image.name_full
							texture_in_list = False
							for texture in texture_list:
								if texture_name == texture:
									texture_in_list = True

							if not texture_in_list:
								texture_list.append(texture_name)
							has_textures = True
					
					if not has_textures:
						layout.label(text="Material has not textures")	
				else:
					layout.label(text="Mesh has not materials")
			else:
				layout.label(text="Object is not mesh")
		else:
			layout.label(text="Opened UV Editor not found")

		for texture in texture_list:
			layout.operator("object.texture_from_material", text=texture).texture_name = texture


# Call menu for select texture In UV Editor from active material
class Call_Select_Texture_Menu_View3D(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "view3d.call_select_texture_menu"
	bl_label = "Select Texture In 3D View From Active Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.wm.call_menu(name="OBJECT_MT_select_texture_menu")
		
		return {'FINISHED'}	


#  Call menu for select texture in UV Editor from active material
class Call_Select_Texture_Menu_Image_Editor(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "image.call_select_texture_menu"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.wm.call_menu(name="OBJECT_MT_select_texture_menu")
		
		return {'FINISHED'}	


# Material tools UI panel in 3D View
class VIEW3D_PT_Material_Tools_Panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and (context.mode == 'OBJECT' or context.mode == 'EDIT_MESH')) and preferences.material_enable

	def draw(self, context):
		act = bpy.context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				box = layout.box()
				row = box.row()
				row.operator("object.material_to_viewport", text="Material -> Viewport Color")

				row = box.row()
				row.operator("object.random_viewport_color", text="Random Material Viewport Color")

				row = box.row()
				row.operator("object.clear_viewport_color", text="Clear Viewport Color")
				
				row = layout.row()
				row.operator("object.clear_vc", text="Clear Vertex Colors")

				row = layout.row()	
				row.operator("object.delete_unused_materials", text="Delete Unused Materials")

				box = layout.box()
				row = box.row()
				row.prop(act, "pbr_workflow", text="PBR_Workflow")
				row = box.row()
				row.prop(act, "custom_save_path", text="Custom Save Path")
				if act.custom_save_path:
					row = box.row(align=True)
					row.label(text="Save Path:")
					row.prop(act, "save_path")
				row = box.row()
				row.operator("object.palette_creator", text="Create Palette Texture")
				if len(act.save_dir) > 0:
					row = box.row()
					row.operator("object.open_save_dir", text="Open Save Directory")

			row = layout.row()
			row.operator("view3d.call_select_texture_menu", text="Open Texture in UV Editor")


# Material tools UI panel in UV Editor
class UV_PT_Material_UV_Tools_Panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and (context.mode == 'OBJECT' or context.mode == 'EDIT_MESH')) and preferences.uv_material_enable

	def draw(self, context):
		act = bpy.context.scene.act
		
		layout = self.layout
		if context.object is not None:
			row = layout.row()
			row.operator("image.call_select_texture_menu", text="Open Texture in UV Editor")


# Material assign UI panel
def Material_Menu_Panel(self, context):
	preferences = bpy.context.preferences.addons[__package__].preferences
	if context.object is not None and preferences.material_properties_enable:
		if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
			layout = self.layout
			row = layout.row()		
			row.operator("object.assign_multiedit_materials", text="Active Material -> Selected")


classes = (
	Palette_Create,
	Open_Save_Dir,
	Assign_Multiedit_Materials,
	Clear_Vertex_Colors,
	Material_To_Viewport,
	Clear_Viewport_Color,
	Random_Viewport_Color,
	Delete_Unused_Materials,
	Texture_From_Active_Material,
	Select_Texture_Menu,
	Call_Select_Texture_Menu_View3D,
	Call_Select_Texture_Menu_Image_Editor,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.CYCLES_PT_context_material.prepend(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.prepend(Material_Menu_Panel)


def unregister():
	try:
		bpy.types.CYCLES_PT_context_material.remove(Material_Menu_Panel)
	except AttributeError as err:
		print(err)

	try:
		bpy.types.EEVEE_MATERIAL_PT_context_material.remove(Material_Menu_Panel)
	except AttributeError as err:
		print(err)
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		