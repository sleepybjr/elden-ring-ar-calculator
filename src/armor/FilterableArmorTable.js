import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';
import WeaponSearchBar from '../weapons/SearchBar';
import ArmorSearchBar from './ArmorSearchBar';
import { getPhyCalcData } from '../weapons/FilterableWeaponTable'
import Weapon_Reqs from '../json/weapon_reqs.json';

import Helmets_Select from '../json/head_group.json';
import Chest_Select from '../json/body_group.json';
import Gauntlets_Select from '../json/arm_group.json';
import Legs_Select from '../json/leg_group.json';

import Armor_Data from '../json/armor_data.json';

import armorOptimizer from './ArmorOptimizer';

const armorResistances = {
    damage_negation: [
        "physical_absorption",
        "strike_absorption",
        "slash_absorption",
        "thrust_absorption",
        "magic_absorption",
        "fire_absorption",
        "lightning_absorption",
        "holy_absorption",
    ],
    resistance: [
        "immunity",
        "robustness",
        "focus",
        "vitality",
        "poise",
    ]
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

const rollTypes = [
    "Light Rolls",
    "Normal Rolls",
    "Fat Rolls",
];

const rollTypeMapping = {// eslint-disable-line no-unused-vars
    "Light Rolls": 29.9,
    "Normal Rolls": 69.9,
    "Fat Rolls": 99.9,
};

const MAX_LIMIT = 6;

export default function FilterableArmorTable() {
    const levels = useSelector((state) => state.allLevels.levels);

    const [armorTypeFilter, setArmorTypeFilter] = useState("");

    const [rollTypeChoice, setRollTypeChoice] = useState("");// eslint-disable-line no-unused-vars

    const [searchedArmorWeapons, setSearchedArmorWeapons] = useState([]);
    const [searchedHelmet, setSearchedHelmet] = useState(null);
    const [searchedChest, setSearchedChest] = useState(null);
    const [searchedGauntlets, setSearchedGauntlets] = useState(null);
    const [searchedLegs, setSearchedLegs] = useState(null);
    const [maxEquip, setMaxEquip] = useState(0);
    const [currEquip, setCurrEquip] = useState(0);
    const [minCurrEquip, setMinCurrEquip] = useState(0);
    const [maxCurrEquip, setMaxCurrEquip] = useState(0);

    const [resistances, setResistances] = useState(startArmorResistances);
    const [resistancesMultiplier, setResistancesMultiplier] = useState(startArmorResistancesMultiplier);

    function handleChangeArmorFilter(event) {
        // console.log(event.target.value);
        setArmorTypeFilter(event.target.value);
    };

    function handleChangeCurrEquip(event) {
        setCurrEquip(event.target.value);
    };

    function handleChangeMaxEquip(event) {
        setMaxEquip(event.target.value);
    };


    function handleClickCalculateArmor(event) {
        const equippedArmor = {
            Head: searchedHelmet !== null ? 0 : 1,
            Body: searchedChest !== null ? 0 : 1,
            Arm: searchedGauntlets !== null ? 0 : 1,
            Leg: searchedLegs !== null ? 0 : 1,
        };

        // console.log(resistancesMultiplier);
        const output = armorOptimizer(
            equippedArmor,
            currEquip,
            maxEquip,
            rollTypeChoice,
            resistances,
            resistancesMultiplier
        );
        console.log(output);
    };

    //
    function handleChangeRollTypes(event) {
        // console.log(event.target);
        setRollTypeChoice(event.target.value);
    };

    function handleSearchItemsChange(searchedWeapons) {
        if (searchedWeapons.length <= MAX_LIMIT) {
            setSearchedArmorWeapons(searchedWeapons);
        }
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

        newResistances[newId] = newValue;

        setResistances(newResistances);
    };

    const displayMins = (data) => {
        return data.map(value => {
            return (
                <div key={value}>
                    <label htmlFor={value}>Minimum {value}</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={0}
                        id={value}
                        name={value}
                        value={resistances[value]}
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

        newResistances[newId] = newValue;

        setResistancesMultiplier(newResistances);
    };

    const displayMultipliers = (data) => {
        return data.map(value => {
            return (
                <div key={value + "_multiplier"}>
                    <label htmlFor={value + "_multiplier"}>{value} Multiplier</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={1}
                        id={value + "_multiplier"}
                        name={value + "_multiplier"}
                        value={resistancesMultiplier[value + "_multiplier"]}
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
        const searchedArmorWeaponsSet = new Set(searchedArmorWeapons.map(row => row.label));
        let newCurrentLoad = 0;

        for (let element of Weapon_Reqs) {
            if (searchedArmorWeaponsSet.has(element.weaponname)) {
                newCurrentLoad += element.weight;
                searchedArmorWeaponsSet.delete(element.weaponname);
            }
        }

        for (let element of Armor_Data) {
            if (searchedHelmet !== null && searchedHelmet.label === element.name) {
                newCurrentLoad += element.weight;
            }
            if (searchedChest !== null && searchedChest.label === element.name) {
                newCurrentLoad += element.weight;
            }
            if (searchedGauntlets !== null && searchedGauntlets.label === element.name) {
                newCurrentLoad += element.weight;
            }
            if (searchedLegs !== null && searchedLegs.label === element.name) {
                newCurrentLoad += element.weight;
            }
        }

        setCurrEquip(newCurrentLoad);
        setMinCurrEquip(newCurrentLoad);
    }, [searchedArmorWeapons, searchedHelmet, searchedChest, searchedGauntlets, searchedLegs]);

    return (
        <div className='extra-spacing'>
            <select name="armor-types" id="armor-types" defaultValue={0} onChange={handleChangeArmorFilter}>
                <option value='0' disabled>Select armor type...</option>
                {armorTypes.map((value, index) => <option key={index + 1} value={value}>{value}</option>)}
            </select>
            <br />
            OR
            <br />
            <WeaponSearchBar
                handleSearchItemsChange={handleSearchItemsChange}
                searchedWeapons={searchedArmorWeapons}
                placeholder="Select equipped weapons..."
                maxLimit={MAX_LIMIT}
            />
            <br />

            <select name="roll-types" id="roll-types" defaultValue={0} onChange={handleChangeRollTypes}>
                <option key={0} value='0' disabled>Select a roll type...</option>
                {Object.keys(rollTypeMapping).map((rollKey, index) => <option key={index + 1} value={rollTypeMapping[rollKey]}>{rollKey}</option>)}
            </select>
            <br />
            <br />
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
            <br />
            <ArmorSearchBar
                handleSearchItemsChange={handleSearchHelmetItemChange}
                searchedArmor={searchedHelmet}
                options={Helmets_Select.options}
                placeholder="Select helmet... Ignore to optimize."
            />
            <ArmorSearchBar
                handleSearchItemsChange={handleSearchChestItemChange}
                searchedArmor={searchedChest}
                options={Chest_Select.options}
                placeholder="Select chest... Ignore to optimize."
            />
            <ArmorSearchBar
                handleSearchItemsChange={handleSearchGauntletsItemChange}
                searchedArmor={searchedGauntlets}
                options={Gauntlets_Select.options}
                placeholder="Select gauntlets... Ignore to optimize."
            />
            <ArmorSearchBar
                handleSearchItemsChange={handleSearchLegsItemChange}
                searchedArmor={searchedLegs}
                options={Legs_Select.options}
                placeholder="Select legs... Ignore to optimize."
            />
            <br />
            <br />
            {displayMins(armorResistances.damage_negation)}
            <br />
            {displayMins(armorResistances.resistance)}
            <br />
            <br />
            {displayMultipliers(armorResistances.damage_negation)}
            <br />
            {displayMultipliers(armorResistances.resistance)}
            <br />
            <br />
            <button className="all-button-style all-button-style-bg" onClick={handleClickCalculateArmor}>Calculate Best Armor</button>
            <br />
            Display results up to 1000? or less depending on how long algorithm takes. display as sets of armor.
            <br /> how to handle passives?
            <ArmorTable
                armorTypeFilter={armorTypeFilter}
            />
        </div>
    );
}