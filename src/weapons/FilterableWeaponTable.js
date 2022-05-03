import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import FilterBar from './FilterBar';
import WeaponTable from './WeaponTable';
import ExtraFilters from './ExtraFilters';
import SearchBar from '../component/SearchBar';

import Table_Data from '../json/weapons/merged_json_data.json';
import Attack_Element_Correct_Param from '../json/attackelementcorrectparam.json';
import Physical_Calculations from '../json/physical_calculations.json';
import Weapon_Groups from '../json/weapons/weapon_groups.json';

const scalingValues = {
    // In MenuValueTableParam
    'S': 175,
    'A': 140,
    'B': 90,
    'C': 60,
    'D': 25,
    'E': 1
}

const autoTwoHandBuff = new Set([
    "Light Bow", "Bow", "Greatbow",
]);

const passiveArcaneScaleId = 6;

const noTwoHandBuff = new Set([
    "Hookclaws", "Venomous Fang", "Bloodhound Claws", "Raptor Talons",
    "Caestus", "Spiked Caestus", "Grafted Dragon", "Iron Ball", "Star Fist", "Katar", "Clinging Bone", "Veteran's Prosthesis", "Cipher Pata",
    "Starscourge Greatsword",
    "Ornamental Straight Sword",
]);

const passiveTypes = [
    "Scarlet Rot",
    "Madness",
    "Sleep",
    "Frost",
    "Poison",
    "Blood",
    "Rune Gain on Hit",
    "Restore HP on Hit",
];

function totalAR(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getPhyData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
        getMagData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
        getFireData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
        getLighData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
        getHolyData(val, maxUpgrade, weaponLevel, levels, twoHanded);
};

export function getPhyCalcData(physScale, level) {
    let physCalc = 0;
    for (const element of Physical_Calculations) {
        if (element.row_id === physScale) {
            if (level > element.stat_max_3) {
                // Don't know what to do if adjustment is 0
                if (element.adj_point_3 > 0.0) {
                    physCalc = element.grow_3 + ((element.grow_4 - element.grow_3) * (((level - element.stat_max_3) / (element.stat_max_4 - element.stat_max_3)) ** element.adj_point_3))
                }
                else {
                    physCalc = element.grow_3 + ((element.grow_4 - element.grow_3) * (1 - ((1 - ((level - element.stat_max_3) / (element.stat_max_4 - element.stat_max_3))) ** -element.adj_point_3)))
                }
            }
            else if (level > element.stat_max_2) {
                if (element.adj_point_2 > 0.0) {
                    physCalc = element.grow_2 + ((element.grow_3 - element.grow_2) * (((level - element.stat_max_2) / (element.stat_max_3 - element.stat_max_2)) ** element.adj_point_2))
                }
                else {
                    physCalc = element.grow_2 + ((element.grow_3 - element.grow_2) * (1 - ((1 - ((level - element.stat_max_2) / (element.stat_max_3 - element.stat_max_2))) ** -element.adj_point_2)))
                }
            }
            else if (level > element.stat_max_1) {
                if (element.adj_point_1 > 0.0) {
                    physCalc = element.grow_1 + ((element.grow_2 - element.grow_1) * (((level - element.stat_max_1) / (element.stat_max_2 - element.stat_max_1)) ** element.adj_point_1))
                }
                else {
                    physCalc = element.grow_1 + ((element.grow_2 - element.grow_1) * (1 - ((1 - ((level - element.stat_max_1) / (element.stat_max_2 - element.stat_max_1))) ** -element.adj_point_1)))
                }
            }
            else {
                if (element.adj_point_0 > 0.0) {
                    physCalc = element.grow_0 + ((element.grow_1 - element.grow_0) * (((level - element.stat_max_0) / (element.stat_max_1 - element.stat_max_0)) ** element.adj_point_0))
                }
                else {
                    physCalc = element.grow_0 + ((element.grow_1 - element.grow_0) * (1 - ((1 - ((level - element.stat_max_0) / (element.stat_max_1 - element.stat_max_0))) ** -element.adj_point_0)))
                }
            }
            break;
        }
    }
    return physCalc;

}

function getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, attackType, shortAttackType) {
    let basePhys = 0;
    let phsyStr = 0;
    let phsyDex = 0;
    let phsyInt = 0;
    let phsyFai = 0;
    let phsyArc = 0;

    let isScale = {};

    for (const element of Attack_Element_Correct_Param) {
        if (element.rowId === val.attackelementcorrectId) {
            isScale = element;
            break;
        }
    }

    let strength = levels.strength;
    if ((twoHanded === true && !noTwoHandBuff.has(val.weaponname)) || autoTwoHandBuff.has(val.weaponType)) {
        strength = levels.twohand_strength;
    }

    const calcStr = isScale[attackType + "ScalingStr"] === 1 ? getPhyCalcData(val[attackType], strength) : 0;
    const calcDex = isScale[attackType + "ScalingDex"] === 1 ? getPhyCalcData(val[attackType], levels.dexterity) : 0;
    const calcInt = isScale[attackType + "ScalingInt"] === 1 ? getPhyCalcData(val[attackType], levels.intelligence) : 0;
    const calcFai = isScale[attackType + "ScalingFai"] === 1 ? getPhyCalcData(val[attackType], levels.faith) : 0;
    const calcArc = isScale[attackType + "ScalingArc"] === 1 ? getPhyCalcData(val[attackType], levels.arcane) : 0;

    if (maxUpgrade === 10) {
        basePhys = val[shortAttackType + weaponLevel.somber];
        phsyStr = basePhys * (val['str' + weaponLevel.somber] * calcStr / 100);
        phsyDex = basePhys * (val['dex' + weaponLevel.somber] * calcDex / 100);
        phsyInt = basePhys * (val['int' + weaponLevel.somber] * calcInt / 100);
        phsyFai = basePhys * (val['fai' + weaponLevel.somber] * calcFai / 100);
        phsyArc = basePhys * (val['arc' + weaponLevel.somber] * calcArc / 100);
    } else if (maxUpgrade === 25) {
        basePhys = val[shortAttackType + weaponLevel.smithing];
        phsyStr = basePhys * (val['str' + weaponLevel.smithing] * calcStr / 100);
        phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * calcDex / 100);
        phsyInt = basePhys * (val['int' + weaponLevel.smithing] * calcInt / 100);
        phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * calcFai / 100);
        phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * calcArc / 100);
    } else if (maxUpgrade === 0) {
        basePhys = val[shortAttackType + 0];
        phsyStr = basePhys * (val['str' + 0] * calcStr / 100);
        phsyDex = basePhys * (val['dex' + 0] * calcDex / 100);
        phsyInt = basePhys * (val['int' + 0] * calcInt / 100);
        phsyFai = basePhys * (val['fai' + 0] * calcFai / 100);
        phsyArc = basePhys * (val['arc' + 0] * calcArc / 100);
    }

    if ((strength < val.strreq && calcStr !== 0) ||
        (levels.dexterity < val.dexreq && calcDex !== 0) ||
        (levels.intelligence < val.intreq && calcInt !== 0) ||
        (levels.faith < val.faireq && calcFai !== 0) ||
        (levels.arcane < val.arcreq && calcArc !== 0)
    ) {
        return basePhys - (basePhys * 0.4);
    }

    return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

};

function getPhyData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, 'physical', 'phys');
};

function getMagData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, 'magic', 'mag');
};

function getFireData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, 'fire', 'fire');
};

function getLighData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, 'lightning', 'ligh');
};

function getHolyData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    return getSingleARData(val, maxUpgrade, weaponLevel, levels, twoHanded, 'holy', 'holy');
};

