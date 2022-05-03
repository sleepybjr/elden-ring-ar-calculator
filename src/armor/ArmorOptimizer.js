import Armor_Data from '../json/armor/armor_data.json';

import Max_Head from '../json/armor/armor_max/max_head.json';
import Max_Body from '../json/armor/armor_max/max_body.json';
import Max_Arm from '../json/armor/armor_max/max_arm.json';
import Max_Leg from '../json/armor/armor_max/max_leg.json';

import Heap from 'heap-js';

// edge cases
// equipmentload == max equipment load

const resultComparator = (a, b) => b.totalResistanceValueWeighted - a.totalResistanceValueWeighted;
const resultComparatorMin = (a, b) => a.totalResistanceValueWeighted - b.totalResistanceValueWeighted;
const resultComparatorMaxReal = (a, b) => b.robustness - a.robustness;
const MAX_HEAP_LENGTH = 1000;
// const MAX_HEAP_LENGTH_FIRST = 100;
const IS_NOT_WEARING = 1;

const armorResistances = [
    "physical_absorption",
    "strike_absorption",
    "slash_absorption",
    "thrust_absorption",
    "magic_absorption",
    "fire_absorption",
    "lightning_absorption",
    "holy_absorption",
    "immunity",
    "robustness",
    "focus",
    "vitality",
    "poise",
]
const armorAbsorptions = [
    "physical_absorption",
    "strike_absorption",
    "slash_absorption",
    "thrust_absorption",
    "magic_absorption",
    "fire_absorption",
    "lightning_absorption",
    "holy_absorption",
]

const armorRegular = [
    "immunity",
    "robustness",
    "focus",
    "vitality",
    "poise",
]

const fillNoneValue = (armorType) => {
    return {
        "name": "None",
        "equipment_type": armorType,
        "weight": 0,
        "physical_absorption": 0,
        "strike_absorption": 0,
        "slash_absorption": 0,
        "thrust_absorption": 0,
        "magic_absorption": 0,
        "fire_absorption": 0,
        "lightning_absorption": 0,
        "holy_absorption": 0,
        "immunity": 0,
        "robustness": 0,
        "focus": 0,
        "vitality": 0,
        "poise": 0,
    };
}

function groupBy(arr, property) {
    return arr.reduce((acc, cur) => {
        acc[cur[property]] = [...acc[cur[property]] || [], cur];
        return acc;
    }, {});
}

