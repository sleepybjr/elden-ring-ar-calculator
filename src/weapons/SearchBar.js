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
                    placeholder={this.props.placeholder}
                    isOptionDisabled={(option) => this.props.maxLimit !== null ? this.props.searchedWeapons.length >= this.props.maxLimit : false}
                />
            </div>
        );
    }
}