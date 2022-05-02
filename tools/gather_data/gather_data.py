# After this, copy all files over to src/json folder.

"""
needed CSV

AttackElementCorrectParam
CalcCorrectGraph
EquipParamWeapon
MenuValueTableParam
ReinforceParamWeapon
SpEffectParam

"""

from collections import OrderedDict
import csv
import math
import pprint
from enum import Enum
import json
from tkinter import E


class Output(Enum):
    STR = "Str"
    DEX = "Dex"
    INT = "Int"
    FAI = "Fai"
    ARC = "Arc"


class Input(Enum):
    STR = "STR"
    DEX = "DEX"
    INT = "INT"
    FAI = "FTH"
    ARC = "ARC"


class InputBoolean(Enum):
    TRUE = "True"
    FALSE = "False"


Input_Affinity = {
    # MenuValueTableParam-
    0: "None",
    100: "Heavy",
    200: "Keen",
    300: "Quality",
    400: "Fire",
    500: "Flame Art",
    600: "Lightning",
    700: "Sacred",
    800: "Magic",
    900: "Cold",
    1000: "Poison",
    1100: "Blood",
    1200: "Occult",
}

Weapon_Type = {
    # MenuValueTableParam- Value: Row Name
    1: "Dagger",
    3: "Straight Sword",
    5: "Greatsword",
    7: "Colossal Sword",
    9: "Curved Sword",
    11: "Curved Greatsword",
    13: "Katana",
    14: "Twinblade",
    15: "Thrusting Sword",
    16: "Heavy Thrusting Sword",
    17: "Axe",
    19: "Greataxe",
    21: "Hammer",
    23: "Warhammer",
    24: "Flail",
    25: "Spear",
    28: "Great Spear",
    29: "Halberd",
    31: "Reaper",
    35: "Fist",
    37: "Claw",
    39: "Whip",
    41: "Colossal Weapon",
    50: "Light Bow",
    51: "Bow",
    53: "Greatbow",
    55: "Crossbow",
    56: "Ballista",
    57: "Glintstone Staff",
    61: "Sacred Seal",
    65: "Small Shield",
    67: "Medium Shield",
    69: "Greatshield",
    87: "Torch"
}

Armor_Type = {
    # MenuValueTableParam- Value: Row Name
    0: "Head",
    1: "Body",
    2: "Arm",
    3: "Leg"
}

def getArmorType(value):
    armortype = int(value)
    return Armor_Type[armortype]


def getWeaponType(value):
    weapontype = int(value)
    return Weapon_Type[weapontype]


def getAffinity(value):
    affinity = int(value) % 10000
    return Input_Affinity[affinity]


def getMaxUpgrade(row):
    max_upgrade = -1  # error case

    if int(row['Origin Weapon +25']) == -1:
        if int(row['Origin Weapon +10']) == -1:
            max_upgrade = 0
        else:
            max_upgrade = 10
    else:
        max_upgrade = 25

    return max_upgrade

max_num_cap =  4         # max number of level caps in correction file

base_weapon = 1000000  # dagger
max_weapon = 44010000  # jar cannon

base_phys = 0          # default
max_phys = 16          # Catalyst

base_stats = 100          # default
item_discovery_stat = 140 # item_discovery
max_stats = 220           # equipload

def writeToFile(filename, input):
    with open('output/' + filename + '.json', "w") as output_file:
        json.dump(input, output_file, indent=4)


##############################################
# AttackElementCorrectParam.json
##############################################
attack_element_types = [
    "physicalScalingStr",
    "physicalScalingDex",
    "physicalScalingInt",
    "physicalScalingFai",
    "physicalScalingArc",
    "magicScalingStr",
    "magicScalingDex",
    "magicScalingInt",
    "magicScalingFai",
    "magicScalingArc",
    "fireScalingStr",
    "fireScalingDex",
    "fireScalingInt",
    "fireScalingFai",
    "fireScalingArc",
    "lightningScalingStr",
    "lightningScalingDex",
    "lightningScalingInt",
    "lightningScalingFai",
    "lightningScalingArc",
    "holyScalingStr",
    "holyScalingDex",
    "holyScalingInt",
    "holyScalingFai",
    "holyScalingArc",
]

# Grab data


def getAttackElementCorrectParam():
    attack_element_correct_param_data = []
    with open("AttackElementCorrectParam.csv") as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = next(reader)[1:]
        for row in reader:
            if 10000 <= int(row[0]) <= 30040:

                row_dict = OrderedDict()
                row_dict["rowId"] = int(row[0])

                for i in range(0, len(attack_element_types)):
                    row_dict[attack_element_types[i]] = int(
                        row[i+2] == InputBoolean.TRUE.value)

                attack_element_correct_param_data.append(row_dict)

    return attack_element_correct_param_data


##############################################
# General Load Data
##############################################

