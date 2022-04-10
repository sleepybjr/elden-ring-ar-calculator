import React, { Component } from 'react'

export default class Levels extends Component {
    constructor(props) {
        super(props);
        this.handleChangeStr = this.handleChangeStr.bind(this);
        this.handleChangeDex = this.handleChangeDex.bind(this);
        this.handleChangeInt = this.handleChangeInt.bind(this);
        this.handleChangeFai = this.handleChangeFai.bind(this);
        this.handleChangeArc = this.handleChangeArc.bind(this);
        this.handleChangeTwoHanded = this.handleChangeTwoHanded.bind(this);
    }

    handleChangeStr = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange(event.target.value, 'strength');
    };
    handleChangeDex = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange(event.target.value, 'dexterity');
    };
    handleChangeInt = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange(event.target.value, 'intelligence');
    };
    handleChangeFai = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange(event.target.value, 'faith');
    };
    handleChangeArc = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange(event.target.value, 'arcane');
    };
    handleChangeTwoHanded = (event) => {
        this.props.handleTwoHandedChange(event.target.checked);
    };

    render() {
        return (
            <div>
            <div className='rowC small-spacing'>
                    <label htmlFor="strength">Strength</label>
                    <input type="number" min="8" max="99" maxLength="2" inputMode="numeric" id="strength" name="strength" value={this.props.levels.strength} onChange={this.handleChangeStr} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="dexterity">Dexterity</label>
                    <input type="number" min="9" max="99" maxLength="2" inputMode="numeric" id="dexterity" name="dexterity" value={this.props.levels.dexterity} onChange={this.handleChangeDex} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="intelligence">Intelligence</label>
                    <input type="number" min="7" max="99" maxLength="2" inputMode="numeric" id="intelligence" name="intelligence" value={this.props.levels.intelligence} onChange={this.handleChangeInt} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                </div>
                <div className='rowC small-spacing'>
                    <label htmlFor="faith">Faith</label>
                    <input type="number" min="7" max="99" maxLength="2" inputMode="numeric" id="faith" name="faith" value={this.props.levels.faith} onChange={this.handleChangeFai} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="arcane">Arcane</label>
                    <input type="number" min="7" max="99" maxLength="2" inputMode="numeric" id="arcane" name="arcane" value={this.props.levels.arcane} onChange={this.handleChangeArc} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="twohand">Two-handed</label>
                    <input type="checkbox" id="twohand" name="twohand" defaultChecked={this.props.twoHanded} onChange={this.handleChangeTwoHanded} />
                </div>
            </div>
        );
    }
}