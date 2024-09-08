bl_info = {
    "name": "Sandstorm Automation Tool",
    "author": "WintorOperator",
    "version": (1, 0, 0),
    "blender": (3, 6, 5),
    "location": "View3D > UI > Sandstorm",
    "description": "Automates tedious repetitive tasks relating to rigging/animation for Insurgency: Sandstorm",
    "warning": "",
    "wiki_url": "",
    "category": "Tools",
}

import bpy
from bpy.props import EnumProperty

class SANDSTORM_PT_main_panel(bpy.types.Panel):
    bl_label = "Sandstorm Automation Tool"
    bl_idname = "SANDSTORM_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Sandstorm'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "armature_1")
        layout.prop(scene, "armature_2")
        layout.operator("sandstorm.automate")

class SANDSTORM_OT_automate(bpy.types.Operator):
    bl_idname = "sandstorm.automate"
    bl_label = "Automate"
    bl_description = "Run automation tasks"

    def execute(self, context):
        scene = context.scene
        armature_1 = scene.armature_1
        armature_2 = scene.armature_2

        # Action 1: Change viewport display to stick for selected armatures
        for armature_name in [armature_1, armature_2]:
            if armature_name in bpy.data.objects:
                armature = bpy.data.objects[armature_name]
                if armature.type == 'ARMATURE':
                    armature.display_type = 'WIRE'
                    armature.show_in_front = True
                    if hasattr(armature.data, 'display_type'):
                        armature.data.display_type = 'STICK'

        self.report({'INFO'}, "Automation completed successfully")
        return {'FINISHED'}

def armature_callback(self, context):
    return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'ARMATURE']

def register():
    bpy.types.Scene.armature_1 = EnumProperty(
        name="Armature 1",
        description="Select first armature",
        items=armature_callback
    )
    bpy.types.Scene.armature_2 = EnumProperty(
        name="Armature 2",
        description="Select second armature",
        items=armature_callback
    )
    bpy.utils.register_class(SANDSTORM_PT_main_panel)
    bpy.utils.register_class(SANDSTORM_OT_automate)

def unregister():
    del bpy.types.Scene.armature_1
    del bpy.types.Scene.armature_2
    bpy.utils.unregister_class(SANDSTORM_PT_main_panel)
    bpy.utils.unregister_class(SANDSTORM_OT_automate)

if __name__ == "__main__":
    register()