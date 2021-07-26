import datetime as dt

def print_space_center_info(sc_streams):
    lines = []
    lines.append("Space Center:")
    lines.append("\tuniversal time approx: "+str(dt.timedelta(seconds=sc_streams["ut"]())))
    lines.append("\tWarp Factor: "+str(sc_streams["warp_factor"]()))
    for line in lines:
        print(line)
    return len(lines)



def print_vessel_info(vessel_streams):
    lines = []
    lines.append("Vessel:")
    lines.append("\tSAS: "+str(vessel_streams["sas"]()))
    for line in lines:
        print(line)
    return len(lines)

def print_flight_info(flight_streams):
    lines = []
    lines.append("Flight:")
    lines.append("\tSurface Altitude (m): "+str(flight_streams["surface_altitude"]()))
    lines.append("\tPitch (degrees): "+str(flight_streams["pitch"]()))
    lines.append("\tHeading (degrees): "+str(flight_streams["heading"]()))
    lines.append("\tRoll (degrees): "+str(flight_streams["roll"]()))
    for line in lines:
        print(line)
    return len(lines)