import bpy


from . import utils


#------------------Align Origin To Min-------------------------------
class AlignMin(bpy.types.Operator):
	"""Origin To Min """
	bl_idname = "object.align_min"
	bl_label = "Origin To Min"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: bpy.props.StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			bpy.context.view_layer.objects.active = x
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy() 
			if x.type == 'MESH':
				bpy.ops.object.mode_set(mode = 'EDIT')
				
				if self.TypeAlign == 'X':
					MinCo = FindMinMaxVerts(x, 0, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[0]
				if self.TypeAlign == 'Y':
					MinCo = FindMinMaxVerts(x, 1, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[1]
				if self.TypeAlign == 'Z':
					MinCo = FindMinMaxVerts(x, 2, 0)
					if MinCo == None:
						MinCo = saved_origin_loc[2]
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor.location = [MinCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], MinCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], MinCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor.location = saved_cursor_loc
				
				if act.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MinCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MinCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MinCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
			
		bpy.context.view_layer.objects.active = current_active_obj

		return {'FINISHED'}
	

#------------------Align Origin To Max-------------------------------
class AlignMax(bpy.types.Operator):
	"""Origin To Max """
	bl_idname = "object.align_max"
	bl_label = "Origin To Max"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: bpy.props.StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			bpy.context.view_layer.objects.active = x
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy() 
			if x.type == 'MESH':
				bpy.ops.object.mode_set(mode = 'EDIT')
				
				if self.TypeAlign == 'X':
					MaxCo = FindMinMaxVerts(x, 0, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[0]
				if self.TypeAlign == 'Y':
					MaxCo = FindMinMaxVerts(x, 1, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[1]
				if self.TypeAlign == 'Z':
					MaxCo = FindMinMaxVerts(x, 2, 1)
					if MaxCo == None:
						MaxCo = saved_origin_loc[2]
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.mode_set(mode = 'OBJECT')
					if self.TypeAlign == 'X':
						bpy.context.scene.cursor.location = [MaxCo, saved_origin_loc[1], saved_origin_loc[2]] 
					if self.TypeAlign == 'Y':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], MaxCo, saved_origin_loc[2]] 
					if self.TypeAlign == 'Z':
						bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], MaxCo]
						
					# Apply origin to Cursor position
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
					# Reset 3D Cursor position  
					bpy.context.scene.cursor.location = saved_cursor_loc
				
				if act.align_geom_to_orig == True:
					if self.TypeAlign == 'X':
						Difference = saved_origin_loc[0] - MaxCo
					if self.TypeAlign == 'Y':
						Difference = saved_origin_loc[1] - MaxCo
					if self.TypeAlign == 'Z':
						Difference = saved_origin_loc[2] - MaxCo
					
					bpy.ops.mesh.reveal()
					bpy.ops.mesh.select_all(action='SELECT')
					if self.TypeAlign == 'X':
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
						
					bpy.ops.object.mode_set(mode = 'OBJECT')

		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
			
		bpy.context.view_layer.objects.active = current_active_obj

		return {'FINISHED'}

	
#------------------Align Cursor------------------
class AlignCur(bpy.types.Operator):
	"""Origin Align To Cursor"""
	bl_idname = "object.align_cur"
	bl_label = "Origin To Cursor"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: bpy.props.StringProperty()
	
	def execute(self, context):
		act = context.scene.act

		# Save selected objects and current position of 3D Cursor
		current_selected_obj = bpy.context.selected_objects
		current_active_obj = bpy.context.active_object
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Change individual origin point
		for x in current_selected_obj:
			# Select only current object (for setting origin)
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True);
			# Save current origin and relocate 3D Cursor
			saved_origin_loc = x.location.copy()
			#Align to 3D Cursor
			if self.TypeAlign == 'X':
				bpy.context.scene.cursor.location = [saved_cursor_loc[0], saved_origin_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Y':
				bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_cursor_loc[1], saved_origin_loc[2]] 
			if self.TypeAlign == 'Z':
				bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], saved_cursor_loc[2]] 
			# Apply origin to Cursor position
			if act.align_geom_to_orig == False:
				bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
			else:
				if self.TypeAlign == 'X':
					Difference = saved_cursor_loc[0] - saved_origin_loc[0]
					bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Y':
					Difference = saved_cursor_loc[1] - saved_origin_loc[1]
					bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				if self.TypeAlign == 'Z':
					Difference = saved_cursor_loc[2] - saved_origin_loc[2]
					bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			# Reset 3D Cursor position  
			bpy.context.scene.cursor.location = saved_cursor_loc
		
		# Select again objects
		for j in current_selected_obj:
			j.select_set(True);
		
		return {'FINISHED'}


