import React, { Component } from 'react';
import Select from 'react-select';

export default class SingleItemSearchBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedOption: "",
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
                    placeholder={this.props.placeholder}
                    isClearable={true}
                />
            </div>
        );
    }
}