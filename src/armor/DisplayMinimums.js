const armorResistances = {
    damage_negation: {
        physical_absorption: "Physical",
        strike_absorption: "Strike",
        slash_absorption: "Slack",
        thrust_absorption: "Thrust",
        magic_absorption: "Magic",
        fire_absorption: "Fire",
        lightning_absorption: "Lightning",
        holy_absorption: "Holy",
    },
    resistance: {
        immunity: "Immunity",
        robustness: "Robustness",
        focus: "Focus",
        vitality: "Vitality",
        poise: "Poise",
    }
}

export default function DisplayMinimums(props) {
    const displayMins = (data) => {
        return Object.keys(data).map((key) => {
            return (
                <div key={key} className="tiny-spacing">
                    <label htmlFor={key}>{data[key]} Minimum</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={0}
                        id={key}
                        name={key}
                        value={props.resistances[key]}
                        onChange={props.handleResistanceChange}
                        onKeyDown={(evt) => ["e", "E", "+", "-"].includes(evt.key) && evt.preventDefault()}
                    />
                </div>
            )
        });
    }

    return (
        <div className="large-spacing">
            <div className="text-description-spacing">
                Set these to the minimum amount of armor resistance.
            </div>
            <div>
                {displayMins(armorResistances.damage_negation)}
            </div>
            <div>
                {displayMins(armorResistances.resistance)}
            </div>
            <div className="tiny-spacing">
                <button className="all-button-style" onClick={props.resetResistanceClick}>Reset Minimums</button>
            </div>
        </div >
    )
};