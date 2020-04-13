import bpy


#-------------------------------------------------------
#Panels
class VIEW3D_PT_Origin_Tools_panel(Panel):
	bl_label = "Origin Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and (context.mode == 'OBJECT' or context.mode == 'EDIT_MESH'))

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.label(text="Origin Align")
				row = layout.row()
				row.prop(act, "align_co", text="Coordinate")
				row = layout.row()
				row.prop(act, "align_geom_to_orig", text="Geometry To Origin")
				
				#--Aligner Labels----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.label(text="X")
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.label(text="Y")
				split = split.split()
				c = split.column()
				c.label(text="Z")
				
				#--Aligner Min Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_min", text="Min").TypeAlign='Z'
				
				#--Aligner Max Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_max", text="Max").TypeAlign='Z'
				
				#--Aligner Cursor Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_cur", text="Cursor").TypeAlign='Z'
				
				#--Aligner Coordinates Buttons----
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.33, align=True)
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='X'
				split = split.split(factor=0.5, align=True)
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='Y'
				split = split.split()
				c = split.column()
				c.operator("object.align_co", text="Coordinates").TypeAlign='Z'
				
		if context.object is not None:
			if context.object.mode == 'EDIT':
				row = layout.row()
				row.operator("object.set_origin_to_select", text="Set Origin To Selected")
				layout.separator()

		else:
			row = layout.row()
			row.label(text=" ")

class VIEW3D_PT_Rename_Tools_panel(Panel):
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
				
class VIEW3D_PT_ImportExport_Tools_panel(Panel):
	bl_label = "Import/Export Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is None or (context.object is not None and context.object.mode == 'OBJECT'))

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout	
		if context.object is not None:
			if context.mode == 'OBJECT':
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.label(text="Export Mode:")
				split = split.split()
				c = split.column()
				c.prop(act, 'fbx_export_mode', expand=False)
				#----
				#Split row
				row = layout.row()
				c = row.column()
				row = c.row()
				split = row.split(factor=0.5, align=True)
				c = split.column()
				c.label(text="Target Engine:")
				split = split.split()
				c = split.column()
				c.prop(act, "export_target_engine", expand=False)
				#----

				row = layout.row()
				layout.label(text="Apply:")
				
				layout.prop(act, "apply_rot", text="Rotation")

				if act.apply_rot and act.fbx_export_mode == '2':
						#Split row
						row = layout.row()
						c = row.column()
						row = c.row()
						split = row.split(factor=0.05, align=True)
						c = split.column()
						c.label(text="")
						split = split.split()
						c = split.column()
						c.prop(act, "apply_rot_rotated")
						#----

				layout.prop(act, "apply_scale", text="Scale")
				
				if act.fbx_export_mode == '0' or act.fbx_export_mode == '2':
					layout.prop(act, "apply_loc", text="Location")
				
				row = layout.row()
				layout.prop(act, "delete_mats_before_export", text="Delete All Materials")

				row = layout.row()
				if act.fbx_export_mode == '1':
					layout.prop(act, "set_custom_fbx_name", text="Custom Name for FBX")
					if act.set_custom_fbx_name:
						#Split row
						row = layout.row()
						c = row.column()
						row = c.row()
						split = row.split(factor=0.5, align=True)
						c = split.column()
						c.label(text="FBX Name:")
						split = split.split()
						c = split.column()
						c.prop(act, "custom_fbx_name")
						#----

				row = layout.row()
				layout.prop(act, "export_custom_options", text="Custom Export Options")
				if act.export_custom_options:
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.45, align=True)
					c = split.column()
					c.label(text=" Smoothing:")
					split = split.split()
					c = split.column()
					c.prop(act, "export_smoothing", expand=False)
					#----
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.8, align=True)
					c = split.column()
					c.label(text=" Apply Modifiers")
					split = split.split()
					c = split.column()
					c.prop(act, "export_apply_modifiers", text="")
					#----
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.8, align=True)
					c = split.column()
					c.label(text=" Loose Edges")
					split = split.split()
					c = split.column()
					c.prop(act, "export_loose_edges",text="")
					#----
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.8, align=True)
					c = split.column()
					c.label(text=" Tangent Space")
					split = split.split()
					c = split.column()
					c.prop(act, "export_tangent_space", text="")
					#----

				row = layout.row()
				layout.prop(act, "custom_export_path", text="Custom Export Path")
				if act.custom_export_path:
					#Split row
					row = layout.row()
					c = row.column()
					row = c.row()
					split = row.split(factor=0.5, align=True)
					c = split.column()
					c.label(text="Export Path:")
					split = split.split()
					c = split.column()
					c.prop(act, "export_path")
					#----

				
				row = layout.row()
				if act.export_target_engine == 'UNITY':
					row.operator("object.multi_fbx_export", text="Export FBX to Unity")
				else:
					row.operator("object.multi_fbx_export", text="Export FBX to Unreal")
				row = layout.row()

				if len(act.export_dir) > 0:
					row = layout.row()
					row.operator("object.open_export_dir", text="Open Export Directory")
					row = layout.row()
		
		if context.mode == 'OBJECT':
			row = layout.row()
			row.operator("object.import_fbxobj", text="Import FBXs/OBJs")

		else:
			row = layout.row()
			row.label(text=" ")
				
class VIEW3D_PT_LowPolyArt_Tools_panel(Panel):
	bl_label = "Low Poly Art Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "ACT"

	@classmethod
	def poll(self, context):
		return (context.object is not None and context.object.mode == 'OBJECT')

	def draw(self, context):
		act = context.scene.act
		
		layout = self.layout
		if context.object is not None:
			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.palette_creator", text="Create Palette Texture")
				layout.separator()
				row = layout.row()
				row.operator("object.material_to_viewport", text="Material -> Viewport Color")
				layout.separator()

			if context.mode == 'OBJECT':
				row = layout.row()
				row.operator("object.uv_remove", text="Clear UV Maps")
				row = layout.row()
				row.operator("object.clear_vc", text="Clear Vertex Colors")
				layout.separator()

class VIEW3D_PT_Other_Tools_panel(Panel):
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

class VIEW3D_PT_Uv_Mover_panel(Panel):
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
		
def Material_Menu_Panel(self, context):
	if context.object is not None:
			if context.object.mode == 'EDIT' and len(context.selected_objects) > 1:
				layout = self.layout
				row = layout.row()		
				row.operator("object.assign_multiedit_materials", text="Active Material -> Selected")


classes = (
    VIEW3D_PT_Origin_Tools_panel,
	VIEW3D_PT_Rename_Tools_panel,
	VIEW3D_PT_ImportExport_Tools_panel,
	VIEW3D_PT_LowPolyArt_Tools_panel,
	VIEW3D_PT_Other_Tools_panel,
	VIEW3D_PT_Uv_Mover_panel,
)	


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.CYCLES_PT_context_material.prepend(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.prepend(Material_Menu_Panel)


def unregister():
	bpy.types.CYCLES_PT_context_material.remove(Material_Menu_Panel)
	bpy.types.EEVEE_MATERIAL_PT_context_material.remove(Material_Menu_Panel)
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
