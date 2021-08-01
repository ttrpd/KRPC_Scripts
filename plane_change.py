import krpc
import math
import time

"""
Calculates the delta-v required for a plane change maneuver
between a target's orbit and a vessel's orbit, assuming the
inclination difference between the two orbits is less than
90 degrees.

target_orb: Orbit - The orbit of the target body
vessel_orb: Orbit - The orbit of the active vessel
ut_asc: double - universal time of ascending node in seconds

returns: a value representing delta-v, calculated using the
         equation given here (https://en.wikipedia.org/wiki/Orbital_inclination_change)
"""
def calculate_plane_change_delta_v(target_orb, vessel_orb, ut_asc):
    delta_incl = vessel_orb.relative_inclination(target_orb)
    print("Initial relative inclination: "+str((180/math.pi)*delta_incl)+" degrees")
    w = vessel_orb.argument_of_periapsis
    e = vessel_orb.eccentricity
    f = vessel_orb.true_anomaly_at_ut(ut_asc)
    n = (2*math.pi) / vessel_orb.period # (period is in seconds)
    a = vessel_orb.semi_major_axis
    numerator = (2 * math.sin(delta_incl/2) * math.sqrt(1-(e**2)) * math.cos(w+f) * n * a)
    denominator = (1 + e*math.cos(f))
    return numerator / denominator

conn = krpc.connect("plane_change_maneuver")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()

if sc.target_vessel is not None:
    target = sc.target_vessel
elif sc.target_body is not None:
    target = sc.target_body
else:
    raise ValueError("No target")


targ_orbit = target.orbit
orbit = vessel.orbit
ut_of_an = orbit.ut_at_true_anomaly(orbit.true_anomaly_at_an(targ_orbit))

print("Creating plane change maneuver node")
inclination_node = vessel.control.add_node(ut_of_an)
inclination_node.normal = -1*calculate_plane_change_delta_v(targ_orbit, orbit, ut_of_an)
while inclination_node.orbit.relative_inclination(targ_orbit)*(180/math.pi) > 0.05:
    inclination_node.normal -= 2
print("Delta-v (m/s): "+str(inclination_node.normal))
print("Final relative inclination: "
    +str(inclination_node.orbit.relative_inclination(targ_orbit)*(180/math.pi))
    +" degrees"
)
    


