import bpy

from bpy.props import (
	StringProperty,
	EnumProperty,
	BoolProperty,
	PointerProperty,
	FloatProperty,
	IntProperty,
)

from .constants import *

# region Update Functions
def update_custom_forward_axis(_, context):
	act = context.scene.act
	if act.custom_export_forward_axis == act.custom_export_up_axis:
		# Get Current item index
		index = 0
		for i in range(len(act.custom_export_axis_items)):
			if act.custom_export_up_axis == act.custom_export_axis_items[i][0]:
				index = i

		if index < len(act.custom_export_axis_items) - 1:
			index += 1
		else:
			index = 0
		act.custom_export_up_axis = act.custom_export_axis_items[index][0]


def update_custom_up_axis(_, context):
	act = context.scene.act
	if act.custom_export_forward_axis == act.custom_export_up_axis:
		# Get Current item index
		index = 0
		for i in range(len(act.custom_export_axis_items)):
			if act.custom_export_forward_axis == act.custom_export_axis_items[i][0]:
				index = i

		if index < len(act.custom_export_axis_items) - 1:
			index += 1
		else:
			index = 0
		act.custom_export_forward_axis = act.custom_export_axis_items[index][0]
# endregion


class ACTAddonProps(bpy.types.PropertyGroup):
# region Palette props
	save_dir: StringProperty(name="", description="Save Directory")

	custom_save_path: BoolProperty(description="Custom Save Path")

	pbr_workflow: BoolProperty(description="PBR Workflow")

	save_path: StringProperty(name="", description="Path for Save Palettes", subtype="DIR_PATH")
#endregion

#region Export props
	export_dir: StringProperty(name="", description="Export Directory")

	export_mode: EnumProperty(name="", items=EXPORT_MODE_ITEMS)

	export_format: EnumProperty(name="", items=EXPORT_FORMAT_ITEMS)

	obj_separate_by_materials: BoolProperty(name="", description="Separate Objects By Materials", default=True)

	obj_export_smooth_groups: BoolProperty(name="", description="Export Smooth Groups", default=True)

	gltf_export_image_format: EnumProperty(name="", items=GLTF_IMAGE_FORMAT_ITEMS)

	gltf_export_attributes: BoolProperty(name="", description="Export Attributes")

	apply_rot: BoolProperty(description="Apply Rotation for Exported Models", default=True)

	apply_rot_rotated: BoolProperty(description="Apply Rotation for Objects with not 0,0,0 rotation", default=True)

	apply_scale: BoolProperty(description="Apply Scale for Exported Models", default=True)

	apply_loc: BoolProperty(description="Apply Location for Exported Models", default=True)

	set_custom_fbx_name: BoolProperty(description="Set Custom Name for FBX")

	custom_fbx_name: StringProperty(name="", description="Custom Name for FBX")

	custom_export_path: BoolProperty(description="Custom Export Path")

	delete_mats_before_export: BoolProperty(description="Delete Materials before Export")

	triangulate_before_export: BoolProperty(description="Triangulate Meshes before Export")

	export_path: StringProperty(name="", description="Path for Export FBX", subtype="DIR_PATH")

	#Custom Export Options props
	export_custom_options: BoolProperty(description="Custom FBX Export Options")

	export_loose_edges: BoolProperty(name="", description="Loose Edges")

	export_tangent_space: BoolProperty(name="", description="Tangent Space")

	export_smoothing: EnumProperty(name="", items=EXPORT_SMOOTHING_ITEMS)

	export_custom_props: BoolProperty(name="", description="Custom Props", default=True)

	# Export FBX Target Engine
	export_target_engine: EnumProperty(name="", items=EXPORT_TARGET_ENGINE_ITEMS)

	export_combine_meshes: BoolProperty(description="Combine Meshes before Export")

	export_only_deform_bones: BoolProperty(name="", description="Only Deform Bones")

	export_add_leaf_bones: BoolProperty(name="", description="Add Leaf Bones")

	# Export Linear/sRGB color space for VC
	export_vc_color_space: EnumProperty(name="", items=EXPORT_VC_COLOR_SPACE_ITEMS)

	# Use Custom Scale (for OBJ/FBX)
	use_custom_export_scale: BoolProperty(name="", description="Set custom scale for export")

	custom_export_scale_value: FloatProperty(name="", description="Scale", default=1.00, min=0.00001, max=9999, step=1)

	# Use Custom Forward/Up Axes
	use_custom_export_axes: BoolProperty(name="", description="Set custom Forward/Up axes")

	# Custom Forward Axis
	custom_export_forward_axis: EnumProperty(name="", default="-Z", items=EXPORT_AXIS_ITEMS,
	                                         update=update_custom_forward_axis)

	# Custom Up Axis
	custom_export_up_axis: EnumProperty(name="", default="Y", items=EXPORT_AXIS_ITEMS, update=update_custom_up_axis)
#endregion

#region Rename props
	delete_prev_nums: BoolProperty(description="Delete Previous Numbers from Object Names", default=True)

	nums_method: EnumProperty(name="", items=NUMBERING_METHOD_ITEMS)

	nums_format: EnumProperty(name="", items=NUMBERING_FORMAT_ITEMS)

	lod_level: IntProperty(description="LOD Level", min=0, max=9)
#endregion

#region Origin tools props
	align_co: FloatProperty( description="Coordinate", min=-9999, max=9999, step=50)

	align_geom_to_orig: BoolProperty(description="Align Geometry To Origin")
#endregion

#region UV tools props
	uv_move_factor: EnumProperty(name="", items=UV_MOVE_FACTOR_ITEMS, default="3")

	uv_index_rename: IntProperty(description="UV Index", min=0, max=10)

	uv_name_rename: StringProperty(name="", description="UV Name")

	uv_name_add: StringProperty(name="", description="UV Name")

	uv_packing_mode: EnumProperty(name="", items=UV_PACKING_ITEMS)

	uv_packing_smart_angle: FloatProperty(description="Project Angle Limit", default=66, min=0, max=89, step=1)

	uv_packing_smart_margin: FloatProperty(description="Project Islands Margin", min=0, max=1, step=1)

	uv_packing_lightmap_quality: IntProperty(description="Packing Quality", default=32, min=1, max=48, step=1)

	uv_packing_lightmap_margin: FloatProperty(description="Project Islands Margin", default=0.3, min=0, max=1,
	                                          step=1)
#endregion

#region Other tools props
	normals_inside: BoolProperty(description="Recalculate Normals Inside")

	calc_normals_en: BoolProperty(description="Recalculate Normals")

	# Merge bones - Delete or Dissolve
	merge_bones_method: EnumProperty(name="", items=MERGE_BONES_METHOD_ITEMS)

	# Add Collection name to objects name or Replace
	col_to_obj_name_method: EnumProperty(name="", items=COL_TO_OBJ_NAME_METHOD_ITEMS)

	# Where Place the collection name
	col_name_position: EnumProperty(name="", items=COL_NAME_POSITION_ITEMS)

	# Style of type's spelling (Mesh or MESH)

	col_name_type_style: EnumProperty(name="", items=COL_NAME_STYLE_ITEMS)

	# Cleanup Empties: Also delete empty meshes
	delete_empty_meshes: BoolProperty(description="Also delete empty meshes", default=True)
#endregion

#region Debug props
	debug: BoolProperty(description="Enable Debug Mode")
#endregion

classes = (
	ACTAddonProps,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.act = PointerProperty(type=ACTAddonProps)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.act
