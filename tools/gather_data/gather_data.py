from collections import OrderedDict
import csv
import pprint
from enum import Enum
import json

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

def getWeaponType(value):
    weapontype = int(value)
    return Weapon_Type[weapontype]

def getAffinity(value):
    affinity = int(value) % 10000
    return Input_Affinity[affinity]

def getMaxUpgrade(row):
    max_upgrade = -1 # error case

    if int(row['Origin Weapon +25']) == -1:
        if int(row['Origin Weapon +10']) == -1:
            max_upgrade = 0
        else:
            max_upgrade = 10
    else:
        max_upgrade = 25
    
    return max_upgrade

base_weapon = 1000000 # dagger
max_weapon = 44010000 # jar cannon

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
                    row_dict[attack_element_types[i]] =  int(row[i+2] == InputBoolean.TRUE.value)

                attack_element_correct_param_data.append(row_dict)
    
    return attack_element_correct_param_data


##############################################
# General Load Data
##############################################

with open("EquipParamWeapon.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    EquipParamWeapon = OrderedDict((row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("ReinforceParamWeapon.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    ReinforceParamWeapon = OrderedDict((row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)


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

                row_dict["strreq"] = int(row['Requirement: ' + Input.STR.value])
                row_dict["dexreq"] = int(row['Requirement: ' + Input.DEX.value])
                row_dict["intreq"] = int(row['Requirement: ' + Input.INT.value])
                row_dict["faireq"] = int(row['Requirement: ' + Input.FAI.value])
                row_dict["arcreq"] = int(row['Requirement: ' + Input.ARC.value])

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
                row_dict["weight"] = int(weight) if weight.is_integer() else weight
                poise_damage = float(row["Poise Damage"])
                row_dict["basePoiseAttack"] = int(poise_damage) if poise_damage.is_integer() else poise_damage
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
                    dmg_phys_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Physical'])
                    phys_name = "phys" + str(upgrade_level)
                    row_dict[phys_name] =  dmg_phys * dmg_phys_perc
                    if row_dict[phys_name].is_integer():
                        row_dict[phys_name] = int(row_dict[phys_name])

                    dmg_mag = float(row['Damage: Magic'])
                    dmg_mag_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Magic'])
                    mag_name = "mag" + str(upgrade_level)
                    row_dict[mag_name] =  dmg_mag * dmg_mag_perc
                    if row_dict[mag_name].is_integer():
                        row_dict[mag_name] = int(row_dict[mag_name])

                    dmg_fire = float(row['Damage: Fire'])
                    dmg_fire_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Fire'])
                    fire_name = "fire" + str(upgrade_level)
                    row_dict[fire_name] =  dmg_fire * dmg_fire_perc
                    if row_dict[fire_name].is_integer():
                        row_dict[fire_name] = int(row_dict[fire_name])

                    dmg_ligh = float(row['Damage: Lightning'])
                    dmg_ligh_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Lightning'])
                    ligh_name = "ligh" + str(upgrade_level)
                    row_dict[ligh_name] =  dmg_ligh * dmg_ligh_perc
                    if row_dict[ligh_name].is_integer():
                        row_dict[ligh_name] = int(row_dict[ligh_name])

                    dmg_holy = float(row['Damage: Holy'])
                    dmg_holy_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Holy'])
                    holy_name = "holy" + str(upgrade_level)
                    row_dict[holy_name] =  dmg_holy * dmg_holy_perc
                    if row_dict[holy_name].is_integer():
                        row_dict[holy_name] = int(row_dict[holy_name])

                    dmg_stam = float(row['Damage: Stamina'])
                    dmg_stam_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Stamina'])
                    stam_name = "stam" + str(upgrade_level)
                    row_dict[stam_name] =  dmg_stam * dmg_stam_perc
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
                    crt_str_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.STR.value])
                    str_name = "str" + str(upgrade_level)
                    row_dict[str_name] =  crt_str * crt_str_perc / 100
                    if row_dict[str_name].is_integer():
                        row_dict[str_name] = int(row_dict[str_name])

                    crt_dex = float(row['Correction: ' + Input.DEX.value])
                    crt_dex_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.DEX.value])
                    dex_name = "dex" + str(upgrade_level)
                    row_dict[dex_name] =  crt_dex * crt_dex_perc / 100
                    if row_dict[dex_name].is_integer():
                        row_dict[dex_name] = int(row_dict[dex_name])

                    crt_int = float(row['Correction: ' + Input.INT.value])
                    crt_int_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.INT.value])
                    int_name = "int" + str(upgrade_level)
                    row_dict[int_name] =  crt_int * crt_int_perc / 100
                    if row_dict[int_name].is_integer():
                        row_dict[int_name] = int(row_dict[int_name])

                    crt_fai = float(row['Correction: ' + Input.FAI.value])
                    crt_fai_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.FAI.value])
                    fai_name = "fai" + str(upgrade_level)
                    row_dict[fai_name] =  crt_fai * crt_fai_perc / 100
                    if row_dict[fai_name].is_integer():
                        row_dict[fai_name] = int(row_dict[fai_name])

                    crt_arc = float(row['Correction: ' + Input.ARC.value])
                    crt_arc_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.ARC.value])
                    arc_name = "arc" + str(upgrade_level)
                    row_dict[arc_name] =  crt_arc * crt_arc_perc / 100
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

