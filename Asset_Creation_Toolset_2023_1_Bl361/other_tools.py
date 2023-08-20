import bpy
import math

from bpy.props import StringProperty
from collections import defaultdict
from . import utils
from datetime import datetime

# Clear custom split normals
class Clear_Normals(bpy.types.Operator):
	"""Clear Custom Split Normals"""
	bl_idname = "object.clear_normals"
	bl_label = "Clear Custom Split Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)
			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.mesh.customdata_custom_splitnormals_clear()
				# Enable Auto Smooth with angle 180 degrees
				bpy.context.object.data.auto_smooth_angle = math.pi
				bpy.context.object.data.use_auto_smooth = True
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Clear Custom Normals", start_time)
		return {'FINISHED'}		
		

# Recalculate normals
class Calc_Normals(bpy.types.Operator):
	"""Recalculate Normals"""
	bl_idname = "object.calc_normals"
	bl_label = "Flip/Calculate Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		selected_obj = bpy.context.selected_objects
		active_obj = bpy.context.active_object
		
		for x in selected_obj:
			bpy.ops.object.select_all(action='DESELECT')
			x.select_set(True)

			if x.type == 'MESH':
				bpy.context.view_layer.objects.active = x
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.mesh.reveal()
				bpy.ops.mesh.select_all(action='SELECT')
				if not act.calc_normals_en:
					bpy.ops.mesh.flip_normals()
				else:
					bpy.ops.mesh.normals_make_consistent(inside=act.normals_inside)
				bpy.ops.mesh.select_all(action='DESELECT')
				bpy.ops.object.mode_set(mode='OBJECT')
				
		# Select again objects
		for j in selected_obj:
			j.select_set(True)
		
		bpy.context.view_layer.objects.active = active_obj

		utils.Print_Execution_Time("Calculate Normals", start_time)
		return {'FINISHED'}


# Object name to data name
def Obj_Name_To_Data_Name():
    obj_dict = defaultdict(list)

    for obj in bpy.context.selected_objects:
        if obj.type != 'EMPTY':
            obj_dict[obj.data].append(obj)

    for mesh, objects in obj_dict.items():
        for enum, object_mesh in enumerate(objects):
			# Skip instances
            if enum == 0:
                object_mesh.data.name = object_mesh.name
            else:
                break

class Obj_Name_To_Mesh_Name(bpy.types.Operator):
	"""Obj Name to Data Name"""
	bl_idname = "object.objname_to_meshname"
	bl_label = "Obj Name to Data Name"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		start_time = datetime.now()
		Obj_Name_To_Data_Name()

		utils.Print_Execution_Time("Object Name to Mesh Name", start_time)
		return {'FINISHED'}


# Collection Name to Object Name
class Col_Name_To_Obj_Name(bpy.types.Operator):
	"""Col Name to Obj Name"""
	bl_idname = "object.colname_to_objname"
	bl_label = "Col Name to Obj Name"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act
		collect_dict = defaultdict(list)

		for i in bpy.context.selected_objects:
			collect_dict[i.users_collection].append(i)

		for collect, bpy_obj in collect_dict.items():
			obj_count_len = len(str(len(collect[0].objects)))
			if obj_count_len == 1:
				obj_count_len = 2

			# Subdiv collections by object types
			obj_types = {x.type for x in bpy_obj}

			for object_type in obj_types:
				add_digit = 0
				# Get list by selected obj and obj types in current collection
				cur_collect_obj_list = [x.name for x in collect_dict[collect] if x.type == object_type and x.select_get()]

				if act.col_to_obj_name_method == 'ADD':
					col_name = collect[0].name
				else:
					if act.col_name_type_style == 'CAPITAL':
						col_name = collect[0].name + '_' + object_type
					else:
						col_name = collect[0].name + '_' + object_type.title()

				# List for skip rename and overwrite name
				all_obj_list = [i.name for i in bpy.data.objects if i.type == object_type and col_name in i.name]

				for obj in cur_collect_obj_list:
					if act.col_to_obj_name_method == 'REPLACE':
						zeros = "0" * (obj_count_len + 1 - len(str(add_digit + 1)))
						name = f'{col_name}_{zeros}{1 + add_digit}'

						while True:
							if name == obj:
								all_obj_list.append(name)
								break
							elif name in all_obj_list:
								add_digit += 1
								zeros = "0" * (obj_count_len + 1 - len(str(add_digit + 1)))
								name = f'{col_name}_{zeros}{1 + add_digit}'
							else:
								current_obj = bpy.data.objects[obj]
								current_obj.name = name
								all_obj_list.append(name)
								break
					else:
						current_obj = bpy.data.objects[obj]
						if act.col_name_position == 'START':
							current_obj.name = col_name + '_' + current_obj.name
						else:
							current_obj.name = current_obj.name + '_' + col_name

		Obj_Name_To_Data_Name()

		utils.Print_Execution_Time("Collection Name to Object Name", start_time)
		return {'FINISHED'}


