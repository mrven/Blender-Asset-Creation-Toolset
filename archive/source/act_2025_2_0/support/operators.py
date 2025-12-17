import bpy
import webbrowser

from ..common import utils as common_utils

class OpenURL(bpy.types.Operator):
	"""Open URL in web-browser"""
	bl_idname = "object.act_open_url"
	bl_label = "Open URL"

	url: bpy.props.StringProperty(
		name="URL",
		description="Destination URL",
		default="https://blender.org"
	)

	def execute(self, _):
		try:
			webbrowser.open(self.url)
			return {'FINISHED'}
		except Exception as e:
			print(f"[ERROR] Failed to Open URL {self.url}: {e}")
			return {'CANCELLED'}


class ShowAddonPrefs(bpy.types.Operator):
	"""Open addon preferences"""
	bl_idname = "object.act_show_addon_prefs"
	bl_label = "Open Addon Preferences"

	def execute(self, _):
		addon_name = common_utils.get_package_name()
		bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
		bpy.context.preferences.active_section = 'ADDONS'
		bpy.ops.preferences.addon_show(module=addon_name)

		return {'FINISHED'}

classes = (
	OpenURL,
	ShowAddonPrefs,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)