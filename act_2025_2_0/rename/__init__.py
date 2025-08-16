import importlib

modules_order = (
	"rename_tools",
)

modules = [importlib.import_module(f".{name}", __package__) for name in modules_order]

def register():
	for m in modules:
		if hasattr(m, "register"):
			m.register()


def unregister():
	for m in reversed(modules):
		if hasattr(m, "unregister"):
			m.unregister()