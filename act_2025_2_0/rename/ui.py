import bpy

from . import operators

package_name = __package__.split('.')[0]

class VIEW3D_PT_rename_tools_panel(bpy.types.Panel):
	bl_label = "Renaming Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.object.mode in {'OBJECT', 'EDIT_ARMATURE'} and preferences.renaming_enable)

	def draw(self, context):
		act = context.scene.act
		layout = self.layout

		if context.mode == 'OBJECT':
			box = layout.box()
			row = box.row()
			row.label(text="Numbering Objects")
			row = box.row(align=True)
			row.label(text="Method:")
			row.prop(act, 'nums_method', expand=False)
			row = box.row(align=True)
			row.label(text="Format:")
			row.prop(act, 'nums_format', expand=False)
			row = box.row()
			row.prop(act, "delete_prev_nums", text="Delete Previous Nums")
			row = box.row()
			row.operator(operators.Numbering.bl_idname)

			box = layout.box()
			row = box.row(align=True)
			row.prop(act, "lod_level", text="LOD Level:")
			row = box.row(align=True)
			row.operator(operators.AddLODToObjName.bl_idname)
			row = box.row(align=True)
			row.operator(operators.RemoveLODFromObjName.bl_idname)

		elif context.mode == 'EDIT_ARMATURE':
			row = layout.row(align=True)
			row.operator(operators.RenameBones.bl_idname, text="Add .L").Value = ".L"
			row.operator(operators.RenameBones.bl_idname, text="Add .R").Value = ".R"


classes = (
	VIEW3D_PT_rename_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)