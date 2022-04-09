import React, { Component } from 'react'

import WeaponTypesFilter from './WeaponTypesFilter';
import AffinityFilter from './AffinityFilter';
import WeaponLevels from './WeaponLevels';

export default class FilterBar extends Component {
    render() {
        return (
            <div className='rowC'>
                <WeaponTypesFilter handleWeaponTypeFilterChange={this.props.handleWeaponTypeFilterChange} />
                <div className='rowD'>
                    <AffinityFilter handleAffinityTypeFilterChange={this.props.handleAffinityTypeFilterChange} {...this.props} />
                    <WeaponLevels handleWeaponLevelChange={this.props.handleWeaponLevelChange} {...this.props} />
                </div>
            </div>
        );
    }
}