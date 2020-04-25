import bpy

from . import utils


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

				if utils.Str_Is_Int(ob_name[-1:]):
					unds_pos = len(ob_name) - 2
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-2]
						
				if utils.Str_Is_Int(ob_name[-2:]):
					unds_pos = len(ob_name) - 3
					if ob_name[unds_pos] == '_':
						ob_name = ob_name[:-3]
						
				if utils.Str_Is_Int(ob_name[-3:]):
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
			if utils.Str_Is_Int(ob_name[-3:]):
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


#-------------------------------------------------------
#Rename bones
class Rename_Bones(bpy.types.Operator):
	"""Rename bones"""
	bl_idname = "object.rename_bones"
	bl_label = "Rename bones"
	bl_options = {'REGISTER', 'UNDO'}
	
	Value: bpy.props.StringProperty()

	def execute(self, context):
		selected_bones = bpy.context.selected_bones	
		for x in selected_bones:
			x.name = x.name + self.Value

		return {'FINISHED'}


#-------------------------------------------------------
#Rename Tools UI Panel
class VIEW3D_Rename_Tools_Panel(bpy.types.Panel):
	bl_label = "Rename Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and (context.object.mode == 'OBJECT'	or context.mode == 'EDIT_ARMATURE'))

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				layout.separator()
				layout.label(text="Numbering Objects")
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Method:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_method', expand=False)
				#----
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Format:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_format', expand=False)
				#----
				
				row = layout.row()
				row.prop(act, "delete_prev_nums", text="Delete Previous Nums")
				row = layout.row()
				row.operator("object.numbering", text="Set Numbering")
			
			elif context.mode == 'EDIT_ARMATURE':
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				row.operator("object.rename_bones", text="Add .L").Value=".L"
				split = split.split()
				c = split.column()
				row.operator("object.rename_bones", text="Add .R").Value=".R"
				#----

			else:
				row = layout.row()
				row.label(text=" ")

		else:
			row = layout.row()
			row.label(text=" ")


classes = (
	Numbering,
	Rename_Bones,
	VIEW3D_Rename_Tools_Panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)