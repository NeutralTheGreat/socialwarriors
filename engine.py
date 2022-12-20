import time
import json
from get_game_config import get_attribute_from_item_id

def timestamp_now():
    return int(time.time())

def map_add_item(map: dict, index: int, item: int, x: int, y: int, orientation: int = 0, timestamp: int = timestamp_now(), attr: dict = None, store: list = None, player: int = 1):
    if not attr:
        attr = {}
    if not store:
        store = []
    map["items"][str(index)] = [item, x, y, timestamp, orientation, store, attr, player]

def map_add_item_from_item(map: dict, index: int, item: list):
    map["items"][str(index)] = item

def map_get_item(map: dict, index: int):
    return map["items"][str(index)]

def map_pop_item(map: dict, index: int):
    return map["items"].pop(str(index))

def map_delete_item(map: dict, index: int):
    del map["items"][str(index)]

def push_unit(unit: dict, building: dict):
    building[5].append(unit)

def pop_unit(building: dict):
    return building[5].pop()

def apply_resources(save: dict, map: dict, resource: list):
    # So these will be negative if the user used resources and positive if the user gained resources, we can detect cheats by checking if any are less than 0 after applying
    unknown = resource[0]
    xp = resource[1]
    gold = resource[2]
    wood = resource[3]
    oil = resource[4]
    steel = resource[5]
    cash = resource[6]
    mana = resource[7]

    map["xp"] = max(map["xp"] + xp, 0)
    map["gold"] = max(map["gold"] + gold, 0)
    map["wood"] = max(map["wood"] + wood, 0)
    map["oil"] = max(map["oil"] + oil, 0)
    map["steel"] = max(map["steel"] + steel, 0)
    save["playerInfo"]["cash"] = max(save["playerInfo"]["cash"] + cash, 0)
    save["privateState"]["mana"] = max(save["privateState"]["mana"] + mana, 0)
    # map["timestamp"] = timestamp_now()

    # print(f"\n [?] Resources changed\n    Unknown {unknown}\n    Xp {xp}\n    gold {gold}\n    Wood {wood}\n    Oil {oil}\n    Steel {steel}\n    Cash {cash}\n    Mana {mana}")