import bpy
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import tempfile
from PIL import Image
from helper_functies import *
import cv2
import argparse

tmpdir = tempfile.TemporaryDirectory()
my_dpi = 96  # Afhankelijk van monitor #96

arg = argparse.ArgumentParser()
arg.add_argument('--json', default = None,help = 'setting json file')
arg = arg.parse_args()

# Parameter Setting ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# path setting ======================================================== #
root_path = 'C:\\Users\\GIST\\workspace\\RenderingModule-master\\'
obj_path = root_path + 'obj\\'  # input obj path
save_path = root_path + 'result\\'  # output img save path
save_name = "result.png"    # output img save name

# Input, Output =============================================================== #
part = '0'
size = [1024, 1024]       # output img size

# camera setting ===================================================== #
option = 'PERSP'    # Camera option 'PERSP': perspective, 'ORTHO': orthogonal
FOV = 60   # Camera focal length
radius = 2  # Camera Location, distance from origin
theta = 0.0001  # Camera Location, theta(euler angle)
phi = 0  # Camera Location, theta(euler angle)

# object setting ===================================================== #
name1 = '1.obj'
obj1_location = [0, 0, 0]   # Object location (x, y, z)
obj1_rotation = [0, 0, 0]   # Object rotation (x-axis, y-axis, z-axis)
obj1_color = [1, 1, 1]  # Object mask color (R, G, B), (1, 1, 1 = white)
obj1_scale = [1, 1, 1]  # Object scale (x, y, z)
name2 = '2.obj'
obj2_location = [0, 0, 0]
obj2_rotation = [0, 0, 0]
obj2_color = [1, 0, 1]
obj2_scale = [1, 1, 1]
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=+++++++++++++

if arg.json:
    setting = arg.json
else:
    ###### Example of json ######
    setting = {'object': [
        {'name': name1,
         'location': obj1_location,
         'rotation':obj1_rotation,
         'color': obj1_color,
         'scale': obj1_scale
         },
        {'name': name2,
         'location': obj2_location,
         'rotation': obj2_rotation,
         'color': obj2_color,
         'scale': obj2_scale
         }
        ],
        'camera': {
            'option': option,
            'fov': FOV,
            'radius': radius,
            'theta': theta,
            'phi': phi
        },
        'input': {
            'part': part
        },
        'output': {
            'size': size
        },
        'path': {
            'root_path': root_path,
            'obj_path': obj_path,
            'save_path': save_path,
            'save_name': save_name
        }
    }



# Preprocess of an obj =============================================== #

def pre_obj(name):
    # Import an original obj file
    file_path = setting['path']['obj_path'] + name
    imp_file_path = file_path.split('.')[0] + '_old.obj'
    try:
        os.remove(imp_file_path)
    except:
        pass
    bpy.ops.import_scene.obj(filepath=file_path, use_split_objects=False, use_split_groups=False)
    os.rename(file_path, imp_file_path)

    obj = bpy.context.selected_objects[0]
    for i in range(1, len(obj.material_slots)):
        bpy.data.objects[obj.name].active_material_index = i
        bpy.ops.object.material_slot_remove({'object': obj})

    # Export the obj file
    blend_file_path = bpy.data.filepath
    directory = os.path.dirname(blend_file_path)
    os.path.join(directory, name[1] + '.obj')
    bpy.ops.export_scene.obj(filepath=file_path)

    # Remove a mtl file and the original obj file

    os.remove(file_path.split('.')[0] + '.mtl')
    bpy.ops.object.delete(use_global=False)
# ==================================================================== #


