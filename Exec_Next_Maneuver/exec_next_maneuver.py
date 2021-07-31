import krpc
import math

# connect
conn = krpc.connect("warp_to_next_maneuver")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()

vessel.control.sas = True
vessel.control.sas_mode = sc.SASMode.maneuver

# get time of next maneuver (t)
next_node = vessel.control.nodes[0]
time_of_maneuver = next_node.ut
# get resulting orbit
target_orbit = next_node.orbit
# get initial orbit for error reporting
initial_orbit = vessel.orbit
# wait for reorientation
burn_vector = next_node.direction(vessel.orbital_reference_frame)
vessel.auto_pilot.wait()

print("reoriented")
# calculate burn duration using the Tsiolkovsky equation (https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)
delta_v = next_node.delta_v
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# warp to (t - burn duration)
if burn_time < 2:
    sc.warp_to(time_of_maneuver - burn_time)
else:
    sc.warp_to(time_of_maneuver - burn_time*0.5)

# begin burn
print("beginning burn")
vessel.control.throttle = 1.0

# get a stream of remaining delta v in burn
remaining_delta_v = conn.get_call(getattr, next_node, 'remaining_delta_v')

# create events for when remaining delta v drops below 10m/s, 2m/s, and 0.1m/s
dv_sub_10_expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(remaining_delta_v),
    conn.krpc.Expression.constant_double(10))

dv_sub_2_expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(remaining_delta_v),
    conn.krpc.Expression.constant_double(2))

dv_sub_01_expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(remaining_delta_v),
    conn.krpc.Expression.constant_double(0.1))
# tell the server to notify us when those events happen
dv_sub_10 = conn.krpc.add_event(dv_sub_10_expr)
dv_sub_2 = conn.krpc.add_event(dv_sub_2_expr)
dv_sub_01 = conn.krpc.add_event(dv_sub_01_expr)

# wait for delta v to drop below 10m/s
with dv_sub_10.condition:
    dv_sub_10.wait()
    # slow to 1/3 throttle
    vessel.control.throttle *= 0.25
# wait for delta v to drop below 2m/s
with dv_sub_2.condition:
    dv_sub_2.wait()
    # slow to 1/6 throttle
    vessel.control.throttle *= 0.25
# wait for delta v to drop below 0.1m/s
with dv_sub_01.condition:
    dv_sub_01.wait()
    # end burn
    vessel.control.throttle = 0.0
    next_node.remove()
    print("burn complete")

# report new orbit features and % error
def print_error(initial, current, target):
    target_diff = target - initial
    actual_diff = target - current
    print("\t"+str(100 - (actual_diff/target_diff)*100))

# get current orbit
current_orbit = vessel.orbit
print("\t\t\t\t\t\tOrbital fearures")
print("\t\t\tCurrent\t\t\tTarget\t\t\tError")
# apoapsis
print("\tApoapsis:\t"+str(current_orbit.apoapsis)+"\t"+str(target_orbit.apoapsis), end='')
print_error(initial_orbit.apoapsis, current_orbit.apoapsis, target_orbit.apoapsis)
# periapsis
print("\tPeriapsis:\t"+str(current_orbit.periapsis)+"\t"+str(target_orbit.periapsis), end='')
print_error(initial_orbit.periapsis, current_orbit.periapsis, target_orbit.periapsis)
# inclination
print("\tInclination:\t"+str(current_orbit.inclination)+"\t"+str(target_orbit.inclination), end='')
print_error(initial_orbit.inclination, current_orbit.inclination, target_orbit.inclination)

