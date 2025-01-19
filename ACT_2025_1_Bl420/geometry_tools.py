import bpy

from . import utils
from datetime import datetime


# Dissolve Checker Loops
class DissolveCheckerLoops(bpy.types.Operator):
	"""Dissolve Checker Loops"""
	bl_idname = "object.dissolve_checker_loops"
	bl_label = "Dissolve Checker Loops"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		if bpy.context.scene.tool_settings.mesh_select_mode[1]:
			utils.show_message_box("Change Selection Mode to EDGE first",
								   "Invalid Selection Mode",
								   'ERROR')
			return {'CANCELLED'}
		else:
			selected_obj = bpy.context.selected_objects
			selected_edges = 0
			bpy.ops.object.mode_set(mode='OBJECT')

			for obj in selected_obj:
				for edge in obj.data.edges:
					selected_edges += edge.select

			bpy.ops.object.mode_set(mode='EDIT')

			if selected_edges != 1:
				utils.show_message_box("Select only one Edge",
									   "Wrong Selection",
									   'ERROR')
				return {'CANCELLED'}

		bpy.ops.mesh.loop_multi_select(ring=True)
		bpy.ops.mesh.select_nth(offset=1)
		bpy.ops.mesh.loop_multi_select(ring=False)
		bpy.ops.mesh.dissolve_mode(use_verts=True)

		utils.print_execution_time("Dissolve Checker Loops", start_time)
		return {'FINISHED'}


# Collapse  Checker Edges
class CollapseCheckerEdges(bpy.types.Operator):
	"""Collapse  Checker Edges"""
	bl_idname = "object.collapse_checker_edges"
	bl_label = "Collapse  Checker Edges"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		if bpy.context.scene.tool_settings.mesh_select_mode[1]:
			utils.show_message_box("Change Selection Mode to EDGE first",
								   "Invalid Selection Mode",
								   'ERROR')
			return {'CANCELLED'}
		else:
			selected_obj = bpy.context.selected_objects
			selected_edges = 0
			bpy.ops.object.mode_set(mode='OBJECT')

			for obj in selected_obj:
				for edge in obj.data.edges:
					selected_edges += edge.select

			bpy.ops.object.mode_set(mode='EDIT')

			if selected_edges != 1:
				utils.show_message_box("Select only one Edge",
									   "Wrong Selection",
									   'ERROR')
				return {'CANCELLED'}

		bpy.ops.mesh.loop_multi_select(ring=False)
		bpy.ops.mesh.select_nth(offset=1)
		bpy.ops.mesh.merge(type='COLLAPSE')

		utils.print_execution_time("Collapse Checker Edges", start_time)
		return {'FINISHED'}


# Panels
class VIEW3D_PT_geometry_tools_panel(bpy.types.Panel):
	bl_label = "Geometry Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and context.mode == 'EDIT_MESH') and preferences.geometry_enable

	def draw(self, context):
		layout = self.layout

		if context.object is not None:
			if context.object.mode == 'OBJECT':
				row = layout.row()

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
				row.operator("object.dissolve_checker_loops", text="Dissolve Checker Loops")
				row = layout.row()
				row.operator("object.collapse_checker_edges", text="Collapse  Checker Edges")


classes = (
	DissolveCheckerLoops,
	CollapseCheckerEdges
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)