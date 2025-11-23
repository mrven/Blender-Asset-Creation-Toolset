import bpy
from bpy.props import (
	StringProperty,
	BoolProperty,
	EnumProperty,
	FloatProperty,
	IntProperty)

from . import utils
from . import config_json
from .constants import *

PANELS_TO_UPDATE = {
	"VIEW3D_PT_act_support_panel": "view3d_support_panel_category",
	"UV_PT_act_support_panel": "uv_support_panel_category",
	"VIEW3D_PT_act_origin_tools_panel": "origin_panel_category",
	"VIEW3D_PT_act_rename_tools_panel": "rename_panel_category",
    "VIEW3D_PT_act_uv_tools_panel": "view3d_uv_panel_category",
    "UV_PT_act_material_uv_tools_panel": "uv_material_panel_category",
	"UV_PT_act_uv_mover_panel": "uv_uv_category",
    "VIEW3D_PT_act_import_export_tools_panel": "export_import_panel_category",
    "VIEW3D_PT_act_material_tools_panel": "material_panel_category",
    "VIEW3D_PT_act_other_tools_panel": "other_panel_category",
	"VIEW3D_PT_act_geometry_tools_panel": "geometry_panel_category",
}

package_name = utils.get_package_name()

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

# region Panels
	view3d_support_enable: BoolProperty(
		name="ACT Support (3D View)",
		description="Show/Hide Support (3D View) UI Panel",
		default=True)

	uv_support_enable: BoolProperty(
		name="ACT Support (UV Editor)",
		description="Show/Hide Support (UV Editor) UI Panel",
		default=True)

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
# endregion
# region Panel Categories
	view3d_support_panel_category: StringProperty(
		description="Choose a name for the category of the Support (3D View) panel",
		default="ACT",
		update=update_panel_categories
	)

	uv_support_panel_category: StringProperty(
		description="Choose a name for the category of the Support (UV Editor) panel",
		default="ACT",
		update=update_panel_categories
	)

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
# endregion
# region Common Settings
	show_export_axis_tooltip: BoolProperty(
		name="",
		description="Show/Hide Export Axes Conversion Tooltip for UE/Unity",
		default=True)
# endregion
# region Defaults
	# Export
	export_mode: EnumProperty(name="", items=EXPORT_MODE_ITEMS)
	export_format: EnumProperty(name="", items=EXPORT_FORMAT_ITEMS)
	obj_separate_by_materials: BoolProperty(name="", default=True)
	obj_export_smooth_groups: BoolProperty(name="", default=True)
	gltf_export_image_format: EnumProperty(name="", items=GLTF_IMAGE_FORMAT_ITEMS)
	gltf_export_attributes: BoolProperty(name="")
	apply_rot: BoolProperty(name="", default=True)
	apply_rot_rotated: BoolProperty(name="", default=True)
	apply_scale: BoolProperty(name="", default=True)
	apply_loc: BoolProperty(name="", default=True)
	set_custom_fbx_name: BoolProperty(name="")
	custom_fbx_name: StringProperty(name="")
	delete_mats_before_export: BoolProperty(name="")
	triangulate_before_export: BoolProperty(name="")
	custom_export_path: BoolProperty(name="")
	export_path: StringProperty(name="", subtype="DIR_PATH")
	export_target_engine: EnumProperty(name="", items=EXPORT_TARGET_ENGINE_ITEMS)
	# Custom Export Options props
	export_custom_options: BoolProperty(name="")
	export_loose_edges: BoolProperty(name="")
	export_tangent_space: BoolProperty(name="")
	export_smoothing: EnumProperty(name="", items=EXPORT_SMOOTHING_ITEMS)
	export_custom_props: BoolProperty(name="", default=True)
	export_combine_meshes: BoolProperty(name="")
	export_only_deform_bones: BoolProperty(name="")
	export_add_leaf_bones: BoolProperty(name="")
	export_vc_color_space: EnumProperty(name="", items=EXPORT_VC_COLOR_SPACE_ITEMS)
	use_custom_export_scale: BoolProperty(name="")
	custom_export_scale_value: FloatProperty(name="", default=1.00, min=0.00001, max=9999, step=1)
	use_custom_export_axes: BoolProperty(name="")
	custom_export_forward_axis: EnumProperty(name="", default="-Z", items=EXPORT_AXIS_ITEMS)
	custom_export_up_axis: EnumProperty(name="", default="Y", items=EXPORT_AXIS_ITEMS)
	# Origin
	align_geom_to_orig: BoolProperty(name="")
	align_co: FloatProperty(name="", min=-9999, max=9999, step=50)
	# Rename
	delete_prev_nums: BoolProperty(name="", default=True)
	nums_method: EnumProperty(name="", items=NUMBERING_METHOD_ITEMS)
	nums_format: EnumProperty(name="", items=NUMBERING_FORMAT_ITEMS)
	lod_level: IntProperty(name="", min=0, max=9)
	# UV
	# Material
	# Other
