import bpy


#-------------------------------------------------------
#Rename UV(s)
class RenameUV(bpy.types.Operator):
	"""Rename UV(s)"""
	bl_idname = "object.uv_rename"
	bl_label = "Rename UV(s)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects	
		uv_index = act.uv_layer_index
		uv_name = act.uv_name
		
		for x in selected_obj:
			if x.type == 'MESH':
				if len(x.data.uv_layers) > 0:
					if uv_index < len(x.data.uv_layers):
						x.data.uv_layers[uv_index].name = uv_name	
		return {'FINISHED'}


#-------------------------------------------------------		
#Numbering
class Numbering(bpy.types.Operator):
	"""Numbering of Objects"""
	bl_idname = "object.numbering"
	bl_label = "Numbering of Objects"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act
		
		selected_obj = bpy.context.selected_objects	
		objects_list = []
		
		#Delete Previous Numbers
		if act.delete_prev_nums:
			for obj in selected_obj:
				ob_name = obj.name

				if StrIsInt(ob_name[-1:]):
					unds_pos = len(ob_name) - 2
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-2]
						
				if StrIsInt(ob_name[-2:]):
					unds_pos = len(ob_name) - 3
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-3]
						
				if StrIsInt(ob_name[-3:]):
					unds_pos = len(ob_name) - 4
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-4]

				obj.name = ob_name;

			selected_obj = bpy.context.selected_objects

		for x in selected_obj:
			#List of Objects
			if act.nums_method == '0' or act.nums_method == '3' or act.nums_method == '4':
				object_class = [x.name, x.location.x]
			if act.nums_method == '1':
				object_class = [x.name, x.location.y]
			if act.nums_method == '2':
				object_class = [x.name, x.location.z]
			
			objects_list.append(object_class)
			
		#Sort List
		if act.nums_method != '3':
			objects_list.sort(key=lambda object: object[1])


		#Preprocess Delete Blender Numbers and add new numbers
		for y in range(len(objects_list)):
			current_obj = bpy.data.objects[objects_list[y][0]]
			
			#Delete Blender Numbers
			ob_name = current_obj.name
			if StrIsInt(ob_name[-3:]):
				dot_pos = len(ob_name) - 4
				if ob_name[dot_pos] == '.':
					ob_name = ob_name[:-4]
									
			#Format for Numbers
			num_str = ''
			
			#_X, _XX, _XXX
			if act.nums_format == '0': 
				num_str = str(y+1)
			
			#_0X, _XX, _XXX
			if act.nums_format == '1':
				if (y <= 8):
					num_str = '0' + str(y+1)
				else:
					num_str = str(y+1)
			
			#_00X, _0XX, _XXX
			if act.nums_format == '2':
				if (y <= 8):
					num_str = '00' + str(y+1)
				elif (y >= 9) and (y <= 98):
					num_str = '0' + str(y+1)
				else:
					num_str = str(y+1)
					
			if act.nums_method == '4':
				bpy.data.objects[objects_list[y][0]].name = ob_name;
			else:
				bpy.data.objects[objects_list[y][0]].name = ob_name + '_' + num_str;
	
		return {'FINISHED'}


classes = (
	RenameUV,
	Numbering,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)