function getSorceryScaling(val, maxUpgrade, weaponLevel, levels, twoHanded) {
    let phsyStr = 0;
    let phsyDex = 0;
    let phsyInt = 0;
    let phsyFai = 0;
    let phsyArc = 0;

    let isSorcererScaling = val.attackelementcorrectId >= 20000 ? true : false;

    if (isSorcererScaling === false) {
        return 0;
    }

    let isScale = {};

    for (const element of Attack_Element_Correct_Param) {
        if (element.rowId === val.attackelementcorrectId) {
            isScale = element;
            break;
        }
    }

    let strength = levels.strength;
    if (twoHanded === true && !noTwoHandBuff.has(val.weaponname)) {
        strength = levels.twohand_strength;
    }

    const physMagStr = isScale.magicScalingStr === 1 ? getPhyCalcData(val.magic, strength) : 0;
    const physMagDex = isScale.magicScalingDex === 1 ? getPhyCalcData(val.magic, levels.dexterity) : 0;
    const physMagInt = isScale.magicScalingInt === 1 ? getPhyCalcData(val.magic, levels.intelligence) : 0;
    const physMagFai = isScale.magicScalingFai === 1 ? getPhyCalcData(val.magic, levels.faith) : 0;
    const physMagArc = isScale.magicScalingArc === 1 ? getPhyCalcData(val.magic, levels.arcane) : 0;

    if (maxUpgrade === 10) {
        phsyStr = (val['str' + weaponLevel.somber] * physMagStr);
        phsyDex = (val['dex' + weaponLevel.somber] * physMagDex);
        phsyInt = (val['int' + weaponLevel.somber] * physMagInt);
        phsyFai = (val['fai' + weaponLevel.somber] * physMagFai);
        phsyArc = (val['arc' + weaponLevel.somber] * physMagArc);
    } else if (maxUpgrade === 25) {
        phsyStr = (val['str' + weaponLevel.smithing] * physMagStr);
        phsyDex = (val['dex' + weaponLevel.smithing] * physMagDex);
        phsyInt = (val['int' + weaponLevel.smithing] * physMagInt);
        phsyFai = (val['fai' + weaponLevel.smithing] * physMagFai);
        phsyArc = (val['arc' + weaponLevel.smithing] * physMagArc);
    } else if (maxUpgrade === 0) {
        phsyStr = (val['str' + 0] * physMagStr);
        phsyDex = (val['dex' + 0] * physMagDex);
        phsyInt = (val['int' + 0] * physMagInt);
        phsyFai = (val['fai' + 0] * physMagFai);
        phsyArc = (val['arc' + 0] * physMagArc);
    }

    return 100 + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;
};

function getScalingLetter(val, maxUpgrade, weaponLevel, type) {
    let output = { letter: '-', value: 0 };
    let scaleNum = 0;
    if (maxUpgrade === 10) {
        const scaling = val[type + weaponLevel.somber];
        scaleNum = scaling * 100;
        if (scaleNum === 0) {
            return output;
        } else if (scaleNum >= scalingValues.S) {
            output = 'S';
        } else if (scaleNum >= scalingValues.A) {
            output = 'A';
        } else if (scaleNum >= scalingValues.B) {
            output = 'B';
        } else if (scaleNum >= scalingValues.C) {
            output = 'C';
        } else if (scaleNum >= scalingValues.D) {
            output = 'D';
        } else {
            output = 'E';
        }
    } else if (maxUpgrade === 25) {
        const scaling = val[type + weaponLevel.smithing];
        scaleNum = scaling * 100;
        if (scaleNum === 0) {
            return output;
        } else if (scaleNum >= scalingValues.S) {
            output = 'S';
        } else if (scaleNum >= scalingValues.A) {
            output = 'A';
        } else if (scaleNum >= scalingValues.B) {
            output = 'B';
        } else if (scaleNum >= scalingValues.C) {
            output = 'C';
        } else if (scaleNum >= scalingValues.D) {
            output = 'D';
        } else {
            output = 'E';
        }
    } else if (maxUpgrade === 0) {
        const scaling = val[type + 0];
        scaleNum = scaling * 100;
        if (scaleNum === 0) {
            return output;
        } else if (scaleNum >= scalingValues.S) {
            output = 'S';
        } else if (scaleNum >= scalingValues.A) {
            output = 'A';
        } else if (scaleNum >= scalingValues.B) {
            output = 'B';
        } else if (scaleNum >= scalingValues.C) {
            output = 'C';
        } else if (scaleNum >= scalingValues.D) {
            output = 'D';
        } else {
            output = 'E';
        }
    }

    return { letter: output, value: Math.trunc(scaleNum) };
};

