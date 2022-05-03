const armorResistances = {
    damage_negation: {
        physical_absorption: "Physical",
        strike_absorption: "Strike",
        slash_absorption: "Slash",
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

export default function DisplayMultipliers(props) {
    const displayMultipliers = (data) => {
        return Object.keys(data).map((key) => {
            return (
                <div key={key + "_multiplier"} className="tiny-spacing">
                    <label htmlFor={key + "_multiplier"}>{data[key]} Multiplier</label>
                    <input
                        type="number"
                        inputMode="numeric"
                        min={0}
                        id={key + "_multiplier"}
                        name={key + "_multiplier"}
                        value={props.resistancesMultiplier[key]}
                        onChange={props.handleResistanceMultiplierChange}
                        onKeyDown={(evt) => ["e", "E", "+", "-"].includes(evt.key) && evt.preventDefault()}
                    />
                </div>
            )
        });
    }

    return (
        <div className="large-spacing">
            <div className="text-description-spacing">
                Set multipliers to your importance of armor resistance.<br />
                0 means to not use the resistance at all, 100 is the maximum.
            </div>
            <div>
                {displayMultipliers(armorResistances.damage_negation)}
            </div>
            <div>
                {displayMultipliers(armorResistances.resistance)}
            </div>
            <div className="tiny-spacing">
                <button className="all-button-style" onClick={props.resetResistanceMultiplierClick}>Reset Multipliers</button>
            </div>
        </div >
    )
};