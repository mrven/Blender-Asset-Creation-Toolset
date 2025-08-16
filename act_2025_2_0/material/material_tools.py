import bpy
import random
import colorsys
import os
import subprocess
from datetime import datetime

from ..common import utils as common_utils
from . import utils

package_name = __package__.split('.')[0]

# Palette texture creator
class CreatePalette(bpy.types.Operator):
	"""Create Palette Texture"""
	bl_idname = "act.create_palette"
	bl_label = "Create Palette Texture"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		act.export_dir = ""
		path = ""
		incorrect_names = []
		# Bake PBR Palette Texture Set (Albedo, Roughness, Metallic, Opacity, Emission) or only Albedo
		pbr_mode = act.pbr_workflow
		# Store temporary data for cleanUp
		temp_meshes = []

		# Check blend file is saved and get export folder path
		if len(bpy.data.filepath) == 0 and not act.custom_save_path:
			common_utils.show_message_box('Blend file is not saved. Try use Custom Save Path',
									'Saving Error',
									'ERROR')
			return {'CANCELLED'}

		if len(bpy.data.filepath) > 0 or act.custom_save_path:
			if len(bpy.data.filepath) > 0:
				path = bpy.path.abspath('//Textures/')

			if act.custom_save_path:
				if len(act.save_path) == 0:
					common_utils.show_message_box('Save Path can\'t be empty',
										   'Saving Error',
										   'ERROR')
					return {'CANCELLED'}

				if not os.path.exists(os.path.realpath(bpy.path.abspath(act.save_path))):
					common_utils.show_message_box('Directory for saving not exist',
										   'Saving Error',
										   'ERROR')
					return {'CANCELLED'}
				else:
					path = os.path.realpath(bpy.path.abspath(act.save_path)) + '/'

			# Create export folder
			if not os.path.exists(path):
				os.makedirs(path)

		# Check Render Engine (Save current and switch to Cycles render engine)
		current_engine = context.scene.render.engine
		context.scene.render.engine = 'CYCLES'

		# Check opened UV Editor window
		ie_areas = []
		flag_exist_area = False
		for area in range(len(context.screen.areas)):
			if context.screen.areas[area].type == 'IMAGE_EDITOR' and context.screen.areas[area].ui_type == 'UV':
				ie_areas.append(area)
				flag_exist_area = True

		# Switch UV Editors to Image Editors
		for ie_area in ie_areas:
			context.screen.areas[ie_area].ui_type = 'IMAGE_EDITOR'

		# Get selected MESH objects and get active object's name
		start_active_obj = context.active_object
		start_selected_obj = context.selected_objects
		current_objects = []

		for selected_mesh in context.selected_objects:
			if selected_mesh.type == 'MESH' and len(selected_mesh.data.materials) > 0:
				current_objects.append(selected_mesh)
				# Remove empty material slots
				for q in reversed(range(len(selected_mesh.data.materials))):
					if selected_mesh.data.materials[q] is None:
						context.object.active_material_index = q
						# Unlink empty slots
						selected_mesh.data.materials.pop(index=q)

		prefilter_add_name_palette = context.active_object.name

		# Replace invalid chars
		add_name_palette = common_utils.prefilter_export_name(prefilter_add_name_palette)

		if add_name_palette != prefilter_add_name_palette:
			incorrect_names.append(prefilter_add_name_palette)

		# Set tool setting for UV Editor
		context.scene.tool_settings.use_uv_select_sync = False
		context.scene.tool_settings.uv_select_mode = 'FACE'

		# Get materials from selected objects
		me = []
		for x in current_objects:
			me += x.data.materials

		palette_back_material = None

		# Check exist material Palette_background
		flag_exist_mat = False
		for a in range(len(bpy.data.materials)):
			if bpy.data.materials[a].name == 'Palette_background':
				flag_exist_mat = True
				palette_back_material = bpy.data.materials[a]

		# Create palette background material
		if not flag_exist_mat:
			palette_back_material = bpy.data.materials.new('Palette_background')
			palette_back_material.diffuse_color = 0.8, 0.8, 0.8, 1.0

		# Check exist palette plane (for baking)
		flag_exist_obj = False
		plane_obj = None
		for o in bpy.data.objects:
			if o.name == ('Palette_' + add_name_palette):
				flag_exist_obj = True
				plane_obj = o

		# Delete plane
		if flag_exist_obj and plane_obj:
			bpy.ops.object.select_all(action='DESELECT')
			plane_obj.select = True
			bpy.ops.object.delete()

		# Create new plane
		bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
		pln = context.object
		pln.name = 'Palette_' + add_name_palette

		temp_meshes.append(pln.data)

		# Add palette background material to palette plane
		pln.data.materials.append(palette_back_material)

		# Names for textures
		albedo_texture_name = 'Palette_' + add_name_palette + '_Albedo'
		roughness_texture_name = 'Palette_' + add_name_palette + '_Roughness'
		metallic_texture_name = 'Palette_' + add_name_palette + '_Metallic'
		opacity_texture_name = 'Palette_' + add_name_palette + '_Opacity'
		emission_texture_name = 'Palette_' + add_name_palette + '_Emission'

		# Add materials to palette plane (only unique)
		mat_offset = len(me)
		for i in range(mat_offset):
			flag_non = False
			palette_mat = pln.data.materials
			palette_mat_len = len(palette_mat)

			for j in range(palette_mat_len):
				if palette_mat[j] == me[i]:
					flag_non = True

			if not flag_non:
				pln.data.materials.append(me[i])

		# Compute number of subdivide palette plane from number of materials
		palette_mat = pln.data.materials
		palette_mat_len = len(palette_mat)
		# Number of materials without background material
		palette_mat_wo_bg = palette_mat_len - 1
		number_of_subdivision = 0

		if 1 < palette_mat_wo_bg <= 4:
			number_of_subdivision = 1

		if 4 < palette_mat_wo_bg <= 16:
			number_of_subdivision = 2

		if 16 < palette_mat_wo_bg <= 64:
			number_of_subdivision = 3

		if 64 < palette_mat_wo_bg <= 256:
			number_of_subdivision = 4

		# Subdivide palette plane
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

		for n in range(number_of_subdivision):
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
		ob = context.object

		for poly in ob.data.polygons:
			if (poly.index + 1) < palette_mat_len:
				poly.material_index = poly.index + 1

		# Baking Albedo
		# ob is plane with materials (source)
		# Create another plane (destination for baking)
		bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
		bake_plane = context.object
		bake_plane.name = 'Palette_Bake_Plane'
		temp_meshes.append(bake_plane.data)
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
		context.scene.cycles.bake_type = 'DIFFUSE'
		context.scene.render.bake.use_pass_direct = False
		context.scene.render.bake.use_pass_indirect = False
		context.scene.render.bake.use_pass_color = True
		context.scene.render.bake.use_selected_to_active = True
		bpy.ops.object.bake(type='DIFFUSE')

		if pbr_mode:
			# Bake Roughness
			tex_node.image = bpy.data.images[roughness_texture_name]
			context.scene.cycles.bake_type = 'ROUGHNESS'
			bpy.ops.object.bake(type='ROUGHNESS')

			# Bake Metallic
			# Replace Roughness values to Metallic values
			# Because Blender do not bake metallic  channel
			# And Bake Roughness (but this is Metallic)
			tex_node.image = bpy.data.images[metallic_texture_name]

			for index in range(palette_mat_len):
				try:
					palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = \
					materials_metallic[index]
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
			context.scene.cycles.bake_type = 'EMIT'
			bpy.ops.object.bake(type='EMIT')

		# Revert materials Metallic and Roughness values
		for index in range(palette_mat_len):
			try:
				palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = \
				materials_metallic[index]
				palette_mat[index].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = \
				materials_roughness[index]
			except:
				continue

		# Delete Bake Plane
		bpy.ops.object.select_all(action='DESELECT')
		bake_plane.select_set(True)
		bpy.ops.object.delete()
		ob.select_set(True)
		context.view_layer.objects.active = ob

		# Create collection materials with (mat_name, uv_x_mat, uv_y_mat)
		# This is UV coordinates for baked materials
		mat_coll_array = []
		current_area = context.area.type

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
			context.area.type = 'IMAGE_EDITOR'

			# If Image Editor has Render Result, Clean it
			if context.area.spaces[0].image is not None:
				if context.area.spaces[0].image.name == 'Render Result':
					context.area.spaces[0].image = None

			# Switch Image Editor to UV Editor
			if context.space_data.mode != 'UV':
				context.space_data.mode = 'UV'

			# Select current polygon in UV Editor and place cursor to center of this polygon
			bpy.ops.uv.select_all(action='SELECT')
			bpy.ops.uv.snap_cursor(target='SELECTED')

			# Get coordinates of center of polygon
			x_loc = context.area.spaces[0].cursor_location[0]
			y_loc = context.area.spaces[0].cursor_location[1]

			# And save these coordinates as material's UV coordinates
			mat_coll_list = [mat_name, x_loc, y_loc]
			mat_coll_array.append(mat_coll_list)

		bpy.ops.object.mode_set(mode='OBJECT')

		# Switch active area to 3D View
		context.area.type = 'VIEW_3D'

		# Create UV and transform it for using one palette instead of many colored materials
		for r in current_objects:
			bpy.ops.object.select_all(action='DESELECT')
			r.select_set(True)
			# Smart unwrap selected objects and add palette texture
			context.view_layer.objects.active = r
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
				context.object.active_material_index = r_mat_index
				r_mat_name = context.object.data.materials[r_mat_index].name
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
				context.area.type = 'IMAGE_EDITOR'
				bpy.ops.uv.cursor_set(location=(r_mat_x, r_mat_y))
				context.space_data.pivot_point = 'CURSOR'
				bpy.ops.transform.resize(
					value=(0, 0, 1), orient_type='GLOBAL', orient_matrix_type='GLOBAL',
					mirror=False, use_proportional_edit=False,
					proportional_edit_falloff='SMOOTH', proportional_size=1,
					use_proportional_connected=False, use_proportional_projected=False)

			bpy.ops.object.mode_set(mode='OBJECT')

		# Delete Palette Plane
		bpy.ops.object.select_all(action='DESELECT')
		ob.select_set(True)
		bpy.ops.object.delete()

		# Switch active area to UV Editor
		context.area.type = 'IMAGE_EDITOR'

		# Save Palette Images
		current_image = context.area.spaces[0].image
		context.area.spaces[0].image = bpy.data.images[albedo_texture_name]
		bpy.ops.image.save_as(
			save_as_render=False, filepath=str(path + albedo_texture_name + '.png'),
			relative_path=True, show_multiview=False, use_multiview=False)
		if pbr_mode:
			context.area.spaces[0].image = bpy.data.images[roughness_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + roughness_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			context.area.spaces[0].image = bpy.data.images[metallic_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + metallic_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			context.area.spaces[0].image = bpy.data.images[opacity_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + opacity_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
			context.area.spaces[0].image = bpy.data.images[emission_texture_name]
			bpy.ops.image.save_as(
				save_as_render=False, filepath=str(path + emission_texture_name + '.png'),
				relative_path=True, show_multiview=False, use_multiview=False)
		context.area.spaces[0].image = current_image

		# Save textures export dir
		act.save_dir = path

		# Switch active area to 3D View
		context.area.type = 'VIEW_3D'

		# Select again objects
		for j in start_selected_obj:
			j.select_set(True)

		# Restore objects selection and areas
		context.view_layer.objects.active = start_active_obj
		context.area.type = current_area

		if flag_exist_area:
			for ie_area in ie_areas:
				context.screen.areas[ie_area].ui_type = 'UV'

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
		if palette_back_material:
			bpy.data.materials.remove(palette_back_material)

		for mesh in temp_meshes:
			bpy.data.meshes.remove(mesh)

		for material in bpy.data.materials:
			if material.name == 'Palette_Bake':
				bpy.data.materials.remove(material)

		# Restore render engine
		context.scene.render.engine = current_engine

		common_utils.print_execution_time("Create Palette Texture", start_time)

		# Show message about incorrect names
		if len(incorrect_names) > 0:
			common_utils.show_message_box("Palette name has invalid characters. Some chars have been replaced",
								   "Incorrect Palette Name")

		return {'FINISHED'}


# Open textures export directory
class OpenSaveDir(bpy.types.Operator):
	"""Open Save Directory in OS"""
	bl_idname = "act.open_palette_save_dir"
	bl_label = "Open Save Directory"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act

		# Try open export directory in OS
		if not os.path.exists(os.path.realpath(bpy.path.abspath(act.save_path))):
			act.save_dir = ""
			common_utils.show_message_box('Directory not exist',
								   'Wrong Path',
								   'ERROR')

			return {'CANCELLED'}

		if len(act.save_dir) > 0:
			try:
				os.startfile(act.save_dir)
			except:
				subprocess.Popen(['xdg-open', act.save_dir])
		else:
			common_utils.show_message_box('Create Palette\'s before',
								   'Info')
			return {'FINISHED'}

		common_utils.print_execution_time("Open Textures Export Directory", start_time)
		return {'FINISHED'}


# Assign materials in multiEdit
class AssignMultiEditMaterials(bpy.types.Operator):
	"""Assign Materials for some objects in MultiEdit Mode"""
	bl_idname = "act.assign_multi_edit_materials"
	bl_label = "Active Material -> Selected"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects
		active_obj = context.active_object
		active_mat = context.active_object.active_material.name_full

		bpy.ops.object.mode_set(mode='OBJECT')

		# Added active material to all selected objects
		# If these objects don't have slot with this material
		# But have selected polygons
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x
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
				context.active_object.active_material_index = mat_index
				bpy.ops.object.material_slot_assign()
				bpy.ops.object.mode_set(mode='OBJECT')

		# Select again objects
		for j in selected_obj:
			j.select_set(True)

		context.view_layer.objects.active = active_obj
		bpy.ops.object.mode_set(mode='EDIT')

		common_utils.print_execution_time("Assign Material in Multi-Edit Mode", start_time)
		return {'FINISHED'}


# Clear vertex colors
class ClearVertexColors(bpy.types.Operator):
	"""Clear Vertex Colors"""
	bl_idname = "act.clear_vc"
	bl_label = "Clear Vertex Colors"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		current_selected_obj = context.selected_objects
		current_active_obj = context.active_object

		for x in current_selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x
			if x.type == 'MESH':
				for color_attribute in reversed(x.data.color_attributes):
					bpy.ops.geometry.color_attribute_remove()

		for x in current_selected_obj:
			x.select_set(True)
		context.view_layer.objects.active = current_active_obj

		common_utils.print_execution_time("Clear Vertex Colors", start_time)
		return {'FINISHED'}


# Material color to viewport color
class MaterialToViewport(bpy.types.Operator):
	"""Material Color to Viewport Color"""
	bl_idname = "act.material_to_viewport"
	bl_label = "Material -> Viewport Colors"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects
		active_obj = context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x
			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				for mat in x.data.materials:
					try:
						mat.diffuse_color = mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value
					except:
						print("Can\'t change viewport material color")

		# Select again objects
		for j in selected_obj:
			j.select_set(True)

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Material Color to Viewport", start_time)
		return {'FINISHED'}


# Random material viewport color
class RandomViewportColor(bpy.types.Operator):
	"""Random Material Viewport Color"""
	bl_idname = "act.random_viewport_color"
	bl_label = "Random Material Viewport Color"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects
		active_obj = context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x

			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				for mat in x.data.materials:
					random_hue = random.randrange(0, 10, 1) / 10
					random_value = random.randrange(2, 10, 1) / 10
					random_saturation = random.randrange(7, 10, 1) / 10
					color = colorsys.hsv_to_rgb(random_hue, random_saturation, random_value)
					color4 = (color[0], color[1], color[2], 1)
					try:
						mat.diffuse_color = color4
					except:
						print("Can\'t change viewport material color")

		# Select again objects
		for j in selected_obj:
			j.select_set(True)

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Random Color to Viewport", start_time)
		return {'FINISHED'}


# Clear viewport color
class ClearViewportColor(bpy.types.Operator):
	"""Clear Viewport Color"""
	bl_idname = "act.clear_viewport_color"
	bl_label = "Clear Viewport Colors"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects
		active_obj = context.active_object

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x

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

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Clear Viewport Color", start_time)
		return {'FINISHED'}


# Delete unused materials
class DeleteUnusedMaterials(bpy.types.Operator):
	"""Delete from Objects Unused Materials and Slots"""
	bl_idname = "act.delete_unused_materials"
	bl_label = "Delete Unused Materials"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects
		active_obj = context.active_object

		# Delete Unused Materials
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x

			if x.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
				bpy.ops.object.material_slot_remove_unused()

		# Select again objects
		for j in selected_obj:
			j.select_set(True)

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Delete Unused Materials", start_time)
		return {'FINISHED'}


# Delete duplicated materials
class DeleteDuplicatedMaterials(bpy.types.Operator):
	"""Delete from Selected Objects Duplicated Materials"""
	bl_idname = "act.delete_duplicated_materials"
	bl_label = "Cleanup Duplicated Materials"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = context.selected_objects

		# Collect original materials names
		material_names = []

		for obj in selected_obj:
			if obj.type == 'MESH':
				for slot_material in obj.data.materials:
					if slot_material:
						material_clean_name = slot_material.name
						if material_clean_name[:-3][-1:] == '.':
							material_clean_name = material_clean_name[:-4]
							name_in_list = False
							for name in material_names:
								if name == material_clean_name:
									name_in_list = True
							if not name_in_list:
								material_names.append(material_clean_name)

		# Try to get materials with these names
		materials = []
		for name in material_names:
			try:
				scene_material = bpy.data.materials[name]
			except:
				continue

			mat_in_list = False
			for material in materials:
				if scene_material == material:
					mat_in_list = True
			if not mat_in_list:
				materials.append(scene_material)

		if len(materials) == 0:
			common_utils.show_message_box("Original Materials (or duplicates) is not found",
									'Material Search',
									'ERROR')
			return {'CANCELLED'}

		# Replace duplicated materials
		materials_for_remove = []
		for obj in selected_obj:
			for material_slot in obj.material_slots:
				if material_slot.material and material_slot.name[:-3][-1:] == '.':
					for material in materials:
						if material.name == material_slot.name[:-4]:
							old_material = material_slot.material
							material_slot.material = material
							if old_material.users == 0:
								materials_for_remove.append(old_material)

		# Cleanup
		for material in materials_for_remove:
			bpy.data.materials.remove(material)

		common_utils.show_message_box("Replaced " + str(len(materials_for_remove)) + \
							   " duplicate(s) with " + str(len(materials)) + " original material(s)",
							   'Materials Replaced')

		common_utils.print_execution_time("Delete Duplicated Materials", start_time)

		return {'FINISHED'}


# Select texture in UV Editor from active material (See Select_Texture_Menu)
class TextureFromActiveMaterial(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "act.texture_from_material"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}
	texture_name: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		for area in context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				area.spaces[0].image = bpy.data.images[self.texture_name]

		common_utils.print_execution_time("Select Texture in UV Editor", start_time)
		
		return {'FINISHED'}


# Menu for select texture In UV Editor from active material
class SelectTextureMenu(bpy.types.Menu):
	bl_idname = "OBJECT_MT_select_texture_menu"
	bl_label = "Select Texture"

	def draw(self, context):
		layout = self.layout
		texture_list = []

		# If now window has Image Editor area
		has_opened_image_editor = False
		for area in context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				has_opened_image_editor = True

		if has_opened_image_editor:
			# If active object is mesh and has material slots
			if context.active_object.type == 'MESH':
				if len(context.active_object.data.materials) > 0:
					has_textures = False

					# Collect all textures from active material to list
					for node in context.active_object.active_material.node_tree.nodes:
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
			layout.operator(TextureFromActiveMaterial.bl_idname, text=texture).texture_name = texture


# Call menu for select texture In UV Editor from active material
class CallSelectTextureMenu(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "act.call_select_texture_menu"
	bl_label = "Open Texture in UV Editor"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, _):
		bpy.ops.wm.call_menu(name=SelectTextureMenu.bl_idname)

		return {'FINISHED'}


# Material tools UI panel in 3D View
class VIEW3D_PT_material_tools_panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {'OBJECT', 'EDIT_MESH'} and prefs.material_enable)

	def draw(self, context):
		act = context.scene.act
		layout = self.layout

		if context.mode == 'OBJECT':
			box = layout.box()
			row = box.row()
			row.operator(MaterialToViewport.bl_idname)

			row = box.row()
			row.operator(RandomViewportColor.bl_idname)

			row = box.row()
			row.operator(ClearViewportColor.bl_idname)

			row = layout.row()
			row.operator(ClearVertexColors.bl_idname)

			row = layout.row()
			row.operator(DeleteUnusedMaterials.bl_idname)

			row = layout.row()
			row.operator(DeleteDuplicatedMaterials.bl_idname)

			box = layout.box()
			row = box.row()
			row.prop(act, "pbr_workflow", text="PBR Workflow")
			row = box.row()
			row.prop(act, "custom_save_path", text="Custom Save Path")
			if act.custom_save_path:
				row = box.row(align=True)
				row.label(text="Save Path:")
				row.prop(act, "save_path")
			row = box.row()
			row.operator(CreatePalette.bl_idname)
			if len(act.save_dir) > 0:
				row = box.row()
				row.operator(OpenSaveDir.bl_idname)

		row = layout.row()
		row.operator(CallSelectTextureMenu.bl_idname)


# Material tools UI panel in UV Editor
class UV_PT_material_uv_tools_panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[__package__].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {'OBJECT', 'EDIT_MESH'} and prefs.uv_material_enable)

	def draw(self, _):
		layout = self.layout

		row = layout.row()
		row.operator(CallSelectTextureMenu.bl_idname)


# Material assign UI panel
def material_menu_panel(self, context):
	prefs = context.preferences.addons[__package__].preferences
	if context.object is not None and context.active_object is not None and prefs.material_properties_enable:
		if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
			layout = self.layout
			row = layout.row()
			row.operator(AssignMultiEditMaterials.bl_idname)


classes = (
	CreatePalette,
	OpenSaveDir,
	AssignMultiEditMaterials,
	ClearVertexColors,
	MaterialToViewport,
	ClearViewportColor,
	RandomViewportColor,
	DeleteUnusedMaterials,
	DeleteDuplicatedMaterials,
	TextureFromActiveMaterial,
	SelectTextureMenu,
	CallSelectTextureMenu,
	VIEW3D_PT_material_tools_panel,
	UV_PT_material_uv_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	if utils.cycles_is_enabled():
		bpy.types.CYCLES_PT_context_material.prepend(material_menu_panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.prepend(material_menu_panel)


def unregister():
	if utils.cycles_is_enabled():
		try:
			bpy.types.CYCLES_PT_context_material.remove(material_menu_panel)
		except AttributeError as err:
			print(err)

	try:
		bpy.types.EEVEE_MATERIAL_PT_context_material.remove(material_menu_panel)
	except AttributeError as err:
		print(err)

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
