from dronekit import connect, VehicleMode

print("Connecting to vehicle on")
vehicle = connect("udp:127.0.0.1:14550", wait_ready=True)


print ("Get some vehicle attribute values:")
print (" GPS: %s" % vehicle.gps_0)
print (" Battery: %s" % vehicle.battery)
print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
print (" Is Armable?: %s" % vehicle.is_armable)
print (" System status: %s" % vehicle.system_status.state)
print (" Mode: %s" % vehicle.mode.name)    # settable

vehicle.close()
print("Completed")
