import krpc
import numpy as np
import time

conn = krpc.connect("wait_for_orientation")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()
ap = vessel.auto_pilot


next_node = vessel.control.nodes[0]
time_of_maneuver = next_node.ut

vessel.control.sas = True
vessel.control.sas_mode = sc.SASMode.maneuver

burn_vector = next_node.direction(vessel.orbital_reference_frame)
# conn.drawing.add_direction(burn_vector, vessel.orbital_reference_frame)
direction = conn.add_stream(getattr, flight, 'direction')
ap.wait()
tolerance = 0.1
reoriented = False

print("Reoriented")