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

    render() {
        const affinityTypesList = affinityTypes.map((type) =>
            <option key={type}>{type}</option>
        );

        return (
            <div>
                <label htmlFor="affinity">Affinity</label>
                <select name="affinity" id="affinity" size="13" defaultValue={this.props.affinityTypeFilter} onChange={this.handleChange} multiple>
                    {affinityTypesList}
                </select>
            </div>
        );
    }
}