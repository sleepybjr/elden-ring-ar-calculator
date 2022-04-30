import Armor_Data from '../json/armor_data.json';

import Max_Head from '../json/armor_max/max_head.json';
import Max_Body from '../json/armor_max/max_body.json';
import Max_Arm from '../json/armor_max/max_arm.json';
import Max_Leg from '../json/armor_max/max_leg.json';

import Heap from 'heap-js';

// edge cases
// equipmentload == max equipment load

const resultComparator = (a, b) => b.totalResistanceValueWeighted - a.totalResistanceValueWeighted;
const resultComparatorMin = (a, b) => a.totalResistanceValueWeighted - b.totalResistanceValueWeighted;
const resultComparatorMaxReal = (a, b) => b.robustness - a.robustness;
const MAX_HEAP_LENGTH = 250;
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

// why does this start duplicating? need to debug with fresher mind
const combineArmor = (iterateArmor1, iterateArmor2) => {
    const result = [];
    const armorSet = [];
    let armorSetWeight = 0;
    let armorSetValue = 0;

    for (const armor1 of iterateArmor1) {
        armorSet.push({ ...armor1 });
        armorSetWeight += armor1.weight;
        armorSetValue += armor1.robustness ? armor1.robustness : 0;

        for (const armor2 of iterateArmor2) {
            armorSet.push({ ...armor2 });
            armorSetWeight += armor2.weight;
            armorSetValue += armor2.robustness ? armor2.robustness : 0;

            result.push({ armorSet: [...armorSet], robustness: armorSetValue, weight: armorSetWeight });

            armorSetWeight -= armor2.weight;
            armorSetValue -= armor2.robustness ? armor2.robustness : 0;
            armorSet.pop();

        }
        armorSetWeight -= armor1.weight;
        armorSetValue -= armor1.robustness ? armor1.robustness : 0;
        armorSet.pop();
    }

    return result;
};

