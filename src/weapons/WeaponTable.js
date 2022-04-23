import React, { useState, useEffect, } from 'react';

import { useTable, useBlockLayout, useSortBy, useFilters } from 'react-table';
import { FixedSizeList } from 'react-window';

// fix row highlight
// fix insufficient req filter
// make input faster for less rows by making it only update filtered columns? not sure if thats possible?
// readd llink to fextralife for weapon name

const typesOrder = {
    'S': 0,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    '-': 6,
};

const noTwoHandBuff = new Set([
    "Hookclaws", "Venomous Fang", "Bloodhound Claws", "Raptor Talons",
    "Caestus", "Spiked Caestus", "Grafted Dragon", "Iron Ball", "Star Fist", "Katar", "Clinging Bone", "Veteran's Prosthesis", "Cipher Pata",
    "Starscourge Greatsword",
    "Ornamental Straight Sword",
]);

const tableHeaders = {
    fullweaponname: "Weapon Name",
    weaponType: "Weapon Type",
    affinity: "Affinity",
    final_physical: "Physical",
    final_magic: "Magic",
    final_fire: "Fire",
    final_lightning: "Lightning",
    final_holy: "Holy",
    final_total_ar: "Total AR",
    final_sorcery_scaling: "Sorcery Scaling",
    type1: "Passive 1",
    final_passive1: "Passive 1 Damage",
    type2: "Passive 2",
    final_passive2: "Passive 2 Damage",
    str_scaling_letter_display: "STR Scaling",
    dex_scaling_letter_display: "DEX Scaling",
    int_scaling_letter_display: "INT Scaling",
    fai_scaling_letter_display: "FAI Scaling",
    arc_scaling_letter_display: "ARC Scaling",
    strreq: "STR Req",
    dexreq: "DEX Req",
    intreq: "INT Req",
    faireq: "FAI Req",
    arcreq: "ARC Req",
    maxUpgrade: "Upgrade",
};

function highlightReqRow(val, levels, isTwoHanded) {
    let strength = levels.strength;
    if ((isTwoHanded && !noTwoHandBuff.has(val.weaponname))) {
        strength = levels.twohand_strength;
    }
    if (strength < val.strreq ||
        levels.dexterity < val.dexreq ||
        levels.intelligence < val.intreq ||
        levels.faith < val.faireq ||
        levels.arcane < val.arcreq) {
        return true;
    } else {
        return false;
    }
};

function sortAlgorithm(rowA, rowB, columnId) {
    // console.log(rowA);
    if (new Set(['fullweaponname', 'weaponType', 'affinity', 'type1', 'type2']).has(columnId)) {
        let sortedColumn = columnId;

        if ('fullweaponname' === columnId) {
            sortedColumn = 'weaponname';
        }

        const nameA = rowA.original[sortedColumn] ? rowA.original[sortedColumn].toUpperCase() : 'Ω';
        const nameB = rowB.original[sortedColumn] ? rowB.original[sortedColumn].toUpperCase() : 'Ω';
        if (nameA < nameB) {
            return -1;
        }
        if (nameA > nameB) {
            return 1;
        }

        if (new Set(['type1', 'type2']).has(columnId)) {
            const second_sort = columnId === 'type1' ? 'final_passive1' : 'final_passive2';
            return rowB.original[second_sort] - rowA.original[second_sort];
        }

        return 0;
    } else if (new Set(['str_scaling_letter_display', 'dex_scaling_letter_display', 'int_scaling_letter_display', 'fai_scaling_letter_display', 'arc_scaling_letter_display']).has(columnId)) {
        const columnType = columnId.substring(0, 3);
        const A = rowA.original[columnType + '_scaling_letter'];
        const B = rowB.original[columnType + '_scaling_letter'];

        const letterAOrder = typesOrder[A.letter];
        const letterBOrder = typesOrder[B.letter];

        const order = letterAOrder - letterBOrder;

        if (order !== 0) {
            return order;
        }

        return B.value - A.value;
    } else {
        const ans = rowB.original[columnId] - rowA.original[columnId];
        if (ans > 0) {
            return 1;
        } else if (ans < 0) {
            return -1;
        }

        return 0;
    }
}

