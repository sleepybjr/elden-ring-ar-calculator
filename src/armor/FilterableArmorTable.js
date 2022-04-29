import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';
import { getPhyCalcData } from '../weapons/FilterableWeaponTable';

import Weapon_Reqs from '../json/weapon_reqs.json';

import Armor_Data from '../json/armor_data.json';

import armorOptimizer from './ArmorOptimizer';

import { FaSpinner } from 'react-icons/fa';

import RollTypes from './RollTypes';
import WeaponSearch from './WeaponSearch';
import ArmorSearch from './ArmorSearch';
import DisplayMultipliers from './DisplayMultipliers';
import DisplayMinimums from './DisplayMinimums';

const startArmorResistances = {
    physical_absorption: 0,
    strike_absorption: 0,
    slash_absorption: 0,
    thrust_absorption: 0,
    magic_absorption: 0,
    fire_absorption: 0,
    lightning_absorption: 0,
    holy_absorption: 0,
    immunity: 0,
    robustness: 0,
    focus: 0,
    vitality: 0,
    poise: 0,
}

const startArmorResistancesMultiplier = {
    physical_absorption_multiplier: 1,
    strike_absorption_multiplier: 1,
    slash_absorption_multiplier: 1,
    thrust_absorption_multiplier: 1,
    magic_absorption_multiplier: 1,
    fire_absorption_multiplier: 1,
    lightning_absorption_multiplier: 1,
    holy_absorption_multiplier: 1,
    immunity_multiplier: 1,
    robustness_multiplier: 1,
    focus_multiplier: 1,
    vitality_multiplier: 1,
    poise_multiplier: 1,
}

// needed because javascript uses floats weird
function roundNumber(number, decimals) {
    return parseFloat(number.toFixed(decimals));
}

const NORMAL_ROLL_DEFAULT = 69.9;

const IS_WEARING = 0;
const IS_NOT_WEARING = 1;

