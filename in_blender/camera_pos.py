import bpy
import mathutils
import random
def update_camera(camera=bpy.data.objects['Camera'], focus_point=mathutils.Vector((0.0, 0.0, 0.0)), distance=3):
    """
    Focus the camera to a focus point and place the camera at a specific distance from that
    focus point. The camera stays in a direct line with the focus point.

    :param camera: the camera object
    :type camera: bpy.types.object
    :param focus_point: the point to focus on (default=``mathutils.Vector((0.0, 0.0, 0.0))``)
    :type focus_point: mathutils.Vector
    :param distance: the distance to keep to the focus point (default=``10.0``)
    :type distance: float
    """
    focus_point = mathutils.Vector((random.random()*6,random.random()*6,random.random()*6))
    camera.location = mathutils.Vector((random.random()*6,random.random()*6,random.random()*6))
    looking_direction = camera.location - focus_point
    rot_quat = looking_direction.to_track_quat('Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    #camera.rotation_euler = ().to_euler()
    # Use * instead of @ for Blender <2.8
    camera.location = rot_quat @ mathutils.Vector((0.0, 0.0, distance))

#update_camera(bpy.data.objects['Camera'],distance=3.45)