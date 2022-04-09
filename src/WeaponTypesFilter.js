import React, { Component } from 'react'

const weaponTypes = [
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

    render() {
        const weaponTypesList = weaponTypes.map((type) =>
            <option key={type}>{type}</option>
        );

        return (
            <div>
                <label htmlFor="weapontypes">Weapon Types</label>
                <select name="weapontypes" id="weapontypes" size="16" onChange={this.handleChange} multiple>
                    {weaponTypesList}
                </select>
            </div>
        );
    }
}