const permuteArmor = function (equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor) {
    const Copy_Armor_Data = [...Armor_Data];

    // add none type, should be added into input data
    for (const value of ['Head', 'Arm', 'Body', 'Leg']) {
        Copy_Armor_Data.push(fillNoneValue(value));
    };

    const sortedWeight = Copy_Armor_Data.sort((a, b) => a.weight - b.weight);

    const maxAbsorption = {};
    armorAbsorptions.forEach(absorption => maxAbsorption["max_" + absorption] = 1 - ((1 - Max_Head["max_" + absorption]) * (1 - Max_Body["max_" + absorption]) * (1 - Max_Arm["max_" + absorption]) * (1 - Max_Leg["max_" + absorption])));

    // console.log(resistanceMultiplier);
    // prefind values
    for (const row of sortedWeight) {
        let totalResistanceValueWeighted = 0;
        let totalAbsorptionValueWeighted = 0;
        let totalRegularValueWeighted = 0;
        for (const resistance of armorResistances) {
            if (resistance.includes('_absorption')) {
                const absorptionPreCalc = 1 - row[resistance];
                row['preCalc' + resistance] = absorptionPreCalc;

                const fullAbsorption = 1 - (absorptionPreCalc);

                const absorptionValueWeighted = fullAbsorption / maxAbsorption["max_" + resistance] * resistanceMultiplier[resistance + "_multiplier"];

                totalAbsorptionValueWeighted += absorptionValueWeighted;
            } else {
                const resistanceValueWeighted = row[resistance] / (Max_Head["max_" + resistance] + Max_Body["max_" + resistance] + Max_Arm["max_" + resistance] + Max_Leg["max_" + resistance]) * resistanceMultiplier[resistance + "_multiplier"]; // if using multiplier, need to normalize values

                totalRegularValueWeighted += resistanceValueWeighted;
            }
            // different formula need for abosroption

        }

        row.totalRegularValueWeighted = totalRegularValueWeighted;
        row.totalResistanceValueWeighted = totalRegularValueWeighted + totalAbsorptionValueWeighted;

    }

    // const splitDataWeight = groupBy(sortedWeight, "weight");
    const splitDataEquipmentType = groupBy(sortedWeight, "equipment_type");
    //Helm.length = 168, Chest.length = 198, Hands.length = 90, Legs.length = 103\

    // console.log(Object.keys(groupBy(splitDataEquipmentType.Arm, "weight")).length);
    // console.log(Object.keys(groupBy(splitDataEquipmentType.Head, "weight")).length);
    // console.log(Object.keys(groupBy(splitDataEquipmentType.Body, "weight")).length);
    // console.log(Object.keys(groupBy(splitDataEquipmentType.Leg, "weight")).length);

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

    // TODO: if remaining weight is > armorsets, eliminiate armor from equation.  this is because the armor cannot be chosen anyways (for optimization of 4)

    // this takes forever
    if (iterateArmor.length === 4) {
        const sortedIterateArmor = iterateArmor.sort((a, b) => a.length - b.length);
        const firstCombined = combineArmor(sortedIterateArmor[0], sortedIterateArmor[3]);
        const secondCombined = combineArmor(sortedIterateArmor[1], sortedIterateArmor[2]);
        // TODO: if remaining weight is > min weight of other set, eliminiate armor from equation.  this is because the armor cannot be chosen anyways
        // console.log(firstCombined);
        iterateArmor = [groupBy(firstCombined, "robustness"), groupBy(secondCombined, "robustness")]; // try sorting each one by weight in each group so i can skip anything that doesnt meet weight constraint
        const ans = findArmorOptimizationDouble(iterateArmor, resultMaxHeap, maxEquipWeight);
        // return [];
        return ans;
    }

    // console.log(iterateArmor);
    const armorSet = [];
    let currPosition = 0;
    const currMinimums = {
        "physical_absorption": 0,
        "strike_absorption": 0,
        "slash_absorption": 0,
        "thrust_absorption": 0,
        "magic_absorption": 0,
        "fire_absorption": 0,
        "lightning_absorption": 0,
        "holy_absorption": 0,
        "preCalcphysical_absorption": 1,
        "preCalcstrike_absorption": 1,
        "preCalcslash_absorption": 1,
        "preCalcthrust_absorption": 1,
        "preCalcmagic_absorption": 1,
        "preCalcfire_absorption": 1,
        "preCalclightning_absorption": 1,
        "preCalcholy_absorption": 1,
        "immunity": 0,
        "robustness": 0,
        "focus": 0,
        "vitality": 0,
        "poise": 0,
    };

    let armorSetWeight = 0;
    let armorSetValue = 0;

    // initialize values to selected armor pieces, should it be included in the total value? I dont think so.
    for (const element of currEquippedArmor) {
        for (const key of Object.keys(currMinimums)) {
            if (key.includes('_absorption') && !key.includes("preCalc")) {
                currMinimums["preCalc" + key] *= (1 - element[key]);
                currMinimums[key] = 1 - currMinimums["preCalc" + key];
            } else if (key.includes("preCalc")) {
            } else {
                currMinimums[key] += element[key];
            }
        }
    }

    console.log(currMinimums);

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

    findArmorOptimization(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption);
    // console.log(result);
    return result.toArray().sort(resultComparator);
    // return [];
};
const findArmorOptimizationDouble = (iterateArmor, resultMaxHeap, maxEquipWeight) => {
    const A = 0;
    const B = 1;
    const keysA = Object.keys(iterateArmor[A]).reverse();
    const keysB = Object.keys(iterateArmor[B]).reverse();

    let iteratorA = 0;
    let iteratorB = 0;

    // console.log(iterateArmor)

    const ans = [];

    // add first combination to heap
    resultMaxHeap.push({ first_key: keysA[iteratorA], second_key: keysB[iteratorB], robustness: parseInt(keysA[iteratorA]) + parseInt(keysB[iteratorB]) });

    // TODO: why isn't it showing 300 mil combinations????????
    // the reason is because im not comparing everything due to the step down... i wonder if this will cause problems?
    // example: 0 legs / guantlets and 132 chest / head isnt checked. far apart variables are ignored.
    // while (ans.length < MAX_HEAP_LENGTH || (iteratorA < keysA.length && iteratorB < keysB.length)) { // this works and gets all solutions
    while (ans.length < MAX_HEAP_LENGTH && (iteratorA < keysA.length && iteratorB < keysB.length)) { // this gets up to heap length

        const maxValue = resultMaxHeap.pop();

        const armorSetsA = iterateArmor[A][maxValue.first_key];
        const armorSetsB = iterateArmor[B][maxValue.second_key];

        // make combinations of each armor set, 
        const results = combineArmor(armorSetsA, armorSetsB);
        // console.log(results);
        for (const result of results) {
            if (result.weight <= maxEquipWeight) {
                ans.push({ armorSet: { ...result } });
            }
        }

        resultMaxHeap.push({ first_key: keysA[iteratorA + 1], second_key: keysB[iteratorB], robustness: parseInt(keysA[iteratorA + 1]) + parseInt(keysB[iteratorB]) });
        resultMaxHeap.push({ first_key: keysA[iteratorA], second_key: keysB[iteratorB + 1], robustness: parseInt(keysA[iteratorA]) + parseInt(keysB[iteratorB + 1]) });
    }

    return ans;
}

