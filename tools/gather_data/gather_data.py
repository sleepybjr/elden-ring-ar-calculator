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
                                row_dict["restore_hp_hit_%"] = -float(
                                    SpEffectParam[str(row_id)]["Change HP %"])
                            if int(SpEffectParam[str(row_id)]["Change HP +"]) != 0:
                                row_dict["restore_hp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change HP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change HP %"]) != 0:
                                row_dict["restore_hp_kill_%"] = -float(
                                    SpEffectParam[str(row_id+1)]["Change HP %"])
                            if int(SpEffectParam[str(row_id+1)]["Change HP +"]) != 0:
                                row_dict["restore_hp_kill"] = -int(
                                    SpEffectParam[str(row_id+1)]["Change HP +"])
                    elif type == "Restore FP on Hit" or type == "Restore FP on Kill":
                        if type == "Restore FP on Hit":
                            if float(SpEffectParam[str(row_id)]["Change FP %"]) != 0:
                                row_dict["restore_fp_hit_%"] = -float(
                                    SpEffectParam[str(row_id)]["Change FP %"])
                            if int(SpEffectParam[str(row_id)]["Change FP +"]) != 0:
                                row_dict["restore_fp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change FP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change FP %"]) != 0:
                                row_dict["restore_fp_kill_%"] = -float(
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
                        row_dict["passive_1"] = getPassiveEffect(SpEffectParam[passive1])

                if passive2 != '-1':
                    if passive2 in SpEffectParam:
                        row_dict["passive_2"] = getPassiveEffect(SpEffectParam[passive2])

                if passive3 != '-1':
                    if passive3 in SpEffectParam:
                        row_dict["passive_3"] = getPassiveEffect(SpEffectParam[passive3])

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


##############################################
# armor_groups.json
##############################################

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


##############################################
# max_armor_data.json
##############################################
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
            row_dict["passive_1"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [1]']) + 2)])
            calcAbsorptions(row_dict, row_dict["passive_1"])
        if int(row['Resident SpEffect ID [2]']) != -1:
            row_dict["passive_2"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [2]']) + 2)])
            calcAbsorptions(row_dict, row_dict["passive_2"])
        if int(row['Resident SpEffect ID [3]']) != -1:
            row_dict["passive_3"] = getPassiveEffect(SpEffectParam[str(int(row['Resident SpEffect ID [3]']) + 2)])
            calcAbsorptions(row_dict, row_dict["passive_3"])
    else:
        if int(row['Resident SpEffect ID [1]']) != -1:
            row_dict["passive_1"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [1]']])
            calcAbsorptions(row_dict, row_dict["passive_1"])
        if int(row['Resident SpEffect ID [2]']) != -1:
            row_dict["passive_2"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [2]']])
            calcAbsorptions(row_dict, row_dict["passive_2"])
        if int(row['Resident SpEffect ID [3]']) != -1:
            row_dict["passive_3"] = getPassiveEffect(SpEffectParam[row['Resident SpEffect ID [3]']])
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
    return -((1.0 - absorption) * absorption_passive) + 1.0


State_Info_Effect = {
    # SpEffectParam - State Info
    0: "None",
    2: "Poison",
    5: "Scarlet Rot",
    50 : "HP/FP/Stamina Recovery",
    123: "Trigger on Roll (Head)",
    124: "Trigger on Roll (Body)",
    125: "Trigger on Roll (Arm)",
    126: "Trigger on Roll (Leg)",
    152: "Enable Attack Effect against Enemy",
    153: "Enable Attack Effect against Player",
    199: "Apply Kill Effect",
    275: "Player Behavior ID Change",
    379: "Trigger in Presence of Blood Loss",
    380: "Trigger in Presence of Rot",
    390: "Pacify Wild Animals",
    437: "Madness",
    450: "Reduce Headshot Impact",
    459: "Unknown",
    460: "Unknown",
    461: "Unknown",
    462: "Unknown",
    463: "Unknown",
    464: "Unknown",
    465: "Unknown"
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
    118 : "Ammunition OnHit Attack"
}


def getPassiveEffect(specialEffect):
    row_dict = OrderedDict()
    row_dict["name"] = specialEffect['Row Name']
    row_dict["state_info"] = State_Info_Effect[int(specialEffect['State Info'])]
    if (int(specialEffect['Trigger at HP Below %']) != -1):
        row_dict["trigger_below_hp_%"] = int(specialEffect['Trigger at HP Below %'])
    if (float(specialEffect['Duration']) != -1.0):
        row_dict["duration"] = float(specialEffect['Duration'])
    if (int(specialEffect['Vigor']) != 0):
        row_dict["vigor"] = int(specialEffect['Vigor'])
    if (int(specialEffect['Mind']) != 0):
        row_dict["mind"] = int(specialEffect['Mind'])
    if (int(specialEffect['Endurance']) != 0):
        row_dict["endurance"] = int(specialEffect['Endurance'])
    if (int(specialEffect['Strength']) != 0):
        row_dict["strength"] = int(specialEffect['Strength'])
    if (int(specialEffect['Dexterity']) != 0):
        row_dict["dexterity"] = int(specialEffect['Dexterity'])
    if (int(specialEffect['Intelligence']) != 0):
        row_dict["intelligence"] = int(specialEffect['Intelligence'])
    if (int(specialEffect['Faith']) != 0):
        row_dict["faith"] = int(specialEffect['Faith'])
    if (int(specialEffect['Arcane']) != 0):
        row_dict["arcane"] = int(specialEffect['Arcane'])
    if (int(specialEffect['Conditional Weapon Effect 1']) != 0):
        row_dict["coditional_weapon_effect_1"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 1'])]
    if (int(specialEffect['Conditional Weapon Effect 2']) != 0):
        row_dict["coditional_weapon_effect_2"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 2'])]
    if (int(specialEffect['Conditional Weapon Effect 3']) != 0):
        row_dict["coditional_weapon_effect_3"] = Conditional_Weapon_Effect[int(specialEffect['Conditional Weapon Effect 3'])]
    if (float(specialEffect['Attack %: Physical']) != 1.0):
        row_dict["attack_percent_physical"] = float(specialEffect['Attack %: Physical']) - 1.0
    if (float(specialEffect['Attack %: Magic']) != 1.0):
        row_dict["attack_percent_magic"] = float(specialEffect['Attack %: Magic']) - 1.0
    if (float(specialEffect['Attack %: Fire']) != 1.0):
        row_dict["attack_percent_fire"] = float(specialEffect['Attack %: Fire']) - 1.0
    if (float(specialEffect['Attack %: Lightning']) != 1.0):
        row_dict["attack_percent_lightning"] = float(specialEffect['Attack %: Lightning'])  - 1.0
    if (float(specialEffect['Attack %: Holy']) != 1.0):
        row_dict["attack_percent_holy"] = float(specialEffect['Attack %: Holy']) - 1.0
    if (float(specialEffect['Power %: Physical']) != 1.0):
        row_dict["power_percent_physical"] = float(specialEffect['Power %: Physical']) - 1.0
    if (float(specialEffect['Power %: Magic']) != 1.0):
        row_dict["power_percent_magic"] = float(specialEffect['Power %: Magic']) - 1.0
    if (float(specialEffect['Power %: Fire']) != 1.0):
        row_dict["power_percent_fire"] = float(specialEffect['Power %: Fire']) - 1.0
    if (float(specialEffect['Power %: Lightning']) != 1.0):
        row_dict["power_percent_lightning"] = float(specialEffect['Power %: Lightning'])  - 1.0
    if (float(specialEffect['Power %: Holy']) != 1.0):
        row_dict["power_percent_holy"] = float(specialEffect['Power %: Holy']) - 1.0
    if (int(specialEffect['Damage +: Physical']) != 0):
        row_dict["damage_physical"] = int(specialEffect['Damage +: Physical'])
    if (int(specialEffect['Damage +: Magic']) != 0):
        row_dict["damage_magic"] = int(specialEffect['Damage +: Magic'])
    if (int(specialEffect['Damage +: Fire']) != 0):
        row_dict["damage_fire"] = int(specialEffect['Damage +: Fire'])
    if (int(specialEffect['Damage +: Lighting']) != 0):
        row_dict["damage_lightning"] = int(specialEffect['Damage +: Lighting'])
    if (int(specialEffect['Damage +: Holy']) != 0):
        row_dict["damage_holy"] = int(specialEffect['Damage +: Holy'])
    if (float(specialEffect['Damage %: Physical']) != 1.0):
        row_dict["damage_percent_physical"] = float(specialEffect['Damage %: Physical']) - 1.0
    if (float(specialEffect['Damage %: Magic']) != 1.0):
        row_dict["damage_percent_magic"] = float(specialEffect['Damage %: Magic']) - 1.0
    if (float(specialEffect['Damage %: Fire']) != 1.0):
        row_dict["damage_percent_fire"] = float(specialEffect['Damage %: Fire']) - 1.0
    if (float(specialEffect['Damage %: Lightning']) != 1.0):
        row_dict["damage_percent_lightning"] = float(specialEffect['Damage %: Lightning'])  - 1.0
    if (float(specialEffect['Damage %: Holy']) != 1.0):
        row_dict["damage_percent_holy"] = float(specialEffect['Damage %: Holy']) - 1.0
    if (int(specialEffect['Defence +: Physical']) != 0):
        row_dict["defense_physical"] = int(specialEffect['Defence +: Physical'])
    if (int(specialEffect['Defence +: Magic']) != 0):
        row_dict["defense_magic"] = int(specialEffect['Defence +: Magic'])
    if (int(specialEffect['Defence +: Fire']) != 0):
        row_dict["defense_fire"] = int(specialEffect['Defence +: Fire'])
    if (int(specialEffect['Defence +: Lightning']) != 0):
        row_dict["defense_lightning"] = int(specialEffect['Defence +: Lightning'])
    if (int(specialEffect['Defence +: Holy']) != 0):
        row_dict["defense_holy"] = int(specialEffect['Defence +: Holy'])
    if (float(specialEffect['Defence %: Physical']) != 1.0):
        row_dict["defense_percent_physical"] = float(specialEffect['Defence %: Physical']) - 1.0
    if (float(specialEffect['Defence %: Magic']) != 1.0):
        row_dict["defense_percent_magic"] = float(specialEffect['Defence %: Magic']) - 1.0
    if (float(specialEffect['Defence %: Fire']) != 1.0):
        row_dict["defense_percent_fire"] = float(specialEffect['Defence %: Fire']) - 1.0
    if (float(specialEffect['Defence %: Lightning']) != 1.0):
        row_dict["defense_percent_lightning"] = float(specialEffect['Defence %: Lightning'])  - 1.0
    if (float(specialEffect['Defence %: Holy']) != 1.0):
        row_dict["defensee_percent_holy"] = float(specialEffect['Defence %: Holy']) - 1.0
    if (float(specialEffect['PVP Damage %: Physical']) != 1.0):
        row_dict["pvp_damage_percent_physical"] = float(specialEffect['PVP Damage %: Physical']) - 1.0
    if (float(specialEffect['PVP Damage %: Magic']) != 1.0):
        row_dict["pvp_damage_percent_magic"] = float(specialEffect['PVP Damage %: Magic']) - 1.0
    if (float(specialEffect['PVP Damage %: Fire']) != 1.0):
        row_dict["pvp_damage_percent_fire"] = float(specialEffect['PVP Damage %: Fire']) - 1.0
    if (float(specialEffect['PVP Damage %: Lightning']) != 1.0):
        row_dict["pvp_damage_percent_lightning"] = float(specialEffect['PVP Damage %: Lightning'])  - 1.0
    if (float(specialEffect['PVP Damage %: Holy']) != 1.0):
        row_dict["pvp_damage_percent_holy"] = float(specialEffect['PVP Damage %: Holy']) - 1.0
    if (float(specialEffect['Absorption %: Physical']) != 1.0):
        row_dict["absorption_percent_physical"] = -(float(specialEffect['Absorption %: Physical']) - 1.0)
    if (float(specialEffect['Absorption %: Magic']) != 1.0):
        row_dict["absorption_percent_magic"] = -(float(specialEffect['Absorption %: Magic']) - 1.0)
    if (float(specialEffect['Absorption %: Fire']) != 1.0):
        row_dict["absorption_percent_fire"] = -(float(specialEffect['Absorption %: Fire']) - 1.0)
    if (float(specialEffect['Absorption %: Lightning']) != 1.0):
        row_dict["absorption_percent_lightning"] = -(float(specialEffect['Absorption %: Lightning'])  - 1.0)
    if (float(specialEffect['Absorption %: Holy']) != 1.0):
        row_dict["absorption_percent_holy"] = -(float(specialEffect['Absorption %: Holy']) - 1.0)
    if (float(specialEffect['PVP Absorption %: Physical']) != 1.0):
        row_dict["pvp_absorption_percent_physical"] = -(float(specialEffect['PVP Absorption %: Physical']) - 1.0)
    if (float(specialEffect['PVP Absorption %: Magic']) != 1.0):
        row_dict["pvp_absorption_percent_magic"] = -(float(specialEffect['PVP Absorption %: Magic']) - 1.0)
    if (float(specialEffect['PVP Absorption %: Fire']) != 1.0):
        row_dict["pvp_absorption_percent_fire"] = -(float(specialEffect['PVP Absorption %: Fire']) - 1.0)
    if (float(specialEffect['PVP Absorption %: Lightning']) != 1.0):
        row_dict["pvp_absorptione_percent_lightning"] = -(float(specialEffect['PVP Absorption %: Lightning'])  - 1.0)
    if (float(specialEffect['PVP Absorption %: Holy']) != 1.0):
        row_dict["pvp_absorption_percent_holy"] = -(float(specialEffect['PVP Absorption %: Holy']) - 1.0)

    # You use this to get the new absorption from armor.
    # An example calculation to get a new physical absorption for armor is found below
    # physical_absorption = -((1 - physical_absorption) * absorption_standard) + 1 
    if (float(specialEffect['Absorption: Standard']) != 1.0):
        row_dict["absorption_standard"] = float(specialEffect['Absorption: Standard'])
    if (float(specialEffect['Absorption: Strike']) != 1.0):
        row_dict["absorption_strike"] = float(specialEffect['Absorption: Strike'])
    if (float(specialEffect['Absorption: Slash']) != 1.0):
        row_dict["absorption_slash"] = float(specialEffect['Absorption: Slash'])
    if (float(specialEffect['Absorption: Thrust']) != 1.0):
        row_dict["absorption_thrust"] = float(specialEffect['Absorption: Thrust'])
    if (float(specialEffect['Absorption: Magic']) != 1.0):
        row_dict["absorption_magic"] = float(specialEffect['Absorption: Magic'])
    if (float(specialEffect['Absorption: Fire']) != 1.0):
        row_dict["absorption_fire"] = float(specialEffect['Absorption: Fire'])
    if (float(specialEffect['Absorption: Lightning']) != 1.0):
        row_dict["absorption_lightning"] = float(specialEffect['Absorption: Lightning'])
    if (float(specialEffect['Absorption: Holy']) != 1.0):
        row_dict["absorption_holy"] = float(specialEffect['Absorption: Holy'])

    if (int(specialEffect['Resist: Poison +']) == int(specialEffect['Resist: Scarlet Rot +'])):
        if (int(specialEffect['Resist: Poison +']) != 0):
            row_dict["resist_immunity"] = int(specialEffect['Resist: Poison +'])
    else:
        if (int(specialEffect['Resist: Poison +']) != 0):
            row_dict["resist_poison"] = int(specialEffect['Resist: Poison +'])
        if (int(specialEffect['Resist: Scarlet Rot +']) != 0):
            row_dict["resist_rot"] = int(specialEffect['Resist: Scarlet Rot +'])
    if (int(specialEffect['Resist: Hemorrhage +']) == int(specialEffect['Resist: Frostbite +'])):
        if (int(specialEffect['Resist: Hemorrhage +']) != 0):
            row_dict["resist_robustness"] = int(specialEffect['Resist: Hemorrhage +'])
    else:
        if (int(specialEffect['Resist: Hemorrhage +']) != 0):
            row_dict["resist_bleed"] = int(specialEffect['Resist: Hemorrhage +'])
        if (int(specialEffect['Resist: Frostbite +']) != 0):
            row_dict["resist_frost"] = int(specialEffect['Resist: Frostbite +'])
    if (int(specialEffect['Resist: Madness +']) == int(specialEffect['Resist: Sleep +'])):
        if (int(specialEffect['Resist: Madness +']) != 0):
            row_dict["resist_focus"] = int(specialEffect['Resist: Madness +'])
    else:
        if (int(specialEffect['Resist: Madness +']) != 0):
            row_dict["resist_madness"] = int(specialEffect['Resist: Madness +'])
        if (int(specialEffect['Resist: Sleep +']) != 0):
            row_dict["resist_sleep"] = int(specialEffect['Resist: Sleep +'])
    if (int(specialEffect['Resist: Blight +']) != 0):
        row_dict["resist_vitality"] = int(specialEffect['Resist: Blight +'])

    if (int(specialEffect['Inflict Poison +']) == int(specialEffect['Inflict Scarlet Rot +'])):
        if (int(specialEffect['Inflict Poison +']) != 0):
            row_dict["resist_immunity"] = int(specialEffect['Inflict Poison +'])
    else:
        if (int(specialEffect['Inflict Poison +']) != 0):
            row_dict["inflict_poison"] = int(specialEffect['Inflict Poison +'])
        if (int(specialEffect['Inflict Scarlet Rot +']) != 0):
            row_dict["inflict_rot"] = int(specialEffect['Inflict Scarlet Rot +'])
    if (int(specialEffect['Inflict Hemorrhage +']) == int(specialEffect['Inflict Frostbite +'])):
        if (int(specialEffect['Inflict Hemorrhage +']) != 0):
            row_dict["inflict_robustness"] = int(specialEffect['Inflict Hemorrhage +'])
    else:
        if (int(specialEffect['Inflict Hemorrhage +']) != 0):
            row_dict["inflict_bleed"] = int(specialEffect['Inflict Hemorrhage +'])
        if (int(specialEffect['Inflict Frostbite +']) != 0):
            row_dict["inflict_frost"] = int(specialEffect['Inflict Frostbite +'])
    if (int(specialEffect['Inflict Madness +']) == int(specialEffect['Inflict Sleep +'])):
        if (int(specialEffect['Inflict Madness +']) != 0):
            row_dict["inflict_focus"] = int(specialEffect['Inflict Madness +'])
    else:
        if (int(specialEffect['Inflict Madness +']) != 0):
            row_dict["inflict_madness"] = int(specialEffect['Inflict Madness +'])
        if (int(specialEffect['Inflict Sleep +']) != 0):
            row_dict["inflict_sleep"] = int(specialEffect['Inflict Sleep +'])
    if (int(specialEffect['Inflict Blight +']) != 0):
        row_dict["inflict_vitality"] = int(specialEffect['Inflict Blight +'])

    if (int(specialEffect['Resist %: Poison']) == int(specialEffect['Resist %: Scarlet Rot'])):
        if (float(specialEffect['Resist %: Poison']) != 1.0):
            row_dict["resist_percent_immunity"] = int(specialEffect['Resist %: Poison'])
    else:
        if (float(specialEffect['Resist %: Poison']) != 1.0):
            row_dict["resist_percent_poison"] = int(specialEffect['Resist %: Poison'])
        if (float(specialEffect['Resist %: Scarlet Rot']) != 1.0):
            row_dict["resist_percent_rot"] = int(specialEffect['Resist %: Scarlet Rot'])
    if (int(specialEffect['Resist %: Hemorrhage']) == int(specialEffect['Resist %: Frostbite'])):
        if (float(specialEffect['Resist %: Hemorrhage']) != 1.0):
            row_dict["resist_percent_robustness"] = int(specialEffect['Resist %: Hemorrhage'])
    else:
        if (float(specialEffect['Resist %: Hemorrhage']) != 1.0):
            row_dict["resist_percent_bleed"] = int(specialEffect['Resist %: Hemorrhage'])
        if (float(specialEffect['Resist %: Frostbite']) != 1.0):
            row_dict["resist_percent_frost"] = int(specialEffect['Resist %: Frostbite'])
    if (int(specialEffect['Resist %: Madness']) == int(specialEffect['Resist %: Sleep'])):
        if (float(specialEffect['Resist %: Sleep']) != 1.0):
            row_dict["resist_percent_focus"] = int(specialEffect['Resist %: Sleep'])
    else:
        if (float(specialEffect['Resist %: Madness']) != 1.0):
            row_dict["resist_percent_madness"] = int(specialEffect['Resist %: Madness'])
        if (float(specialEffect['Resist %: Sleep']) != 1.0):
            row_dict["resist_percent_sleep"] = int(specialEffect['Resist %: Sleep'])
    if (float(specialEffect['Resist %: Blight']) != 1.0):
        row_dict["resist_percent_vitality"] = int(specialEffect['Resist %: Blight'])

    if (int(specialEffect['Status Damage %: Poison']) == int(specialEffect['Status Damage %: Scarlet Rot'])):
        if (float(specialEffect['Status Damage %: Poison']) != 1.0):
            row_dict["status_damage_percent_immunity"] = int(specialEffect['Status Damage %: Poison'])
    else:
        if (float(specialEffect['Status Damage %: Poison']) != 1.0):
            row_dict["status_damage_percent_poison"] = int(specialEffect['Status Damage %: Poison'])
        if (float(specialEffect['Status Damage %: Scarlet Rot']) != 1.0):
            row_dict["status_damage_percent_rot"] = int(specialEffect['Status Damage %: Scarlet Rot'])
    if (int(specialEffect['Status Damage %: Hemorrhage']) == int(specialEffect['Status Damage %: Frostbite'])):
        if (float(specialEffect['Status Damage %: Hemorrhage']) != 1.0):
            row_dict["status_damage_percent_robustness"] = int(specialEffect['Status Damage %: Hemorrhage'])
    else:
        if (float(specialEffect['Status Damage %: Hemorrhage']) != 1.0):
            row_dict["status_damage_percent_bleed"] = int(specialEffect['Status Damage %: Hemorrhage'])
        if (float(specialEffect['Status Damage %: Frostbite']) != 1.0):
            row_dict["status_damage_percent_frost"] = int(specialEffect['Status Damage %: Frostbite'])
    if (int(specialEffect['Status Damage %: Madness']) == int(specialEffect['Status Damage %: Sleep'])):
        if (float(specialEffect['Status Damage %: Sleep']) != 1.0):
            row_dict["status_damage_percent_focus"] = int(specialEffect['Status Damage %: Sleep'])
    else:
        if (float(specialEffect['Status Damage %: Madness']) != 1.0):
            row_dict["status_damage_percent_madness"] = int(specialEffect['Status Damage %: Madness'])
        if (float(specialEffect['Status Damage %: Sleep']) != 1.0):
            row_dict["status_damage_percent_sleep"] = int(specialEffect['Status Damage %: Sleep'])
    if (float(specialEffect['Status Damage %: Blight']) != 1.0):
        row_dict["status_damage_percent_vitality"] = int(specialEffect['Status Damage %: Blight'])

    if (float(specialEffect['Target Priority']) != 0.0):
        row_dict["target_priority_%"] = float(specialEffect['Target Priority'])
    if (float(specialEffect['Enemy Sight Adjustment']) != 1.0):
        row_dict["enemy_sight_adjustment_%"] = float(specialEffect['Enemy Sight Adjustment']) - 1.0
    if (float(specialEffect['Enemy Listen Adjustment']) != 1.0):
        row_dict["enemy_listen_adjustment_%"] = float(specialEffect['Enemy Listen Adjustment']) - 1.0
    if (float(specialEffect['Sight Search - Enemy Addition']) != 0.0):
        row_dict["sight_search_enemy_addition_%"] = float(specialEffect['Sight Search - Enemy Addition'])
    if (float(specialEffect['Listen Search - Enemy Addition']) != 0.0):
        row_dict["listen_search_enemy_addition_%"] = float(specialEffect['Listen Search - Enemy Addition'])
    if (float(specialEffect['Sight Search Addition']) != 0.0):
        row_dict["sight_search_addition_%"] = float(specialEffect['Sight Search Addition'])
    if (float(specialEffect['Listen Search Addition']) != 0.0):
        row_dict["listen_search_addition_%"] = float(specialEffect['Listen Search Addition'])
    if (float(specialEffect['Listen Search Correction']) != 1.0):
        row_dict["listen_search_correction_%"] = float(specialEffect['Listen Search Correction']) - 1.0
    if (int(specialEffect['Change HP +']) != 0):
        row_dict["change_hp"] = -int(specialEffect['Change HP +'])
    if (int(specialEffect['Change FP +']) != 0):
        row_dict["change_fp"] = -int(specialEffect['Change FP +'])
    if (int(specialEffect['Change Stamina +']) != 0):
        row_dict["change_stamina"] = -int(specialEffect['Change Stamina +'])
    if (float(specialEffect['Change HP %']) != 0):
        row_dict["change_hp_%"] = -float(specialEffect['Change HP %'])
    if (float(specialEffect['Change FP %']) != 0):
        row_dict["change_fp_%"] = -float(specialEffect['Change FP %'])
    if (float(specialEffect['Change Stamina %']) != 0):
        row_dict["change_stamina_%"] = -float(specialEffect['Change Stamina %'])
    if (int(specialEffect['FP Recovery']) != 0):
        row_dict["fp_recovery"] = int(specialEffect['FP Recovery'])
    if (int(specialEffect['Stamina Recovery']) != 0):
        row_dict["stamina_recovery"] = int(specialEffect['Stamina Recovery'])
    if (float(specialEffect['Max HP']) != 1.0):
        row_dict["max_hp_%"] = float(specialEffect['Max HP']) - 1.0
    if (float(specialEffect['Max FP']) != 1.0):
        row_dict["max_fp_%"] = float(specialEffect['Max FP']) - 1.0
    if (float(specialEffect['Max Stamina']) != 1.0):
        row_dict["max_stamina_%"] = float(specialEffect['Max Stamina']) - 1.0
    if (float(specialEffect['Poise %']) != 1.0):
        row_dict["poise_%"] = float(specialEffect['Poise %']) - 1.0
    if (float(specialEffect['Poise +']) != 0.0):
        row_dict["poise"] = float(specialEffect['Poise +'])
    if (float(specialEffect['Fall Damage %']) != 1.0):
        row_dict["fall_damage_%"] = float(specialEffect['Fall Damage %']) - 1.0
    if (float(specialEffect['Equip Load %']) != 1.0):
        row_dict["equip_load_%"] = float(specialEffect['Equip Load %']) - 1.0
    if (float(specialEffect['Effect Duration %']) != 1.0):
        row_dict["effect_duration_%"] = float(specialEffect['Effect Duration %']) - 1.0
    if (float(specialEffect['Guard Stability %']) != 1.0):
        row_dict["guard_stability_%"] = float(specialEffect['Guard Stability %']) - 1.0
    if (float(specialEffect['Attack %: Stamina']) != 1.0):
        row_dict["guard_break_%"] = float(specialEffect['Attack %: Stamina']) - 1.0
    if (float(specialEffect['No Guard Damage %']) != 1.0):
        row_dict["no_guard_damage_%"] = float(specialEffect['No Guard Damage %']) - 1.0
    if (float(specialEffect['Poise Recovery Time %']) != 1.0):
        row_dict["poise_recovery_time_%"] = float(specialEffect['Poise Recovery Time %']) - 1.0
    if (float(specialEffect['Regain Correction %']) != 1.0):
        row_dict["regain_correction_%"] = float(specialEffect['Regain Correction %']) - 1.0
    if (float(specialEffect['Poise Damage %']) != 1.0):
        row_dict["poise_damage_%"] = float(specialEffect['Poise Damage %']) - 1.0
    if (int(specialEffect['Rune Gain +']) != 0):
        row_dict["rune_gain"] = int(specialEffect['Rune Gain +'])
    if (float(specialEffect['Rune Gain %']) != 1.0):
        row_dict["rune_gain_%"] = float(specialEffect['Rune Gain %']) - 1.0
    if (float(specialEffect['HP Flask - HP Restore Correction']) != 1.0):
        row_dict["hp_restore_correction_%"] = float(specialEffect['HP Flask - HP Restore Correction']) - 1.0
    if (float(specialEffect['FP Flask - HP Restore Correction']) != 1.0):
        row_dict["fp_restore_correction_%"] = float(specialEffect['FP Flask - HP Restore Correction']) - 1.0
    if (float(specialEffect['Skill FP Cost %']) != 1.0):
        row_dict["skill_fp_cost_%"] = float(specialEffect['Skill FP Cost %']) - 1.0 
    if (float(specialEffect['Sorcery FP Cost %']) != 1.0):
        row_dict["sorcery_fp_cost_%"] = float(specialEffect['Sorcery FP Cost %']) - 1.0 
    if (float(specialEffect['Incantation FP Cost %']) != 1.0):
        row_dict["incantation_fp_cost_%"] = float(specialEffect['Incantation FP Cost %']) - 1.0  
    if (int(specialEffect['Cast Speed']) != 0):
        row_dict["cast_speed"] = int(specialEffect['Cast Speed'])
    if (int(specialEffect['Memory Slot']) != 0):
        row_dict["memory_slot"] = int(specialEffect['Memory Slot'])  
    if (int(specialEffect['Bow Distance']) != 0):
        row_dict["bow_distance"] = int(specialEffect['Bow Distance'])  

    if (specialEffect['Trigger for Opponent'] == InputBoolean.TRUE.value):
        row_dict["trigger_effect_for_opponent"] = InputBoolean.TRUE.value
    if (specialEffect['Trigger for Friendly'] == InputBoolean.TRUE.value):
        row_dict["trigger_effect_for_friendly"] = InputBoolean.TRUE.value
    if (specialEffect['Trigger for Self'] == InputBoolean.TRUE.value):
        row_dict["trigger_effect_for_self"] = InputBoolean.TRUE.value

    if (int(specialEffect['Trigger on State Info [1]']) != 0):
        row_dict["trigger_on_state_info_1"] = State_Info_Effect[int(specialEffect['Trigger on State Info [1]'])]
    if (int(specialEffect['Trigger on State Info [2]']) != 0):
        row_dict["trigger_on_state_info_2"] = State_Info_Effect[int(specialEffect['Trigger on State Info [2]'])]
    if (int(specialEffect['Trigger on State Info [3]']) != 0):
        row_dict["trigger_on_state_info_3"] = State_Info_Effect[int(specialEffect['Trigger on State Info [3]'])]

    if (int(specialEffect['Chain SpEffect ID']) != -1):
        row_dict["chain_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Chain SpEffect ID']])

    if (int(specialEffect['Cycle SpEffect ID']) != -1):
        row_dict["cycle_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Cycle SpEffect ID']])
    
    if (int(specialEffect['Attack SpEffect ID']) != -1):
        row_dict["attack_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Attack SpEffect ID']])

    if (int(specialEffect['Kill SpEffect ID']) != 0):
        row_dict["kill_special_effect"] = getPassiveEffect(SpEffectParam[specialEffect['Kill SpEffect ID']])

    return row_dict



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
