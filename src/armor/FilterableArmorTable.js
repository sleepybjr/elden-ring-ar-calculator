import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';
import WeaponSearchBar from '../weapons/SearchBar';
import { getPhyCalcData } from '../weapons/FilterableWeaponTable'
import Weapon_Reqs from '../json/weapon_reqs.json';

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
    light: 29.9,
    normal: 69.9,
    fat: 99.9,
};

const MAX_LIMIT = 6;

export default function FilterableArmorTable() {
    const levels = useSelector((state) => state.allLevels.levels);

    const [armorTypeFilter, setArmorTypeFilter] = useState("");
    const [minimumPoise, setMinimumPoise] = useState(0);
    const [rollTypeChoice, setRollTypeChoice] = useState("");// eslint-disable-line no-unused-vars

    const [searchedArmorWeapons, setSearchedArmorWeapons] = useState([]);
    const [maxEquip, setMaxEquip] = useState(0);
    const [currEquip, setCurrEquip] = useState(0);
    const [minCurrEquip, setMinCurrEquip] = useState(0);
    const [maxCurrEquip, setMaxCurrEquip] = useState(0);

    function handleChangeArmorFilter(event) {
        // console.log(event.target.value);
        setArmorTypeFilter(event.target.value);
    };

    function handleChangePoise(event) {
        setMinimumPoise(event.target.value);
    };

    function handleChangeCurrEquip(event) {
        setCurrEquip(event.target.value);
    };

    function handleChangeMaxEquip(event) {
        setMaxEquip(event.target.value);
    };


    function handleClickCalculateArmor(event) {
        console.log(event.target.value);
    };

    //
    function handleChangeRollTypes(event) {
        // console.log(event.target.value);
        setRollTypeChoice(event.target.value);
    };

    function handleSearchItemsChange(searchedWeapons) {
        if (searchedWeapons.length <= MAX_LIMIT) {
            setSearchedArmorWeapons(searchedWeapons);
        }
    };

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

        setCurrEquip(newCurrentLoad);
        setMinCurrEquip(newCurrentLoad);
    }, [searchedArmorWeapons]);

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
                <option value='0' disabled>Select a roll type...</option>
                {rollTypes.map((value, index) => <option key={index + 1} value={value}>{value}</option>)}
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
            <label htmlFor="helmet">Helmet</label>
            <input
                type="text"
                id="helmet"
                name="helmet"
                placeholder="ignore if wanting to optimize"
                disabled
            />
            <br />
            <label htmlFor="chest">Chest</label>
            <input
                type="text"
                id="chest"
                name="chest"
                placeholder="ignore if wanting to optimize"
                disabled
            />
            <br />
            <label htmlFor="gauntlets">Gauntlets</label>
            <input
                type="text"
                id="gauntlets"
                name="gauntlets"
                placeholder="ignore if wanting to optimize"
                disabled
            />
            <br />
            <label htmlFor="legs">Legs</label>
            <input
                type="text"
                id="legs"
                name="legs"
                placeholder="ignore if wanting to optimize"
                disabled
            />
            <br />
            <br />
            Poise: choose if you want to set min/max for poise or leave default<br />
            Allow user to pick importance of stats? <br />
            <label htmlFor="min-poise">Minimum Poise</label>
            <input
                type="number"
                inputMode="numeric"
                id="min-poise"
                name="min-poise"
                value={minimumPoise}
                onChange={handleChangePoise}
                onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()}
            />
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