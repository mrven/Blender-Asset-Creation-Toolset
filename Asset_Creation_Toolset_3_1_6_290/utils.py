import bpy
import bmesh


#-------------------------------------------------------
#Find Min and Max Vertex Coordinates
def Find_Min_Max_Verts(obj, coord_index, min_or_max):
	bpy.ops.mesh.reveal()
	
	#get bmesh from active object
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


#-------------------------------------------------------
#Check String is a Number
def Str_Is_Int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#-------------------------------------------------------
#Get BlenderVersion
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