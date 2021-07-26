

def get_space_center_streams(conn, sc):
    streams = {}
    streams["warp_factor"] = conn.add_stream(getattr, sc, "warp_factor")
    streams["ut"] = conn.add_stream(getattr, sc, "ut")
    return streams


def get_vessel_streams(conn, vessel):
    streams = {}
    streams["sas"] = conn.add_stream(getattr, vessel.auto_pilot, "sas")
    return streams

def get_flight_streams(conn, flight):
    streams = {}
    streams["surface_altitude"] = conn.add_stream(getattr, flight, "surface_altitude")
    streams["pitch"] = conn.add_stream(getattr, flight, "pitch")
    streams["heading"] = conn.add_stream(getattr, flight, "heading")
    streams["roll"] = conn.add_stream(getattr, flight, "roll")
    return streams