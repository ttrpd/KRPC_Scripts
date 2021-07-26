import krpc
import math
import time

# get target_apoapsis and target_periapsis
# calculate target_average_altitude using (target_apoapsis+target_periapsis) / 2
# get time to periapsis
# create maneuver node at ut of periapsis
# increase prograde component of maneuver until new periapsis reaches average_target_altitude or a target encounter happens
# if no target encounter happens, increase time of maneuver to adjust its place in the orbit until a target encounter happens