PassiveTypes = {
    'Scarlet Rot': 'Scarlet Rot', 
    'Madness': 'Madness', 
    'Sleep': 'Sleep', 
    'Frostbite': 'Frost', 
    'Poison': 'Poison', 
    'Hemorrhage': 'Blood',
    }

EffectAttribute = {
    21: 'Scarlet Rot', 
    26: 'Madness', 
    24: 'Sleep', 
    23: 'Frost', 
    20: 'Poison', 
    22: 'Blood',
    27: 'Blight',
    254: 'None',
}

SortOrder = {
    'Scarlet Rot': 0,
    'Madness': 1,
    'Sleep': 2, 
    'Frost': 3, 
    'Poison': 4,
    'Blood': 5,
}

def getWeaponPassive():
    with open("SpEffectParam.csv") as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = next(reader)[1:]
        SpEffectParam = OrderedDict((row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

    weapon_passive_data = []
    
    # ReinforceParamWeapon['Behavior SpEffect 1 Offset'] used for something?

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                passive1 = row["Behavior SpEffect 1"]
                passive2 = row["Behavior SpEffect 2"]
                passive3 = row["Behavior SpEffect 3"]
                
                types = []
                rows = []
                row_nums = []

                # need if statements for type of passive, for example poison is "Inflict Poison +"
                # -1 means not used
                if passive1 != '-1':
                    if passive1 in SpEffectParam: # needed because regulation.bin has a bug with certain weapons
                        row1 = SpEffectParam[passive1]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in PassiveTypes.items():
                            if type in row1['Row Name']:
                                rows.append(row1)
                                row_nums.append(passive1)
                                types.append(value)
                                break

                if passive2 != '-1':
                    if passive2 in SpEffectParam:
                        row2 = SpEffectParam[passive2]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in PassiveTypes.items():
                            if type in row2['Row Name']:
                                rows.append(row2)
                                row_nums.append(passive2)
                                types.append(value)
                                break

                if passive3 != '-1':
                    if passive3 in SpEffectParam:
                        row3 = SpEffectParam[passive3]
                        # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                        for type, value in PassiveTypes.items(): # this is filtering out the other types of passive which is a bun
                            if type in row3['Row Name']:
                                rows.append(row3)
                                row_nums.append(passive3)
                                types.append(value)
                                break

                # passive type 1 and 2 are sorted in SortOrder
                if len(types) > 0:
                    zipped_lists = list(zip(types, rows, row_nums))
                    sorted_lists = sorted(zipped_lists, key=lambda value: SortOrder[value[0]])
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

                    if row_id in {5010600, 5121300, 5121800, 5140600, 5151200, 5160600}:
                        # edge case for celebrant's  and others, this id is for the rune gain or health regain
                        continue

                    # currently filtering out types by using own data and row name - row name isn't a var and can be changed, is there a real link in yapped?
                    if type == "Scarlet Rot":
                        row_dict["scarletRot0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Scarlet Rot +"]) if not (6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Scarlet Rot +"])
                    elif type == "Madness":
                        row_dict["madness0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Madness +"]) if not (6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Madness +"])
                    elif type == "Sleep":
                        row_dict["sleep0"] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Sleep +"]) if not (6400 <= row_id <= 6805) else int(SpEffectParam[str(row_id)]["Inflict Sleep +"])
                    else:
                        upgrade_level_max = getMaxUpgrade(row)
                        for upgrade_level in range(0, upgrade_level_max+1):
                            if not (6400 <= row_id <= 6805) and row_dict['name'] != 'Cold Antspur Rapier': # special passives, don't increase with level
                                if type == "Frost":
                                    row_dict["frost" + str(upgrade_level)] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Frostbite +"])

                                elif type == "Poison":
                                    row_dict["poison" + str(upgrade_level)] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Poison +"])

                                elif type == "Blood":
                                    row_dict["blood" + str(upgrade_level)] = int(SpEffectParam[str(row_id+upgrade_level)]["Inflict Hemorrhage +"])
                            else:
                                if type == "Frost":
                                    row_dict["frost" + str(upgrade_level)] = int(SpEffectParam[str(row_id)]["Inflict Frostbite +"])

                                elif type == "Poison":
                                    row_dict["poison" + str(upgrade_level)] = int(SpEffectParam[str(row_id)]["Inflict Poison +"])

                                elif type == "Blood":
                                    row_dict["blood" + str(upgrade_level)] = int(SpEffectParam[str(row_id)]["Inflict Hemorrhage +"])
                    
                    
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

                row_dict["attackelementcorrectId"] = int(row['Attack Element Correct ID'])


                calc_correct_id.append(row_dict)
        
    return calc_correct_id

##############################################
# main
##############################################

attack_element_correct_param_data = getAttackElementCorrectParam()
weapon_reqs_data = getWeaponReqs()
weapon_damage_data = getWeaponDamage()
weapon_scaling_data = getWeaponScaling()
weapon_passive_data = getWeaponPassive()
calc_correct_id = getCalcCorrectId()

writeToFile('attackelementcorrectparam', attack_element_correct_param_data)
writeToFile('weapon_reqs', weapon_reqs_data)
writeToFile('weapon_damage', weapon_damage_data)
writeToFile('weapon_scaling', weapon_scaling_data)
writeToFile('weapon_passive', weapon_passive_data)
writeToFile('calc_correct_id', calc_correct_id)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(weapon_passive_data)