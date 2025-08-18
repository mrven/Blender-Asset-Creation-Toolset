import bpy

from bpy.props import (
	StringProperty,
	BoolProperty)

PANELS_TO_UPDATE = {
	"VIEW3D_PT_origin_tools_panel": "origin_panel_category",
	"VIEW3D_PT_rename_tools_panel": "rename_panel_category",
    "VIEW3D_PT_uv_tools_panel": "view3d_uv_panel_category",
    "UV_PT_material_uv_tools_panel": "uv_material_panel_category",
	"UV_PT_uv_mover_panel": "uv_uv_category",
    "VIEW3D_PT_import_export_tools_panel": "export_import_panel_category",
    "VIEW3D_PT_material_tools_panel": "material_panel_category",
    "VIEW3D_PT_other_tools_panel": "other_panel_category",


}

package_name = __package__.split('.')[0]

def update_panel_categories(_, context):
	prefs = context.preferences.addons[package_name].preferences

	for panel_name, pref_attr in PANELS_TO_UPDATE.items():
		panel_cls = getattr(bpy.types, panel_name)
		category = getattr(prefs, pref_attr, None)

		if not category:
			continue

		try:
			bpy.utils.unregister_class(panel_cls)
		except RuntimeError:
			pass

		panel_cls.bl_category = category
		bpy.utils.register_class(panel_cls)


class ACTAddonPreferences(bpy.types.AddonPreferences):
	bl_idname = package_name

	export_import_enable: BoolProperty(
		name="Import/Export Tools",
		description="Show/Hide Import/Export Tools UI Panel",
		default=True)

	material_enable: BoolProperty(
		name="Material/Texture Tools (3D View)",
		description="Show/Hide Material/Texture Tools (3D View) UI Panel",
		default=True)

	origin_enable: BoolProperty(
		name="Origin Tools",
		description="Show/Hide Origin Tools UI Panel",
		default=True)

	other_enable: BoolProperty(
		name="Other Tools",
		description="Show/Hide Other Tools UI Panel",
		default=True)

	geometry_enable: BoolProperty(
		name="Geometry Tools",
		description="Show/Hide Geometry Tools UI Panel",
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

	uv_material_enable: BoolProperty(
		name="Material/Texture Tools (Image Editor)",
		description="Show/Hide Material/Texture Tools (Image Editor) UI Panel",
		default=True)

	material_properties_enable: BoolProperty(
		name="Material (Properties) Tools",
		description="Show/Hide Export Material (Properties) UI Panel",
		default=True)

	export_import_panel_category: StringProperty(
		description="Choose a name for the category of the Export panel",
		default="ACT",
		update=update_panel_categories
	)

	material_panel_category: StringProperty(
		description="Choose a name for the category of the Material (3D View) panel",
		default="ACT",
		update=update_panel_categories
	)

	origin_panel_category: StringProperty(
		description="Choose a name for the category of the Origin panel",
		default="ACT",
		update=update_panel_categories
	)

	other_panel_category: StringProperty(
		description="Choose a name for the category of the Other panel",
		default="ACT",
		update=update_panel_categories
	)

	geometry_panel_category: StringProperty(
		description="Choose a name for the category of the Geometry panel",
		default="ACT",
		update=update_panel_categories
	)

	rename_panel_category: StringProperty(
		description="Choose a name for the category of the Rename panel",
		default="ACT",
		update=update_panel_categories
	)

	uv_uv_category: StringProperty(
		description="Choose a name for the category of the UV (UV Editor) panel",
		default="ACT",
		update=update_panel_categories
	)

	view3d_uv_panel_category: StringProperty(
		description="Choose a name for the category of the UV (3D View) panel",
		default="ACT",
		update=update_panel_categories
	)

	uv_material_panel_category: StringProperty(
		description="Choose a name for the category of the Material (Image Editor) panel",
		default="ACT",
		update=update_panel_categories
	)

	def draw(self, _):
		layout = self.layout
		row = layout.row()
		row.label(text='Visibility and Category for Panels:')

		box = layout.box()
		row = box.row(align=True)
		row.prop(self, 'origin_enable')
		if self.origin_enable:
			row.prop(self, 'origin_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'renaming_enable')
		if self.renaming_enable:
			row.prop(self, 'rename_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'uv_view3d_enable')
		if self.uv_view3d_enable:
			row.prop(self, 'view3d_uv_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'uv_uv_enable')
		if self.uv_uv_enable:
			row.prop(self, 'uv_uv_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'export_import_enable')
		if self.export_import_enable:
			row.prop(self, 'export_import_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'material_enable')
		if self.material_enable:
			row.prop(self, 'material_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'uv_material_enable')
		if self.uv_material_enable:
			row.prop(self, 'uv_material_panel_category', text="Panel")

		row = box.row()
		row.prop(self, 'material_properties_enable')

		row = box.row(align=True)
		row.prop(self, 'other_enable')
		if self.other_enable:
			row.prop(self, 'other_panel_category', text="Panel")

		row = box.row(align=True)
		row.prop(self, 'geometry_enable')
		if self.geometry_enable:
			row.prop(self, 'geometry_panel_category', text="Panel")


classes = (
	ACTAddonPreferences,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