function getPassiveData(val, maxUpgrade, weaponLevel, levels) {
    let physRotMadSleep = 0;
    let physFrost = 0;
    let phsyPoison = 0;
    let phsyBlood = 0;
    let arcScaling = 0;


    let passiveArcaneCalcCorrect = 0;
    const passiveArcaneScale = Physical_Calculations[passiveArcaneScaleId];
    if (levels.arcane > passiveArcaneScale.stat_max_3) {
        // Don't know what to do if adjustment is 0
        if (passiveArcaneScale.adj_point_3 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_3 + ((passiveArcaneScale.grow_4 - passiveArcaneScale.grow_3) * (((levels.arcane - passiveArcaneScale.stat_max_3) / (passiveArcaneScale.stat_max_4 - passiveArcaneScale.stat_max_3)) ** passiveArcaneScale.adj_point_3))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_3 + ((passiveArcaneScale.grow_4 - passiveArcaneScale.grow_3) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_3) / (passiveArcaneScale.stat_max_4 - passiveArcaneScale.stat_max_3))) ** -passiveArcaneScale.adj_point_3)))
        }
    }
    else if (levels.arcane > passiveArcaneScale.stat_max_2) {
        if (passiveArcaneScale.adj_point_2 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_2 + ((passiveArcaneScale.grow_3 - passiveArcaneScale.grow_2) * (((levels.arcane - passiveArcaneScale.stat_max_2) / (passiveArcaneScale.stat_max_3 - passiveArcaneScale.stat_max_2)) ** passiveArcaneScale.adj_point_2))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_2 + ((passiveArcaneScale.grow_3 - passiveArcaneScale.grow_2) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_2) / (passiveArcaneScale.stat_max_3 - passiveArcaneScale.stat_max_2))) ** -passiveArcaneScale.adj_point_2)))
        }
    }
    else if (levels.arcane > passiveArcaneScale.stat_max_1) {
        if (passiveArcaneScale.adj_point_1 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_1 + ((passiveArcaneScale.grow_2 - passiveArcaneScale.grow_1) * (((levels.arcane - passiveArcaneScale.stat_max_1) / (passiveArcaneScale.stat_max_2 - passiveArcaneScale.stat_max_1)) ** passiveArcaneScale.adj_point_1))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_1 + ((passiveArcaneScale.grow_2 - passiveArcaneScale.grow_1) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_1) / (passiveArcaneScale.stat_max_2 - passiveArcaneScale.stat_max_1))) ** -passiveArcaneScale.adj_point_1)))
        }
    }
    else {
        if (passiveArcaneScale.adj_point_0 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_0 + ((passiveArcaneScale.grow_1 - passiveArcaneScale.grow_0) * (((levels.arcane - passiveArcaneScale.stat_max_0) / (passiveArcaneScale.stat_max_1 - passiveArcaneScale.stat_max_0)) ** passiveArcaneScale.adj_point_0))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_0 + ((passiveArcaneScale.grow_1 - passiveArcaneScale.grow_0) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_0) / (passiveArcaneScale.stat_max_1 - passiveArcaneScale.stat_max_0))) ** -passiveArcaneScale.adj_point_0)))
        }
    }

    passiveArcaneCalcCorrect /= 100;

    let type = "scarletRot"; // default rot
    if (val.type1 === "Madness") {
        type = "madness";
    } else if (val.type1 === "Sleep") {
        type = "sleep";
    }

    physRotMadSleep = val[type + '0'];

    if (maxUpgrade === 10) {
        physFrost = val['frost' + weaponLevel.somber];
        phsyPoison = val['poison' + weaponLevel.somber];
        phsyBlood = val['blood' + weaponLevel.somber];
        arcScaling = val['arc' + weaponLevel.somber]
    } else if (maxUpgrade === 25) {
        physFrost = val['frost' + weaponLevel.smithing];
        phsyPoison = val['poison' + weaponLevel.smithing];
        phsyBlood = val['blood' + weaponLevel.smithing];
        arcScaling = val['arc' + weaponLevel.smithing]
    } else if (maxUpgrade === 0) {
        physFrost = val['frost0'];
        phsyPoison = val['poison0'];
        phsyBlood = val['blood0'];
        arcScaling = val['arc0']
    }

    if (val.fullweaponname === "Cold Antspur Rapier") {
        switch (weaponLevel.smithing) {
            case 0:
                return 50;
            case 1:
                return 55;
            case 2:
                return 60;
            case 3:
                return 65;
            case 4:
                return 70;
            case 5:
                return 75;
            default:
                return 0;
        }
    } else if (val.fullweaponname === "Poison Fingerprint Stone Shield" || val.fullweaponname === "Blood Fingerprint Stone Shield") {
        if (arcScaling > 0) {
            return (arcScaling * passiveArcaneCalcCorrect * physRotMadSleep) + physRotMadSleep;
        } else {
            return physRotMadSleep;
        }
    } else if (val.fullweaponname === "Occult Fingerprint Stone Shield") {
        return 0;
    } else {
        switch (val.type1) {
            case "Scarlet Rot":
            case "Madness":
            case "Sleep":
                return physRotMadSleep;
            case "Frost":
                return physFrost;
            case "Poison":
                if (arcScaling > 0) {
                    return (arcScaling * passiveArcaneCalcCorrect * phsyPoison) + phsyPoison;
                }
                return phsyPoison;
            case "Blood":
                if (arcScaling > 0) {
                    return (arcScaling * passiveArcaneCalcCorrect * phsyBlood) + phsyBlood;
                }
                return phsyBlood;
            default:
                return 0;
        }

    }
};