with open("EquipParamWeapon.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    EquipParamWeapon = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("ReinforceParamWeapon.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    ReinforceParamWeapon = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("EquipParamAccessory.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    EquipParamAccessory = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("EquipParamProtector.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    EquipParamProtector = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("SpEffectParam.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    SpEffectParam = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("SpEffectVfxParam.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    SpEffectVfxParam = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

##############################################
# weapon_reqs.json
##############################################

def getWeaponReqs():
    weapon_reqs_data = []
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):

                row_dict = OrderedDict()
                row_dict["fullweaponname"] = row['Row Name']
                row_dict["weaponname"] = EquipParamWeapon[row['Origin Weapon +0']]['Row Name']

                row_dict["affinity"] = getAffinity(key)

                row_dict["maxUpgrade"] = getMaxUpgrade(row)

                row_dict["strreq"] = int(
                    row['Requirement: ' + Input.STR.value])
                row_dict["dexreq"] = int(
                    row['Requirement: ' + Input.DEX.value])
                row_dict["intreq"] = int(
                    row['Requirement: ' + Input.INT.value])
                row_dict["faireq"] = int(
                    row['Requirement: ' + Input.FAI.value])
                row_dict["arcreq"] = int(
                    row['Requirement: ' + Input.ARC.value])

                if row["Type Display: Normal"] == "True":
                    if row["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Standard/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Standard"
                elif row["Type Display: Strike"] == "True":
                    if row["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Strike/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Strike"
                elif row["Type Display: Slash"] == "True":
                    if row["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Slash/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Slash"
                elif row["Type Display: Thrust"] == "True":
                    row_dict["physicalDamageType"] = "Pierce"
                else:
                    row_dict["physicalDamageType"] = 0

                weight = float(row["Weight"])
                row_dict["weight"] = int(
                    weight) if weight.is_integer() else weight
                poise_damage = float(row["Poise Damage"])
                row_dict["basePoiseAttack"] = int(
                    poise_damage) if poise_damage.is_integer() else poise_damage
                row_dict["critical"] = 100 + int(row["Critical Multiplier"])
                row_dict["weaponType"] = getWeaponType(row["Weapon Type"])

                weapon_reqs_data.append(row_dict)

    return weapon_reqs_data


##############################################
# weapon_damage.json
##############################################

def getWeaponDamage():
    weapon_damage_data = []

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                # shields might be edge case for matching, as well as cross bow and bows?

                upgrade_level_max = getMaxUpgrade(row)
                for upgrade_level in range(0, upgrade_level_max+1):
                    # (EquipParamWeapon) Damage: Physical * (ReinforceParamWeapon) Damage % Physical --------- NEED UPGRADE LEVEL
                    dmg_phys = float(row['Damage: Physical'])
                    dmg_phys_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Physical'])
                    phys_name = "phys" + str(upgrade_level)
                    row_dict[phys_name] = dmg_phys * dmg_phys_perc
                    if row_dict[phys_name].is_integer():
                        row_dict[phys_name] = int(row_dict[phys_name])

                    dmg_mag = float(row['Damage: Magic'])
                    dmg_mag_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Magic'])
                    mag_name = "mag" + str(upgrade_level)
                    row_dict[mag_name] = dmg_mag * dmg_mag_perc
                    if row_dict[mag_name].is_integer():
                        row_dict[mag_name] = int(row_dict[mag_name])

                    dmg_fire = float(row['Damage: Fire'])
                    dmg_fire_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Fire'])
                    fire_name = "fire" + str(upgrade_level)
                    row_dict[fire_name] = dmg_fire * dmg_fire_perc
                    if row_dict[fire_name].is_integer():
                        row_dict[fire_name] = int(row_dict[fire_name])

                    dmg_ligh = float(row['Damage: Lightning'])
                    dmg_ligh_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Lightning'])
                    ligh_name = "ligh" + str(upgrade_level)
                    row_dict[ligh_name] = dmg_ligh * dmg_ligh_perc
                    if row_dict[ligh_name].is_integer():
                        row_dict[ligh_name] = int(row_dict[ligh_name])

                    dmg_holy = float(row['Damage: Holy'])
                    dmg_holy_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Holy'])
                    holy_name = "holy" + str(upgrade_level)
                    row_dict[holy_name] = dmg_holy * dmg_holy_perc
                    if row_dict[holy_name].is_integer():
                        row_dict[holy_name] = int(row_dict[holy_name])

                    dmg_stam = float(row['Damage: Stamina'])
                    dmg_stam_perc = float(ReinforceParamWeapon[str(
                        int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Stamina'])
                    stam_name = "stam" + str(upgrade_level)
                    row_dict[stam_name] = dmg_stam * dmg_stam_perc
                    if row_dict[stam_name].is_integer():
                        row_dict[stam_name] = int(row_dict[stam_name])

                # probably delete later, unneeded but used to match current data
                if upgrade_level_max != 25:
                    for upgrade_level in range(upgrade_level_max+1, 26):
                        row_dict["phys" + str(upgrade_level)] = 0
                        row_dict["mag" + str(upgrade_level)] = 0
                        row_dict["fire" + str(upgrade_level)] = 0
                        row_dict["ligh" + str(upgrade_level)] = 0
                        row_dict["holy" + str(upgrade_level)] = 0
                        row_dict["stam" + str(upgrade_level)] = 0

                weapon_damage_data.append(row_dict)

    return weapon_damage_data


##############################################
# weapon_scaling.json
# Not exact, but very very very close
##############################################

def getWeaponScaling():
    weapon_scaling_data = []

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                # shields might be edge case for matching, as well as cross bow and bows?

                upgrade_level_max = getMaxUpgrade(row)
                for upgrade_level in range(0, upgrade_level_max+1):
                    # (EquipParamWeapon) Correction: STR * (ReinforceParamWeapon) Correction % STR / 100 --------- NEED UPGRADE LEVEL
                    crt_str = float(row['Correction: ' + Input.STR.value])
                    crt_str_perc = float(ReinforceParamWeapon[str(int(
                        row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.STR.value])
                    str_name = "str" + str(upgrade_level)
                    row_dict[str_name] = crt_str * crt_str_perc / 100
                    if row_dict[str_name].is_integer():
                        row_dict[str_name] = int(row_dict[str_name])

                    crt_dex = float(row['Correction: ' + Input.DEX.value])
                    crt_dex_perc = float(ReinforceParamWeapon[str(int(
                        row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.DEX.value])
                    dex_name = "dex" + str(upgrade_level)
                    row_dict[dex_name] = crt_dex * crt_dex_perc / 100
                    if row_dict[dex_name].is_integer():
                        row_dict[dex_name] = int(row_dict[dex_name])

                    crt_int = float(row['Correction: ' + Input.INT.value])
                    crt_int_perc = float(ReinforceParamWeapon[str(int(
                        row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.INT.value])
                    int_name = "int" + str(upgrade_level)
                    row_dict[int_name] = crt_int * crt_int_perc / 100
                    if row_dict[int_name].is_integer():
                        row_dict[int_name] = int(row_dict[int_name])

                    crt_fai = float(row['Correction: ' + Input.FAI.value])
                    crt_fai_perc = float(ReinforceParamWeapon[str(int(
                        row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.FAI.value])
                    fai_name = "fai" + str(upgrade_level)
                    row_dict[fai_name] = crt_fai * crt_fai_perc / 100
                    if row_dict[fai_name].is_integer():
                        row_dict[fai_name] = int(row_dict[fai_name])

                    crt_arc = float(row['Correction: ' + Input.ARC.value])
                    crt_arc_perc = float(ReinforceParamWeapon[str(int(
                        row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.ARC.value])
                    arc_name = "arc" + str(upgrade_level)
                    row_dict[arc_name] = crt_arc * crt_arc_perc / 100
                    if row_dict[arc_name].is_integer():
                        row_dict[arc_name] = int(row_dict[arc_name])

                # probably delete later, unneeded but used to match current data
                if upgrade_level_max != 25:
                    for upgrade_level in range(upgrade_level_max+1, 26):
                        row_dict["str" + str(upgrade_level)] = 0
                        row_dict["dex" + str(upgrade_level)] = 0
                        row_dict["int" + str(upgrade_level)] = 0
                        row_dict["fai" + str(upgrade_level)] = 0
                        row_dict["arc" + str(upgrade_level)] = 0

                weapon_scaling_data.append(row_dict)

    return weapon_scaling_data


##############################################
# weapon_passive.json
# need read, doesn't use direct ID's to calculate scaling
# need write
##############################################

BehaviorTypes = {
    'Scarlet Rot': 'Scarlet Rot',
    'Madness': 'Madness',
    'Sleep': 'Sleep',
    'Frostbite': 'Frost',
    'Poison': 'Poison',
    'Hemorrhage': 'Blood',
    'Rune Gain on Hit' : 'Rune Gain on Hit',
    'Rune Gain on Kill' : 'Rune Gain on Kill',
    'Restore HP on Hit' : 'Restore HP on Hit',
    'Restore HP on Kill' : 'Restore HP on Kill',
    'Restore FP on Hit' : 'Restore FP on Hit',
    'Restore FP on Kill' : 'Restore FP on Kill'
}

SortOrder = {
    'Scarlet Rot': 0,
    'Madness': 1,
    'Sleep': 2,
    'Frost': 3,
    'Poison': 4,
    'Blood': 5,
    'Rune Gain on Hit' : 6,
    'Rune Gain on Kill' : 7,
    'Restore HP on Hit' : 8,
    'Restore HP on Kill' : 9,
    'Restore FP on Hit' : 10,
    'Restore FP on Kill' : 11
}


def getWeaponPassive():
    weapon_passive_data = []

    # ReinforceParamWeapon['Behavior SpEffect 1 Offset'] used for something?
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                behavior1 = row["Behavior SpEffect 1"]
                behavior2 = row["Behavior SpEffect 2"]
                behavior3 = row["Behavior SpEffect 3"]

                types = []
                rows = []
                row_nums = []

                # need if statements for type of behavior, for example poison is "Inflict Poison +"
                # -1 means not used
                if behavior1 != '-1':
                    if behavior1 in SpEffectParam:  # needed because regulation.bin has a bug with certain weapons
                        row1 = SpEffectParam[behavior1]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in BehaviorTypes.items():
                            if type in row1['Row Name']:
                                rows.append(row1)
                                row_nums.append(behavior1)
                                types.append(value)
                                break

                if behavior2 != '-1':
                    if behavior2 in SpEffectParam:
                        row2 = SpEffectParam[behavior2]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in BehaviorTypes.items():
                            if type in row2['Row Name']:
                                rows.append(row2)
                                row_nums.append(behavior2)
                                types.append(value)
                                break

                if behavior3 != '-1':
                    if behavior3 in SpEffectParam:
                        row3 = SpEffectParam[behavior3]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in BehaviorTypes.items():  # this is filtering out the other types of behavior which is a bun
                            if type in row3['Row Name']:
                                rows.append(row3)
                                row_nums.append(behavior3)
                                types.append(value)
                                break

                # behavior type 1 and 2 are sorted in SortOrder
                if len(types) > 0:
                    zipped_lists = list(zip(types, rows, row_nums))
                    sorted_lists = sorted(
                        zipped_lists, key=lambda value: SortOrder[value[0]])
                    tuples = zip(*sorted_lists)
                    types, rows, row_nums = [list(tuple) for tuple in tuples]

                # INIT VALUES
                for idx, type in enumerate(types):
                    row_dict["type" + str(idx+1)] = ''
                row_dict["scarletRot0"] = 0
                row_dict["madness0"] = 0
                row_dict["sleep0"] = 0
                for upgrade_level in range(0, 26):
                    row_dict["frost" + str(upgrade_level)] = 0
                    row_dict["poison" + str(upgrade_level)] = 0
                    row_dict["blood" + str(upgrade_level)] = 0
                

                # UPDATE VALUES VALUES
                for idx, type in enumerate(types):
                    row_dict["type" + str(idx+1)] = type
                    row_id = int(row_nums[idx])

                    # currently filtering out types by using own data and row name - row name isn't a var and can be changed, is there a real link in yapped?\
                    # Link is EquipParamWeapon.Reinforce Type ID to ReinforceParamWeapon.RowNum.
                    # SpEffectParam (1/2/3) increase in damage is offset from ReinforceParamWeapon.Behavior SpEffect 1/2/3 Offset
                    # EquipParamWeapon.Behavior SpEffect 1/2/3
                    if type == "Scarlet Rot":
                        row_dict["scarletRot0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Scarlet Rot +"]) if not (
                            6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Scarlet Rot +"])
                    elif type == "Madness":
                        row_dict["madness0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Madness +"]) if not (
                            6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Madness +"])
                    elif type == "Sleep":
                        row_dict["sleep0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Sleep +"]) if not (
                            6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Sleep +"])
                    elif type == "Frost" or type == "Poison" or type == "Blood":
                        upgrade_level_max = getMaxUpgrade(row)
                        for upgrade_level in range(0, upgrade_level_max+1):
                            # special behaviors, don't increase with level
                            if not (6400 <= row_id <= 6805) and row_dict['name'] != 'Cold Antspur Rapier':
                                if type == "Frost":
                                    row_dict["frost" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id+upgrade_level)]["Inflict Frostbite +"])

                                elif type == "Poison":
                                    row_dict["poison" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id+upgrade_level)]["Inflict Poison +"])

                                elif type == "Blood":
                                    row_dict["blood" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id+upgrade_level)]["Inflict Hemorrhage +"])
                            else:
                                if type == "Frost":
                                    row_dict["frost" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id)]["Inflict Frostbite +"])

                                elif type == "Poison":
                                    row_dict["poison" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id)]["Inflict Poison +"])

                                elif type == "Blood":
                                    row_dict["blood" + str(upgrade_level)] = int(
                                        SpEffectParam[str(row_id)]["Inflict Hemorrhage +"])
                    elif type == "Rune Gain on Hit" or type == "Rune Gain on Kill":
                        if type == "Rune Gain on Hit":
                            row_dict["rune_gain_hit"] = int(
                                SpEffectParam[str(row_id)]["Rune Gain +"])
                        else:
                            row_dict["rune_gain_kill"] = int(
                                SpEffectParam[str(row_id+1)]["Rune Gain +"])
                    elif type == "Restore HP on Hit" or type == "Restore HP on Kill":
                        if type == "Restore HP on Hit":
                            if float(SpEffectParam[str(row_id)]["Change HP %"]) != 0:
                                row_dict["restore_hp_hit_percentage"] = -float(
                                    SpEffectParam[str(row_id)]["Change HP %"])
                            if int(SpEffectParam[str(row_id)]["Change HP +"]) != 0:
                                row_dict["restore_hp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change HP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change HP %"]) != 0:
                                row_dict["restore_hp_kill_percentage"] = -float(
                                    SpEffectParam[str(row_id+1)]["Change HP %"])
                            if int(SpEffectParam[str(row_id+1)]["Change HP +"]) != 0:
                                row_dict["restore_hp_kill"] = -int(
                                    SpEffectParam[str(row_id+1)]["Change HP +"])
                    elif type == "Restore FP on Hit" or type == "Restore FP on Kill":
                        if type == "Restore FP on Hit":
                            if float(SpEffectParam[str(row_id)]["Change FP %"]) != 0:
                                row_dict["restore_fp_hit_percentage"] = -float(
                                    SpEffectParam[str(row_id)]["Change FP %"])
                            if int(SpEffectParam[str(row_id)]["Change FP +"]) != 0:
                                row_dict["restore_fp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change FP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change FP %"]) != 0:
                                row_dict["restore_fp_kill_percentage"] = -float(
                                    SpEffectParam[str(row_id+1)]["Change FP %"])
                            if int(SpEffectParam[str(row_id+1)]["Change FP +"]) != 0:
                                row_dict["restore_fp_kill"] = -int(
                                    SpEffectParam[str(row_id+1)]["Change FP +"])
                    else:
                        row_dict["unknown_type"] = "unknown"

                passive1 = row["Passive SpEffect 1"]
                passive2 = row["Passive SpEffect 2"]
                passive3 = row["Passive SpEffect 3"]

                # -1 means not used
                if passive1 != '-1':
                    if passive1 in SpEffectParam:  # needed because regulation.bin has a bug with certain weapons
                        row_dict["passive_1"] = getPassiveEffect(SpEffectParam[passive1], passive1, False)

                if passive2 != '-1':
                    if passive2 in SpEffectParam:
                        row_dict["passive_2"] = getPassiveEffect(SpEffectParam[passive2], passive2, False)

                if passive3 != '-1':
                    if passive3 in SpEffectParam:
                        row_dict["passive_3"] = getPassiveEffect(SpEffectParam[passive3], passive3, False)

                # # probably delete later, unneeded but used to match current data
                # if upgrade_level_max != 25:
                #     for upgrade_level in range(upgrade_level_max+1, 26):
                #         row_dict["frost" + str(upgrade_level)] = 0
                #         row_dict["poison" + str(upgrade_level)] = 0
                #         row_dict["blood" + str(upgrade_level)] = 0

                weapon_passive_data.append(row_dict)

    return weapon_passive_data


##############################################
# calc_correct_id.json
##############################################

def getCalcCorrectId():
    calc_correct_id = []
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):

                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                row_dict["physical"] = int(row['Correction Type: Physical'])
                row_dict["magic"] = int(row['Correction Type: Magic'])
                row_dict["fire"] = int(row['Correction Type: Fire'])
                row_dict["lightning"] = int(row['Correction Type: Lightning'])
                row_dict["holy"] = int(row['Correction Type: Holy'])

                row_dict["attackelementcorrectId"] = int(
                    row['Attack Element Correct ID'])

                calc_correct_id.append(row_dict)

    return calc_correct_id


##############################################
# weapon_groups.json
##############################################

def getWeaponGroups():
    weapon_groups = []
    weaponTypes = set()
    weapons = OrderedDict()
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            # REFORMAT DATA SO IT IS
            """
            [
                {
                    label: 'weapontype',
                    options: [
                        {
                            label: 'weaponname',
                            value: 'weaponname',
                        },
                        {
                            label: 'weaponname',
                            value: 'weaponname',
                        },
                    ]
                }
            ]
            """
            weaponTypes.add(getWeaponType(row["Weapon Type"]))
            weapons[EquipParamWeapon[row['Origin Weapon +0']]['Row Name']] = getWeaponType(row["Weapon Type"])
    
    i = 1
    for key, val in weapons.items():
        isGroup = -1
        if len(weapon_groups) != 0:
            for idx, groups in enumerate(weapon_groups):
                if val == groups['label']:
                    isGroup = idx

        if isGroup == -1:
            group = OrderedDict()
            group['label'] = val
            group['options'] = []
            group['options'].append({'label': key, 'value': str(i)})
            i+=1
            weapon_groups.append(group)
        else:
            weapon_groups[isGroup]['options'].append(OrderedDict({'label': key, 'value': i}))
            i+=1

    return weapon_groups


######################################################################
# arm_group.json, leg_group.json, body_group.json, head_group.json
######################################################################

def getArmorGroups():
    head = OrderedDict()
    head['label'] = "Head"
    head['options'] = []
    body = OrderedDict()
    body['label'] = "Body"
    body['options'] = []
    arm = OrderedDict()
    arm['label'] = "Arm"
    arm['options'] = []
    leg = OrderedDict()
    leg['label'] = "Leg"
    leg['options'] = []
    i = 1
    for key, row in EquipParamProtector.items():
        if row['Can Drop'] == InputBoolean.TRUE.value:
            if getArmorType(row['Armor Category']) == head['label']:
                head["options"].append({'label': row['Row Name'], 'value': i})
                i+=1
            elif getArmorType(row['Armor Category']) == body['label']:
                body["options"].append({'label': row['Row Name'], 'value': i})
                i+=1
            elif getArmorType(row['Armor Category']) == arm['label']:
                arm["options"].append({'label': row['Row Name'], 'value': i})
                i+=1
            elif getArmorType(row['Armor Category']) == leg['label']:
                leg["options"].append({'label': row['Row Name'], 'value': i})
                i+=1

    return head, body, arm, leg


##############################################
# physical_calculations.json
##############################################

def getPhysCalc():
    with open("CalcCorrectGraph.csv") as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = next(reader)[1:]
        CalcCorrectGraph = OrderedDict(
            (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)
            
    phys_calc_data = []
    for key, row in CalcCorrectGraph.items():
        if (int(key) >= base_phys and int(key) <= max_phys) or (int(key) >= base_stats and int(key) <= max_stats):
            row_dict = OrderedDict()
            row_dict["row_id"] = int(key)
            row_dict["name"] = row['Row Name']
            for scaling_cap in range (0, max_num_cap+1):
                row_dict["stat_max_"+str(scaling_cap)] = int(row['Stat Max '+str(scaling_cap)])
                if (int(key) == item_discovery_stat):
                    row_dict["grow_"+str(scaling_cap)] = float(row['Grow '+str(scaling_cap)])
                else:
                    row_dict["grow_"+str(scaling_cap)] = int(row['Grow '+str(scaling_cap)])
                row_dict["adj_point_"+str(scaling_cap)] = float(row['Adjustment Point - Grow '+str(scaling_cap)])

            phys_calc_data.append(row_dict)
    
    return phys_calc_data


##############################################
# armor_data.json
##############################################

def getArmorData():
    armor_data = []
    for key, row in EquipParamProtector.items():
        if row['Can Drop'] == InputBoolean.TRUE.value:
            row_dict = OrderedDict()
            extractArmor(row_dict, row, key)
            armor_data.append(row_dict)
    
    return armor_data


######################################################################
# max_arm.json, max_leg.json, max_body.json, max_head.json
######################################################################

def getMaxArmorData():
    max_head = OrderedDict()
    max_head['label'] = "Head"
    max_head['max_physical_absorption'] = 0.0
    max_head["max_strike_absorption"] = 0.0
    max_head["max_slash_absorption"] = 0.0
    max_head["max_thrust_absorption"] = 0.0
    max_head["max_magic_absorption"] = 0.0
    max_head["max_fire_absorption"] = 0.0
    max_head["max_lightning_absorption"] = 0.0
    max_head["max_holy_absorption"] = 0.0
    max_head["max_poison_resist"] = 0
    max_head["max_rot_resist"] = 0
    max_head["max_bleed_resist"] = 0
    max_head["max_frost_resist"] = 0
    max_head["max_madness_resist"] = 0
    max_head["max_sleep_resist"] = 0
    max_head["max_poise"] = 0
    max_head["max_vitality"] = 0
    max_body = OrderedDict()
    max_body['label'] = "Body"
    max_body['max_physical_absorption'] = 0.0
    max_body["max_strike_absorption"] = 0.0
    max_body["max_slash_absorption"] = 0.0
    max_body["max_thrust_absorption"] = 0.0
    max_body["max_magic_absorption"] = 0.0
    max_body["max_fire_absorption"] = 0.0
    max_body["max_lightning_absorption"] = 0.0
    max_body["max_holy_absorption"] = 0.0
    max_body["max_poison_resist"] = 0
    max_body["max_rot_resist"] = 0
    max_body["max_bleed_resist"] = 0
    max_body["max_frost_resist"] = 0
    max_body["max_madness_resist"] = 0
    max_body["max_sleep_resist"] = 0
    max_body["max_poise"] = 0
    max_body["max_vitality"] = 0
    max_arm = OrderedDict()
    max_arm['label'] = "Arm"
    max_arm['max_physical_absorption'] = 0.0
    max_arm["max_strike_absorption"] = 0.0
    max_arm["max_slash_absorption"] = 0.0
    max_arm["max_thrust_absorption"] = 0.0
    max_arm["max_magic_absorption"] = 0.0
    max_arm["max_fire_absorption"] = 0.0
    max_arm["max_lightning_absorption"] = 0.0
    max_arm["max_holy_absorption"] = 0.0
    max_arm["max_poison_resist"] = 0
    max_arm["max_rot_resist"] = 0
    max_arm["max_bleed_resist"] = 0
    max_arm["max_frost_resist"] = 0
    max_arm["max_madness_resist"] = 0
    max_arm["max_sleep_resist"] = 0
    max_arm["max_poise"] = 0
    max_arm["max_vitality"] = 0
    max_leg = OrderedDict()
    max_leg['label'] = "Leg"
    max_leg['max_physical_absorption'] = 0.0
    max_leg["max_strike_absorption"] = 0.0
    max_leg["max_slash_absorption"] = 0.0
    max_leg["max_thrust_absorption"] = 0.0
    max_leg["max_magic_absorption"] = 0.0
    max_leg["max_fire_absorption"] = 0.0
    max_leg["max_lightning_absorption"] = 0.0
    max_leg["max_holy_absorption"] = 0.0
    max_leg["max_poison_resist"] = 0
    max_leg["max_rot_resist"] = 0
    max_leg["max_bleed_resist"] = 0
    max_leg["max_frost_resist"] = 0
    max_leg["max_madness_resist"] = 0
    max_leg["max_sleep_resist"] = 0
    max_leg["max_poise"] = 0
    max_leg["max_vitality"] = 0
    for key, row in EquipParamProtector.items():
        if row['Can Drop'] == InputBoolean.TRUE.value:
            row_dict = OrderedDict()
            extractArmor(row_dict, row, key)
            if getArmorType(row['Armor Category']) == max_head['label']:
                compareMaxArmor(row_dict, max_head)
            elif getArmorType(row['Armor Category']) == max_body['label']:
                compareMaxArmor(row_dict, max_body)
            elif getArmorType(row['Armor Category']) == max_arm['label']:
                compareMaxArmor(row_dict, max_arm)
            elif getArmorType(row['Armor Category']) == max_leg['label']:
                compareMaxArmor(row_dict, max_leg)

    if (max_head["max_poison_resist"] == max_head["max_rot_resist"]):
        max_head.pop("max_poison_resist")
        max_head["max_immunity"] = max_head.pop("max_rot_resist")
    if (max_head["max_bleed_resist"] == max_head["max_frost_resist"]):
        max_head.pop("max_bleed_resist")
        max_head["max_robustness"] = max_head.pop("max_frost_resist")
    if (max_head["max_madness_resist"] == max_head["max_sleep_resist"]):
        max_head.pop("max_madness_resist")
        max_head["max_focus"] = max_head.pop("max_sleep_resist")

    if (max_body["max_poison_resist"] == max_body["max_rot_resist"]):
        max_body.pop("max_poison_resist")
        max_body["max_immunity"] = max_body.pop("max_rot_resist")
    if (max_body["max_bleed_resist"] == max_body["max_frost_resist"]):
        max_body.pop("max_bleed_resist")
        max_body["max_robustness"] = max_body.pop("max_frost_resist")
    if (max_body["max_madness_resist"] == max_body["max_sleep_resist"]):
        max_body.pop("max_madness_resist")
        max_body["max_focus"] = max_body.pop("max_sleep_resist")

    if (max_arm["max_poison_resist"] == max_arm["max_rot_resist"]):
        max_arm.pop("max_poison_resist")
        max_arm["max_immunity"] = max_arm.pop("max_rot_resist")
    if (max_arm["max_bleed_resist"] == max_arm["max_frost_resist"]):
        max_arm.pop("max_bleed_resist")
        max_arm["max_robustness"] = max_arm.pop("max_frost_resist")
    if (max_arm["max_madness_resist"] == max_arm["max_sleep_resist"]):
        max_arm.pop("max_madness_resist")
        max_arm["max_focus"] = max_arm.pop("max_sleep_resist")

    if (max_leg["max_poison_resist"] == max_leg["max_rot_resist"]):
        max_leg.pop("max_poison_resist")
        max_leg["max_immunity"] = max_leg.pop("max_rot_resist")
    if (max_leg["max_bleed_resist"] == max_leg["max_frost_resist"]):
        max_leg.pop("max_bleed_resist")
        max_leg["max_robustness"] = max_leg.pop("max_frost_resist")
    if (max_leg["max_madness_resist"] == max_leg["max_sleep_resist"]):
        max_leg.pop("max_madness_resist")
        max_leg["max_focus"] = max_leg.pop("max_sleep_resist")

    return max_head, max_body, max_arm, max_leg

def extractArmor(row_dict, row, key):
    row_dict["row_id"] = int(key)
    row_dict["name"] = row['Row Name']
    row_dict["equipment_type"] = getArmorType(row['Armor Category'])
    row_dict["weight"] = float(row['Weight'])
    row_dict["physical_absorption"] = 1 - float(row['Absorption - Physical'])
    row_dict["strike_absorption"] = 1 - float(row['Absorption - Strike'])
    row_dict["slash_absorption"] = 1 - float(row['Absorption - Slash'])
    row_dict["thrust_absorption"] = 1 - float(row['Absorption - Thrust'])
    row_dict["magic_absorption"] = 1 - float(row['Absorption - Magic'])
    row_dict["fire_absorption"] = 1 - float(row['Absorption - Fire'])
    row_dict["lightning_absorption"] = 1 - float(row['Absorption - Lightning'])
    row_dict["holy_absorption"] = 1 - float(row['Absorption - Holy'])
    if (int(row['Resist - Poison']) == int(row['Resist - Scarlet Rot'])):
        row_dict["immunity"] = int(row['Resist - Poison'])
    else:
        row_dict["poison_resist"] = int(row['Resist - Poison'])
        row_dict["rot_resist"] = int(row['Resist - Scarlet Rot'])
    if (int(row['Resist - Hemorrhage']) == int(row['Resist - Frost'])):
        row_dict["robustness"] = int(row['Resist - Hemorrhage'])
    else:
        row_dict["robustness"] = int(row['Resist - Hemorrhage'])
        row_dict["frost_resist"] = int(row['Resist - Frost'])
    if (int(row['Resist - Madness']) == int(row['Resist - Sleep'])):
        row_dict["focus"] = int(row['Resist - Madness'])
    else:
        row_dict["focus"] = int(row['Resist - Madness'])
        row_dict["sleep_resist"] = int(row['Resist - Sleep'])
    row_dict["vitality"] = int(row['Resist - Blight'])
    row_dict["poise"] = int(float(row['Poise']) * 1000.0)
    
    # if death bed dress
    if (int(key) == 1930100):
        if int(row['Resident SpEffect ID [1]']) != -1:
            row_dict["passive_1"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [1]']) + 2)], str(int(row['Resident SpEffect ID [1]']) + 2), True)
            calcAbsorptions(row_dict, row_dict["passive_1"])
        if int(row['Resident SpEffect ID [2]']) != -1:
            row_dict["passive_2"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [2]']) + 2)], str(int(row['Resident SpEffect ID [2]']) + 2), True)
            calcAbsorptions(row_dict, row_dict["passive_2"])
        if int(row['Resident SpEffect ID [3]']) != -1:
            row_dict["passive_3"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [3]']) + 2)], str(int(row['Resident SpEffect ID [3]']) + 2), True)
            calcAbsorptions(row_dict, row_dict["passive_3"])
    else:
        # if not Gravekeeper Cloak.
        # Gravekeeper Cloak has a passive attached to it but is not used in game currently
        if (int(key) != 310100):
            if int(row['Resident SpEffect ID [1]']) != -1:
                row_dict["passive_1"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [1]']], row['Resident SpEffect ID [1]'], True)
                calcAbsorptions(row_dict, row_dict["passive_1"])
            if int(row['Resident SpEffect ID [2]']) != -1:
                row_dict["passive_2"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [2]']], row['Resident SpEffect ID [2]'], True)
                calcAbsorptions(row_dict, row_dict["passive_2"])
            if int(row['Resident SpEffect ID [3]']) != -1:
                row_dict["passive_3"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [3]']], row['Resident SpEffect ID [3]'], True)
                calcAbsorptions(row_dict, row_dict["passive_3"])

def compareMaxArmor(row_dict, max_armor):
    if (max_armor['max_physical_absorption'] < row_dict["physical_absorption"]):
        max_armor['max_physical_absorption'] = row_dict["physical_absorption"]
    if (max_armor['max_strike_absorption'] < row_dict["strike_absorption"]):
        max_armor['max_strike_absorption'] = row_dict["strike_absorption"]
    if (max_armor['max_slash_absorption'] < row_dict["slash_absorption"]):
        max_armor['max_slash_absorption'] = row_dict["slash_absorption"]
    if (max_armor['max_thrust_absorption'] < row_dict["thrust_absorption"]):
        max_armor['max_thrust_absorption'] = row_dict["thrust_absorption"]
    if (max_armor['max_magic_absorption'] < row_dict["magic_absorption"]):
        max_armor['max_magic_absorption'] = row_dict["magic_absorption"]
    if (max_armor['max_fire_absorption'] < row_dict["fire_absorption"]):
        max_armor['max_fire_absorption'] = row_dict["fire_absorption"]
    if (max_armor['max_lightning_absorption'] < row_dict["lightning_absorption"]):
        max_armor['max_lightning_absorption'] = row_dict["lightning_absorption"]
    if (max_armor['max_holy_absorption'] < row_dict["holy_absorption"]):
        max_armor['max_holy_absorption'] = row_dict["holy_absorption"]

    if "immunity" in row_dict:
        if (max_armor['max_poison_resist'] < row_dict["immunity"]):
            max_armor["max_poison_resist"] = row_dict["immunity"]
            max_armor["max_rot_resist"] = row_dict["immunity"]
    else:
        if (max_armor['max_poison_resist'] < row_dict["poison_resist"]):
            max_armor["max_poison_resist"] = row_dict["poison_resist"]
        if (max_armor['max_rot_resist'] < row_dict["rot_resist"]):
            max_armor["max_rot_resist"] = row_dict["rot_resist"]
    
    if "robustness" in row_dict:
        if (max_armor['max_bleed_resist'] < row_dict["robustness"]):
            max_armor["max_bleed_resist"] = row_dict["robustness"]
            max_armor["max_frost_resist"] = row_dict["robustness"]
    else:
        if (max_armor['max_bleed_resist'] < row_dict["bleed_resist"]):
            max_armor["max_bleed_resist"] = row_dict["bleed_resist"]
        if (max_armor['max_frost_resist'] < row_dict["frost_resist"]):
            max_armor["max_frost_resist"] = row_dict["frost_resist"]

    if "focus" in row_dict:
        if (max_armor['max_madness_resist'] < row_dict["focus"]):
            max_armor["max_madness_resist"] = row_dict["focus"]
            max_armor["max_sleep_resist"] = row_dict["focus"]
    else:
        if (max_armor['max_madness_resist'] < row_dict["madness_resist"]):
            max_armor["max_madness_resist"] = row_dict["madness_resist"]
        if (max_armor['max_sleep_resist'] < row_dict["sleep_resist"]):
            max_armor["max_sleep_resist"] = row_dict["sleep_resist"]
    
    if (max_armor["max_poise"] < row_dict["poise"]):
        max_armor["max_poise"] = row_dict["poise"]

    if (max_armor["max_vitality"] < row_dict["vitality"]):
        max_armor["max_vitality"] = row_dict["vitality"]


def calcAbsorptions(row_dict, passive):
    if "absorption_standard" in passive:
        row_dict["physical_absorption"] = calcAbsorption(row_dict["physical_absorption"], passive.pop("absorption_standard"))
    if "absorption_strike" in passive:
        row_dict["strike_absorption"] = calcAbsorption(row_dict["strike_absorption"], passive.pop("absorption_strike"))
    if "absorption_slash" in passive:
        row_dict["slash_absorption"] = calcAbsorption(row_dict["slash_absorption"], passive.pop("absorption_slash"))
    if "absorption_thrust" in passive:
        row_dict["thrust_absorption"] = calcAbsorption(row_dict["thrust_absorption"], passive.pop("absorption_thrust"))
    if "absorption_magic" in passive:
        row_dict["magic_absorption"] = calcAbsorption(row_dict["magic_absorption"], passive.pop("absorption_magic"))
    if "absorption_fire" in passive:
        row_dict["fire_absorption"] = calcAbsorption(row_dict["fire_absorption"], passive.pop("absorption_fire"))
    if "absorption_lightning" in passive:
        row_dict["lightning_absorption"] = calcAbsorption(row_dict["lightning_absorption"], passive.pop("absorption_lightning"))
    if "absorption_holy" in passive:
        row_dict["holy_absorption"] = calcAbsorption(row_dict["holy_absorption"], passive.pop("absorption_holy"))
    

def calcAbsorption(absorption, absorption_passive):
    return -((1.0 - absorption) * (-absorption_passive + 1.0)) + 1.0


##############################################
# talisman_data.json
##############################################

def getTalismanData():
    accessory_data = []
    for key, row in EquipParamAccessory.items():
        if row['Is Droppable'] == InputBoolean.TRUE.value:
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']
            row_dict["weight"] = float(row['Weight'])
            row_dict["passive_1"] = getPassiveEffect(SpEffectParam[row['SpEffect ID [0]']], row['SpEffect ID [0]'],  False)
            # Millicent's Prosthesis
            if (int(row['SpEffect ID [0]']) == 312500):
                row_dict["passive_2"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 1)], str(int(row['SpEffect ID [0]']) + 1), False)
                row_dict["passive_3"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 2)], str(int(row['SpEffect ID [0]']) + 2), False)
                row_dict["passive_4"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 3)], str(int(row['SpEffect ID [0]']) + 3), False)
                row_dict["passive_5"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 4)], str(int(row['SpEffect ID [0]']) + 4), False)
            # Winged Sword Insignia and Rotten Winged Sword Insignia
            elif (int(row['SpEffect ID [0]']) == 320800 or int(row['SpEffect ID [0]']) == 320810):
                row_dict["passive_2"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 1)], str(int(row['SpEffect ID [0]']) + 1), False)
                row_dict["passive_3"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 2)], str(int(row['SpEffect ID [0]']) + 2), False)
                row_dict["passive_4"] = getPassiveEffect(SpEffectParam[str(int(row['SpEffect ID [0]']) + 3)], str(int(row['SpEffect ID [0]']) + 3), False)
            accessory_data.append(row_dict)

    return accessory_data


