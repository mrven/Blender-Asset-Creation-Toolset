import bpy
import math

from bpy.props import StringProperty
from collections import defaultdict


#-------------------------------------------------------
#Clear Custom Split Normals
class Clear_Normals(bpy.types.Operator):
	"""Clear Custom Split Normals"""
	bl_idname = "object.clear_normals"
	bl_label = "Clear Custom Split Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.mesh.customdata_custom_splitnormals_clear()
				bpy.context.object.data.auto_smooth_angle = math.pi
				bpy.context.object.data.use_auto_smooth = True
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj					
		return {'FINISHED'}		
		
#-------------------------------------------------------
#Recalculate Normals
class Calc_Normals(bpy.types.Operator):
	"""Recalculate Normals"""
	bl_idname = "object.calc_normals"
	bl_label = "Flip/Calculate Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = bpy.context.scene.act
		
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				if act.calc_normals_en == False:
					bpy.ops.mesh.flip_normals()
				else:
					bpy.ops.mesh.normals_make_consistent(inside=act.normals_inside)
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.ops.object.mode_set(mode='OBJECT')
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj
		return {'FINISHED'}


#-------------------------------------------------------
#Obj Name to Data Name

def objNameToDataName():

    obj_dict = defaultdict(list)

    for obj in bpy.context.selected_objects:
        if obj.type != 'EMPTY':
            obj_dict[obj.data].append(obj)

    for mesh, objects in obj_dict.items():
        for enum, object_mesh in enumerate(objects):
            if enum == 0:  # Skip instances
                object_mesh.data.name = object_mesh.name  # Rename Data
            else:
                break

class Obj_Name_To_Mesh_Name(bpy.types.Operator):
	"""Obj Name to Data Name"""
	bl_idname = "object.objname_to_meshname"
	bl_label = "Obj Name to Data Name"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		objNameToDataName()
		return {'FINISHED'}

#-------------------------------------------------------
#Col Name to Obj Name
class Col_Name_To_Obj_Name(bpy.types.Operator):
	"""Col Name to Obj Name"""
	bl_idname = "object.colname_to_objname"
	bl_label = "Col Name to Obj Name"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		def matches(li1, li2):
			matches_ = [i for i in li1 if i in li2]
			return matches_

		selected_obj = [i.name for i in bpy.context.selected_objects]
		collect_dict = defaultdict(list)

		for i in bpy.context.selected_objects:
			collect_dict[i.users_collection].append(i)

		for collect, _ in collect_dict.items():

			objCountLen = len(str(len(collect[0].objects)))
			if objCountLen == 1:
				objCountLen = 2
			addDigit = 0
			curCollectObjList = [x.name for x in collect_dict[collect]]

			intersect = matches(curCollectObjList, selected_obj)

			for obj in intersect:
				bpy_objects = bpy.data.objects[obj]
				col_name = bpy_objects.users_collection[0].name + '_' + bpy_objects.type

				zeros = "0" * (objCountLen + 1 - len(str(addDigit + 1)))
				name = f'{col_name}_{zeros}{1 + addDigit}'
				allObjList = [i.name for i in bpy.data.objects]
				while True:
					if name == obj:
						break
					elif name in allObjList:
						addDigit += 1
						zeros = "0" * (objCountLen + 1 - len(str(addDigit + 1)))
						name = f'{col_name}_{zeros}{1 + addDigit}'

						if addDigit > 5000:
							break
					else:
						__obj = bpy.data.objects[obj]
						__obj.name = name
						addDigit = 0
						break

		objNameToDataName()
		return {'FINISHED'}
