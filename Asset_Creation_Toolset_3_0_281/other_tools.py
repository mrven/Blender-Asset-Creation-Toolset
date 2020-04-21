import bpy

from bpy.props import StringProperty


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
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.mesh.customdata_custom_splitnormals_clear()
				bpy.context.object.data.auto_smooth_angle = math.pi
				bpy.context.object.data.use_auto_smooth = True
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj					
		return {'FINISHED'}		
		
#-------------------------------------------------------
#Recalculate Normals
class CalcNormals(bpy.types.Operator):
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
#Delete Unused Materials
class DeleteUnusedMaterials(bpy.types.Operator):
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
	texture_name: StringProperty()

	def execute(self, context):
		for area in bpy.context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				area.spaces[0].image = bpy.data.images[self.texture_name]
		
		return {'FINISHED'}		

#-------------------------------------------------------
#Select Texture In UV Editor From Active Material
class Test_Call_Menu(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "uv.test_call_menu"
	bl_label = "Select Texture In UV Editor From Active Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.wm.call_menu(name="UV_MT_select_texture")
		
		return {'FINISHED'}	

classes = (
	ClearNormals,
	CalcNormals,
	ObjNameToMeshName,
	DeleteUnusedMaterials,
	Texture_From_Active_Material,
	Test_Call_Menu,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)