##############################################
# talisman_groups.json
##############################################

def getTalismanGroups():
    accessory_groups = OrderedDict()
    accessory_groups['label'] = "Talismans"
    accessory_groups['options'] = []
    i = 1
    for key, row in EquipParamAccessory.items():
        if row['Is Droppable'] == InputBoolean.TRUE.value:
            accessory_groups["options"].append({'label': row['Row Name'], 'value': i})
            i+=1

    return accessory_groups


# Avg Accumulator Value for attacks. Could potentially switch for weapons in subsequent patches
# Look at AtkParam_Pc to see if the TargetSpEffect [0] for each weapon changes the ID of SpEffect ID 
# used to know if using different Id for acummulator
accumulatorIncrementValue = int(SpEffectParam['6903']['Accumulator - Increment Value'])

State_Info_Effect = {
    # SpEffectParam - State Info
    0: "None",
    2: "Poison",
    5: "Scarlet Rot",
    48 : "Increase Damage",
    49 : "Increase Defence",
    50 : "HP/FP/Stamina Recovery",
    54 : "Modify Enemy listen Reduction",
    66 : "Modify Item Discovery",
    71 : "Spell Power Boost",
    75 : "Green Blossom VFX",
    76 : "Modify Rune Gain",
    123: "Trigger on Roll (Head)",
    124: "Trigger on Roll (Body)",
    125: "Trigger on Roll (Arm)",
    126: "Trigger on Roll (Leg)",
    152: "Enable Attack Effect against Enemy",
    153: "Enable Attack Effect against Player",
    158: "Left Hand Buff VFX",
    159: "Destroy Accessory but Save Runes",
    168: "Bow Distance Change",
    193: "Modify Effect Duration",
    197: "Enhance Thrusting Counter Attacks",
    199: "Apply Kill Effect",
    275: "Player Behavior ID Change",
    288: "Trigger on Critical Hit (HP)",
    289: "Trigger on Critical Hit (FP)",
    290: "Extend Roll Invinsibility",
    303: "Conditional 1",
    304: "Conditional 2",
    305: "Conditional 3",
    315: "Scale Attack Power with Equip Load",
    335: "Trigger during Critical Hits",
    367: "Enhance Critical Attacks",
    379: "Trigger in Presence of Blood Loss",
    380: "Trigger in Presence of Rot",
    390: "Pacify Wild Animals",
    391: "Unknown",
    392: "Unknown",
    393: "Unknown",
    397: "Unknown",
    437: "Madness",
    450: "Reduce Headshot Impact",
    459: "Unknown",
    460: "Unknown",
    461: "Unknown",
    462: "Unknown",
    463: "Unknown",
    464: "Unknown",
    465: "Unknown",
    466: "Trigger on Crouch"
}

Conditional_Weapon_Effect = {
    # SpEffectParam - Conditional Weapon Effect
    0 : "None",
    1 : "Full Moon Spell",
    2 : "Carian Sword Spell",
    3 : "Glintblade Spell",
    4 : "Stonedigger Spell",
    5 : "Crystalian Spell",
    6 : "Karolos Spell",
    7 : "Olivinus Spell",
    8 : "Lava Spell",
    9 : "Thorn Spell",
    10 : "Death Spell",
    11 : "Gravity Spell",
    12 : "Night Spell",
    13 : "Ranni Spell",
    14 : "Azur Spell",
    15 : "Lusat Spell",
    20 : "Black Flame Spell",
    21: "Flame Spell",
    22 : "Dragon Cult Spell",
    23 : "Bestial Spell",
    24 : "Golden Order Spell",
    25 : "Dragon Communion Spell",
    26 : "Frenzied Flame Spell",
    27 : "Godslayer Spell",
    28 : "Primordial Crucible Spell",
    100 : "Charge Attack",
    101 : "Horseback Attack",
    102 : "Jump Attack",
    103 : "Guard Counter Attack",
    104 : "Final Chain Attack",
    105 : "Ammunition Attack",
    106 : "Roar Attack",
    107 : "Breath Attack",
    108 : "Pot Item Attack",
    109 : "Perfume Item Attack",
    110 : "Charged Attack",
    111 : "Charged Skill Attack",
    112 : "Skill Attack",
    113 : "Ranged Skill Attack",
    114 : "Vapor Attack",
    115 : "Unknown Attack",
    116 : "Unknown Attack",
    117 : "Wraith Attack",
    118 : "Ammunition On Hit Attack"
}


