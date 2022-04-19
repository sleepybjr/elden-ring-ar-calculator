import React, { Component } from 'react';
import Select from 'react-select';
import WeaponGroups from './json/weapon_groups';

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
                    value={this.props.searchItems}
                    onChange={this.handleChange}
                    options={WeaponGroups}
                    isMulti
                    placeholder={"Search weapons... Select affinities using filter."}
                    styles={{
                        control: (provided, state) => ({
                            ...provided,
                            borderColor: "#767676",
                            "&:hover": {
                                borderColor: "#767676"
                            }
                        }),
                    }}
                />
            </div>
        );
    }
}