function getPassiveData2(val, maxUpgrade, weaponLevel, levels) {
    let physRotMadSleep = 0;
    let physFrost = 0;
    let phsyPoison = 0;
    let phsyBlood = 0;
    let arcScaling = 0;

    let passiveArcaneCalcCorrect = 0;
    const passiveArcaneScale = Physical_Calculations[passiveArcaneScaleId];
    if (levels.arcane > passiveArcaneScale.stat_max_3) {
        // Don't know what to do if adjustment is 0
        if (passiveArcaneScale.adj_point_3 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_3 + ((passiveArcaneScale.grow_4 - passiveArcaneScale.grow_3) * (((levels.arcane - passiveArcaneScale.stat_max_3) / (passiveArcaneScale.stat_max_4 - passiveArcaneScale.stat_max_3)) ** passiveArcaneScale.adj_point_3))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_3 + ((passiveArcaneScale.grow_4 - passiveArcaneScale.grow_3) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_3) / (passiveArcaneScale.stat_max_4 - passiveArcaneScale.stat_max_3))) ** -passiveArcaneScale.adj_point_3)))
        }
    }
    else if (levels.arcane > passiveArcaneScale.stat_max_2) {
        if (passiveArcaneScale.adj_point_2 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_2 + ((passiveArcaneScale.grow_3 - passiveArcaneScale.grow_2) * (((levels.arcane - passiveArcaneScale.stat_max_2) / (passiveArcaneScale.stat_max_3 - passiveArcaneScale.stat_max_2)) ** passiveArcaneScale.adj_point_2))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_2 + ((passiveArcaneScale.grow_3 - passiveArcaneScale.grow_2) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_2) / (passiveArcaneScale.stat_max_3 - passiveArcaneScale.stat_max_2))) ** -passiveArcaneScale.adj_point_2)))
        }
    }
    else if (levels.arcane > passiveArcaneScale.stat_max_1) {
        if (passiveArcaneScale.adj_point_1 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_1 + ((passiveArcaneScale.grow_2 - passiveArcaneScale.grow_1) * (((levels.arcane - passiveArcaneScale.stat_max_1) / (passiveArcaneScale.stat_max_2 - passiveArcaneScale.stat_max_1)) ** passiveArcaneScale.adj_point_1))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_1 + ((passiveArcaneScale.grow_2 - passiveArcaneScale.grow_1) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_1) / (passiveArcaneScale.stat_max_2 - passiveArcaneScale.stat_max_1))) ** -passiveArcaneScale.adj_point_1)))
        }
    }
    else {
        if (passiveArcaneScale.adj_point_0 > 0.0) {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_0 + ((passiveArcaneScale.grow_1 - passiveArcaneScale.grow_0) * (((levels.arcane - passiveArcaneScale.stat_max_0) / (passiveArcaneScale.stat_max_1 - passiveArcaneScale.stat_max_0)) ** passiveArcaneScale.adj_point_0))
        }
        else {
            passiveArcaneCalcCorrect = passiveArcaneScale.grow_0 + ((passiveArcaneScale.grow_1 - passiveArcaneScale.grow_0) * (1 - ((1 - ((levels.arcane - passiveArcaneScale.stat_max_0) / (passiveArcaneScale.stat_max_1 - passiveArcaneScale.stat_max_0))) ** -passiveArcaneScale.adj_point_0)))
        }
    }

    passiveArcaneCalcCorrect /= 100;

    let type = "scarletRot"; // default rot
    if (val.type2 === "Madness") {
        type = "madness";
    } else if (val.type2 === "Sleep") {
        type = "sleep";
    }

    if (maxUpgrade === 10) {
        physRotMadSleep = val[type + weaponLevel.somber];
        physFrost = val['frost' + weaponLevel.somber];
        phsyPoison = val['poison' + weaponLevel.somber];
        phsyBlood = val['blood' + weaponLevel.somber];
        arcScaling = val['arc' + weaponLevel.somber]
    } else if (maxUpgrade === 25) {
        physRotMadSleep = val[type + weaponLevel.smithing];
        physFrost = val['frost' + weaponLevel.smithing];
        phsyPoison = val['poison' + weaponLevel.smithing];
        phsyBlood = val['blood' + weaponLevel.smithing];
        arcScaling = val['arc' + weaponLevel.smithing]
    } else if (maxUpgrade === 0) {
        physRotMadSleep = val[type + '0'];
        physFrost = val['frost0'];
        phsyPoison = val['poison0'];
        phsyBlood = val['blood0'];
        arcScaling = val['arc0']
    }

    switch (val.type2) {
        case "Scarlet Rot":
        case "Madness":
        case "Sleep":
            return physRotMadSleep;
        case "Frost":
            return physFrost;
        case "Poison":
            if (arcScaling > 0) {
                return (arcScaling * passiveArcaneCalcCorrect * phsyPoison) + phsyPoison;
            }
            return phsyPoison;
        case "Blood":
            if (arcScaling > 0) {
                return (arcScaling * passiveArcaneCalcCorrect * phsyBlood) + phsyBlood;
            }
            return phsyBlood;
        default:
            return 0;

    }
};

