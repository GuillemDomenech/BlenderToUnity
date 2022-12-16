# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any laTter version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


##########################################################################################################
##########################################################################################################

import bpy, bmesh
from bpy.props import *
from bpy.types import Operator, PropertyGroup, Mesh, Scene
from mathutils import Vector


# report
def report (self, item, error_or_info):
    self.report({error_or_info}, item)
    

class PG_GYAZ_Export_EncodeShapeKeysInUVChannel (PropertyGroup):

    def update_base_mesh (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.base_mesh
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.base_mesh = None
                
    def update_shape_mesh_1 (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.shape_key_mesh_1
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.shape_key_mesh_1 = None
                
    def update_shape_mesh_2 (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.shape_key_mesh_2
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.shape_key_mesh_2 = None
                
    def update_shape_mesh_3 (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.shape_key_mesh_3
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.shape_key_mesh_3 = None
                
    def update_shape_mesh_4 (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.shape_key_mesh_4
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.shape_key_mesh_4 = None
                
    def update_shape_mesh_5 (self, context):
        prop = bpy.context.scene.gyaz_export_shapes.shape_key_mesh_5
        if prop is not None:
            if prop.type != 'MESH':
                bpy.context.scene.gyaz_export_shapes.shape_key_mesh_5 = None
    
    show_props: BoolProperty (name='Shape Keys In UVs')
    base_mesh: PointerProperty (type = bpy.types.Object, name='Base Mesh', update=update_base_mesh)
    shape_key_mesh_1: PointerProperty (type = bpy.types.Object, name='Shape Mesh 1', update=update_shape_mesh_1)
    shape_key_mesh_2: PointerProperty (type = bpy.types.Object, name='Shape Mesh 2', update=update_shape_mesh_2)
    shape_key_mesh_3: PointerProperty (type = bpy.types.Object, name='Shape Mesh 3', update=update_shape_mesh_3)
    shape_key_mesh_4: PointerProperty (type = bpy.types.Object, name='Shape Mesh 4', update=update_shape_mesh_4)
    shape_key_mesh_5: PointerProperty (type = bpy.types.Object, name='Shape Mesh 5', update=update_shape_mesh_5)
    shape_nor_to_vert_col: EnumProperty (name='Shape Normal To Vert Color', items=(('None', 'None', ''), ('0', 'Shape 1', ''), ('1', 'Shape 2', ''), ('2', 'Shape 3', ''), ('3', 'Shape 4', ''), ('4', 'Shape 5', '')), default='None')    
    encode_normals: BoolProperty (name='Normals', description='Whether to encode normals, too for higher quality')
    
    
class Op_GYAZ_Export_EncodeShapeKeysInUVChannels (Operator):
    
    bl_idname = "object.gyaz_export_encode_shape_keys_in_uv_channels"  
    bl_label = "Encode Shape Keys In UV Channels"
    bl_description = "UV1-UV3: World Position Offset, Normal"
    bl_options = {'REGISTER', 'UNDO'}
            
    # operator function
    def execute(self, context):
        
        owner = bpy.context.scene.gyaz_export_shapes
        
        base_mesh = owner.base_mesh
        shape_1 = owner.shape_key_mesh_1
        shape_2 = owner.shape_key_mesh_2
        shape_3 = owner.shape_key_mesh_3
        shape_4 = owner.shape_key_mesh_4
        shape_5 = owner.shape_key_mesh_5
        
        if base_mesh is not None:
            base_mesh = base_mesh.data
        if shape_1 is not None:
            shape_1 = shape_1.data
        if shape_2 is not None:
            shape_2 = shape_2.data
        if shape_3 is not None:
            shape_3 = shape_3.data
        if shape_4 is not None:
            shape_4 = shape_4.data
        if shape_5 is not None:
            shape_5 = shape_5.data

        def main (uv_maps):

            def set_uvs_by_vert (vert, co, uv_layer):
                for loop in vert.link_loops:
                    loop[uv_layer].uv = co
            
            if owner.encode_normals and shape_3 == None or not owner.encode_normals and shape_5 == None:
                if len (uv_maps) == 0:
                    uv_maps.new (name='UVMap')
            
            if owner.encode_normals:
                
                uv_map_1 = uv_maps.new (name='Shape1_WPOxy')
                uv_map_2 = uv_maps.new (name='Shape1_WPOz_NORx')
                uv_map_3 = uv_maps.new (name='Shape1_NORyz')
                
                if shape_2 is not None:
                    uv_map_4 = uv_maps.new (name='Shape2_WPOxy')
                    uv_map_5 = uv_maps.new (name='Shape2_WPOz_NORx')
                    uv_map_6 = uv_maps.new (name='Shape2_NORyz')
                    
                if shape_3 is not None:
                    uv_map_7 = uv_maps.new (name='Shape3_WPOxy')
                    uv_map_8 = uv_maps.new (name='Shape3_WPOz')                    
                
                bm = bmesh.new ()
                bm.from_mesh (base_mesh)
                
                verts = bm.verts                
                        
                uv_layer_1 = bm.loops.layers.uv[uv_map_1.name]
                uv_layer_2 = bm.loops.layers.uv[uv_map_2.name]
                uv_layer_3 = bm.loops.layers.uv[uv_map_3.name]
                
                if shape_2 is not None:
                    uv_layer_4 = bm.loops.layers.uv[uv_map_4.name]
                    uv_layer_5 = bm.loops.layers.uv[uv_map_5.name]
                    uv_layer_6 = bm.loops.layers.uv[uv_map_6.name]
                    
                if shape_3 is not None:
                    uv_layer_7 = bm.loops.layers.uv[uv_map_7.name]
                    uv_layer_8 = bm.loops.layers.uv[uv_map_8.name]
                    

                def pack_data (shape_key_mesh, vert_index, vert, uv_layer_1, uv_layer_2, uv_layer_3):
                    vec = (shape_key_mesh.vertices[vert_index].co - vert.co) * 100
                    nor = ( shape_key_mesh.vertices[vert_index].normal + Vector ((1, 1, 1)) ) * 0.5
                    set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_1)
                    set_uvs_by_vert (vert, (vec[2], nor[1]), uv_layer_2)
                    set_uvs_by_vert (vert, (1-nor[0], 1-nor[2]), uv_layer_3)
                
                pack_shape_2 = True if shape_2 is not None else False
                pack_shape_3 = True if shape_3 is not None else False
                
                for vert_index, vert in enumerate (verts):
                    pack_data (shape_1, vert_index, vert, uv_layer_1, uv_layer_2, uv_layer_3)
                    if pack_shape_2:
                        pack_data (shape_2, vert_index, vert, uv_layer_4, uv_layer_5, uv_layer_6)
                    if pack_shape_3:                   
                        vec = (shape_3.vertices[vert_index].co - vert.co) * 100
                        set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_7)
                        set_uvs_by_vert (vert, (vec[2], 0), uv_layer_8)
                        
            else:
                
                uv_map_1 = uv_maps.new (name='Shape1_WPOxy')
                uv_map_2 = uv_maps.new (name='Shape1_WPOz')         
                
                if shape_2 is not None:
                    uv_map_2.name = 'Shape1_WPOz_Shape2_WPOx'
                    uv_map_3 = uv_maps.new (name='Shape2_WPOyz')
                
                    if shape_3 is not None:
                        uv_map_4 = uv_maps.new (name='Shape3_WPOxy')
                        uv_map_5 = uv_maps.new (name='Shape3_WPOz')
                        
                        if shape_4 is not None:
                            uv_map_5.name = 'Shape3_WPOz_Shape4_WPOx'
                            uv_map_6 = uv_maps.new (name='Shape4_WPOyz')
                            
                            if shape_5 is not None:
                                uv_map_7 = uv_maps.new (name='Shape5_WPOxy')   
                                uv_map_8 = uv_maps.new (name='Shape5_WPOz')                                
                            
                bm = bmesh.new ()
                bm.from_mesh (base_mesh)
                
                verts = bm.verts
                
                uv_layer_1 = bm.loops.layers.uv[uv_map_1.name]
                uv_layer_2 = bm.loops.layers.uv[uv_map_2.name]             
                
                if shape_2 is not None:
                    uv_layer_3 = bm.loops.layers.uv[uv_map_3.name]  
                
                    if shape_3 is not None:
                        uv_layer_4 = bm.loops.layers.uv[uv_map_4.name]
                        uv_layer_5 = bm.loops.layers.uv[uv_map_5.name] 
                        
                        if shape_4 is not None:
                            uv_layer_6 = bm.loops.layers.uv[uv_map_6.name]
                            
                            if shape_5 is not None:
                                uv_layer_7 = bm.loops.layers.uv[uv_map_7.name]
                                uv_layer_8 = bm.loops.layers.uv[uv_map_8.name]                                               
                
                
                if shape_2 == None:
                
                    for vert_index, vert in enumerate (verts):
                        vec = (shape_1.vertices[vert_index].co - vert.co) * 100
                        set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_1)
                        set_uvs_by_vert (vert, (vec[2], 0), uv_layer_2)
                        
                else:
                    
                    for vert_index, vert in enumerate (verts):
                        vec = (shape_1.vertices[vert_index].co - vert.co) * 100
                        vec2 = (shape_2.vertices[vert_index].co - vert.co) * 100
                        set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_1)
                        set_uvs_by_vert (vert, (vec[2], vec2[1]), uv_layer_2)                    
                        set_uvs_by_vert (vert, (-vec2[0], -vec2[2]), uv_layer_3)                    
                
                    if shape_3 and not shape_4:
                        
                        for vert_index, vert in enumerate (verts):
                            vec = (shape_3.vertices[vert_index].co - vert.co) * 100
                            set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_4)
                            set_uvs_by_vert (vert, (vec[2], 0), uv_layer_5)
                            
                    if shape_3 and shape_4:
                        
                        for vert_index, vert in enumerate (verts):
                            vec = (shape_3.vertices[vert_index].co - vert.co) * 100
                            vec2 = (shape_4.vertices[vert_index].co - vert.co) * 100
                            set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_4)
                            set_uvs_by_vert (vert, (vec[2], vec2[1]), uv_layer_5)                    
                            set_uvs_by_vert (vert, (-vec2[0], -vec2[2]), uv_layer_6)
                            
                    if shape_5:
                        
                        for vert_index, vert in enumerate (verts):
                            vec = (shape_5.vertices[vert_index].co - vert.co) * 100
                            set_uvs_by_vert (vert, (-vec[1], vec[0]), uv_layer_7)
                            set_uvs_by_vert (vert, (vec[2], 0), uv_layer_8)                        
                
             
            nor_to_vc = owner.shape_nor_to_vert_col           
            if nor_to_vc != 'None':
                
                shape_mesh = None    
                shapes = [shape_1, shape_2, shape_3, shape_4, shape_5]
                shape_mesh = shapes[int(nor_to_vc)]    
                
                if shape_mesh is not None:
                    
                    color_layer = bm.loops.layers.color.new ('Shape'+str(int(nor_to_vc)+1)+'_NOR')
                    
                    for vert_index, vert in enumerate (verts):
                        nor = ( shape_mesh.vertices[vert_index].normal + Vector ((1, 1, 1)) ) * 0.5
                        for loop in vert.link_loops:
                            loop[color_layer] = 1-nor[1], 1-nor[0], nor[2], 1.0                   
                        
                
            bm.to_mesh (base_mesh)
            bm.free ()
        
            
        def call (limit):
            if len (uv_maps) > limit:
                report (self, 'Base Mesh has more than ' +str(limit)+ ' uv maps.', 'WARNING')
            else:
                
                nor_to_vc = owner.shape_nor_to_vert_col
                if nor_to_vc != 'None':
                    if len (base_mesh.vertex_colors) >= 8:
                        report (self, 'No empty vertex color slot.', 'WARNING')
                    else:
                        main (uv_maps)
                else:
                    main (uv_maps)
        
        if base_mesh is not None and shape_1 is not None:
            
            uv_maps = base_mesh.uv_layers
        
            if owner.encode_normals:
            
                if shape_2 is not None:
                    limit = 2
                    if shape_3 is not None:
                        limit = 0        
                else:
                    limit = 5
                        
            else:
                
                limit = 6
                if shape_2 is not None:
                    limit = 5
                    if shape_3 is not None:
                        limit = 3
                        if shape_4 is not None:
                            limit = 2
                            if shape_5 is not None:
                                limit = 0
                            
            call (limit)
                
        else:
            report (self, 'Base Mesh and Shape Mesh 1 always have to be set.', 'WARNING')
                
                                                   
        return {'FINISHED'}
    
    #when the buttons should show up    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == 'OBJECT'

    
