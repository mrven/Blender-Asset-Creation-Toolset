import bpy
from datetime import datetime

from . import utils

class Align(bpy.types.Operator):
	"""Origin To Min/Max/Mid/Coordinate/Cursor"""
	bl_idname = "act.align"
	bl_label = "Origin To ..."
	bl_options = {'REGISTER', 'UNDO'}
	mode: bpy.props.StringProperty()
	axis: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = context.selected_objects
		current_active_obj = context.active_object
		saved_cursor_loc = context.scene.cursor.location.copy()

		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')

		axis_index = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]

		# Change individual origin point
		for obj in current_selected_obj:
			if obj.type != 'MESH':
				continue

			obj.select_set(True)
			context.view_layer.objects.active = obj
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = obj.location.copy()

			bpy.ops.object.mode_set(mode='EDIT')

			target_co = None

			if self.mode == 'MIN':
				target_co = utils.find_min_max_verts(obj, axis_index)[0]
			elif self.mode == 'MAX':
				target_co = utils.find_min_max_verts(obj, axis_index)[1]
			elif self.mode == 'MID':
				min_co, max_co = utils.find_min_max_verts(obj, axis_index)
				target_co = (min_co + max_co) / 2
			elif self.mode == 'CURSOR':
				target_co = saved_cursor_loc[axis_index]
			elif self.mode == 'COORDINATE':
				target_co = act.align_co

			if target_co is None:
				target_co = saved_origin_loc[axis_index]

			if not act.align_geom_to_orig:
				# Move cursor
				bpy.ops.object.mode_set(mode='OBJECT')

				new_cursor = list(saved_origin_loc)
				new_cursor[axis_index] = target_co
				context.scene.cursor.location = new_cursor

				# Apply origin to cursor position
				bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
				# Reset 3D Cursor position to previous point
				context.scene.cursor.location = saved_cursor_loc

			# Align Geometry To Origin (Optional)
			# Move Geometry of object instead of origin
			if act.align_geom_to_orig:
				if self.mode in {'CURSOR','COORDINATE'}:
					bpy.ops.object.mode_set(mode='OBJECT')
					difference = target_co - saved_origin_loc[axis_index]
				else:
					difference = saved_origin_loc[axis_index] - target_co
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')

				move_vector = [0.0, 0.0, 0.0]
				move_vector[axis_index] = difference

				constraint_axis = [False, False, False]
				constraint_axis[axis_index] = True

				translate_params = {
					'value': tuple(move_vector),
					'constraint_axis': tuple(constraint_axis),
					'orient_type': 'GLOBAL',
					'orient_matrix_type': 'GLOBAL',
					'mirror': False,
					'use_proportional_edit': False
				}

				bpy.ops.transform.translate(**translate_params)

				bpy.ops.object.mode_set(mode='OBJECT')

			obj.select_set(False)

		# Select again objects
		for j in current_selected_obj:
			j.select_set(True)

		context.view_layer.objects.active = current_active_obj

		utils.print_execution_time("Align To ...", start_time)
		return {'FINISHED'}


# Set origin to selection in edit mode
class OriginToSelection(bpy.types.Operator):
	"""Set Origin To Selection"""
	bl_idname = "act.set_origin_to_select"
	bl_label = "Set Origin To Selection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		saved_cursor_loc = context.scene.cursor.location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.mode_set(mode='OBJECT')
		# Apply origin to Cursor position
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		# Reset 3D Cursor position  
		context.scene.cursor.location = saved_cursor_loc
		bpy.ops.object.mode_set(mode='EDIT')

		utils.print_execution_time("Set Origin to Selection", start_time)
		return {'FINISHED'}


# Origin tools UI panel
class VIEW3D_PT_origin_tools_panel(bpy.types.Panel):
	bl_label = "Origin Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[__package__].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {'OBJECT', 'EDIT_MESH'} and preferences.origin_enable)

	def draw(self, context):
		act = context.scene.act

		layout = self.layout
		if context.mode == 'OBJECT':
			row = layout.row()
			row.label(text="Origin Align")

			row = layout.row()
			row.prop(act, "align_geom_to_orig", text="Geometry To Origin")

			# Aligner Labels
			row = layout.row(align=True)
			row.label(text="X")
			row.label(text="Y")
			row.label(text="Z")

			align_modes = [
				("Min", "MIN"),
				("Max", "MAX"),
				("Middle", "MID"),
				("Cursor", "CURSOR"),
				("Coordinate", "COORDINATE")
			]

			axes = ['X', 'Y', 'Z']

			for label, align_mode in align_modes:
				row = layout.row(align=True)
				for axis in axes:
					op = row.operator(Align.bl_idname, text=label)
					op.axis = axis
					op.mode = align_mode

			row = layout.row()
			row.prop(act, "align_co", text="Coordinate")

		if context.object.mode == 'EDIT':
			row = layout.row()
			row.operator(OriginToSelection.bl_idname, text="Set Origin To Selected")


classes = (
	Align,
	OriginToSelection,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
