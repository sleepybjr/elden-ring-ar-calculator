from collections import OrderedDict
import csv
import pprint
from enum import Enum

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


##############################################
# AttackElementCorrectParam.json
# read done, need to finish write
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
    # keep commented incase i find a way to link through ID's rather than name
    headers = next(reader)[1:]
    ReinforceParamWeapon = OrderedDict((row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)
    # headers = next(reader)[2:]
    # ReinforceParamWeapon = OrderedDict((row[1], OrderedDict(zip(headers, row[2:]))) for row in reader)


##############################################
# weapon_reqs.json
# missing values for read
# need to finish write
##############################################

def getWeaponReqs():
    weapon_reqs_data = []   
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:

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
            # row_dict["physicalDamageType"] = row[1] # not correct, use WeaponTypes.json?
            row_dict["weight"] = float(row["Weight"])
            row_dict["basePoiseAttack"] = float(row["Poise Damage"])
            # row_dict["weaponType"] = row[1] # not correct, maybe just load from previous values? Only issue is new weapons won't be matched until added. use WeaponTypes.json?

            weapon_reqs_data.append(row_dict)
    
    return weapon_reqs_data


##############################################
# weapon_damage.json
# read done, shouldn't be any edge cases, need to compare with current json
# need write
##############################################

def getWeaponDamage():
    weapon_damage_data = []

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']
            
            # shields might be edge case for matching, as well as cross bow and bows?

            upgrade_level_max = getMaxUpgrade(row)
            for upgrade_level in range(0, upgrade_level_max+1):
                # (EquipParamWeapon) Damage: Physical * (ReinforceParamWeapon) Damage % Physical --------- NEED UPGRADE LEVEL
                dmg_phys = float(row['Damage: Physical'])
                dmg_phys_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Physical'])
                row_dict["phys" + str(upgrade_level)] =  dmg_phys * dmg_phys_perc

                dmg_mag = float(row['Damage: Magic'])
                dmg_mag_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Magic'])
                row_dict["mag" + str(upgrade_level)] =  dmg_mag * dmg_mag_perc

                dmg_fire = float(row['Damage: Fire'])
                dmg_fire_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Fire'])
                row_dict["fire" + str(upgrade_level)] =  dmg_fire * dmg_fire_perc

                dmg_ligh = float(row['Damage: Lightning'])
                dmg_ligh_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Lightning'])
                row_dict["ligh" + str(upgrade_level)] =  dmg_ligh * dmg_ligh_perc

                dmg_holy = float(row['Damage: Holy'])
                dmg_holy_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Damage %: Holy'])
                row_dict["holy" + str(upgrade_level)] =  dmg_holy * dmg_holy_perc

                # row_dict["stam0"] = 81

            weapon_damage_data.append(row_dict)
    
    return weapon_damage_data


##############################################
# weapon_scaling.json
# read done, shouldn't be any edge cases, need to compare with current json
# need write
##############################################

def getWeaponScaling():
    weapon_scaling_data = []

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']
            
            # shields might be edge case for matching, as well as cross bow and bows?

            upgrade_level_max = getMaxUpgrade(row)
            for upgrade_level in range(0, upgrade_level_max+1):
                # (EquipParamWeapon) Correction: STR * (ReinforceParamWeapon) Correction % STR / 100 --------- NEED UPGRADE LEVEL
                crt_str = float(row['Correction: ' + Input.STR.value])
                crt_str_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.STR.value])
                row_dict["str" + str(upgrade_level)] =  crt_str * crt_str_perc / 100

                crt_dex = float(row['Correction: ' + Input.DEX.value])
                crt_dex_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.DEX.value])
                row_dict["dex" + str(upgrade_level)] =  crt_dex * crt_dex_perc / 100

                crt_int = float(row['Correction: ' + Input.INT.value])
                crt_int_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.INT.value])
                row_dict["int" + str(upgrade_level)] =  crt_int * crt_int_perc / 100

                crt_fai = float(row['Correction: ' + Input.FAI.value])
                crt_fai_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.FAI.value])
                row_dict["fai" + str(upgrade_level)] =  crt_fai * crt_fai_perc / 100

                crt_arc = float(row['Correction: ' + Input.ARC.value])
                crt_arc_perc = float(ReinforceParamWeapon[str(int(row["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.ARC.value])
                row_dict["arc" + str(upgrade_level)] =  crt_arc * crt_arc_perc / 100

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

def getWeaponPassive():
    with open("SpEffectParam.csv") as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = next(reader)[1:]
        SpEffectParam = OrderedDict((row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

    weapon_passive_data = []
    
    # ReinforceParamWeapon['Behavior SpEffect 1 Offset'] used for something?

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and base_weapon <= int(key) <= max_weapon:
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']

            passive1 = row["Behavior SpEffect 1"]
            passive2 = row["Behavior SpEffect 2"]
            passive3 = row["Behavior SpEffect 3"]
            
            types = []
            rows = []

            # need if statements for type of passive, for example poison is "Inflict Poison +"
            # -1 means not used
            if passive1 != '-1':
                if passive1 in SpEffectParam:
                    row1 = SpEffectParam[passive1]
                    # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                    rows.append(row1)
                    for type, value in PassiveTypes.items():
                        if type in row1['Row Name']:
                            types.append(value)
                            break

            if passive2 != '-1':
                row2 = SpEffectParam[passive2]
                # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                rows.append(row2)
                for type, value in PassiveTypes.items():
                    if type in row2['Row Name']:
                        types.append(value)
                        break

            if passive3 != '-1':
                row3 = SpEffectParam[passive3]
                # currently filtering out types by using own data and row name - row name isn't a var and can be changed
                rows.append(row3)
                for type, value in PassiveTypes.items():
                    if type in row3['Row Name']:
                        types.append(value)
                        break

            types.reverse()
            rows.reverse()

            for idx, type in enumerate(types):
                row_dict["type" + str(idx+1)] = type

                # currently filtering out types by using own data and row name - row name isn't a var and can be changed, is there a real link in yapped?
                if type == "Scarlet Rot":
                    row_dict["scarletRot0"] = rows[idx]["Inflict Scarlet Rot +"]
                elif type == "Madness":
                    row_dict["madness0"] = rows[idx]["Inflict Madness +"]
                elif type == "Sleep":
                    row_dict["sleep0"] = rows[idx]["Inflict Sleep +"]

                # upgrade_level_max = getMaxUpgrade(row)
                # for upgrade_level in range(0, upgrade_level_max+1):
                #     row_dict["frost" + str(upgrade_level)] =  0

                #     row_dict["poison" + str(upgrade_level)] = 0

                #     row_dict["blood" + str(upgrade_level)] =  0

            weapon_passive_data.append(row_dict)

    return weapon_passive_data


##############################################
# calc_correct_id.json
# need read & write
##############################################

def getCalcCorrectId():
    calc_correct_id = []

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

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(weapon_passive_data)