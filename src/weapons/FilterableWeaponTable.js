import React, { useState } from 'react';
import { useSelector } from 'react-redux';

import FilterBar from './FilterBar';
import WeaponTable from './WeaponTable';
import ExtraFilters from './ExtraFilters';
import SearchBar from './SearchBar';

export default function FilterableWeaponTable() {
    const levels = useSelector((state) => state.allLevels.levels);
    const weaponLevels = useSelector((state) => state.allLevels.weaponLevels);
    const twoHanded = useSelector((state) => state.allLevels.twoHanded);

    const [weaponTypeFilter, setWeaponTypeFilter] = useState([]);
    const [affinityTypeFilter, setaffinityTypeFilter] = useState(["None"]);
    const [somberFilter, setSomberFilter] = useState(true);
    const [smithingFilter, setSmithingFilter] = useState(true);
    const [hideNoReqWeapons, setHideNoReqWeapons] = useState(true);
    const [searchedWeapons, setSearchedWeapons] = useState([]);

    function handleWeaponTypeFilterChange(weaponTypeFilter) {
        setWeaponTypeFilter(weaponTypeFilter);
    };

    function handleAffinityTypeFilterChange(affinityTypeFilter) {
        setaffinityTypeFilter(affinityTypeFilter);
    };

    function handleExtraFilterChange(isChecked, type) {
        if (type === 'somber-weapons') {
            setSomberFilter(isChecked);
        } else if (type === 'smithing-weapons') {
            setSmithingFilter(isChecked);
        } else if (type === 'missing-req-weapons') {
            setHideNoReqWeapons(isChecked);
        }
    };

    function handleSearchItemsChange(searchedWeapons) {
        setSearchedWeapons(searchedWeapons);
    };

    return (
        <div className="container">
            <div className="spacing">
                <FilterBar
                    handleWeaponTypeFilterChange={handleWeaponTypeFilterChange}
                    handleAffinityTypeFilterChange={handleAffinityTypeFilterChange}
                    weaponTypeFilter={weaponTypeFilter}
                    affinityTypeFilter={affinityTypeFilter}
                />

                <ExtraFilters
                    handleExtraFilterChange={handleExtraFilterChange}
                    somberFilter={somberFilter}
                    smithingFilter={smithingFilter}
                    hideNoReqWeapons={hideNoReqWeapons}
                />

                <SearchBar
                    handleSearchItemsChange={handleSearchItemsChange}
                    searchedWeapons={searchedWeapons}
                />

            </div>
            <WeaponTable
                weaponTypeFilter={weaponTypeFilter}
                affinityTypeFilter={affinityTypeFilter}
                somberFilter={somberFilter}
                smithingFilter={smithingFilter}
                hideNoReqWeapons={hideNoReqWeapons}
                searchedWeapons={searchedWeapons}
                levels={levels}
                weaponLevels={weaponLevels}
                twoHanded={twoHanded}
            />

        </div>
    );
}