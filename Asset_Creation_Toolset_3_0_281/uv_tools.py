import bpy


#-------------------------------------------------------
#UV Mover
class UV_Mover(bpy.types.Operator):
	"""UV Mover"""
	bl_idname = "uv.uv_mover"
	bl_label = "Move and Scale UV islands"
	bl_options = {'REGISTER', 'UNDO'}
	Value: bpy.props.StringProperty()
	
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


classes = (
	UV_Mover,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)