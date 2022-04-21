import React, { useState } from 'react';
// import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';

const armorTypes = [
    "Helm",
    "Chest",
    "Gauntlets",
    "Legs",
];

export default function FilterableArmorTable() {
    const [armorTypeFilter, setArmorTypeFilter] = useState("");
    // const [affinityTypeFilter, setaffinityTypeFilter] = useState(["None"]);
    // const [somberFilter, setSomberFilter] = useState(true);
    // const [smithingFilter, setSmithingFilter] = useState(true);
    // const [hideNoReqWeapons, setHideNoReqWeapons] = useState(true);
    // const [searchedWeapons, setSearchedWeapons] = useState([]);


    function handleChangeArmorFilter(event) {
        // console.log(event.target.value);
        setArmorTypeFilter(event.target.value);
    };

    return (
        <div className='extra-spacing'>
            <select name="armor-types" id="armor-types" defaultValue={0} onChange={handleChangeArmorFilter}>
                <option value='0' disabled>Select armor type...</option>
                {armorTypes.map((value, index) => <option key={index + 1} value={value}>{value}</option>)}
            </select>
            <ArmorTable
                armorTypeFilter={armorTypeFilter}
            />
        </div>
    );
}