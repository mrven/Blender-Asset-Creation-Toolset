import bpy


#-------------------------------------------------------
#Merge Bones
class MergeBones(Operator):
	"""Merge Selected Bones to Active"""
	bl_idname = "object.merge_bones"
	bl_label = "Merge Selected Bones to Active"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		act = context.scene.act

		#BUG!! Active Bone not updating if switch MODE frome POSE to EDIT
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='EDIT')

		armature = bpy.context.active_object
		active_bone_name = armature.data.bones.active.name
		selected_bones_name = []

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

		bpy.ops.object.select_all(action='DESELECT')
		parent_mesh.select_set(True)
		bpy.context.view_layer.objects.active = parent_mesh

		print(active_bone_name)
		print(parent_mesh.name)
		for b in selected_bones_name:
			print(b)

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
#Rename bones
class RenameBones(Operator):
	"""Rename bones"""
	bl_idname = "object.rename_bones"
	bl_label = "Rename bones"
	bl_options = {'REGISTER', 'UNDO'}
	
	Value: StringProperty()

	def execute(self, context):
		selected_bones = bpy.context.selected_bones	
		for x in selected_bones:
			x.name = x.name + self.Value

		return {'FINISHED'}


classes = (
	MergeBones,
	RenameBones,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)