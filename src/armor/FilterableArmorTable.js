import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';
import SingleItemSearchBar from '../component/SingleItemSeachBar';
import { getPhyCalcData } from '../weapons/FilterableWeaponTable'


import Weapons_Select from '.././json/weapon_groups';
import Weapon_Reqs from '../json/weapon_reqs.json';

import Helmets_Select from '../json/head_group.json';
import Chest_Select from '../json/body_group.json';
import Gauntlets_Select from '../json/arm_group.json';
import Legs_Select from '../json/leg_group.json';
import Armor_Data from '../json/armor_data.json';

import armorOptimizer from './ArmorOptimizer';

import { FaSpinner } from 'react-icons/fa';

import RollTypes from './RollTypes';

const armorResistances = {
    damage_negation: {
        physical_absorption: "Physical",
        strike_absorption: "Strike",
        slash_absorption: "Slack",
        thrust_absorption: "Thrust",
        magic_absorption: "Magic",
        fire_absorption: "Fire",
        lightning_absorption: "Lightning",
        holy_absorption: "Holy",
    },
    resistance: {
        immunity: "Immunity",
        robustness: "Robustness",
        focus: "Focus",
        vitality: "Vitality",
        poise: "Poise",
    }
}

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

const armorTypes = [
    "Helm",
    "Chest",
    "Gauntlets",
    "Legs",
];

const rollTypeMapping = {// eslint-disable-line no-unused-vars
    "Light Rolls": 29.9,
    "Normal Rolls": 69.9,
    "Fat Rolls": 99.9,
};