# Class of objects =================================================== #
class Object:
    def __init__(self, name, obj, obj_data):
        # Re-Import the converted obj file
        file_loc = setting['path']['obj_path'] + name
        bpy.ops.import_scene.obj(filepath=file_loc)
        self.object = bpy.context.selected_objects[0]
        self.object_data = bpy.data.objects[self.object.name]

        # Shadow of object is removed
        self.object.active_material.use_shadeless = True    # True hasn't shadow, False has shadow

        # Set transform of object
        self.object.location = (0, 0, 0)
        self.object.rotation_euler = (0, 0, 0)
        self.object.scale = (0, 0, 0)

        obj.append(self.object)
        obj_data.append(bpy.data.objects[self.object.name])
        n[0] += 1

    def location(self, x, y, z):
        self.object.location[0] = x
        self.object.location[1] = y
        self.object.location[2] = z

    def scale(self, x, y, z):
        self.object.scale[0] = x
        self.object.scale[1] = y
        self.object.scale[2] = z

    def rotation(self, x, y, z):
        self.object.rotation_euler[0] = x * (math.pi / 180)
        self.object.rotation_euler[1] = y * (math.pi / 180)
        self.object.rotation_euler[2] = z * (math.pi / 180)

    def color(self, r, g, b):
        self.object_data.active_material.diffuse_color = (r, g, b)
        self.object_data.active_material.diffuse_intensity = 1
# ==================================================================== #


# Get an image ======================================================= #
def get_img(tmpdir=tmpdir, size=size, save_loc=save_path):

    # Save a postprocessed image of wireframe
    if os.path.isfile("wireframe.png"):
        img = cv2.imread(setting['path']['root_path'] +'wireframe.png')
        cv2.imwrite(os.path.join(setting['path']['root_path'], "result.png"), img)
        cv2.waitKey(0)
        os.remove('wireframe.png')
        return img

    scene = bpy.context.scene

    # Set resolution of x and y
    scene.render.resolution_x = size[0]
    scene.render.resolution_y = size[1]
    scene.render.resolution_percentage = 100
    scene.render.filepath = tmpdir.name + "/image"

    # Render the image
    bpy.ops.render.render(write_still=True)

    # Save the rendered image
    bpy.data.images['Render Result'].save_render(filepath=save_loc)

    img = Image.open(tmpdir.name + "/image.png")
    return img
# ==================================================================== #


# Freestyle information ============================================== #
class Freestyle_info:
    def __init__(self, name, select_by_visibility=True, select_by_edge_types=True, select_by_face_marks=False,
                 select_by_group=False, select_by_image_border=True, silhouette=False, edge_mark=False,
                 crease=False, border=False, contour=False, suggestive_contour=False, ridge_valley=False,
                 external_contour=False, material_boundary=False, thickness=2):
        self = bpy.context.scene.render.layers.active.freestyle_settings.linesets.new(name)

        # Refer to each function on the site.
        # http://builder.openhmd.net/blender-hmd-viewport-temp/render/freestyle/parameter_editor/line_set.html
        self.select_by_visibility = select_by_visibility
        self.select_by_edge_types = select_by_edge_types
        self.select_by_face_marks = select_by_face_marks
        self.select_by_group = select_by_group
        self.select_by_image_border = select_by_image_border

        self.select_silhouette = silhouette
        self.select_edge_mark = edge_mark
        self.select_crease = crease
        self.select_border = border
        self.select_contour = contour
        self.select_suggestive_contour = suggestive_contour
        self.select_ridge_valley = ridge_valley
        self.select_external_contour = external_contour
        self.select_material_boundary = material_boundary

        self.linestyle.thickness = thickness
# ==================================================================== #


# rendering each mode ================================================ #
def render_pass(n, part):
    # Set a standard mode
    bpy.context.scene.render.use_freestyle = False
    bpy.context.scene.render.use_edge_enhance = False

    # Set the color of the background and object to white
    bpy.context.scene.world.horizon_color = (1, 1, 1)
    for i in range(0, n[0]):
        obj[i].active_material.diffuse_color = (1, 1, 1)
        obj[i].active_material.diffuse_intensity = 0
        obj[i].active_material.transparency_method = 'MASK'

    sceneR = bpy.context.scene
    freestyle = sceneR.render.layers.active.freestyle_settings
    sceneR.render.use_freestyle = True
    freestyle.linesets.active_index = 0
    bpy.ops.scene.freestyle_lineset_remove()
    if part == '0':
        Freestyle_info(name='outline', contour=True, thickness=3.0)  # Outline
        Freestyle_info(name='details', silhouette=True, crease=True, border=True, thickness=1.7)    # inline
    elif part == '1':
        Freestyle_info(name="outline", crease=True, crease_angle=165, external_contour=True, thickness=4)  # Outline
        Freestyle_info(name="details", thickness=4, crease_angle=165, silhouette=True, crease=True, border=True)  # Inline
