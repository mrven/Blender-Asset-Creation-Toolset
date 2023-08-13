import bpy
import bmesh
from datetime import datetime
import re

# Find min and max vertex coordinates
def Find_Min_Max_Verts(obj, coord_index, min_or_max):
	bpy.ops.mesh.reveal()

	# Get bmesh from active object
	bm = bmesh.from_edit_mesh(obj.data)
	bm.verts.ensure_lookup_table()

	if len(bm.verts) == 0:
		result = None
	else:
		min_co = (obj.matrix_world @ bm.verts[0].co)[coord_index]
		max_co = (obj.matrix_world @ bm.verts[0].co)[coord_index]

		for v in bm.verts:
			if (obj.matrix_world @ v.co)[coord_index] < min_co:
				min_co = (obj.matrix_world @ v.co)[coord_index]
			if (obj.matrix_world @ v.co)[coord_index] > max_co:
				max_co = (obj.matrix_world @ v.co)[coord_index]

		if min_or_max == 0:
			result = min_co
		else:
			result = max_co

	return result


# Check string is a number
def Str_Is_Int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


# Get BlenderVersion
def Get_Version():
	result = 0
	version = bpy.app.version_string[:4]
	if version[-1:] == ".":
		version = version[:3]
	try:
		result = float(version)
	except:
		result = 2.90

	return result

# Message Box
def Show_Message_Box(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


# Prefilter Export Name
def Prefilter_Export_Name(name):
	result = re.sub("[#%&{}\<>*?/'\":`|]","_",name)

	return result


# Export Model
def Export_Model(path, name):
	act = bpy.context.scene.act
	if act.export_custom_options:
		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_ALL',
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_NONE',
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_NONE',
					use_mesh_modifiers=True, mesh_smooth_type=act.export_smoothing,
					use_mesh_edges=act.export_loose_edges, use_tspace=act.export_tangent_space,
					global_scale=0.01, colors_type='LINEAR', axis_forward='Y', axis_up='Z')

		if act.export_format == 'OBJ':
			bpy.ops.export_scene.obj(
				filepath=str(path + name + '.obj'), use_selection=True, use_mesh_modifiers=True,
				use_edges=True, use_smooth_groups=act.obj_export_smooth_groups,
				use_normals=True, use_uvs=True, use_materials=True,
				use_triangles=act.triangulate_before_export, group_by_object=True,
				group_by_material=act.obj_separate_by_materials,
				keep_vertex_order=True, global_scale=1, path_mode='AUTO',
				axis_forward='-Z', axis_up='Y')
	else:
		if act.export_format == 'FBX':
			if act.export_target_engine == 'UNITY':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_ALL')
			elif act.export_target_engine == 'UNREAL':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True,
					apply_scale_options='FBX_SCALE_NONE', mesh_smooth_type='FACE', use_tspace=True)
			elif act.export_target_engine == 'UNITY2023':
				bpy.ops.export_scene.fbx(
					filepath=str(path + name + '.fbx'), use_selection=True, apply_scale_options='FBX_SCALE_NONE',
					global_scale=0.01, colors_type='LINEAR', axis_forward='Y', axis_up='Z')
		if act.export_format == 'OBJ':
			bpy.ops.export_scene.obj(
				filepath=str(path + name + '.obj'), use_selection=True, use_mesh_modifiers=True,
				use_edges=True, use_smooth_groups=True, use_normals=True, use_uvs=True,
				use_materials=True, use_triangles=act.triangulate_before_export,
				group_by_object=True, group_by_material=True, keep_vertex_order=True,
				global_scale=1, path_mode='AUTO', axis_forward='-Z', axis_up='Y')


# Execution Time
def Print_Execution_Time(function_name, start_time):
	act = bpy.context.scene.act

	if act.debug:
		finish_time = datetime.now()
		execution_time = finish_time - start_time
		seconds = (execution_time.total_seconds())
		milliseconds = round(seconds * 1000)
		print(function_name + " finished in " + str(seconds) + "s (" + str(milliseconds) + "ms)")