const permuteArmor = function (equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor) {
    const Copy_Armor_Data = [...Armor_Data];

    // add none type, should be added into input data
    for (const value of ['Head', 'Arm', 'Body', 'Leg']) {
        Copy_Armor_Data.push(fillNoneValue(value));
    };

    const sortedWeight = Copy_Armor_Data.sort((a, b) => a.weight - b.weight);

    // create max absorption so it doesnt need to be recalculated
    const maxAbsorption = {};
    armorAbsorptions.forEach(absorption => maxAbsorption[absorption] = 1 - ((1 - Max_Head["max_" + absorption]) * (1 - Max_Body["max_" + absorption]) * (1 - Max_Arm["max_" + absorption]) * (1 - Max_Leg["max_" + absorption])));

    // prefind values
    for (const row of sortedWeight) {
        let totalAbsorptionValueWeighted = 0;
        let totalRegularValueWeighted = 0;
        for (const resistance of armorResistances) {
            if (resistance.includes('_absorption')) {
                const absorptionPreCalc = 1 - row[resistance];
                row['preCalc' + resistance] = absorptionPreCalc;

                const fullAbsorption = 1 - (absorptionPreCalc);

                const absorptionValueWeighted = fullAbsorption / maxAbsorption[resistance] * resistanceMultiplier[resistance];

                totalAbsorptionValueWeighted += absorptionValueWeighted;
            } else {
                const resistanceValueWeighted = row[resistance] / (Max_Head["max_" + resistance] + Max_Body["max_" + resistance] + Max_Arm["max_" + resistance] + Max_Leg["max_" + resistance]) * resistanceMultiplier[resistance]; // if using multiplier, need to normalize values

                totalRegularValueWeighted += resistanceValueWeighted;
            }
        }

        row.totalRegularValueWeighted = totalRegularValueWeighted;
        row.totalResistanceValueWeighted = totalRegularValueWeighted + totalAbsorptionValueWeighted;

    }

    const splitDataEquipmentType = groupBy(sortedWeight, "equipment_type");
    //Helm.length = 168, Chest.length = 198, Hands.length = 90, Legs.length = 103

    // if i exclude items by weight, you get:
    // arm: 29, head: 35, body: 64, leg: 28. 

    const result = new Heap(resultComparatorMin);
    result.init();

    const resultMaxHeap = new Heap(resultComparatorMaxReal);
    resultMaxHeap.init();

    const maxEquipWeight = loadRemaining;
    // no armor can be found
    if (maxEquipWeight <= 0) {
        return -1;
    }

    // console.log(splitDataEquipmentType);

    // remove armor type that is already equipped
    let iterateArmor = [];
    for (const [key, value] of Object.entries(equippedArmor)) {
        if (value === IS_NOT_WEARING) {
            iterateArmor.push(splitDataEquipmentType[key])
        }
    }

    // error case
    if (iterateArmor.length === 0) {
        return -1;
    }

    // TODO: if remaining weight is > armorsets, eliminiate armor from equation.  this is because the armor cannot be chosen anyways (for optimization)

    
    const armorSet = [];
    let currPosition = 0;
    const currMinimums = {
        damage_negation: {
            "physical_absorption": 0,
            "strike_absorption": 0,
            "slash_absorption": 0,
            "thrust_absorption": 0,
            "magic_absorption": 0,
            "fire_absorption": 0,
            "lightning_absorption": 0,
            "holy_absorption": 0,
        },
        resistance: {
            "immunity": 0,
            "robustness": 0,
            "focus": 0,
            "vitality": 0,
            "poise": 0,
        }
    };

    let armorSetWeight = 0;
    let armorSetValue = 0;

    const armorSetAbsorption = {
        "physical_absorption": 1,
        "strike_absorption": 1,
        "slash_absorption": 1,
        "thrust_absorption": 1,
        "magic_absorption": 1,
        "fire_absorption": 1,
        "lightning_absorption": 1,
        "holy_absorption": 1,
    }

    const preCalcAbsorptions = {
        "physical_absorption": 1,
        "strike_absorption": 1,
        "slash_absorption": 1,
        "thrust_absorption": 1,
        "magic_absorption": 1,
        "fire_absorption": 1,
        "lightning_absorption": 1,
        "holy_absorption": 1,
    };

    // this takes forever
    if (iterateArmor.length === 4) {
        // first remove all duplicates from weight using scale
        const uniqueWeights = [];
        for (const equipTypeKey of Object.keys(splitDataEquipmentType)) {
            const newList = [];
            const armorList = groupBy(splitDataEquipmentType[equipTypeKey], "weight");

            // console.log(armorList);

            for (const weightKey of Object.keys(armorList)) {
                if (armorList[weightKey].length > 1) {
                    // this means there are multiple weights, pick the best one?
			        let maxArmorPiece = armorList[weightKey].reduce(function(prev, current) { return (prev.totalResistanceValueWeighted > current.totalResistanceValueWeighted) ? prev : current });
                    newList.push(maxArmorPiece);
                } else {
                    newList.push(armorList[weightKey][0]);
                }
            }

            uniqueWeights.push(newList);
        }

        // then run normal algorithm
        findArmorOptimization2(armorSet, uniqueWeights, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption, preCalcAbsorptions, MAX_HEAP_LENGTH);

        return result.toArray().sort(resultComparator);

        //****************************** */
        // below is code to recalculate the armor to make calculation even better by readding options that were skipped
        // not perfect, needs to be refined
        //****************************** */
        // const weights = {
        //     Head: new Set(),
        //     Arm: new Set(),
        //     Body: new Set(),
        //     Leg: new Set(),
        // }

        // // re-add weight back??
        // for (const row of result.toArray()) {
        //     for (const armor of row.armorSet) {
        //         weights[armor.equipment_type].add(armor.weight);
        //     }
        // }

        // const uniqueWeights2 = [];
        // for (const equipTypeKey of Object.keys(splitDataEquipmentType)) {
        //     const newList = [];
        //     const armorList = groupBy(splitDataEquipmentType[equipTypeKey], "weight");

        //     // console.log(armorList);

        //     for (const weightKey of Object.keys(armorList)) {
        //         if (weights[equipTypeKey].has(parseFloat(weightKey))) {
        //             newList.push(...armorList[weightKey]);
        //         }
        //     }
        //     uniqueWeights2.push(newList);
        // }

        // console.log(uniqueWeights2);

        // const armorSet2 = [];
        // let currPosition2 = 0;
        // const currMinimums2 = {
        //     damage_negation: {
        //         "physical_absorption": 0,
        //         "strike_absorption": 0,
        //         "slash_absorption": 0,
        //         "thrust_absorption": 0,
        //         "magic_absorption": 0,
        //         "fire_absorption": 0,
        //         "lightning_absorption": 0,
        //         "holy_absorption": 0,
        //     },
        //     resistance: {
        //         "immunity": 0,
        //         "robustness": 0,
        //         "focus": 0,
        //         "vitality": 0,
        //         "poise": 0,
        //     }
        // };
    
        // let armorSetWeight2 = 0;
        // let armorSetValue2 = 0;
    
        // const armorSetAbsorption2 = {
        //     "physical_absorption": 1,
        //     "strike_absorption": 1,
        //     "slash_absorption": 1,
        //     "thrust_absorption": 1,
        //     "magic_absorption": 1,
        //     "fire_absorption": 1,
        //     "lightning_absorption": 1,
        //     "holy_absorption": 1,
        // }
    
        // const preCalcAbsorptions2 = {
        //     "physical_absorption": 1,
        //     "strike_absorption": 1,
        //     "slash_absorption": 1,
        //     "thrust_absorption": 1,
        //     "magic_absorption": 1,
        //     "fire_absorption": 1,
        //     "lightning_absorption": 1,
        //     "holy_absorption": 1,
        // };
        // const result2 = new Heap(resultComparatorMin);
        // result2.init();
        
        // then run algorithm again?
        // need to see how many combinations there are after re-adding all the weight

        // findArmorOptimization2(armorSet2, uniqueWeights2, result2, maxEquipWeight, currPosition2, currMinimums2, resistanceMinimum, armorSetWeight2, armorSetValue2, armorSetAbsorption2, resistanceMultiplier, maxAbsorption, preCalcAbsorptions2, MAX_HEAP_LENGTH);
        // return result2.toArray().sort(resultComparator);
    }

    // initialize values to selected armor pieces, should it be included in the total value? I dont think so.
    for (const element of currEquippedArmor) {
        for (const key of Object.keys(currMinimums.damage_negation)) {
            preCalcAbsorptions[key] *= (1 - element[key]);
            currMinimums.damage_negation[key] = 1 - preCalcAbsorptions[key];
        }

        for (const key of Object.keys(currMinimums.resistance)) {
            currMinimums.resistance[key] += element[key];
        }
    }
    // findArmorOptimization(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption);
    findArmorOptimization2(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption, preCalcAbsorptions, MAX_HEAP_LENGTH);

    // console.log(result);
    return result.toArray().sort(resultComparator);
    // return [];
};