# endregion
# region Show/Hide Preferences Groups
	show_panels_prefs: BoolProperty(name="", default=False)
	show_default_export: BoolProperty(name="", default=False)
	show_default_origin: BoolProperty(name="", default=False)
	show_default_rename: BoolProperty(name="", default=False)
	show_default_uv: BoolProperty(name="", default=False)
	show_default_material: BoolProperty(name="", default=False)
	show_default_other: BoolProperty(name="", default=False)
# endregion

	def draw(self, _):
		layout = self.layout
		box = layout.box()
		row = box.row(align=True)
		row.prop(self, "show_panels_prefs", icon = "TRIA_DOWN" if self.show_panels_prefs else "TRIA_RIGHT")
		row.label(text="  Visibility and Category for Panels")
		if self.show_panels_prefs:
			row = box.row(align=True)
			row.prop(self, "view3d_support_enable")
			if self.view3d_support_enable:
				row.prop(self, "view3d_support_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "uv_support_enable")
			if self.uv_support_enable:
				row.prop(self, "uv_support_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "origin_enable")
			if self.origin_enable:
				row.prop(self, "origin_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "renaming_enable")
			if self.renaming_enable:
				row.prop(self, "rename_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "uv_view3d_enable")
			if self.uv_view3d_enable:
				row.prop(self, "view3d_uv_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "uv_uv_enable")
			if self.uv_uv_enable:
				row.prop(self, "uv_uv_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "export_import_enable")
			if self.export_import_enable:
				row.prop(self, "export_import_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "material_enable")
			if self.material_enable:
				row.prop(self, "material_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "uv_material_enable")
			if self.uv_material_enable:
				row.prop(self, "uv_material_panel_category", text="Panel")

			row = box.row()
			row.prop(self, "material_properties_enable")

			row = box.row(align=True)
			row.prop(self, "other_enable")
			if self.other_enable:
				row.prop(self, "other_panel_category", text="Panel")

			row = box.row(align=True)
			row.prop(self, "geometry_enable")
			if self.geometry_enable:
				row.prop(self, "geometry_panel_category", text="Panel")

		box = layout.box()
		row = box.row()
		row.label(text="Common Settings:")
		row = box.row(align=True)
		row.label(text="Show Export Axes for UE/Unity Tooltip")
		row.prop(self, "show_export_axis_tooltip")

		box = layout.box()
		row = box.row()
		row.label(text='Default Settings:')
		row = box.row(align=True)
		row.prop(self, "show_default_export", icon="TRIA_DOWN" if self.show_default_export else "TRIA_RIGHT")
		row.label(text="  Export Tools")
		if self.show_default_export:
			row = box.row(align=True)
			row.label(text="Export Mode")
			row.prop(self, "export_mode")
			row = box.row(align=True)
			row.label(text="File Format")
			row.prop(self, "export_format")
			if self.export_format == "FBX":
				row = box.row(align=True)
				row.label(text="Target Engine")
				row.prop(self, "export_target_engine")
			if not (self.export_format == "OBJ" and self.export_mode in {"ALL", "COLLECTION"}):
				row = box.row(align=True)
				row.label(text="Apply")
				if self.export_format in {"FBX", "GLTF"}:
					if self.apply_rot:
						row.prop(self, "apply_rot", text="Rotation", icon="CHECKBOX_HLT")
					else:
						row.prop(self, "apply_rot", text="Rotation", icon="CHECKBOX_DEHLT")
					if self.apply_scale:
						row.prop(self, "apply_scale", text="Scale", icon="CHECKBOX_HLT")
					else:
						row.prop(self, "apply_scale", text="Scale", icon="CHECKBOX_DEHLT")
				if self.export_mode in {"INDIVIDUAL", "PARENT"}:
					if self.apply_loc:
						row.prop(self, "apply_loc", text="Location", icon="CHECKBOX_HLT")
					else:
						row.prop(self, "apply_loc", text="Location", icon="CHECKBOX_DEHLT")
				if self.export_format == "FBX":
					if self.apply_rot and self.export_mode == "PARENT" and self.export_target_engine != "UNITY":
						row = box.row(align=True)
						row.label(text="Apply for Rotated Objects")
						row.prop(self, "apply_rot_rotated")
				row = box.row(align=True)
				row.label(text="Delete All Materials")
				row.prop(self, "delete_mats_before_export")
				if self.export_mode != "INDIVIDUAL":
					row = box.row(align=True)
					row.label(text="Combine All Meshes")
					row.prop(self, "export_combine_meshes")
				row = box.row(align=True)
				row.label(text="Triangulate Meshes")
				row.prop(self, "triangulate_before_export")
				if self.export_mode == "ALL":
					local_box = box.box()
					row = local_box.row(align=True)
					row.label(text="Custom Name for File")
					row.prop(self, "set_custom_fbx_name")
					if self.set_custom_fbx_name:
						row = local_box.row(align=True)
						row.label(text="    File Name")
						row.prop(self, "custom_fbx_name")
				# Custom Export Options
				local_box = box.box()
				row = local_box.row(align=True)
				row.label(text="Custom Export Options")
				row.prop(self, "export_custom_options")
				if self.export_custom_options:
					if self.export_format == "FBX":
						row = local_box.row(align=True)
						row.label(text="    Smoothing")
						row.prop(self, "export_smoothing")
						row = local_box.row(align=True)
						row.label(text="    Loose Edges")
						row.prop(self, "export_loose_edges")
						row = local_box.row(align=True)
						row.label(text="    Tangent Space")
						row.prop(self, "export_tangent_space")
						row = local_box.row(align=True)
						row.label(text="    Only Deform Bones")
						row.prop(self, "export_only_deform_bones")
						row = local_box.row(align=True)
						row.label(text="    Add Leaf Bones")
						row.prop(self, "export_add_leaf_bones")
						row = local_box.row(align=True)
						row.label(text="    VC color space")
						row.prop(self, "export_vc_color_space", expand=False)
						row = local_box.row(align=True)
						row.label(text="    Custom Properties")
						row.prop(self, "export_custom_props")
					if self.export_format == "OBJ":
						row = local_box.row(align=True)
						row.label(text="    Separate By Mats")
						row.prop(self, "obj_separate_by_materials")
						row = local_box.row(align=True)
						row.label(text="    Smooth Groups")
						row.prop(self, "obj_export_smooth_groups")
					if self.export_format in {"FBX", "OBJ"}:
						row = local_box.row(align=True)
						row.label(text="    Use Custom Scale")
						row.prop(self, "use_custom_export_scale")
						if self.use_custom_export_scale:
							row = local_box.row(align=True)
							row.label(text="      Scale")
							row.prop(self, "custom_export_scale_value")
						row = local_box.row(align=True)
						row.label(text="    Use Custom Axes")
						row.prop(self, "use_custom_export_axes")
						if self.use_custom_export_axes:
							row = local_box.row(align=True)
							row.label(text="      Forward")
							row.prop(self, "custom_export_forward_axis", expand=False)
							row = local_box.row(align=True)
							row.label(text="      Up")
							row.prop(self, "custom_export_up_axis", expand=False)
					if self.export_format == "GLTF":
						row = local_box.row(align=True)
						row.label(text="    Pack Images")
						row.prop(self, "gltf_export_image_format")

						row = local_box.row(align=True)
						row.label(text="    Deform Bones Only")
						row.prop(self, "export_only_deform_bones")

						row = local_box.row(align=True)
						row.label(text="    Custom Properties")
						row.prop(self, "export_custom_props")

						row = local_box.row(align=True)
						row.label(text="    Tangents")
						row.prop(self, "export_tangent_space")

						row = local_box.row(align=True)
						row.label(text="    Attributes")
						row.prop(self, "gltf_export_attributes")
				# Custom Export Path
				local_box = box.box()
				row = local_box.row(align=True)
				row.label(text="Custom Export Path")
				row.prop(self, "custom_export_path")
				if self.custom_export_path:
					row = local_box.row(align=True)
					row.label(text="    Export Path")
					row.prop(self, "export_path")

		row = box.row(align=True)
		row.prop(self, "show_default_origin", icon="TRIA_DOWN" if self.show_default_origin else "TRIA_RIGHT")
		row.label(text="  Origin Tools")
		if self.show_default_origin:
			row = box.row(align=True)
			row.label(text="Geometry To Origin")
			row.prop(self, "align_geom_to_orig")
			row = box.row(align=True)
			row.label(text="Coordinate")
			row.prop(self, "align_co")

		row = box.row(align=True)
		row.prop(self, "show_default_rename", icon="TRIA_DOWN" if self.show_default_rename else "TRIA_RIGHT")
		row.label(text="  Renaming Tools")
		if self.show_default_rename:
			local_box = box.box()
			row = local_box.row(align=True)
			row.label(text="Method")
			row.prop(self, "nums_method", expand=False)
			row = local_box.row(align=True)
			row.label(text="Format")
			row.prop(self, "nums_format", expand=False)
			row = local_box.row(align=True)
			row.label(text="Delete Previous Nums")
			row.prop(self, "delete_prev_nums")
			local_box = box.box()
			row = local_box.row(align=True)
			row.label(text="LOD Level")
			row.prop(self, "lod_level")

		row = box.row(align=True)
		row.prop(self, "show_default_uv", icon="TRIA_DOWN" if self.show_default_uv else "TRIA_RIGHT")
		row.label(text="  UV Tools")
		if self.show_default_uv:
			row = box.row(align=True)
			row.label(text="Export Mode")
			row.prop(self, "export_mode")

		row = box.row(align=True)
		row.prop(self, "show_default_material", icon="TRIA_DOWN" if self.show_default_material else "TRIA_RIGHT")
		row.label(text="  Material/Texture Tools")
		if self.show_default_material:
			row = box.row(align=True)
			row.label(text="Export Mode")
			row.prop(self, "export_mode")

		row = box.row(align=True)
		row.prop(self, "show_default_other", icon="TRIA_DOWN" if self.show_default_other else "TRIA_RIGHT")
		row.label(text="  Other Tools")
		if self.show_default_other:
			row = box.row(align=True)
			row.label(text="Export Mode")
			row.prop(self, "export_mode")

		box.separator(factor=0.5)
		row = box.row()
		row.operator(ApplyDefaultsToProps.bl_idname, icon='PRESET')

		layout.separator(factor=0.5)
		row = layout.row()
		row.operator(ResetPreferences.bl_idname, icon='FILE_REFRESH')


class ResetPreferences(bpy.types.Operator):
	"""Reset all preferences to default values"""
	bl_idname = "object.act_reset_preferences"
	bl_label = "Reset Preferences"

	def execute(self, _):
		success = config_json.apply_defaults_from_file()

		if success:
			self.report({'INFO'}, "Preferences was successfully reset")
		else:
			self.report({'ERROR'}, "Failed to reset preferences")
		return {'FINISHED'}


class ApplyDefaultsToProps(bpy.types.Operator):
	"""Apply current defaults from preferences to props"""
	bl_idname = "object.act_apply_defaults_to_props"
	bl_label = "Copy Default Settings To Current Session"

	def execute(self, _):
		config_json.copy_prefs_to_props(force=True)
		return {'FINISHED'}


classes = (
	ApplyDefaultsToProps,
	ResetPreferences,
	ACTAddonPreferences,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
