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

const permuteArmor = function (equippedArmor, loadRemaining, resistanceMinimum, resistanceMultiplier) {
    const Copy_Armor_Data = [...Armor_Data];

    // add none type, should be added into input data
    for (const value of ['Head', 'Arm', 'Body', 'Leg']) {
        Copy_Armor_Data.push(fillNoneValue(value));
    };

    const sortedWeight = Copy_Armor_Data.sort((a, b) => a.weight - b.weight);

    console.log(resistanceMultiplier);
    // prefind values
    for (const row of sortedWeight) {
        let totalResistanceValueWeighted = 0;
        for (const resistance of armorResistances) {
            const resistanceValueWeighted = row[resistance] / (Max_Head["max_" + resistance] + Max_Body["max_" + resistance] + Max_Arm["max_" + resistance] + Max_Leg["max_" + resistance]) * resistanceMultiplier[resistance + "_multiplier"]; // if using multiplier, need to normalize values

            totalResistanceValueWeighted += resistanceValueWeighted;
        }

        row.totalResistanceValueWeighted = totalResistanceValueWeighted;

    }

    // const splitDataWeight = groupBy(sortedWeight, "weight");
    const splitDataEquipmentType = groupBy(sortedWeight, "equipment_type");
    //Helm.length = 168, Chest.length = 198, Hands.length = 90, Legs.length = 103\

    // console.log(splitDataEquipmentType);

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
        if (value === 1) {
            iterateArmor.push(splitDataEquipmentType[key])
        }
    }

    // error case
    if (iterateArmor.length === 0) {
        return -1;
    }

    // TODO: if remaining weight is > armorsets, eliminiate armor from equation.  this is because the armor cannot be chosen anyways

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
        "immunity": 0,
        "robustness": 0,
        "focus": 0,
        "vitality": 0,
        "poise": 0,
    };
    
    findArmorOptimization(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum);
    console.log(result);
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

    let count = 0;
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
        count += results.length;
        // console.log(results);
        for (const result of results) {
            if (result.weight <= maxEquipWeight) {
                console.log(result);
                ans.push({ armorSet: { ...result } });
            }
        }

        resultMaxHeap.push({ first_key: keysA[iteratorA + 1], second_key: keysB[iteratorB], robustness: parseInt(keysA[iteratorA + 1]) + parseInt(keysB[iteratorB]) });
        resultMaxHeap.push({ first_key: keysA[iteratorA], second_key: keysB[iteratorB + 1], robustness: parseInt(keysA[iteratorA]) + parseInt(keysB[iteratorB + 1]) });
    }

    return ans;
}

