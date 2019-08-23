bl_info = {
    "name": "Ply Tools",
    "author": "Paweł Łyczkowski",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Edit Mode > Context Menu",
    "description": "Adds additional tools to the context menu",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


class OriginToSelection(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.origin_to_selection"
    bl_label = "Origin to Selection"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        obj_type = obj.type
        return(obj and obj_type in {'MESH'} and context.mode == 'EDIT_MESH')

    def execute(self, context):
        
        bpy.ops.object.editmode_toggle()

        selected = context.selected_objects
        obj = context.active_object
        objects = bpy.data.objects
        
        bpy.ops.object.select_all(action='DESELECT')
        context.active_object.select_set(True)
    
        storeCursorX = context.scene.cursor.location.x
        storeCursorY = context.scene.cursor.location.y
        storeCursorZ = context.scene.cursor.location.z
       
        bpy.ops.object.editmode_toggle() 
       
        bpy.ops.view3d.snap_cursor_to_selected()

        bpy.ops.object.editmode_toggle()
        
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                
        context.scene.cursor.location.x = storeCursorX
        context.scene.cursor.location.y = storeCursorY
        context.scene.cursor.location.z = storeCursorZ
        
        for obj in selected:
            obj.select_set(True)
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}
    
def ply_tools_edit_mesh(self, context):
     self.layout.operator_context = 'INVOKE_REGION_WIN'
     self.layout.separator()
     self.layout.operator("mesh.origin_to_selection")


def register():
    bpy.utils.register_class(OriginToSelection)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(ply_tools_edit_mesh)


def unregister():
    bpy.utils.unregister_class(OriginToSelection)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(ply_tools_edit_mesh)


if __name__ == "__main__":
    register()