#-------------------------------------------------------
#Merge Bones
class Merge_Bones(bpy.types.Operator):
	"""Merge Selected Bones to Active"""
	bl_idname = "object.merge_bones"
	bl_label = "Merge Selected Bones to Active"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = bpy.context.scene.act

		#BUG!! Active Bone not updating if switch MODE frome POSE to EDIT
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='EDIT')

		armature = bpy.context.active_object
		active_bone_name = armature.data.bones.active.name
		selected_bones_name = []
		parent_mesh = None

		bpy.ops.object.mode_set(mode='OBJECT')

		#Collect Selected Bones, but Not Active
		for bone in armature.data.bones:
			if bone.select == True:
				if bone.name != active_bone_name:
					selected_bones_name.append(bone.name)

		#Find Mesh Deformed with this Armature
		for m in bpy.context.scene.objects:
			if m.type == 'MESH':
				if (len(m.modifiers) > 0):
					for n in m.modifiers:
						if n.type == 'ARMATURE' and n.object.name_full == armature.name_full:
							parent_mesh = m

		if parent_mesh == None:
			self.report({'INFO'}, 'Armature has no mesh')
			bpy.ops.object.mode_set(mode='EDIT')
			return {'CANCELLED'}

		bpy.ops.object.select_all(action='DESELECT')
		parent_mesh.select_set(True)
		bpy.context.view_layer.objects.active = parent_mesh

		if len(selected_bones_name) > 0:
			for b_name in selected_bones_name:
				try:
					parent_mesh.vertex_groups.active_index = parent_mesh.vertex_groups[b_name].index
				except:
					continue

				bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
						
				parent_mesh.modifiers['VertexWeightMix'].vertex_group_a = active_bone_name
				parent_mesh.modifiers['VertexWeightMix'].vertex_group_b = b_name
				parent_mesh.modifiers['VertexWeightMix'].mix_mode = 'ADD'
				parent_mesh.modifiers['VertexWeightMix'].mix_set = 'ALL'
				
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="VertexWeightMix")

				bpy.ops.object.vertex_group_remove()

		bpy.ops.object.select_all(action='DESELECT')
		armature.select_set(True)
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.armature.select_all(action='DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')

		for need_delete in selected_bones_name:
			try:
				armature.data.bones[need_delete].select = True
			except:
				continue
			bpy.ops.object.mode_set(mode='EDIT')
			if act.merge_bones_method == 'DELETE':
				bpy.ops.armature.delete()
			elif act.merge_bones_method == 'DISSOLVE':
				bpy.ops.armature.dissolve()
			bpy.ops.object.mode_set(mode='OBJECT')

		armature.data.bones[active_bone_name].select = True
		bpy.ops.object.mode_set(mode='EDIT')

		return {'FINISHED'}


#-------------------------------------------------------
#Weight Paint Brush Mode Invert
class Weight_Paint_Brush_Invert(bpy.types.Operator):
	"""Weight Paint Brush Substract Mode"""
	bl_idname = "paint.weigth_paint_brush_invert"
	bl_label = "Weight Paint Brush Substract Mode"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		current_brush = bpy.context.scene.tool_settings.weight_paint.brush
		if current_brush.blend == 'ADD':
			current_brush.blend = 'SUB'
		elif current_brush.blend == 'SUB':
			current_brush.blend = 'ADD'
		else:
			weight = bpy.context.scene.tool_settings.unified_paint_settings.weight
			bpy.context.scene.tool_settings.unified_paint_settings.weight = 1 - weight
		return {'FINISHED'}


#-------------------------------------------------------
#Panels
class VIEW3D_PT_Other_Tools_Panel(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and (context.object.mode == 'OBJECT' or context.mode == 'EDIT_ARMATURE' or context.mode == 'PAINT_WEIGHT')) and preferences.other_enable

	def draw(self, context):
		act = bpy.context.scene.act
		
		layout = self.layout	

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
		
		if context.object is not None:
			if context.mode == 'OBJECT':
				
				row = layout.row()	
				row.operator("object.colname_to_objname", text="Col Name -> Obj Name")
				
				row = layout.row()	
				row.operator("object.objname_to_meshname", text="Obj Name -> Data Name")

				row = layout.row()
				row.operator("object.clear_normals", text="Clear Custom Normals")
				
				box = layout.box()
				row = box.row()
				row.operator("object.calc_normals", text="Flip/Calculate Normals")				
				row = box.row(align=True)
				if act.calc_normals_en:
					row.prop(act, "calc_normals_en", text="Recalc Normals", icon="CHECKBOX_HLT")
					if act.normals_inside:
						row.prop(act, "normals_inside", text="Inside", icon="CHECKBOX_HLT")
					else:
						row.prop(act, "normals_inside", text="Inside", icon="CHECKBOX_DEHLT")
				else:
					row.prop(act, "calc_normals_en", text="Recalc Normals", icon="CHECKBOX_DEHLT")
				

			if context.mode == 'EDIT_ARMATURE':
				row = layout.row()
				row.label(text="Merge Bones:")

				row = layout.row(align=True)
				row.label(text="Method")
				row.prop(act, "merge_bones_method", text="", expand=False)
				
				row = layout.row()
				row.operator("object.merge_bones", text="Merge Bones")

			if context.mode == 'PAINT_WEIGHT':
				box = layout.box()
				row = box.row(align = True)
				row.label(text="Current Mode:")
				row.label(text=bpy.context.scene.tool_settings.weight_paint.brush.blend)
				row = box.row()
				row.operator("paint.weigth_paint_brush_invert", text="Invert Brush")		


classes = (
	Clear_Normals,
	Calc_Normals,
	Obj_Name_To_Mesh_Name,
	Col_Name_To_Obj_Name,
	Merge_Bones,
	Weight_Paint_Brush_Invert,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
