import bpy


#-------------------------------------------------------
#Panels

class VIEW3D_PT_Rename_Tools_panel(bpy.types.Panel):
	bl_label = "Rename Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and (context.object.mode == 'OBJECT'	or context.mode == 'EDIT_ARMATURE'))

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				layout.label(text="Rename UV")
				row = layout.row()
				row.prop(act, "uv_layer_index", text="UV Index")
				
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.4, align=True)
				c = split.column()
				c.label(text="UV Name:")
				split = split.split()
				c = split.column()
				c.prop(act, "uv_name")
				#----

				row = layout.row()
				row.operator("object.uv_rename", text="Rename UV(s)")
				layout.separator()
				
				layout.separator()
				layout.label(text="Numbering Objects")
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Method:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_method', expand=False)
				#----
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.35, align=True)
				c = split.column()
				c.label(text="Format:")
				split = split.split()
				c = split.column()
				c.prop(act, 'nums_format', expand=False)
				#----
				
				row = layout.row()
				row.prop(act, "delete_prev_nums", text="Delete Previous Nums")
				row = layout.row()
				row.operator("object.numbering", text="Set Numbering")
			
			elif context.mode == 'EDIT_ARMATURE':
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				row.operator("object.rename_bones", text="Add .L").Value=".L"
				split = split.split()
				c = split.column()
				row.operator("object.rename_bones", text="Add .R").Value=".R"
				#----

			else:
				row = layout.row()
				row.label(text=" ")

		else:
			row = layout.row()
			row.label(text=" ")

class VIEW3D_PT_Other_Tools_panel(bpy.types.Panel):
	bl_label = "Other Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and (context.object.mode == 'OBJECT' or context.mode == 'EDIT_ARMATURE'))

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		row = layout.row()	

		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
		
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()	
				row.operator("object.objname_to_meshname", text="Obj Name -> Mesh Name")
				layout.separator()
				row = layout.row()
				row.operator("object.clear_normals", text="Clear Custom Normals")
				row = layout.row()
				row.operator("object.calc_normals", text="Flip/Calculate Normals")
				layout.prop(act, "calc_normals_en", text="Recalc Normals")
				if act.calc_normals_en:
					layout.prop(act, "normals_inside", text="Inside")
				layout.separator()
				row = layout.row()	
				row.operator("object.delete_unused_materials", text="Delete Unused Materials")
				layout.separator()

			if context.mode == 'EDIT_ARMATURE':
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.4, align=True)
				c = split.column()
				c.label(text="Method")
				split = split.split()
				c = split.column()
				c.prop(act, "merge_bones_method", text="", expand=False)
				#----
				row = layout.row()
				row.operator("object.merge_bones", text="Merge Bones")

class VIEW3D_PT_Uv_Mover_panel(bpy.types.Panel):
	bl_label = "UV Mover"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = "UI"
	bl_category = "ACT"

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object.mode == 'EDIT' and context.area.ui_type == 'UV':
			layout.label(text="Set Cursor To Corner:")
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Top Left").Value="TL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Top Right").Value="TR"
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Left").Value="BL"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Bottom Right").Value="BR"
			
			layout.separator()
			row = layout.row()
			
			#--Aligner Buttons----
			layout.label(text="Scale and Move:")
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.33, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="Scale-").Value="MINUS"
			split = split.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="UP").Value="UP"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="Scale+").Value="PLUS"
				
			#--Aligner Buttons----
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.33, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="LEFT").Value="LEFT"
			split = split.split(factor=0.5, align=True)
			c = split.column()
			c.operator("uv.uv_mover", text="DOWN").Value="DOWN"
			split = split.split()
			c = split.column()
			c.operator("uv.uv_mover", text="RIGHT").Value="RIGHT"
			
			layout.separator()
			
			row = layout.row()
			c = row.column()
			row = c.row()
			split = row.split(factor=0.5, align=True)
			c = split.column()
			c.label(text="Move Step   1/")
			split = split.split()
			c = split.column()
			c.prop(act, 'uv_move_factor', expand=False)

		else:
			row = layout.row()
			row.label(text=" ")
		
class Select_Texture_Menu(bpy.types.Menu):
	bl_idname = "UV_MT_select_texture"
	bl_label = "Select Texture"

	def draw(self, context):
		layout = self.layout
		if bpy.context.active_object.type == 'MESH':
			if len(bpy.context.active_object.data.materials) > 0:
				for node in bpy.context.active_object.active_material.node_tree.nodes:
					if node.type == 'TEX_IMAGE':
						texture_name = node.image.name_full
						row = layout.row()
						row.operator("uv.texture_from_material", text=texture_name).texture_name=texture_name
			else:
				row.label("Mesh has not materials")
		else:
			row.label("Object is not mesh")


classes = (
	VIEW3D_PT_Origin_Tools_panel,
	VIEW3D_PT_Rename_Tools_panel,
	VIEW3D_PT_Other_Tools_panel,
	VIEW3D_PT_Uv_Mover_panel,
	Select_Texture_Menu
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