// works for 3 sets, but once it hits 4, it's incredibly slow.
const findArmorOptimization = (armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption) => {
    const currentIterationArmor = iterateArmor[currPosition];
    currPosition += 1;
    // console.log(currMinimums);

    for (var i = 0; i < currentIterationArmor.length; i++) {
        const newArmorPiece = currentIterationArmor[i];
        armorSet.push(newArmorPiece);

        armorSetWeight += newArmorPiece.weight;
        let absorptionValues = 0;
        for (const resistance of Object.keys(armorSetAbsorption)) {
            armorSetAbsorption[resistance] *= newArmorPiece['preCalc' + resistance];

            const fullAbsorption = 1 - (armorSetAbsorption[resistance]);

            const absorptionValueWeighted = fullAbsorption / maxAbsorption["max_" + resistance]  * resistanceMultiplier[resistance + "_multiplier"];

            absorptionValues += absorptionValueWeighted;
        }

        armorSetValue += newArmorPiece.totalRegularValueWeighted ? newArmorPiece.totalRegularValueWeighted + absorptionValues : 0;
        for (const key of Object.keys(currMinimums)) {
            if (key.includes('_absorption') && !key.includes("preCalc")) {
                currMinimums[key] = 1 - (armorSetAbsorption[key] * currMinimums["preCalc" + key]);
            } else if (key.includes("preCalc")) {
            } else {
                currMinimums[key] += newArmorPiece[key];
            }
        }


        if (currPosition < iterateArmor.length) {
            findArmorOptimization(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue, armorSetAbsorption, resistanceMultiplier, maxAbsorption);
        } else {
            if (armorSetWeight > maxEquipWeight) {
                armorSetWeight -= newArmorPiece.weight;

                absorptionValues = 0;
                for (const resistance of Object.keys(armorSetAbsorption)) {
                    armorSetAbsorption[resistance] /= newArmorPiece['preCalc' + resistance];

                    const fullAbsorption = 1 - (armorSetAbsorption[resistance]);

                    const absorptionValueWeighted = fullAbsorption / maxAbsorption["max_" + resistance]  * resistanceMultiplier[resistance + "_multiplier"];

                    absorptionValues += absorptionValueWeighted;
                }

                armorSetValue -= newArmorPiece.totalRegularValueWeighted ? newArmorPiece.totalRegularValueWeighted + absorptionValues : 0;
                for (const key of Object.keys(currMinimums)) {
                    if (key.includes('_absorption') && !key.includes("preCalc")) {
                        currMinimums[key] = 1 - (armorSetAbsorption[key] * currMinimums["preCalc" + key]);
                    } else if (key.includes("preCalc")) {
                    } else {
                        currMinimums[key] -= newArmorPiece[key];
                    }
                }
                armorSet.pop();
                break;
            } else {
                let meetsMinimum = true;
                for (const key of Object.keys(currMinimums)) {
                    if (!key.includes("preCalc") && currMinimums[key] < resistanceMinimum[key]) {
                        meetsMinimum = false;
                        break;
                    }
                }
                if (meetsMinimum === true) {
                    if (result.length < MAX_HEAP_LENGTH) {
                        result.push({ armorSet: [...armorSet], totalResistanceValueWeighted: armorSetValue });
                    } else {
                        if (result.peek().totalResistanceValueWeighted < armorSetValue) {
                            result.pushpop({ armorSet: [...armorSet], totalResistanceValueWeighted: armorSetValue });
                        }
                    }
                }
            }
        }
        armorSetWeight -= newArmorPiece.weight;
        absorptionValues = 0;
        for (const resistance of Object.keys(armorSetAbsorption)) {
            armorSetAbsorption[resistance] /= newArmorPiece['preCalc' + resistance];

            const fullAbsorption = 1 - (armorSetAbsorption[resistance]);

            const absorptionValueWeighted = fullAbsorption / maxAbsorption["max_" + resistance]  * resistanceMultiplier[resistance + "_multiplier"];

            absorptionValues += absorptionValueWeighted;
        }
        armorSetValue -= newArmorPiece.totalRegularValueWeighted ? newArmorPiece.totalRegularValueWeighted + absorptionValues : 0;
        for (const key of Object.keys(currMinimums)) {
            if (key.includes('_absorption') && !key.includes("preCalc")) {
                currMinimums[key] = 1 - (armorSetAbsorption[key] * currMinimums["preCalc" + key]);
            } else if (key.includes("preCalc")) {
            } else {
                currMinimums[key] -= newArmorPiece[key];
            }
        }
        armorSet.pop();

    }

    currPosition -= 1;
};

export default function armorOptimizer(equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor) {
    return permuteArmor(equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier, currEquippedArmor);
}
