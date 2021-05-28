import pygame
from dronekit import connect,VehicleMode, LocationGlobalRelative,Vehicle
import time 
from pymavlink import mavutil

pygame.init()    
pygame.display.set_caption(u'Drone Controls')  
s = pygame.display.set_mode((200,200))  

vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("[INFO] waiting to initialize.....")
        time.sleep(1)
    print("[INFO] arming motors")

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True 

    while not vehicle.armed:
        print("[INFO] waiting to arm")
        time.sleep(1)



    print("[INFO] Taking off....")
    vehicle.simple_takeoff(altitude)

    while True:
        print('[INFO] Altitude {}'.format(vehicle.location.global_relative_frame.alt))
        if vehicle.location.global_relative_frame.alt >= 0.95 * altitude:
            print("[INFO] Target altitude reached ")
            break
        time.sleep(1)

def send_ned_velocity(Vx, Vy, Vz, duration):
 
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,      
        0, 0,  
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
        0b0000111111000111, 
        0, 0, 0, 
        Vx, Vy, Vz, 
        0, 0, 0, 
        0, 0)    

    # send command to vehicle on 1 Hz cycle
    for i in range(0,duration):
        vehicle.send_mavlink(msg)
        
#yaw conditon
def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    


def keyboard_controls():
    while True :
        event = pygame.event.wait()  
        if event.type == pygame.QUIT:
            break  
        #### PRESS KEYS
        
        if  event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                print("moving forward")
                send_ned_velocity(40,0,0,5)

            elif event.key == pygame.K_a:
                print("moving left")
                send_ned_velocity(0,-40,0,5)

            elif event.key == pygame.K_s:
                print("moving backward")
                send_ned_velocity(-40,0,0,5)

            elif event.key == pygame.K_d:
                print("moving right ")
                send_ned_velocity(0,40,0,5)
        
            elif event.key == pygame.K_UP:
                print("going up ")
                send_ned_velocity(0,0,-40,5)

            elif event.key == pygame.K_DOWN:
                print("going dowm")
                send_ned_velocity(0,0,40,5)

            elif event.key == pygame.K_LEFT:
                print("yaw left")
                condition_yaw(300,1)
                
            elif event.key == pygame.K_RIGHT:
                print("yaw right")
                condition_yaw(60,1)


        #### RELEASE KEYS 

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                print("stop moving forward")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_a:
                print("stop moving left")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_s:
                print("stop moving backward")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_d:
                print("stop moving right ")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_UP:
                print("stop going up ")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_DOWN:
                print("stop going dowm")
                send_ned_velocity(0,0,0,1)

            elif event.key == pygame.K_LEFT:
                print("stop yaw left")
                condition_yaw(0,1)

            elif event.key == pygame.K_RIGHT:
                print("stop yaw right")
                condition_yaw(0,1)




arm_and_takeoff(50)
            
keyboard_controls()