import bpy

from . import operators

package_name = __package__.split(".")[0]


class VIEW3D_PT_other_tools_panel(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.object.mode in {"OBJECT", "EDIT_ARMATURE", "PAINT_WEIGHT"} and preferences.other_enable)

	def draw(self, context):
		act = context.scene.act

		layout = self.layout

		if context.mode == "OBJECT":
			row = layout.row()
			row.operator(operators.ObjNameToMeshName.bl_idname)

			box = layout.box()
			row = box.row(align=True)
			row.label(text=" Method")
			row.prop(act, "col_to_obj_name_method", expand=False)
			if act.col_to_obj_name_method == "ADD":
				row = box.row(align=True)
				row.label(text=" Place ")
				row.prop(act, "col_name_position", expand=False)
			else:
				row = box.row(align=True)
				row.label(text=" Style of Type ")
				row.prop(act, "col_name_type_style", expand=False)
			row = box.row()
			row.operator(operators.CollectionNameToObjName.bl_idname)

			row = layout.row()
			row.operator(operators.ClearNormals.bl_idname)

			box = layout.box()
			row = box.row()
			row.operator(operators.CalcNormals.bl_idname)
			row = box.row(align=True)
			if act.calc_normals_en:
				row.prop(act, "calc_normals_en", text="Recalc Normals", icon="CHECKBOX_HLT")
				if act.normals_inside:
					row.prop(act, "normals_inside", text="Inside", icon="CHECKBOX_HLT")
				else:
					row.prop(act, "normals_inside", text="Inside", icon="CHECKBOX_DEHLT")
			else:
				row.prop(act, "calc_normals_en", text="Recalc Normals", icon="CHECKBOX_DEHLT")

			row = layout.row()
			row.operator(operators.SelectNegativeScaledObjects.bl_idname)

			box = layout.box()
			row = box.row()
			row.operator(operators.CleanupEmpties.bl_idname)
			row = box.row()
			row.prop(act, "delete_empty_meshes", text="Also delete empty meshes")

		if context.mode == "EDIT_ARMATURE":
			row = layout.row()
			row.label(text="Merge Bones:")

			row = layout.row(align=True)
			row.label(text="Method")
			row.prop(act, "merge_bones_method", expand=False)

			row = layout.row()
			row.operator(operators.MergeBones.bl_idname)

		if context.mode == "PAINT_WEIGHT":
			box = layout.box()
			row = box.row(align=True)
			row.label(text="Current Mode:")
			row.label(text=context.scene.tool_settings.weight_paint.brush.blend)
			row = box.row()
			row.operator(operators.InvertWeightPaintBrush.bl_idname)


classes = (
	VIEW3D_PT_other_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)