export default function FilterableArmorTable() {
    const levels = useSelector((state) => state.allLevels.levels);

    const [rollTypeChoice, setRollTypeChoice] = useState(69.9);

    const [searchedWeaponsLH1, setSearchedWeaponsLH1] = useState(null);
    const [searchedWeaponsLH2, setSearchedWeaponsLH2] = useState(null);
    const [searchedWeaponsLH3, setSearchedWeaponsLH3] = useState(null);
    const [searchedWeaponsRH1, setSearchedWeaponsRH1] = useState(null);
    const [searchedWeaponsRH2, setSearchedWeaponsRH2] = useState(null);
    const [searchedWeaponsRH3, setSearchedWeaponsRH3] = useState(null);
    const [searchedHelmet, setSearchedHelmet] = useState(null);
    const [searchedChest, setSearchedChest] = useState(null);
    const [searchedGauntlets, setSearchedGauntlets] = useState(null);
    const [searchedLegs, setSearchedLegs] = useState(null);
    const [currEquippedArmor, setCurrEquippedArmor] = useState([]);

    const [maxEquip, setMaxEquip] = useState(0);
    const [currEquip, setCurrEquip] = useState(0);
    const [minCurrEquip, setMinCurrEquip] = useState(0);
    const [maxCurrEquip, setMaxCurrEquip] = useState(0);
    const [loadRemaining, setLoadRemaining] = useState(0);

    const [preppedData, setPreppedData] = useState([]);
    const [errors, setErrors] = useState("");

    const [resistances, setResistances] = useState(startArmorResistances);
    const [resistancesMultiplier, setResistancesMultiplier] = useState(startArmorResistancesMultiplier);

    const [spinner, setSpinner] = useState(null);

    function handleChangeCurrEquip(event) {
        setCurrEquip(event.target.value);
    };

    function handleChangeMaxEquip(event) {
        setMaxEquip(event.target.value);
    };


    function handleClickCalculateArmor(event) {
        setSpinner(<FaSpinner className="icon_pulse" />);
        setErrors("");

        const equippedArmor = {
            Head: searchedHelmet !== null ? 0 : 1,
            Body: searchedChest !== null ? 0 : 1,
            Arm: searchedGauntlets !== null ? 0 : 1,
            Leg: searchedLegs !== null ? 0 : 1,
        };

        // temporary until  we get 4 select faster, don't allow 4 armor since 300 mil operations
        if (equippedArmor.Head === 1 && equippedArmor.Body === 1 && equippedArmor.Arm === 1 && equippedArmor.Leg === 1) {
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

        // console.log(resistancesMultiplier);

        const output = armorOptimizer(
            equippedArmor,
            loadRemaining,
            adjustedResistances,
            resistancesMultiplier,
            currEquippedArmor
        );

        // console.log(output);

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
                } else if (armor.equipment_type === "Arm") {
                    row.chest_name = armor.name;
                } else if (armor.equipment_type === "Body") {
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

    function handleSearchWeaponItemsLH1Change(searchedWeapon) {
        setSearchedWeaponsLH1(searchedWeapon);
    };
    function handleSearchWeaponItemsLH2Change(searchedWeapon) {
        setSearchedWeaponsLH2(searchedWeapon);
    };
    function handleSearchWeaponItemsLH3Change(searchedWeapon) {
        setSearchedWeaponsLH3(searchedWeapon);
    };
    function handleSearchWeaponItemsRH1Change(searchedWeapon) {
        setSearchedWeaponsRH1(searchedWeapon);
    };
    function handleSearchWeaponItemsRH2Change(searchedWeapon) {
        setSearchedWeaponsRH2(searchedWeapon);
    };
    function handleSearchWeaponItemsRH3Change(searchedWeapon) {
        setSearchedWeaponsRH3(searchedWeapon);
    };

    function handleSearchHelmetItemChange(searchedArmor) {
        setSearchedHelmet(searchedArmor);
    };
    function handleSearchChestItemChange(searchedArmor) {
        setSearchedChest(searchedArmor);
    };
    function handleSearchGauntletsItemChange(searchedArmor) {
        setSearchedGauntlets(searchedArmor);
    };
    function handleSearchLegsItemChange(searchedArmor) {
        setSearchedLegs(searchedArmor);
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

    const displayMins = (data) => {
        return Object.keys(data).map((key) => {
            return (
                <div key={key}>
                    <label htmlFor={key}>{data[key]} Minimum</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={0}
                        id={key}
                        name={key}
                        value={resistances[key]}
                        onChange={handleResistanceChange}
                        onKeyDown={(evt) => ["e", "E", "+", "-"].includes(evt.key) && evt.preventDefault()}
                    />
                </div>
            )
        });
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

    const displayMultipliers = (data) => {
        return Object.keys(data).map((key) => {
            return (
                <div key={key + "_multiplier"}>
                    <label htmlFor={key + "_multiplier"}>{data[key]} Multiplier</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={0}
                        id={key + "_multiplier"}
                        name={key + "_multiplier"}
                        value={resistancesMultiplier[key + "_multiplier"]}
                        onChange={handleResistanceMultiplierChange}
                        onKeyDown={(evt) => ["e", "E", "+", "-"].includes(evt.key) && evt.preventDefault()}
                    />
                </div>
            )
        });
    }

    useEffect(() => {
        const newMaxLoad = getPhyCalcData(220, levels.endurance);
        setMaxEquip(newMaxLoad);
        setMaxCurrEquip(newMaxLoad);
    }, [levels.endurance]);

    useEffect(() => {
        const searchedWeaponsMap = {};
        for (const weapon of [searchedWeaponsLH1, searchedWeaponsLH2, searchedWeaponsLH3, searchedWeaponsRH1, searchedWeaponsRH2, searchedWeaponsRH3]) {
            if (weapon !== null) {
                if (searchedWeaponsMap.hasOwnProperty(weapon.label))
                    searchedWeaponsMap[weapon.label]++;
                else
                    searchedWeaponsMap[weapon.label] = 1;
            }
        }

        let newCurrentLoad = 0;

        for (let element of Weapon_Reqs) {
            if (searchedWeaponsMap.hasOwnProperty(element.weaponname)) {
                newCurrentLoad += (element.weight * searchedWeaponsMap[element.weaponname]);
                delete searchedWeaponsMap[element.weaponname];
            }
        }

        let newCurrEquippedArmor = [];

        for (let element of Armor_Data) {
            if (searchedHelmet !== null && searchedHelmet.label === element.name) {
                newCurrentLoad += element.weight;
                newCurrEquippedArmor.push(element);
            }
            if (searchedChest !== null && searchedChest.label === element.name) {
                newCurrentLoad += element.weight;
                newCurrEquippedArmor.push(element);
            }
            if (searchedGauntlets !== null && searchedGauntlets.label === element.name) {
                newCurrentLoad += element.weight;
                newCurrEquippedArmor.push(element);
            }
            if (searchedLegs !== null && searchedLegs.label === element.name) {
                newCurrentLoad += element.weight;
                newCurrEquippedArmor.push(element);
            }
        }

        setCurrEquippedArmor(newCurrEquippedArmor);
        setCurrEquip(newCurrentLoad);
        setMinCurrEquip(newCurrentLoad);
    }, [searchedWeaponsLH1, searchedWeaponsLH2, searchedWeaponsLH3, searchedWeaponsRH1, searchedWeaponsRH2, searchedWeaponsRH3, searchedHelmet, searchedChest, searchedGauntlets, searchedLegs]);

    useEffect(() => {
        const loadLeft = (maxEquip * (rollTypeChoice / 100)) - currEquip;

        setLoadRemaining(loadLeft);

    }, [maxEquip, rollTypeChoice, currEquip]);

    return (
        <div className='extra-spacing'>
            <br />
            <br />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsRH1Change}
                searchedItems={searchedWeaponsRH1}
                options={Weapons_Select}
                placeholder="Select equipped RH1 weapon..."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsRH2Change}
                searchedItems={searchedWeaponsRH2}
                options={Weapons_Select}
                placeholder="Select equipped RH2 weapon..."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsRH3Change}
                searchedItems={searchedWeaponsRH3}
                options={Weapons_Select}
                placeholder="Select equipped RH3 weapon..."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsLH1Change}
                searchedItems={searchedWeaponsLH1}
                options={Weapons_Select}
                placeholder="Select equipped LH1 weapon..."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsLH2Change}
                searchedItems={searchedWeaponsLH2}
                options={Weapons_Select}
                placeholder="Select equipped LH2 weapon..."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchWeaponItemsLH3Change}
                searchedItems={searchedWeaponsLH3}
                options={Weapons_Select}
                placeholder="Select equipped LH3 weapon..."
            />
            <br />
            <br />
            <p className="search-bar">
                Due to armor optimization being a <a target="_blank" rel="noopener noreferrer" href={"https://en.wikipedia.org/wiki/Knapsack_problem"}>Knapsack problem</a>, you
                currently must select at least one piece of armor. <br />
                There are over 300 million combinations to check when searching for a complete armor set, which takes hours to do.
                We are currently looking into how to speed up search times for a full armor set search.
            </p>

            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchHelmetItemChange}
                searchedItems={searchedHelmet}
                options={Helmets_Select.options}
                placeholder="Select helmet... Ignore to optimize."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchChestItemChange}
                searchedItems={searchedChest}
                options={Chest_Select.options}
                placeholder="Select chest... Ignore to optimize."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchGauntletsItemChange}
                searchedItems={searchedGauntlets}
                options={Gauntlets_Select.options}
                placeholder="Select gauntlets... Ignore to optimize."
            />
            <SingleItemSearchBar
                handleSearchItemsChange={handleSearchLegsItemChange}
                searchedItems={searchedLegs}
                options={Legs_Select.options}
                placeholder="Select legs... Ignore to optimize."
            />


            <br />
            <br />
            <RollTypes handleChangeRollTypes={handleChangeRollTypes} rollTypeChoice={rollTypeChoice} />

            <br />
            <br />
            <br />
            <p>
                Currently working on talismans.<br />
                You can increase the current and max load manually here to account for talismans.<br />
            </p>
            <label htmlFor="curr-equip">Current Equipment Load</label>
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
            <br />
            <label htmlFor="max-equip">Max Equipment Load</label>
            <input
                type="number"
                id="max-equip"
                name="max-equip"
                min={maxCurrEquip}
                value={maxEquip}
                onChange={handleChangeMaxEquip}
            />
            <br />
            <label htmlFor="load-remaining">Load Remaining</label>
            <input
                type="number"
                inputMode="numeric"
                id="load-remaining"
                name="load-remaining"
                disabled
                value={loadRemaining}
            />
            <br />
            <br />
            <br />
            <p>
                Set these to the minimum amount of armor resistance.<br />
                Default: 0<br />
            </p>
            {displayMins(armorResistances.damage_negation)}
            <br />
            {displayMins(armorResistances.resistance)}
            <br />
            <br />
            <p>
                Set these to the importance of armor resistance.<br />
                For example, 100 means important over everything else.<br />
                Using 0 means to not use the resistance at all when optimizing.<br />
                Default: 1<br />
                Range: 0-100<br />
            </p>
            {displayMultipliers(armorResistances.damage_negation)}
            <br />
            {displayMultipliers(armorResistances.resistance)}
            <br />
            <br />
            <div className="error">{errors}</div>
            <button className="all-button-style all-button-style-bg" onClick={handleClickCalculateArmor}>Calculate Best Armor</button><span>{spinner}</span>
            <p>
                Displays up to 250 sets of best matching armor.
            </p>
            <br />
            <ArmorTable
                preppedData={preppedData}
            />
        </div>
    );
}