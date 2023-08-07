"""Soft Body Animation"""
from tabnanny import check
import bpy
from math import radians
import random
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
create_force=bpy.data.texts['create_force.py'].as_module()
camera_pos=bpy.data.texts['camera_pos.py'].as_module()
clear_func=bpy.data.texts['clear_func.py'].as_module()
##############################################################################################
##############################################################################################
proj_dir="E:/Documents/Omer_repos/UBUNTU/Documents/My_Repos/Blender/"
slash='/'
sh='_'  
subtre='_'
### TAKE NOISE TEXTURE
dir_texture_general=proj_dir+"texture_maps"+slash#"/home/omer/Documents/My_Repos/Blender/texture_maps/"
dir_matched_noise=dir_texture_general+"matched_noise"+slash
dir_pure_hdrs_png=dir_texture_general+"a_pure_hdrs_png"+slash
dir_noises=[dir_matched_noise,dir_pure_hdrs_png]

### TAKE ILLUMINATION MAP
hdrs_general="E:/Documents/Omer_repos/UBUNTU/Documents/My_Repos/Blender/HDR files/"
dir_pure_hdrs=hdrs_general+"a_pure_hdrs/"
dir_matched_noise_hdrs=hdrs_general+"a_matched_noise_hdrs/"
dir_hdrs=[dir_pure_hdrs,dir_matched_noise_hdrs]

### Make a noise list and stack it
noise_dir=hdrs_general+"matched_nosie_b"+slash #get path
noise_list=os.listdir(noise_dir) # get every item as list
noise_list=sorted(noise_list)

#noise_list=noise_list
ligh_field_dir=hdrs_general+"light_fields_gray"+slash
light_field_list=os.listdir(ligh_field_dir)
light_field_list=sorted(light_field_list)
#light_field_list=light_field_list
real_texture_dir=hdrs_general+"real_textures"+slash
real_texture_list=os.listdir(real_texture_dir)


## MAKE stacked noise list
stack_num=len(noise_list)//len(light_field_list)
stack_noises=[]
for i in range(stack_num): 
    stack_noises.append(noise_list[((i)*stack_num):((i+1)*stack_num)]) 
       

#a=animate("ico_sphere",init_rotation,scale=1.8,surface="shiny",texture=tex)
#a.rigid_anim(init_rotation,0,45)
#a.non_rigid_anim(speed=0.15 ,push=0.0 ,pull=0.8)
soft_types=["FORCE","VORTEX","FLUID","WIND","MAGNET","LENNARDJ","GUIDE","TURBULENCE","DRAG","CHARGE"]
rots=[60,-60,-50,50,40,-40,30,-30]
#rots=rots*3
rots=list(range(-53,-30))+list(range(30,53))+[0]*10   
       
pi=3.14
init_rotation=45

############################################## ################################################
##############################################################################################  

class object:
    def __init__(self,shape,rotation=None,scale=1.8):
        if shape=="ico_sphere":
            bpy.ops.mesh.primitive_ico_sphere_add()
            self.so=bpy.context.active_object #selected object(self.so) is active object
            #modifiers
            mod_subsurf=self.so.modifiers.new("My Modif","SUBSURF")
            mod_subsurf.levels=3  #or random.randint(#is easier faster  
            mod_subsurf.render_levels=6  #or random.randint(#is easier faster  
            mod_subsurf.quality=6
            bpy.ops.object.convert(target='MESH')
        elif shape=="cube":
            bpy.ops.mesh.primitive_cube_add()
            self.so=bpy.context.active_object #selected object(self.so) is active object
            #modifiers
            mod_subsurf=self.so.modifiers.new("My Modif","SUBSURF")
            mod_subsurf.levels=2  #or random.randint(#is easier faster  
            mod_subsurf.render_levels=6
            mod_subsurf.quality=2
            mod_cast=self.so.modifiers.new("Casting","CAST")
            mod_cast.cast_type = 'SPHERE'
            mod_cast.factor=1
            bpy.ops.object.convert(target='MESH')
            mod_subsurf=self.so.modifiers.new("My Modif","SUBSURF")
            mod_subsurf.levels=3  #or random.randint(#is easier faster  
            mod_subsurf.render_levels=6
            mod_subsurf.quality=6
            bpy.ops.object.convert(target='MESH')

        elif shape=="uv_sphere":
            bpy.ops.mesh.primitive_uv_sphere_add()
            self.so=bpy.context.active_object #selected object(self.so) is active object
            #modifiers
            mod_subsurf=self.so.modifiers.new("My Modif","SUBSURF")
            mod_subsurf.levels=3  #or random.randint(#is easier faster
            mod_subsurf.render_levels=6   
            mod_subsurf.quality=6
            bpy.ops.object.convert(target='MESH')
        
        self.rotation=rotation
        self.so=bpy.context.active_object #selected object(self.so) is active object
        #location of object 
        self.so.location[0],self.so.location[1],self.so.location[2]=0,0,0
        self.so.scale[2]=scale
        #rotate
        if rotation!=None:
            self.so.rotation_euler[0] +=radians(rotation)    
        #smoothh the object
        bpy.ops.object.shade_smooth()        
        
        """Create Displacement modifier for Shape Deformation"""
        mod_disp= self.so.modifiers.new("My Displacement","DISPLACE")
        #create texturess23
        new_text=bpy.data.textures.new("My Texture","CLOUDS",)
        noise_bases=["BLENDER_ORIGINAL","ORIGINAL_PERLIN",'IMPROVED_PERLIN']
        new_text.noise_basis = noise_bases[random.randint(0,2)]   
        #new_text.noise_basis="BLENDER_ORIGINAL"
        new_text.noise_type = "SOFT_NOISE"
        #change edit texuter
        if new_text.noise_basis=="BLENDER_ORIGINAL":        
            new_text.noise_scale=random.uniform(1.00,2.00)
        else:
            new_text.noise_scale=random.uniform(0.82,2.00)
        
        if new_text.noise_scale > 1.15 and new_text.noise_scale < 1.5:
            new_text.noise_depth=random.randint(0,1)
        elif new_text.noise_scale > 1.5:
            new_text.noise_depth=random.randint(1,2)
        else:
            new_text.noise_depth=0
        
        new_text.nabla=random.uniform(0.00,0.10)
        #assign the texture to dipslacement modif
        mod_disp.texture = new_text

