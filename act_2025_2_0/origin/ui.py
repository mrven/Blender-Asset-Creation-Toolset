import bpy

from . import operators

package_name = __package__.split('.')[0]

class VIEW3D_PT_origin_tools_panel(bpy.types.Panel):
	bl_label = "Origin Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {'OBJECT', 'EDIT_MESH'} and preferences.origin_enable)

	def draw(self, context):
		act = context.scene.act

		layout = self.layout
		if context.mode == 'OBJECT':
			row = layout.row()
			row.label(text="Origin Align")

			row = layout.row()
			row.prop(act, "align_geom_to_orig", text="Geometry To Origin")

			# Aligner Labels
			row = layout.row(align=True)
			row.label(text="X")
			row.label(text="Y")
			row.label(text="Z")

			align_modes = [
				("Min", "MIN"),
				("Max", "MAX"),
				("Middle", "MID"),
				("Cursor", "CURSOR"),
				("Coordinate", "COORDINATE")
			]

			axes = ['X', 'Y', 'Z']

			for label, align_mode in align_modes:
				row = layout.row(align=True)
				for axis in axes:
					op = row.operator(operators.Align.bl_idname, text=label)
					op.axis = axis
					op.mode = align_mode

			row = layout.row()
			row.prop(act, "align_co", text="Coordinate")

		if context.object.mode == 'EDIT':
			row = layout.row()
			row.operator(operators.OriginToSelection.bl_idname)


classes = (
	VIEW3D_PT_origin_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)