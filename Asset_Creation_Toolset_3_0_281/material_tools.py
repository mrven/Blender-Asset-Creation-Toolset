import bpy

#-------------------------------------------------------
#Palette Texture Creator
class Palette_Create(bpy.types.Operator):
	"""Palette Texture Creator"""
	bl_idname = "object.palette_creator"
	bl_label = "Palette Texture Creator"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#Check Render Engine
		current_engine = bpy.context.scene.render.engine
		bpy.context.scene.render.engine = 'CYCLES'

		#check opened image editor window
		ie_area = 0
		flag_exist_area = False
		for area in range(len(bpy.context.screen.areas)):
			if bpy.context.screen.areas[area].type == 'IMAGE_EDITOR':
				ie_area = area
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
		for material in bpy.data.materials:
			if material.name == 'Palette_Bake':
				bpy.data.materials.remove(material)
				
		palette_bake_mat = bpy.data.materials.new('Palette_Bake')

		#Setup material for baking
		bake_plane.data.materials.append(palette_bake_mat)
		palette_bake_mat.use_nodes = True
		nodes = palette_bake_mat.node_tree.nodes
		tex_node = nodes.new('ShaderNodeTexImage')
		tex_node.location = (-500,0)
		tex_node.image = bpy.data.images['Palette_' + add_name_palette]

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
			bpy.context.screen.areas[ie_area].type = 'IMAGE_EDITOR'

		atlas_material_exist = False
		for material in bpy.data.materials:
			if material.name_full == 'Palette_' + add_name_palette:
				atlas_material_exist = True
		
		if not atlas_material_exist:
			#Connect Texture to Shader Base Color and rename
			palette_bake_mat.node_tree.links.new(tex_node.outputs['Color'], palette_bake_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
			palette_bake_mat.name = 'Palette_' + add_name_palette

		#Delete Temp Materials
		bpy.data.materials.remove(bpy.data.materials['Palette_background'])

		for material in bpy.data.materials:
			if material.name == 'Palette_Bake':
				bpy.data.materials.remove(material)

		bpy.context.scene.render.engine = current_engine

		return {'FINISHED'}


#-------------------------------------------------------
#Assign Materials in MultiEdit
class Assign_Multiedit_Materials(bpy.types.Operator):
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

				selected_poly = False
				for p in x.data.polygons:
					if p.select == True:
						selected_poly = True

				if append_mat and selected_poly:
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
#Clear Vertex Colors
class Clear_Vertex_Colors(bpy.types.Operator):
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
#Material Color to Viewport Color
class Material_To_Viewport(bpy.types.Operator):
	"""Material Color to Viewport Color"""
	bl_idname = "object.material_to_viewport"
	bl_label = "Material Color to Viewport Color"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		#Delete Unused Materials
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				for mat in x.data.materials:
					try:
						mat.diffuse_color = mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value
					except:
						print("Can\'t change viewport material color")
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		return {'FINISHED'}


#-------------------------------------------------------
#Delete Unused Materials
class Delete_Unused_Materials(bpy.types.Operator):
	"""Delete from Objects Unused Materials and Slots"""
	bl_idname = "object.delete_unused_materials"
	bl_label = "Delete Unused Materials"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object

		#Delete Unused Materials
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			if x.type == 'MESH':
				bpy.ops.object.material_slot_remove_unused()
			
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		return {'FINISHED'}


#-------------------------------------------------------
#Select Texture In UV Editor From Active Material
class Texture_From_Active_Material(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "uv.texture_from_material"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}
	texture_name: bpy.props.StringProperty()

	def execute(self, context):
		for area in bpy.context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				area.spaces[0].image = bpy.data.images[self.texture_name]
		
		return {'FINISHED'}		


#-------------------------------------------------------
#Select Texture In UV Editor From Active Material
class Select_Texture_Menu(bpy.types.Menu):
	bl_idname = "uv.select_texture_menu"
	bl_label = "Select Texture"

	def draw(self, context):
		layout = self.layout
		if bpy.context.active_object.type == 'MESH':
			if len(bpy.context.active_object.data.materials) > 0:
				for node in bpy.context.active_object.active_material.node_tree.nodes:
					if node.type == 'TEX_IMAGE':
						texture_name = node.image.name_full
						row = layout.row()
						row.operator("uv.texture_from_material", text=texture_name).texture_name=texture_name
			else:
				row.label("Mesh has not materials")
		else:
			row.label("Object is not mesh")


class Call_Select_Texture_Menu(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "uv.call_select_texture_menu"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.wm.call_menu(name="uv.select_texture_menu")
		
		return {'FINISHED'}	


#-------------------------------------------------------
#Low-Poly Art Tools UI Panel
class VIEW3D_Material_Tools_Panel(bpy.types.Panel):
	bl_label = "Low Poly Art Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and context.object.mode == 'OBJECT')

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.palette_creator", text="Create Palette Texture")
				layout.separator()
				row = layout.row()
				row.operator("object.material_to_viewport", text="Material -> Viewport Color")
				layout.separator()

			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.uv_remove", text="Clear UV Maps")
				row = layout.row()
				row.operator("object.clear_vc", text="Clear Vertex Colors")
				layout.separator()


#-------------------------------------------------------
#Material Assign UI Panel
def Material_Menu_Panel(self, context):
	if context.object is not None:
			if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
				layout = self.layout
				row = layout.row()		
				row.operator("object.assign_multiedit_materials", text="Active Material -> Selected")


classes = (
	Palette_Create,
	Assign_Multiedit_Materials,
	Clear_Vertex_Colors,
	Material_To_Viewport,
	Delete_Unused_Materials,
	Texture_From_Active_Material,
	Select_Texture_Menu,
	Call_Select_Texture_Menu,
	VIEW3D_Material_Tools_Panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.CYCLES_PT_context_material.prepend(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.prepend(Material_Menu_Panel)


def unregister():
	bpy.types.CYCLES_PT_context_material.remove(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.remove(Material_Menu_Panel)
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)