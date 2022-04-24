import React, { useEffect, } from 'react';

import { useTable, useBlockLayout, useSortBy, useFilters } from 'react-table';
import { FixedSizeList } from 'react-window';

import {FaSortDown, FaSortUp} from 'react-icons/fa';

// make input faster for less rows by making it only update filtered columns? could pull out filters to make input faster, but then filters will be slower due to needing to redo calculations everytime. 
// it's either filter first, then calculate. or calculate, then filter. trade-off.

const typesOrder = {
    'S': 0,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    '-': 6,
};

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
    final_sorcery_scaling: "Sorcery",
    type1: "Passive 1 (P1)",
    final_passive1: "P1 Damage",
    type2: "Passive 2 (P2)",
    final_passive2: "P2 Damage",
    str_scaling_letter: "STR Scaling",
    dex_scaling_letter: "DEX Scaling",
    int_scaling_letter: "INT Scaling",
    fai_scaling_letter: "FAI Scaling",
    arc_scaling_letter: "ARC Scaling",
    strreq: "STR Req",
    dexreq: "DEX Req",
    intreq: "INT Req",
    faireq: "FAI Req",
    arcreq: "ARC Req",
    maxUpgrade: "Upgrade",
    missedReq: "Meets Req",
};

function sortAlgorithm(rowA, rowB, columnId) {
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
    } else if (new Set(['str_scaling_letter', 'dex_scaling_letter', 'int_scaling_letter', 'fai_scaling_letter', 'arc_scaling_letter']).has(columnId)) {
        const A = rowA.original[columnId];
        const B = rowB.original[columnId];

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
    const scrollDiv = document.createElement('div');
    scrollDiv.setAttribute('style', 'width: 100px; height: 100px; overflow: scroll; position:absolute; top:-9999px;');
    document.body.appendChild(scrollDiv);
    const scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;
    document.body.removeChild(scrollDiv);
    return scrollbarWidth;
}

export default function WeaponTable(props) {
    const skipPageResetRef = React.useRef();

    useEffect(() => {
        setFilter("weaponType", { weaponTypeFilter: props.weaponTypeFilter, searchedWeapons: props.searchedWeapons });
        // eslint-disable-next-line
    }, [props.weaponTypeFilter, props.searchedWeapons]);

    useEffect(() => {
        setFilter("affinity", { affinityTypeFilter: props.affinityTypeFilter, searchedWeapons: props.searchedWeapons });
        // eslint-disable-next-line
    }, [props.affinityTypeFilter, props.searchedWeapons]);

    useEffect(() => {
        setFilter("maxUpgrade", { somberFilter: props.somberFilter, smithingFilter: props.smithingFilter, searchedWeapons: props.searchedWeapons });
        // eslint-disable-next-line
    }, [props.somberFilter, props.smithingFilter, props.searchedWeapons]);

    useEffect(() => {
        setFilter("missedReq", { hideNoReqWeapons: props.hideNoReqWeapons, searchedWeapons: props.searchedWeapons });
        // eslint-disable-next-line
    }, [props.hideNoReqWeapons, props.searchedWeapons]);

    const defaultColumn = React.useMemo(
        () => ({
            width: 150,
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

    const weaponTypeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            return filterValue.weaponTypeFilter.includes(row.original.weaponType) || filterValue.searchedWeapons.includes(row.original.weaponname);
        });
    };

    const affinityTypeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            if (row.original.maxUpgrade === 0 || row.original.maxUpgrade === 10) {
                return true;
            } else {
                return filterValue.affinityTypeFilter.includes(row.original.affinity) || (filterValue.searchedWeapons.includes(row.original.weaponname) && filterValue.affinityTypeFilter.includes(row.original.affinity));
            }
        });
    };

    const upgradeFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            if (row.original.maxUpgrade === 0 || row.original.maxUpgrade === 10) {
                return filterValue.somberFilter || filterValue.searchedWeapons.includes(row.original.weaponname);
            } else if (row.original.maxUpgrade === 25) {
                return filterValue.smithingFilter || filterValue.searchedWeapons.includes(row.original.weaponname);
            }

            return false;
        });
    };

    const hideNoReqWeaponsFilter = (rows, id, filterValue) => {
        return rows.filter((row) => {
            if (filterValue.hideNoReqWeapons === true) {
                return true;
            }

            return !row.original.missedReq || filterValue.searchedWeapons.includes(row.original.weaponname);
        });
    };

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
                if (row.accessor === "fullweaponname") {
                    row.Cell = ({ row, value }) => {
                        return (
                            <a target="_blank" rel="noopener noreferrer" href={"https://eldenring.wiki.fextralife.com/" + row.original.weaponname} >{value}</a>
                        );
                    };
                    row.width = 340;
                } else if (row.accessor === "weaponType") {
                    row.filter = weaponTypeFilter;
                    row.width = 180;
                } else if (row.accessor === "affinity") {
                    row.filter = affinityTypeFilter;
                    row.width = 110;
                } else if (new Set(['final_physical', 'final_magic', 'final_fire', 'final_lightning', 'final_holy', 'final_total_ar', 'final_sorcery_scaling']).has(row.accessor)) {
                    row.width = 90;
                } else if (row.accessor === "type1" || row.accessor === "type2") {
                    row.Cell = ({ value }) => {
                        return (
                            <>{value ? value : '-'}</>
                        );
                    };
                    row.width = 125;
                } else if (row.accessor === "final_passive1" || row.accessor === "final_passive2") {
                    row.Cell = ({ value }) => {
                        return (
                            <>{value !== 0 ? value : '-'}</>
                        );
                    };
                    row.width = 110;
                } else if (new Set(['str_scaling_letter', 'dex_scaling_letter', 'int_scaling_letter', 'fai_scaling_letter', 'arc_scaling_letter']).has(row.accessor)) {
                    row.Cell = ({ value }) => {
                        return (
                            <>{value ? value.letter !== '-' ? value.letter + ' (' + value.value + ')' : value.letter : '-'}</>
                        );
                    };
                    row.width = 115;
                } else if (new Set(['strreq', 'dexreq', 'intreq', 'faireq', 'arcreq']).has(row.accessor)) {
                    row.width = 80;
                } else if (row.accessor === "missedReq")
                    row.filter = hideNoReqWeaponsFilter;
                else if (row.accessor === "maxUpgrade") {
                    row.filter = upgradeFilter;
                    row.Cell = ({ value }) => {
                        return (
                            <>{value === 25 || value === 10? 'Somber' : 'Smithing'}</>
                        );
                    };
                    row.width = 89;
                }
            });

            return newColumns;
        },
        []
    );


    const initialState = { hiddenColumns: ['missedReq'] };

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
        initialState,
    },
        useFilters,
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
                    className={row.original.missedReq === true ? "tr highlight-red" : "tr"}
                    // className="tr"
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
                                                    ? <FaSortDown/>
                                                    : <FaSortUp/>
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
                        itemSize={40}
                        width={totalColumnsWidth + scrollBarSize}
                    >
                        {RenderRow}
                    </FixedSizeList>
                </div>
            </div>
        </div>
    );
}