def getPassiveEffect(specialEffect, specialEffectId, passiveFromArmor):
    row_dict = OrderedDict()
    row_dict["name"] = specialEffect['Row Name']
    row_dict["state_info"] = State_Info_Effect[int(specialEffect['State Info'])]
    row_dict["trigger_on_state_info_1"] = State_Info_Effect[int(specialEffect['Trigger on State Info [1]'])]
    row_dict["trigger_on_state_info_2"] = State_Info_Effect[int(specialEffect['Trigger on State Info [2]'])]
    row_dict["trigger_on_state_info_3"] = State_Info_Effect[int(specialEffect['Trigger on State Info [3]'])]
    descriptionArray = []
            
    attack_percent_dict = OrderedDict()
    if (float(specialEffect['Attack %: Physical']) != 1.0):
        row_dict["attack_percent_physical"] = float(specialEffect['Attack %: Physical']) - 1.0
        if ((float(specialEffect['Attack %: Physical']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['Attack %: Physical']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Physical']) - 1.0) * 100] = "Increase the Calculated Attack of Physical"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Physical']) - 1.0) * 100] = "Decrease the Calculated Attack of Physical"
    if (float(specialEffect['Attack %: Standard']) != 1.0):
        row_dict["attack_percent_standard"] = float(specialEffect['Attack %: Standard']) - 1.0
        if ((float(specialEffect['Attack %: Standard']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Standard']) - 1.0) * 100] += ", Standard"
        else:
            if float(specialEffect['Attack %: Standard']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Standard']) - 1.0) * 100] = "Increase the Calculated Attack of Standard"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Standard']) - 1.0) * 100] = "Decrease the Calculated Attack of Standard"
    if (float(specialEffect['Attack %: Thrust']) != 1.0):
        row_dict["attack_percent_thrust"] = float(specialEffect['Attack %: Thrust']) - 1.0
        if ((float(specialEffect['Attack %: Thrust']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Thrust']) - 1.0) * 100] += ", Thrust"
        else:
            if float(specialEffect['Attack %: Thrust']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Thrust']) - 1.0) * 100] = "Increase the Calculated Attack of Thrust"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Thrust']) - 1.0) * 100] = "Decrease the Calculated Attack of Thrust"
    if (float(specialEffect['Attack %: Strike']) != 1.0):
        row_dict["attack_percent_strike"] = float(specialEffect['Attack %: Strike']) - 1.0
        if ((float(specialEffect['Attack %: Strike']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Strike']) - 1.0) * 100] += ", Strike"
        else:
            if float(specialEffect['Attack %: Strike']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Strike']) - 1.0) * 100] = "Increase the Calculated Attack of Strike"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Strike']) - 1.0) * 100] = "Decrease the Calculated Attack of Strike"
    if (float(specialEffect['Attack %: Slash']) != 1.0):
        row_dict["attack_percent_slash"] = float(specialEffect['Attack %: Slash']) - 1.0
        if ((float(specialEffect['Attack %: Slash']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Slash']) - 1.0) * 100] += ", Slash"
        else:
            if float(specialEffect['Attack %: Slash']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Slash']) - 1.0) * 100] = "Increase the Calculated Attack of Slash"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Slash']) - 1.0) * 100] = "Decrease the Calculated Attack of Slash"
    if (float(specialEffect['Attack %: Magic']) != 1.0):
        row_dict["attack_percent_magic"] = float(specialEffect['Attack %: Magic']) - 1.0
        if ((float(specialEffect['Attack %: Magic']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['Attack %: Magic']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Magic']) - 1.0) * 100] = "Increase the Calculated Attack of Magic"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Magic']) - 1.0) * 100] = "Decrease the Calculated Attack of Magic"
    if (float(specialEffect['Attack %: Fire']) != 1.0):
        row_dict["attack_percent_fire"] = float(specialEffect['Attack %: Fire']) - 1.0
        if ((float(specialEffect['Attack %: Fire']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['Attack %: Fire']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Fire']) - 1.0) * 100] = "Increase the Calculated Attack of Fire"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Fire']) - 1.0) * 100] = "Decrease the Calculated Attack of Fire"
    if (float(specialEffect['Attack %: Lightning']) != 1.0):
        row_dict["attack_percent_lightning"] = float(specialEffect['Attack %: Lightning'])  - 1.0
        if ((float(specialEffect['Attack %: Lightning']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['Attack %: Lightning']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Lightning']) - 1.0) * 100] = "Increase the Calculated Attack of Lightning"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Lightning']) - 1.0) * 100] = "Decrease the Calculated Attack of Lightning"
    if (float(specialEffect['Attack %: Holy']) != 1.0):
        row_dict["attack_percent_holy"] = float(specialEffect['Attack %: Holy']) - 1.0
        if ((float(specialEffect['Attack %: Holy']) - 1.0) * 100 in attack_percent_dict):
            attack_percent_dict[(float(specialEffect['Attack %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['Attack %: Holy']) > 1.0:
                attack_percent_dict[(float(specialEffect['Attack %: Holy']) - 1.0) * 100] = "Increase the Calculated Attack of Holy"
            else:
                attack_percent_dict[(float(specialEffect['Attack %: Holy']) - 1.0) * 100] = "Decrease the Calculated Attack of Holy"
    for key, value in attack_percent_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")
    

    power_percent_dict = OrderedDict()
    if (float(specialEffect['Power %: Physical']) != 1.0):
        row_dict["power_percent_physical"] = float(specialEffect['Power %: Physical']) - 1.0
        if ((float(specialEffect['Power %: Physical']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['Power %: Physical']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Physical']) - 1.0) * 100] = "Increase the Attack Power of Physical"
            else:
                power_percent_dict[(float(specialEffect['Power %: Physical']) - 1.0) * 100] = "Decrease the Attack Power of Physical"
    if (float(specialEffect['Power %: Standard']) != 1.0):
        row_dict["power_percent_standard"] = float(specialEffect['Power %: Standard']) - 1.0
        if ((float(specialEffect['Power %: Standard']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Standard']) - 1.0) * 100] += ", Standard"
        else:
            if float(specialEffect['Power %: Standard']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Standard']) - 1.0) * 100] = "Increase the Attack Power of Standard"
            else:
                power_percent_dict[(float(specialEffect['Power %: Standard']) - 1.0) * 100] = "Decrease the Attack Power of Standard"
    if (float(specialEffect['Power %: Thrust']) != 1.0):
        row_dict["power_percent_thrust"] = float(specialEffect['Power %: Thrust']) - 1.0
        if ((float(specialEffect['Power %: Thrust']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Thrust']) - 1.0) * 100] += ", Thrust"
        else:
            if float(specialEffect['Power %: Thrust']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Thrust']) - 1.0) * 100] = "Increase the Attack Power of Thrust"
            else:
                power_percent_dict[(float(specialEffect['Power %: Thrust']) - 1.0) * 100] = "Decrease the Attack Power of Thrust"
    if (float(specialEffect['Power %: Strike']) != 1.0):
        row_dict["power_percent_strike"] = float(specialEffect['Power %: Strike']) - 1.0
        if ((float(specialEffect['Power %: Strike']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Strike']) - 1.0) * 100] += ", Strike"
        else:
            if float(specialEffect['Power %: Strike']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Strike']) - 1.0) * 100] = "Increase the Attack Power of Strike"
            else:
                power_percent_dict[(float(specialEffect['Power %: Strike']) - 1.0) * 100] = "Decrease the Attack Power of Strike"
    if (float(specialEffect['Attack +: Slash']) != 1.0):
        row_dict["power_percent_slash"] = float(specialEffect['Attack +: Slash']) - 1.0
        if ((float(specialEffect['Attack +: Slash']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Attack +: Slash']) - 1.0) * 100] += ", Slash"
        else:
            if float(specialEffect['Attack +: Slash']) > 1.0:
                power_percent_dict[(float(specialEffect['Attack +: Slash']) - 1.0) * 100] = "Increase the Attack Power of Slash"
            else:
                power_percent_dict[(float(specialEffect['Attack +: Slashe']) - 1.0) * 100] = "Decrease the Attack Power of Slash"
    if (float(specialEffect['Power %: Magic']) != 1.0):
        row_dict["power_percent_magic"] = float(specialEffect['Power %: Magic']) - 1.0
        if ((float(specialEffect['Power %: Magic']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['Power %: Magic']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Magic']) - 1.0) * 100] = "Increase the Attack Power of Magic"
            else:
                power_percent_dict[(float(specialEffect['Power %: Magic']) - 1.0) * 100] = "Decrease the Attack Power of Magic"
    if (float(specialEffect['Power %: Fire']) != 1.0):
        row_dict["power_percent_fire"] = float(specialEffect['Power %: Fire']) - 1.0
        if ((float(specialEffect['Power %: Fire']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['Power %: Fire']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Fire']) - 1.0) * 100] = "Increase the Attack Power of Fire"
            else:
                power_percent_dict[(float(specialEffect['Power %: Fire']) - 1.0) * 100] = "Decrease the Attack Power of Fire"
    if (float(specialEffect['Power %: Lightning']) != 1.0):
        row_dict["power_percent_lightning"] = float(specialEffect['Power %: Lightning'])  - 1.0
        if ((float(specialEffect['Power %: Lightning']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['Power %: Lightning']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Lightning']) - 1.0) * 100] = "Increase the Attack Power of Lightning"
            else:
                power_percent_dict[(float(specialEffect['Power %: Lightning']) - 1.0) * 100] = "Decrease the Attack Power of Lightning"
    if (float(specialEffect['Power %: Holy']) != 1.0):
        row_dict["power_percent_holy"] = float(specialEffect['Power %: Holy']) - 1.0
        if ((float(specialEffect['Power %: Holy']) - 1.0) * 100 in power_percent_dict):
            power_percent_dict[(float(specialEffect['Power %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['Power %: Holy']) > 1.0:
                power_percent_dict[(float(specialEffect['Power %: Holy']) - 1.0) * 100] = "Increase the Attack Power of Holy"
            else:
                power_percent_dict[(float(specialEffect['Power %: Holy']) - 1.0) * 100] = "Decrease the Attack Power of Holy"
    for key, value in power_percent_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    damage_dict = OrderedDict()
    if (int(specialEffect['Damage +: Physical']) != 0):
        row_dict["damage_physical"] = int(specialEffect['Damage +: Physical'])
        if (int(specialEffect['Damage +: Physical']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Physical'])] += ", Physical"
        else:
            if int(specialEffect['Damage +: Physical']) > 0:
                damage_dict[int(specialEffect['Damage +: Physical'])] = "Add Attack Power for Physical"
            else:
                damage_dict[int(specialEffect['Damage +: Physical'])] = "Subtract Attack Power for Physical"
    if (int(specialEffect['Damage +: Standard']) != 0.0):
        row_dict["damage_standard"] = int(specialEffect['Damage +: Standard'])
        if (int(specialEffect['Damage +: Standard']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Standard'])] += ", Standard"
        else:
            if int(specialEffect['Damage +: Standard']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Standard'])] = "Add Attack Power for Standard"
            else:
                damage_dict[int(specialEffect['Damage +: Standard'])] = "Subtract Attack Power for Standard"
    if (int(specialEffect['Damage +: Thrust']) != 0.0):
        row_dict["damage_thrust"] = int(specialEffect['Damage +: Thrust'])
        if (int(specialEffect['Damage +: Thrust']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Thrust'])] += ", Thrust"
        else:
            if int(specialEffect['Damage +: Thrust']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Thrust'])] = "Add Attack Power for Thrust"
            else:
                damage_dict[int(specialEffect['Damage +: Thrust'])] = "Subtract Attack Power for Thrust"
    if (int(specialEffect['Damage +: Strike']) != 0.0):
        row_dict["damage_strike"] = int(specialEffect['Damage +: Strike'])
        if (int(specialEffect['Damage +: Strike']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Strike'])] += ", Strike"
        else:
            if int(specialEffect['Damage +: Strike']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Strike'])] = "Add Attack Power for Strike"
            else:
                damage_dict[int(specialEffect['Damage +: Strike'])] = "Subtract Attack Power for Strike"
    if (int(specialEffect['Power +: Slash']) != 0.0):
        row_dict["damage_slash"] = int(specialEffect['Power +: Slash'])
        if (int(specialEffect['Power +: Slash']) in damage_dict):
            damage_dict[int(specialEffect['Power +: Slash'])] += ", Slash"
        else:
            if int(specialEffect['Power +: Slash']) > 0.0:
                damage_dict[int(specialEffect['Power +: Slash'])] = "Add Attack Power for Slash"
            else:
                damage_dict[int(specialEffect['Power +: Slash'])] = "Subtract Attack Power for Slash"
    if (int(specialEffect['Damage +: Magic']) != 0):
        row_dict["damage_magic"] = int(specialEffect['Damage +: Magic'])
        if (int(specialEffect['Damage +: Magic']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Magic'])] += ", Magic"
        else:
            if int(specialEffect['Damage +: Magic']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Magic'])] = "Add Attack Power for Magic"
            else:
                damage_dict[int(specialEffect['Damage +: Magic'])] = "Subtract Attack Power for Magic"
    if (int(specialEffect['Damage +: Fire']) != 0):
        row_dict["damage_fire"] = int(specialEffect['Damage +: Fire'])
        if (int(specialEffect['Damage +: Fire']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Fire'])] += ", Fire"
        else:
            if int(specialEffect['Damage +: Fire']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Fire'])] = "Add Attack Power for Fire"
            else:
                damage_dict[int(specialEffect['Damage +: Fire'])] = "Subtract Attack Power for Fire"
    if (int(specialEffect['Damage +: Lighting']) != 0):
        row_dict["damage_lightning"] = int(specialEffect['Damage +: Lighting'])
        if (int(specialEffect['Damage +: Lighting']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Lighting'])] += ", Lightning"
        else:
            if int(specialEffect['Damage +: Lighting']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Lighting'])] = "Add Attack Power for Lightning"
            else:
                damage_dict[int(specialEffect['Damage +: Lighting'])] = "Subtract Attack Power for Lightning"
    if (int(specialEffect['Damage +: Holy']) != 0):
        row_dict["damage_holy"] = int(specialEffect['Damage +: Holy'])
        if (int(specialEffect['Damage +: Holy']) in damage_dict):
            damage_dict[int(specialEffect['Damage +: Holy'])] += ", Holy"
        else:
            if int(specialEffect['Damage +: Holy']) > 0.0:
                damage_dict[int(specialEffect['Damage +: Holy'])] = "Add Attack Power for Holy"
            else:
                damage_dict[int(specialEffect['Damage +: Holy'])] = "Subtract Attack Power for Holy"
    for key, value in damage_dict.items():
        descriptionArray.append(value + " types by " + str(abs(key)))
    
    damage_percent_enemy_dict = OrderedDict()
    if (float(specialEffect['Damage %: Physical']) != 1.0):
        row_dict["damage_percent_physical"] = float(specialEffect['Damage %: Physical']) - 1.0
        if ((float(specialEffect['Damage %: Physical']) - 1.0) * 100 in damage_percent_enemy_dict):
            damage_percent_enemy_dict[(float(specialEffect['Damage %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['Damage %: Physical']) > 1.0:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Physical']) - 1.0) * 100] = "Increase the Damage against non-player enemies for Physical"
            else:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Physical']) - 1.0) * 100] = "Decrease the Damage against non-player enemies for Physical"
    if (float(specialEffect['Damage %: Magic']) != 1.0):
        row_dict["damage_percent_magic"] = float(specialEffect['Damage %: Magic']) - 1.0
        if ((float(specialEffect['Damage %: Magic']) - 1.0) * 100 in damage_percent_enemy_dict):
            damage_percent_enemy_dict[(float(specialEffect['Damage %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['Damage %: Magic']) > 1.0:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Magic']) - 1.0) * 100] = "Increase the Damage against non-player enemies for Magic"
            else:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Magic']) - 1.0) * 100] = "Decrease the Damage against non-player enemies for Magic"
    if (float(specialEffect['Damage %: Fire']) != 1.0):
        row_dict["damage_percent_fire"] = float(specialEffect['Damage %: Fire']) - 1.0
        if ((float(specialEffect['Damage %: Fire']) - 1.0) * 100 in damage_percent_enemy_dict):
            damage_percent_enemy_dict[(float(specialEffect['Damage %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['Damage %: Fire']) > 1.0:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Fire']) - 1.0) * 100] = "Increase the Damage against non-player enemies for Fire"
            else:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Fire']) - 1.0) * 100] = "Decrease the Damage against non-player enemies for Fire"
    if (float(specialEffect['Damage %: Lightning']) != 1.0):
        row_dict["damage_percent_lightning"] = float(specialEffect['Damage %: Lightning'])  - 1.0
        if ((float(specialEffect['Damage %: Fire']) - 1.0) * 100 in damage_percent_enemy_dict):
            damage_percent_enemy_dict[(float(specialEffect['Damage %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['Damage %: Lightning']) > 1.0:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Lightning']) - 1.0) * 100] = "Increase the Damage against non-player enemies for Lightning"
            else:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Lightning']) - 1.0) * 100] = "Decrease the Damage against non-player enemies for Lightning"
    if (float(specialEffect['Damage %: Holy']) != 1.0):
        row_dict["damage_percent_holy"] = float(specialEffect['Damage %: Holy']) - 1.0
        if ((float(specialEffect['Damage %: Holy']) - 1.0) * 100 in damage_percent_enemy_dict):
            damage_percent_enemy_dict[(float(specialEffect['Damage %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['Damage %: Holy']) > 1.0:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Holy']) - 1.0) * 100] = "Increase the Damage against non-player enemies for Holy"
            else:
                damage_percent_enemy_dict[(float(specialEffect['Damage %: Holy']) - 1.0) * 100] = "Decrease the Damage against non-player enemies for Holy"
    for key, value in damage_percent_enemy_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    damage_percent_player_dict = OrderedDict()    
    if (float(specialEffect['PVP Damage %: Physical']) != 1.0):
        row_dict["pvp_damage_percent_physical"] = float(specialEffect['PVP Damage %: Physical']) - 1.0
        if ((float(specialEffect['PVP Damage %: Physical']) - 1.0) * 100 in damage_percent_player_dict):
            damage_percent_player_dict[(float(specialEffect['PVP Damage %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['PVP Damage %: Physical']) > 1.0:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Physical']) - 1.0) * 100] = "Increase the Damage against players for Physical"
            else:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Physical']) - 1.0) * 100] = "Decrease the Damage against players for Physical"
    if (float(specialEffect['PVP Damage %: Magic']) != 1.0):
        row_dict["pvp_damage_percent_magic"] = float(specialEffect['PVP Damage %: Magic']) - 1.0
        if ((float(specialEffect['PVP Damage %: Magic']) - 1.0) * 100 in damage_percent_player_dict):
            damage_percent_player_dict[(float(specialEffect['PVP Damage %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['PVP Damage %: Magic']) > 1.0:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Magic']) - 1.0) * 100] = "Increase the Damage against players for Magic"
            else:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Magic']) - 1.0) * 100] = "Decrease the Damage against players for Magic"
    if (float(specialEffect['PVP Damage %: Fire']) != 1.0):
        row_dict["pvp_damage_percent_fire"] = float(specialEffect['PVP Damage %: Fire']) - 1.0
        if ((float(specialEffect['PVP Damage %: Fire']) - 1.0) * 100 in damage_percent_player_dict):
            damage_percent_player_dict[(float(specialEffect['PVP Damage %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['PVP Damage %: Fire']) > 1.0:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Fire']) - 1.0) * 100] = "Increase the Damage against players for Fire"
            else:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Fire']) - 1.0) * 100] = "Decrease the Damage against players for Fire"
    if (float(specialEffect['PVP Damage %: Lightning']) != 1.0):
        row_dict["pvp_damage_percent_lightning"] = float(specialEffect['PVP Damage %: Lightning'])  - 1.0
        if ((float(specialEffect['PVP Damage %: Lightning']) - 1.0) * 100 in damage_percent_player_dict):
            damage_percent_player_dict[(float(specialEffect['PVP Damage %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['PVP Damage %: Lightning']) > 1.0:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Lightning']) - 1.0) * 100] = "Increase the Damage against players for Lightning"
            else:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Lightning']) - 1.0) * 100] = "Decrease the Damage against players for Lightning"
    if (float(specialEffect['PVP Damage %: Holy']) != 1.0):
        row_dict["pvp_damage_percent_holy"] = float(specialEffect['PVP Damage %: Holy']) - 1.0
        if ((float(specialEffect['PVP Damage %: Holy']) - 1.0) * 100 in damage_percent_player_dict):
            damage_percent_player_dict[(float(specialEffect['PVP Damage %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['PVP Damage %: Holy']) > 1.0:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Holy']) - 1.0) * 100] = "Increase the Damage against players for Holy"
            else:
                damage_percent_player_dict[(float(specialEffect['PVP Damage %: Holy']) - 1.0) * 100] = "Decrease the Damage against players for Holy"
    for key, value in damage_percent_player_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    
    conditional_weapons = []
    if (int(specialEffect['Conditional Weapon Effect 1']) != 0):
        row_dict["coditional_weapon_effect_1"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 1'])]
        conditional_weapons.append(Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 1'])])
    if (int(specialEffect['Conditional Weapon Effect 2']) != 0):
        row_dict["coditional_weapon_effect_2"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 2'])]
        conditional_weapons.append(Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 2'])])
    if (int(specialEffect['Conditional Weapon Effect 3']) != 0):
        row_dict["coditional_weapon_effect_3"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 3'])]
        conditional_weapons.append(Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 3'])])

    for value in conditional_weapons:
        descriptionArray.append("Damage Effect Only Applies for " + value + "s")

    defense_dict = OrderedDict() 
    if (int(specialEffect['Defence +: Physical']) != 0):
        row_dict["defense_physical"] = int(specialEffect['Defence +: Physical'])
        if (int(specialEffect['Defence +: Physical']) in defense_dict):
            defense_dict[int(specialEffect['Defence +: Physical'])] += ", Physical"
        else:
            if int(specialEffect['Defence +: Physical']) > 0:
                defense_dict[int(specialEffect['Defence +: Physical'])] = "Add Defense for Physical"
            else:
                defense_dict[int(specialEffect['Defence +: Physical'])] = "Subtract Defense for Physical"
    if (int(specialEffect['Defence +: Magic']) != 0):
        row_dict["defense_magic"] = int(specialEffect['Defence +: Magic'])
        if (int(specialEffect['Defence +: Magic']) in defense_dict):
            defense_dict[int(specialEffect['Defence +: Magic'])] += ", Magic"
        else:
            if int(specialEffect['Defence +: Magic']) > 0:
                defense_dict[int(specialEffect['Defence +: Magic'])] = "Add Defense for Magic"
            else:
                defense_dict[int(specialEffect['Defence +: Magic'])] = "Subtract Defense for Magic"
    if (int(specialEffect['Defence +: Fire']) != 0):
        row_dict["defense_fire"] = int(specialEffect['Defence +: Fire'])
        if (int(specialEffect['Defence +: Fire']) in defense_dict):
            defense_dict[int(specialEffect['Defence +: Fire'])] += ", Fire"
        else:
            if int(specialEffect['Defence +: Fire']) > 0:
                defense_dict[int(specialEffect['Defence +: Fire'])] = "Add Defense for Fire"
            else:
                defense_dict[int(specialEffect['Defence +: Fire'])] = "Subtract Defense for Fire"
    if (int(specialEffect['Defence +: Lightning']) != 0):
        row_dict["defense_lightning"] = int(specialEffect['Defence +: Lightning'])
        if (int(specialEffect['Defence +: Lightning']) in defense_dict):
            defense_dict[int(specialEffect['Defence +: Lightning'])] += ", Lightning"
        else:
            if int(specialEffect['Defence +: Lightning']) > 0:
                defense_dict[int(specialEffect['Defence +: Lightning'])] = "Add Defense for Lightning"
            else:
                defense_dict[int(specialEffect['Defence +: Lightning'])] = "Subtract Defense for Lightning"
    if (int(specialEffect['Defence +: Holy']) != 0):
        row_dict["defense_holy"] = int(specialEffect['Defence +: Holy'])
        if (int(specialEffect['Defence +: Holy']) in defense_dict):
            defense_dict[int(specialEffect['Defence +: Holy'])] += ", Holy"
        else:
            if int(specialEffect['Defence +: Holy']) > 0:
                defense_dict[int(specialEffect['Defence +: Holy'])] = "Add Defense for Holy"
            else:
                defense_dict[int(specialEffect['Defence +: Holy'])] = "Subtract Defense for Holy"
    for key, value in defense_dict.items():
        descriptionArray.append(value + " types by " + str(abs(key)))

    defense_percent_dict = OrderedDict() 
    if (float(specialEffect['Defence %: Physical']) != 1.0):
        row_dict["defense_percent_physical"] = float(specialEffect['Defence %: Physical']) - 1.0
        if ((float(specialEffect['Defence %: Physical']) - 1.0) * 100 in defense_percent_dict):
            defense_percent_dict[(float(specialEffect['Defence %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['Defence %: Physical']) > 1.0:
                defense_percent_dict[(float(specialEffect['Defence %: Physical']) - 1.0) * 100] = "Increase Defence of Physical"
            else:
                defense_percent_dict[(float(specialEffect['Defence %: Physical']) - 1.0) * 100] = "Decrease Defence of Physical"
    if (float(specialEffect['Defence %: Magic']) != 1.0):
        row_dict["defense_percent_magic"] = float(specialEffect['Defence %: Magic']) - 1.0
        if ((float(specialEffect['Defence %: Magic']) - 1.0) * 100 in defense_percent_dict):
            defense_percent_dict[(float(specialEffect['Defence %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['Defence %: Magic']) > 1.0:
                defense_percent_dict[(float(specialEffect['Defence %: Magic']) - 1.0) * 100] = "Increase Defence of Magic"
            else:
                defense_percent_dict[(float(specialEffect['Defence %: Magic']) - 1.0) * 100] = "Decrease Defence of Magic"
    if (float(specialEffect['Defence %: Fire']) != 1.0):
        row_dict["defense_percent_fire"] = float(specialEffect['Defence %: Fire']) - 1.0
        if ((float(specialEffect['Defence %: Fire']) - 1.0) * 100 in defense_percent_dict):
            defense_percent_dict[(float(specialEffect['Defence %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['Defence %: Fire']) > 1.0:
                defense_percent_dict[(float(specialEffect['Defence %: Fire']) - 1.0) * 100] = "Increase Defence of Fire"
            else:
                defense_percent_dict[(float(specialEffect['Defence %: Fire']) - 1.0) * 100] = "Decrease Defence of Fire"
    if (float(specialEffect['Defence %: Lightning']) != 1.0):
        row_dict["defense_percent_lightning"] = float(specialEffect['Defence %: Lightning'])  - 1.0
        if ((float(specialEffect['Defence %: Lightning']) - 1.0) * 100 in defense_percent_dict):
            defense_percent_dict[(float(specialEffect['Defence %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['Defence %: Lightning']) > 1.0:
                defense_percent_dict[(float(specialEffect['Defence %: Lightning']) - 1.0) * 100] = "Increase Defence of Lightning"
            else:
                defense_percent_dict[(float(specialEffect['Defence %: Lightning']) - 1.0) * 100] = "Decrease Defence of Lightning"
    if (float(specialEffect['Defence %: Holy']) != 1.0):
        row_dict["defensee_percent_holy"] = float(specialEffect['Defence %: Holy']) - 1.0
        if ((float(specialEffect['Defence %: Holy']) - 1.0) * 100 in defense_percent_dict):
            defense_percent_dict[(float(specialEffect['Defence %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['Defence %: Holy']) > 1.0:
                defense_percent_dict[(float(specialEffect['Defence %: Holy']) - 1.0) * 100] = "Increase Defence of Holy"
            else:
                defense_percent_dict[(float(specialEffect['Defence %: Holy']) - 1.0) * 100] = "Decrease Defence of Holy"
    for key, value in defense_percent_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    absorption_percent_enemy_dict = OrderedDict()
    if (float(specialEffect['Absorption %: Physical']) != 1.0):
        row_dict["absorption_percent_physical"] = -(float(specialEffect['Absorption %: Physical']) - 1.0)
        if (-(float(specialEffect['Absorption %: Physical']) - 1.0) * 100 in absorption_percent_enemy_dict):
            absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['Absorption %: Physical']) < 1.0:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Physical']) - 1.0) * 100] = \
                    "Increase the Absorption from non-player enemy attacks for Physical"
            else:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Physical']) - 1.0) * 100] = \
                    "Decrease the Absorption from non-player enemy attacks for Physical"
    if (float(specialEffect['Absorption %: Magic']) != 1.0):
        row_dict["absorption_percent_magic"] = -(float(specialEffect['Absorption %: Magic']) - 1.0)
        if (-(float(specialEffect['Absorption %: Magic']) - 1.0) * 100 in absorption_percent_enemy_dict):
            absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['Absorption %: Magic']) < 1.0:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Magic']) - 1.0) * 100] = "Increase the Absorption from non-player enemy attacks for Magic"
            else:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Magic']) - 1.0) * 100] = "Decrease the Absorption from non-player enemy attacks for Magic"
    if (float(specialEffect['Absorption %: Fire']) != 1.0):
        row_dict["absorption_percent_fire"] = -(float(specialEffect['Absorption %: Fire']) - 1.0)
        if (-(float(specialEffect['Absorption %: Fire']) - 1.0) * 100 in absorption_percent_enemy_dict):
            absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['Absorption %: Fire']) < 1.0:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Fire']) - 1.0) * 100] = "Increase the Absorption from non-player enemy attacks for Fire"
            else:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Fire']) - 1.0) * 100] = "Decrease the Absorption from non-player enemy attacks for Fire"
    if (float(specialEffect['Absorption %: Lightning']) != 1.0):
        row_dict["absorption_percent_lightning"] = -(float(specialEffect['Absorption %: Lightning'])  - 1.0)
        if (-(float(specialEffect['Absorption %: Lightning']) - 1.0) * 100 in absorption_percent_enemy_dict):
            absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['Absorption %: Lightning']) < 1.0:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Lightning']) - 1.0) * 100] = \
                    "Increase the Absorption from non-player enemy attacks for Lightning"
            else:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Lightning']) - 1.0) * 100] = \
                    "Decrease the Absorption from non-player enemy attacks for Lightning"
    if (float(specialEffect['Absorption %: Holy']) != 1.0):
        row_dict["absorption_percent_holy"] = -(float(specialEffect['Absorption %: Holy']) - 1.0)
        if (-(float(specialEffect['Absorption %: Holy']) - 1.0) * 100 in absorption_percent_enemy_dict):
            absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['Absorption %: Holy']) < 1.0:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Holy']) - 1.0) * 100] = "Increase the Absorption from non-player enemy attacks for Holy"
            else:
                absorption_percent_enemy_dict[-(float(specialEffect['Absorption %: Holy']) - 1.0) * 100] = "Decrease the Absorption from non-player enemy attacks for Holy"
    for key, value in absorption_percent_enemy_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    absorption_percent_player_dict = OrderedDict()
    if (float(specialEffect['PVP Absorption %: Physical']) != 1.0):
        row_dict["pvp_absorption_percent_physical"] = -(float(specialEffect['PVP Absorption %: Physical']) - 1.0)
        if (-(float(specialEffect['PVP Absorption %: Physical']) - 1.0) * 100 in absorption_percent_player_dict):
            absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Physical']) - 1.0) * 100] += ", Physical"
        else:
            if float(specialEffect['PVP Absorption %: Physical']) < 1.0:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Physical']) - 1.0) * 100] = "Increase the Absorption from player attacks for Physical"
            else:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Physical']) - 1.0) * 100] = "Decrease the Absorption from player attacks for Physical"
    if (float(specialEffect['PVP Absorption %: Magic']) != 1.0):
        row_dict["pvp_absorption_percent_magic"] = -(float(specialEffect['PVP Absorption %: Magic']) - 1.0)
        if (-(float(specialEffect['PVP Absorption %: Magic']) - 1.0) * 100 in absorption_percent_player_dict):
            absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Magic']) - 1.0) * 100] += ", Magic"
        else:
            if float(specialEffect['PVP Absorption %: Magic']) < 1.0:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Magic']) - 1.0) * 100] = "Increase the Absorption from player attacks for Magic"
            else:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Magic']) - 1.0) * 100] = "Decrease the Absorption from player attacks for Magic"
    if (float(specialEffect['PVP Absorption %: Fire']) != 1.0):
        row_dict["pvp_absorption_percent_fire"] = -(float(specialEffect['PVP Absorption %: Fire']) - 1.0)
        if (-(float(specialEffect['PVP Absorption %: Fire']) - 1.0) * 100 in absorption_percent_player_dict):
            absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Fire']) - 1.0) * 100] += ", Fire"
        else:
            if float(specialEffect['PVP Absorption %: Fire']) < 1.0:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Fire']) - 1.0) * 100] = "Increase the Absorption from player attacks for Fire"
            else:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Fire']) - 1.0) * 100] = "Decrease the Absorption from player attacks for Fire"
    if (float(specialEffect['PVP Absorption %: Lightning']) != 1.0):
        row_dict["pvp_absorptione_percent_lightning"] = -(float(specialEffect['PVP Absorption %: Lightning'])  - 1.0)
        if (-(float(specialEffect['PVP Absorption %: Lightning']) - 1.0) * 100 in absorption_percent_player_dict):
            absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Lightning']) - 1.0) * 100] += ", Lightning"
        else:
            if float(specialEffect['PVP Absorption %: Lightning']) < 1.0:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Lightning']) - 1.0) * 100] = "Increase the Absorption from player attacks for Lightning"
            else:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Lightning']) - 1.0) * 100] = "Decrease the Absorption from player attacks for Lightning"
    if (float(specialEffect['PVP Absorption %: Holy']) != 1.0):
        row_dict["pvp_absorption_percent_holy"] = -(float(specialEffect['PVP Absorption %: Holy']) - 1.0)
        if (-(float(specialEffect['PVP Absorption %: Holy']) - 1.0) * 100 in absorption_percent_player_dict):
            absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Holy']) - 1.0) * 100] += ", Holy"
        else:
            if float(specialEffect['PVP Absorption %: Holy']) < 1.0:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Holy']) - 1.0) * 100] = "Increase the Absorption from player attacks for Holy"
            else:
                absorption_percent_player_dict[-(float(specialEffect['PVP Absorption %: Holy']) - 1.0) * 100] = "Decrease the Absorption from player attacks for Holy"
    for key, value in absorption_percent_player_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    # You use this to get the new absorption from armor.
    # An example calculation to get a new physical absorption for armor is found below
    # physical_absorption = -((1 - physical_absorption) * absorption_standard) + 1 
    # Needs Description for talismans
    absorption_percent_all_dict = OrderedDict()
    if (float(specialEffect['Absorption: Standard']) != 1.0):
        row_dict["absorption_standard"] = -(float(specialEffect['Absorption: Standard']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Standard']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Standard']) - 1.0) * 100] += ", Standard"
            else:
                if float(specialEffect['Absorption: Standard']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Standard']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Standard"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Standard']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Standard"
    if (float(specialEffect['Absorption: Strike']) != 1.0):
        row_dict["absorption_strike"] = -(float(specialEffect['Absorption: Strike']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Strike']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Strike']) - 1.0) * 100] += ", Strike"
            else:
                if float(specialEffect['Absorption: Strike']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Strike']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Strike"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Strike']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Strike"
    if (float(specialEffect['Absorption: Slash']) != 1.0):
        row_dict["absorption_slash"] = -(float(specialEffect['Absorption: Slash']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Slash']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Slash']) - 1.0) * 100] += ", Slash"
            else:
                if float(specialEffect['Absorption: Slash']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Slash']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Slash"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Slash']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Slash"
    if (float(specialEffect['Absorption: Thrust']) != 1.0):
        row_dict["absorption_thrust"] = -(float(specialEffect['Absorption: Thrust']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Thrust']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Thrust']) - 1.0) * 100] += ", Thrust"
            else:
                if float(specialEffect['Absorption: Thrust']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Thrust']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Thrust"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Thrust']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Thrust"
    if (float(specialEffect['Absorption: Magic']) != 1.0):
        row_dict["absorption_magic"] = -(float(specialEffect['Absorption: Magic']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Magic']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Magic']) - 1.0) * 100] += ", Magic"
            else:
                if float(specialEffect['Absorption: Magic']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Magic']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Magic"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Magic']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Magic"
    if (float(specialEffect['Absorption: Fire']) != 1.0):
        row_dict["absorption_fire"] = -(float(specialEffect['Absorption: Fire']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Fire']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Fire']) - 1.0) * 100] += ", Fire"
            else:
                if float(specialEffect['Absorption: Fire']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Fire']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Fire"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Fire']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Fire"
    if (float(specialEffect['Absorption: Lightning']) != 1.0):
        row_dict["absorption_lightning"] = -(float(specialEffect['Absorption: Lightning']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Lightning']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Lightning']) - 1.0) * 100] += ", Lightning"
            else:
                if float(specialEffect['Absorption: Lightning']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Lightning']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Lightning"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Lightning']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Lightning"
    if (float(specialEffect['Absorption: Holy']) != 1.0):
        row_dict["absorption_holy"] = -(float(specialEffect['Absorption: Holy']) - 1.0)
        if (not(passiveFromArmor)):
            if (-(float(specialEffect['Absorption: Holy']) - 1.0) * 100 in absorption_percent_all_dict):
                absorption_percent_all_dict[-(float(specialEffect['Absorption: Holy']) - 1.0) * 100] += ", Holy"
            else:
                if float(specialEffect['Absorption: Holy']) < 1.0:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Holy']) - 1.0) * 100] = "Increase the Absorption from all enemy attacks for Holy"
                else:
                    absorption_percent_all_dict[-(float(specialEffect['Absorption: Holy']) - 1.0) * 100] = "Decrease the Absorption from all enemy attacks for Holy"
    for key, value in absorption_percent_all_dict.items():
        descriptionArray.append(value + " types by " + str(abs(round(key, 2))) + "%")

    if (int(specialEffect['Resist: Poison +']) == int(specialEffect['Resist: Scarlet Rot +'])):
        if (int(specialEffect['Resist: Poison +']) != 0):
            row_dict["immunity"] = int(specialEffect['Resist: Poison +'])
            if (int(specialEffect['Resist: Poison +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Poison +']))) + " Immunity")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Poison +']))) + " Immunity")
    else:
        if (int(specialEffect['Resist: Poison +']) != 0):
            row_dict["resist_poison"] = int(specialEffect['Resist: Poison +'])
            if (int(specialEffect['Resist: Poison +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Poison +']))) + " Poison Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Poison +']))) + " Poison Resist")
        if (int(specialEffect['Resist: Scarlet Rot +']) != 0):
            row_dict["resist_rot"] = int(specialEffect['Resist: Scarlet Rot +'])
            if (int(specialEffect['Resist: Scarlet Rot +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Scarlet Rot +']))) + " Scarlet Rot Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Scarlet Rot +']))) + " Scarlet Rot Resist")
    if (int(specialEffect['Resist: Hemorrhage +']) == int(specialEffect['Resist: Frostbite +'])):
        if (int(specialEffect['Resist: Hemorrhage +']) != 0):
            row_dict["robustness"] = int(specialEffect['Resist: Hemorrhage +'])
            if (int(specialEffect['Resist: Hemorrhage +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Hemorrhage +']))) + " Robustness")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Hemorrhage +']))) + " Robustness")
    else:
        if (int(specialEffect['Resist: Hemorrhage +']) != 0):
            row_dict["resist_bleed"] = int(specialEffect['Resist: Hemorrhage +'])
            if (int(specialEffect['Resist: Hemorrhage +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Hemorrhage +']))) + " Bleed Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Hemorrhage +']))) + " Bleed Resist")
        if (int(specialEffect['Resist: Frostbite +']) != 0):
            row_dict["resist_frost"] = int(specialEffect['Resist: Frostbite +'])
            if (int(specialEffect['Resist: Frostbite +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Frostbite +']))) + " Frost Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Frostbite +']))) + " Frost Resist")
    if (int(specialEffect['Resist: Madness +']) == int(specialEffect['Resist: Sleep +'])):
        if (int(specialEffect['Resist: Madness +']) != 0):
            row_dict["focus"] = int(specialEffect['Resist: Madness +'])
            if (int(specialEffect['Resist: Madness +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Madness +']))) + " Focus")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Madness +']))) + " Focus")
    else:
        if (int(specialEffect['Resist: Madness +']) != 0):
            row_dict["resist_madness"] = int(specialEffect['Resist: Madness +'])
            if (int(specialEffect['Resist: Madness +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Madness +']))) + " Madness Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Madness +']))) + " Madness Resist")
        if (int(specialEffect['Resist: Sleep +']) != 0):
            row_dict["resist_sleep"] = int(specialEffect['Resist: Sleep +'])
            if (int(specialEffect['Resist: Sleep +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Sleep +']))) + " Sleep Resist")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Sleep +']))) + " Sleep Resist")
    if (int(specialEffect['Resist: Blight +']) != 0):
        row_dict["vitality"] = int(specialEffect['Resist: Blight +'])
        if (int(specialEffect['Resist: Blight +']) > 0):
            descriptionArray.append("Add " + str(abs(int(specialEffect['Resist: Blight +']))) + " Vitality")
        else:
            descriptionArray.append("Subtract " + str(abs(int(specialEffect['Resist: Blight +']))) + " Vitality")

    if (int(specialEffect['Inflict Poison +']) == int(specialEffect['Inflict Scarlet Rot +'])):
        if (int(specialEffect['Inflict Poison +']) != 0):
            if (int(specialEffect['Inflict Poison +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Poison +']))) + " Poison and Scarlet Rot")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Poison +']))) + " Poison and Scarlet Rot")
    else:
        if (int(specialEffect['Inflict Poison +']) != 0):
            row_dict["inflict_poison"] = int(specialEffect['Inflict Poison +'])
            if (int(specialEffect['Inflict Poison +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Poison +']))) + " Poison")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Poison +']))) + " Poison")
        if (int(specialEffect['Inflict Scarlet Rot +']) != 0):
            row_dict["inflict_rot"] = int(specialEffect['Inflict Scarlet Rot +'])
            if (int(specialEffect['Inflict Scarlet Rot +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Scarlet Rot +']))) + " Scarlet Rot")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Scarlet Rot +']))) + " Scarlet Rot")
    if (int(specialEffect['Inflict Hemorrhage +']) == int(specialEffect['Inflict Frostbite +'])):
        if (int(specialEffect['Inflict Hemorrhage +']) != 0):
            row_dict["inflict_robustness"] = int(specialEffect['Inflict Hemorrhage +'])
            if (int(specialEffect['Inflict Hemorrhage +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Hemorrhage +']))) + " Bleed and Frost")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Hemorrhage +']))) + " Bleed and Frost")
    else:
        if (int(specialEffect['Inflict Hemorrhage +']) != 0):
            row_dict["inflict_bleed"] = int(specialEffect['Inflict Hemorrhage +'])
            if (int(specialEffect['Inflict Hemorrhage +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Hemorrhage +']))) + " Bleed")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Hemorrhage +']))) + " Bleed")
        if (int(specialEffect['Inflict Frostbite +']) != 0):
            row_dict["inflict_frost"] = int(specialEffect['Inflict Frostbite +'])
            if (int(specialEffect['Inflict Frostbite +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Frostbite +']))) + " Frost")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Frostbite +']))) + " Frost")
    if (int(specialEffect['Inflict Madness +']) == int(specialEffect['Inflict Sleep +'])):
        if (int(specialEffect['Inflict Madness +']) != 0):
            row_dict["inflict_focus"] = int(specialEffect['Inflict Madness +'])
            if (int(specialEffect['Inflict Madness +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Madness +']))) + " Madness and Sleep")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Madness +']))) + " Madness and Sleep")
    else:
        if (int(specialEffect['Inflict Madness +']) != 0):
            row_dict["inflict_madness"] = int(specialEffect['Inflict Madness +'])
            if (int(specialEffect['Inflict Madness +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Madness +']))) + " Madness")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Madness +']))) + " Madness")
        if (int(specialEffect['Inflict Sleep +']) != 0):
            row_dict["inflict_sleep"] = int(specialEffect['Inflict Sleep +'])
            if (int(specialEffect['Inflict Sleep +']) > 0):
                descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Sleep +']))) + " Sleep")
            else:
                descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Sleep +']))) + " Sleep")
    if (int(specialEffect['Inflict Blight +']) != 0):
        row_dict["inflict_vitality"] = int(specialEffect['Inflict Blight +'])
        if (int(specialEffect['Inflict Blight +']) > 0):
            descriptionArray.append("Inflict " + str(abs(int(specialEffect['Inflict Blight +']))) + " Blight")
        else:
            descriptionArray.append("Restore " + str(abs(int(specialEffect['Inflict Blight +']))) + " Blight")


    if (float(specialEffect['Resist %: Poison']) == float(specialEffect['Resist %: Scarlet Rot'])):
        if (float(specialEffect['Resist %: Poison']) != 1.0):
            row_dict["resist_percent_immunity"] = float(specialEffect['Resist %: Poison'])
            if float(specialEffect['Resist %: Poison']) > 1.0:
                descriptionArray.append("Increase Immunity by " + str(round(abs((float(specialEffect['Resist %: Poison']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Immunity by " + str(round(abs((float(specialEffect['Resist %: Poison']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Resist %: Poison']) != 1.0):
            row_dict["resist_percent_poison"] = float(specialEffect['Resist %: Poison'])
            if float(specialEffect['Resist %: Poison']) > 1.0:
                descriptionArray.append("Increase Poison Resist by " + str(round(abs((float(specialEffect['Resist %: Poison']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Poison Resist by " + str(round(abs((float(specialEffect['Resist %: Poison']) - 1.0) * 100), 2)) + "%")
        if (float(specialEffect['Resist %: Scarlet Rot']) != 1.0):
            row_dict["resist_percent_rot"] = float(specialEffect['Resist %: Scarlet Rot'])
            if float(specialEffect['Resist %: Scarlet Rot']) > 1.0:
                descriptionArray.append("Increase Scarlet Rot Resist by " + str(round(abs((float(specialEffect['Resist %: Scarlet Rot']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Scarlet Rot Resist by " + str(round(abs((float(specialEffect['Resist %: Scarlet Rot']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Resist %: Hemorrhage']) == float(specialEffect['Resist %: Frostbite'])):
        if (float(specialEffect['Resist %: Hemorrhage']) != 1.0):
            row_dict["resist_percent_robustness"] = float(specialEffect['Resist %: Hemorrhage'])
            if float(specialEffect['Resist %: Hemorrhage']) > 1.0:
                descriptionArray.append("Increase Robustness by " + str(round(abs((float(specialEffect['Resist %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Robustness by " + str(round(abs((float(specialEffect['Resist %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Resist %: Hemorrhage']) != 1.0):
            row_dict["resist_percent_bleed"] = float(specialEffect['Resist %: Hemorrhage'])
            if float(specialEffect['Resist %: Hemorrhage']) > 1.0:
                descriptionArray.append("Increase Bleed Resist by " + str(round(abs((float(specialEffect['Resist %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Bleed Resist by " + str(round(abs((float(specialEffect['Resist %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
        if (float(specialEffect['Resist %: Frostbite']) != 1.0):
            row_dict["resist_percent_frost"] = float(specialEffect['Resist %: Frostbite'])
            if float(specialEffect['Resist %: Frostbite']) > 1.0:
                descriptionArray.append("Increase Frost Resist by " + str(round(abs((float(specialEffect['Resist %: Frostbite']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Frost Resist by " + str(round(abs((float(specialEffect['Resist %: Frostbite']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Resist %: Madness']) == float(specialEffect['Resist %: Sleep'])):
        if (float(specialEffect['Resist %: Sleep']) != 1.0):
            row_dict["resist_percent_focus"] = float(specialEffect['Resist %: Sleep'])
            if float(specialEffect['Resist %: Sleep']) > 1.0:
                descriptionArray.append("Increase Focus by " + str(round(abs((float(specialEffect['Resist %: Sleep']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Focus by " + str(round(abs((float(specialEffect['Resist %: Sleep']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Resist %: Madness']) != 1.0):
            row_dict["resist_percent_madness"] = float(specialEffect['Resist %: Madness'])
            if float(specialEffect['Resist %: Madness']) > 1.0:
                descriptionArray.append("Increase Madness Resist by " + str(round(abs((float(specialEffect['Resist %: Madness']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Madness Resist by " + str(round(abs((float(specialEffect['Resist %: Madness']) - 1.0) * 100), 2)) + "%")
        if (float(specialEffect['Resist %: Sleep']) != 1.0):
            row_dict["resist_percent_sleep"] = float(specialEffect['Resist %: Sleep'])
            if float(specialEffect['Resist %: Sleep']) > 1.0:
                descriptionArray.append("Increase Sleep Resist by " + str(round(abs((float(specialEffect['Resist %: Sleep']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease Sleep Resist by " + str(round(abs((float(specialEffect['Resist %: Sleep']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Resist %: Blight']) != 1.0):
        row_dict["resist_percent_vitality"] = float(specialEffect['Resist %: Blight'])
        if float(specialEffect['Resist %: Blight']) > 1.0:
            descriptionArray.append("Increase Vitality by " + str(round(abs((float(specialEffect['Resist %: Blight']) - 1.0) * 100), 2)) + "%")
        else:
            descriptionArray.append("Decrease Vitality by " + str(round(abs((float(specialEffect['Resist %: Blight']) - 1.0) * 100), 2)) + "%")

    if (float(specialEffect['Status Damage %: Poison']) == float(specialEffect['Status Damage %: Scarlet Rot'])):
        if (float(specialEffect['Status Damage %: Poison']) != 1.0):
            row_dict["status_damage_percent_immunity"] = float(specialEffect['Status Damage %: Poison'])
            if float(specialEffect['Status Damage %: Poison']) > 1.0:
                descriptionArray.append("Increase status damage Poison and Scarlet Rot by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Poison']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Poison and Scarlet Rot by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Poison']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Status Damage %: Poison']) != 1.0):
            row_dict["status_damage_percent_poison"] = float(specialEffect['Status Damage %: Poison'])
            if float(specialEffect['Status Damage %: Poison']) > 1.0:
                descriptionArray.append("Increase status damage Poison by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Poison']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Poison by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Poison']) - 1.0) * 100, 2))) + "%")
        if (float(specialEffect['Status Damage %: Scarlet Rot']) != 1.0):
            row_dict["status_damage_percent_rot"] = float(specialEffect['Status Damage %: Scarlet Rot'])
            if float(specialEffect['Status Damage %: Scarlet Rot']) > 1.0:
                descriptionArray.append("Increase status damage Scarlet Rot by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Scarlet Rot']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Scarlet Rot by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Scarlet Rot']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Status Damage %: Hemorrhage']) == float(specialEffect['Status Damage %: Frostbite'])):
        if (float(specialEffect['Status Damage %: Hemorrhage']) != 1.0):
            row_dict["status_damage_percent_robustness"] = float(specialEffect['Status Damage %: Hemorrhage'])
            if float(specialEffect['Status Damage %: Hemorrhage']) > 1.0:
                descriptionArray.append("Increase status damage Bleed and Frost by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Bleed and Frost by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Status Damage %: Hemorrhage']) != 1.0):
            row_dict["status_damage_percent_bleed"] = float(specialEffect['Status Damage %: Hemorrhage'])
            if float(specialEffect['Status Damage %: Hemorrhage']) > 1.0:
                descriptionArray.append("Increase status damage Bleed by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Bleed by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Hemorrhage']) - 1.0) * 100), 2)) + "%")
        if (float(specialEffect['Status Damage %: Frostbite']) != 1.0):
            row_dict["status_damage_percent_frost"] = float(specialEffect['Status Damage %: Frostbite'])
            if float(specialEffect['Status Damage %: Frostbite']) > 1.0:
                descriptionArray.append("Increase status damage Frost by " + str
                    (round(abs((float(specialEffect['Status Damage %: Frostbite']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Frost by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Frostbite']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Status Damage %: Madness']) == float(specialEffect['Status Damage %: Sleep'])):
        if (float(specialEffect['Status Damage %: Sleep']) != 1.0):
            row_dict["status_damage_percent_focus"] = float(specialEffect['Status Damage %: Sleep'])
            if float(specialEffect['Status Damage %: Sleep']) > 1.0:
                descriptionArray.append("Increase status damage Sleep and Madness by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Sleep']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Sleep and Madness by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Sleep']) - 1.0) * 100), 2)) + "%")
    else:
        if (float(specialEffect['Status Damage %: Madness']) != 1.0):
            row_dict["status_damage_percent_madness"] = float(specialEffect['Status Damage %: Madness'])
            if float(specialEffect['Status Damage %: Madness']) > 1.0:
                descriptionArray.append("Increase status damage Madness by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Madness']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Madness by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Madness']) - 1.0) * 100), 2)) + "%")
        if (float(specialEffect['Status Damage %: Sleep']) != 1.0):
            row_dict["status_damage_percent_sleep"] = float(specialEffect['Status Damage %: Sleep'])
            if float(specialEffect['Status Damage %: Sleep']) > 1.0:
                descriptionArray.append("Increase status damage Sleep by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Sleep']) - 1.0) * 100), 2)) + "%")
            else:
                descriptionArray.append("Decrease status damage Sleep by " + 
                    str(round(abs((float(specialEffect['Status Damage %: Sleep']) - 1.0) * 100), 2)) + "%")
    if (float(specialEffect['Status Damage %: Blight']) != 1.0):
        row_dict["status_damage_percent_vitality"] = float(specialEffect['Status Damage %: Blight'])
        if float(specialEffect['Status Damage %: Blight']) > 1.0:
            descriptionArray.append("Increase status damage Blight by " + str(round(abs((float(specialEffect['Status Damage %: Blight']) - 1.0) * 100), 2)) + "%")
        else:
            descriptionArray.append("Decrease status damage Blight by " + str(round(abs((float(specialEffect['Status Damage %: Blight']) - 1.0) * 100), 2)) + "%")

    if (float(specialEffect['Target Priority']) != 0.0):
        row_dict["target_priority_percentage"] = float(specialEffect['Target Priority'])
        if (float(specialEffect['Target Priority']) > 0.0):
            descriptionArray.append("Increase attraction of enemies by " + str(round(abs(float(specialEffect['Target Priority']) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease attraction of enemies by " + str(round(abs(float(specialEffect['Target Priority']) * 100.0), 2)) + "%")
    if (float(specialEffect['Enemy Listen Adjustment']) != 1.0):
        row_dict["enemy_listen_adjustment_percentage"] = float(specialEffect['Enemy Listen Adjustment']) - 1.0
        if (float(specialEffect['Enemy Listen Adjustment']) > 1.0):
            descriptionArray.append("Increase sound emmitted to all enemies by " + str(round(abs((float(specialEffect['Enemy Listen Adjustment']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease sound emmitted to all enemies by " + str(round(abs((float(specialEffect['Enemy Listen Adjustment']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Max HP']) != 1.0):
        if (float(specialEffect['Max HP']) > 1.0):
            descriptionArray.append("Increase Max HP by " + str(round(abs((float(specialEffect['Max HP']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max HP by " + str(round(abs((float(specialEffect['Max HP']) - 1.0) * 100.0), 2)) + "%")
        row_dict["max_hp_percentage"] = float(specialEffect['Max HP']) - 1.0
    if (float(specialEffect['Max FP']) != 1.0):
        row_dict["max_fp_percentage"] = float(specialEffect['Max FP']) - 1.0
        if (float(specialEffect['Max FP']) > 1.0):
            descriptionArray.append("Increase Max FP by " + str(round(abs((float(specialEffect['Max FP']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max FP by " + str(round(abs((float(specialEffect['Max FP']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Max Stamina']) != 1.0):
        row_dict["max_stamina_percentage"] = float(specialEffect['Max Stamina']) - 1.0
        if (float(specialEffect['Max Stamina']) > 1.0):
            descriptionArray.append("Increase Max Stamina by " + str(round(abs((float(specialEffect['Max Stamina']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max Stamina by " + str(round(abs((float(specialEffect['Max Stamina']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Poise %']) != 1.0):
        row_dict["poise_percentage"] = -(float(specialEffect['Poise %']) - 1.0)
        if (-(float(specialEffect['Poise %']) - 1.0) > 0.0):
            descriptionArray.append("Increase Poise by " + str(round(abs((float(specialEffect['Poise %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Poise by " + str(round(abs((float(specialEffect['Poise %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Poise +']) != 0.0):
        row_dict["poise"] = float(specialEffect['Poise +'])
        if (float(specialEffect['Poise +']) > 0.0):
            descriptionArray.append("Add Poise by " + str(round(abs(float(specialEffect['Poise +'])), 2)))
        else:
            descriptionArray.append("Subtract Poise by " + str(round(abs(float(specialEffect['Poise +'])), 2)))
    if (float(specialEffect['Fall Damage %']) != 1.0):
        row_dict["fall_damage_percentage"] = float(specialEffect['Fall Damage %']) - 1.0
        if (float(specialEffect['Fall Damage %']) > 1.0):
            descriptionArray.append("Increase Fall Damage taken by " + str(round(abs((float(specialEffect['Fall Damage %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Fall Damage taken by " + str(round(abs((float(specialEffect['Fall Damage %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Equip Load %']) != 1.0):
        row_dict["equip_load_percentage"] = float(specialEffect['Equip Load %']) - 1.0
        if (float(specialEffect['Equip Load %']) > 1.0):
            descriptionArray.append("Increase Equip Load by " + str(round(abs((float(specialEffect['Equip Load %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Equip Load by " + str(round(abs((float(specialEffect['Equip Load %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Effect Duration %']) != 1.0):
        row_dict["effect_duration_percentage"] = float(specialEffect['Effect Duration %']) - 1.0
        if (float(specialEffect['Effect Duration %']) > 1.0):
            descriptionArray.append("Increase Effect Duration by " + str(round(abs((float(specialEffect['Effect Duration %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Effect Duration by " + str(round(abs((float(specialEffect['Effect Duration %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Extend SpEffect Duration %']) != 1.0):
        row_dict["Extend SpEffect Duration %"] = float(specialEffect['Extend SpEffect Duration %']) - 1.0
        if (float(specialEffect['Extend SpEffect Duration %']) > 1.0):
            descriptionArray.append("Extend Special Effect Duration by " + 
                str(round(abs((float(specialEffect['Extend SpEffect Duration %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Contract Special Effect Duration by " + 
                str(round(abs((float(specialEffect['Extend SpEffect Duration %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Contract SpEffect Duration %']) != 1.0):
        row_dict["Contract SpEffect Duration %"] = float(specialEffect['Contract SpEffect Duration %']) - 1.0
        if (float(specialEffect['Contract SpEffect Duration %']) > 1.0):
            descriptionArray.append("Contract Special Effect Duration by " + 
                str(round(abs((float(specialEffect['Contract SpEffect Duration %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Extend Special Effect Duration by " + 
                str(round(abs((float(specialEffect['Contract SpEffect Duration %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Guard Stability %']) != 1.0):
        row_dict["guard_stability_percentage"] = float(specialEffect['Guard Stability %']) - 1.0
        if (float(specialEffect['Guard Stability %']) > 1.0):
            descriptionArray.append("Increase Guard Stability by " + str(round(abs((float(specialEffect['Guard Stability %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Guard Stability by " + str(round(abs((float(specialEffect['Guard Stability %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Attack %: Stamina']) != 1.0):
        row_dict["guard_break_percentage"] = float(specialEffect['Attack %: Stamina']) - 1.0
        if (float(specialEffect['Attack %: Stamina']) > 1.0):
            descriptionArray.append("Increase Guard Break by " + str(round(abs((float(specialEffect['Attack %: Stamina']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Guard Break by " + str(round(abs((float(specialEffect['Attack %: Stamina']) - 1.0) * 100.0), 2)) + "%")
    if (int(specialEffect['Rune Gain +']) != 0):
        row_dict["rune_gain"] = int(specialEffect['Rune Gain +'])
        if (int(specialEffect['Rune Gain +']) > 0.0):
            descriptionArray.append("Add Rune by " + str(round(abs(int(specialEffect['Rune Gain +'])), 2)))
        else:
            descriptionArray.append("Subtract Rune by " + str(round(abs(int(specialEffect['Rune Gain +'])), 2)))
    if (float(specialEffect['Rune Gain %']) != 1.0):
        row_dict["rune_gain_percentage"] = float(specialEffect['Rune Gain %']) - 1.0
        if (float(specialEffect['Rune Gain %']) > 1.0):
            descriptionArray.append("Increase Runes Gained by " + str(round(abs((float(specialEffect['Rune Gain %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Runes Gained by " + str(round(abs((float(specialEffect['Rune Gain %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Item Discovery %']) != 0.0):
        row_dict["item_discovery"] = int(float(specialEffect['Item Discovery %']) * 100.0)
        if (float(specialEffect['Item Discovery %']) > 0.0):
            descriptionArray.append("Add Item Discovery by " + str(round(abs(int(float(specialEffect['Item Discovery %']) * 100.0)), 2)))
        else:
            descriptionArray.append("Add Item Discovery by " + str(round(abs(int(float(specialEffect['Item Discovery %']) * 100.0)), 2)))
    if (float(specialEffect['HP Flask - HP Restore Correction']) != 1.0):
        row_dict["hp_restore_correction_percentage"] = float(specialEffect['HP Flask - HP Restore Correction']) - 1.0
        if (float(specialEffect['HP Flask - HP Restore Correction']) > 1.0):
            descriptionArray.append("Increase HP Restore from Flask of Crimson Tears by " + 
                str(round(abs((float(specialEffect['HP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease HP Restore from Flask of Crimson Tears by " + 
                str(round(abs((float(specialEffect['HP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['FP Flask - HP Restore Correction']) != 1.0):
        row_dict["fp_restore_correction_percentage"] = float(specialEffect['FP Flask - HP Restore Correction']) - 1.0
        if (float(specialEffect['FP Flask - HP Restore Correction']) > 1.0):
            descriptionArray.append("Increase FP Restore from Flask of Cerulean Tears by " + 
                str(round(abs((float(specialEffect['FP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Restore from Flask of Cerulean Tears by " + 
                str(round(abs((float(specialEffect['FP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Skill FP Cost %']) != 1.0):
        row_dict["skill_fp_cost_percentage"] = float(specialEffect['Skill FP Cost %']) - 1.0
        if (float(specialEffect['Skill FP Cost %']) > 1.0):
            descriptionArray.append("Increase FP Cost for Skill by " + str(round(abs((float(specialEffect['Skill FP Cost %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Cost for Skill by " + str(round(abs((float(specialEffect['Skill FP Cost %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Sorcery FP Cost %']) != 1.0):
        row_dict["sorcery_fp_cost_percentage"] = float(specialEffect['Sorcery FP Cost %']) - 1.0
        if (float(specialEffect['Sorcery FP Cost %']) > 1.0):
            descriptionArray.append("Increase FP Cost for Sorcery by " + str(round(abs((float(specialEffect['Sorcery FP Cost %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Cost for Sorcery by " + str(round(abs((float(specialEffect['Sorcery FP Cost %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Incantation FP Cost %']) != 1.0):
        row_dict["incantation_fp_cost_percentage"] = float(specialEffect['Incantation FP Cost %']) - 1.0  
        if (float(specialEffect['Incantation FP Cost %']) > 1.0):
            descriptionArray.append("Increase FP Cost for Incantation by " + 
                str(round(abs((float(specialEffect['Incantation FP Cost %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Cost for Incantation by " + 
                str(round(abs((float(specialEffect['Incantation FP Cost %']) - 1.0) * 100.0), 2)) + "%")
    if (int(specialEffect['Cast Speed']) != 0):
        row_dict["cast_speed"] = int(specialEffect['Cast Speed'])
        if (int(specialEffect['Cast Speed']) > 0):
            descriptionArray.append("Add " + str(abs(int(specialEffect['Cast Speed']))) + " to Cast Speed Value")
        else:
            descriptionArray.append("Subtract " + str(abs(int(specialEffect['Cast Speed']))) + " to Cast Speed Value")
    if (int(specialEffect['Memory Slot']) != 0):
        row_dict["memory_slot"] = int(specialEffect['Memory Slot'])
        if (int(specialEffect['Memory Slot']) > 0):
            descriptionArray.append("Add " + str(abs(int(specialEffect['Memory Slot']))) + " Memory Slots")
        else:
            descriptionArray.append("Subtract " + str(abs(int(specialEffect['Memory Slot']))) + " to Memory Slots")
    if (int(specialEffect['Bow Distance']) != 0):
        row_dict["bow_distance"] = int(specialEffect['Bow Distance'])
        if (int(specialEffect['Bow Distance']) > 0):
            descriptionArray.append("Add " + str(abs(int(specialEffect['Bow Distance']))) + " to Bow Distance")
        else:
            descriptionArray.append("Subtract " + str(abs(int(specialEffect['Bow Distance']))) + " to Bow Distance")

        
    # Doesn't need description yet as I don't see any passives that currently use this yet.
    # Will add description if used though
    if (float(specialEffect['Enemy Sight Adjustment']) != 1.0):
        row_dict["enemy_sight_adjustment_percentage"] = float(specialEffect['Enemy Sight Adjustment']) - 1.0
    if (float(specialEffect['Sight Search - Enemy Addition']) != 0.0):
        row_dict["sight_search_enemy_addition_percentage"] = float(specialEffect['Sight Search - Enemy Addition'])
    if (float(specialEffect['Listen Search - Enemy Addition']) != 0.0):
        row_dict["listen_search_enemy_addition_percentage"] = float(specialEffect['Listen Search - Enemy Addition'])
    if (float(specialEffect['Listen Search Correction']) != 1.0):
        row_dict["listen_search_correction_percentage"] = float(specialEffect['Listen Search Correction']) - 1.0
    if (float(specialEffect['Listen Search Addition']) != 0.0):
        row_dict["listen_search_addition_percentage"] = float(specialEffect['Listen Search Addition'])
    if (float(specialEffect['Sight Search Addition']) != 0.0):
        row_dict["sight_search_addition_percentage"] = float(specialEffect['Sight Search Addition'])
    if (float(specialEffect['No Guard Damage %']) != 1.0):
        row_dict["no_guard_damage_percentage"] = float(specialEffect['No Guard Damage %']) - 1.0
    if (float(specialEffect['Vital Spot Change %']) != -1.0):
        row_dict["vital_spot_change_percentage"] = float(specialEffect['Vital Spot Change %'])
    if (float(specialEffect['Normal Spot Change %']) != -1.0):
        row_dict["normal_spot_change_percentage"] = float(specialEffect['Normal Spot Change %'])
    if (float(specialEffect['Look-At Target Position Offset']) != 0.0):
        row_dict["look_at_target_position_offset"] = float(specialEffect['Look-At Target Position Offset'])
    if (float(specialEffect['Poise Recovery Time %']) != 1.0):
        row_dict["poise_recovery_time_percentage"] = float(specialEffect['Poise Recovery Time %']) - 1.0
    if (float(specialEffect['Regain Correction %']) != 1.0):
        row_dict["regain_correction_percentage"] = float(specialEffect['Regain Correction %']) - 1.0
    if (float(specialEffect['Poise Damage %']) != 1.0):
        row_dict["poise_damage_percentage"] = float(specialEffect['Poise Damage %']) - 1.0

    if (int(specialEffect['Vigor']) != 0):
        row_dict["vigor"] = int(specialEffect['Vigor'])
        if (int(specialEffect['Vigor']) > 0):
            descriptionArray.append("Increase Vigor by " + specialEffect['Vigor'])
        else:
            descriptionArray.append("Decrease Vigor by " + specialEffect['Vigor'])
    if (int(specialEffect['Mind']) != 0):
        row_dict["mind"] = int(specialEffect['Mind'])
        if (int(specialEffect['Mind']) > 0):
            descriptionArray.append("Increase Mind by " + specialEffect['Mind'])
        else:
            descriptionArray.append("Decrease Mind by " + specialEffect['Mind'])
    if (int(specialEffect['Endurance']) != 0):
        row_dict["endurance"] = int(specialEffect['Endurance'])
        if (int(specialEffect['Endurance']) > 0):
            descriptionArray.append("Increase Endurance by " + specialEffect['Endurance'])
        else:
            descriptionArray.append("Decrease Endurance by " + specialEffect['Endurance'])
    if (int(specialEffect['Strength']) != 0):
        row_dict["strength"] = int(specialEffect['Strength'])
        if (int(specialEffect['Strength']) > 0):
            descriptionArray.append("Increase Strength by " + specialEffect['Strength'])
        else:
            descriptionArray.append("Decrease Strength by " + specialEffect['Strength'])
    if (int(specialEffect['Dexterity']) != 0):
        row_dict["dexterity"] = int(specialEffect['Dexterity'])
        if (int(specialEffect['Dexterity']) > 0):
            descriptionArray.append("Increase Dexterity by " + specialEffect['Dexterity'])
        else:
            descriptionArray.append("Decrease Dexterity by " + specialEffect['Dexterity'])
    if (int(specialEffect['Intelligence']) != 0):
        row_dict["intelligence"] = int(specialEffect['Intelligence'])
        if (int(specialEffect['Intelligence']) > 0):
            descriptionArray.append("Increase Intelligence by " + specialEffect['Intelligence'])
        else:
            descriptionArray.append("Decrease Intelligence by " + specialEffect['Intelligence'])
    if (int(specialEffect['Faith']) != 0):
        row_dict["faith"] = int(specialEffect['Faith'])
        if (int(specialEffect['Faith']) > 0):
            descriptionArray.append("Increase Faith by " + specialEffect['Faith'])
        else:
            descriptionArray.append("Decrease Faith by " + specialEffect['Faith'])
    if (int(specialEffect['Arcane']) != 0):
        row_dict["arcane"] = int(specialEffect['Arcane'])
        if (int(specialEffect['Arcane']) > 0):
            descriptionArray.append("Increase Arcane by " + specialEffect['Arcane'])
        else:
            descriptionArray.append("Decrease Arcane by " + specialEffect['Arcane'])

    if (int(specialEffect['Change HP +']) != 0):
        row_dict["change_hp"] = -int(specialEffect['Change HP +'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-int(specialEffect['Change HP +']) > 0):
                descriptionArray.append("Regen HP by " + str(abs(int(specialEffect['Change HP +']))) + " points per second")
            else:
                descriptionArray.append("Drain HP by " + str(abs(int(specialEffect['Change HP +']))) + " points per second")
        else:
            if (not(checkStringState("Poison", row_dict)) and not(checkStringState("Scarlet Rot", row_dict))):
                if (-int(specialEffect['Change HP +']) > 0):
                    descriptionArray.append("Add " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
                else:
                    descriptionArray.append("Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")

    if (int(specialEffect['Change FP +']) != 0):
        row_dict["change_fp"] = -int(specialEffect['Change FP +'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-int(specialEffect['Change FP +']) > 0):
                descriptionArray.append("Regen FP by " + str(abs(int(specialEffect['Change FP +']))) + " points per second")
            else:
                descriptionArray.append("Drain FP by " + str(abs(int(specialEffect['Change FP +']))) + " points per second")
        else:
            if (-int(specialEffect['Change FP +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
    if (int(specialEffect['Change Stamina +']) != 0):
        row_dict["change_stamina"] = -int(specialEffect['Change Stamina +'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-int(specialEffect['Change Stamina +']) > 0):
                descriptionArray.append("Regen Stamina by " + str(abs(int(specialEffect['Change Stamina +']))) + " points per second")
            else:
                descriptionArray.append("Drain Stamina by " + str(abs(int(specialEffect['Change Stamina +']))) + " points per second")
        else:
            if (-int(specialEffect['Change Stamina +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
            else:
                descriptionArray.append("Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
    if (float(specialEffect['Change HP %']) != 0):
        row_dict["change_hp_percentage"] = -float(specialEffect['Change HP %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change HP %']) > 0.0):
                descriptionArray.append("Regen HP by " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain HP by " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% per second")
        else:
            if (not(checkStringState("Poison", row_dict)) and not(checkStringState("Scarlet Rot", row_dict))):
                if (-float(specialEffect['Change HP %']) > 0.0):
                    descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% HP")
                else:
                    descriptionArray.append("Subtract " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% HP")
    if (float(specialEffect['Change FP %']) != 0):
        row_dict["change_fp_percentage"] = -float(specialEffect['Change FP %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change FP %']) > 0.0):
                descriptionArray.append("Regen FP by " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain FP by " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% per second")
        else:
            if (-float(specialEffect['Change FP %']) > 0.0):
                descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% FP")
            else:
                descriptionArray.append("Subtract " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% FP")
    if (float(specialEffect['Change Stamina %']) != 0):
        row_dict["change_stamina_percentage"] = -float(specialEffect['Change Stamina %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change Stamina %']) > 0.0):
                descriptionArray.append("Regen Stamina by " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain Stamina by " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% per second")
        else:
            if (-float(specialEffect['Change Stamina %']) > 0.0):
                descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% Stamina")
            else:
                descriptionArray.append("Subtract " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% Stamina")
    if (int(specialEffect['FP Recovery']) != 0):
        row_dict["fp_recovery"] = int(specialEffect['FP Recovery'])
        if (int(specialEffect['FP Recovery']) > 0):
            descriptionArray.append("Increase FP Recovery by " + specialEffect['FP Recovery'] + " points per second")
        else:
            descriptionArray.append("Decrease FP Recovery by " + specialEffect['FP Recovery'] + " points per second")
    if (int(specialEffect['Stamina Recovery']) != 0):
        row_dict["stamina_recovery"] = int(specialEffect['Stamina Recovery'])
        if (int(specialEffect['Stamina Recovery']) > 0):
            descriptionArray.append("Increase Stamina Recovery by " + specialEffect['Stamina Recovery'] + " points per second")
        else:
            descriptionArray.append("Decrease Stamina Recovery by " + specialEffect['Stamina Recovery'] + " points per second")

    getPassiveEffectVfx(row_dict, specialEffectId, descriptionArray)


    # This is a hard code. Nothing I can find currently to indicated parameters
    if (row_dict["name"] == "Torch Effect"):
        descriptionArray.append("Illuminate dark locations")
    if (row_dict["name"] == "Sentry's Torch - Effect"):
        descriptionArray.append("Reveal Invisible Enemies")

    if (checkStringAllStates("Destroy Accessory but Save Runes", row_dict)):
        descriptionArray.append("Destroy Talisman but Save Runes")

    if (checkStringAllStates("Trigger on Crouch", row_dict)):
        descriptionArray.append("Trigger Effect when Crouching")

    if (checkStringAllStates("Reduce Headshot Impact", row_dict)):
        descriptionArray.append("Reduce Headshot Impact")

    if (checkStringAllStates("Pacify Wild Animals", row_dict)):
        descriptionArray.append("Pacify Wild Animals")

    if (checkStringAllStates("Left Hand Buff VFX", row_dict)):
        descriptionArray.append("Increase Guard Boost scaling it based on innate Guard Boost. Lower innate Guard Boost increases scaling.")
    
    if (checkStringAllStates("Extend Roll Invinsibility", row_dict)):
        descriptionArray.append("Extend Roll Invinsibility Frames")

    if (checkStringAllStates("Scale Attack Power with Equip Load", row_dict)):
        descriptionArray.append("Scale Attack Power Increase based on innate Equip Load. Lower innate Equip Load increases scaling.")

    if (checkStringAllStates("Trigger during Critical Hit", row_dict)):
        descriptionArray.append("Trigger only when taking a Critical Hit")

    if (checkStringAllStates("Trigger in Presence of Blood Loss", row_dict)):
        descriptionArray.append("Trigger in Presence of Blood Loss")

    if (checkStringAllStates("Trigger in Presence of Rot", row_dict)):
        descriptionArray.append("Trigger in Presence of Rot")

    if (checkStringAllStates("Madness", row_dict)):
        descriptionArray.append("Trigger in Presence of Madness")

    if (checkStringAllStates("Trigger on Roll", row_dict)):
        descriptionArray.append("Trigger Effect on Roll")

    if (checkStringAllStates("Enhance Thrusting Counter Attacks", row_dict)):
        descriptionArray.append("Only Apply to Thrusting Counter Attacks")

    if (checkStringAllStates("Enhance Critical Attacks", row_dict)):
        descriptionArray.append("Only Apply to Critical Attacks")

    if (int(specialEffect['Trigger at HP Below %']) != -1):
        row_dict["trigger_below_hp_percentage"] = int(specialEffect['Trigger at HP Below %'])
        descriptionArray.append("Trigger Effect when HP is below or equal to " + str(int(specialEffect['Trigger at HP Below %'])) + "%")
    if (int(specialEffect['Trigger on HP Above %']) != -1):
        row_dict["trigger_above_hp_percentage"] = int(specialEffect['Trigger on HP Above %'])
        descriptionArray.append("Trigger Effect when HP is above or equal to " + str(int(specialEffect['Trigger on HP Above %'])) + "%")


    if (specialEffect['Trigger for Opponent'] == InputBoolean.TRUE.value):
        row_dict["trigger_effect_for_opponent"] = InputBoolean.TRUE.value
    if (specialEffect['Trigger for Self'] == InputBoolean.FALSE.value):
        row_dict["trigger_effect_for_self"] = InputBoolean.FALSE.value
        if (specialEffect['Trigger for Friendly'] == InputBoolean.TRUE.value):
            row_dict["trigger_effect_for_friendly"] = InputBoolean.TRUE.value
            descriptionArray.append("Effect is not Triggered on Self but on Friendlies")

    if (specialEffect['Affects Sorcery'] == InputBoolean.TRUE.value):
        row_dict["affects_sorcery"] = InputBoolean.TRUE.value
        if (checkStringAllStates("Spell Power Boost", row_dict)):
            descriptionArray.append("Effect only gives Boost to Sorceries")
        else:
            descriptionArray.append("Affect Sorceries")
    if (specialEffect['Affects Incantation'] == InputBoolean.TRUE.value):
        row_dict["affects_incantation"] = InputBoolean.TRUE.value
        if (checkStringAllStates("Spell Power Boost", row_dict)):
            descriptionArray.append("Effect only gives Boost to Incantations")
        else:
            descriptionArray.append("Affect Incantations")
    
    if (float(specialEffect['Trigger Interval']) != 0.0):
        row_dict["trigger_interval"] = float(specialEffect['Trigger Interval'])
        if not(checkStringAllStates("Trigger", row_dict)):
            if (descriptionArray != [] and float(specialEffect['Duration']) == -1.0) and float(specialEffect['Trigger Interval']) != 0.06 and \
                float(specialEffect['Trigger Interval']) != 0.01:
                if (float(specialEffect['Trigger Interval']) == 1.0):
                    descriptionArray.append("Effect is triggered every second")
                else:
                    descriptionArray.append("Effect is triggered every " + str(round(abs((float(specialEffect['Trigger Interval']))), 2)) + " seconds")

    if checkStringState("Trigger on Critical Hit", row_dict):
        descriptionArray.append("When Enemy Takes a Critical Hit")
        row_dict["trigger_special_effect"] = getPassiveEffect(SpEffectParam[str(int(specialEffectId) + 1)], str(int(specialEffectId) + 1), False)
        if (row_dict["trigger_special_effect"]["description"] != ""):
            for value in row_dict["trigger_special_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["trigger_special_effect"].pop("description")

    if (int(specialEffect['Chain SpEffect ID']) != -1):
        row_dict["chain_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Chain SpEffect ID']], specialEffect['Chain SpEffect ID'], False)
        if (row_dict["chain_special_effect"]["description"] != ""):
            for value in row_dict["chain_special_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["chain_special_effect"].pop("description")

    if (int(specialEffect['Cycle SpEffect ID']) != -1):
        row_dict["cycle_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Cycle SpEffect ID']], specialEffect['Cycle SpEffect ID'], False)
        if (row_dict["cycle_special_effect"]["description"] != ""):
            for value in row_dict["cycle_special_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["cycle_special_effect"].pop("description")
    
    if (int(specialEffect['Attack SpEffect ID']) != -1):
        descriptionArray.append("When Enemy is Hit")
        row_dict["attack_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Attack SpEffect ID']], specialEffect['Attack SpEffect ID'], False)
        if (row_dict["attack_special_effect"]["description"] != ""):
            for value in row_dict["attack_special_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["attack_special_effect"].pop("description")

    if (int(specialEffect['Kill SpEffect ID']) != 0):
        descriptionArray.append("When Enemy is Killed")
        row_dict["kill_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Kill SpEffect ID']], specialEffect['Kill SpEffect ID'], False)
        if (row_dict["kill_special_effect"]["description"] != ""):
            for value in row_dict["kill_special_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["kill_special_effect"].pop("description")
            

    if (int(specialEffect['Accumulator - Over Value - SpEffect ID']) != -1):
        row_dict["accumulator_over_value"] = int(specialEffect['Accumulator - Over Value'])
        descriptionArray.append("Activate the following effect when consecutively attacking an enemy approximately " + 
            str(math.ceil((int(specialEffect['Accumulator - Over Value']) / accumulatorIncrementValue))) + " times" )
        row_dict["accumulator_over_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Accumulator - Over Value - SpEffect ID']], \
            specialEffect['Accumulator - Over Value - SpEffect ID'], False)
        if (row_dict["accumulator_over_effect"]["description"] != ""):
            for value in row_dict["accumulator_over_effect"]["description"]:
                descriptionArray.append(value)
            row_dict["accumulator_over_effect"].pop("description")

    if (float(specialEffect['Duration']) != -1.0):
        row_dict["duration"] = float(specialEffect['Duration'])
        if not(checkStringAllStates("Trigger", row_dict)):
            if (descriptionArray != [] and (float(specialEffect['Trigger Interval']) == 0.0 or float(row_dict['trigger_interval']) < float(row_dict["duration"])) and \
                    float(specialEffect['Duration']) != 0.1 and not(checkStringState("Poison", row_dict)) and not(checkStringState("Scarlet Rot", row_dict))):
                if (float(specialEffect['Duration']) > 0.0):
                    if (float(specialEffect['Duration']) == 1.0):
                        descriptionArray.append("Effect lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " second")
                    else:
                        descriptionArray.append("Effect lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " seconds")
                else:
                    descriptionArray.append("Effect is applied for a brief moment")

    row_dict["description"] = descriptionArray

    if ("None" in row_dict["state_info"]):
        row_dict.pop("state_info")
    if ("None" in row_dict["trigger_on_state_info_1"]):
        row_dict.pop("trigger_on_state_info_1")
    if ("None" in row_dict["trigger_on_state_info_2"]):
        row_dict.pop("trigger_on_state_info_2")
    if ("None" in row_dict["trigger_on_state_info_3"]):
        row_dict.pop("trigger_on_state_info_3")

    return row_dict

def checkStringState(state, row_dict):
    return state in row_dict["state_info"]

def checkStringAllStates(state, row_dict):
    return state in row_dict["state_info"] or state in row_dict["trigger_on_state_info_1"] or state in row_dict["trigger_on_state_info_2"] or \
        state in row_dict["trigger_on_state_info_3"]

def getPassiveEffectVfx(row_dict, specialEffectId, descriptionArray):
    if specialEffectId  in SpEffectVfxParam:
        specialEffectVfx = SpEffectVfxParam[specialEffectId]
        if (specialEffectVfx['Is Silent'] == InputBoolean.TRUE.value):
            row_dict['silent_footsteps'] = InputBoolean.TRUE.value
            descriptionArray.append("Silence Footsteps")
        if (specialEffectVfx['Camouflage - Fields'] == InputBoolean.TRUE.value):
            row_dict['hide'] = InputBoolean.TRUE.value
            descriptionArray.append("Camouflage to the Background")
        if (specialEffectVfx['Camouflage - Translucent Appearance'] == InputBoolean.TRUE.value):
            row_dict['translucent'] = InputBoolean.TRUE.value
            descriptionArray.append("Camouflage to be Translucent")
        if (float(specialEffectVfx['Camouflage - Start Distance']) != -1.0):
            row_dict['hide_start'] = float(specialEffectVfx['Camouflage - Start Distance'])
            descriptionArray.append("Start Camouflage at " + str(round(float(specialEffectVfx['Camouflage - Start Distance']), 2)) + " distance")
        if (float(specialEffectVfx['Camouflage - End Distance']) != -1.0):
            row_dict['hide_end'] = float(specialEffectVfx['Camouflage - End Distance'])
            descriptionArray.append("End Camouflage at " + str(round(float(specialEffectVfx['Camouflage - End Distance']), 2)) + " distance")
        if (specialEffectVfx['Is Invisible Weapon'] == InputBoolean.TRUE.value):
            row_dict['invisible_weapon'] = InputBoolean.TRUE.value
            descriptionArray.append("Weapon is Invisible")
        if (int(specialEffectVfx['Phantom Param Overwrite Type']) != 0):
            row_dict['phantom_overwrite_type'] = int(specialEffectVfx['Phantom Param Overwrite Type'])
            if int(row_dict['phantom_overwrite_type'] == 2):
                if (int(specialEffectVfx['Phantom Param Overwrite ID']) != 0):
                    row_dict['phantom_overwrite_id'] = int(specialEffectVfx['Phantom Param Overwrite ID'])
                    if int(row_dict['phantom_overwrite_id']) == 61:
                        descriptionArray.append("Disguise as Host")
                    else:
                        descriptionArray.append("Disguise as Unknown Phantom 2")
                else:
                    descriptionArray.append("Disguise as Furled Finger")
            else:
                descriptionArray.append("Disguise as Unknown Phantom")

##############################################
# main
##############################################

attack_element_correct_param_data = getAttackElementCorrectParam()
weapon_reqs_data = getWeaponReqs()
weapon_damage_data = getWeaponDamage()
weapon_scaling_data = getWeaponScaling()
weapon_passive_data = getWeaponPassive()
calc_correct_id = getCalcCorrectId()
weapon_groups = getWeaponGroups()
physical_calculations = getPhysCalc()
armor_data = getArmorData()
talisman_data = getTalismanData()
talisman_groups = getTalismanGroups()
max_head, max_body, max_arm, max_leg = getMaxArmorData()
head_group, body_group, arm_group, leg_group = getArmorGroups()

writeToFile('attackelementcorrectparam', attack_element_correct_param_data)
writeToFile('weapon_reqs', weapon_reqs_data)
writeToFile('weapon_damage', weapon_damage_data)
writeToFile('weapon_scaling', weapon_scaling_data)
writeToFile('weapon_passive', weapon_passive_data)
writeToFile('calc_correct_id', calc_correct_id)
writeToFile('weapon_groups', weapon_groups)
writeToFile('physical_calculations', physical_calculations)
writeToFile('armor_data', armor_data)
writeToFile('talisman_data', talisman_data)
writeToFile('talisman_groups', talisman_groups)
writeToFile('max_head', max_head)
writeToFile('max_body', max_body)
writeToFile('max_arm', max_arm)
writeToFile('max_leg', max_leg)
writeToFile('head_group', head_group)
writeToFile('body_group', body_group)
writeToFile('arm_group', arm_group)
writeToFile('leg_group', leg_group)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(weapon_groups)
