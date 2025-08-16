import bpy
import collections

# Exclude unnecessary objects
def selected_obj_with_unique_data(obj_type='MESH'):
	objs_with_instances = collections.defaultdict(list)

	for obj in bpy.context.selected_objects:
		if obj.type == obj_type:
			objs_with_instances[obj.data].append(obj)
	return [objs[0] for objs in objs_with_instances.values()]


# Get Mesh Selection
def get_mesh_selection(obj):
	selection = []
	start_object_mode = bpy.context.object.mode
	bpy.ops.object.mode_set(mode='OBJECT')
	if bpy.context.scene.tool_settings.mesh_select_mode[2]:
		selection_source = obj.data.polygons
	elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
		selection_source = obj.data.edges
	else:
		selection_source = obj.data.vertices

	for i in range(len(selection_source)):
		if selection_source[i].select:
			selection.append(i)
	bpy.ops.object.mode_set(mode=start_object_mode)

	return selection


# Set Mesh Selection
def set_mesh_selection(obj, selection):
	start_object_mode = bpy.context.object.mode
	bpy.ops.object.mode_set(mode='OBJECT')
	if bpy.context.scene.tool_settings.mesh_select_mode[2]:
		for item in selection:
			obj.data.polygons[item].select = True
	elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
		for item in selection:
			obj.data.edges[item].select = True
	else:
		for item in selection:
			obj.data.vertices[item].select = True
	bpy.ops.object.mode_set(mode=start_object_mode)