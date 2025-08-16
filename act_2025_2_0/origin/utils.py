import bpy
import bmesh

# Find min and max vertex coordinates
def find_min_max_verts(obj, coord_index):
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

		result = (min_co, max_co)

	return result