# ==================================================================== #


# Class of camera ==================================================== #
class Camera:
    def __init__(self, mode):
        bpy.ops.object.camera_add()
        self.camera_obj = bpy.data.objects['Camera']
        bpy.ops.object.empty_add(
            type='PLAIN_AXES', radius=1, view_align=False,
            location=(0, 0, 0),
            layers=(True, False, False, False, False, False, False,
                    False, False, False, False, False, False, False,
                    False, False, False, False, False, False)
        )

        # Perspective or Orthographic
        self.camera_obj.data.type = mode

        # Camera tracks to an object
        self.ttc = self.camera_obj.constraints.new(type='TRACK_TO')
        self.ttc.target = bpy.context.selected_objects[0]
        self.ttc.track_axis = 'TRACK_NEGATIVE_Z'
        self.ttc.up_axis = 'UP_Y'

        self.x = 0
        self.y = 0
        self.z = 0
        self.camera_obj.data.lens = 35

    def pos(self, r, theta, phi):
        # Spherical coord. is converted to cartesian coord.
        self.x = r * math.sin(theta * (math.pi / 180)) * math.cos(phi * (math.pi / 180))
        self.y = r * math.sin(theta * (math.pi / 180)) * math.sin(phi * (math.pi / 180))
        self.z = r * math.cos(theta * (math.pi / 180))

        # Position of camera
        self.camera_obj.location.x = self.x
        self.camera_obj.location.y = self.y
        self.camera_obj.location.z = self.z

    def intrinsic(self, focal, shift_x, shift_y):
        if self.camera_obj.data.type == 'PERSP':
            self.camera_obj.data.lens = focal
            self.camera_obj.data.shift_x = shift_x
            self.camera_obj.data.shift_y = shift_y
# ==================================================================== #


# Class of camera ==================================================== #
def obj_set(name, need_normal, obj_location, obj_rotation, obj_color, obj_scale):
    if need_normal == True:
        pre_obj(name)
    obj1 = Object(name, obj, obj_data)
    obj1.location(setting['object']['location'][0], setting['object']['location'][1], setting['object']['location'][2])  # Location (x, y, z)
    obj1.rotation(setting['object']['rotation'][0], setting['object']['rotation'][1], setting['object']['rotation'][2])  # Rotation (x-axis, y-axis, z-axis)
    obj1.color(setting['object']['color'][0], setting['object']['color'][1], setting['object']['color'][2])  # color (R, G, B)
    obj1.scale(setting['object']['scale'][0], setting['object']['scale'][1], setting['object']['scale'][2])  # scale (x, y, z)
# ==================================================================== #


zero(my_dpi)
#Set the light, RECOMMENDED TYPE :  SUN or POINT 
bpy.ops.object.lamp_add(type='SUN', location=(5,2,1))

# Set the environment lighting and the color of background
bpy.context.scene.world.light_settings.use_environment_light = True
bpy.context.scene.world.horizon_color = (0, 0, 0)  # the color of background


# Camera setting
cam = Camera(setting['camera']['option'])   # 'PERSP: perspective', 'ORTHO: orthogonal'
cam.intrinsic(setting['camera']['fov'], 0, 0)    # (FOV: 60 is optimized by tuning, shift_x, shift_y)
cam.pos(setting['camera']['radius'], setting['camera']['theta'], setting['camera']['phi'])  # (radius, theta, phi)

obj = []
obj_data = []
n = [0]
for i in range(len(setting['object'])):
    obj_set(setting['object'][i]['name'], True, setting['object'][i]['location'], setting['object'][i]['rotation'], setting['object'][i]['color'], setting['object'][i]['scale'])
# If you want to arrange more obj, add obj_set(name3, ...), obj_set(name4, ...), ...

# Save and show Image
render_pass(n, setting['input']['part'])
get_img(size=setting['output']['size'], save_loc=setting['path']['save_path'] + setting['path']['save_name'])
tmpdir.cleanup()
