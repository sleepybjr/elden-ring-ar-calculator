"""
needed CSV

SpEffectVfxParam
SpEffectParam

"""

from collections import OrderedDict
import csv
import math
import pprint
from enum import Enum
from tkinter import E

class InputBoolean(Enum):
    TRUE = "True"
    FALSE = "False"


##############################################
# General Load Data
##############################################

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



# Avg Accumulator Value for attacks. Could potentially switch for weapons in subsequent patches
# Look at AtkParam_Pc to see if the TargetSpEffect [0] for each weapon changes the ID of SpEffect ID 
# used to know if using different Id for acummulator
accumulatorIncrementValue = int(SpEffectParam['6903']['Accumulator - Increment Value'])

State_Info_Effect = {
    # SpEffectParam - State Info
    0: "None",
    2: "Poison",
    5: "Scarlet Rot",
    6: "Hemmorage",
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
    395: "Unknown",
    397: "Unknown",
    404: "Unknown",
    436: "Sleep",
    437: "Madness",
    450: "Reduce Headshot Impact",
    459: "Unknown",
    460: "Unknown",
    461: "Unknown",
    462: "Unknown",
    463: "Unknown",
    464: "Unknown",
    465: "Unknown",
    466: "Trigger on Crouch",
    467: "Unknown"
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
        row_dict["target_priority_percent"] = float(specialEffect['Target Priority'])
        if (float(specialEffect['Target Priority']) > 0.0):
            descriptionArray.append("Increase attraction of enemies by " + str(round(abs(float(specialEffect['Target Priority']) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease attraction of enemies by " + str(round(abs(float(specialEffect['Target Priority']) * 100.0), 2)) + "%")
    if (float(specialEffect['Enemy Listen Adjustment']) != 1.0):
        row_dict["enemy_listen_adjustment_percent"] = float(specialEffect['Enemy Listen Adjustment']) - 1.0
        if (float(specialEffect['Enemy Listen Adjustment']) > 1.0):
            descriptionArray.append("Increase sound emmitted to all enemies by " + str(round(abs((float(specialEffect['Enemy Listen Adjustment']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease sound emmitted to all enemies by " + str(round(abs((float(specialEffect['Enemy Listen Adjustment']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Max HP']) != 1.0):
        if (float(specialEffect['Max HP']) > 1.0):
            descriptionArray.append("Increase Max HP by " + str(round(abs((float(specialEffect['Max HP']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max HP by " + str(round(abs((float(specialEffect['Max HP']) - 1.0) * 100.0), 2)) + "%")
        row_dict["max_hp_percent"] = float(specialEffect['Max HP']) - 1.0
    if (float(specialEffect['Max FP']) != 1.0):
        row_dict["max_fp_percent"] = float(specialEffect['Max FP']) - 1.0
        if (float(specialEffect['Max FP']) > 1.0):
            descriptionArray.append("Increase Max FP by " + str(round(abs((float(specialEffect['Max FP']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max FP by " + str(round(abs((float(specialEffect['Max FP']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Max Stamina']) != 1.0):
        row_dict["max_stamina_percent"] = float(specialEffect['Max Stamina']) - 1.0
        if (float(specialEffect['Max Stamina']) > 1.0):
            descriptionArray.append("Increase Max Stamina by " + str(round(abs((float(specialEffect['Max Stamina']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Max Stamina by " + str(round(abs((float(specialEffect['Max Stamina']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Poise %']) != 1.0):
        row_dict["poise_percent"] = -(float(specialEffect['Poise %']) - 1.0)
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
        row_dict["fall_damage_percent"] = float(specialEffect['Fall Damage %']) - 1.0
        if (float(specialEffect['Fall Damage %']) > 1.0):
            descriptionArray.append("Increase Fall Damage taken by " + str(round(abs((float(specialEffect['Fall Damage %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Fall Damage taken by " + str(round(abs((float(specialEffect['Fall Damage %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Equip Load %']) != 1.0):
        row_dict["equip_load_percent"] = float(specialEffect['Equip Load %']) - 1.0
        if (float(specialEffect['Equip Load %']) > 1.0):
            descriptionArray.append("Increase Equip Load by " + str(round(abs((float(specialEffect['Equip Load %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Equip Load by " + str(round(abs((float(specialEffect['Equip Load %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Effect Duration %']) != 1.0):
        row_dict["effect_duration_percent"] = float(specialEffect['Effect Duration %']) - 1.0
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
        row_dict["guard_stability_percent"] = float(specialEffect['Guard Stability %']) - 1.0
        if (float(specialEffect['Guard Stability %']) > 1.0):
            descriptionArray.append("Increase Guard Stability by " + str(round(abs((float(specialEffect['Guard Stability %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease Guard Stability by " + str(round(abs((float(specialEffect['Guard Stability %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Attack %: Stamina']) != 1.0):
        row_dict["guard_break_percent"] = float(specialEffect['Attack %: Stamina']) - 1.0
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
        row_dict["rune_gain_percent"] = float(specialEffect['Rune Gain %']) - 1.0
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
        row_dict["hp_restore_correction_percent"] = float(specialEffect['HP Flask - HP Restore Correction']) - 1.0
        if (float(specialEffect['HP Flask - HP Restore Correction']) > 1.0):
            descriptionArray.append("Increase HP Restore from Flask of Crimson Tears by " + 
                str(round(abs((float(specialEffect['HP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease HP Restore from Flask of Crimson Tears by " + 
                str(round(abs((float(specialEffect['HP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['FP Flask - HP Restore Correction']) != 1.0):
        row_dict["fp_restore_correction_percent"] = float(specialEffect['FP Flask - HP Restore Correction']) - 1.0
        if (float(specialEffect['FP Flask - HP Restore Correction']) > 1.0):
            descriptionArray.append("Increase FP Restore from Flask of Cerulean Tears by " + 
                str(round(abs((float(specialEffect['FP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Restore from Flask of Cerulean Tears by " + 
                str(round(abs((float(specialEffect['FP Flask - HP Restore Correction']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Skill FP Cost %']) != 1.0):
        row_dict["skill_fp_cost_percent"] = float(specialEffect['Skill FP Cost %']) - 1.0
        if (float(specialEffect['Skill FP Cost %']) > 1.0):
            descriptionArray.append("Increase FP Cost for Skill by " + str(round(abs((float(specialEffect['Skill FP Cost %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Cost for Skill by " + str(round(abs((float(specialEffect['Skill FP Cost %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Sorcery FP Cost %']) != 1.0):
        row_dict["sorcery_fp_cost_percent"] = float(specialEffect['Sorcery FP Cost %']) - 1.0
        if (float(specialEffect['Sorcery FP Cost %']) > 1.0):
            descriptionArray.append("Increase FP Cost for Sorcery by " + str(round(abs((float(specialEffect['Sorcery FP Cost %']) - 1.0) * 100.0), 2)) + "%")
        else:
            descriptionArray.append("Decrease FP Cost for Sorcery by " + str(round(abs((float(specialEffect['Sorcery FP Cost %']) - 1.0) * 100.0), 2)) + "%")
    if (float(specialEffect['Incantation FP Cost %']) != 1.0):
        row_dict["incantation_fp_cost_percent"] = float(specialEffect['Incantation FP Cost %']) - 1.0  
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
        row_dict["enemy_sight_adjustment_percent"] = float(specialEffect['Enemy Sight Adjustment']) - 1.0
    if (float(specialEffect['Sight Search - Enemy Addition']) != 0.0):
        row_dict["sight_search_enemy_addition_percent"] = float(specialEffect['Sight Search - Enemy Addition'])
    if (float(specialEffect['Listen Search - Enemy Addition']) != 0.0):
        row_dict["listen_search_enemy_addition_percent"] = float(specialEffect['Listen Search - Enemy Addition'])
    if (float(specialEffect['Listen Search Correction']) != 1.0):
        row_dict["listen_search_correction_percent"] = float(specialEffect['Listen Search Correction']) - 1.0
    if (float(specialEffect['Listen Search Addition']) != 0.0):
        row_dict["listen_search_addition_percent"] = float(specialEffect['Listen Search Addition'])
    if (float(specialEffect['Sight Search Addition']) != 0.0):
        row_dict["sight_search_addition_percent"] = float(specialEffect['Sight Search Addition'])
    if (float(specialEffect['No Guard Damage %']) != 1.0):
        row_dict["no_guard_damage_percent"] = float(specialEffect['No Guard Damage %']) - 1.0
    if (float(specialEffect['Vital Spot Change %']) != -1.0):
        row_dict["vital_spot_change_percent"] = float(specialEffect['Vital Spot Change %'])
    if (float(specialEffect['Normal Spot Change %']) != -1.0):
        row_dict["normal_spot_change_percent"] = float(specialEffect['Normal Spot Change %'])
    if (float(specialEffect['Look-At Target Position Offset']) != 0.0):
        row_dict["look_at_target_position_offset"] = float(specialEffect['Look-At Target Position Offset'])
    if (float(specialEffect['Poise Recovery Time %']) != 1.0):
        row_dict["poise_recovery_time_percent"] = float(specialEffect['Poise Recovery Time %']) - 1.0
    if (float(specialEffect['Regain Correction %']) != 1.0):
        row_dict["regain_correction_percent"] = float(specialEffect['Regain Correction %']) - 1.0
    if (float(specialEffect['Poise Damage %']) != 1.0):
        row_dict["poise_damage_percent"] = float(specialEffect['Poise Damage %']) - 1.0

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
            if (-int(specialEffect['Change HP +']) > 0):
                descriptionArray.append("Add " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
            else:
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change HP +']))) + " HP points")
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
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change FP +']))) + " FP points")
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
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
                else:
                    descriptionArray.append("Subtract " + str(abs(int(specialEffect['Change Stamina +']))) + " Stamina points")
    if (float(specialEffect['Change HP %']) != 0):
        row_dict["change_hp_percent"] = -float(specialEffect['Change HP %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change HP %']) > 0.0):
                descriptionArray.append("Regen HP by " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain HP by " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% per second")
        else:
            if (-float(specialEffect['Change HP %']) > 0.0):
                descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change HP %']))), 2)) + "% HP")
            else:
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
                else:
                    descriptionArray.append("Subtract " + str(abs(float(specialEffect['Change HP %']))) + "% HP")
    if (float(specialEffect['Change FP %']) != 0):
        row_dict["change_fp_percent"] = -float(specialEffect['Change FP %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change FP %']) > 0.0):
                descriptionArray.append("Regen FP by " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain FP by " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% per second")
        else:
            if (-float(specialEffect['Change FP %']) > 0.0):
                descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change FP %']))), 2)) + "% FP")
            else:
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change FP %']))) + "% FP")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(ifloatnt(specialEffect['Change FP %']))) + "% FP")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change FP %']))) + "% FP")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change FP %']))) + "% FP")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change FP %']))) + "% FP")
                else:
                    descriptionArray.append("Subtract " + str(abs(float(specialEffect['Change FP %']))) + "% FP")
    if (float(specialEffect['Change Stamina %']) != 0):
        row_dict["change_stamina_percent"] = -float(specialEffect['Change Stamina %'])
        if (checkStringState("HP/FP/Stamina Recovery", row_dict)):
            if (-float(specialEffect['Change Stamina %']) > 0.0):
                descriptionArray.append("Regen Stamina by " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% per second")
            else:
                descriptionArray.append("Drain Stamina by " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% per second")
        else:
            if (-float(specialEffect['Change Stamina %']) > 0.0):
                descriptionArray.append("Add " + str(round(abs((float(specialEffect['Change Stamina %']))), 2)) + "% Stamina")
            else:
                if (checkStringState("Poison", row_dict)):
                    descriptionArray.append("If Poison Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
                elif (checkStringState("Scarlet Rot", row_dict)):
                    descriptionArray.append("If Scarlet Rot Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
                elif (checkStringState("Hemmorage", row_dict)):
                    descriptionArray.append("If Bleed Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
                elif (checkStringState("Sleep", row_dict)):
                    descriptionArray.append("If Sleep Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
                elif (checkStringState("Madness", row_dict)):
                    descriptionArray.append("If Madness Status Effect is applied, Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
                else:
                    descriptionArray.append("Subtract " + str(abs(float(specialEffect['Change Stamina %']))) + "% Stamina")
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
        row_dict["trigger_below_hp_percent"] = int(specialEffect['Trigger at HP Below %'])
        descriptionArray.append("Trigger Effect when HP is below or equal to " + str(int(specialEffect['Trigger at HP Below %'])) + "%")
    if (int(specialEffect['Trigger on HP Above %']) != -1):
        row_dict["trigger_above_hp_percent"] = int(specialEffect['Trigger on HP Above %'])
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
            if (descriptionArray != [] and (float(specialEffect['Duration']) == -1.0)) and float(specialEffect['Trigger Interval']) != 0.06 and \
                float(specialEffect['Trigger Interval']) != 0.01 and not(checkStringState("Unknown", row_dict)):
                if (float(specialEffect['Trigger Interval']) == 1.0):
                    descriptionArray.append("Effect is triggered every second")
                else:
                    descriptionArray.append("Effect is triggered every " + str(round(abs((float(specialEffect['Trigger Interval']))), 2)) + " seconds")
            elif (checkStringState("Poison", row_dict)):
                if (float(specialEffect['Trigger Interval']) == 1.0):
                    descriptionArray.append("Poison damage is triggered every second")
                else:
                    descriptionArray.append("Poison damage is triggered every " + str(round(abs((float(specialEffect['Trigger Interval']))), 2)) + " seconds")          
            elif (checkStringState("Scarlet Rot", row_dict)):
                if (float(specialEffect['Trigger Interval']) == 1.0):
                    descriptionArray.append("Scarlet Rot damage is triggered every second")
                else:
                    descriptionArray.append("Scarlet Rot damage is triggered every " + str(round(abs((float(specialEffect['Trigger Interval']))), 2)) + " seconds")          


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
                if value != "Effect is applied for a brief moment":
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
                    float(specialEffect['Duration']) != 0.1) and not(checkStringState("Unknown", row_dict)):
                if (float(specialEffect['Duration']) > 0.0):
                    if (float(specialEffect['Duration']) == 1.0):
                        if (checkStringState("Poison", row_dict)):
                            descriptionArray.append("Poison Status Effect if applied lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " second")
                        elif (checkStringState("Scarlet Rot", row_dict)):
                            descriptionArray.append("Scarlet Rot Status Effect if applied lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " second")
                        else:
                            descriptionArray.append("Effect lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " second")
                    else:
                        if (checkStringState("Poison", row_dict)):
                            descriptionArray.append("Poison Status Effect if applied lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " seconds")
                        elif (checkStringState("Scarlet Rot", row_dict)):
                            descriptionArray.append("Scarlet Rot Status Effect if applied lasts for " + str(round(abs((float(specialEffect['Duration']))), 2)) + " seconds")
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
