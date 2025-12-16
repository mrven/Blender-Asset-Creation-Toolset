import bpy

from . import operators
from ..common import utils as common_utils
from ..common import constants

package_name = common_utils.get_package_name()

class VIEW3D_PT_act_support_panel(bpy.types.Panel):
	bl_label = "ACT 2025.2 Support"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {"OBJECT", "EDIT_MESH", "EDIT_ARMATURE", "PAINT_WEIGHT"} and prefs.view3d_support_enable)

	def draw(self, _):
		layout = self.layout

		box = layout.box()
		row = box.row(align=True)
		row.operator(operators.ShowAddonPrefs.bl_idname, text="Prefs", icon='PREFERENCES')
		row.operator(operators.OpenURL.bl_idname, text="Docs", icon='HELP').url = constants.ACT_DOC_URL
		row.operator(operators.OpenURL.bl_idname, text="Report", icon='URL').url = constants.ACT_REPORT_URL


class UV_PT_act_support_panel(bpy.types.Panel):
	bl_label = "ACT 2025.2 Support"
	bl_space_type = "IMAGE_EDITOR"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return context.mode in {"OBJECT", "EDIT_MESH"} and prefs.uv_support_enable

	def draw(self, _):
		layout = self.layout

		box = layout.box()
		row = box.row(align=True)
		row.operator(operators.ShowAddonPrefs.bl_idname, text="Prefs", icon='PREFERENCES')
		row.operator(operators.OpenURL.bl_idname, text="Docs", icon='HELP').url = constants.ACT_DOC_URL
		row.operator(operators.OpenURL.bl_idname, text="Report", icon='URL').url = constants.ACT_REPORT_URL


classes = (
	VIEW3D_PT_act_support_panel,
	UV_PT_act_support_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)