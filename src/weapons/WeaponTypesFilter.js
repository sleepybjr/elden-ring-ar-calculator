import React, { Component } from 'react'

const weaponTypes = [
    "Unarmed",
    "Reusable Items",
    "Dagger",
    "Straight Sword",
    "Curved Sword",
    "Greatsword",
    "Colossal Sword",
    "Thrusting Sword",
    "Heavy Thrusting Sword",
    "Curved Greatsword",
    "Katana",
    "Twinblade",
    "Hammer",
    "Warhammer",
    "Flail",
    "Axe",
    "Greataxe",
    "Spear",
    "Great Spear",
    "Halberd",
    "Reaper",
    "Whip",
    "Fist",
    "Claw",
    "Colossal Weapon",
    "Torch",
    "Small Shield",
    "Medium Shield",
    "Greatshield",
    "Glintstone Staff",
    "Sacred Seal",
    "Light Bow",
    "Bow",
    "Greatbow",
    "Crossbow",
    "Ballista",
    "Arrow",
    "Greatarrow",
    "Bolt",
    "Greatbolt",
];

export default class WeaponTypesFilter extends Component {
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

        this.props.handleWeaponTypeFilterChange(value);
    };

    handleChangeAll = (weaponTypes) => (_) => {
        this.props.handleWeaponTypeFilterChange(weaponTypes);
    };

    render() {
        const weaponTypesList = weaponTypes.map((type) =>
            <option key={type} value={type}>{type}</option>
        );
        return (
            <div className="middle-spacing">
                <label htmlFor="weapontypes" className="top-label">Weapon Types</label>
                <select name="weapontypes" id="weapontypes" size="13" title="<ctrl> + click for multiple selection and deselect." value={this.props.weaponTypeFilter} onChange={this.handleChange} multiple>
                    {weaponTypesList}
                </select>
                <div>
                    <button className="all-button-style" onClick={this.handleChangeAll(weaponTypes)}>Select All</button>
                    <button className="all-button-style" onClick={this.handleChangeAll([])}>Select None</button>
                </div>
            </div>
        );
    }
}