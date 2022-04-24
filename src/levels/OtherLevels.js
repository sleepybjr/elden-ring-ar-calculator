import React, { Component } from 'react'

export default class OtherLevels extends Component {
    constructor(props) {
        super(props);
        this.handleChangeVig = this.handleChangeVig.bind(this);
        this.handleChangeMin = this.handleChangeMin.bind(this);
        this.handleChangeEnd = this.handleChangeEnd.bind(this);
    }

    handleChangeVig = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'vigor': event.target.value});
    };
    handleChangeMin = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'mind': event.target.value});
    };
    handleChangeEnd = (event) => {
        if (event.target.value.length === event.target.maxLength && event.target.value[0] === '0')
            event.target.value = event.target.value.slice(1, event.target.maxLength);
        if (Number(event.target.value) > event.target.max)
            event.target.value = Math.trunc(event.target.value / 10);
        this.props.handleLevelChange({'endurance': event.target.value});
    };

    render() {
        return (
            <div className="extra-spacing">
                <div className='rowC small-spacing'>
                    <label htmlFor="vigor">Vigor</label>
                    <input type="number" min="8" max="99" maxLength="2" inputMode="numeric" id="vigor" name="vigor" value={this.props.levels.vigor} onChange={this.handleChangeVig} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="mind">Mind</label>
                    <input type="number" min="9" max="99" maxLength="2" inputMode="numeric" id="mind" name="mind" value={this.props.levels.mind} onChange={this.handleChangeMin} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                    <label htmlFor="endurance">Endurance</label>
                    <input type="number" min="7" max="99" maxLength="2" inputMode="numeric" id="endurance" name="endurance" value={this.props.levels.endurance} onChange={this.handleChangeEnd} onKeyDown={(evt) => ["e", "E", "+", "-", "."].includes(evt.key) && evt.preventDefault()} />
                </div>
                <div className='rowC small-spacing'>
                    <label htmlFor="total-level">Total Level</label>
                    <input type="number" id="total-level" name="total-level" value={this.props.levels.total_level} disabled />
                </div>
            </div>
        );
    }
}