function highlightReqRow(val, levels, isTwoHanded) {
    let strength = levels.strength;
    if ((isTwoHanded && !noTwoHandBuff.has(val.weaponname))) {
        strength = levels.twohand_strength;
    }
    if (strength < val.strreq ||
        levels.dexterity < val.dexreq ||
        levels.intelligence < val.intreq ||
        levels.faith < val.faireq ||
        levels.arcane < val.arcreq) {
        return true;
    } else {
        return false;
    }
};

export default function FilterableWeaponTable() {
    const levels = useSelector((state) => state.allLevels.levels);
    const weaponLevels = useSelector((state) => state.allLevels.weaponLevels);
    const twoHanded = useSelector((state) => state.allLevels.twoHanded);

    const [weaponTypeFilter, setWeaponTypeFilter] = useState([]);
    const [affinityTypeFilter, setaffinityTypeFilter] = useState(["None"]);
    const [somberFilter, setSomberFilter] = useState(true);
    const [smithingFilter, setSmithingFilter] = useState(true);
    const [hideNoReqWeapons, setHideNoReqWeapons] = useState(true);
    const [searchedWeapons, setSearchedWeapons] = useState([]);

    const [preppedData, setPreppedData] = useState([]);

    function handleWeaponTypeFilterChange(weaponTypeFilter) {
        setWeaponTypeFilter(weaponTypeFilter);
    };

    function handleAffinityTypeFilterChange(affinityTypeFilter) {
        setaffinityTypeFilter(affinityTypeFilter);
    };

    function handleExtraFilterChange(isChecked, type) {
        if (type === 'somber-weapons') {
            setSomberFilter(isChecked);
        } else if (type === 'smithing-weapons') {
            setSmithingFilter(isChecked);
        } else if (type === 'missing-req-weapons') {
            setHideNoReqWeapons(isChecked);
        }
    };

    function handleSearchItemsChange(searchedWeapons) {
        setSearchedWeapons(searchedWeapons);
    };

    useEffect(() => {
        let data = [...Table_Data];

        //calc data
        data.forEach((val) => {
            val.final_physical = Math.trunc(getPhyData(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_magic = Math.trunc(getMagData(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_fire = Math.trunc(getFireData(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_lightning = Math.trunc(getLighData(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_holy = Math.trunc(getHolyData(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_total_ar = Math.trunc(totalAR(val, val.maxUpgrade, weaponLevels, levels, twoHanded));
            val.final_sorcery_scaling = Math.trunc(getSorceryScaling(val, val.maxUpgrade, weaponLevels, levels, twoHanded));

            val.str_scaling_letter = getScalingLetter(val, val.maxUpgrade, weaponLevels, "str");
            val.dex_scaling_letter = getScalingLetter(val, val.maxUpgrade, weaponLevels, "dex");
            val.int_scaling_letter = getScalingLetter(val, val.maxUpgrade, weaponLevels, "int");
            val.fai_scaling_letter = getScalingLetter(val, val.maxUpgrade, weaponLevels, "fai");
            val.arc_scaling_letter = getScalingLetter(val, val.maxUpgrade, weaponLevels, "arc");

            // init passives
            for (const passive of passiveTypes) {
                val[passive.replace(/\s+/g, '_').toLowerCase()] = 0;
            }

            const final_passive1 = Math.trunc(getPassiveData(val, val.maxUpgrade, weaponLevels, levels));
            if (val.type1 !== undefined) {
                val[(val.type1).replace(/\s+/g, '_').toLowerCase()] = final_passive1;
            }
            const final_passive2 = Math.trunc(getPassiveData2(val, val.maxUpgrade, weaponLevels, levels));
            if (val.type2 !== undefined) {
                val[(val.type2).replace(/\s+/g, '_').toLowerCase()] = final_passive2;
            }

            if (val.restore_hp_hit_percent === undefined) {
                val.restore_hp_hit_percent = 0;
            }

            if (val.rune_gain_hit === undefined) {
                val.rune_gain_hit = 0;
            }

            val.missedReq = highlightReqRow(val, levels, twoHanded)
        });

        setPreppedData([...data]);
    }, [levels, weaponLevels, twoHanded]);

    return (
        <div className="container">
            <div className="spacing">
                <FilterBar
                    handleWeaponTypeFilterChange={handleWeaponTypeFilterChange}
                    handleAffinityTypeFilterChange={handleAffinityTypeFilterChange}
                    weaponTypeFilter={weaponTypeFilter}
                    affinityTypeFilter={affinityTypeFilter}
                />

                <ExtraFilters
                    handleExtraFilterChange={handleExtraFilterChange}
                    somberFilter={somberFilter}
                    smithingFilter={smithingFilter}
                    hideNoReqWeapons={hideNoReqWeapons}
                />

                <SearchBar
                    handleSearchItemsChange={handleSearchItemsChange}
                    searchedItems={searchedWeapons}
                    options={Weapon_Groups}
                    placeholder="Search weapons... Select affinities using filter."
                />

            </div>
            <WeaponTable
                weaponTypeFilter={weaponTypeFilter}
                affinityTypeFilter={affinityTypeFilter}
                somberFilter={somberFilter}
                smithingFilter={smithingFilter}
                hideNoReqWeapons={hideNoReqWeapons}
                searchedWeapons={searchedWeapons.map(row => row.label)}
                preppedData={preppedData}
            />

        </div>
    );
}