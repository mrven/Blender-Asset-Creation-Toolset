import bpy

from bpy.props import (
		StringProperty,
		EnumProperty,
		BoolProperty
		)

from . import import_export_tools

'''
def update_export_import_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_Import_Export_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.export_import_panel_category

	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_Import_Export_Tools_Panel)
		except:
			pass
	VIEW3D_Import_Export_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_Import_Export_Tools_Panel)
'''

class ACT_Addon_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	export_import_enable: BoolProperty(
		name="Import/Export Tools",
		description="Show/Hide Import/Export Tools UI Panel",
		default=True)

	material_enable: BoolProperty(
		name="Material/Texture Tools",
		description="Show/Hide Material/Texture Tools UI Panel",
		default=True)

	origin_enable: BoolProperty(
		name="Origin Tools",
		description="Show/Hide Origin Tools UI Panel",
		default=True)

	other_enable: BoolProperty(
		name="Other Tools",
		description="Show/Hide Other Tools UI Panel",
		default=True)

	uv_view3d_enable: BoolProperty(
		name="UV Tools (3D View)",
		description="Show/Hide UV Tools (3D View) UI Panel",
		default=True)

	uv_uv_enable: BoolProperty(
		name="UV Tools (UV Editor) Tools",
		description="Show/Hide UV Tools (UV Editor) UI Panel",
		default=True)

	renaming_enable: BoolProperty(
		name="Renaming Tools",
		description="Show/Hide Renaming Tools UI Panel",
		default=True)

	material_properties_enable: BoolProperty(
		name="Material (Properties) Tools",
		description="Show/Hide Import/Export Material (Properties) UI Panel",
		default=True)

	export_import_panel_category: StringProperty(
		description="Choose a name for the category of the Import/Export panel",
		default="ACT"
		)

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text='Visibility of Addon UI Panels:')
		
		box = layout.box()
		row = box.row()
		row.prop(self, 'export_import_enable')
		row = box.row(align=True)
		row.label(text='    Import/Export Panel Category:')
		row.prop(self, 'export_import_panel_category', text="")
		
		row = layout.row()
		row.prop(self, 'material_enable')
		row = layout.row()
		row.prop(self, 'origin_enable')
		row = layout.row()
		row.prop(self, 'other_enable')
		row = layout.row()
		row.prop(self, 'uv_view3d_enable')
		row = layout.row()
		row.prop(self, 'uv_uv_enable')
		row = layout.row()
		row.prop(self, 'renaming_enable')
		row = layout.row()
		row.prop(self, 'material_properties_enable')

classes = (
	ACT_Addon_Preferences,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)