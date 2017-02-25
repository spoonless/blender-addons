bl_info = {
    "name": "UI tweaks on context menus",
    "description": "Miscellaneous UI tweaks : contextual menus for pivot point, proportional editing and proportional editing falloff. Toggling between Outline and Property Editor.",
    "location": "COMMA, O, SHIFT+O, TAB on Property Editor or Outliner",
    "category": "User Interface",
    "author": "David Gayerie",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "wiki_url": "https://github.com/spoonless/blender-addons",
    "tracker_url": "https://github.com/spoonless/blender-addons/issues",
}

import bpy

class KeymapsAddon():
    """Utility class to manage keymaps bindings"""

    created_keymaps = []
    keyconfig = bpy.context.window_manager.keyconfigs.addon

    keymaps_name = {
        'PROPERTIES': ('Property Editor', 'PROPERTIES'),
        'OUTLINER': ('Outliner', 'OUTLINER'),
        'VIEW_3D': ('3D View', 'VIEW_3D'),
        'IMAGE_EDITOR': ('Image', 'IMAGE_EDITOR'),
        'GRAPH_EDITOR': ('Graph Editor', 'GRAPH_EDITOR'),
        'CLIP_EDITOR': ('Clip Editor', 'CLIP_EDITOR'),
        'MESH': ('Mesh', 'EMPTY'),
        'GREASE_PENCIL_STROKE_EDIT_MODE': ('Grease Pencil Stroke Edit Mode', 'EMPTY'),
        'METABALL': ('Metaball', 'EMPTY'),
        'LATTICE': ('Lattice', 'EMPTY'),
        'PARTICLE': ('Particle', 'EMPTY'),
        'UV_EDITOR': ('UV Editor', 'EMPTY'),
        'OBJECT_MODE': ('Object Mode', 'EMPTY'),
        'MASK_EDITING': ('Mask Editing', 'EMPTY'),
        'SCULPT': ('Sculpt', 'EMPTY'),
    }

    @classmethod
    def is_available(cls):
        return cls.keyconfig != None

    @classmethod
    def new(cls, keymap_name, *args, **kargs):
        keymap = cls.keymaps_name[keymap_name]
        if cls.is_available():
            km = cls.keyconfig.keymaps.find(name=keymap[0], space_type=keymap[1])
            if not km:
                km = cls.keyconfig.keymaps.new(name=keymap[0], space_type=keymap[1])
            kmi = km.keymap_items.new(*args, **kargs)
            cls.created_keymaps.append((km, kmi))
            return kmi

    @classmethod
    def unregister(cls):
        for km, kmi in cls.created_keymaps:
            km.keymap_items.remove(kmi)
        cls.created_keymaps.clear()


class PropertiesOutlinerTogglerOperator(bpy.types.Operator):
    """Toggling from Properties panel to Outliner panel (and vice-versa)"""
    bl_idname = "outliner.toggle_properties"
    bl_label = "Toggle Properties/Outliner views"
    bl_options = {'REGISTER'}

    @classmethod
    def create_keymaps(cls):
        KeymapsAddon.new('PROPERTIES', cls.bl_idname, 'TAB', 'PRESS')
        KeymapsAddon.new('OUTLINER', cls.bl_idname, 'TAB', 'PRESS')

    def execute(self, context):
        if context.area.type == 'OUTLINER':
            context.area.type = 'PROPERTIES'
        elif context.area.type == 'PROPERTIES':
            context.area.type = 'OUTLINER'
        return {'FINISHED'}


class ArmaturePositionTogglerOperator(bpy.types.Operator):
    """Toggle Pose/Rest position for parent armature"""
    bl_idname = "armature.toggle_position"
    bl_label = "[DGA] Toggle Pose/Rest position for parent armature"
    bl_options = {'REGISTER'}

    @classmethod
    def create_keymaps(cls):
        pass

    def execute(self, context):
        armatures = []
        for obj in bpy.context.selected_objects:
            while obj is not None and obj.type != 'ARMATURE':
                obj = obj.parent
            if obj is not None and obj not in armatures:
                obj.data.pose_position = 'POSE' if obj.data.pose_position == 'REST' else 'REST'
                armatures.append(obj)
        return {'FINISHED'}


