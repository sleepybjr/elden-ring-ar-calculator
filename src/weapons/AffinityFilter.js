import React, { Component } from 'react'

const affinityTypes = [
    "None",
    "Heavy",
    "Keen",
    "Quality",
    "Fire",
    "Flame Art",
    "Lightning",
    "Sacred",
    "Magic",
    "Cold",
    "Poison",
    "Blood",
    "Occult",
];

export default class AffinityFilter extends Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange = (event) => {
        var options = event.target.options;
        var value = [];
        for (var i = 0, l = options.length; i < l; i++) {
            if (options[i].selected) {
                value.push(options[i].value);
            }
        }

        this.props.handleAffinityTypeFilterChange(value);
    };

    handleChangeAll = (affinityTypes) => (_) => {
        this.props.handleAffinityTypeFilterChange(affinityTypes);
    };

    render() {
        const affinityTypesList = affinityTypes.map((type) =>
            <option key={type}>{type}</option>
        );

        return (
            <div className="middle-spacing">
                <label htmlFor="affinity" className="top-label">Affinity</label>
                <select name="affinity" id="affinity" size="13" title="<ctrl> + click for multiple selection and deselect." value={this.props.affinityTypeFilter} onChange={this.handleChange} multiple>
                    {affinityTypesList}
                </select>
                <div>
                    <button className="all-button-style" onClick={this.handleChangeAll(affinityTypes)}>Select All</button>
                    <button className="all-button-style" onClick={this.handleChangeAll([])}>Select None</button>
                </div>
            </div>
        );
    }
}