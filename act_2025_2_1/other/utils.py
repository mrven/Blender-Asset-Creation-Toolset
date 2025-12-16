import bpy
from collections import defaultdict

# Object name to data name
def obj_name_to_data_name():
	obj_dict = defaultdict(list)

	for obj in bpy.context.selected_objects:
		if obj.type != "EMPTY":
			obj_dict[obj.data].append(obj)

	for mesh, objects in obj_dict.items():
		for enum, object_mesh in enumerate(objects):
			# Skip instances
			if enum == 0:
				object_mesh.data.name = object_mesh.name
			else:
				break

# Get children of object recursively (for < 3, 3, 0)
def get_children_recursive(obj):
	result = []

	def collect(o):
		for child in o.children:
			result.append(child)
			collect(child)

	collect(obj)
	return result