# mesh props
class PG_GYAZ_Export_MeshProps (PropertyGroup):
    uv_export: BoolVectorProperty (size=8, default=[True]*8, description='Whether the GYAZ Exporter keeps this uv map')
    vert_color_export: BoolVectorProperty (size=8, default=(True, False, False, False, False, False, False, False), description='Whether the GYAZ Exporter keeps this vertex color layer')
    merge_materials: BoolProperty (name='Merge Materials', default=False, description='Whether the GYAZ Exporter merges materials on export or keeps them as they are')
    atlas_name: StringProperty (name='Atlas', default='', description='Name of the merged material')
    

def register():
    bpy.utils.register_class (PG_GYAZ_Export_MeshProps)
    Mesh.gyaz_export = PointerProperty (type=PG_GYAZ_Export_MeshProps)
    
    bpy.utils.register_class (PG_GYAZ_Export_EncodeShapeKeysInUVChannel)
    Scene.gyaz_export_shapes = PointerProperty (type=PG_GYAZ_Export_EncodeShapeKeysInUVChannel)
    
    bpy.utils.register_class (Op_GYAZ_Export_EncodeShapeKeysInUVChannels)


def unregister():
    bpy.utils.unregister_class (PG_GYAZ_Export_MeshProps)
    del Mesh.gyaz_export
    
    bpy.utils.unregister_class (PG_GYAZ_Export_EncodeShapeKeysInUVChannel)
    del Scene.gyaz_export_shapes
    
    bpy.utils.unregister_class (Op_GYAZ_Export_EncodeShapeKeysInUVChannels)
    