class material(object):
    def __init__(self, anim, rotation=None, scale=1.8,surface=None,texture=None):
        super().__init__(anim, rotation, scale)
        """Create Material"""
        new_mat = bpy.data.materials.new(name="My material")
        self.so.data.materials.append(new_mat)
        new_mat.use_nodes=True
        nodes=new_mat.node_tree.nodes # here short url for nodes
        if surface=="shiny":
            nodes["Principled BSDF"].inputs[6].default_value = 1#metalic
            nodes["Principled BSDF"].inputs[7].default_value = 1#specular
            nodes["Principled BSDF"].inputs[8].default_value = 0#specular ting
            nodes["Principled BSDF"].inputs[9].default_value = 0#roughness
            nodes["Principled BSDF"].inputs[10].default_value = 1# Antisoptic
            nodes["Principled BSDF"].inputs[14].default_value = 0#clearcoat
            nodes["Principled BSDF"].inputs[17].default_value = 1#transmission
        elif surface=="matte":
            nodes["Principled BSDF"].inputs[6].default_value = 0  # Metalic
            nodes["Principled BSDF"].inputs[7].default_value = 0  # Specular
            nodes["Principled BSDF"].inputs[8].default_value = 1  # Specular Tint
            nodes["Principled BSDF"].inputs[9].default_value = 1  # Roughness
            nodes["Principled BSDF"].inputs[10].default_value = 0  # Antisoptic
            nodes["Principled BSDF"].inputs[14].default_value = 0 #clearcoat
            nodes["Principled BSDF"].inputs[15].default_value = 1 #clearcoat roughness
            nodes["Principled BSDF"].inputs[13].default_value = 0 #sheen tint
            nodes["Principled BSDF"].inputs[17].default_value = 0 #transmission
            """Embed Texture to material"""
            #material_output= nodes.get("Material Output") 
            bsdf_output=nodes.get("Principled BSDF")   
            node_texture=nodes.new(type='ShaderNodeTexImage')
            node_texture.location = (-300, 100)
            nodes["Image Texture"].image = texture
            links = new_mat.node_tree.links
            links.new(nodes["Image Texture"].outputs[0],bsdf_output.inputs[0])
            if texture.name in real_texture_list:
                nodes["Image Texture"].projection='BOX'
                nodes["Image Texture"].projection_blend=0.1
            else:    
                nodes["Image Texture"].projection='SPHERE'
            nodes["Image Texture"].interpolation='Smart'                
            nodes["Image Texture"].extension='REPEAT'
            image_output=nodes.get("Image Texture")
            node_coordinate=nodes.new(type="ShaderNodeTexCoord")
            node_coordinate.location = (-600, 100)
            links.new(nodes["Texture Coordinate"].outputs[0],image_output.inputs[0])
            #bpy.ops.node.add_search(use_transform=True, node_item='61')


