import React, { useState } from 'react';
// import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';

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

export default function FilterableArmorTable() {
    const [armorTypeFilter, setArmorTypeFilter] = useState("");
    const [minimumPoise, setMinimumPoise] = useState(0);
    const [rollTypeChoice, setRollTypeChoice] = useState("");// eslint-disable-line no-unused-vars
    // const [affinityTypeFilter, setaffinityTypeFilter] = useState(["None"]);
    // const [somberFilter, setSomberFilter] = useState(true);
    // const [smithingFilter, setSmithingFilter] = useState(true);
    // const [hideNoReqWeapons, setHideNoReqWeapons] = useState(true);
    // const [searchedWeapons, setSearchedWeapons] = useState([]);

    function handleChangeArmorFilter(event) {
        // console.log(event.target.value);
        setArmorTypeFilter(event.target.value);
    };

    function handleChangePoise(event) {
        setMinimumPoise(event.target.value);
    };

    function handleClickCalculateArmor(event) {
        console.log(event.target.value);
    };
    
    //
    function handleChangeRollTypes(event) {
        // console.log(event.target.value);
        setRollTypeChoice(event.target.value);
    };

    return (
        <div className='extra-spacing'>
            <select name="armor-types" id="armor-types" defaultValue={0} onChange={handleChangeArmorFilter}>
                <option value='0' disabled>Select armor type...</option>
                {armorTypes.map((value, index) => <option key={index + 1} value={value}>{value}</option>)}
            </select>
            <br/>
            OR
            <br/>
            <select name="roll-types" id="roll-types" defaultValue={0} onChange={handleChangeRollTypes}>
                <option value='0' disabled>Select a roll type...</option>
                {rollTypes.map((value, index) => <option key={index + 1} value={value}>{value}</option>)}
            </select> 
            <label htmlFor="poise">Minimum Poise</label>
            <input
                type="number"
                min="8"
                max="99"
                maxLength="2"
                inputMode="numeric"
                id="poise"
                name="poise"
                value={minimumPoise}
                onChange={handleChangePoise}
                onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()}
            />
            <label htmlFor="total-load">Total Load</label>
            <input
                type="number"
                min="8"
                max="99"
                maxLength="2"
                inputMode="numeric"
                id="total-load"
                name="total-load"
                disabled
                value={minimumPoise}
                onChange={handleChangePoise}
                onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()}
            />
            <br />
            <br />
            <button className="all-button-style all-button-style-bg" onClick={handleClickCalculateArmor}>Calculate Best Armor</button>
            <ArmorTable
                armorTypeFilter={armorTypeFilter}
            />
        </div>
    );
}