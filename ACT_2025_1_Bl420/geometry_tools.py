import bpy

from . import utils
from datetime import datetime

# Panels
class VIEW3D_PT_Geometry_Tools_Panel(bpy.types.Panel):
	bl_label = "Geometry Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		preferences = bpy.context.preferences.addons[__package__].preferences
		return (context.object is not None and context.mode == 'EDIT_MESH') and preferences.geometry_enable

	def draw(self, context):
		act = bpy.context.scene.act
		layout = self.layout

		if context.object is not None:
			if context.object.mode == 'OBJECT':
				row = layout.row()

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
				row.label(text=" New Panel")
				# row.operator("object.objname_to_meshname", text="Obj Name -> Data Name")


classes = (

)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)