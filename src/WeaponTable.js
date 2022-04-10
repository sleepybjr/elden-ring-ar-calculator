import React, { Component } from 'react'

import Weapon_Reqs_Data from './json/weapon_reqs';
import Weapon_Damage from './json/weapon_damage';
import Weapon_Scaling from './json/weapon_scaling';
import Calc_Correct_Id from './json/calc_correct_id';
import Attack_Element_Correct_Param from './json/attackelementcorrectparam';

const merged_weapons = Weapon_Damage.map(x => Object.assign(x, Weapon_Reqs_Data.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const merged_weapons_scaling = Weapon_Scaling.map(x => Object.assign(x, merged_weapons.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const merged_weapons_all = Calc_Correct_Id.map(x => Object.assign(x, merged_weapons_scaling.find(y => y.fullweaponname.toUpperCase() === x.name.toUpperCase())));
const typesOrder = {
    'S' : 0, 
    'A' : 1, 
    'B' : 2, 
    'C' : 3, 
    'D' : 4, 
    'E' : 5, 
    '-' : 6,
};

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

    filterByWeaponTypes(weaponTypes) {
        return function (row) {
            return weaponTypes.includes(row.weaponType);
        };
    };

    filterByAffinityTypes(affinityTypes) {
        return function (row) {
            return affinityTypes.includes(row.affinity);
        };
    };

    prepareData = () => {
        const data = merged_weapons_all;
        const weaponTypeFilter = this.props.weaponTypeFilter;
        const affinityTypeFilter = this.props.affinityTypeFilter;
        const filteredDataWeapon = weaponTypeFilter.length === 0 ? data : data.filter(this.filterByWeaponTypes(weaponTypeFilter));
        const filteredDataAffinity = affinityTypeFilter.length === 0 ? filteredDataWeapon : filteredDataWeapon.filter(this.filterByAffinityTypes(affinityTypeFilter));

        return filteredDataAffinity;
    };

    render() {
        const totalAR = function (val, maxUpgrade, weaponLevel, levels, twoHanded) {
            return getPhyData(val, maxUpgrade, weaponLevel, levels, twoHanded) +
                getMagData(val, maxUpgrade, weaponLevel, levels) +
                getFireData(val, maxUpgrade, weaponLevel, levels) +
                getLighData(val, maxUpgrade, weaponLevel, levels) +
                getHolyData(val, maxUpgrade, weaponLevel, levels);
        };

        const highlightReqRow = function (val, levels, isTwoHanded) {
            let strength = levels.strength;
            if (isTwoHanded) {
                strength = levels.twohand_strength;
            }
            if (strength < val.strreq ||
                levels.dexterity < val.dexreq ||
                levels.intelligence < val.intreq ||
                levels.faith < val.faireq ||
                levels.arcane < val.arcreq) {
                return "#FFBBAE";
            } else {
                return '';
            }
        };

        function getPhyCalcData(physScale, level) {
            let physCalc = 0;

            if (physScale === 0) {
                if (level > 80) {
                    physCalc = 90 + (20 * (level - 80) / 70);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 18) {
                    physCalc = 25 + (50 * (1 - ((1 - ((level - 18) / 42)) ** 1.2)));
                } else {
                    physCalc = 25 * (((level - 1) / 17) ** 1.2);
                }
            } else if (physScale === 1) {
                if (level > 80) {
                    physCalc = 90 + (20 * (level - 80) / 70);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 20) {
                    physCalc = 35 + (40 * (1 - ((1 - ((level - 20) / 40)) ** 1.2)));
                } else {
                    physCalc = 35 * (((level - 1) / 19) ** 1.2);
                }
            } else if (physScale === 2) {
                if (level > 80) {
                    physCalc = 90 + (20 * (level - 80) / 70);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 20) {
                    physCalc = 35 + (40 * (1 - ((1 - ((level - 20) / 40)) ** 1.2)));
                } else {
                    physCalc = 35 * (((level - 1) / 19) ** 1.2);
                }
            } else if (physScale === 4) {
                if (level > 80) {
                    physCalc = 95 + (5 * (level - 80) / 19);
                } else if (level > 50) {
                    physCalc = 80 + (15 * (level - 50) / 30);
                } else if (level > 20) {
                    physCalc = 40 + (40 * (level - 20) / 19);
                } else {
                    physCalc = 40 * (level - 1) / 19;
                }
            } else if (physScale === 7) {
                if (level > 80) {
                    physCalc = 90 + (20 * (level - 80) / 70);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 20) {
                    physCalc = 35 + (40 * (1 - ((1 - ((level - 20) / 40)) ** 1.2)));
                } else {
                    physCalc = 35 * (((level - 1) / 19) ** 1.2);
                }
            } else if (physScale === 8) {
                if (level > 80) {
                    physCalc = 90 + (20 * (level - 80) / 70);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 16) {
                    physCalc = 25 + (50 * (1 - ((1 - ((level - 16) / 44)) ** 1.2)));
                } else {
                    physCalc = 25 * (((level - 1) / 15) ** 1.2);
                }
            } else if (physScale === 12) {
                if (level > 45) {
                    physCalc = 75 + (25 * (level - 45) / 54);
                } else if (level > 30) {
                    physCalc = 55 + (20 * (level - 30) / 15);
                } else if (level > 15) {
                    physCalc = 10 + (45 * (level - 15) / 15);
                } else {
                    physCalc = 10 * (level - 1) / 14;
                }
            } else if (physScale === 14) {
                if (level > 80) {
                    physCalc = 85 + (15 * (level - 80) / 19);
                } else if (level > 40) {
                    physCalc = 60 + (25 * (level - 40) / 40);
                } else if (level > 20) {
                    physCalc = 40 + (20 * (level - 20) / 20);
                } else {
                    physCalc = 40 * (level - 1) / 19;
                }
            } else if (physScale === 15) {
                if (level > 80) {
                    physCalc = 95 + (5 * (level - 80) / 19);
                } else if (level > 60) {
                    physCalc = 65 + (30 * (level - 60) / 20);
                } else if (level > 25) {
                    physCalc = 25 + (40 * (level - 25) / 35);
                } else {
                    physCalc = 25 * (level - 1) / 24;
                }
            } else if (physScale === 16) {
                if (level > 80) {
                    physCalc = 90 + (10 * (level - 80) / 19);
                } else if (level > 60) {
                    physCalc = 75 + (15 * (level - 60) / 20);
                } else if (level > 18) {
                    physCalc = 20 + (55 * (level - 18) / 42);
                } else {
                    physCalc = 20 * (level - 1) / 17;
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
            if (twoHanded === true) {
                strength *= 1.5;
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

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getMagData(val, maxUpgrade, weaponLevel, levels) {
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

            const physMagStr = isScale.magicScalingStr === 1 ? getPhyCalcData(val.magic, levels.strength) : 0;
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

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getFireData(val, maxUpgrade, weaponLevel, levels) {
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

            const physFireStr = isScale.fireScalingStr === 1 ? getPhyCalcData(val.fire, levels.strength) : 0;
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

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getLighData(val, maxUpgrade, weaponLevel, levels) {
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

            const physFireStr = isScale.lightningScalingStr === 1 ? getPhyCalcData(val.lightning, levels.strength) : 0;
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

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getHolyData(val, maxUpgrade, weaponLevel, levels) {
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

            const physFireStr = isScale.holyScalingStr === 1 ? getPhyCalcData(val.holy, levels.strength) : 0;
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

            return basePhys + phsyStr + phsyDex + phsyInt + phsyFai + phsyArc;

        };

        function getSorceryScaling(val, maxUpgrade, weaponLevel, levels) {
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

            const physMagStr = isScale.magicScalingStr === 1 ? getPhyCalcData(val.magic, levels.strength) : 0;
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
            let output = {letter: '-', value: 0};
            let scaleNum = 0;
            if (maxUpgrade === 10) {
                const scaling = val[type + weaponLevel.somber];
                if (scaling === 0) {
                    return output;
                } else if (scaling > 1.75) {
                    output = 'S';
                } else if (scaling >= 1.4) {
                    output = 'A';
                } else if (scaling >= 0.9) {
                    output = 'B';
                } else if (scaling >= 0.6) {
                    output = 'C';
                } else if (scaling >= 0.2) {
                    output = 'D';
                } else {
                    output = 'E';
                }
                scaleNum = scaling * 100;
            } else if (maxUpgrade === 25) {
                const scaling = val[type + weaponLevel.smithing];
                if (scaling === 0) {
                    return output;
                } else if (scaling > 1.75) {
                    output = 'S';
                } else if (scaling >= 1.4) {
                    output = 'A';
                } else if (scaling >= 0.9) {
                    output = 'B';
                } else if (scaling >= 0.6) {
                    output = 'C';
                } else if (scaling >= 0.2) {
                    output = 'D';
                } else {
                    output = 'E';
                }
                scaleNum = scaling * 100;
            } else if (maxUpgrade === 0) {
                const scaling = val[type + 0];
                if (scaling === 0) {
                    return output;
                } else if (scaling > 1.75) {
                    output = 'S';
                } else if (scaling >= 1.4) {
                    output = 'A';
                } else if (scaling >= 0.9) {
                    output = 'B';
                } else if (scaling >= 0.6) {
                    output = 'C';
                } else if (scaling >= 0.2) {
                    output = 'D';
                } else {
                    output = 'E';
                }
                scaleNum = scaling * 100;
            }

            return { letter: output, value: Math.trunc(scaleNum)};
        };

        let data = this.prepareData();

        //calc data
        data.forEach((val) => {
            val.final_physical = Math.trunc(getPhyData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_magic = Math.trunc(getMagData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
            val.final_fire = Math.trunc(getFireData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
            val.final_lightning = Math.trunc(getLighData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
            val.final_holy = Math.trunc(getHolyData(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));
            val.final_total_ar = Math.trunc(totalAR(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels, this.props.twoHanded));
            val.final_sorcery_scaling = Math.trunc(getSorceryScaling(val, val.maxUpgrade, this.props.weaponLevels, this.props.levels));

            val.str_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "str");
            val.dex_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "dex");
            val.int_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "int");
            val.fai_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "fai");
            val.arc_scaling_letter = getScalingLetter(val, val.maxUpgrade, this.props.weaponLevels, "arc");
        });

        let sortedData = data;
        if (this.state.sort.direction !== null) {
            sortedData = data.sort((a, b) => {
                if (['fullweaponname', 'weaponType', 'affinity'].includes(this.state.sort.column)) {
                    const nameA = a[this.state.sort.column].toUpperCase();
                    const nameB = b[this.state.sort.column].toUpperCase();
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }

                    return 0;
                } else if (['str_scaling_letter', 'dex_scaling_letter', 'int_scaling_letter', 'fai_scaling_letter', 'arc_scaling_letter'].includes(this.state.sort.column)) {
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
                                    STR Requirement
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'dexreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('dexreq')}>
                                    DEX Requirement
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'intreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('intreq')}>
                                    INT Requirement
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'faireq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('faireq')}>
                                    FAI Requirement
                                </button>
                            </th>
                            <th>
                                <button type="button"
                                    className={'arcreq' === this.state.sort.column ? this.state.sort.direction === "asc" ? "ascending" : this.state.sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={this.onSort('arcreq')}>
                                    ARC Requirement
                                </button>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((val, key) => {
                            return (
                                <tr style={{ backgroundColor: highlightReqRow(val, this.props.levels, this.props.twoHanded) }} key={key}>
                                    <td>{val.fullweaponname}</td>
                                    <td>{val.weaponType}</td>
                                    <td>{val.affinity}</td>
                                    <td>{val.final_physical}</td>
                                    <td>{val.final_magic}</td>
                                    <td>{val.final_fire}</td>
                                    <td>{val.final_lightning}</td>
                                    <td>{val.final_holy}</td>
                                    <td>{val.final_total_ar}</td>
                                    <td>{val.final_sorcery_scaling}</td>
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
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        );
    }
}