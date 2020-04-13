import bpy

from bpy.props import (
		StringProperty,
		EnumProperty,
        BoolProperty,
        PointerProperty,
        )


class ACTAddonProps(PropertyGroup):
	old_text: StringProperty(
		name="",
		description="Text for search",
		default="")
	
	new_text: StringProperty(
		name="",
		description="Text for replace",
		default="")

	export_dir: StringProperty(
		name="",
		description="Export Directory",
		default="")
		
	prefix: StringProperty(
		name="",
		description="Prefix Text",
		default="")
		
	postfix: StringProperty(
		name="",
		description="Postfix Text",
		default="")
	
	new_name: StringProperty(
		name="",
		description="New Name for Objects",
		default="")
	
	delete_nums: BoolProperty(
		name="Delete Blender Nums",
		description="Delete Blender Numbers from Object Names",
		default = True)
	
	delete_prev_nums: BoolProperty(
		name="Delete Previous Nums",
		description="Delete Previous Numbers from Object Names",
		default = True)
	
	align_co: FloatProperty(
		name="",
		description="Coordinate",
		default=0.00,
		min = -9999,
        max = 9999,
		step = 50)
	
	nums_method_items = (('0','Along X',''),('1','Along Y',''), ('2','Along Z',''), ('3','Simple',''), ('4','None',''))
	nums_method: EnumProperty(name="", items = nums_method_items)
	
	nums_format_items = (('0','_X, _XX, _XXX',''),('1','_0X, _XX, _XXX',''), ('2','_00X, _0XX, _XXX',''))
	nums_format: EnumProperty(name="", items = nums_format_items)
	
	axis_items = (('0','X',''),('1','Y',''), ('2','Z',''))
	axis_select: EnumProperty(name="Axis", items = axis_items)
	
	rename_menu_items = (('0','Add Pre/Postfix',''),('1','Replace',''), ('2','New name',''))
	rename_select: EnumProperty(name="", items = rename_menu_items)
	
	orientation_menu_items = (('0','GLOBAL',''),('1','LOCAL',''))
	orientation_select: EnumProperty(name="", items = orientation_menu_items)

	fbx_export_mode_menu_items = (('0','1 Obj->1 FBX',''),('1','All->One FBX',''),('2','By Parent',''),('3','By Collection',''))
	fbx_export_mode: EnumProperty(name="", items = fbx_export_mode_menu_items)
	
	uv_move_factor_items = (('1','2',''),('2','4',''), ('3','8',''), ('4','16',''), ('5','32',''))
	uv_move_factor: EnumProperty(name="", items = uv_move_factor_items, default = '3')
	
	apply_rot: BoolProperty(
		name="Apply Rotation",
		description="Apply Rotation for Exported Models",
		default = True)

	apply_rot_rotated: BoolProperty(
		name="Apply for Rotated Objects",
		description="Apply Rotation for Objects with not 0,0,0 rotation",
		default = True)
		
	apply_scale: BoolProperty(
		name="Apply Scale",
		description="Apply Scale for Exported Models",
		default = True)
		
	apply_loc: BoolProperty(
		name="Apply Location",
		description="Apply Location for Exported Models",
		default = True)
		
	set_custom_fbx_name: BoolProperty(
		name="Set Custom Name for FBX",
		description="Set Custom Name for FBX",
		default = False)
		
	custom_fbx_name: StringProperty(
		name="",
		description="Custom Name for FBX",
		default="")
	
	custom_export_path: BoolProperty(
		name="Custom Export Path",
		description="Custom Export Path",
		default = False)

	delete_mats_before_export: BoolProperty(
		name="Delete Materials",
		description="Delete Materials before Export",
		default = False)
	
	normals_inside: BoolProperty(
		name="Inside Normals",
		description="Recalculate Normals Inside",
		default = False)
	
	calc_normals_en: BoolProperty(
		name="Recalc Normals",
		description="Recalculate Normals",
		default = False)

	align_geom_to_orig: BoolProperty(
		name="Geometry To Origin",
		description="Align Geometry To Origin",
		default = False)
	
	origin_rotate_value: FloatProperty(
		name="",
		description="Angle for Origin Rotate ",
		default=5.00,
		min = -1000,
        max = 1000,
		step = 50)
	
	uv_layer_index: IntProperty(
        name = "UV Index", 
        description = "UV Index",
		default = 0,
		min = 0,
        max = 10)
	
	uv_name: StringProperty(
		name="",
		description="UV Name",
		default="")
		
	export_path: StringProperty(
      name = "",
      default = "",
      description = "Path for Export FBX",
      subtype = 'DIR_PATH'
      )

	#Custom FBX Export Opyions
	export_custom_options: BoolProperty(
		name="Custom Export Options",
		description="Custom FBX Export Options",
		default = False)

	export_apply_modifiers: BoolProperty(
		name="Apply Modifiers",
		description="Apply Modifiers",
		default = True)

	export_loose_edges: BoolProperty(
		name="Loose Edges",
		description="Loose Edges",
		default = False)

	export_tangent_space: BoolProperty(
		name="Tangent Space",
		description="Tangent Space",
		default = False)

	export_smoothing_items = (('OFF','Normals Only',''),('FACE','Face',''),('EDGE','Edge',''))
	export_smoothing: EnumProperty(name="", items = export_smoothing_items)

	#Merge Bones - Delete or Dissolve
	merge_bones_method_items = (('DELETE','Delete',''),('DISSOLVE','Dissolve',''))
	merge_bones_method: EnumProperty(name="", items = merge_bones_method_items)

	#Export FBX Target Engine
	export_target_engine_items = (('UNITY','Unity',''),('UNREAL','Unreal',''))
	export_target_engine: EnumProperty(name="", items = export_target_engine_items)


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