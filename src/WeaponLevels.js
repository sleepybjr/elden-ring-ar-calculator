import React, { Component } from 'react'

export default class WeaponLevels extends Component {
    constructor(props) {
        super(props);
        this.handleChangeSomber = this.handleChangeSomber.bind(this);
        this.handleChangeSmithing = this.handleChangeSmithing.bind(this);
    }

    handleChangeSomber = (event) => {
        this.props.handleWeaponLevelChange(event.target.value, true);
    };

    handleChangeSmithing = (event) => {
        this.props.handleWeaponLevelChange(event.target.value, false);
    };

    render() {
        return (
            <div>
                <div className='rowC'>
                    <label htmlFor="somberlevel">Somber Level</label>
                    <input type="number" min="0" max="10" pattern="^\d+$" id="somberlevel" name="somberlevel" value={this.props.weaponLevels.somber} onChange={this.handleChangeSomber} />
                </div>
                <div className='rowC'>
                    <label htmlFor="smithinglevel">Smithing Level</label>
                    <input type="number" min="0" max="25" pattern="^\d+$" id="smithinglevel" name="smithinglevel" value={this.props.weaponLevels.smithing} onChange={this.handleChangeSmithing} />
                </div>
            </div>
        );
    }
}