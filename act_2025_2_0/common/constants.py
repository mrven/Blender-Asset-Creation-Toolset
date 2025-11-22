# URLs
TD_DOC_URL = "https://github.com/mrven/Blender-Asset-Creation-Toolset/blob/master/README.md#documentation"
TD_REPORT_URL = "https://github.com/mrven/Blender-Asset-Creation-Toolset/blob/master/docs/bug_report.md"


# Enums/Dictionaries/Lists
EXPORT_MODE_ITEMS = (("INDIVIDUAL", "One-to-One", ""),
					("ALL", "All-to-One", ""),
					("PARENT", "By Parent", ""),
					("COLLECTION", "By Collection", ""))

EXPORT_FORMAT_ITEMS = (("FBX", "FBX", ""),
						("OBJ", "OBJ", ""),
						("GLTF", "GLTF", ""))

GLTF_IMAGE_FORMAT_ITEMS = (("AUTO", "Auto", ""),
							("JPEG", "JPEG", ""),
							("WEBP", "WebP", ""),
							("NONE", "None", ""))

EXPORT_SMOOTHING_ITEMS = (("OFF", "Normals Only", ""),
							("FACE", "Face", ""),
							("EDGE", "Edge", ""))

EXPORT_TARGET_ENGINE_ITEMS = (("UNITY", "Unity", ""),
								("UNREAL", "Unreal", ""),
								("UNITY_PRE_ROTATED", "Unity (Pre-Rotated)", ""))

EXPORT_VC_COLOR_SPACE_ITEMS = (("LINEAR", "Linear", ""),
								("SRGB", "sRGB", ""))

EXPORT_AXIS_ITEMS = (("X", "X", ""),
					("Y", "Y", ""),
					("Z", "Z", ""),
					("-X", "-X", ""),
					("-Y", "-Y", ""),
					("-Z", "-Z", ""))

NUMBERING_METHOD_ITEMS = (("ALONG_X", "Along X", ""),
							("ALONG_Y", "Along Y", ""),
							("ALONG_Z", "Along Z", ""),
							("SIMPLE", "Simple", ""),
							("NONE", "None", ""))

NUMBERING_FORMAT_ITEMS = (("NO_ZEROS", "_X, _XX, _XXX", ""),
							("ONE_ZERO", "_0X, _XX, _XXX", ""),
							("TWO_ZEROS", "_00X, _0XX, _XXX", ""))

UV_MOVE_FACTOR_ITEMS = (("1", "2", ""),
						("2", "4", ""),
						("3", "8", ""),
						("4", "16", ""),
						("5", "32", ""))

UV_PACKING_ITEMS = (("NO", "Copy Active", ""),
					("SMART", "Smart", ""),
					("LIGHTMAP", "Lightmap", ""))

MERGE_BONES_METHOD_ITEMS = (("DELETE", "Delete", ""),
							("DISSOLVE", "Dissolve", ""))

COL_TO_OBJ_NAME_METHOD_ITEMS = (
		("ADD", "Add", "Add Collection name to current object name"),
		("REPLACE", "Replace", "Replace current object name to {Collection}_{Type}_{Num}"))

COL_NAME_POSITION_ITEMS = (
		("START", "To Start", "Add Collection name to beginning of object name"),
		("END", "To End", "Add Collection name to end of object name"))

COL_NAME_STYLE_ITEMS = (
		("DEFAULT", "Default", "Example: Collection_Mesh_001"),
		("CAPITAL", "CAPITAL", "Example: Collection_MESH_001"))