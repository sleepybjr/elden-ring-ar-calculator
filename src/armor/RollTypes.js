const rollTypeMapping = {
    "Light Rolls": 29.9,
    "Normal Rolls": 69.9,
    "Fat Rolls": 99.9,
};

export default function RollTypes(props) {
    return (
        <div className="large-spacing">
            {Object.keys(rollTypeMapping).map((rollKey, index) =>
                <div key={index}>
                    <input
                        type="radio"
                        name={rollKey}
                        checked={props.rollTypeChoice === rollTypeMapping[rollKey]}
                        value={rollTypeMapping[rollKey]}
                        onChange={() => props.handleChangeRollTypes(rollTypeMapping[rollKey])}
                    /> {rollKey} (less than {rollTypeMapping[rollKey]}% of total weight)
                </div>)}
        </div>
    );
}