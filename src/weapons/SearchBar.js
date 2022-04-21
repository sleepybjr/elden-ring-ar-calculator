import React, { Component } from 'react';
import Select from 'react-select';
import WeaponGroups from '.././json/weapon_groups';

export default class SearchBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedOption: [],
        }
    }

    handleChange = (selectedOption) => {
        this.props.handleSearchItemsChange(selectedOption);
    };

    render() {
        return (
            <div className='search-bar'>
                <Select
                    value={this.props.searchedWeapons}
                    onChange={this.handleChange}
                    options={WeaponGroups}
                    className='react-select-container'
                    classNamePrefix="react-select"
                    isMulti
                    placeholder={"Search weapons... Select affinities using filter."}
                />
            </div>
        );
    }
}