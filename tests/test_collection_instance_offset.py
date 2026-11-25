"""Run: blender -b --factory-startup --python-exit-code 1 --python tests/test_collection_instance_offset.py

Tests the offset helper with real Blender objects and an intercepted exporter.
Full ACT operator / FBX round-trip testing is separate.
"""
import importlib.util
from pathlib import Path
import bpy
from mathutils import Vector

path = Path(__file__).resolve().parents[1] / "act_2025_2_1/import_export/utils.py"
spec = importlib.util.spec_from_file_location("act_export_utils", path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
collection = bpy.data.collections.new("Offset Test")
scene.collection.children.link(collection)

def make(name, loc, parent=None):
    obj = bpy.data.objects.new(name, None)
    collection.objects.link(obj)
    obj.parent = parent
    obj.location = loc
    return obj

root = make("Root", (10, -8, 4))
root.rotation_euler.z = 0.4
root.scale = (2, 3, 1)
middle = make("Intermediate", (2, 0, 0), root)
child = make("Child", (1, 2, 0), middle)
outside = make("Outside", (5, 6, 7))
outside.rotation_euler.z = 0.7
outside.scale = (2, 3, 4)
external_child = make("External child", (3, 2, 1), outside)
for obj in (root, child, external_child):
    obj.select_set(True)
bpy.context.view_layer.update()
selected = list(bpy.context.selected_objects)
original = {obj: obj.matrix_world.copy() for obj in collection.objects}

def assert_matrix(a, b):
    assert all(abs(a[i][j] - b[i][j]) < 1e-4 for i in range(4) for j in range(4)), (a, b)

for offset in (Vector((10, -8, 4)), Vector((-5, 2, -1)), Vector((0, 0, 0))):
    collection.instance_offset = offset
    calls = []
    def fake_export(path, name):
        calls.append(name)
        for obj in selected:
            expected = original[obj].copy()
            expected.translation -= offset
            assert_matrix(obj.matrix_world, expected)
        assert_matrix(outside.matrix_world, original[outside])
    utils.export_model = fake_export
    utils.export_model_with_offset(bpy.context, "", "Test", offset)
    assert calls == ["Test"]
    for obj, matrix in original.items():
        assert_matrix(obj.matrix_world, matrix)

def failing_export(*args):
    raise RuntimeError("test export failure")
utils.export_model = failing_export
try:
    utils.export_model_with_offset(bpy.context, "", "Test", Vector((2, 3, 4)))
except RuntimeError as exc:
    assert str(exc) == "test export failure"
else:
    raise AssertionError("Expected export error")
for obj, matrix in original.items():
    assert_matrix(obj.matrix_world, matrix)

print("Collection Instance Offset tests passed")