#------------------Align Coordinate------------------ 
class AlignCo(bpy.types.Operator):
	"""Origin Align To Spec Coordinate"""
	bl_idname = "object.align_co"
	bl_label = "Origin Align To Spec Coordinate"
	bl_options = {'REGISTER', 'UNDO'}
	TypeAlign: bpy.props.StringProperty()

	def execute(self, context):
		act = context.scene.act

		wrong_align_co = False
		#Check coordinate if check tgis option
		try:
			align_coordinate = float(act.align_co)
		except:
			self.report({'INFO'}, 'Coordinate is wrong')
			wrong_align_co = True   
		
		if wrong_align_co == False:
			# Save selected objects and current position of 3D Cursor
			current_selected_obj = bpy.context.selected_objects
			saved_cursor_loc = bpy.context.scene.cursor.location.copy()
			bpy.ops.object.mode_set(mode = 'OBJECT')
			# Change individual origin point
			for x in current_selected_obj:
				# Select only current object (for setting origin)
				bpy.ops.object.select_all(action='DESELECT')
				x.select_set(True);
				# Save current origin and relocate 3D Cursor
				saved_origin_loc = x.location.copy()
				
				#Align to Coordinate
				if self.TypeAlign == 'X':
					bpy.context.scene.cursor.location = [align_coordinate, saved_origin_loc[1], saved_origin_loc[2]] 
				if self.TypeAlign == 'Y':
					bpy.context.scene.cursor.location = [saved_origin_loc[0], align_coordinate, saved_origin_loc[2]] 
				if self.TypeAlign == 'Z':
					bpy.context.scene.cursor.location = [saved_origin_loc[0], saved_origin_loc[1], align_coordinate] 
				
				if act.align_geom_to_orig == False:
					bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
				else:
					if self.TypeAlign == 'X':
						Difference = align_coordinate - saved_origin_loc[0]
						bpy.ops.transform.translate(value=(Difference, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Y':
						Difference = align_coordinate - saved_origin_loc[1]
						bpy.ops.transform.translate(value=(0, Difference, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
					if self.TypeAlign == 'Z':
						Difference = align_coordinate - saved_origin_loc[2]
						bpy.ops.transform.translate(value=(0, 0, Difference), constraint_axis=(False, False, True), orient_type='GLOBAL', orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
				# Reset 3D Cursor position  
				bpy.context.scene.cursor.location = saved_cursor_loc
			
			# Select again objects
			for j in current_selected_obj:
				j.select_set(True);
			
		return {'FINISHED'}


#-------------------------------------------------------
#Set Origin To Selection
class SetOriginToSelect(bpy.types.Operator):
	"""Set Origin To Selection"""
	bl_idname = "object.set_origin_to_select"
	bl_label = "Set Origin To Selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		saved_cursor_loc = bpy.context.scene.cursor.location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.mode_set(mode = 'OBJECT')
		# Apply origin to Cursor position
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		# Reset 3D Cursor position  
		bpy.context.scene.cursor.location = saved_cursor_loc
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		return {'FINISHED'} 	


classes = (
	AlignMin,
	AlignMax,
	AlignCur,
	AlignCo,
	SetOriginToSelect,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)