// works for 3 sets, but once it hits 4, it's incredibly slow.
const findArmorOptimization = (armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight = 0, armorSetValue = 0) => {
    const currentIterationArmor = iterateArmor[currPosition];
    currPosition += 1;
    // console.log(currMinimums);

    for (var i = 0; i < currentIterationArmor.length; i++) {
        const newArmorPiece = currentIterationArmor[i];
        armorSet.push(newArmorPiece);

        armorSetWeight += newArmorPiece.weight;
        armorSetValue += newArmorPiece.totalResistanceValueWeighted ? newArmorPiece.totalResistanceValueWeighted : 0;
        for (const key of Object.keys(currMinimums)) {
            currMinimums[key] += newArmorPiece[key];
        }


        if (currPosition < iterateArmor.length) {
            findArmorOptimization(armorSet, iterateArmor, result, maxEquipWeight, currPosition, currMinimums, resistanceMinimum, armorSetWeight, armorSetValue);
        } else {
            if (armorSetWeight > maxEquipWeight) {
                armorSetWeight -= newArmorPiece.weight;
                armorSetValue -= newArmorPiece.totalResistanceValueWeighted ? newArmorPiece.totalResistanceValueWeighted : 0;
                for (const key of Object.keys(currMinimums)) {
                    currMinimums[key] -= newArmorPiece[key];
                }
                armorSet.pop();
                break;
            } else {
                let meetsMinimum = true;
                for (const key of Object.keys(currMinimums)) {
                    if (currMinimums[key] < resistanceMinimum[key]) {
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
        armorSetValue -= newArmorPiece.totalResistanceValueWeighted ? newArmorPiece.totalResistanceValueWeighted : 0;
        for (const key of Object.keys(currMinimums)) {
            currMinimums[key] -= newArmorPiece[key];
        }
        armorSet.pop();

    }

    currPosition -= 1;
};

export default function armorOptimizer(equippedArmor, currWeight, maxWeight, rollMultipler, resistanceMinimum, resistanceMultiplier) {
    return permuteArmor(equippedArmor, currWeight, maxWeight, rollMultipler, resistanceMinimum, resistanceMultiplier);
    // const result = new Heap(resultComparator);
    // result.init();



    // for (const helmetName of Helmets_Select.options) {
    //     if (end === 100000) break;
    //     for (const chestName of Chest_Select.options) {
    //         if (end === 100000) break;
    //         for (const gauntletsName of Gauntlets_Select.options) {
    //             if (end === 100000) break;
    //             for (const legsName of Legs_Select.options) {
    //                 end += 1;
    //                 if (end === 100000) break;
    //                 const armorSet = {};
    //                 let helmet = null;
    //                 let chest = null;
    //                 let gauntlets = null;
    //                 let legs = null;

    //                 const count = {
    //                     helmet: 0,
    //                     chest: 0,
    //                     gauntlets: 0,
    //                     legs: 0,
    //                 }
    //                 for (const element of Armor_Data) {
    //                     // console.log(element);
    //                     if (count.helmet === 0 && helmetName.label === element.name) {
    //                         count.helmet += 1;
    //                         helmet = element;
    //                     } else if (count.chest === 0 && chestName.label === element.name) {
    //                         count.chest += 1;
    //                         chest = element;
    //                     } else if (count.gauntlets === 0 && gauntletsName.label === element.name) {
    //                         count.gauntlets += 1;
    //                         gauntlets = element;
    //                     } else if (count.legs === 0 && legsName.label === element.name) {
    //                         count.legs += 1;
    //                         legs = element;
    //                     } else {
    //                         // console.log("NOT FOUND SO FAR");
    //                     }

    //                     // need to add an error check
    //                 }

    //                 // console.log(helmet);
    //                 // console.log(chest);
    //                 // console.log(gauntlets);
    //                 // console.log(legs);

    //                 // helmet = fillDummyValues(helmet);
    //                 // chest = fillDummyValues(chest);
    //                 // gauntlets = fillDummyValues(gauntlets);
    //                 // legs = fillDummyValues(legs);

    //                 const totalWeight = equippedArmor.helmet * helmet.weight + equippedArmor.chest * chest.weight + equippedArmor.gauntlets * gauntlets.weight + equippedArmor.legs * legs.weight;
    //                 if (totalWeight + currWeight > maxWeight * (rollMultipler / 100)) {
    //                     break;
    //                 }
    //                 armorSet.weight = totalWeight;

    //                 const loopResistances = () => {
    //                     for (const resistance of armorResistances) {
    //                         // console.log(resistance);

    //                         const totalResistanceValue = equippedArmor.helmet * helmet[resistance] + equippedArmor.chest * chest[resistance] + equippedArmor.gauntlets * gauntlets[resistance] + equippedArmor.legs * legs[resistance];
    //                         if (totalResistanceValue < resistanceMinimum[resistance]) {
    //                             return -1;
    //                         }

    //                         armorSet[resistance] = totalResistanceValue
    //                     }
    //                     return 0;
    //                 }

    //                 if (loopResistances() === -1) {
    //                     break;
    //                 }

    //                 const MinPhysical = -1; // need to set these to tru values of the true minimum and max of resistance values
    //                 const MaxPhysical = 1; // need to set these to true values
    //                 let totalResistance = 0;
    //                 for (const [key, value] of Object.entries(armorSet)) {
    //                     if (key !== "weight") {
    //                         totalResistance += resistanceMultiplier[key + "_multiplier"] * (value - MinPhysical) / (MaxPhysical - MinPhysical);
    //                     }
    //                 }

    //                 armorSet.totalResistance = totalResistance;
    //                 armorSet.helmet = helmet;
    //                 armorSet.chest = chest;
    //                 armorSet.gauntlets = gauntlets;
    //                 armorSet.legs = legs;
    //                 if (result.length === 0 || result.length < MAX_HEAP_LENGTH) {
    //                     result.push(armorSet)
    //                 } else {
    //                     if (result.peek().totalResistance < armorSet.totalResistance) { // should i replace anything that is the same?
    //                         result.pushpop(armorSet);
    //                     }
    //                 }

    //             }

    //         }

    //     }
    // }

    // return result.toArray().sort(resultComparator).reverse();
}