class SimplifySceneTogglerOperator(bpy.types.Operator):
    """Toggle simplify scene"""
    bl_idname = "scene.toggle_simplify"
    bl_label = "[DGA] Toggle simplify scene"
    bl_options = {'REGISTER'}

    @classmethod
    def create_keymaps(cls):
        pass

    def execute(self, context):
        bpy.context.scene.render.use_simplify = not bpy.context.scene.render.use_simplify
        return {'FINISHED'}


class CtxPivotPointMenu(bpy.types.Menu):
    """Contextual menu to select the pivot point"""
    bl_label = "Pivot Point"
    bl_idname = "ANY_MT_pivot_point_ctx_menu"

    @classmethod
    def poll(cls, context):
        return context.space_data.type != 'CLIP_EDITOR' or context.space_data.clip != None

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('VIEW_3D', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('IMAGE_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('GRAPH_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('CLIP_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        self.layout.prop(context.space_data, "pivot_point", expand=True)


class ProportionalEditingMenu(bpy.types.Menu):
    """Contextual menu to select the proportional editing"""
    bl_label = "Proportional Editing"
    bl_idname = "ANY_MT_proportional_editing_ctx_menu"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('MESH', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('GREASE_PENCIL_STROKE_EDIT_MODE', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('METABALL', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('LATTICE', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('PARTICLE', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname
            KeymapsAddon.new('UV_EDITOR', "wm.call_menu", 'O', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        self.layout.prop(context.tool_settings, "proportional_edit", expand=True)


class ProportionalEditingFalloffMenu(bpy.types.Menu):
    """Contextual menu to select the proportional editing falloff"""
    bl_label = "Proportional Editing Falloff"
    bl_idname = "CTXMENU_MT_proportional_editing_falloff_ctx_menu"

    @classmethod
    def poll(cls, context):
        if context.space_data.type == 'CLIP_EDITOR':
            return context.space_data.mode == 'MASK' and context.tool_settings.use_proportional_edit_mask
        elif context.mode == 'OBJECT':
            return context.tool_settings.use_proportional_edit_objects
        else:
            return context.tool_settings.proportional_edit != 'DISABLED'

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('OBJECT_MODE', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('MESH', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('GREASE_PENCIL_STROKE_EDIT_MODE', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('METABALL', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('LATTICE', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('PARTICLE', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('UV_EDITOR', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname
            KeymapsAddon.new('MASK_EDITING', "wm.call_menu", 'O', 'PRESS', shift=True).properties.name = cls.bl_idname

    def draw(self, context):
        self.layout.prop(context.tool_settings, "proportional_edit_falloff", expand=True)


class SculptBrushMenu(bpy.types.Menu):
    bl_idname = "CTXMENU_MT_sculpt_brush_ctx_menu"
    bl_label = "Sculpt Brushes"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('SCULPT', "wm.call_menu", 'W', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        sculpt_bruhes = [b for b in bpy.data.brushes if b.use_paint_sculpt]
        nb_columns, remainder = divmod(len(sculpt_bruhes), 8)
        if remainder > 0:
            nb_columns += 1

        layout = self.layout.column_flow(columns=nb_columns)
        for i, b in enumerate(sculpt_bruhes):
            op = layout.operator("brush.active_index_set", text=b.name, icon_value=layout.icon(b))
            op.index = i
            op.mode = "sculpt"


CLASSES=[
    PropertiesOutlinerTogglerOperator,
    ArmaturePositionTogglerOperator,
    SimplifySceneTogglerOperator,
    CtxPivotPointMenu,
    ProportionalEditingMenu,
    ProportionalEditingFalloffMenu,
    SculptBrushMenu
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
        if cls.create_keymaps:
            cls.create_keymaps()


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)
    KeymapsAddon.unregister()


if __name__ == "__main__":
    register()
