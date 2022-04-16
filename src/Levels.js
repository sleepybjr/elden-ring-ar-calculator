import React, { Component } from 'react'

const starting_classes = ['Vagabond', 'Warrior', 'Hero', 'Bandit', 'Astrologer', 'Prophet', 'Samurai', 'Prisoner', 'Confessor', 'Wretch',];

export default class Levels extends Component {
    constructor(props) {
        super(props);
        this.handleChangeStr = this.handleChangeStr.bind(this);
        this.handleChangeDex = this.handleChangeDex.bind(this);
        this.handleChangeInt = this.handleChangeInt.bind(this);
        this.handleChangeFai = this.handleChangeFai.bind(this);
        this.handleChangeArc = this.handleChangeArc.bind(this);
        this.handleChangeTwoHanded = this.handleChangeTwoHanded.bind(this);
        this.handleChangeClass = this.handleChangeClass.bind(this);
    }

    handleChangeStr = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'strength': event.target.value});
    };
    handleChangeDex = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'dexterity': event.target.value});
    };
    handleChangeInt = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'intelligence': event.target.value});
    };
    handleChangeFai = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'faith': event.target.value});
    };
    handleChangeArc = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'arcane': event.target.value});
    };
    handleChangeTwoHanded = (event) => {
        this.props.handleTwoHandedChange(event.target.checked);
    };
    handleChangeClass= (event) => {
        // CharaInitParam rows 3000 - 3009
        // Vagabond
        if (event.target.value === starting_classes[0]) {
            this.props.handleLevelChange({'strength':14, 'dexterity':13, 'intelligence':9, 'faith':9, 'arcane':7, 'vigor':15, 'mind':10, 'endurance':11});
        }
        // Warrior
        else if (event.target.value === starting_classes[1]) {
            this.props.handleLevelChange({'strength':10, 'dexterity':16, 'intelligence':10, 'faith':8, 'arcane':9, 'vigor':11, 'mind':12, 'endurance':11});
        }
        // Hero
        else if (event.target.value === starting_classes[2]) {
            this.props.handleLevelChange({'strength':16, 'dexterity':9, 'intelligence':7, 'faith':8, 'arcane':11, 'vigor':14, 'mind':9, 'endurance':12});
        }
        // Bandit
        else if (event.target.value === starting_classes[3]) {
            this.props.handleLevelChange({'strength':9, 'dexterity':13, 'intelligence':9, 'faith':8, 'arcane':14, 'vigor':10, 'mind':11, 'endurance':10});
        }
        // Astrologer
        else if (event.target.value === starting_classes[4]) {
            this.props.handleLevelChange({'strength':8, 'dexterity':12, 'intelligence':16, 'faith':7, 'arcane':9, 'vigor':9, 'mind':15, 'endurance':9});
        }
        // Prophet
        else if (event.target.value === starting_classes[5]) {
            this.props.handleLevelChange({'strength':11, 'dexterity':10, 'intelligence':7, 'faith':16, 'arcane':10, 'vigor':10, 'mind':14, 'endurance':8});
        }
        // Samurai
        else if (event.target.value === starting_classes[6]) {
            this.props.handleLevelChange({'strength':12, 'dexterity':12, 'intelligence':9, 'faith':14, 'arcane':9, 'vigor':10, 'mind':13, 'endurance':10});
        }
        // Prisoner
        else if (event.target.value === starting_classes[7]) {
            this.props.handleLevelChange({'strength':12, 'dexterity':15, 'intelligence':9, 'faith':8, 'arcane':8, 'vigor':12, 'mind':11, 'endurance':13});
        }
        // Confessor
        else if (event.target.value === starting_classes[8]) {
            this.props.handleLevelChange({'strength':11, 'dexterity':14, 'intelligence':14, 'faith':6, 'arcane':9, 'vigor':11, 'mind':12, 'endurance':11});
        }
        // Wretch
        else if (event.target.value === starting_classes[9]) {
            this.props.handleLevelChange({'strength':10, 'dexterity':10, 'intelligence':10, 'faith':10, 'arcane':10, 'vigor':10, 'mind':10, 'endurance':10});
        }
    };

    render() {
        return (
            <div>
                <div className='rowC small-spacing'>
                    <select name="starting-classes" id="starting-classes" defaultValue={0} onChange={this.handleChangeClass}>
                        <option value='0' disabled>Select a class...</option>
                        {starting_classes.map((value, index) => <option key={index+1} value={value}>{value}</option>)}
                    </select>
                </div>
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