class animate(material):
    def __init__(self, anim, rotation=None, scale=1.8, surface=None,texture=None):
        super().__init__(anim, rotation, scale, surface, texture)
        
    def non_rigid_anim(self,push=0.0,pull=0.5,force_method=None):
        """Soft Body""" 
        force=create_force.force(force_type=force_method)       
        scene = bpy.context.scene
        scene.frame_set(1)
        bpy.context.view_layer.objects.active=bpy.data.objects[bases[base]]
        bpy.ops.object.modifier_add(type='SOFT_BODY')
        soft_body=bpy.context.object.modifiers["Softbody"]
        soft_body.settings.speed=0.09
        soft_body.settings.plastic=30        
        soft_body.settings.bend=1.5
        if force_method  =='DRAG':
            soft_body.settings.speed=0.055
        elif force_method=='FLUID':
            soft_body.settings.speed=0.05
            soft_body.settings.bend=4
        elif force_method == 'TURBULENCE':
            soft_body.settings.speed=0.07
        elif force_method=='CHARGE':
            soft_body.settings.speed=0.08
            soft_body.settings.bend=0.7
        elif force_method=="GUIDE" and push==0.5:
            soft_body.settings.speed=0.07
        elif force_method=="LENNARDJ" and push==0.5:
            soft_body.settings.speed=0.06    
        elif force_method=="WIND":
            soft_body.settings.speed=0.12
        elif force_method=='FORCE' and push==0.5:
            soft_body.settings.speed=0.07
            soft_body.settings.bend=3
                                                     
        soft_body.settings.pull=pull  
        soft_body.settings.push=push
        soft_body.settings.use_goal = False
        soft_body.settings.effector_weights.gravity = 0
        soft_body.point_cache.frame_end=20
        scene.frame_set(20)
    def rigid_anim(self,rot_x=0,rot_y=0,rot_z=0): 
        def deg2rad(x):
            return x*(pi/180)
        rot_x,rot_y,rot_z=deg2rad(rot_x),deg2rad(rot_y),deg2rad(rot_z)
        scene = bpy.context.scene
        
        scene.frame_set(1)    
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        self.so.rotation_euler[2]=0
        self.so.rotation_euler[1]=0
        self.so.rotation_euler[0]=self.rotation
        scene.frame_set(20)
        self.so.rotation_euler[2]=rot_z
        self.so.rotation_euler[1]=rot_y
        self.so.rotation_euler[0]=rot_x
        bpy.ops.anim.keyframe_insert_menu(type='Rotation' )


#######################################################################################################################
push_pull=[[0.25,0.75],[0.5,0.5]]
#######################################################################################################################
def create_files(rep=1,texture_name=None,hdr=None,surface=None,general_type=None,test=False):
    gray=random.uniform(0.108,0.324)
    bpy.data.worlds["World"].node_tree.nodes["Background.002"].inputs[0].default_value = (gray, gray, gray, 1)
    if texture_name is not None:
        tex=bpy.data.images.get(texture_name) #load image to tex var
    for x in range(1):
        x=rep
        scale=1.8 
        init_rot_x=random.randint(0,90)
        a=animate(base,init_rot_x,scale,surface,texture=tex)
        orient_init=str([init_rot_x,0,0])
        if anim =="rigid":
            random.shuffle(rots)
            a.rigid_anim(rots[0],rots[1],rots[2])
            orient_end=str([rots[0],rots[1],rots[2]])
            soft_type='None'
        else:  
            type_index=random.randint(0,len(soft_types)-1)
            soft_type=soft_types[type_index]
            random.shuffle(push_pull)
            a.non_rigid_anim(push=push_pull[0][1],pull=push_pull[0][0],force_method=soft_type)
            orient_end=orient_init
            bpy.ops.ptcache.bake_all(bake=True)
        ### camera   
        camera_pos.update_camera(distance=4)
        ##  Naming
        if test==True:
            break                     
        hdr=hdr[0:-4]
        disp_size=round(bpy.data.textures["My Texture"].noise_scale,3) # between 0.60 and 2.00 -> lower is more bumpy
        disp_depth=bpy.data.textures["My Texture"].noise_depth # 0 1 or 2
        disp_prop=[disp_size,disp_depth]
        if surface=="shiny":
            texture_name='NoneNone'
        obj_type=surface+"_"+anim
        fName=anim+'_'+general_type
        obj_name=obj_type+'_'+hdr+'_'+texture_name[0:-4]+"_"+orient_init+'_'+orient_end+'_'+soft_type+'_'+str(disp_size)+'_'+str(disp_depth)+'_'+str(x)
        ### render
        bpy.context.scene.render.image_settings.color_mode = 'BW'
        bpy.context.scene.render.image_settings.file_format = "PNG" # FFMPEG / PNG
        if bpy.context.scene.render.image_settings.file_format=="FFMPEG":
            bpy.context.scene.render.filepath=proj_dir+'Object_movs/'+anim+'_'+surface+"/"+anim+'_'+surface+'_'+hdr+texture_name[1:6]+'_'+str(x)+"_"
        else:
            bpy.context.scene.render.filepath = proj_dir+"Objects/"+fName+"/"+obj_name+"/"+obj_name+"_"
        bpy.ops.render.render(animation=True)

        clear_func.clear_assets()

 
