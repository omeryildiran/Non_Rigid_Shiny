import bpy

def clear_assets():
    for texture in list(bpy.data.textures):
        bpy.data.textures.remove(texture,do_unlink=True) # delete material
    for meshes in list(bpy.data.meshes):
        bpy.data.meshes.remove(meshes,do_unlink=True) # delete material
    #bpy.data.materials.remove(bpy.data.materials["My material"],do_unlink=True) # delete material
    for material in list(bpy.data.materials):
        bpy.data.materials.remove(material,do_unlink=True) # delete material
    for im in list(bpy.data.images):
        bpy.data.images.remove(im,do_unlink=True)
    #bpy.ops.object.delete(use_global=True) #delete the object
    for obj in list(bpy.data.objects):        
        if obj is not bpy.data.objects['Camera']:
            bpy.data.objects.remove(obj,do_unlink=True)    
    bpy.ops.ptcache.free_bake_all()
    
#clear_assets()