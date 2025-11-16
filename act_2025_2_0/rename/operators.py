import bpy
from datetime import datetime

from ..common import utils as common_utils
from . import utils

package_name = __package__.split(".")[0]

# Numbering
class Numbering(bpy.types.Operator):
	"""Set Numbering of Objects"""
	bl_idname = "object.act_numbering"
	bl_label = "Set Numbering"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		selected_obj = context.selected_objects
		objects_list = []

		# Delete previous numbers
		if act.delete_prev_nums:
			for obj in selected_obj:
				ob_name = obj.name

				if utils.str_is_int(ob_name[-1:]):
					underscore_pos = len(ob_name) - 2
					if ob_name[underscore_pos] == "_":
						ob_name = ob_name[:-2]

				if utils.str_is_int(ob_name[-2:]):
					underscore_pos = len(ob_name) - 3
					if ob_name[underscore_pos] == "_":
						ob_name = ob_name[:-3]

				if utils.str_is_int(ob_name[-3:]):
					underscore_pos = len(ob_name) - 4
					if ob_name[underscore_pos] == "_":
						ob_name = ob_name[:-4]

				obj.name = ob_name

			selected_obj = context.selected_objects

		for x in selected_obj:
			object_class = [x, 0]

			# List of objects
			if act.nums_method == "ALONG_X" or act.nums_method == "SIMPLE" or act.nums_method == "NONE":
				object_class = [x, x.location.x]
			if act.nums_method == "ALONG_Y":
				object_class = [x, x.location.y]
			if act.nums_method == "ALONG_Z":
				object_class = [x, x.location.z]

			objects_list.append(object_class)

		# Sort list
		if act.nums_method != "SIMPLE":
			objects_list.sort(key=lambda obj_sort: obj_sort[1])

		# Preprocess delete Blender numbers and add new numbers
		for y in range(len(objects_list)):
			current_obj = objects_list[y][0]

			# Delete Blender numbers (.001, .002, etc.)
			ob_name = current_obj.name
			if utils.str_is_int(ob_name[-3:]):
				dot_pos = len(ob_name) - 4
				if ob_name[dot_pos] == ".":
					ob_name = ob_name[:-4]

			# Format for numbers
			num_str = ""

			# _X, _XX, _XXX
			if act.nums_format == "NO_ZEROS":
				num_str = str(y + 1)

			# _0X, _XX, _XXX
			if act.nums_format == "ONE_ZERO":
				if y <= 8:
					num_str = "0" + str(y + 1)
				else:
					num_str = str(y + 1)

			# _00X, _0XX, _XXX
			if act.nums_format == "TWO_ZEROS":
				if y <= 8:
					num_str = "00" + str(y + 1)
				elif (y >= 9) and (y <= 98):
					num_str = "0" + str(y + 1)
				else:
					num_str = str(y + 1)

			if act.nums_method == "NONE":
				objects_list[y][0].name = ob_name
			else:
				objects_list[y][0].name = ob_name + "_" + num_str

		common_utils.print_execution_time("Numbering", start_time)
		return {"FINISHED"}


# Added LOD Postfix
class AddLODToObjName(bpy.types.Operator):
	"""Add LOD to Obj Name"""
	bl_idname = "object.act_lod_to_objname"
	bl_label = "Add LOD to Name"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		start_time = datetime.now()
		act = context.scene.act
		selected_objects = context.selected_objects

		for obj in selected_objects:
			if obj.name[-5:][:-1] == "_LOD":
				obj.name = obj.name[:-5]
			obj.name = obj.name + "_LOD" + str(act.lod_level)

		common_utils.print_execution_time("Add LOD to Obj Name", start_time)
		return {"FINISHED"}


# Remove LOD Postfix
class RemoveLODFromObjName(bpy.types.Operator):
	"""Remove LOD from Obj Name"""
	bl_idname = "object.act_remove_lod_from_objname"
	bl_label = "Remove LOD from Name"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		start_time = datetime.now()
		selected_objects = context.selected_objects

		for obj in selected_objects:
			if obj.name[-5:][:-1] == "_LOD":
				obj.name = obj.name[:-5]

		common_utils.print_execution_time("Remove LOD from Obj Name", start_time)
		return {"FINISHED"}


# Rename bones
class RenameBones(bpy.types.Operator):
	"""Rename bones"""
	bl_idname = "object.act_rename_bones"
	bl_label = "Rename bones"
	bl_options = {"REGISTER", "UNDO"}

	Value: bpy.props.StringProperty()

	def execute(self, context):
		start_time = datetime.now()
		selected_bones = context.selected_bones

		for x in selected_bones:
			x.name = x.name + self.Value

		common_utils.print_execution_time("Rename Bones", start_time)
		return {"FINISHED"}


classes = (
	Numbering,
	RenameBones,
	AddLODToObjName,
	RemoveLODFromObjName,
)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