export default function FilterableArmorTable() {
    const levels = useSelector((state) => state.allLevels.levels);

    const [rollTypeChoice, setRollTypeChoice] = useState(NORMAL_ROLL_DEFAULT);

    const [searchedWeapons, setSearchedWeapons] = useState({});
    const [searchedArmor, setSearchedArmor] = useState({});

    const [currEquippedArmor, setCurrEquippedArmor] = useState([]);

    const [maxEquip, setMaxEquip] = useState(0);
    const [currEquip, setCurrEquip] = useState(0);
    const [minCurrEquip, setMinCurrEquip] = useState(0);
    const [maxCurrEquip, setMaxCurrEquip] = useState(0);
    const [loadRemaining, setLoadRemaining] = useState(0);

    const [preppedData, setPreppedData] = useState([]);
    const [errors, setErrors] = useState("");

    const [resistances, setResistances] = useState({ ...startArmorResistances });
    const [resistancesMultiplier, setResistancesMultiplier] = useState({ ...startArmorResistancesMultiplier });

    const [spinner, setSpinner] = useState(null);

    function handleChangeCurrEquip(event) {
        const currEquipValue = event.target.value;
        if (currEquipValue > 300) {
            setCurrEquip(300);
        } else {
            setCurrEquip(currEquipValue);
        }
    };

    function handleChangeMaxEquip(event) {
        const maxEquipValue = event.target.value;
        if (maxEquipValue > 300) {
            setMaxEquip(300);
        } else {
            setMaxEquip(maxEquipValue);
        }
    };

    function handleClickCalculateArmor(event) {
        setSpinner(<FaSpinner className="icon_pulse" />);
        setErrors("");

        const equippedArmor = {
            Head: searchedArmor.hasOwnProperty("helmet") && searchedArmor.helmet !== null ? IS_WEARING : IS_NOT_WEARING,
            Body: searchedArmor.hasOwnProperty("chest") && searchedArmor.chest !== null ? IS_WEARING : IS_NOT_WEARING,
            Arm: searchedArmor.hasOwnProperty("gauntlets") && searchedArmor.gauntlets !== null ? IS_WEARING : IS_NOT_WEARING,
            Leg: searchedArmor.hasOwnProperty("legs") && searchedArmor.legs !== null ? IS_WEARING : IS_NOT_WEARING,
        };

        // temporary until  we get 4 select faster, don't allow 4 armor since 300 mil operations
        if (equippedArmor.Head === IS_NOT_WEARING && equippedArmor.Body === IS_NOT_WEARING && equippedArmor.Arm === IS_NOT_WEARING && equippedArmor.Leg === IS_NOT_WEARING) {
            setErrors("Please select at least one equipped armor.");
            setSpinner(null);
            return;
        }

        if (loadRemaining <= 0) {
            setErrors("The load remaining cannot be less than 0.");
            setSpinner(null);
            return;
        }

        const adjustedResistances = {}
        for (const key of Object.keys(resistances)) {
            if (resistances[key] === "") {
                setErrors("All minimums must have a value. Default: 0.");
                setSpinner(null);
                return;
            }

            if (new Set(['physical_absorption', 'strike_absorption', 'slash_absorption', 'thrust_absorption', 'magic_absorption', 'fire_absorption', 'lightning_absorption', 'holy_absorption']).has(key)) {
                adjustedResistances[key] = resistances[key] / 1000;
            } else {
                adjustedResistances[key] = resistances[key];
            }
        }

        for (const key of Object.keys(resistancesMultiplier)) {
            if (resistancesMultiplier[key] === "") {
                setErrors("All multipliers must have a value. Default: 1.");
                setSpinner(null);
                return;
            }
        }

        const output = armorOptimizer(
            equippedArmor,
            loadRemaining,
            adjustedResistances,
            resistancesMultiplier,
            currEquippedArmor
        );

        if (output === -1 || output.length === 0) {
            setErrors("Incorrect input, unable to find an answer.");
            setPreppedData([]);
            setSpinner(null);
            return;
        }

        // get pre status armor and add it here too.

        const trueOutput = [];
        for (const row of output) {
            const newRow = {
                helm_name: "-",
                chest_name: "-",
                gauntlet_name: "-",
                leg_name: "-",
                weight: 0,
                physical_absorption: 0,
                strike_absorption: 0,
                slash_absorption: 0,
                thrust_absorption: 0,
                magic_absorption: 0,
                fire_absorption: 0,
                lightning_absorption: 0,
                holy_absorption: 0,
                immunity: 0,
                robustness: 0,
                focus: 0,
                vitality: 0,
                poise: 0,
            }

            for (const armor of row.armorSet) {
                if (armor.equipment_type === "Head") {
                    newRow.helm_name = armor.name;
                } else if (armor.equipment_type === "Body") {
                    newRow.chest_name = armor.name;
                } else if (armor.equipment_type === "Arm") {
                    newRow.gauntlet_name = armor.name;
                } else if (armor.equipment_type === "Leg") {
                    newRow.leg_name = armor.name;
                }

                newRow.weight += armor.weight;
                newRow.physical_absorption += armor.physical_absorption;
                newRow.strike_absorption += armor.strike_absorption;
                newRow.slash_absorption += armor.slash_absorption;
                newRow.thrust_absorption += armor.thrust_absorption;
                newRow.magic_absorption += armor.magic_absorption;
                newRow.fire_absorption += armor.fire_absorption;
                newRow.lightning_absorption += armor.lightning_absorption;
                newRow.holy_absorption += armor.holy_absorption;
                newRow.immunity += armor.immunity;
                newRow.robustness += armor.robustness;
                newRow.focus += armor.focus;
                newRow.vitality += armor.vitality;
                newRow.poise += armor.poise;
            }

            trueOutput.push(newRow);
        }

        for (const row of trueOutput) {
            for (const armor of currEquippedArmor) {
                if (armor.equipment_type === "Head") {
                    row.helm_name = armor.name;
                } else if (armor.equipment_type === "Body") {
                    row.chest_name = armor.name;
                } else if (armor.equipment_type === "Arm") {
                    row.gauntlet_name = armor.name;
                } else if (armor.equipment_type === "Leg") {
                    row.leg_name = armor.name;
                }

                row.weight += armor.weight;
                row.physical_absorption += armor.physical_absorption;
                row.strike_absorption += armor.strike_absorption;
                row.slash_absorption += armor.slash_absorption;
                row.thrust_absorption += armor.thrust_absorption;
                row.magic_absorption += armor.magic_absorption;
                row.fire_absorption += armor.fire_absorption;
                row.lightning_absorption += armor.lightning_absorption;
                row.holy_absorption += armor.holy_absorption;
                row.immunity += armor.immunity;
                row.robustness += armor.robustness;
                row.focus += armor.focus;
                row.vitality += armor.vitality;
                row.poise += armor.poise;
            }
        }

        setSpinner(null);
        setPreppedData(trueOutput);
    };

    function handleChangeRollTypes(value) {
        setRollTypeChoice(value);
    };

    function handleSearchWeaponItemsChange(searchedWeapon, weaponHand) {
        const newSearchedWeapons = { ...searchedWeapons };

        newSearchedWeapons[weaponHand] = searchedWeapon;

        setSearchedWeapons(newSearchedWeapons);
    };

    function handleSearchArmorItemsChange(armorPiece, armorType) {
        const newSearchedArmor = { ...searchedArmor };

        newSearchedArmor[armorType] = armorPiece;

        setSearchedArmor(newSearchedArmor);
    };

    function handleResistanceChange(event) {
        const newValue = event.target.value;
        const newId = event.target.id;

        let newResistances = { ...resistances };

        newResistances[newId] = newValue ? parseFloat(newValue) : "";

        // need to limit length as well
        if (newResistances[newId] > 300) {
            newResistances[newId] = 300;
        }

        setResistances(newResistances);
    };

    function resetResistanceClick() {
        setResistances({ ...startArmorResistances });
    }

    function handleResistanceMultiplierChange(event) {
        const newValue = event.target.value;
        const newId = event.target.id;

        let newResistances = { ...resistancesMultiplier };

        newResistances[newId] = newValue ? parseFloat(newValue) : "";

        // need to limit length as well
        if (newResistances[newId] > 100) {
            newResistances[newId] = 100;
        }

        setResistancesMultiplier(newResistances);
    };

    function resetResistanceMultiplierClick() {
        setResistancesMultiplier({ ...startArmorResistancesMultiplier });
    }

    useEffect(() => {
        const newMaxLoad = getPhyCalcData(220, levels.endurance);
        setMaxEquip(newMaxLoad);
        setMaxCurrEquip(newMaxLoad);
    }, [levels.endurance]);

    useEffect(() => {
        // count the amount of weapons
        const searchedWeaponsMap = {};
        for (const hand of Object.keys(searchedWeapons)) {
            const weaponInHand = searchedWeapons[hand];
            if (weaponInHand !== null) {
                if (searchedWeaponsMap.hasOwnProperty(weaponInHand.label))
                    searchedWeaponsMap[weaponInHand.label]++;
                else
                    searchedWeaponsMap[weaponInHand.label] = 1;
            }
        }

        let newCurrentLoad = 0;

        // get weapon weight values from amount of weapons
        for (let element of Weapon_Reqs) {
            if (searchedWeaponsMap.hasOwnProperty(element.weaponname)) {
                newCurrentLoad += (element.weight * searchedWeaponsMap[element.weaponname]);
                delete searchedWeaponsMap[element.weaponname]; // need to remove due to multiple weapon names
            }
        }


        // get list of armor names that were searched
        const valuesSearchedArmor = new Set(Object.entries(searchedArmor).flatMap(([key, value]) => value !== null ? value.label : []));

        let newCurrEquippedArmor = [];
        for (let element of Armor_Data) {
            if (valuesSearchedArmor.has(element.name)) {
                newCurrentLoad += element.weight;
                newCurrentLoad = roundNumber(newCurrentLoad, 1);
                newCurrEquippedArmor.push(element);
            }
        }

        setCurrEquippedArmor(newCurrEquippedArmor);
        setCurrEquip(newCurrentLoad);
        setMinCurrEquip(newCurrentLoad);
    }, [searchedWeapons, searchedArmor]);

    useEffect(() => {
        const loadLeft = roundNumber((maxEquip * (rollTypeChoice / 100)) - currEquip, 2);
        setLoadRemaining(loadLeft);

    }, [maxEquip, rollTypeChoice, currEquip]);

    return (
        <div className='large-spacing'>
            <WeaponSearch handleSearchWeaponItemsChange={handleSearchWeaponItemsChange} searchedWeapons={searchedWeapons} />
            <ArmorSearch handleSearchArmorItemsChange={handleSearchArmorItemsChange} searchedArmor={searchedArmor} />
            <RollTypes handleChangeRollTypes={handleChangeRollTypes} rollTypeChoice={rollTypeChoice} />


            <div className="large-spacing">
                <div className="text-description-spacing">
                    You can increase the current and max weight manually.<br />
                    Selecting a new weapon or armor piece will reset changes.
                </div>
                <div className="tiny-spacing">
                    <label htmlFor="curr-equip">Current Equipment Weight</label>
                    <input
                        type="number"
                        min={minCurrEquip}
                        max={maxEquip}
                        inputMode="numeric"
                        id="curr-equip"
                        name="curr-equip"
                        value={currEquip}
                        onChange={handleChangeCurrEquip}
                        onKeyDown={(evt) => ["e", "E", "+", "-",].includes(evt.key) && evt.preventDefault()}
                    />
                </div>
                <div className="tiny-spacing">
                    <label htmlFor="max-equip">Max Equipment Weight</label>
                    <input
                        type="number"
                        id="max-equip"
                        name="max-equip"
                        min={maxCurrEquip}
                        value={maxEquip}
                        onChange={handleChangeMaxEquip}
                    />
                </div>
                <div className="tiny-spacing important-field">
                    Weight Remaining {loadRemaining}
                </div>
            </div>

            <DisplayMinimums
                handleResistanceChange={handleResistanceChange}
                resistances={resistances}
                resetResistanceClick={resetResistanceClick}
            />

            <DisplayMultipliers
                handleResistanceMultiplierChange={handleResistanceMultiplierChange}
                resistancesMultiplier={resistancesMultiplier}
                resetResistanceMultiplierClick={resetResistanceMultiplierClick}
            />

            <div className="large-spacing spacing">
                <div className="text-description-spacing">
                    Displays up to 1,000 sets of best matching armor.
                </div>
                <div className="error">{errors}</div>
                <button className="all-button-style all-button-style-bg" onClick={handleClickCalculateArmor}>Calculate Best Armor</button><span>{spinner}</span>

            </div>

            <ArmorTable preppedData={preppedData} />
        </div>
    );
}