import bpy

# Check Cycles Addon is Enabled or Not
def cycles_is_enabled():
	is_cycles_enabled = False

	for module_name in bpy.context.preferences.addons.keys():
		if module_name == "cycles":
			is_cycles_enabled = True

	return is_cycles_enabled