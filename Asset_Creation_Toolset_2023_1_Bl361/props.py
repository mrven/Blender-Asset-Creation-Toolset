import bpy

from bpy.props import (
	StringProperty,
	EnumProperty,
	BoolProperty,
	PointerProperty,
	FloatProperty,
	IntProperty,
)


class ACT_Addon_Props(bpy.types.PropertyGroup):
	# Palette props
	save_dir: StringProperty(
		name="",
		description="Save Directory",
		default="")
	custom_save_path: BoolProperty(
		name="Custom Save Path",
		description="Custom Save Path",
		default=False)
	pbr_workflow: BoolProperty(
		name="PBR Workflow",
		description="PBR Workflow",
		default=False)

	save_path: StringProperty(
		name="",
		default="",
		description="Path for Save Palettes",
		subtype='DIR_PATH'
	)

	# Export props
	export_dir: StringProperty(
		name="",
		description="Export Directory",
		default="")

	fbx_export_mode_menu_items = (
		('INDIVIDUAL', '1 Obj->1 FBX', ''),
		('ALL', 'All->One FBX', ''),
		('PARENT', 'By Parent', ''),
		('COLLECTION', 'By Collection', ''))
	fbx_export_mode: EnumProperty(name="", items=fbx_export_mode_menu_items)

	export_format_menu_items = (
		('FBX', 'FBX', ''),
		('OBJ', 'OBJ', ''))
	export_format: EnumProperty(name="", items=export_format_menu_items)

	obj_separate_by_materials: BoolProperty(
		name="Separate By Materials",
		description="Separate Objects By Materials",
		default=True)

	obj_export_smooth_groups: BoolProperty(
		name="Smooth Groups",
		description="Export Smooth Groups",
		default=True)

	apply_rot: BoolProperty(
		name="Apply Rotation",
		description="Apply Rotation for Exported Models",
		default=True)

	apply_rot_rotated: BoolProperty(
		name="Apply for Rotated Objects",
		description="Apply Rotation for Objects with not 0,0,0 rotation",
		default=True)

	apply_scale: BoolProperty(
		name="Apply Scale",
		description="Apply Scale for Exported Models",
		default=True)

	apply_loc: BoolProperty(
		name="Apply Location",
		description="Apply Location for Exported Models",
		default=True)

	set_custom_fbx_name: BoolProperty(
		name="Set Custom Name for FBX",
		description="Set Custom Name for FBX",
		default=False)

	custom_fbx_name: StringProperty(
		name="",
		description="Custom Name for FBX",
		default="")

	custom_export_path: BoolProperty(
		name="Custom Export Path",
		description="Custom Export Path",
		default=False)

	delete_mats_before_export: BoolProperty(
		name="Delete Materials",
		description="Delete Materials before Export",
		default=False)

	triangulate_before_export: BoolProperty(
		name="Triangulate",
		description="Triangulate Meshes before Export",
		default=False)

	export_path: StringProperty(
		name="",
		default="",
		description="Path for Export FBX",
		subtype='DIR_PATH'
	)

	# Custom FBX Export Options
	export_custom_options: BoolProperty(
		name="Custom Export Options",
		description="Custom FBX Export Options",
		default=False)

	export_loose_edges: BoolProperty(
		name="Loose Edges",
		description="Loose Edges",
		default=False)

	export_tangent_space: BoolProperty(
		name="Tangent Space",
		description="Tangent Space",
		default=False)

	export_smoothing_items = (
		('OFF', 'Normals Only', ''),
		('FACE', 'Face', ''),
		('EDGE', 'Edge', ''))
	export_smoothing: EnumProperty(name="", items=export_smoothing_items)

	# Export FBX Target Engine
	export_target_engine_items = (
		('UNITY2023', 'Unity', ''),
		('UNREAL', 'Unreal', ''),
		('UNITY', 'Unity (Legacy)', ''))
	export_target_engine: EnumProperty(name="", items=export_target_engine_items)

	export_combine_meshes: BoolProperty(
		name="Combine Meshes before Export",
		description="Combine Meshes before Export",
		default=False)

	export_add_leaf_bones: BoolProperty(
		name="Add Leaf Bones",
		description="Add Leaf Bones",
		default=False)

	# Export Linear/sRGB color space for VC
	export_vc_color_space_items = (
		('LINEAR', 'Linear', ''),
		('SRGB', 'sRGB', ''))
	export_vc_color_space: EnumProperty(name="", items=export_vc_color_space_items)

	# Custom Import Options
	import_custom_options: BoolProperty(
		name="Custom Import Options",
		description="Custom FBX/OBJ Import Options",
		default=False)

	import_normals: BoolProperty(
		name="Import Normals/Smooth Groups",
		description="Import Normals/Smooth Groups",
		default=True)

	import_animation: BoolProperty(
		name="Import Animation",
		description="Import Animation",
		default=True)

	import_automatic_bone_orientation: BoolProperty(
		name="Automatic Bone Orientation",
		description="Automatic Bone Orientation",
		default=True)

	import_ignore_leaf_bones: BoolProperty(
		name="Ignore Leaf Bones",
		description="Ignore Leaf Bones",
		default=False)

	# Rename props
	delete_nums: BoolProperty(
		name="Delete Blender Nums",
		description="Delete Blender Numbers from Object Names",
		default=True)

	delete_prev_nums: BoolProperty(
		name="Delete Previous Nums",
		description="Delete Previous Numbers from Object Names",
		default=True)

	nums_method_items = (
		('ALONG_X', 'Along X', ''),
		('ALONG_Y', 'Along Y', ''),
		('ALONG_Z', 'Along Z', ''),
		('SIMPLE', 'Simple', ''),
		('NONE', 'None', ''))
	nums_method: EnumProperty(name="", items=nums_method_items)

	nums_format_items = (
		('NO_ZEROS', '_X, _XX, _XXX', ''),
		('ONE_ZERO', '_0X, _XX, _XXX', ''),
		('TWO_ZEROS', '_00X, _0XX, _XXX', ''))
	nums_format: EnumProperty(name="", items=nums_format_items)

	# Origin tools props
	align_co: FloatProperty(
		name="",
		description="Coordinate",
		default=0.00,
		min=-9999,
		max=9999,
		step=50)

	align_geom_to_orig: BoolProperty(
		name="Geometry To Origin",
		description="Align Geometry To Origin",
		default=False)

	# UV tools props
	uv_move_factor_items = (
		('1', '2', ''),
		('2', '4', ''),
		('3', '8', ''),
		('4', '16', ''),
		('5', '32', ''))
	uv_move_factor: EnumProperty(name="", items=uv_move_factor_items, default='3')

	uv_index_rename: IntProperty(
		name="UV Index",
		description="UV Index",
		default=0,
		min=0,
		max=10)

	uv_name_rename: StringProperty(
		name="",
		description="UV Name",
		default="")

	uv_name_add: StringProperty(
		name="",
		description="UV Name",
		default="")

	# Other tools props
	normals_inside: BoolProperty(
		name="Inside Normals",
		description="Recalculate Normals Inside",
		default=False)

	calc_normals_en: BoolProperty(
		name="Recalc Normals",
		description="Recalculate Normals",
		default=False)

	# Merge bones - Delete or Dissolve
	merge_bones_method_items = (
		('DELETE', 'Delete', ''),
		('DISSOLVE', 'Dissolve', ''))
	merge_bones_method: EnumProperty(name="", items=merge_bones_method_items)

	# Add Collection name to objects name or Replace
	col_to_obj_name_method_items = (
		('ADD', 'Add', 'Add Collection name to current object name'),
		('REPLACE', 'Replace', 'Replace current object name to {Collection}_{Type}_{Num}'))
	col_to_obj_name_method: EnumProperty(name="", items=col_to_obj_name_method_items)

	# Where Place the collection name
	col_name_position_items = (
		('START', 'To Start', 'Add Collection name to beginning of object name'),
		('END', 'To End', 'Add Collection name to end of object name'))
	col_name_position: EnumProperty(name="", items=col_name_position_items)

	# Style of type's spelling (Mesh or MESH)
	col_name_type_style_items = (
		('DEFAULT', 'Default', 'Example: Collection_Mesh_001'),
		('CAPITAL', 'CAPITAL', 'Example: Collection_MESH_001'))
	col_name_type_style: EnumProperty(name="", items=col_name_type_style_items)

	# Debug Property
	debug: BoolProperty(
		name="Enable Debug Mode",
		description="Enable Debug Mode",
		default=False)

classes = (
	ACT_Addon_Props,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.act = PointerProperty(type=ACT_Addon_Props)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.act
