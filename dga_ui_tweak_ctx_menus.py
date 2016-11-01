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
from bpy.app.translations import contexts as i18n_contexts

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


class PropertiesOutlinerToggler(bpy.types.Operator):
    """Toggling from Properties panel to Outliner panel (and vice-versa)"""
    bl_idname = "vm.properties_outliner_toggler"
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


class View3DPivotPointMenu(bpy.types.Menu):
    """Contextual menu to select the pivot point in the 3D View"""
    bl_label = "Pivot Point"
    bl_idname = "VIEW_3D_MT_pivot_point_ctx_menu"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('VIEW_3D', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        self.add_item('ACTIVE_ELEMENT', text='Active Element', icon='ROTACTIVE', text_ctxt=i18n_contexts.default)
        self.add_item('MEDIAN_POINT', text='Median Point', icon='ROTATECENTER', text_ctxt=i18n_contexts.default)
        self.add_item('INDIVIDUAL_ORIGINS', text='Individual Origins', icon='ROTATECOLLECTION', text_ctxt=i18n_contexts.default)
        self.add_item('CURSOR', text='3D Cursor', icon='CURSOR', text_ctxt=i18n_contexts.default)
        self.add_item('BOUNDING_BOX_CENTER', text='Bounding Box Center', icon='ROTATE', text_ctxt=i18n_contexts.default)

    def add_item(self, value, **kargs):
        props = self.layout.operator("wm.context_set_enum", **kargs)
        props.data_path, props.value = 'space_data.pivot_point', value


class ImageEditorPivotPointMenu(bpy.types.Menu):
    """Contextual menu to select the pivot point in the UV/Image editor"""
    bl_label = "Pivot"
    bl_idname = "IMAGE_EDITOR_MT_pivot_point_ctx_menu"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('IMAGE_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        self.add_item('INDIVIDUAL_ORIGINS', text='Individual Origins', icon='ROTATECOLLECTION', text_ctxt=i18n_contexts.default)
        self.add_item('CURSOR', text='2D Cursor', icon='CURSOR', text_ctxt=i18n_contexts.default)
        self.add_item('MEDIAN', text='Median Point', icon='ROTATECENTER', text_ctxt=i18n_contexts.default)
        self.add_item('CENTER', text='Bounding Box Center', icon='ROTATE', text_ctxt=i18n_contexts.default)

    def add_item(self, value, **kargs):
        props = self.layout.operator("wm.context_set_enum", **kargs)
        props.data_path, props.value = 'space_data.pivot_point', value


class GraphEditorPivotPointMenu(bpy.types.Menu):
    """Contextual menu to select the pivot point in the graph editor"""
    bl_label = "Pivot Point"
    bl_idname = "GRAPH_EDITOR_MT_pivot_point_ctx_menu"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('GRAPH_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname

    def draw(self, context):
        self.add_item('INDIVIDUAL_ORIGINS', text='Individual Origins', icon='ROTATECOLLECTION', text_ctxt=i18n_contexts.default)
        self.add_item('CURSOR', text='2D Cursor', icon='CURSOR', text_ctxt=i18n_contexts.default)
        self.add_item('BOUNDING_BOX_CENTER', text='Bounding Box Center', icon='ROTATE', text_ctxt=i18n_contexts.default)

    def add_item(self, value, **kargs):
        props = self.layout.operator("wm.context_set_enum", **kargs)
        props.data_path, props.value = 'space_data.pivot_point', value


class ClipEditorPivotPointMenu(bpy.types.Menu):
    """Contextual menu to select the pivot point in the movie clip editor"""
    bl_label = "Pivot Point"
    bl_idname = "CLIP_EDITOR_MT_pivot_point_ctx_menu"

    @classmethod
    def create_keymaps(cls):
        if KeymapsAddon.is_available():
            KeymapsAddon.new('CLIP_EDITOR', "wm.call_menu", 'COMMA', 'PRESS').properties.name = cls.bl_idname

    @classmethod
    def poll(cls, context):
        return context.space_data.view == 'CLIP' and context.space_data.clip is not None

    def draw(self, context):
        self.add_item('MEDIAN_POINT', text='Median Point', icon='ROTATECENTER', text_ctxt=i18n_contexts.default)
        self.add_item('INDIVIDUAL_ORIGINS', text='Individual Origins', icon='ROTATECOLLECTION', text_ctxt=i18n_contexts.default)
        self.add_item('CURSOR', text='2D Cursor', icon='CURSOR', text_ctxt=i18n_contexts.default)
        self.add_item('BOUNDING_BOX_CENTER', text='Bounding Box Center', icon='ROTATE', text_ctxt=i18n_contexts.default)

    def add_item(self, value, **kargs):
        props = self.layout.operator("wm.context_set_enum", **kargs)
        props.data_path, props.value = 'space_data.pivot_point', value


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


def register_classes(*args):
    for cls in args:
        bpy.utils.register_class(cls)
        if cls.create_keymaps:
            cls.create_keymaps()

def unregister_classes(*args):
    for cls in args:
        bpy.utils.unregister_class(cls)

def register():
    register_classes(PropertiesOutlinerToggler, View3DPivotPointMenu, ImageEditorPivotPointMenu, GraphEditorPivotPointMenu, ClipEditorPivotPointMenu)
    register_classes(ProportionalEditingMenu, ProportionalEditingFalloffMenu)

def unregister():
    unregister_classes(PropertiesOutlinerToggler, View3DPivotPointMenu, ImageEditorPivotPointMenu, GraphEditorPivotPointMenu, ClipEditorPivotPointMenu)
    unregister_classes(ProportionalEditingMenu, ProportionalEditingFalloffMenu)
    KeymapsAddon.unregister()

if __name__ == "__main__":
    register()
