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
from passives import getPassiveEffect
from passives import SpEffectParam
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
    0: "Reusable Items",
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
    33: "Unarmed",
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
    81: "Arrow",
    83: "Greatarrow",
    85: "Bolt",
    86: "Greatbolt",
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
    if ((int(value) >= base_weapon and int(value) < start_weapon) or (end_weapon < int(value) and int(value) <= max_weapon)):
        return Input_Affinity[0]
    else:
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

base_weapon = 110000    # Unarmed
start_weapon = 1000000  # dagger
start_arrow = 50000000  # arrow
end_weapon = 44010000   # jar cannon
max_weapon = 53030000   # Bone Ballista Bolt

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
            if (10000 <= int(row[0]) <= 30040) or (200300 <= int(row[0]) <= 203610):

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

with open("EquipParamGoods.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    EquipParamGoods = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("Bullet.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    Bullet = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

with open("AtkParam_Pc.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    headers = next(reader)[1:]
    AtkParam_Pc = OrderedDict(
        (row[0], OrderedDict(zip(headers, row[1:]))) for row in reader)

##############################################
# weapon_reqs.json
##############################################

def getWeaponReqs():
    weapon_reqs_data = []


    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            if row['Weapon Reference ID'] in EquipParamWeapon:
                row_dict = OrderedDict()
                row_dict["fullweaponname"] = EquipParamWeapon[row['Weapon Reference ID']]['Row Name']
                row_dict["weaponname"] = EquipParamWeapon[row['Weapon Reference ID']]['Row Name']

                row_dict["affinity"] = getAffinity('0')

                row_dict["maxUpgrade"] = getMaxUpgrade(EquipParamWeapon[row['Weapon Reference ID']])

                row_dict["strreq"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Requirement: ' + Input.STR.value])
                row_dict["dexreq"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Requirement: ' + Input.DEX.value])
                row_dict["intreq"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Requirement: ' + Input.INT.value])
                row_dict["faireq"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Requirement: ' + Input.FAI.value])
                row_dict["arcreq"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Requirement: ' + Input.ARC.value])

                if EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Normal"] == "True":
                    if EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Standard/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Standard"
                elif EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Strike"] == "True":
                    if EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Strike/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Strike"
                elif EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Slash"] == "True":
                    if EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Thrust"] == "True":
                        row_dict["physicalDamageType"] = "Slash/Pierce"
                    else:
                        row_dict["physicalDamageType"] = "Slash"
                elif EquipParamWeapon[row['Weapon Reference ID']]["Type Display: Thrust"] == "True":
                    row_dict["physicalDamageType"] = "Pierce"
                else:
                    row_dict["physicalDamageType"] = 0

                row_dict["weight"] = 0
                poise_damage = float(EquipParamWeapon[row['Weapon Reference ID']]["Poise Damage"])
                row_dict["basePoiseAttack"] = int(
                    poise_damage) if poise_damage.is_integer() else poise_damage
                row_dict["critical"] = 100 + int(EquipParamWeapon[row['Weapon Reference ID']]["Critical Multiplier"])
                row_dict["weaponType"] = getWeaponType(EquipParamWeapon[row['Weapon Reference ID']]["Weapon Type"])
                if (int(EquipParamWeapon[row['Weapon Reference ID']]["Weapon Hold Position - 2H"]) == 0):
                    row_dict["canTwoHand"] = InputBoolean.FALSE.value
                else:
                    row_dict["canTwoHand"] = InputBoolean.TRUE.value

            else:
                row_dict = OrderedDict()
                row_dict["fullweaponname"] = row['Row Name']
                row_dict["weaponname"] = row['Row Name']

                row_dict["affinity"] = getAffinity('0')

                row_dict["maxUpgrade"] = 0

                row_dict["strreq"] = 0
                row_dict["dexreq"] = 0
                row_dict["intreq"] = 0
                row_dict["faireq"] = 0
                row_dict["arcreq"] = 0
                row_dict["physicalDamageType"] = 0

                row_dict["weight"] = 0
                poise_damage = 0.0
                row_dict["basePoiseAttack"] = 0
                row_dict["critical"] = 100
                row_dict["weaponType"] = getWeaponType('0')
                row_dict["canTwoHand"] = InputBoolean.FALSE.value

            weapon_reqs_data.append(row_dict)


    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):

                row_dict = OrderedDict()
                row_dict["fullweaponname"] = row['Row Name']
                if (int (row['Origin Weapon +0']) == -1):
                    row_dict["weaponname"] = row['Row Name']
                else:
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
                if (int(row["Weapon Hold Position - 2H"]) == 0):
                    row_dict["canTwoHand"] = InputBoolean.FALSE.value
                else:
                    row_dict["canTwoHand"] = InputBoolean.TRUE.value

                weapon_reqs_data.append(row_dict)

    return weapon_reqs_data


def getAllBulletsFromAttack(referenceId, attackParamIds, emitter):
    if not(referenceId in Bullet):
        row_dict = OrderedDict()
        row_dict['atkParamId'] = '-1'
        row_dict['bulletCount'] = 0
        row_dict['prjctId'] = '-1'
        row_dict['impactId'] = '-1'
        row_dict['hitBulletID'] = '-1'
        row_dict['isEmitter'] = False
        row_dict['useShareHitList'] = InputBoolean.FALSE.value
        row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = '0'
        attackParamIds[referenceId] = row_dict
        return attackParamIds

    if int(Bullet[referenceId]['Hit Bullet ID']) != -1 and int(Bullet[referenceId]['AtkParam ID']) != 0 and int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1:
        returnVal1 =  getAllBulletsFromAttack(Bullet[referenceId]['Hit Bullet ID'], attackParamIds, emitter)
        returnVal2 =  getAllBulletsFromAttack(Bullet[referenceId]['Bullet Emitter: Bullet ID'], attackParamIds, True)

        returnVal1 = {**returnVal2, **returnVal1}
        row_dict = OrderedDict()
        row_dict['atkParamId'] = Bullet[referenceId]['AtkParam ID']
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = Bullet[referenceId]['Projectile SFX ID']
        row_dict['impactId'] = Bullet[referenceId]['Impact SFX ID']
        row_dict['hitBulletID'] = Bullet[referenceId]['Hit Bullet ID']
        row_dict['isEmitter'] = emitter
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return returnVal1
    elif int(Bullet[referenceId]['Hit Bullet ID']) != -1 and int(Bullet[referenceId]['AtkParam ID']) != 0:
        row_dict = OrderedDict()
        row_dict['atkParamId'] = Bullet[referenceId]['AtkParam ID']
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = Bullet[referenceId]['Projectile SFX ID']
        row_dict['impactId'] = Bullet[referenceId]['Impact SFX ID']
        row_dict['hitBulletID'] = Bullet[referenceId]['Hit Bullet ID']
        row_dict['isEmitter'] = emitter
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return getAllBulletsFromAttack(Bullet[referenceId]['Hit Bullet ID'], attackParamIds, emitter)
    elif int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1 and int(Bullet[referenceId]['AtkParam ID']) != 0:
        row_dict = OrderedDict()
        row_dict['atkParamId'] = Bullet[referenceId]['AtkParam ID']
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = Bullet[referenceId]['Projectile SFX ID']
        row_dict['impactId'] = Bullet[referenceId]['Impact SFX ID']
        row_dict['hitBulletID'] = '-1'
        row_dict['isEmitter'] = emitter
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return getAllBulletsFromAttack(Bullet[referenceId]['Bullet Emitter: Bullet ID'], attackParamIds, True)
    elif int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1 and int(Bullet[referenceId]['Hit Bullet ID']) != -1:
        returnVal1 =  getAllBulletsFromAttack(Bullet[referenceId]['Hit Bullet ID'], attackParamIds, emitter)
        returnVal2 =  getAllBulletsFromAttack(Bullet[referenceId]['Bullet Emitter: Bullet ID'], attackParamIds, True)
        returnVal1 = {**returnVal2, **returnVal1}
        row_dict = OrderedDict()
        row_dict['atkParamId'] = '-1'
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = Bullet[referenceId]['Projectile SFX ID']
        row_dict['impactId'] = Bullet[referenceId]['Impact SFX ID']
        row_dict['hitBulletID'] = Bullet[referenceId]['Hit Bullet ID']
        row_dict['isEmitter'] = emitter
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return returnVal1
    elif (int(Bullet[referenceId]['AtkParam ID']) != 0):
        row_dict = OrderedDict()
        row_dict['atkParamId'] = Bullet[referenceId]['AtkParam ID']
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = Bullet[referenceId]['Projectile SFX ID']
        row_dict['impactId'] = Bullet[referenceId]['Impact SFX ID']
        row_dict['isEmitter'] = emitter
        row_dict['hitBulletID'] = '-1'
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return attackParamIds
    elif int(Bullet[referenceId]['Hit Bullet ID']) != -1:
        row_dict = OrderedDict()
        row_dict['atkParamId'] = '-1'
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = '-1'
        row_dict['impactId'] = '-1'
        row_dict['isEmitter'] = False
        row_dict['hitBulletID'] = Bullet[referenceId]['Hit Bullet ID']
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return getAllBulletsFromAttack(Bullet[referenceId]['Hit Bullet ID'], attackParamIds, emitter)
    elif int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1:
        row_dict = OrderedDict()
        row_dict['atkParamId'] = '-1'
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = '-1'
        row_dict['impactId'] = '-1'
        row_dict['hitBulletID'] = '-1'
        row_dict['isEmitter'] = False
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return getAllBulletsFromAttack(Bullet[referenceId]['Bullet Emitter: Bullet ID'], attackParamIds, True)
    else:
        row_dict = OrderedDict()
        row_dict['atkParamId'] = '-1'
        row_dict['bulletCount'] = int(Bullet[referenceId]['Bullet Count'])
        row_dict['prjctId'] = '-1'
        row_dict['impactId'] = '-1'
        row_dict['hitBulletID'] = '-1'
        row_dict['isEmitter'] = False
        if (Bullet[referenceId]['Use Shared Hit List'] == InputBoolean.TRUE.value):
            row_dict['useShareHitList'] = InputBoolean.TRUE.value
        else:
            row_dict['useShareHitList'] = InputBoolean.FALSE.value
        if (Bullet[referenceId]['Continuous Hitbox'] == InputBoolean.TRUE.value):
            row_dict['continuousHitbox'] = InputBoolean.TRUE.value
        else:
            row_dict['continuousHitbox'] = InputBoolean.FALSE.value
        row_dict['bulletDuration'] = Bullet[referenceId]['Duration']
        attackParamIds[referenceId] = row_dict
        return attackParamIds

def getTotalDamage(atkParamId):
    return float(AtkParam_Pc[atkParamId]['Damage: Physical']) + float(AtkParam_Pc[atkParamId]['Damage: Magic']) + float(AtkParam_Pc[atkParamId]['Damage: Fire']) + \
                        float(AtkParam_Pc[atkParamId]['Damage: Lightning']) + float(AtkParam_Pc[atkParamId]['Damage: Holy'])


def getAttackIdForBullets(bullets, weaponName):
    attackId = '0'
    prjctId = '-1'
    impactId = '-1'
    total_dmg = 0.0
    for key, bullet in bullets.items():
        if (bullet['atkParamId'] in AtkParam_Pc):
            tempTotal = getTotalDamage(bullet['atkParamId'])
            if "Omen Bairn" in weaponName and bullet['prjctId'] != '-1' and bullet['impactId'] != '-1':
                attackId = bullet['atkParamId']
                prjctId = bullet['prjctId']
                impactId = bullet['impactId']
                break

            if (tempTotal > total_dmg or tempTotal == total_dmg == 0.0):
                total_dmg = tempTotal
                attackId = bullet['atkParamId']
                prjctId = bullet['prjctId']
                impactId = bullet['impactId']

    return attackId, prjctId, impactId


def getAmmountofHitsInBullet(bullets, attackId, prjctId, impactId):
    amountOfAttack = 1
    for key, bullet in bullets.items():
        if int(bullet['bulletCount']) > amountOfAttack and bullet['useShareHitList'] == InputBoolean.FALSE.value:
            if prjctId == bullet['prjctId'] and bullet['impactId'] == impactId and bullet['atkParamId'] == attackId and not(bullet['isEmitter']):
                amountOfAttack = int(bullet['bulletCount'])
            elif ((bullet['atkParamId'] ==  '-1' or getTotalDamage(bullet['atkParamId']) == 0) and bullet['hitBulletID'] != '-1' and bullets[bullet['hitBulletID']]['atkParamId'] == attackId):
                amountOfAttack = int(bullet['bulletCount'])
            elif ((bullet['atkParamId'] ==  '-1' or getTotalDamage(bullet['atkParamId']) == 0) and bullet['hitBulletID'] != '-1' and bullets[bullet['hitBulletID']]['hitBulletID'] != '-1' and \
                (bullets[bullet['hitBulletID']]['atkParamId'] ==  '-1' or getTotalDamage(bullets[bullet['hitBulletID']]['atkParamId']) == 0) and bullets[bullets[bullet['hitBulletID']]['hitBulletID']]['atkParamId'] == attackId):
                amountOfAttack = int(bullet['bulletCount'])
    for key, bullet in bullets.items():
        if (attackId == bullet['atkParamId'] and prjctId == bullet['prjctId'] and bullet['impactId'] == impactId and bullet['isEmitter']):
            amountOfAttack += int(bullet['bulletCount'])

    return amountOfAttack


def ifItemDoesAttack(attackId, row):
    if ((attackId != '0' and int(AtkParam_Pc[attackId]['Attack Correction: Physical']) > 0) or \
        (attackId != '0' and int(AtkParam_Pc[attackId]['Attack Correction: Magic']) > 0) or (attackId != '0' and int(AtkParam_Pc[attackId]['Attack Correction: Fire']) > 0) or \
            (attackId != '0' and int(AtkParam_Pc[attackId]['Attack Correction: Lightning']) > 0)  or (attackId != '0' and int(AtkParam_Pc[attackId]['Damage: Physical']) > 0) or \
                (attackId != '0' and int(AtkParam_Pc[attackId]['Attack Correction: Holy']) > 0)) and int(row['Reference Type']) == 1 and row['Row Name'] != '':
                return True
    else:
        return False


##############################################
# weapon_damage.json
##############################################

def getWeaponDamage():
    weapon_damage_data = []

    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']
            
            dmg_phys = 0.0
            dmg_mag = 0.0
            dmg_fire = 0.0
            dmg_ligh = 0.0
            dmg_holy = 0.0
            dmg_stam = 0.0
            upgrade_level_max = 0
            if attackId != '0':
                for upgrade_level in range(0, upgrade_level_max+1):
                    dmg_phys = float(AtkParam_Pc[attackId]['Damage: Physical'])
                    phys_name = "phys" + str(upgrade_level)
                    row_dict[phys_name] = dmg_phys
                    if row_dict[phys_name].is_integer():
                        row_dict[phys_name] = int(row_dict[phys_name])

                    dmg_mag = float(AtkParam_Pc[attackId]['Damage: Magic'])
                    mag_name = "mag" + str(upgrade_level)
                    row_dict[mag_name] = dmg_mag 
                    if row_dict[mag_name].is_integer():
                        row_dict[mag_name] = int(row_dict[mag_name])

                    dmg_fire = float(AtkParam_Pc[attackId]['Damage: Fire'])
                    fire_name = "fire" + str(upgrade_level)
                    row_dict[fire_name] = dmg_fire
                    if row_dict[fire_name].is_integer():
                        row_dict[fire_name] = int(row_dict[fire_name])

                    dmg_ligh = float(AtkParam_Pc[attackId]['Damage: Lightning'])
                    ligh_name = "ligh" + str(upgrade_level)
                    row_dict[ligh_name] = dmg_ligh
                    if row_dict[ligh_name].is_integer():
                        row_dict[ligh_name] = int(row_dict[ligh_name])

                    dmg_holy = float(AtkParam_Pc[attackId]['Damage: Holy'])
                    holy_name = "holy" + str(upgrade_level)
                    row_dict[holy_name] = dmg_holy
                    if row_dict[holy_name].is_integer():
                        row_dict[holy_name] = int(row_dict[holy_name])

                    dmg_stam = float(AtkParam_Pc[attackId]['Damage: Stamina'])
                    stam_name = "stam" + str(upgrade_level)
                    row_dict[stam_name] = dmg_stam
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

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
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


    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            if row['Weapon Reference ID'] in EquipParamWeapon:
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                upgrade_level_max = getMaxUpgrade(EquipParamWeapon[row['Weapon Reference ID']])
                for upgrade_level in range(0, upgrade_level_max+1):
                    # (EquipParamWeapon) Correction: STR * (ReinforceParamWeapon) Correction % STR / 100 --------- NEED UPGRADE LEVEL
                    crt_str = float(EquipParamWeapon[row['Weapon Reference ID']]['Correction: ' + Input.STR.value])
                    crt_str_perc = float(ReinforceParamWeapon[str(int(
                        EquipParamWeapon[row['Weapon Reference ID']]["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.STR.value])
                    str_name = "str" + str(upgrade_level)
                    row_dict[str_name] = crt_str * crt_str_perc / 100
                    if row_dict[str_name].is_integer():
                        row_dict[str_name] = int(row_dict[str_name])

                    crt_dex = float(EquipParamWeapon[row['Weapon Reference ID']]['Correction: ' + Input.DEX.value])
                    crt_dex_perc = float(ReinforceParamWeapon[str(int(
                        EquipParamWeapon[row['Weapon Reference ID']]["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.DEX.value])
                    dex_name = "dex" + str(upgrade_level)
                    row_dict[dex_name] = crt_dex * crt_dex_perc / 100
                    if row_dict[dex_name].is_integer():
                        row_dict[dex_name] = int(row_dict[dex_name])

                    crt_int = float(EquipParamWeapon[row['Weapon Reference ID']]['Correction: ' + Input.INT.value])
                    crt_int_perc = float(ReinforceParamWeapon[str(int(
                        EquipParamWeapon[row['Weapon Reference ID']]["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.INT.value])
                    int_name = "int" + str(upgrade_level)
                    row_dict[int_name] = crt_int * crt_int_perc / 100
                    if row_dict[int_name].is_integer():
                        row_dict[int_name] = int(row_dict[int_name])

                    crt_fai = float(EquipParamWeapon[row['Weapon Reference ID']]['Correction: ' + Input.FAI.value])
                    crt_fai_perc = float(ReinforceParamWeapon[str(int(
                        EquipParamWeapon[row['Weapon Reference ID']]["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.FAI.value])
                    fai_name = "fai" + str(upgrade_level)
                    row_dict[fai_name] = crt_fai * crt_fai_perc / 100
                    if row_dict[fai_name].is_integer():
                        row_dict[fai_name] = int(row_dict[fai_name])

                    crt_arc = float(EquipParamWeapon[row['Weapon Reference ID']]['Correction: ' + Input.ARC.value])
                    crt_arc_perc = float(ReinforceParamWeapon[str(int(
                        EquipParamWeapon[row['Weapon Reference ID']]["Reinforce Type ID"]) + upgrade_level)]['Correction %: ' + Input.ARC.value])
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
            else:
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                for upgrade_level in range(0, 26):
                    row_dict["str" + str(upgrade_level)] = 0
                    row_dict["dex" + str(upgrade_level)] = 0
                    row_dict["int" + str(upgrade_level)] = 0
                    row_dict["fai" + str(upgrade_level)] = 0
                    row_dict["arc" + str(upgrade_level)] = 0

                weapon_scaling_data.append(row_dict)

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
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

def findEffectFromBullet(referenceId, specialEffects):
    if not(referenceId in Bullet):
        return specialEffects

    if int(Bullet[referenceId]['Hit Bullet ID']) != -1 and int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1:
        returnVal1 = findEffectFromBullet(Bullet[referenceId]['Hit Bullet ID'], specialEffects)
        returnVal2 = findEffectFromBullet(Bullet[referenceId]['Bullet Emitter: Bullet ID'], specialEffects)
        returnVal1 += returnVal2
        if (Bullet[referenceId]['Target SpEffect ID 0'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 0'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 0'])
        if (Bullet[referenceId]['Target SpEffect ID 1'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 1'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 1'])
        if (Bullet[referenceId]['Target SpEffect ID 2'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 2'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 2'])
        if (Bullet[referenceId]['Target SpEffect ID 3'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 3'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 3'])
        return returnVal1
    elif (int(Bullet[referenceId]['Hit Bullet ID']) != -1):
        if (Bullet[referenceId]['Target SpEffect ID 0'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 0'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 0'])
        if (Bullet[referenceId]['Target SpEffect ID 1'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 1'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 1'])
        if (Bullet[referenceId]['Target SpEffect ID 2'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 2'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 2'])
        if (Bullet[referenceId]['Target SpEffect ID 3'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 3'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 3'])
        return findEffectFromBullet(Bullet[referenceId]['Hit Bullet ID'], specialEffects)
    elif (int(Bullet[referenceId]['Bullet Emitter: Bullet ID']) != -1):
        if (Bullet[referenceId]['Target SpEffect ID 0'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 0'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 0'])
        if (Bullet[referenceId]['Target SpEffect ID 1'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 1'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 1'])
        if (Bullet[referenceId]['Target SpEffect ID 2'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 2'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 2'])
        if (Bullet[referenceId]['Target SpEffect ID 3'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 3'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 3'])
        return findEffectFromBullet(Bullet[referenceId]['Bullet Emitter: Bullet ID'], specialEffects)
    else:
        if (Bullet[referenceId]['Target SpEffect ID 0'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 0'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 0'])
        if (Bullet[referenceId]['Target SpEffect ID 1'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 1'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 1'])
        if (Bullet[referenceId]['Target SpEffect ID 2'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 2'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 2'])
        if (Bullet[referenceId]['Target SpEffect ID 3'] != '0' and not(Bullet[referenceId]['Target SpEffect ID 3'] in specialEffects)):
            specialEffects.append(Bullet[referenceId]['Target SpEffect ID 3'])
        return specialEffects


def setItemPassive(row_dict, row_dict_passive, idx):
    if "inflict_poison" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Poison"]
        row_dict["poison0"] = row_dict_passive["inflict_poison"]
        idx += 1
    elif "inflict_bleed" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Hemorrhage"]
        row_dict["blood0"] = row_dict_passive["inflict_bleed"]
        idx += 1
    elif "inflict_rot" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Scarlet Rot"]
        row_dict["scarletRot0"] = row_dict_passive["inflict_rot"]
        idx += 1
    elif "inflict_frost" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Frostbite"]
        row_dict["frost0"] = row_dict_passive["inflict_frost"]
        idx += 1
    elif "inflict_madness" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Madness"]
        row_dict["madness0"] = row_dict_passive["inflict_madness"]
        idx += 1
    elif "inflict_sleep" in row_dict_passive:
        row_dict["type" + str(idx)] = BehaviorTypes["Sleep"]
        row_dict["sleep0"] = row_dict_passive["inflict_sleep"]
        idx += 1
    elif "cycle_special_effect" in row_dict_passive:
        setItemPassive(row_dict, row_dict_passive["cycle_special_effect"], idx)
    
    return idx


def checkForLingeringHitbox(bullets, name):
    hitbox = ""
    for key, bullet in bullets.items():
        if (bullet['continuousHitbox'] == InputBoolean.TRUE.value and float(bullet['bulletDuration']) > 0.0):
            hitbox  = "Has Lingering Hitbox for attack that lasts " + bullet['bulletDuration'] + " seconds"
        elif ("Ancestral Infant's Head" in name):
            hitbox  = "Has Lingering Hitbox for attack that lasts " + bullet['bulletDuration'] + " seconds"
    return hitbox


def getWeaponPassive():
    weapon_passive_data = []

    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            row_dict = OrderedDict()
            row_dict["name"] = row['Row Name']

            effects = findEffectFromBullet(row['Reference ID [0]'], list())
            hitbox = checkForLingeringHitbox(bullets, row_dict["name"])
            amountOfAttack = getAmmountofHitsInBullet(bullets, attackId, prjctId, impactId)

            # INIT VALUES
            row_dict["scarletRot0"] = 0
            row_dict["madness0"] = 0
            row_dict["sleep0"] = 0
            for upgrade_level in range(0, 26):
                row_dict["frost" + str(upgrade_level)] = 0
                row_dict["poison" + str(upgrade_level)] = 0
                row_dict["blood" + str(upgrade_level)] = 0


            amountOfEffects = 1
            idx = 1
            for effect in effects:
                if effect in SpEffectParam:  # needed because regulation.bin has a bug with certain weapons
                    row_dict["passive_" + str(amountOfEffects)] = getPassiveEffect(SpEffectParam[effect], effect, False)
                    idx = setItemPassive(row_dict, row_dict["passive_" + str(amountOfEffects)], idx)
                    amountOfEffects += 1
                            

            if hitbox != "":
                if "passive_1" in row_dict:
                    row_dict["passive_1"]["description"].append(hitbox)
                else:
                    row_dict["passive_1"] = OrderedDict()
                    row_dict["passive_1"]["description"] = list()
                    row_dict["passive_1"]["description"].append(hitbox)

            if amountOfAttack > 1:
                amountOfAttackString = "The attack for this item hits an enemy up to " + str(amountOfAttack) + " times per use"
                if "passive_1" in row_dict:
                    row_dict["passive_1"]["description"].append(amountOfAttackString)
                else:
                    row_dict["passive_1"] = OrderedDict()
                    row_dict["passive_1"]["description"] = list()
                    row_dict["passive_1"]["description"].append(amountOfAttackString)

            weapon_passive_data.append(row_dict)

    # ReinforceParamWeapon['Behavior SpEffect 1 Offset'] used for something?
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
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
                                row_dict["restore_hp_hit_percent"] = -float(
                                    SpEffectParam[str(row_id)]["Change HP %"])
                            if int(SpEffectParam[str(row_id)]["Change HP +"]) != 0:
                                row_dict["restore_hp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change HP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change HP %"]) != 0:
                                row_dict["restore_hp_kill_percent"] = -float(
                                    SpEffectParam[str(row_id+1)]["Change HP %"])
                            if int(SpEffectParam[str(row_id+1)]["Change HP +"]) != 0:
                                row_dict["restore_hp_kill"] = -int(
                                    SpEffectParam[str(row_id+1)]["Change HP +"])
                    elif type == "Restore FP on Hit" or type == "Restore FP on Kill":
                        if type == "Restore FP on Hit":
                            if float(SpEffectParam[str(row_id)]["Change FP %"]) != 0:
                                row_dict["restore_fp_hit_percent"] = -float(
                                    SpEffectParam[str(row_id)]["Change FP %"])
                            if int(SpEffectParam[str(row_id)]["Change FP +"]) != 0:
                                row_dict["restore_fp_hit"] = -int(
                                    SpEffectParam[str(row_id)]["Change FP +"])
                        else:
                            if float(SpEffectParam[str(row_id+1)]["Change FP %"]) != 0:
                                row_dict["restore_fp_kill_percent"] = -float(
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

    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            if row['Weapon Reference ID'] in EquipParamWeapon:
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                row_dict["physical"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Physical'])
                row_dict["magic"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Magic'])
                row_dict["fire"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Fire'])
                row_dict["lightning"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Lightning'])
                row_dict["poison"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Poison'])
                row_dict["bleed"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Hemorrhage'])
                row_dict["sleep"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Sleep'])
                row_dict["madness"] = int(EquipParamWeapon[row['Weapon Reference ID']]['Correction Type: Mandesss'])

                row_dict["attackelementcorrectId"] = int(
                    EquipParamWeapon[row['Weapon Reference ID']]['Attack Element Correct ID'])
            else:
                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                row_dict["physical"] = 0
                row_dict["magic"] = 0
                row_dict["fire"] = 0
                row_dict["lightning"] = 0
                row_dict["poison"] = 0
                row_dict["bleed"] = 0
                row_dict["sleep"] = 0
                row_dict["madness"] = 0

                row_dict["attackelementcorrectId"] = 0

            calc_correct_id.append(row_dict)

    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
            if not (row["Prevent Affinity Change"] == "True" and getAffinity(key) != "None"):

                row_dict = OrderedDict()
                row_dict["name"] = row['Row Name']

                row_dict["physical"] = int(row['Correction Type: Physical'])
                row_dict["magic"] = int(row['Correction Type: Magic'])
                row_dict["fire"] = int(row['Correction Type: Fire'])
                row_dict["lightning"] = int(row['Correction Type: Lightning'])
                row_dict["poison"] = int(row['Correction Type: Poison'])
                row_dict["bleed"] = int(row['Correction Type: Hemorrhage'])
                row_dict["sleep"] = int(row['Correction Type: Sleep'])
                row_dict["madness"] = int(row['Correction Type: Mandesss'])

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
    for key, row in EquipParamGoods.items():
        bullets = getAllBulletsFromAttack(row['Reference ID [0]'], OrderedDict(), False)
        attackId, prjctId, impactId = getAttackIdForBullets(bullets, row['Row Name'])
        if ifItemDoesAttack(attackId, row):
            weaponTypes.add(getWeaponType('0'))
            weapons[row['Row Name']] = getWeaponType('0')
    for key, row in EquipParamWeapon.items():
        if row['Row Name'] != '' and ((start_weapon <= int(key) <= end_weapon) or int(key) == base_weapon or (start_arrow <= int(key) <= max_weapon)):
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
            if (int (row['Origin Weapon +0']) == -1):
                weapons[row['Row Name']] = getWeaponType(row["Weapon Type"])
            else:
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
            row_dict["accessory_group"] = int(row['Accessory Group'])
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
