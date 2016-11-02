bl_info = {
    "name": "Walk/Fly mode support for azerty keyboard layout",
    "location": "shift+F and ZQSD (instead of WASD)",
    "category": "User Interface",
    "author": "David Gayerie",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "wiki_url": "https://github.com/spoonless/blender-addons",
    "tracker_url": "https://github.com/spoonless/blender-addons/issues",
}

import bpy

keymaps = []

def register():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new('View3D Fly Modal', space_type='EMPTY', region_type='WINDOW', modal=True)
        kmis = km.keymap_items

        keymaps.append((km, kmis.new_modal('FORWARD', 'Z', 'PRESS')))
        keymaps.append((km, kmis.new_modal('BACKWARD', 'S', 'PRESS')))
        keymaps.append((km, kmis.new_modal('LEFT', 'Q', 'PRESS')))
        keymaps.append((km, kmis.new_modal('RIGHT', 'D', 'PRESS')))
        keymaps.append((km, kmis.new_modal('UP', 'E', 'PRESS')))
        keymaps.append((km, kmis.new_modal('DOWN', 'A', 'PRESS')))
        keymaps.append((km, kmis.new_modal('UP', 'R', 'PRESS')))
        keymaps.append((km, kmis.new_modal('DOWN', 'F', 'PRESS')))
        keymaps.append((km, kmis.new_modal('AXIS_LOCK_X', 'X', 'PRESS')))
        keymaps.append((km, kmis.new_modal('AXIS_LOCK_Z', 'W', 'PRESS')))

        km = kc.keymaps.new('View3D Walk Modal', space_type='EMPTY', region_type='WINDOW', modal=True)
        kmis = km.keymap_items

        keymaps.append((km, kmis.new_modal('FORWARD', 'Z', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('BACKWARD', 'S', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('LEFT', 'Q', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('RIGHT', 'D', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('UP', 'E', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('DOWN', 'A', 'PRESS', any=True)))
        keymaps.append((km, kmis.new_modal('FORWARD_STOP', 'Z', 'RELEASE', any=True)))
        keymaps.append((km, kmis.new_modal('BACKWARD_STOP', 'S', 'RELEASE', any=True)))
        keymaps.append((km, kmis.new_modal('LEFT_STOP', 'Q', 'RELEASE', any=True)))
        keymaps.append((km, kmis.new_modal('RIGHT_STOP', 'D', 'RELEASE', any=True)))
        keymaps.append((km, kmis.new_modal('UP_STOP', 'E', 'RELEASE', any=True)))
        keymaps.append((km, kmis.new_modal('DOWN_STOP', 'A', 'RELEASE', any=True)))

def unregister():
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()