const scrollbarWidth = () => {
    const scrollDiv = document.createElement('div')
    scrollDiv.setAttribute('style', 'width: 100px; height: 100px; overflow: scroll; position:absolute; top:-9999px;')
    document.body.appendChild(scrollDiv)
    const scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
    document.body.removeChild(scrollDiv)
    return scrollbarWidth
}

export default function WeaponTable(props) {
    const skipPageResetRef = React.useRef();

    useEffect(() => {
        setFilter("weaponType", { weaponTypeFilter: props.weaponTypeFilter, searchedWeapons: props.searchedWeapons });
    }, [props.weaponTypeFilter, props.searchedWeapons]);

    useEffect(() => {
        setFilter("affinity", { affinityTypeFilter: props.affinityTypeFilter, searchedWeapons: props.searchedWeapons });
    }, [props.affinityTypeFilter, props.searchedWeapons]);

    useEffect(() => {
        setFilter("maxUpgrade", { somberFilter: props.somberFilter, smithingFilter: props.smithingFilter, searchedWeapons: props.searchedWeapons });
    }, [props.somberFilter, props.smithingFilter, props.searchedWeapons]);

    const defaultColumn = React.useMemo(
        () => ({
            width: 150,
        }),
        []
    )

    const scrollBarSize = React.useMemo(() => scrollbarWidth(), []);

    React.useEffect(() => {
        // After the table has updated, always remove the flag
        skipPageResetRef.current = false
    })

    const data = React.useMemo(
        () => {
            skipPageResetRef.current = true;
            return props.preppedData;
        },
        [props.preppedData]
    )
    const weaponTypeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            return filterValue.weaponTypeFilter.includes(row.original.weaponType) || filterValue.searchedWeapons.includes(row.original.weaponname);
        });
    }

    const affinityTypeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            if (row.original.maxUpgrade === 0 || row.original.maxUpgrade === 10) {
                return filterValue.affinityTypeFilter.includes(row.original.affinity) || filterValue.searchedWeapons.includes(row.original.weaponname);
            } else if (row.original.maxUpgrade === 25) {
                return filterValue.affinityTypeFilter.includes(row.original.affinity) || (filterValue.searchedWeapons.includes(row.original.weaponname) && filterValue.affinityTypeFilter.includes(row.original.affinity));
            }
        });
    }

    const upgradeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            if (row.original.maxUpgrade === 0 || row.original.maxUpgrade === 10) {
                return filterValue.somberFilter || filterValue.searchedWeapons.includes(row.original.weaponname);
            } else if (row.original.maxUpgrade === 25) {
                return filterValue.smithingFilter || filterValue.searchedWeapons.includes(row.original.weaponname);
            }

            return false;
        });
    }

    const hideNoReqWeaponsFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            // if (hideNoReqWeapons === true) {
            // return highlightReqRow(weapon, levels, twoHanded) === false;
            // }
            return true;
        });
    }

    const columns = React.useMemo(
        () => {
            let newColumns = Object.keys(tableHeaders).map(key => {
                return {
                    Header: tableHeaders[key],
                    accessor: key,
                    sortType: sortAlgorithm,
                }
            })

            newColumns.forEach((row) => {
                if (row.accessor === "weaponType")
                    row.filter = weaponTypeFilter
                else if (row.accessor === "affinity")
                    row.filter = affinityTypeFilter;
                else if (row.accessor === "maxUpgrade")
                    row.filter = upgradeFilter;
            });

            return newColumns;
        },
        []
    )
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        totalColumnsWidth,
        prepareRow,
        setFilter,
    } = useTable({
        columns,
        data,
        defaultColumn,
        autoResetPage: !skipPageResetRef.current,
        autoResetExpanded: !skipPageResetRef.current,
        autoResetGroupBy: !skipPageResetRef.current,
        autoResetSelectedRows: !skipPageResetRef.current,
        autoResetSortBy: !skipPageResetRef.current,
        autoResetFilters: !skipPageResetRef.current,
        autoResetRowState: !skipPageResetRef.current,
    },
        useFilters,
        useBlockLayout,
        useSortBy
    )

    const RenderRow = React.useCallback(
        ({ index, style }) => {
            const row = rows[index]
            prepareRow(row)
            return (
                <div
                    {...row.getRowProps({
                        style,
                    })}
                    className="tr"
                >
                    {row.cells.map(cell => {
                        return (
                            <div {...cell.getCellProps()} className="td">
                                {cell.render('Cell')}
                            </div>
                        )
                    })}
                </div>
            )
        },
        [prepareRow, rows]
    )

    return (
        <div>
            <div {...getTableProps()} className="table">
                <div>
                    {headerGroups.map(headerGroup => (
                        <div {...headerGroup.getHeaderGroupProps()} className="tr">
                            {headerGroup.headers.map(column => (
                                <div>
                                    <div {...column.getHeaderProps(column.getSortByToggleProps())} className="th">
                                        {column.render('Header')}

                                        {/* Add a sort direction indicator */}
                                        <span>
                                            {column.isSorted
                                                ? column.isSortedDesc
                                                    ? ' 🔽'
                                                    : ' 🔼'
                                                : ''}
                                        </span>

                                    </div>
                                </div>
                            ))}
                        </div>
                    ))}
                </div>

                <div {...getTableBodyProps()}>
                    <FixedSizeList
                        height={800}
                        itemCount={rows.length}
                        itemSize={35}
                        width={totalColumnsWidth + scrollBarSize}
                    >
                        {RenderRow}
                    </FixedSizeList>
                </div>
            </div>
            )
            {/* <table>
                <thead>
                    <tr>
                        {Object.keys(tableHeaders).map(key =>
                            <th key={key}>
                                <button
                                    type="button"
                                    className={key === sort.column ? sort.direction === "asc" ? "ascending" : sort.direction === "desc" ? "descending" : "" : ""}
                                    onClick={() => onSort(key)}>
                                    {tableHeaders[key]}
                                </button>
                            </th>
                        )}
                    </tr>
                </thead>
                <tbody>
                    {sortedData.map((val, key) => {
                        return (
                            <tr
                                className={highlightReqRow(val, props.levels, props.twoHanded) ? "highlight-red" : ""}
                                key={key}
                            >
                                <td><a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + val.weaponname} >{val.fullweaponname}</a></td>
                                <td>{val.weaponType}</td>
                                <td>{val.affinity}</td>
                                <td>{val.final_physical}</td>
                                <td>{val.final_magic}</td>
                                <td>{val.final_fire}</td>
                                <td>{val.final_lightning}</td>
                                <td>{val.final_holy}</td>
                                <td>{val.final_total_ar}</td>
                                <td>{val.final_sorcery_scaling}</td>
                                <td>{val.type1 ? val.type1 : '-'}</td>
                                <td>{val.final_passive1 !== 0 ? val.final_passive1 : '-'}</td>
                                <td>{val.type2 ? val.type2 : '-'}</td>
                                <td>{val.final_passive2 !== 0 ? val.final_passive2 : '-'}</td>
                                <td>{val.str_scaling_letter ? val.str_scaling_letter.letter !== '-' ? val.str_scaling_letter.letter + ' (' + val.str_scaling_letter.value + ')' : val.str_scaling_letter.letter : '-'}</td>
                                <td>{val.dex_scaling_letter ? val.dex_scaling_letter.letter !== '-' ? val.dex_scaling_letter.letter + ' (' + val.dex_scaling_letter.value + ')' : val.dex_scaling_letter.letter : '-'}</td>
                                <td>{val.int_scaling_letter ? val.int_scaling_letter.letter !== '-' ? val.int_scaling_letter.letter + ' (' + val.int_scaling_letter.value + ')' : val.int_scaling_letter.letter : '-'}</td>
                                <td>{val.fai_scaling_letter ? val.fai_scaling_letter.letter !== '-' ? val.fai_scaling_letter.letter + ' (' + val.fai_scaling_letter.value + ')' : val.fai_scaling_letter.letter : '-'}</td>
                                <td>{val.arc_scaling_letter ? val.arc_scaling_letter.letter !== '-' ? val.arc_scaling_letter.letter + ' (' + val.arc_scaling_letter.value + ')' : val.arc_scaling_letter.letter : '-'}</td>
                                <td>{val.strreq}</td>
                                <td>{val.dexreq}</td>
                                <td>{val.intreq}</td>
                                <td>{val.faireq}</td>
                                <td>{val.arcreq}</td>
                                <td>{val.maxUpgrade === 25 ? "Smithing" : "Somber"}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table> */}
        </div>
    );
}