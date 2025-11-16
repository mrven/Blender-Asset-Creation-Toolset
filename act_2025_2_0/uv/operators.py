import bpy
from datetime import datetime
import math

from ..common import utils as common_utils
from . import utils

package_name = __package__.split('.')[0]

# UV remover
class ClearUV(bpy.types.Operator):
	"""Clear UV layers"""
	bl_idname = "object.act_uv_clear"
	bl_label = "Clear UV Maps"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		restore_selected = context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = context.active_object
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x
			for a in range(len(x.data.uv_layers)):
				bpy.ops.mesh.uv_texture_remove()

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Clear UV", start_time)
		return {'FINISHED'}


# Rename UV
class RenameUV(bpy.types.Operator):
	"""Rename UV"""
	bl_idname = "object.act_uv_rename"
	bl_label = "Rename UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		selected_obj = utils.selected_obj_with_unique_data()
		uv_index = act.uv_index_rename
		uv_name = act.uv_name_rename
		if len(uv_name) == 0:
			uv_name = "UVMap"

		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].name = uv_name

		common_utils.print_execution_time("Rename UV", start_time)
		return {'FINISHED'}


# Add UV
class AddUV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.act_uv_add"
	bl_label = "Add UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		restore_selected = context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = context.active_object
		uv_name = act.uv_name_add

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x
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

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Add UV", start_time)
		return {'FINISHED'}


# Remove UV
class RemoveUV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.act_uv_remove"
	bl_label = "Remove UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		restore_selected = context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = context.active_object
		uv_index = act.uv_index_rename

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x

			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].active = True
					bpy.ops.mesh.uv_texture_remove()

		# Select again objects
		for j in restore_selected:
			j.select_set(True)

		context.view_layer.objects.active = active_obj

		common_utils.print_execution_time("Remove UV", start_time)
		return {'FINISHED'}


# Select UV
class SelectUV(bpy.types.Operator):
	"""Add UV"""
	bl_idname = "object.act_uv_select"
	bl_label = "Set Active UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		selected_obj = utils.selected_obj_with_unique_data()
		uv_index = act.uv_index_rename

		for x in selected_obj:
			if len(x.data.uv_layers) > 0:
				if uv_index < len(x.data.uv_layers):
					x.data.uv_layers[uv_index].active_render = True
					x.data.uv_layers[uv_index].active = True

		common_utils.print_execution_time("Select UV", start_time)
		return {'FINISHED'}


# UV mover
class UVMover(bpy.types.Operator):
	"""UV Mover"""
	bl_idname = "uv.act_uv_mover"
	bl_label = "Move and Scale UV islands"
	bl_options = {'REGISTER', 'UNDO'}
	move_command: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act

		start_pivot_mode = context.space_data.pivot_point
		context.space_data.pivot_point = 'CURSOR'
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

		context.space_data.pivot_point = start_pivot_mode

		common_utils.print_execution_time("UV Mover", start_time)
		return {'FINISHED'}


#Mark Seams from UV
class MarkSeamsFromUV(bpy.types.Operator):
	"""Mark Seams from UV"""
	bl_idname = "object.act_mark_seams_from_uv"
	bl_label = "Mark Seams from UV"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		current_area = context.area.type
		restore_selected = context.selected_objects[:]
		selected_obj = utils.selected_obj_with_unique_data()
		active_obj = context.active_object

		# Switch active area to Image Editor
		context.area.type = 'IMAGE_EDITOR'

		# If Image Editor has Render Result, Clean it
		if context.area.spaces[0].image is not None:
			if context.area.spaces[0].image.name == 'Render Result':
				context.area.spaces[0].image = None

		# Switch Image Editor to UV Editor
		if context.space_data.mode != 'UV':
			context.space_data.mode = 'UV'

		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			context.view_layer.objects.active = x

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

		context.area.type = current_area
		context.view_layer.objects.active = active_obj
		common_utils.print_execution_time("Mark Seams from UV", start_time)
		return {'FINISHED'}


classes = (
	ClearUV,
	RenameUV,
	AddUV,
	RemoveUV,
	SelectUV,
	UVMover,
	MarkSeamsFromUV,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)