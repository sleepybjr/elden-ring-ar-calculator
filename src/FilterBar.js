import React, { Component } from 'react'

import WeaponTypesFilter from './WeaponTypesFilter';
import AffinityFilter from './AffinityFilter';

export default class FilterBar extends Component {
    render() {
        return (
            <div>
                <div className='rowC small-spacing'>
                    <WeaponTypesFilter handleWeaponTypeFilterChange={this.props.handleWeaponTypeFilterChange} />
                    <AffinityFilter handleAffinityTypeFilterChange={this.props.handleAffinityTypeFilterChange} {...this.props} />
                </div>
            </div>
        );
    }
}