import React, { Component } from 'react'

export default class WeaponLevels extends Component {
    constructor(props) {
        super(props);
        this.handleChangeSomber = this.handleChangeSomber.bind(this);
        this.handleChangeSmithing = this.handleChangeSmithing.bind(this);
    }

    handleChangeSomber = (event) => {
        console.log(event.target.value + ": " + event.target.min + ": " + event.target.max);
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleWeaponLevelChange(event.target.value, true);
    };

    handleChangeSmithing = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleWeaponLevelChange(event.target.value, false);
    };

    render() {
        return (
            <div>
                <div className='rowC small-spacing'>
                    <label htmlFor="somberlevel">Somber Level</label>
                    <input type="number" min="0" max="10" maxLength="2" inputMode="numeric" id="somberlevel" name="somberlevel" value={this.props.weaponLevels.somber} onChange={this.handleChangeSomber} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()}/>
                    <label htmlFor="smithinglevel">Smithing Level</label>
                    <input type="number" min="0" max="25" maxLength="2" inputMode="numeric" id="smithinglevel" name="smithinglevel" value={this.props.weaponLevels.smithing} onChange={this.handleChangeSmithing} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()}/>
                </div>
            </div>
        );
    }
}