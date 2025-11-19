import bpy

from . import operators
from ..common import utils as common_utils

package_name = common_utils.get_package_name()

# Menu for select texture In UV Editor from active material
class OBJECT_MT_select_texture_menu(bpy.types.Menu):
	bl_idname = "OBJECT_MT_select_texture_menu"
	bl_label = "Select Texture"

	def draw(self, context):
		layout = self.layout
		texture_list = []

		# If now window has Image Editor area
		has_opened_image_editor = False
		for area in context.screen.areas:
			if area.type == "IMAGE_EDITOR":
				has_opened_image_editor = True

		if has_opened_image_editor:
			# If active object is mesh and has material slots
			if context.active_object.type == "MESH":
				if len(context.active_object.data.materials) > 0:
					has_textures = False

					# Collect all textures from active material to list
					for node in context.active_object.active_material.node_tree.nodes:
						if node.type == "TEX_IMAGE":
							texture_name = node.image.name_full
							texture_in_list = False
							for texture in texture_list:
								if texture_name == texture:
									texture_in_list = True

							if not texture_in_list:
								texture_list.append(texture_name)
							has_textures = True

					if not has_textures:
						layout.label(text="Material has not textures")
				else:
					layout.label(text="Mesh has not materials")
			else:
				layout.label(text="Object is not mesh")
		else:
			layout.label(text="Opened UV Editor not found")

		for texture in texture_list:
			layout.operator(operators.TextureFromActiveMaterial.bl_idname, text=texture).texture_name = texture


# Call menu for select texture In UV Editor from active material
class CallSelectTextureMenu(bpy.types.Operator):
	"""Select Texture In UV Editor From Active Material"""
	bl_idname = "object.act_call_select_texture_menu"
	bl_label = "Open Texture in UV Editor"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, _):
		bpy.ops.wm.call_menu(name=OBJECT_MT_select_texture_menu.bl_idname)

		return {"FINISHED"}


# Material tools UI panel in 3D View
class VIEW3D_PT_material_tools_panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {"OBJECT", "EDIT_MESH"} and prefs.material_enable)

	def draw(self, context):
		act = context.scene.act
		layout = self.layout

		if context.mode == "OBJECT":
			box = layout.box()
			row = box.row()
			row.operator(operators.MaterialToViewport.bl_idname)

			row = box.row()
			row.operator(operators.RandomViewportColor.bl_idname)

			row = box.row()
			row.operator(operators.ClearViewportColor.bl_idname)

			row = layout.row()
			row.operator(operators.ClearVertexColors.bl_idname)

			row = layout.row()
			row.operator(operators.DeleteUnusedMaterials.bl_idname)

			row = layout.row()
			row.operator(operators.DeleteDuplicatedMaterials.bl_idname)

			box = layout.box()
			row = box.row()
			row.prop(act, "pbr_workflow", text="PBR Workflow")
			row = box.row()
			row.prop(act, "custom_save_path", text="Custom Save Path")
			if act.custom_save_path:
				row = box.row(align=True)
				row.label(text="Save Path:")
				row.prop(act, "save_path")
			row = box.row()
			row.operator(operators.CreatePalette.bl_idname)
			if len(act.save_dir) > 0:
				row = box.row()
				row.operator(operators.OpenSaveDir.bl_idname)

		row = layout.row()
		row.operator(CallSelectTextureMenu.bl_idname)


# Material tools UI panel in UV Editor
class UV_PT_material_uv_tools_panel(bpy.types.Panel):
	bl_label = "Material/Texture Tools"
	bl_space_type = "IMAGE_EDITOR"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(cls, context):
		prefs = context.preferences.addons[package_name].preferences
		return (context.object is not None and context.active_object is not None
		        and context.mode in {"OBJECT", "EDIT_MESH"} and prefs.uv_material_enable)

	def draw(self, _):
		layout = self.layout

		row = layout.row()
		row.operator(CallSelectTextureMenu.bl_idname)


# Material assign UI panel
def material_menu_panel(self, context):
	prefs = context.preferences.addons[package_name].preferences
	if context.object is not None and context.active_object is not None and prefs.material_properties_enable:
		if context.object.mode == "EDIT" and len(context.selected_objects) > 1:
			layout = self.layout
			row = layout.row()
			row.operator(operators.AssignMultiEditMaterials.bl_idname)


classes = (
	OBJECT_MT_select_texture_menu,
	CallSelectTextureMenu,
	VIEW3D_PT_material_tools_panel,
	UV_PT_material_uv_tools_panel,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	cycles_panel = getattr(bpy.types, "CYCLES_PT_context_material", None)
	if cycles_panel is not None:
		cycles_panel.prepend(material_menu_panel)

	eevee_panel = getattr(bpy.types, "EEVEE_MATERIAL_PT_context_material", None)
	if eevee_panel is not None:
		eevee_panel.prepend(material_menu_panel)


def unregister():
	cycles_panel = getattr(bpy.types, "CYCLES_PT_context_material", None)
	if cycles_panel is not None:
		try:
			cycles_panel.remove(material_menu_panel)
		except Exception as err:
			print("Cycles remove:", err)

	eevee_panel = getattr(bpy.types, "EEVEE_MATERIAL_PT_context_material", None)
	if eevee_panel is not None:
		try:
			eevee_panel.remove(material_menu_panel)
		except Exception as err:
			print("Eevee remove:", err)

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)