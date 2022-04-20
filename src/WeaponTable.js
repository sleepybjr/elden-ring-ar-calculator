import React, { Component } from 'react'

import Attack_Element_Correct_Param from './json/attackelementcorrectparam';
import Physical_Calculations from './json/physical_calculations.json';
import Table_Data from './json/merged_json_data';

const typesOrder = {
    'S': 0,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    '-': 6,
};

const scalingValues = {
    // In MenuValueTableParam
    'S': 175,
    'A': 140,
    'B': 90,
    'C': 60,
    'D': 25,
    'E': 1
}

const noTwoHandBuff = new Set([
    "Hookclaws", "Venomous Fang", "Bloodhound Claws", "Raptor Talons",
    "Caestus", "Spiked Caestus", "Grafted Dragon", "Iron Ball", "Star Fist", "Katar", "Clinging Bone", "Veteran's Prosthesis", "Cipher Pata",
    "Starscourge Greatsword",
    "Ornamental Straight Sword",
]);
const autoTwoHandBuff = new Set([
    "Light Bow", "Bow", "Greatbow",
]);

const passiveArcaneScaleId = 6;

export default class WeaponTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            sort: {
                column: null,
                direction: null,
            },
        };
    }

    onSort = (column) => (e) => {
        let direction = null;
        if (column === this.state.sort.column) {
            if (this.state.sort.direction === null) {
                direction = 'asc';
            } else if (this.state.sort.direction === 'asc') {
                direction = 'desc';
            } else {
                direction = null;
            }
        } else {
            direction = 'asc';
        }

        this.setState({
            sort: {
                column,
                direction,
            }
        });
    };

    filterBySearchedWeapons(searchedWeapons) {
        return function (row) {
            return searchedWeapons.includes(row.weaponname);
        };
    };

    filterByWeaponTypes(weaponTypes) {
        return function (row) {
            return weaponTypes.includes(row.weaponType);
        };
    };

    filterByAffinityTypes(affinityTypes) {
        return function (row) {
            if (row.maxUpgrade === 25)
                return affinityTypes.includes(row.affinity);
            return true;
        };
    };

    prepareData = () => {
        const data = Table_Data;
        const searchedWeaponsFilter = this.props.searchedWeapons.map(row => row.label);
        const filteredDataSearched = data.filter(this.filterBySearchedWeapons(searchedWeaponsFilter));
        const weaponTypeFilter = this.props.weaponTypeFilter;
        const affinityTypeFilter = this.props.affinityTypeFilter;
        const filteredDataWeapon = data.filter(this.filterByWeaponTypes(weaponTypeFilter));
        const filteredDataSomber = this.props.somberFilter === true ? filteredDataWeapon : filteredDataWeapon.filter((weapon) => weapon.maxUpgrade !== 10 && weapon.maxUpgrade !== 0);
        const filteredDataSmithing = this.props.smithingFilter === true ? filteredDataSomber : filteredDataSomber.filter((weapon) => weapon.maxUpgrade !== 25);
        const filteredDataReqWeapons = this.props.hideNoReqWeapons === true ? filteredDataSmithing : filteredDataSmithing.filter((weapon) => this.highlightReqRow(weapon, this.props.levels, this.props.twoHanded) === false);

        const filteredDataAffinity = filteredDataSearched.concat(filteredDataReqWeapons).filter(this.filterByAffinityTypes(affinityTypeFilter));

        return filteredDataAffinity;
    };

    highlightReqRow(val, levels, isTwoHanded) {
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

    render() {
        const totalAR = function (val, maxUpgrade, weaponLevel, levels, twoHanded) {
            return getPhyData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
                getMagData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
                getFireData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
                getLighData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
                getHolyData(val, maxUpgrade, weaponLevel, levels, twoHanded);
        };

        function getPhyCalcData(physScale, level) {
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

        function getPhyData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
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

            const physCalcStr = isScale.physicalScalingStr === 1 ? getPhyCalcData(val.physical, strength) : 0;
            const physCalcDex = isScale.physicalScalingDex === 1 ? getPhyCalcData(val.physical, levels.dexterity) : 0;
            const physCalcInt = isScale.physicalScalingInt === 1 ? getPhyCalcData(val.physical, levels.intelligence) : 0;
            const physCalcFai = isScale.physicalScalingFai === 1 ? getPhyCalcData(val.physical, levels.faith) : 0;
            const physCalcArc = isScale.physicalScalingArc === 1 ? getPhyCalcData(val.physical, levels.arcane) : 0;

            if (maxUpgrade === 10) {
                basePhys = val['phys' + weaponLevel.somber];
                phsyStr = basePhys * (val['str' + weaponLevel.somber] * physCalcStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.somber] * physCalcDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.somber] * physCalcInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.somber] * physCalcFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.somber] * physCalcArc / 100);
            } else if (maxUpgrade === 25) {
                basePhys = val['phys' + weaponLevel.smithing];
                phsyStr = basePhys * (val['str' + weaponLevel.smithing] * physCalcStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * physCalcDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.smithing] * physCalcInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * physCalcFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * physCalcArc / 100);
            } else if (maxUpgrade === 0) {
                basePhys = val['phys' + 0];
                phsyStr = basePhys * (val['str' + 0] * physCalcStr / 100);
                phsyDex = basePhys * (val['dex' + 0] * physCalcDex / 100);
                phsyInt = basePhys * (val['int' + 0] * physCalcInt / 100);
                phsyFai = basePhys * (val['fai' + 0] * physCalcFai / 100);
                phsyArc = basePhys * (val['arc' + 0] * physCalcArc / 100);
            }

            if ((strength < val.strreq && physCalcStr !== 0) ||
                (levels.dexterity < val.dexreq && physCalcDex !== 0) ||
                (levels.intelligence < val.intreq && physCalcInt !== 0) ||
                (levels.faith < val.faireq && physCalcFai !== 0) ||
                (levels.arcane < val.arcreq && physCalcArc !== 0)
            ) {
                return basePhys - (basePhys * 0.4);
            }

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getMagData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
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

            const physMagStr = isScale.magicScalingStr === 1 ? getPhyCalcData(val.magic, strength) : 0;
            const physMagDex = isScale.magicScalingDex === 1 ? getPhyCalcData(val.magic, levels.dexterity) : 0;
            const physMagInt = isScale.magicScalingInt === 1 ? getPhyCalcData(val.magic, levels.intelligence) : 0;
            const physMagFai = isScale.magicScalingFai === 1 ? getPhyCalcData(val.magic, levels.faith) : 0;
            const physMagArc = isScale.magicScalingArc === 1 ? getPhyCalcData(val.magic, levels.arcane) : 0;

            if (maxUpgrade === 10) {
                basePhys = val['mag' + weaponLevel.somber];
                phsyStr = basePhys * (val['str' + weaponLevel.somber] * physMagStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.somber] * physMagDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.somber] * physMagInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.somber] * physMagFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.somber] * physMagArc / 100);
            } else if (maxUpgrade === 25) {
                basePhys = val['mag' + weaponLevel.smithing];
                phsyStr = basePhys * (val['str' + weaponLevel.smithing] * physMagStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * physMagDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.smithing] * physMagInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * physMagFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * physMagArc / 100);
            } else if (maxUpgrade === 0) {
                basePhys = val['mag' + 0];
                phsyStr = basePhys * (val['str' + 0] * physMagStr / 100);
                phsyDex = basePhys * (val['dex' + 0] * physMagDex / 100);
                phsyInt = basePhys * (val['int' + 0] * physMagInt / 100);
                phsyFai = basePhys * (val['fai' + 0] * physMagFai / 100);
                phsyArc = basePhys * (val['arc' + 0] * physMagArc / 100);
            }

            if ((strength < val.strreq && physMagStr !== 0) ||
                (levels.dexterity < val.dexreq && physMagDex !== 0) ||
                (levels.intelligence < val.intreq && physMagInt !== 0) ||
                (levels.faith < val.faireq && physMagFai !== 0) ||
                (levels.arcane < val.arcreq && physMagArc !== 0)
            ) {
                return basePhys - (basePhys * 0.4);
            }

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getFireData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
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

            const physFireStr = isScale.fireScalingStr === 1 ? getPhyCalcData(val.fire, strength) : 0;
            const physFireDex = isScale.fireScalingDex === 1 ? getPhyCalcData(val.fire, levels.dexterity) : 0;
            const physFireInt = isScale.fireScalingInt === 1 ? getPhyCalcData(val.fire, levels.intelligence) : 0;
            const physFireFai = isScale.fireScalingFai === 1 ? getPhyCalcData(val.fire, levels.faith) : 0;
            const physFireArc = isScale.fireScalingArc === 1 ? getPhyCalcData(val.fire, levels.arcane) : 0;

            if (maxUpgrade === 10) {
                basePhys = val['fire' + weaponLevel.somber];
                phsyStr = basePhys * (val['str' + weaponLevel.somber] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.somber] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.somber] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.somber] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.somber] * physFireArc / 100);
            } else if (maxUpgrade === 25) {
                basePhys = val['fire' + weaponLevel.smithing];
                phsyStr = basePhys * (val['str' + weaponLevel.smithing] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.smithing] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * physFireArc / 100);
            } else if (maxUpgrade === 0) {
                basePhys = val['fire' + 0];
                phsyStr = basePhys * (val['str' + 0] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + 0] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + 0] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + 0] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + 0] * physFireArc / 100);
            }

            if ((strength < val.strreq && physFireStr !== 0) ||
                (levels.dexterity < val.dexreq && physFireDex !== 0) ||
                (levels.intelligence < val.intreq && physFireInt !== 0) ||
                (levels.faith < val.faireq && physFireFai !== 0) ||
                (levels.arcane < val.arcreq && physFireArc !== 0)
            ) {
                return basePhys - (basePhys * 0.4);
            }

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getLighData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
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

            const physFireStr = isScale.lightningScalingStr === 1 ? getPhyCalcData(val.lightning, strength) : 0;
            const physFireDex = isScale.lightningScalingDex === 1 ? getPhyCalcData(val.lightning, levels.dexterity) : 0;
            const physFireInt = isScale.lightningScalingInt === 1 ? getPhyCalcData(val.lightning, levels.intelligence) : 0;
            const physFireFai = isScale.lightningScalingFai === 1 ? getPhyCalcData(val.lightning, levels.faith) : 0;
            const physFireArc = isScale.lightningScalingArc === 1 ? getPhyCalcData(val.lightning, levels.arcane) : 0;

            if (maxUpgrade === 10) {
                basePhys = val['ligh' + weaponLevel.somber];
                phsyStr = basePhys * (val['str' + weaponLevel.somber] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.somber] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.somber] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.somber] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.somber] * physFireArc / 100);
            } else if (maxUpgrade === 25) {
                basePhys = val['ligh' + weaponLevel.smithing];
                phsyStr = basePhys * (val['str' + weaponLevel.smithing] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.smithing] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * physFireArc / 100);
            } else if (maxUpgrade === 0) {
                basePhys = val['ligh' + 0];
                phsyStr = basePhys * (val['str' + 0] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + 0] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + 0] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + 0] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + 0] * physFireArc / 100);
            }

            if ((strength < val.strreq && physFireStr !== 0) ||
                (levels.dexterity < val.dexreq && physFireStr !== 0) ||
                (levels.intelligence < val.intreq && physFireStr !== 0) ||
                (levels.faith < val.faireq && physFireStr !== 0) ||
                (levels.arcane < val.arcreq && physFireStr !== 0)
            ) {
                return basePhys - (basePhys * 0.4);
            }

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getHolyData(val, maxUpgrade, weaponLevel, levels, twoHanded) {
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

            const physFireStr = isScale.holyScalingStr === 1 ? getPhyCalcData(val.holy, strength) : 0;
            const physFireDex = isScale.holyScalingDex === 1 ? getPhyCalcData(val.holy, levels.dexterity) : 0;
            const physFireInt = isScale.holyScalingInt === 1 ? getPhyCalcData(val.holy, levels.intelligence) : 0;
            const physFireFai = isScale.holyScalingFai === 1 ? getPhyCalcData(val.holy, levels.faith) : 0;
            const physFireArc = isScale.holyScalingArc === 1 ? getPhyCalcData(val.holy, levels.arcane) : 0;

            if (maxUpgrade === 10) {
                basePhys = val['holy' + weaponLevel.somber];
                phsyStr = basePhys * (val['str' + weaponLevel.somber] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.somber] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.somber] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.somber] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.somber] * physFireArc / 100);
            } else if (maxUpgrade === 25) {
                basePhys = val['holy' + weaponLevel.smithing];
                phsyStr = basePhys * (val['str' + weaponLevel.smithing] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + weaponLevel.smithing] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + weaponLevel.smithing] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + weaponLevel.smithing] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + weaponLevel.smithing] * physFireArc / 100);
            } else if (maxUpgrade === 0) {
                basePhys = val['holy' + 0];
                phsyStr = basePhys * (val['str' + 0] * physFireStr / 100);
                phsyDex = basePhys * (val['dex' + 0] * physFireDex / 100);
                phsyInt = basePhys * (val['int' + 0] * physFireInt / 100);
                phsyFai = basePhys * (val['fai' + 0] * physFireFai / 100);
                phsyArc = basePhys * (val['arc' + 0] * physFireArc / 100);
            }

            if ((strength < val.strreq && physFireStr !== 0) ||
                (levels.dexterity < val.dexreq && physFireDex !== 0) ||
                (levels.intelligence < val.intreq && physFireInt !== 0) ||
                (levels.faith < val.faireq && physFireFai !== 0) ||
                (levels.arcane < val.arcreq && physFireArc !== 0)
            ) {
                return basePhys - (basePhys * 0.4);
            }

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

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

        let data = this.prepareData();

        //calc data
        data.forEach((val) => {
            val.final_physical = Math.trunc(getPhyData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_magic = Math.trunc(getMagData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_fire = Math.trunc(getFireData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_lightning = Math.trunc(getLighData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_holy = Math.trunc(getHolyData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_total_ar = Math.trunc(totalAR(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_sorcery_scaling = Math.trunc(getSorceryScaling(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));

            val.str_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "str");
            val.dex_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "dex");
            val.int_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "int");
            val.fai_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "fai");
            val.arc_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "arc");

            val.final_passive1 = Math.trunc(getPassiveData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
            val.final_passive2 = Math.trunc(getPassiveData2(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
        });

        let sortedData = data;
        if (this.state.sort.direction !== null) {
            sortedData = data.sort((a, b) => {
                if (new Set(['fullweaponname', 'weaponType', 'affinity', 'type1', 'type2']).has(this.state.sort.column)) {
                    let column = this.state.sort.column;

                    if ('fullweaponname' === this.state.sort.column) {
                        column = 'weaponname';
                    }

                    const nameA = a[column] ? a[column].toUpperCase() : 'Ω';
                    const nameB = b[column] ? b[column].toUpperCase() : 'Ω';
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }

                    if (new Set(['type1', 'type2']).has(this.state.sort.column)) {
                        const second_sort = this.state.sort.column === 'type1' ? 'final_passive1' : 'final_passive2';
                        return b[second_sort] - a[second_sort];
                    }

                    return 0;
                } else if (new Set(['str_scaling_letter', 'dex_scaling_letter', 'int_scaling_letter', 'fai_scaling_letter', 'arc_scaling_letter']).has(this.state.sort.column)) {
                    const A = a[this.state.sort.column];
                    const B = b[this.state.sort.column];

                    const letterAOrder = typesOrder[A.letter];
                    const letterBOrder = typesOrder[B.letter];

                    const order = letterAOrder - letterBOrder;

                    if (order !== 0) {
                        return order;
                    }

                    return B.value - A.value;
                } else {
                    return b[this.state.sort.column] - a[this.state.sort.column];
                }
            });

            if (this.state.sort.direction === 'desc') {
                sortedData.reverse();
            }
        }

        return (
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>
                                <button type="button"
                                    className={'fullweaponname' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('fullweaponname')}>
                                    Weapon Name
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'weaponType' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('weaponType')}>
                                    Weapon Type
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'affinity' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('affinity')}>
                                    Affinity
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_physical' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_physical')}>
                                    Physical
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_magic' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_magic')}>
                                    Magic
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_fire' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_fire')}>
                                    Fire
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_lightning' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_lightning')}>
                                    Lightning
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_holy' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_holy')}>
                                    Holy
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_total_ar' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_total_ar')}>
                                    Total AR
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_sorcery_scaling' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_sorcery_scaling')}>
                                    Sorcery Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'type1' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('type1')}>
                                    Passive 1
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_passive1' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_passive1')}>
                                    Passive 1 Damage
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'type2' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('type2')}>
                                    Passive 2
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'final_passive2' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('final_passive2')}>
                                    Passive 2 Damage
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'str_scaling_letter' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('str_scaling_letter')}>
                                    STR Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'dex_scaling_letter' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('dex_scaling_letter')}>
                                    DEX Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'int_scaling_letter' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('int_scaling_letter')}>
                                    INT Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'fai_scaling_letter' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('fai_scaling_letter')}>
                                    FAI Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'arc_scaling_letter' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('arc_scaling_letter')}>
                                    ARC Scaling
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'strreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('strreq')}>
                                    STR Req
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'dexreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('dexreq')}>
                                    DEX Req
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'intreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('intreq')}>
                                    INT Req
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'faireq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('faireq')}>
                                    FAI Req
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'arcreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('arcreq')}>
                                    ARC Req
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'maxUpgrade' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('maxUpgrade')}>
                                    Upgrade
                                </button>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((val, key) => {
                            return (
                                <tr className={this.highlightReqRow(val, this.props.levels, this.props.twoHanded) ? "highlight-red" : "" } key={key}>
                                    <td><a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + val.weaponname} >{val.fullweaponname}</a></td>
                                    <td>{val.weaponType}</td>
                                    <td>{val.affinity}</td>
                                    <td>{val.final_physical}</td>
                                    <td>{val.final_magic}</td>
                                    <td>{val.final_fire}</td>
                                    <td>{val.final_lightning}</td>
                                    <td>{val.final_holy}</td>
                                    <td>{val.final_total_ar}</td>
                                    <td>{val.final_sorcery_scaling}</td>
                                    <td>{val.type1 ? val.type1 : '-'}</td>
                                    <td>{val.final_passive1 !== 0 ? val.final_passive1 : '-'}</td>
                                    <td>{val.type2 ? val.type2 : '-'}</td>
                                    <td>{val.final_passive2 !== 0 ? val.final_passive2 : '-'}</td>
                                    <td>{val.str_scaling_letter.letter !== '-' ? val.str_scaling_letter.letter + ' (' + val.str_scaling_letter.value + ')' : val.str_scaling_letter.letter}</td>
                                    <td>{val.dex_scaling_letter.letter !== '-' ? val.dex_scaling_letter.letter + ' (' + val.dex_scaling_letter.value + ')' : val.dex_scaling_letter.letter}</td>
                                    <td>{val.int_scaling_letter.letter !== '-' ? val.int_scaling_letter.letter + ' (' + val.int_scaling_letter.value + ')' : val.int_scaling_letter.letter}</td>
                                    <td>{val.fai_scaling_letter.letter !== '-' ? val.fai_scaling_letter.letter + ' (' + val.fai_scaling_letter.value + ')' : val.fai_scaling_letter.letter}</td>
                                    <td>{val.arc_scaling_letter.letter !== '-' ? val.arc_scaling_letter.letter + ' (' + val.arc_scaling_letter.value + ')' : val.arc_scaling_letter.letter}</td>
                                    <td>{val.strreq}</td>
                                    <td>{val.dexreq}</td>
                                    <td>{val.intreq}</td>
                                    <td>{val.faireq}</td>
                                    <td>{val.arcreq}</td>
                                    <td>{val.maxUpgrade === 25 ? "Smithing" : "Somber"}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        );
    }
}