import bpy

from . import operators
from ..common import utils as common_utils

package_name = common_utils.get_short_package_name()

class VIEW3D_PT_geometry_tools_panel(bpy.types.Panel):
	bl_label = "Geometry Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return ((context.object is not None and context.active_object is not None and context.mode == "EDIT_MESH")
		        and prefs.geometry_enable)

	def draw(self, _):
		layout = self.layout
		row = layout.row()
		row.operator(operators.DissolveCheckerLoops.bl_idname)
		row = layout.row()
		row.operator(operators.CollapseCheckerEdges.bl_idname)


classes = (
	VIEW3D_PT_geometry_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)