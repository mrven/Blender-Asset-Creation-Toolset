import bpy

# Export Model
def export_model(path, name):
	act = bpy.context.scene.act

	export_fbx_params = dict(filepath=str(path + name + '.fbx'),
	                         use_selection=True,
	                         apply_scale_options='FBX_SCALE_ALL',
	                         add_leaf_bones=False,
	                         colors_type='LINEAR',
	                         use_custom_props=True,
	                         use_mesh_modifiers = True,
	                         mesh_smooth_type='OFF',
	                         use_mesh_edges=False,
	                         use_tspace=False,
	                         use_armature_deform_only=True,
	                         global_scale=1.0,
	                         axis_forward='-Z',
	                         axis_up='Y',
	                         use_space_transform=True)

	export_obj_params = dict(filepath=str(path + name + '.obj'),
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
	                         path_mode='AUTO',
	                         forward_axis='NEGATIVE_Z',
	                         up_axis='Y')

	export_gltf_params = dict(filepath=str(path + name + '.glb'),
	                          check_existing=False,
	                          export_image_format='AUTO',
	                          export_tangents=False,
	                          export_attributes=False,
	                          use_selection=True,
	                          export_extras=True,
	                          export_def_bones=False)

	if act.export_target_engine == 'UNITY':
		export_fbx_params['apply_scale_options'] = 'FBX_SCALE_UNITS'
		export_fbx_params['axis_forward'] = '-Y'
		export_fbx_params['axis_up'] = 'Z'
		export_fbx_params['use_space_transform'] = False
	elif act.export_target_engine == 'UNREAL':
		export_fbx_params['apply_scale_options'] = 'FBX_SCALE_NONE'

	if act.export_custom_options:
		# Custom Scale Option
		if act.use_custom_export_scale:
			export_fbx_params['apply_scale_options'] = 'FBX_SCALE_CUSTOM'
			export_fbx_params['global_scale'] = act.custom_export_scale_value

			export_obj_params['global_scale'] = act.custom_export_scale_value

		# Custom Axes Option
		if act.use_custom_export_axes:
			forward_axis = act.custom_export_forward_axis
			up_axis = act.custom_export_up_axis

			export_fbx_params['axis_forward'] = forward_axis
			export_fbx_params['axis_up'] = up_axis
			export_fbx_params['use_space_transform'] = False

			export_obj_params['forward_axis'] = forward_axis.replace('-', 'NEGATIVE_')
			export_obj_params['up_axis'] = up_axis.replace('-', 'NEGATIVE_')

		# Other Custom Options
		export_fbx_params['use_mesh_edges'] = act.export_loose_edges
		export_fbx_params['use_tspace'] = act.export_tangent_space
		export_fbx_params['mesh_smooth_type'] = act.export_smoothing
		export_fbx_params['use_custom_props'] = act.export_custom_props
		export_fbx_params['add_leaf_bones'] = act.export_add_leaf_bones
		export_fbx_params['use_armature_deform_only'] = act.export_only_deform_bones
		export_fbx_params['colors_type'] = act.export_vc_color_space

		export_obj_params['export_smooth_groups'] = act.obj_export_smooth_groups
		export_obj_params['export_material_groups'] = act.obj_separate_by_materials

		export_gltf_params['export_image_format'] = act.gltf_export_image_format
		export_gltf_params['export_tangents'] = act.gltf_export_tangents
		export_gltf_params['export_attributes'] = act.gltf_export_attributes
		export_gltf_params['export_extras'] = act.gltf_export_custom_properties
		export_gltf_params['export_def_bones'] = act.gltf_export_deform_bones_only

	if act.export_format == 'FBX':
		bpy.ops.export_scene.fbx(**export_fbx_params)

	if act.export_format == 'OBJ':
		bpy.ops.wm.obj_export(**export_obj_params)

	if act.export_format == 'GLTF':
		bpy.ops.export_scene.gltf(**export_gltf_params)