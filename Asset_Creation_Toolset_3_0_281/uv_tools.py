import bpy

#-------------------------------------------------------
#UV-Remover
class UV_Remove(bpy.types.Operator):
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

#-------------------------------------------------------
#Rename UV(s)
class Rename_UV(bpy.types.Operator):
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


#-------------------------------------------------------
#UV Mover UI Panel
class UV_UV_Mover_Panel(bpy.types.Panel):
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


#-------------------------------------------------------
#UV Tools UI Panels
class VIEW3D_UV_Tools_Panel(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and (context.object.mode == 'OBJECT' or context.mode == 'EDIT_ARMATURE'))

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
				layout.separator()
				

classes = (
	UV_Remove,
	Rename_UV,
	UV_Mover,
	UV_UV_Mover_Panel,
	VIEW3D_UV_Tools_Panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)