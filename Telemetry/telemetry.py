import krpc
import time
import sys
import telemetry_printing as telprnt
import telemetry_streams as telstrm

def delete_previous_lines(num):
    for i in range(num):
        sys.stdout.write('\x1b[1A')

conn = krpc.connect("Telemetry")
sc = conn.space_center
vessel = sc.active_vessel
flight = vessel.flight()

sc_streams = telstrm.get_space_center_streams(conn, sc)
flight_streams = telstrm.get_flight_streams(conn, flight)
vessel_streams = telstrm.get_vessel_streams(conn, vessel)

num_lines = 0
while True:
    time.sleep(0.2)
    num_lines += telprnt.print_space_center_info(sc_streams)
    num_lines += telprnt.print_vessel_info(vessel_streams)
    num_lines += telprnt.print_flight_info(flight_streams)
    delete_previous_lines(num_lines)
    num_lines = 0

# altitude, vertical velocity

# pitch heading and roll with angle and direction

# orbital surface and target velocity

# time until next maneuver node
# burn time, burn delta_v

# event logging