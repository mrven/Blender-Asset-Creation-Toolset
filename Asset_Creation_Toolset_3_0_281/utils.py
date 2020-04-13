import bpy
import bmesh


#-------------------------------------------------------
#Find Min and Max Vertex Coordinates
def FindMinMaxVerts(obj, CoordIndex, MinOrMax):
	
	bpy.ops.mesh.reveal()
	
	#get bmesh from active object
	bm = bmesh.from_edit_mesh(obj.data)
	bm.verts.ensure_lookup_table()
	
	if len(bm.verts) == 0:
		result = None
	else:
		min_co = (obj.matrix_world @ bm.verts[0].co)[CoordIndex]
		max_co = (obj.matrix_world @ bm.verts[0].co)[CoordIndex]
		
		for v in bm.verts:
			if (obj.matrix_world @ v.co)[CoordIndex] < min_co:
				min_co = (obj.matrix_world @ v.co)[CoordIndex]
			if (obj.matrix_world @ v.co)[CoordIndex] > max_co:
				max_co = (obj.matrix_world @ v.co)[CoordIndex]
		
		if MinOrMax == 0:
			result = min_co
		else:
			result = max_co
		
	return result	


#-------------------------------------------------------
#Check String is a Number
def StrIsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False