import os
import json
import bpy
from bpy.utils import user_resource

from ..common import utils as common_utils

saving_enabled = False
package_name = common_utils.get_package_name()

def get_prefs_path():
    config_dir = user_resource('CONFIG', path='act', create=True)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'preferences.json')


def save_addon_prefs():
    prefs = bpy.context.preferences.addons[package_name].preferences
    data = {}
    for prop in prefs.bl_rna.properties:
        key = prop.identifier
        if key == "rna_type":
            continue
        value = getattr(prefs, key)
        data[key] = value
    with open(get_prefs_path(), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def load_or_initialize_prefs():
    prefs = bpy.context.preferences.addons[package_name].preferences
    path = get_prefs_path()

    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for k, v in data.items():
                if hasattr(prefs, k):
                    setattr(prefs, k, v)
        except Exception as e:
            print(f"[ACT Prefs] Failed to load: {e}")
    else:
        print(f"[ACT Prefs] No preferences file found at {path}")
        save_addon_prefs()


def copy_prefs_to_props(force = False):
    props = getattr(bpy.context.scene, "act", None)

    if props is None:
        return

    prefs = bpy.context.preferences.addons[package_name].preferences

    if not getattr(props, "initialized", False) or force:
        props.export_mode = prefs.export_mode

        props.initialized = True


def load_default_prefs():
    default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default_prefs.json")
    try:
        with open(default_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ACT Prefs] Failed to load default prefs: {e}")
        return {}


def apply_defaults_from_file():
    prefs = bpy.context.preferences.addons[package_name].preferences
    defaults = load_default_prefs()
    if not defaults:
        return False

    for key, value in defaults.items():
        try:
            prop_type = type(getattr(prefs, key))
            setattr(prefs, key, prop_type(value))
        except Exception as e:
            print(f"[ACT Prefs] Failed to apply {key}: {e}")
    return True