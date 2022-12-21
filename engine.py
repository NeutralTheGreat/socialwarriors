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
    if player == 1:
        # if building is assigned to player, activate some properties
        # properties
        properties = get_attribute_from_item_id(item, "properties")
        # enable SI (Socially In Construction), because the game expects it
        if properties:
            properties = json.loads(properties)
            if "friend_assistable" in properties:
                if int(properties["friend_assistable"]) > 0:
                    attr["si"] = []
        # click to build
        click_to_build = get_attribute_from_item_id(item, "clicks_to_build")
        if click_to_build:
            if int(click_to_build) > 0:
                attr["nc"] = 0

    map["items"][str(index)] = [item, x, y, timestamp, orientation, store, attr, player]

def map_add_item_from_item(map: dict, index: int, item: list):
    map["items"][str(index)] = item

def map_get_item(map: dict, index: int):
    itemstr = str(index)
    if itemstr not in map["items"]:
        return None
    return map["items"][itemstr]

def map_pop_item(map: dict, index: int):
    itemstr = str(index)
    if itemstr not in map["items"]:
        return None
    return map["items"].pop(itemstr)

def map_delete_item(map: dict, index: int):
    itemstr = str(index)
    if itemstr not in map["items"]:
        return None
    del map["items"][str(itemstr)]

def push_unit(unit: dict, building: dict):
    building[5].append(unit)
    building[3] = timestamp_now()

def pop_unit(building: dict):
    if len(building[5]) > 0:
        return building[5].pop()
    else:
        return None

def add_store_item(map: dict, item: int, quantity: int = 1):
    itemstr = str(item)
    if itemstr not in map["store"]:
        map["store"][itemstr] = quantity
    else:
        map["store"][itemstr] += quantity

def remove_store_item(map: dict, item: int, quantity: int = 1):
    itemstr = str(item)
    if itemstr in map["store"]:
        new_quantity = map["store"][itemstr] - quantity
        if new_quantity <= 0:
            del map["store"][itemstr]
        else:
            map["store"][itemstr] = new_quantity

def bought_unit_add(save: dict, item: int):
    boughtUnits = save["privateState"]["boughtUnits"]
    if item not in boughtUnits:
        boughtUnits.append(item)

def unit_collection_complete(save: dict, collection: int):
    unitCollectionsCompleted = save["privateState"]["unitCollectionsCompleted"]
    if collection not in unitCollectionsCompleted:
        unitCollectionsCompleted.append(collection)

def set_goals(privateState: dict, goal: int, progress: list):
    goals = privateState["goals"]
    while goal >= len(goals):
        goals.append(None)
    goals[goal] = progress

def inventory_set(privateState: dict, item: int, quantity: int):
    if quantity > 0:
        privateState["inventoryItems"][str(item)] = quantity
    else:
        del privateState["inventoryItems"][itemstr]

def inventory_add(privateState: dict, item: int, quantity: int):
    itemstr = str(item)
    if itemstr not in privateState["inventoryItems"]:
        privateState["inventoryItems"][itemstr] = quantity
    else:
        privateState["inventoryItems"][itemstr] += quantity

def inventory_remove(privateState: dict, item: int, quantity: int):
    itemstr = str(item)
    if itemstr in privateState["inventoryItems"]:
        new_quantity = privateState["inventoryItems"][itemstr] - quantity
        if new_quantity <= 0:
            del privateState["inventoryItems"][itemstr]
        else:
            privateState["inventoryItems"][itemstr] = new_quantity

def add_click(item: dict):
    attr = item[6]
    if "nc" not in attr:
        attr["nc"] = 1
    else:
        attr["nc"] += 1

def activate_item_click(item: dict):
    attr = item[6]
    if "nc" in attr:
        del attr["nc"]

def buy_si_help(item: dict):
    attr = item[6]
    if "si" not in attr:
        return
    attr["si"].append(0) # 0 is for buying instead of hiring friends

def finish_si(item: dict):
    attr = item[6]
    if "si" in attr:
        del attr["si"]

def reset_stuff(save: dict):
    # This function performs some resets in save whenever the game loads the map
    # Resets market trades if it's a new day
    # 1 week = 604800 seconds
    # 1 day = 86400 seconds

    now = timestamp_now()
    for map in save["maps"]:
        last_trade = map["timestampLastTrade"]
        if now // 86400 != last_trade // 86400:
            map["numTradesDone"] = 0
    # Reset targets if start of a new week, game will call darts_reset if timestamp is 0
    privateState = save["privateState"]
    if "timeStampDartsReset" in privateState:
        # take away 3 days since timestamp 0 is thursday, we want reset to happen on monday
        # 3 days = 259200 seconds
        last_darts_reset = privateState["timeStampDartsReset"] + 259200
        temp = now + 259200
        if temp // 604800 != last_darts_reset // 604800:
            privateState["timeStampDartsReset"] = 0

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