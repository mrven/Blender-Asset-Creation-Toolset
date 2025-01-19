import bpy
from . import utils
from datetime import datetime
import math


# UV remover
class ClearUV(bpy.types.Operator):
	"""Clear UV layers"""
	bl_idname = "object.uv_clear"
	bl_label = "Clear UV layers"
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

		utils.print_execution_time("Clear UV", start_time)
		return {'FINISHED'}


# Rename UV
class RenameUV(bpy.types.Operator):
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
		if len(uv_name) == 0:
			uv_name = "UVMap"

		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].name = uv_name

		utils.print_execution_time("Rename UV", start_time)
		return {'FINISHED'}


# Add UV
class AddUV(bpy.types.Operator):
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
			if act.uv_packing_mode == 'SMART':
				bpy.ops.object.mode_set(mode='EDIT')
				angle = math.pi * act.uv_packing_smart_angle / 180
				bpy.ops.uv.smart_project(angle_limit=angle, margin_method='SCALED', rotate_method='AXIS_ALIGNED_Y',
										 island_margin=act.uv_packing_smart_margin, area_weight=0.0,
										 correct_aspect=True, scale_to_bounds=False)
				bpy.ops.object.mode_set(mode='OBJECT')
			if act.uv_packing_mode == 'LIGHTMAP':
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.uv.lightmap_pack(PREF_CONTEXT='ALL_FACES', PREF_PACK_IN_ONE=False, PREF_NEW_UVLAYER=False,
										 PREF_BOX_DIV=act.uv_packing_lightmap_quality,
										 PREF_MARGIN_DIV=act.uv_packing_lightmap_margin)
				bpy.ops.object.mode_set(mode='OBJECT')

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		bpy.context.view_layer.objects.active = active_obj

		utils.print_execution_time("Add UV", start_time)
		return {'FINISHED'}


# Remove UV
class RemoveUV(bpy.types.Operator):
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

		utils.print_execution_time("Remove UV", start_time)
		return {'FINISHED'}


# Select UV
class SelectUV(bpy.types.Operator):
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

		utils.print_execution_time("Select UV", start_time)
		return {'FINISHED'}


# UV mover
class UVMover(bpy.types.Operator):
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

		utils.print_execution_time("UV Mover", start_time)
		return {'FINISHED'}


#Mark Seams from UV
class MarkSeamsFromUV(bpy.types.Operator):
	"""Mark Seams from UV"""
	bl_idname = "object.mark_seams_from_uv"
	bl_label = "Mark Seams from UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		current_area = bpy.context.area.type
		restore_selected = bpy.context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = bpy.context.active_object

		# Switch active area to Image Editor
		bpy.context.area.type = 'IMAGE_EDITOR'

		# If Image Editor has Render Result, Clean it
		if bpy.context.area.spaces[0].image is not None:
			if bpy.context.area.spaces[0].image.name == 'Render Result':
				bpy.context.area.spaces[0].image = None

		# Switch Image Editor to UV Editor
		if bpy.context.space_data.mode != 'UV':
			bpy.context.space_data.mode = 'UV'

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			bpy.context.view_layer.objects.active = x

			if len(x.data.uv_layers) > 0:
				bpy.ops.object.mode_set(mode='EDIT')
				selection = utils.get_mesh_selection(x)
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				bpy.ops.uv.select_all(action='SELECT')
				bpy.ops.uv.seams_from_islands()
				bpy.ops.mesh.select_all(action='DESELECT')
				utils.set_mesh_selection(x, selection)
				bpy.ops.object.mode_set(mode='OBJECT')

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		bpy.context.area.type = current_area
		bpy.context.view_layer.objects.active = active_obj
		utils.print_execution_time("Mark Seams from UV", start_time)
		return {'FINISHED'}


# UV mover UI panel
class UV_PT_uv_mover_panel(bpy.types.Panel):
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
class VIEW3D_PT_uv_tools_panel(bpy.types.Panel):
	bl_label = "UV Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and (context.mode == 'OBJECT' or context.mode == 'EDIT_MESH')) \
			and preferences.uv_view3d_enable

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

				box = layout.box()
				row = box.row(align=True)
				row.prop(act, "uv_name_add")
				row.operator("object.uv_add", text="Add UV")
				row = box.row(align=True)
				row.label(text="Packing:")
				row.prop(act, "uv_packing_mode", expand=False)
				if act.uv_packing_mode == 'SMART':
					row = box.row()
					row.prop(act, "uv_packing_smart_angle", text="Angle:")
					row = box.row()
					row.prop(act, "uv_packing_smart_margin", text="Margin:")
				if act.uv_packing_mode == 'LIGHTMAP':
					row = box.row()
					row.prop(act, "uv_packing_lightmap_quality", text="Quality:")
					row = box.row()
					row.prop(act, "uv_packing_lightmap_margin", text="Margin:")
				row = layout.row()
				row.operator("object.uv_clear", text="Clear UV Maps")
				row = layout.row()
				row.operator("object.mark_seams_from_uv", text="Mark Seams from UV")

classes = (
	ClearUV,
	RenameUV,
	AddUV,
	RemoveUV,
	SelectUV,
	UVMover,
	MarkSeamsFromUV
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
