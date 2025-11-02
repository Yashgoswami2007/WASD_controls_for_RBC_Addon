import bpy

# --- Settings ---
DRIVE_VALUE = 30.0
STEERING_VALUE = 10.0

keys = {"W": False, "A": False, "S": False, "D": False}

def update_rbc_controls():
    try:
        rig = bpy.context.scene.sna_rbc_rig_collection[0]
        
        # Drive control
        if keys["W"]:
            rig.rig_drivers.drive = DRIVE_VALUE
        elif keys["S"]:
            rig.rig_drivers.drive = -DRIVE_VALUE
        else:
            rig.rig_drivers.drive = 0.0
        
        # Steering control
        if keys["D"]:
            rig.rig_drivers.steering = STEERING_VALUE
        elif keys["A"]:
            rig.rig_drivers.steering = -STEERING_VALUE
        else:
            rig.rig_drivers.steering = 0.0
            
    except Exception as e:
        print(f"RBC control error: {e}")

def frame_handler(scene):
    update_rbc_controls()

def register_handlers():
    if frame_handler not in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.append(frame_handler)

def modal_operator(self, context, event):
    if event.type in keys:
        keys[event.type] = (event.value == 'PRESS')
        return {'RUNNING_MODAL'}
    
    if event.type == 'ESC':
        # Reset controls on exit
        try:
            rig = bpy.context.scene.sna_rbc_rig_collection[0]
            rig.rig_drivers.drive = 0.0
            rig.rig_drivers.steering = 0.0
        except:
            pass
        return {'FINISHED'}
    
    return {'PASS_THROUGH'}

class CarControlOperator(bpy.types.Operator):
    bl_idname = "wm.car_control"
    bl_label = "Car Control Operator"
    
    def modal(self, context, event):
        return modal_operator(self, context, event)
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(CarControlOperator)
    register_handlers()
    bpy.ops.wm.car_control('INVOKE_DEFAULT')
    print("✅ RBC Car Control Active! W/S for drive, A/D for steering, ESC to exit")

register()