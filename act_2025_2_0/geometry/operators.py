import bpy
from datetime import datetime

from ..common import utils as common_utils

package_name = __package__.split('.')[0]

class DissolveCheckerLoops(bpy.types.Operator):
	bl_idname = "object.act_dissolve_checker_loops"
	bl_label = "Dissolve Checker Loops"
	bl_description = "Dissolve Checker Loops (best for cylindrical topology)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		if not context.scene.tool_settings.mesh_select_mode[1]:
			common_utils.show_message_box("Change Selection Mode to EDGE first",
								   "Invalid Selection Mode",
								   'ERROR')
			return {'CANCELLED'}

		selected_obj = context.selected_objects
		selected_edges = 0
		bpy.ops.object.mode_set(mode='OBJECT')

		for obj in selected_obj:
			for edge in obj.data.edges:
				selected_edges += edge.select

		bpy.ops.object.mode_set(mode='EDIT')

		if selected_edges != 1:
			common_utils.show_message_box("Select only one Edge",
								   "Wrong Selection",
								   'ERROR')
			return {'CANCELLED'}

		bpy.ops.mesh.loop_multi_select(ring=True)
		bpy.ops.mesh.select_nth(offset=1)
		bpy.ops.mesh.loop_multi_select(ring=False)
		bpy.ops.mesh.dissolve_mode(use_verts=True)

		common_utils.print_execution_time("Dissolve Checker Loops", start_time)
		return {'FINISHED'}


class CollapseCheckerEdges(bpy.types.Operator):
	bl_idname = "object.act_collapse_checker_edges"
	bl_label = "Collapse Checker Edges"
	bl_description = "Collapse Checker Edges (best for ring topology)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		if not context.scene.tool_settings.mesh_select_mode[1]:
			common_utils.show_message_box("Change Selection Mode to EDGE first",
								   "Invalid Selection Mode",
								   'ERROR')
			return {'CANCELLED'}

		selected_obj = context.selected_objects
		selected_edges = 0
		bpy.ops.object.mode_set(mode='OBJECT')

		for obj in selected_obj:
			for edge in obj.data.edges:
				selected_edges += edge.select

		bpy.ops.object.mode_set(mode='EDIT')

		if selected_edges != 1:
			common_utils.show_message_box("Select only one Edge",
								   "Wrong Selection",
								   'ERROR')
			return {'CANCELLED'}

		bpy.ops.mesh.loop_multi_select(ring=False)
		bpy.ops.mesh.select_nth(offset=1)
		bpy.ops.mesh.merge(type='COLLAPSE')

		common_utils.print_execution_time("Collapse Checker Edges", start_time)
		return {'FINISHED'}


classes = (
	DissolveCheckerLoops,
	CollapseCheckerEdges,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)