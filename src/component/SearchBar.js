import React, { Component } from 'react';
import Select from 'react-select';

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
                    value={this.props.searchedItems}
                    onChange={this.handleChange}
                    options={this.props.options}
                    className='react-select-container'
                    classNamePrefix="react-select"
                    isMulti
                    placeholder={this.props.placeholder}
                    isOptionDisabled={(option) => this.props.maxLimit !== undefined ? this.props.searchedItems.length >= this.props.maxLimit : false}
                    filterOption={this.props.filterOption ? this.props.filterOption : undefined}
                />
            </div>
        );
    }
}