const findArmorOptimization2 = (armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption, preCalcAbsorptions, heapLength) => {
    
    const startOptimization = () => {
        const currentIterationArmor = iterateArmor[currPosition];
        currPosition += 1;
        // console.log(currPosition);

        // console.log("START-LOOP");
        for (let i = 0; i < currentIterationArmor.length; i++) {
            const newArmorPiece = currentIterationArmor[i];
            armorSet.push(newArmorPiece);

            // keep running count of armor stats
            armorSetWeight += newArmorPiece.weight;

            for (let j = 0; j < armorAbsorptions.length; j++) {
                armorSetAbsorption[armorAbsorptions[j]] *= (1 - newArmorPiece[armorAbsorptions[j]]);
            }

            armorSetValue += newArmorPiece.totalRegularValueWeighted;

            for (let j = 0; j < armorRegular.length; j++) {
                currMinimums.resistance[armorRegular[j]] += newArmorPiece[armorRegular[j]];
            }

            if (currPosition < iterateArmor.length) {
                startOptimization();
            } else {
                if (armorSetWeight > maxEquipWeight) {
                    armorSetWeight -= newArmorPiece.weight;
                    for (let j = 0; j < armorAbsorptions.length; j++) {
                        armorSetAbsorption[armorAbsorptions[j]] /= (1 - newArmorPiece[armorAbsorptions[j]]);
                    }
                    armorSetValue -= newArmorPiece.totalRegularValueWeighted;

                    for (let j = 0; j < armorRegular.length; j++) {
                        currMinimums.resistance[armorRegular[j]] -= newArmorPiece[armorRegular[j]];
                    }

                    armorSet.pop();
                    break;
                } else {
                    let meetsMinimum = true;

                    let absorptionValues = 0;
            
                    // kcalculate final damage negations
                    for (let j = 0; j < armorAbsorptions.length; j++) {
                        absorptionValues = (1 - (armorSetAbsorption[armorAbsorptions[j]])) / maxAbsorption[armorAbsorptions[j]] * resistanceMultiplier[armorAbsorptions[j]];
                        currMinimums.damage_negation[armorAbsorptions[j]] = 1 - (armorSetAbsorption[armorAbsorptions[j]] * preCalcAbsorptions[armorAbsorptions[j]]);
                    }
        
                    armorSetValue += absorptionValues;

                    for (let j = 0; j < armorAbsorptions.length; j++) {
                        if (currMinimums.damage_negation[armorAbsorptions[j]] < resistanceMinimum.damage_negation[armorAbsorptions[j]]) {
                            meetsMinimum = false;
                            break;
                        }
                    }
                    
                    for (let j = 0; j < armorRegular.length; j++) {
                        if (currMinimums.resistance[armorRegular[j]] < resistanceMinimum.resistance[armorRegular[j]]) {
                            meetsMinimum = false;
                            break;
                        }
                    }

                    if (meetsMinimum === true) {
                        if (result.length < heapLength) {
                            result.push({ armorSet: [...armorSet], totalResistanceValueWeighted: armorSetValue });
                        } else {
                            if (result.peek().totalResistanceValueWeighted < armorSetValue) {
                                result.pushpop({ armorSet: [...armorSet], totalResistanceValueWeighted: armorSetValue });
                            }
                        }
                    }

                    armorSetValue -= absorptionValues;
                }
            }
            armorSetWeight -= newArmorPiece.weight;

            for (let j = 0; j < armorAbsorptions.length; j++) {
                armorSetAbsorption[armorAbsorptions[j]] /= (1 - newArmorPiece[armorAbsorptions[j]]);
            }

            armorSetValue -= newArmorPiece.totalRegularValueWeighted;

            for (let j = 0; j < armorRegular.length; j++) {
                currMinimums.resistance[armorRegular[j]] -= newArmorPiece[armorRegular[j]];
            }
            armorSet.pop();

        }
        // console.log("END-LOOP");

        currPosition -= 1;
    };

    startOptimization();
};

export default function armorOptimizer(equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor) {
    return permuteArmor(equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor);
}
