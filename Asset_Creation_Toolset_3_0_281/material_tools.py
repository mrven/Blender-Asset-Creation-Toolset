import bpy

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
#Material Assign UI Panel
def Material_Menu_Panel(self, context):
	if context.object is not None:
			if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
				layout = self.layout
				row = layout.row()		
				row.operator("object.assign_multiedit_materials", text="Active Material -> Selected")


classes = (
	Assign_Multiedit_Materials,
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