# Merge bones
class Merge_Bones(bpy.types.Operator):
	"""Merge Selected Bones to Active"""
	bl_idname = "object.merge_bones"
	bl_label = "Merge Selected Bones to Active"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		start_time = datetime.now()
		act = bpy.context.scene.act

		# TODO: BUG!! Active Bone not updating if switch MODE from POSE to EDIT
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='EDIT')

		armature = bpy.context.active_object
		active_bone_name = armature.data.bones.active.name
		selected_bones_name = []
		parent_mesh = None
		meshes = []

		bpy.ops.object.mode_set(mode='OBJECT')

		# Collect selected bones, but not active
		for bone in armature.data.bones:
			if bone.select and bone.name != active_bone_name:
				selected_bones_name.append(bone.name)

		# Cancel if select only one bone
		if len(selected_bones_name) == 0:
			self.report({'INFO'}, 'Select more than one bone')
			bpy.ops.object.mode_set(mode='EDIT')
			return {'CANCELLED'}

		# Find mesh deformed with this armature
		for m in bpy.context.scene.objects:
			if m.type == 'MESH':
				if len(m.modifiers) > 0:
					for n in m.modifiers:
						if n.type == 'ARMATURE' and n.object.name_full == armature.name_full:
							meshes.append(m)

		if len(meshes) == 0:
			self.report({'INFO'}, 'Armature has no mesh')
			bpy.ops.object.mode_set(mode='EDIT')
			return {'CANCELLED'}

		for mesh in meshes:
			bpy.ops.object.select_all(action='DESELECT')
			mesh.select_set(True)
			bpy.context.view_layer.objects.active = mesh

			# Check mesh has needed vertex groups
			has_active_bone_group = False
			for group in mesh.vertex_groups:
				if group.name == active_bone_name:
					has_active_bone_group = True

			# Transfer weights from selected bones to active with modifier and clean up vertex groups
			for bone_name in selected_bones_name:
				# Check mesh has needed vertex groups
				has_dissolve_bone_group = False
				for group in mesh.vertex_groups:
					if group.name == bone_name:
						has_dissolve_bone_group = True

				if not has_dissolve_bone_group:
					continue

				# Case if mesh has group for dissolve bone, but do not have group for active
				# Add group for active bone
				if not has_active_bone_group:
					bpy.ops.object.vertex_group_add()
					mesh.vertex_groups.active.name = active_bone_name

				mesh.vertex_groups.active_index = mesh.vertex_groups[bone_name].index

				bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
				mesh.modifiers['VertexWeightMix'].vertex_group_a = active_bone_name
				mesh.modifiers['VertexWeightMix'].vertex_group_b = bone_name
				mesh.modifiers['VertexWeightMix'].mix_mode = 'ADD'
				mesh.modifiers['VertexWeightMix'].mix_set = 'ALL'
				bpy.ops.object.modifier_apply(modifier="VertexWeightMix")
				bpy.ops.object.vertex_group_remove()

		bpy.ops.object.select_all(action='DESELECT')
		armature.select_set(True)
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.armature.select_all(action='DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')

		# Delete selected bones
		for bone_name in selected_bones_name:
			try:
				armature.data.bones[bone_name].select = True
			except:
				continue

			bpy.ops.object.mode_set(mode='EDIT')

			if act.merge_bones_method == 'DELETE':
				bpy.ops.armature.delete()
			elif act.merge_bones_method == 'DISSOLVE':
				bpy.ops.armature.dissolve()

			bpy.ops.object.mode_set(mode='OBJECT')

		if act.merge_bones_method == 'DELETE':
			armature.data.bones[active_bone_name].select = True
		bpy.ops.object.mode_set(mode='EDIT')

		utils.Print_Execution_Time("Merge Bones", start_time)
		return {'FINISHED'}


# Weight paint brush mode invert
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


# Panels
class VIEW3D_PT_Other_Tools_Panel(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and (context.object.mode == 'OBJECT' or context.mode == 'EDIT_ARMATURE' or context.mode == 'PAINT_WEIGHT')) \
			and preferences.other_enable

	def draw(self, context):
		act = bpy.context.scene.act
		
		layout = self.layout	

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
		
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()	
				row.operator("object.objname_to_meshname", text="Obj Name -> Data Name")

				box = layout.box()
				row = box.row(align=True)
				row.label(text=" Method")
				row.prop(act, "col_to_obj_name_method", expand=False)
				if act.col_to_obj_name_method == 'ADD':
					row = box.row(align=True)
					row.label(text=" Place ")
					row.prop(act, "col_name_position", expand=False)
				else:
					row = box.row(align=True)
					row.label(text=" Style of Type ")
					row.prop(act, "col_name_type_style", expand=False)
				row = box.row()
				row.operator("object.colname_to_objname", text="Collection Name -> Obj Name")

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