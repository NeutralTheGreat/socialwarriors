from sessions import session, neighbors, neighbor_session
from engine import timestamp_now, reset_trades

def get_player_info(USERID):
    # Update last logged in
    ts_now = timestamp_now()
    session(USERID)["playerInfo"]["last_logged_in"] = ts_now
    # Reset trades if possible
    reset_trades(session(USERID))
    # player
    player_info = {
        "result": "ok",
        "processed_errors": 0,
        "timestamp": ts_now,
        "playerInfo": session(USERID)["playerInfo"],
        "map": session(USERID)["maps"][0],
        "privateState": session(USERID)["privateState"],
        "neighbors": neighbors(USERID)
    }
	
    return player_info

def get_neighbor_info(userid, map_number):
    neighbor_info = {
        "result": "ok",
        "processed_errors": 0,
        "timestamp": timestamp_now(),
        "playerInfo": neighbor_session(userid)["playerInfo"],
        "map": neighbor_session(userid)["maps"][map_number],
        "privateState": neighbor_session(userid)["privateState"]
    }
    return neighbor_info