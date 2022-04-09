import React, { Component } from 'react'

import FilterBar from './FilterBar';
import WeaponTable from './WeaponTable';
import Levels from './Levels';
import ReactGA from "react-ga4";

export default class FilterableWeaponTable extends Component {
    constructor(props) {
        super(props);
        this.handleWeaponTypeFilterChange = this.handleWeaponTypeFilterChange.bind(this);
        this.handleAffinityTypeFilterChange = this.handleAffinityTypeFilterChange.bind(this);
        this.handleWeaponLevelChange = this.handleWeaponLevelChange.bind(this);
        this.handleLevelChange = this.handleLevelChange.bind(this);
        this.handleTwoHandedChange = this.handleTwoHandedChange.bind(this);
        this.state = {
            weaponTypeFilter: [],
            affinityTypeFilter: ["None"],
            weaponLevels: {
                'somber': 0,
                'smithing': 0,
            },
            levels: {
                'strength': 99,
                'dexterity': 99,
                'intelligence': 99,
                'faith': 99,
                'arcane': 99,
            },
            twoHanded: false,
        };
    }

    setGA = () => {
        ReactGA.initialize("G-VKJF4MLFV3");
        ReactGA.send("pageview");
    };

    componentDidMount() {
        this.setGA();
    };

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

    handleLevelChange(level, type) {
        let newLevels = { ...this.state.levels };
        if (type === 'strength') {
            newLevels.strength = level;
        } else if (type === 'dexterity') {
            newLevels.dexterity = level;
        } else if (type === 'intelligence') {
            newLevels.intelligence = level;
        } else if (type === 'faith') {
            newLevels.faith = level;
        } else if (type === 'arcane') {
            newLevels.arcane = level;
        }
        this.setState({ levels: newLevels });
    };

    handleTwoHandedChange(isTwoHanded) {
        this.setState({ twoHanded: isTwoHanded });
    };

    render() {
        return (
            <div className="container">
                <Levels
                    handleLevelChange={this.handleLevelChange}
                    handleTwoHandedChange={this.handleTwoHandedChange}
                    {...this.state}
                />

                <FilterBar
                    handleWeaponTypeFilterChange={this.handleWeaponTypeFilterChange}
                    handleAffinityTypeFilterChange={this.handleAffinityTypeFilterChange}
                    handleWeaponLevelChange={this.handleWeaponLevelChange}
                    {...this.state}
                />
                <WeaponTable {...this.state} />
            </div>
        )
    };
}