""" Take Object Type and Send to Render Accordingly """        
def in_tex_probe(rep=1,texture=noise_list[0],env=light_field_list[0],dir_txt=noise_dir,dir_env=ligh_field_dir,surface=None,general_type=None,test=False):	
    ## Assert ENViroment
    bpy.data.images.load(dir_env+env, check_existing=True) #load
    probe=bpy.data.images.get(env)
    bpy.data.worlds["World"].node_tree.nodes["Environment Texture"].image=probe
    ## Assert TEXture Map
    bpy.data.images.load(dir_txt+texture, check_existing=True) # load
    # tex=bpy.data.images.get(texture_name) #load image to tex var
    create_files(rep,texture_name=texture,hdr=env,surface=surface,general_type=general_type,test=test)


#######     SHINY
### Light Field as ENV map (10) - NEED to done 100 times	
def obj_type_1(rep=1,test=False):
    for light_field in light_field_list:
        in_tex_probe(env=light_field,dir_env=ligh_field_dir,surface="shiny",rep=rep,general_type='type1',test=test) #00)
        if test==True: break


### NOISE as ENViroment Map (100) - NEED to done 10 times	
def obj_type_3(rep=1,test=False):
    randomlist = random.sample(range(0, 100), 10)
    noises=[]
    for i in randomlist:
        noises.append(noise_list[i])
    for noise in noises:	
        in_tex_probe(env=noise,dir_env=noise_dir,surface="shiny",rep=rep,general_type='type3',test=test)
        if test==True: break

#######     MATTE
### Noise as TEXture Map and Light field as illumination (10x100= 1000) - No NEED to rep
def obj_type_4(rep=1,test=False):
    randomlist = random.sample(range(0, 10), 10)
    j=0
    for i in randomlist:
        light_field=light_field_list[i]
        noise=stack_noises[i][randomlist[i]]
        in_tex_probe(dir_txt=noise_dir,texture=noise,env=light_field,dir_env=ligh_field_dir,surface="matte",rep=1,general_type='type4',test=test)
        j+=1
        if test==True: break


### Real Texture as TEXture Map #(10x10= 100) - NEED to done 10 times
def obj_type_2(rep=1,test=False):
    randomlist = random.sample(range(0, 10), 10)
    for i in randomlist:
        txt=real_texture_list[i]
        light_field=light_field_list[i]
        in_tex_probe(dir_txt=real_texture_dir,texture=txt,env=light_field,dir_env=ligh_field_dir,surface="matte",rep=1,general_type='type2',test=test)
        if test==True: break
        
def test_obj():
    txt=real_texture_list[0]
    env=light_field_list[0]
    dir_env=ligh_field_dir
    dir_txt=real_texture_dir    
    ## Assert ENViroment
    bpy.data.images.load(dir_env+env, check_existing=True) #load
    probe=bpy.data.images.get(env)
    bpy.data.worlds["World"].node_tree.nodes["Environment Texture"].image=probe
    ## Assert TEXture Map
    bpy.data.images.load(dir_txt+txt, check_existing=True) # load
    tex=bpy.data.images.get(txt) #load image to tex var
    original_rot=45
    a=animate(base,original_rot,scale=1.8,surface="matte",texture=tex)
    #a.rigid_anim(original_rot,0,45)
    a.non_rigid_anim(speed=0.15,push=0.25 ,pull=0.65)


    
original_rot=45
bases={'uv_sphere':'Sphere','ico_sphere':'Icosphere','cube':'Cube'}
base="cube"
anim="soft"
#create_files(1,10,format,surface,anim,base)

#force=force
#force.create_vortex()

#create_force.force("VORTEX")
clear_func.clear_assets()
obj_type_3(test=True)
#test_obj()
#clear_func.clear_assets()
#obj_type_1()
def whole_creation():
    for rep in range(50):
        obj_type_1(rep=rep)
        obj_type_2(rep=rep)
        obj_type_3(rep=rep)
        obj_type_4(rep=rep)
#obj_type_3( test=True)
#clear_func.clear_assets()
#for i in ["soft","rigid"]
#    anim=i
#    whole_creation():


