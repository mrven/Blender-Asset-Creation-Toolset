import bpy
import re
from datetime import datetime

def get_package_name():
	package_parts = __package__.split(".")
	return ".".join(package_parts[:3]) if package_parts[0] == "bl_ext" else package_parts[0]


# Message Box
def show_message_box(message="", title="Message Box", icon="INFO"):
	def draw(self, _):
		self.layout.label(text=message)

	bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# Prefilter Export Name
def prefilter_export_name(name):
	result = re.sub("[#%&{}<>\\\*?/'\":`|]", "_", name)

	return result


# Execution Time
def print_execution_time(function_name, start_time):
	act = bpy.context.scene.act

	if act.debug:
		finish_time = datetime.now()
		execution_time = finish_time - start_time
		seconds = (execution_time.total_seconds())
		milliseconds = round(seconds * 1000)
		print(function_name + " finished in " + str(seconds) + "s (" + str(milliseconds) + "ms)")