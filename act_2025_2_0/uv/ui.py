import bpy

from . import operators

package_name = __package__.split('.')[0]

# UV mover UI panel
class UV_PT_uv_mover_panel(bpy.types.Panel):
	bl_label = "UV Mover"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[package_name].preferences
		return context.mode == 'EDIT_MESH' and context.area.ui_type == 'UV' and preferences.uv_uv_enable

	def draw(self, context):
		act = context.scene.act

		layout = self.layout

		row = layout.row()
		row.label(text="Set Cursor To Corner:")

		# Aligner buttons
		row = layout.row(align=True)
		row.operator(operators.UVMover.bl_idname, text="Top Left").move_command = "TL"
		row.operator(operators.UVMover.bl_idname, text="Top Right").move_command = "TR"

		row = layout.row(align=True)
		row.operator(operators.UVMover.bl_idname, text="Bottom Left").move_command = "BL"
		row.operator(operators.UVMover.bl_idname, text="Bottom Right").move_command = "BR"

		row = layout.row()
		row.label(text="Scale and Move:")

		# Aligner buttons
		row = layout.row(align=True)
		row.operator(operators.UVMover.bl_idname, text="Scale-").move_command = "MINUS"
		row.operator(operators.UVMover.bl_idname, text="UP").move_command = "UP"
		row.operator(operators.UVMover.bl_idname, text="Scale+").move_command = "PLUS"

		row = layout.row(align=True)
		row.operator(operators.UVMover.bl_idname, text="LEFT").move_command = "LEFT"
		row.operator(operators.UVMover.bl_idname, text="DOWN").move_command = "DOWN"
		row.operator(operators.UVMover.bl_idname, text="RIGHT").move_command = "RIGHT"

		row = layout.row(align=True)
		row.label(text="Move Step   1/")
		row.prop(act, 'uv_move_factor', expand=False)


# UV tools UI panels
class VIEW3D_PT_uv_tools_panel(bpy.types.Panel):
	bl_label = "UV Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		preferences = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode == 'OBJECT' and preferences.uv_view3d_enable)

	def draw(self, context):
		act = context.scene.act
		layout = self.layout

		# Rename UV
		box = layout.box()
		row = box.row(align=True)
		row.prop(act, "uv_index_rename", text="UV ID:")

		row = box.row(align=True)
		row.prop(act, "uv_name_rename")
		row.operator(operators.RenameUV.bl_idname)

		row = box.row()
		row.operator(operators.RemoveUV.bl_idname)

		row = box.row()
		row.operator(operators.SelectUV.bl_idname)

		box = layout.box()
		row = box.row(align=True)
		row.prop(act, "uv_name_add")
		row.operator(operators.AddUV.bl_idname)
		row = box.row(align=True)
		row.label(text="Packing:")
		row.prop(act, "uv_packing_mode", expand=False)
		if act.uv_packing_mode == 'SMART':
			row = box.row()
			row.prop(act, "uv_packing_smart_angle", text="Angle:")
			row = box.row()
			row.prop(act, "uv_packing_smart_margin", text="Margin:")
		if act.uv_packing_mode == 'LIGHTMAP':
			row = box.row()
			row.prop(act, "uv_packing_lightmap_quality", text="Quality:")
			row = box.row()
			row.prop(act, "uv_packing_lightmap_margin", text="Margin:")
		row = layout.row()
		row.operator(operators.ClearUV.bl_idname)
		row = layout.row()
		row.operator(operators.MarkSeamsFromUV.bl_idname)


classes = (
	UV_PT_uv_mover_panel,
	VIEW3D_PT_uv_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)