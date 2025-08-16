import bpy

# Export Model
def export_model(path, name):
	act = bpy.context.scene.act

	if act.export_custom_options:
		# Scale Defaults
		apply_scale_options_value = 'FBX_SCALE_NONE'
		global_scale_value = 1.0
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY':
			apply_scale_options_value = 'FBX_SCALE_ALL'
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY2023':
			global_scale_value = 0.01

		# Custom Scale Option
		if act.use_custom_export_scale:
			apply_scale_options_value = 'FBX_SCALE_CUSTOM'
			global_scale_value = act.custom_export_scale_value

		# Axes Defaults
		forward_axis = '-Z'
		up_axis = 'Y'
		use_transform = True
		if act.export_format == 'FBX' and act.export_target_engine == 'UNITY2023':
			forward_axis = '-Y'
			up_axis = 'Z'
			use_transform = False
		if act.export_format == 'OBJ':
			forward_axis = 'NEGATIVE_Z'

		# Custom Axes Option
		if act.use_custom_export_axes:
			forward_axis = act.custom_export_forward_axis
			up_axis = act.custom_export_up_axis
			use_transform = False
			if act.export_format == 'OBJ':
				forward_axis = forward_axis.replace('-', 'NEGATIVE_')
				up_axis = up_axis.replace('-', 'NEGATIVE_')

		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					use_space_transform=use_transform)
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					use_space_transform=use_transform)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options=apply_scale_options_value,
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					global_scale=global_scale_value, axis_forward=forward_axis, axis_up=up_axis,
					add_leaf_bones=act.export_add_leaf_bones,
					use_armature_deform_only=act.export_only_deform_bones,
					colors_type=act.export_vc_color_space, use_custom_props=act.export_custom_props,
					use_space_transform=use_transform)

		if act.export_format == 'OBJ':
			bpy.ops.wm.obj_export(
				filepath=str(path + name + '.obj'), export_selected_objects=True, apply_modifiers=True,
				export_smooth_groups=act.obj_export_smooth_groups, export_normals=True, export_uv=True,
				export_materials=True, export_triangulated_mesh=act.triangulate_before_export,
				export_object_groups=True, export_material_groups=act.obj_separate_by_materials,
				global_scale=global_scale_value, path_mode='AUTO', forward_axis=forward_axis, up_axis=up_axis)

		if act.export_format == 'GLTF':
			bpy.ops.export_scene.gltf(
				filepath=str(path + name + '.glb'), check_existing=False,
				export_image_format=act.gltf_export_image_format,
				export_tangents=act.gltf_export_tangents, export_attributes=act.gltf_export_attributes,
				use_selection=True, export_extras=act.gltf_export_custom_properties,
				export_def_bones=act.gltf_export_deform_bones_only)
	else:
		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_ALL', add_leaf_bones=False, colors_type='LINEAR',
					use_custom_props=True)
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True,
					add_leaf_bones=False, colors_type='LINEAR', use_custom_props=True)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options='FBX_SCALE_NONE',
					global_scale=0.01, colors_type='LINEAR', axis_forward='-Y', axis_up='Z',
					add_leaf_bones=False,
					use_custom_props=True, use_space_transform=False)

		if act.export_format == 'OBJ':
			bpy.ops.wm.obj_export(
				filepath=str(path + name + '.obj'), export_selected_objects=True, apply_modifiers=True,
				export_smooth_groups=True, export_normals=True, export_uv=True,
				export_materials=True, export_triangulated_mesh=act.triangulate_before_export,
				export_object_groups=True, export_material_groups=True,
				global_scale=1, path_mode='AUTO', forward_axis='NEGATIVE_Z', up_axis='Y')

		if act.export_format == 'GLTF':
			bpy.ops.export_scene.gltf(
				filepath=str(path + name + '.glb'), check_existing=False, export_image_format='AUTO',
				export_tangents=False, export_attributes=False,
				use_selection=True, export_extras=True, export_def_bones=False)