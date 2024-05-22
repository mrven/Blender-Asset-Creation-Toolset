import bpy

from bpy.props import (
		StringProperty,
		EnumProperty,
		BoolProperty
		)

from . import origin_tools, rename_tools, uv_tools, import_export_tools, material_tools, other_tools

from .origin_tools import VIEW3D_PT_Origin_Tools_Panel
from .rename_tools import VIEW3D_PT_Rename_Tools_Panel
from .uv_tools import UV_PT_UV_Mover_Panel, VIEW3D_PT_UV_Tools_Panel
from .import_export_tools import VIEW3D_PT_Import_Export_Tools_Panel
from .material_tools import VIEW3D_PT_Material_Tools_Panel, UV_PT_Material_UV_Tools_Panel
from .other_tools import VIEW3D_PT_Other_Tools_Panel


def update_export_import_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_Import_Export_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.export_import_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_Import_Export_Tools_Panel)
		except:
			pass
	VIEW3D_PT_Import_Export_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_Import_Export_Tools_Panel)


def update_material_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_Material_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.material_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_Material_Tools_Panel)
		except:
			pass
	VIEW3D_PT_Material_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_Material_Tools_Panel)


def update_origin_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_Origin_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.origin_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_Origin_Tools_Panel)
		except:
			pass
	VIEW3D_PT_Origin_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_Origin_Tools_Panel)


def update_other_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_Other_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.other_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_Other_Tools_Panel)
		except:
			pass
	VIEW3D_PT_Other_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_Other_Tools_Panel)


def update_rename_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_Rename_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.rename_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_Rename_Tools_Panel)
		except:
			pass
	VIEW3D_PT_Rename_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_Rename_Tools_Panel)


def update_uv_uv_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'UV_PT_UV_Mover_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.uv_uv_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(UV_PT_UV_Mover_Panel)
		except:
			pass
	UV_PT_UV_Mover_Panel.bl_category = category
	bpy.utils.register_class(UV_PT_UV_Mover_Panel)


def update_view3d_uv_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'VIEW3D_PT_UV_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.view3d_uv_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(VIEW3D_PT_UV_Tools_Panel)
		except:
			pass
	VIEW3D_PT_UV_Tools_Panel.bl_category = category
	bpy.utils.register_class(VIEW3D_PT_UV_Tools_Panel)


def update_uv_material_panel_category(self, context):
	is_panel = hasattr(bpy.types, 'UV_PT_Material_UV_Tools_Panel')
	category = bpy.context.preferences.addons[__package__].preferences.uv_material_panel_category
	
	if is_panel:
		try:
			bpy.utils.unregister_class(UV_PT_Material_UV_Tools_Panel)
		except:
			pass
	UV_PT_Material_UV_Tools_Panel.bl_category = category
	bpy.utils.register_class(UV_PT_Material_UV_Tools_Panel)
	

class ACT_Addon_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	export_import_enable: BoolProperty(
		name="Import/Export Tools",
		description="Show/Hide Import/Export Tools UI Panel",
		default=True)

	material_enable: BoolProperty(
		name="Material/Texture Tools",
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
		description="Show/Hide Import/Export Material (Properties) UI Panel",
		default=True)

	export_import_panel_category: StringProperty(
		description="Choose a name for the category of the Import/Export panel",
		default="ACT",
		update = update_export_import_panel_category
		)

	material_panel_category: StringProperty(
		description="Choose a name for the category of the Material (3D View) panel",
		default="ACT",
		update = update_material_panel_category
		)

	origin_panel_category: StringProperty(
		description="Choose a name for the category of the Origin panel",
		default="ACT",
		update = update_origin_panel_category
		)

	other_panel_category: StringProperty(
		description="Choose a name for the category of the Other panel",
		default="ACT",
		update = update_other_panel_category
		)

	rename_panel_category: StringProperty(
		description="Choose a name for the category of the Rename panel",
		default="ACT",
		update = update_rename_panel_category
		)

	uv_uv_category: StringProperty(
		description="Choose a name for the category of the UV (UV Editor) panel",
		default="ACT",
		update = update_uv_uv_panel_category
		)

	view3d_uv_panel_category: StringProperty(
		description="Choose a name for the category of the UV (3D View) panel",
		default="ACT",
		update = update_view3d_uv_panel_category
		)

	uv_material_panel_category: StringProperty(
		description="Choose a name for the category of the Material (Image Editor) panel",
		default="ACT",
		update = update_uv_material_panel_category
		)

	def draw(self, context):
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


classes = (
	ACT_Addon_Preferences,
	VIEW3D_PT_Origin_Tools_Panel,
	VIEW3D_PT_Rename_Tools_Panel,
	VIEW3D_PT_UV_Tools_Panel,
	VIEW3D_PT_Import_Export_Tools_Panel,
	VIEW3D_PT_Material_Tools_Panel,
	VIEW3D_PT_Other_Tools_Panel,
	UV_PT_UV_Mover_Panel,
	UV_PT_Material_UV_Tools_Panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# Update Category
	context = bpy.context
	prefs = bpy.context.preferences.addons[__package__].preferences
	update_origin_panel_category(prefs, context)
	update_rename_panel_category(prefs, context)
	update_view3d_uv_panel_category(prefs, context)
	update_export_import_panel_category(prefs, context)
	update_material_panel_category(prefs, context)	
	update_other_panel_category(prefs, context)	
	update_uv_uv_panel_category(prefs, context)
	update_uv_material_panel_category(prefs, context)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)