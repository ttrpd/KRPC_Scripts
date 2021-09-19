import krpc
import math
import time

# https://en.wikipedia.org/wiki/Hohmann_transfer_orbit#Calculation
def init_to_transfer_delta_v(mu, r1, r2):
    return math.sqrt(mu/r1) * (math.sqrt((2*r2)/(r1+r2)) - 1)

def create_transfer_node(vessel, target_orbit, ut):
    std_grav_param = vessel.orbit.body.gravitational_parameter
    init_radius = vessel.orbit.semi_major_axis
    final_radius = target_orbit.semi_major_axis
    # Compute delta_v to achieve transfer orbit using vis-viva equation
    delta_v1 = init_to_transfer_delta_v(std_grav_param, init_radius, final_radius)
    node = vessel.control.add_node(ut + 60)# add a new node 1 minute from now
    node.prograde = delta_v1

    # adjust transfer node time until the resulting orbit intercepts the target
    target_soi = sc.target_body.sphere_of_influence
    while node.orbit.distance_at_closest_approach(target_orbit) > target_soi:
        node.ut += vessel.orbit.period*0.05

def create_insertion_node(vessel, ut):
    # sc.warp_to(ut + vessel.orbit.time_to_soi_change + 10)
    ut_at_periapsis = vessel.orbit.ut_at_true_anomaly(0)
    node = vessel.control.add_node(ut_at_periapsis)
    periapsis_speed = vessel.orbit.orbital_speed_at(ut_at_periapsis)
    desired_orbital_velocity = math.sqrt(vessel.orbit.body.gravitational_parameter/vessel.orbit.periapsis_altitude)
    node.prograde = 1.05*(desired_orbital_velocity - periapsis_speed)
    print("periapsis speed: "+str(periapsis_speed))
    print("desired orbital velocity: "+str(desired_orbital_velocity))
    print("retrograde delta v: "+str(node.prograde))



conn = krpc.connect("create_transfer_node")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()
target_orbit = sc.target_body.orbit

create_transfer_node(vessel, target_orbit, sc.ut)

# create_insertion_node(vessel, sc.ut)




