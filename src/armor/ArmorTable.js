import React from 'react';
// import React, { useEffect, } from 'react';

import { useTable, useBlockLayout, useSortBy } from 'react-table';
import { FixedSizeList } from 'react-window';

import { FaSortDown, FaSortUp } from 'react-icons/fa';

const tableHeaders = {
    // name: "Armor Name",
    // equipment_type: "Armor Type",
    helm_name: "Helmet Name",
    chest_name: "Chest Name",
    gauntlet_name: "Gauntlets Name",
    leg_name: "Leg Name",
    poise: "Poise",
    physical_absorption: "Physical",
    strike_absorption: "Strike",
    slash_absorption: "Slash",
    thrust_absorption: "Thrust",
    magic_absorption: "Magic",
    fire_absorption: "Fire",
    lightning_absorption: "Lightning",
    holy_absorption: "Holy",
    immunity: "Immunity",
    robustness: "Robust",
    focus: "Focus",
    vitality: "Vitality",
    weight: "Weight",
};

function sortAlgorithm(rowA, rowB, columnId) {
    if (new Set(['helm_name', 'chest_name', 'gauntlet_name', 'leg_name']).has(columnId)) {

        const nameA = rowA.original[columnId] ? rowA.original[columnId].toUpperCase() : 'Ω';
        const nameB = rowB.original[columnId] ? rowB.original[columnId].toUpperCase() : 'Ω';
        if (nameA < nameB) {
            return -1;
        }
        if (nameA > nameB) {
            return 1;
        }

        return 0;
    } else {
        return rowB.original[columnId] - rowA.original[columnId];
    }
};

const scrollbarWidth = () => {
    const scrollDiv = document.createElement('div');
    scrollDiv.setAttribute('style', 'width: 100px; height: 100px; overflow: scroll; position:absolute; top:-9999px;');
    document.body.appendChild(scrollDiv);
    const scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;
    document.body.removeChild(scrollDiv);
    return scrollbarWidth;
}

export default function ArmorTable(props) {
    const skipPageResetRef = React.useRef();

    const defaultColumn = React.useMemo(
        () => ({
            width: 90,
        }),
        []
    );

    const scrollBarSize = React.useMemo(() => scrollbarWidth(), []);

    React.useEffect(() => {
        // After the table has updated, always remove the flag
        skipPageResetRef.current = false
    });

    const data = React.useMemo(
        () => {
            skipPageResetRef.current = true;
            return props.preppedData;
        },
        [props.preppedData]
    );

    const columns = React.useMemo(
        () => {
            let newColumns = Object.keys(tableHeaders).map(key => {
                return {
                    Header: tableHeaders[key],
                    accessor: key,
                    sortType: sortAlgorithm,
                }
            });
            newColumns.forEach((row) => {
                // if (row.accessor === "name") {
                if (new Set(['helm_name', 'chest_name', 'gauntlet_name', 'leg_name']).has(row.accessor)) {
                    if (row.accessor === "helm_name") {
                        row.Cell = ({ row, value }) => {
                            return (
                                <a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + row.original.helm_name} >{value}</a>
                            );
                        };
                    } else if (row.accessor === "chest_name") {
                        row.Cell = ({ row, value }) => {
                            return (
                                <a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + row.original.chest_name} >{value}</a>
                            );
                        };
                    } else if (row.accessor === "gauntlet_name") {
                        row.Cell = ({ row, value }) => {
                            return (
                                <a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + row.original.gauntlet_name} >{value}</a>
                            );
                        };
                    } else if (row.accessor === "leg_name") {
                        row.Cell = ({ row, value }) => {
                            return (
                                <a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + row.original.leg_name} >{value}</a>
                            );
                        };
                    }
                    row.width = 262 / 2;
                } else if (row.accessor === "weight") {
                    row.Cell = ({ value }) => {
                        return (
                            <>{Math.round(value * 10) / 10}</>
                        );
                    };
                    // row.width = 100;
                } else if (new Set(['physical_absorption', 'strike_absorption', 'slash_absorption', 'thrust_absorption', 'magic_absorption', 'fire_absorption', 'lightning_absorption', 'holy_absorption']).has(row.accessor)) {
                    row.Cell = ({ value }) => {
                        return (
                            <>{value ? Math.round(value * 100000) / 1000 : '-'}</>
                        );
                    };
                    // row.width = 100;
                } else if (new Set(['immunity', 'robustness', 'focus', 'vitality', 'poise']).has(row.accessor)) {
                    // row.width = 100;
                }
            });

            return newColumns;
        },
        []
    );


    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        totalColumnsWidth,
        prepareRow,
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
        useBlockLayout,
        useSortBy
    );


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
    );

    return (
        <div>
            <div {...getTableProps()} className="table">
                <div className="thead">
                    {headerGroups.map(headerGroup => (
                        <div {...headerGroup.getHeaderGroupProps()} className="tr">
                            {headerGroup.headers.map(column => (
                                <div>
                                    <div {...column.getHeaderProps(column.getSortByToggleProps())} className={column.isSorted ? "th sorted noselect" : "th noselect"}>
                                        {column.render('Header')}

                                        <span className="sortspan">
                                            {column.isSorted
                                                ? column.isSortedDesc
                                                    ? <FaSortDown />
                                                    : <FaSortUp />
                                                : ""}
                                        </span>

                                    </div>
                                </div>
                            ))}
                        </div>
                    ))}
                </div>

                <div {...getTableBodyProps()}

                    className="tbody">
                    <FixedSizeList
                        height={600}
                        itemCount={rows.length}
                        itemSize={40 * 2}
                        width={totalColumnsWidth + scrollBarSize}
                    >
                        {RenderRow}
                    </FixedSizeList>
                </div>
            </div>
        </div>
    );
}