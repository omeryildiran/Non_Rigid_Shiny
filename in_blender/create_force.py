import bpy
import random
class force():
    def __init__(self,force_type="FORCE"):
        self.force_type=force_type
        if force_type=="FORCE":
            self.efx_name="Force"
        elif force_type=="VORTEX":
            self.efx_name="Vortex"
        elif force_type=="FLUID":
            self.efx_name="FluidField"
        elif force_type=="WIND":
            self.efx_name="Wind"
        elif force_type=="MAGNET":
            self.efx_name="Magnet"
        elif force_type=="LENNARDJ":
            self.efx_name="Lennard-Jones"
        elif force_type=="GUIDE":
            self.efx_name="CurveGuide"                            
        elif force_type=="TURBULENCE":
            self.efx_name="Turbulence"
        elif force_type=="DRAG":
            self.efx_name="Drag"
        elif force_type=="CHARGE":
            self.efx_name="Charge"
                                    
        self.__create_effector()
        
    def __create_effector(self):
        bpy.ops.object.effector_add(type=self.force_type, enter_editmode=False, location=(0, 0, 0))
        self.force=bpy.data.objects[self.efx_name]
        self.force.field.shape="POINT"#or LINE, PLANE 
        self.force.scale[0]=1.5
        self.force.scale[1]=1.5
        self.force.scale[2]=1.5
        self.force.field.flow=0.000 #[0.000,10.000]
        self.force.field.noise=1.000 #[1.000,10.000]
        self.force.field.apply_to_rotation=True
        self.force.field.apply_to_location=True
        if self.efx_name=="Force":
            self.__create_force()
        elif self.efx_name=="Vortex":
            self.__create_vortex()
        elif self.efx_name=="FluidField":
            self.__create_fluid_flow()
        elif self.efx_name=="Wind":
            self.__create_wind()
        elif self.efx_name=="Magnet":
            self.__create_magnet()
        elif self.efx_name=="Lennard-Jones":
            self.__create_lennard()
        elif self.efx_name=="CurveGuide":
            self.__create_guide()
        elif self.efx_name=="Drag":
            self.__create_drag()
        elif self.efx_name=="Turbulence":
            self.__create_turbulance()
        elif self.efx_name=="Charge":
            self.__create_charge()															
        
    def __create_vortex(self):
        self.force.rotation_euler[0]=random.uniform(0.00,6.28)
        self.force.rotation_euler[1]=random.uniform(0.00,6.28)
        self.force.rotation_euler[2]=random.uniform(0.00,6.28)
        self.force.field.strength=random.uniform(30.00,50.00)

    def __create_force(self):
        self.force.field.strength=random.uniform(30.00,60.00)
    
    def __create_fluid_flow(self):
        self.force.field.strength=10.00

    def __create_wind(self):
        self.force.field.strength=random.uniform(30.00,50.00)
        self.force.field.flow=random.uniform(0.00,5.00)
         
    def __create_magnet(self):
        self.force.field.strength=random.uniform(1.00,15.00)
        self.force.field.flow=random.uniform(0.00,3.00)

    def __create_turbulance(self):
        self.force.field.strength=random.uniform(1.00,15.00)
        self.force.field.flow=random.uniform(0.00,3.00)

    def __create_charge(self):
        self.force.field.strength=10
        self.force.field.flow=0	         

    def __create_guide(self):
        self.force.field.guide_minimum=15

    def __create_drag(self):
        bpy.context.object.field.linear_drag = 1
        bpy.context.object.field.quadratic_drag = 1

    def __create_lennard(self):
        self.force.field.strength=15
        self.force.field.flow=0.5

    def delete_force(self):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # Select the object
        objs = bpy.data.objects
        bpy.data.objects.remove(objs[self.efx_name], do_unlink=True)
        
        
#delete_force()
#force=force(force_type="VORTEX")
#force.create_force()
#force.delete_force()