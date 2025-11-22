import bpy

# Export Model
def export_model(path, name):
	act = bpy.context.scene.act

	if act.export_format == "FBX":
		export_fbx(path, name)

	if act.export_format == "OBJ":
		export_obj(path, name)

	if act.export_format == "GLTF":
		export_gltf(path, name)


def export_fbx(path, name):
	act = bpy.context.scene.act

	# Defaults for UNITY_PRE_ROTATED
	export_fbx_params = dict(filepath=str(path + name + ".fbx"),
							 use_selection=True,
							 apply_scale_options="FBX_SCALE_ALL",
							 add_leaf_bones=False,
							 colors_type="LINEAR",
							 use_custom_props=True,
							 use_mesh_modifiers=True,
							 mesh_smooth_type="OFF",
							 use_mesh_edges=False,
							 use_tspace=False,
							 use_armature_deform_only=True,
							 global_scale=1.0,
							 axis_forward="-Z",
							 axis_up="Y",
							 use_space_transform=True)

	if act.export_target_engine == "UNITY":
		export_fbx_params["apply_scale_options"] = "FBX_SCALE_UNITS"
		export_fbx_params["axis_forward"] = "-Y"
		export_fbx_params["axis_up"] = "Z"
		export_fbx_params["use_space_transform"] = False
	elif act.export_target_engine == "UNREAL":
		export_fbx_params["apply_scale_options"] = "FBX_SCALE_NONE"

	if act.export_custom_options:
		# Custom Scale Option
		if act.use_custom_export_scale:
			export_fbx_params["apply_scale_options"] = "FBX_SCALE_CUSTOM"
			export_fbx_params["global_scale"] = act.custom_export_scale_value

		# Custom Axes Option
		if act.use_custom_export_axes:
			export_fbx_params["axis_forward"] = act.custom_export_forward_axis
			export_fbx_params["axis_up"] = act.custom_export_up_axis
			export_fbx_params["use_space_transform"] = False

		# Other Custom Options
		export_fbx_params["use_mesh_edges"] = act.export_loose_edges
		export_fbx_params["use_tspace"] = act.export_tangent_space
		export_fbx_params["mesh_smooth_type"] = act.export_smoothing
		export_fbx_params["use_custom_props"] = act.export_custom_props
		export_fbx_params["add_leaf_bones"] = act.export_add_leaf_bones
		export_fbx_params["use_armature_deform_only"] = act.export_only_deform_bones
		export_fbx_params["colors_type"] = act.export_vc_color_space

	allowed_args = bpy.ops.export_scene.fbx.get_rna_type().properties.keys()
	export_params = {k: v for k, v in export_fbx_params.items() if k in allowed_args}
	bpy.ops.export_scene.fbx(**export_params)


def export_obj(path, name):
	version = bpy.app.version
	act = bpy.context.scene.act

	if version >= (4, 0, 0):
		export_obj_params = dict(filepath=str(path + name + ".obj"),
								 export_selected_objects=True,
								 apply_modifiers=True,
								 export_smooth_groups=True,
								 export_normals=True,
								 export_uv=True,
								 export_materials=True,
								 export_triangulated_mesh=act.triangulate_before_export,
								 export_object_groups=True,
								 export_material_groups=True,
								 global_scale=1.0,
								 path_mode="AUTO",
								 forward_axis="NEGATIVE_Z",
								 up_axis="Y")
	else:
		export_obj_params = dict(filepath=str(path + name + ".obj"),
								use_selection=True,
								use_mesh_modifiers=True,
								use_edges=True,
								use_smooth_groups=True,
								use_normals=True,
								use_uvs=True,
								use_materials=True,
								use_triangles=act.triangulate_before_export,
								group_by_object=True,
								group_by_material=True,
								keep_vertex_order=True,
								global_scale=1,
								path_mode="AUTO",
								axis_forward="-Z",
								axis_up="Y")

	if act.export_custom_options:
		# Custom Scale Option
		if act.use_custom_export_scale:
			export_obj_params["global_scale"] = act.custom_export_scale_value

		# Custom Axes Option
		if act.use_custom_export_axes:
			forward_axis = act.custom_export_forward_axis
			up_axis = act.custom_export_up_axis

			if version >= (4, 0, 0):
				export_obj_params["forward_axis"] = forward_axis.replace("-", "NEGATIVE_")
				export_obj_params["up_axis"] = up_axis.replace("-", "NEGATIVE_")
			else:
				export_obj_params["axis_forward"] = forward_axis
				export_obj_params["axis_up"] = up_axis

		# Other Custom Options
		if version >= (4, 0, 0):
			export_obj_params["export_smooth_groups"] = act.obj_export_smooth_groups
			export_obj_params["export_material_groups"] = act.obj_separate_by_materials
		else:
			export_obj_params["use_smooth_groups"] = act.obj_export_smooth_groups
			export_obj_params["group_by_material"] = act.obj_separate_by_materials

	if version >= (4, 0, 0):
		allowed_args = bpy.ops.wm.obj_export.get_rna_type().properties.keys()
		export_params = {k: v for k, v in export_obj_params.items() if k in allowed_args}
		bpy.ops.wm.obj_export(**export_params)
	else:
		allowed_args = bpy.ops.export_scene.obj.get_rna_type().properties.keys()
		export_params = {k: v for k, v in export_obj_params.items() if k in allowed_args}
		bpy.ops.export_scene.obj(**export_params)


def export_gltf(path, name):
	act = bpy.context.scene.act

	export_gltf_params = dict(filepath=str(path + name + ".glb"),
							  check_existing=False,
							  export_image_format="AUTO",
							  export_tangents=False,
							  export_attributes=False,
							  use_selection=True,
							  export_extras=True,
							  export_def_bones=False)

	if act.export_custom_options:
		# Other Custom Options
		export_gltf_params["export_image_format"] = act.gltf_export_image_format
		export_gltf_params["export_tangents"] = act.export_tangent_space
		export_gltf_params["export_attributes"] = act.gltf_export_attributes
		export_gltf_params["export_extras"] = act.export_custom_props
		export_gltf_params["export_def_bones"] = act.export_only_deform_bones

	allowed_args = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
	export_params = {k: v for k, v in export_gltf_params.items() if k in allowed_args}
	bpy.ops.export_scene.gltf(**export_params)