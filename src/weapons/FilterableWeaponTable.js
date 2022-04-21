import React, { Component } from 'react';

import FilterBar from './FilterBar';
import WeaponTable from './WeaponTable';
import Levels from '../levels/Levels';
import WeaponLevels from '../levels/WeaponLevels';
import OtherLevels from '../levels/OtherLevels';
import ExtraFilters from './ExtraFilters';
import SearchBar from './SearchBar';
import Saves from '../levels/Saves';

function calculateTotalLevel(newLevels) {
    const newLevel = 1 +
        Number(newLevels.strength) +
        Number(newLevels.dexterity) +
        Number(newLevels.intelligence) +
        Number(newLevels.faith) +
        Number(newLevels.arcane) +
        Number(newLevels.vigor) +
        Number(newLevels.mind) +
        Number(newLevels.endurance) -
        80;
    return newLevel;
}

export default class FilterableWeaponTable extends Component {
    constructor(props) {
        super(props);
        this.handleWeaponTypeFilterChange = this.handleWeaponTypeFilterChange.bind(this);
        this.handleAffinityTypeFilterChange = this.handleAffinityTypeFilterChange.bind(this);
        this.handleWeaponLevelChange = this.handleWeaponLevelChange.bind(this);
        this.handleLevelChange = this.handleLevelChange.bind(this);
        this.handleTwoHandedChange = this.handleTwoHandedChange.bind(this);
        this.handleExtraFilterChange = this.handleExtraFilterChange.bind(this);
        this.handleSearchItemsChange = this.handleSearchItemsChange.bind(this);
        this.handleLoadSave = this.handleLoadSave.bind(this);

        this.state = {
            weaponTypeFilter: [],
            affinityTypeFilter: ["None"],
            weaponLevels: {
                'somber': 10,
                'smithing': 25,
            },
            levels: {
                'strength': 99,
                'twohand_strength': Math.trunc(99 * 1.5),
                'dexterity': 99,
                'intelligence': 99,
                'faith': 99,
                'arcane': 99,
                'vigor': 99,
                'mind': 99,
                'endurance': 99,
                'total_level': 713,
            },
            twoHanded: false,
            somberFilter: true,
            smithingFilter: true,
            hideNoReqWeapons: true,
            searchedWeapons: [],
        };
    }

    componentDidMount() {
        // need to handle if get returns nothing
        const windowUrl = window.location.search;
        const params = new URLSearchParams(windowUrl);

        let newLevels = { ...this.state.levels };

        const strength = params.get('str');
        const dexterity = params.get('dex');
        const intelligence = params.get('int');
        const faith = params.get('fai');
        const arcane = params.get('arc');
        const vigor = params.get('vig');
        const mind = params.get('min');
        const endurance = params.get('end');
        const somber = params.get('somber');
        const smithing = params.get('smith');
        let newTwoHanded = params.get('twoHanded');


        if (strength !== null) {
            newLevels.strength = strength;
            newLevels.twohand_strength = Math.trunc(strength * 1.5);
        }
        if (dexterity !== null) {
            newLevels.dexterity = dexterity;
        }
        if (intelligence !== null) {
            newLevels.intelligence = intelligence;
        }
        if (faith !== null) {
            newLevels.faith = faith;
        }
        if (arcane !== null) {
            newLevels.arcane = arcane;
        }
        if (vigor !== null) {
            newLevels.vigor = vigor;
        }
        if (mind !== null) {
            newLevels.mind = mind;
        }
        if (endurance !== null) {
            newLevels.endurance = endurance;
        }
        
        newLevels.total_level = calculateTotalLevel(newLevels);
        
        let newWeaponLevels = { ...this.state.weaponLevels };

        if (somber !== null) {
            newWeaponLevels.somber = somber;
        }
        if (smithing !== null) {
            newWeaponLevels.smithing = smithing;
        }
        if (newTwoHanded === null) {
            newTwoHanded = this.state.twoHanded;
        } else {
            newTwoHanded = newTwoHanded === 'true';
        }

        this.setState({ levels: newLevels, weaponLevels: newWeaponLevels, twoHanded: newTwoHanded})
        window.history.pushState(null, "", window.location.href.split("?")[0]);
    }

    handleWeaponTypeFilterChange(weaponTypeFilter) {
        this.setState({ weaponTypeFilter: weaponTypeFilter });
    };

    handleAffinityTypeFilterChange(affinityTypeFilter) {
        this.setState({ affinityTypeFilter: affinityTypeFilter });
    };

    handleWeaponLevelChange(weaponLevels, isSomber) {
        let newWeaponLevels = { ...this.state.weaponLevels };
        if (isSomber === true) {
            newWeaponLevels.somber = weaponLevels;
        } else {
            newWeaponLevels.smithing = weaponLevels;
        }
        this.setState({ weaponLevels: newWeaponLevels });
    };

    handleLevelChange(type) {
        let newLevels = { ...this.state.levels };

        if ('strength' in type) {
            newLevels.strength = type.strength;
            newLevels.twohand_strength = Math.trunc(type.strength * 1.5);
        }
        if ('dexterity' in type) {
            newLevels.dexterity = type.dexterity;
        }
        if ('intelligence' in type) {
            newLevels.intelligence = type.intelligence;
        }
        if ('faith' in type) {
            newLevels.faith = type.faith;
        }
        if ('arcane' in type) {
            newLevels.arcane = type.arcane;
        }
        if ('vigor' in type) {
            newLevels.vigor = type.vigor;
        }
        if ('mind' in type) {
            newLevels.mind = type.mind;
        }
        if ('endurance' in type) {
            newLevels.endurance = type.endurance;
        }

        newLevels.total_level = calculateTotalLevel(newLevels);

        this.setState({ levels: newLevels });
    };

    handleTwoHandedChange(isTwoHanded) {
        this.setState({ twoHanded: isTwoHanded });
    };

    handleExtraFilterChange(isChecked, type) {
        if (type === 'somber-weapons') {
            this.setState({ somberFilter: isChecked });
        } else if (type === 'smithing-weapons') {
            this.setState({ smithingFilter: isChecked });
        } else if (type === 'missing-req-weapons') {
            this.setState({ hideNoReqWeapons: isChecked });
        }
    };

    handleSearchItemsChange(searchedWeapons) {
        this.setState({ searchedWeapons: searchedWeapons });
    };

    handleLoadSave(save) {
        // i can filter out what actually gets loaded here
        this.setState(save);
    };

    render() {
        return (
            <div className="container">
                <div className="spacing">
                    <div>
                        <Levels
                            handleLevelChange={this.handleLevelChange}
                            handleTwoHandedChange={this.handleTwoHandedChange}
                            {...this.state}
                        />
                        <WeaponLevels handleWeaponLevelChange={this.handleWeaponLevelChange} {...this.state} />
                    </div>

                    <FilterBar
                        handleWeaponTypeFilterChange={this.handleWeaponTypeFilterChange}
                        handleAffinityTypeFilterChange={this.handleAffinityTypeFilterChange}
                        handleWeaponLevelChange={this.handleWeaponLevelChange}
                        {...this.state}
                    />

                    <ExtraFilters
                        handleExtraFilterChange={this.handleExtraFilterChange}
                        {...this.state}
                    />

                    <SearchBar
                        handleSearchItemsChange={this.handleSearchItemsChange}
                        {...this.state}
                    />

                    <OtherLevels
                        handleLevelChange={this.handleLevelChange}
                        {...this.state}
                    />

                    <Saves
                        handleLoadSave={this.handleLoadSave}
                        {...this.state}
                    />
                </div>
                <WeaponTable {...this.state} />

            </div>
        )
    };
}