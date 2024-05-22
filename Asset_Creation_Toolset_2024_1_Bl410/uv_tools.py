import bpy
from . import utils
from datetime import datetime

# UV remover
class Clear_UV(bpy.types.Operator):
	"""Clear UV layers"""
	bl_idname = "object.uv_clear"
	bl_label = "Claer UV layers"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		restore_selected = bpy.context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = bpy.context.active_object
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			for a in range(len(x.data.uv_layers)):
				bpy.ops.mesh.uv_texture_remove()

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Clear UV", start_time)
		return {'FINISHED'}


# Rename UV
class Rename_UV(bpy.types.Operator):
	"""Rename UV"""
	bl_idname = "object.uv_rename"
	bl_label = "Rename UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		selected_obj = utils.selected_obj_with_unique_data()
		uv_index = act.uv_index_rename
		uv_name = act.uv_name_rename

		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].name = uv_name

		utils.Print_Execution_Time("Rename UV", start_time)
		return {'FINISHED'}


# Add UV
class Add_UV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.uv_add"
	bl_label = "Add UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		restore_selected = bpy.context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = bpy.context.active_object
		uv_name = act.uv_name_add

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x
			bpy.ops.mesh.uv_texture_add()
			x.data.uv_layers.active.name = uv_name

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Add UV", start_time)
		return {'FINISHED'}


# Remove UV
class Remove_UV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.uv_remove"
	bl_label = "Remove UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		restore_selected = bpy.context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = bpy.context.active_object
		uv_index = act.uv_index_rename

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x

			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].active = True
					bpy.ops.mesh.uv_texture_remove()

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Remove UV", start_time)
		return {'FINISHED'}


# Select UV
class Select_UV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.uv_select"
	bl_label = "Set Active UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		selected_obj = utils.selected_obj_with_unique_data()
		uv_index = act.uv_index_rename

		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].active_render = True
					x.data.uv_layers[uv_index].active = True

		utils.Print_Execution_Time("Select UV", start_time)
		return {'FINISHED'}


# UV mover
class UV_Mover(bpy.types.Operator):
	"""UV Mover"""
	bl_idname = "uv.uv_mover"
	bl_label = "Move and Scale UV islands"
	bl_options = {'REGISTER', 'UNDO'}
	move_command: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act

		start_pivot_mode = bpy.context.space_data.pivot_point
		bpy.context.space_data.pivot_point = 'CURSOR'
		move_step = 1 / 2 ** int(act.uv_move_factor)
		if self.move_command == "TL":
			bpy.ops.uv.cursor_set(location=(0, 1))
		if self.move_command == "TR":
			bpy.ops.uv.cursor_set(location=(1, 1))
		if self.move_command == "BL":
			bpy.ops.uv.cursor_set(location=(0, 0))
		if self.move_command == "BR":
			bpy.ops.uv.cursor_set(location=(1, 0))

		if self.move_command == "MINUS":
			bpy.ops.transform.resize(
				value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), orient_type='GLOBAL',
				orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False,
				proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.move_command == "PLUS":
			bpy.ops.transform.resize(
				value=(2, 2, 2), constraint_axis=(False, False, False), orient_type='GLOBAL',
				orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False,
				proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.move_command == "RIGHT":
			bpy.ops.transform.translate(
				value=(move_step, 0, 0), constraint_axis=(True, False, False),
				orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False,
				use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.move_command == "LEFT":
			bpy.ops.transform.translate(
				value=(-1 * move_step, 0, 0), constraint_axis=(True, False, False),
				orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False,
				use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.move_command == "UP":
			bpy.ops.transform.translate(
				value=(0, move_step, 0), constraint_axis=(False, True, False),
				orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False,
				use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		if self.move_command == "DOWN":
			bpy.ops.transform.translate(
				value=(0, -1 * move_step, 0), constraint_axis=(False, True, False),
				orient_type='GLOBAL', orient_matrix_type='GLOBAL', use_proportional_edit=False,
				proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.context.space_data.pivot_point = start_pivot_mode

		utils.Print_Execution_Time("UV Mover", start_time)
		return {'FINISHED'}


# UV mover UI panel
class UV_PT_UV_Mover_Panel(bpy.types.Panel):
	bl_label = "UV Mover"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.mode == 'EDIT_MESH') and preferences.uv_uv_enable

	def draw(self, context):
		act = bpy.context.scene.act

		layout = self.layout
		if context.object.mode == 'EDIT' and context.area.ui_type == 'UV':
			row = layout.row()
			row.label(text="Set Cursor To Corner:")

			# Aligner buttons
			row = layout.row(align=True)
			row.operator("uv.uv_mover", text="Top Left").move_command = "TL"
			row.operator("uv.uv_mover", text="Top Right").move_command = "TR"

			row = layout.row(align=True)
			row.operator("uv.uv_mover", text="Bottom Left").move_command = "BL"
			row.operator("uv.uv_mover", text="Bottom Right").move_command = "BR"

			row = layout.row()
			row.label(text="Scale and Move:")

			# Aligner buttons
			row = layout.row(align=True)
			row.operator("uv.uv_mover", text="Scale-").move_command = "MINUS"
			row.operator("uv.uv_mover", text="UP").move_command = "UP"
			row.operator("uv.uv_mover", text="Scale+").move_command = "PLUS"

			row = layout.row(align=True)
			row.operator("uv.uv_mover", text="LEFT").move_command = "LEFT"
			row.operator("uv.uv_mover", text="DOWN").move_command = "DOWN"
			row.operator("uv.uv_mover", text="RIGHT").move_command = "RIGHT"

			row = layout.row(align=True)
			row.label(text="Move Step   1/")
			row.prop(act, 'uv_move_factor', expand=False)

		else:
			row = layout.row()
			row.label(text=" ")


# UV tools UI panels
class VIEW3D_PT_UV_Tools_Panel(bpy.types.Panel):
	bl_label = "UV Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and context.object.mode == 'OBJECT') and preferences.uv_view3d_enable

	def draw(self, context):
		act = bpy.context.scene.act

		layout = self.layout
		row = layout.row()

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()

		if context.object is not None:
			if context.mode == 'OBJECT':
				# Rename UV
				box = layout.box()
				row = box.row(align=True)
				row.prop(act, "uv_index_rename", text="UV ID:")

				row = box.row(align=True)
				row.prop(act, "uv_name_rename")
				row.operator("object.uv_rename", text="Rename UV")

				row = box.row()
				row.operator("object.uv_remove", text="Remove UV")

				row = box.row()
				row.operator("object.uv_select", text="Set Active UV")

				row = layout.row(align=True)
				row.prop(act, "uv_name_add")
				row.operator("object.uv_add", text="Add UV")

				row = layout.row()
				row.operator("object.uv_clear", text="Clear UV Maps")


classes = (
	Clear_UV,
	Rename_UV,
	Add_UV,
	Remove_UV,
	Select_UV,
	UV_Mover,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
