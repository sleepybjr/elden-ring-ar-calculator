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
        this.props.handleLevelChange(event.target.value, 'strength');
    };
    handleChangeDex = (event) => {
        this.props.handleLevelChange(event.target.value, 'dexterity');
    };
    handleChangeInt = (event) => {
        this.props.handleLevelChange(event.target.value, 'intelligence');
    };
    handleChangeFai = (event) => {
        this.props.handleLevelChange(event.target.value, 'faith');
    };
    handleChangeArc = (event) => {
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
                    <input type="number" min="1" max="99" pattern="^\d+$" id="strength" name="strength" value={this.props.levels.strength} onChange={this.handleChangeStr} />
                    <label htmlFor="dexterity">Dexterity</label>
                    <input type="number" min="1" max="99" pattern="^\d+$" id="dexterity" name="dexterity" value={this.props.levels.dexterity} onChange={this.handleChangeDex} />
                    <label htmlFor="intelligence">Intelligence</label>
                    <input type="number" min="1" max="99" pattern="^\d+$" id="intelligence" name="intelligence" value={this.props.levels.intelligence} onChange={this.handleChangeInt} />
                </div>
                <div className='rowC small-spacing'>
                    <label htmlFor="faith">Faith</label>
                    <input type="number" min="1" max="99" pattern="^\d+$" id="faith" name="faith" value={this.props.levels.faith} onChange={this.handleChangeFai} />
                    <label htmlFor="arcane">Arcane</label>
                    <input type="number" min="1" max="99" pattern="^^\d+$" id="arcane" name="arcane" value={this.props.levels.arcane} onChange={this.handleChangeArc} />
                    <label htmlFor="twohand">Two-handed</label>
                    <input type="checkbox" id="twohand" name="twohand" defaultChecked={this.props.twoHanded} onChange={this.handleChangeTwoHanded} />
                </div>
            </div>
        );
    }
}