import krpc
import math
import time

def init_to_transfer_delta_v(mu, r1, r2):
    return math.sqrt(mu/r1) * (math.sqrt((2*r2)/(r1+r2)) - 1)

conn = krpc.connect("create_transfer_node")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()

# https://en.wikipedia.org/wiki/Hohmann_transfer_orbit#Calculation

std_grav_param = vessel.orbit.body.gravitational_parameter
init_radius = vessel.orbit.semi_major_axis
final_radius = sc.target_body.orbit.semi_major_axis
# Compute delta_v to achieve transfer orbit using vis-viva equation
delta_v1 = init_to_transfer_delta_v(std_grav_param, init_radius, final_radius)

# transfer_time is 1/2 the transfer orbit period
# wait until target is transfer_time away from the point opposite vessel periapsis
# create maneuver node at that point, burning prograde for total delta_v

# wait transfer_time seconds
# make maneuver node at periapsis around target
# target_velocity = orbital velocity of a circular orbit where R is current periapsis
# current_velocity = orbital velocity of current orbit (where R is current semi-major axis)
# burn retrograde at maneuver for (current_velocity - target_velocity) m/s


