import { useEffect, useState } from 'react';
import SearchBar from '../component/SearchBar';

import Talisman_Select from '../json/talismans/talisman_groups.json';
import Talisman_Data from '../json/talismans/talisman_data.json';

const TOTAL_TALISMANS = 4;
let talismanAccessoryGroupMap = {};
let talismanNameMap = {};

function groupBy(arr, property) {
    return arr.reduce((acc, cur) => {
        acc[cur[property]] = [...acc[cur[property]] || [], cur];
        return acc;
    }, {});
}

export default function TalismanSearch(props) {
    const [ignoreList, setIgnoredList] = useState(new Set());

    const filterOption = (candidate, input) => {
        if (ignoreList.has(candidate.label)) {
            return false;
        }
        return candidate.data.__isNew__ || candidate.label.includes(input);
    };

    useEffect(() => {
        const newIgnoreList = new Set();
        for (const talisman of props.searchedTalismans) {
            if (talismanNameMap[talisman.label])
                for (const element of talismanAccessoryGroupMap[talismanNameMap[talisman.label][0].accessory_group]) {
                    newIgnoreList.add(element.name);
                }
        }
        setIgnoredList(newIgnoreList);
    }, [props.searchedTalismans]);

    useEffect(() => {
        talismanAccessoryGroupMap = groupBy(Talisman_Data, 'accessory_group');
        talismanNameMap = groupBy(Talisman_Data, 'name');
    }, []);

    return (
        <div className="large-spacing">
            <div className="text-description-spacing">
                Talisman's are used in weight, max weight and endurance.<br />
                Other buffs are not shown in the result table below yet.
            </div>
            <SearchBar
                handleSearchItemsChange={props.handleSearchTalismansItemsChange}
                searchedItems={props.searchedTalismans}
                options={Talisman_Select.options}
                placeholder="Search equipped talismans..."
                maxLimit={TOTAL_TALISMANS}
                filterOption={filterOption}
            />
        </div>
    )
};