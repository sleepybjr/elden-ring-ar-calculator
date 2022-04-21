import React, { useState, useEffect } from 'react';

const data = [
    {
        "fullarmorname": "Helmet",
        "armor_type": "Helm",
        "vs_strength": 15,
        "vs_slash": 25,
        "vs_pierce": 5,
        "magic": 9,
        "fire": 0,
        "lightning": 0,
        "holy": 0,
        "immunity": 8,
        "robustness": 1.5,
        "focus": 1.5,
        "vitality": 3,
        "poise": 7,
        "weight": 3.5,
        "passive_1": 3,
        "passive_2": 3,
        "passive_3": 3,
    },
    {
        "fullarmorname": "Apple Helmet",
        "armor_type": "Helm",
        "vs_strength": 15,
        "vs_slash": 25,
        "vs_pierce": 5,
        "magic": 9,
        "fire": 0,
        "lightning": 0,
        "holy": 0,
        "immunity": 8,
        "robustness": 1.5,
        "focus": 1.5,
        "vitality": 3,
        "poise": 7,
        "weight": 3.5,
        "passive_1": 3,
        "passive_2": 3,
        "passive_3": 3,
    },
    {
        "fullarmorname": "Chest",
        "armor_type": "Chest",
        "vs_strength": 15,
        "vs_slash": 25,
        "vs_pierce": 5,
        "magic": 9,
        "fire": 0,
        "lightning": 0,
        "holy": 0,
        "immunity": 8,
        "robustness": 1.5,
        "focus": 1.5,
        "vitality": 3,
        "poise": 7,
        "weight": 3.5,
        "passive_1": 3,
        "passive_2": 3,
        "passive_3": 3,
    },
];

export default function ArmorTable(props) {
    const [column, setColumn] = useState(null);
    const [direction, setDirection] = useState(null);
    const [sortedData, setSortedData] = useState(data);

    function onSort(sortedColumn) {
        let newDirection = null;
        if (sortedColumn === column) {
            if (direction === null) {
                newDirection = 'asc';
            } else if (direction === 'asc') {
                newDirection = 'desc';
            } else {
                newDirection = null;
            }
        } else {
            newDirection = 'asc';
        }

        setColumn(sortedColumn);
        setDirection(newDirection);
    };

    useEffect(() => {
        let startData = data;
        let finalData = startData.filter((row) => row.armor_type === props.armorTypeFilter);

        if (direction !== null) {
            finalData = data.sort((a, b) => {
                if (new Set(['fullarmorname', 'armor_type']).has(column)) {

                    const nameA = a[column] ? a[column].toUpperCase() : 'Ω';
                    const nameB = b[column] ? b[column].toUpperCase() : 'Ω';
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }

                    return 0;
                } else {
                    return b[column] - a[column];
                }
            });

            if (direction === 'desc') {
                finalData.reverse();
            }
        }
        
        setSortedData(finalData);
    }, [column, direction, props.armorTypeFilter]);

    return (
        <div className='extra-spacing'>
            <table>
                <thead>
                    <tr>
                        <th>
                            <button type="button"
                                className={'fullarmorname' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('fullarmorname')}>
                                Armor Name
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'armor_type' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('armor_type')}>
                                Armor Type
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'vs_strength' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('vs_strength')}>
                                VS Strength
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'vs_slash' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('vs_slash')}>
                                VS Slash
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'vs_pierce' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('vs_pierce')}>
                                VS Pierce
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'magic' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('magic')}>
                                Magic
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'fire' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('fire')}>
                                Fire
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'lightning' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('lightning')}>
                                Lightning
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'holy' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('holy')}>
                                Holy
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'immunity' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('immunity')}>
                                Immunity
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'robustness' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('robustness')}>
                                Robustness
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'focus' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('focus')}>
                                Focus
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'vitality' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('vitality')}>
                                Vitality
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'poise' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('poise')}>
                                Poise
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'weight' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('weight')}>
                                Weight
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'passive_1' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('passive_1')}>
                                Passive 1
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'passive_2' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('passive_2')}>
                                Passive 2
                            </button>
                        </th>
                        <th>
                            <button type="button"
                                className={'passive_3' === column ? direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "" : ""}
                                onClick={() => onSort('passive_3')}>
                                Passive 3
                            </button>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {sortedData.map((val, key) => {
                        return (
                            <tr key={key}>
                                <td>{val.fullarmorname}</td>
                                <td>{val.armor_type}</td>
                                <td>{val.vs_strength}</td>
                                <td>{val.vs_slash}</td>
                                <td>{val.vs_pierce}</td>
                                <td>{val.magic}</td>
                                <td>{val.fire}</td>
                                <td>{val.lightning}</td>
                                <td>{val.holy}</td>
                                <td>{val.immunity}</td>
                                <td>{val.robustness}</td>
                                <td>{val.focus}</td>
                                <td>{val.vitality}</td>
                                <td>{val.poise}</td>
                                <td>{val.weight}</td>
                                <td>{val.passive_1}</td>
                                <td>{val.passive_2}</td>
                                <td>{val.passive_3}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    );
}