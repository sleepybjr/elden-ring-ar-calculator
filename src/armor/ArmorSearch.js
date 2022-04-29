import SingleItemSearchBar from '../component/SingleItemSeachBar';
import Collapsible from 'react-collapsible';

import Helmets_Select from '../json/head_group.json';
import Chest_Select from '../json/body_group.json';
import Gauntlets_Select from '../json/arm_group.json';
import Legs_Select from '../json/leg_group.json';

const armorTypes = {
    helmet: Helmets_Select,
    chest: Chest_Select,
    gauntlets: Gauntlets_Select,
    legs: Legs_Select,
};

export default function ArmorSearch(props) {
    const armorTypeKeys = Object.keys(armorTypes);

    return (
        <div className="large-spacing">
            <div className="build-collapsible">
                <Collapsible trigger="Armor Information">
                    <p className="align-left">
                        Due to armor optimization being a <a target="_blank" rel="noopener noreferrer" href={"https://en.wikipedia.org/wiki/Knapsack_problem"}>Knapsack problem</a>, you
                        currently <b>must select at least one piece of armor</b>.
                        <br />
                        <br />
                        There are over 300 million combinations to check when searching for a complete armor set, which takes hours to do.
                        We are currently looking into how to speed up search times for a full armor set search.
                        <br />
                        <br />
                        An armor type that is not selected will be optimized (helmet, chest, gauntlets, legs).
                    </p>
                </Collapsible>
            </div>

            {/* need to change to className that can collapse*/}
            <div>
                {armorTypeKeys.map((armorType, index) => {
                    if (index % 2 === 0) {
                        const left = armorTypeKeys[index];
                        const right = armorTypeKeys[index + 1];
                        return (
                            <div key={index}>
                                <SingleItemSearchBar
                                    key={left}
                                    handleSearchItemsChange={(e) => props.handleSearchArmorItemsChange(e, left)}
                                    searchedItems={props.searchedArmor[left]}
                                    options={armorTypes[left].options}
                                    placeholder={"Select equipped " + left + "..."}
                                />
                                <SingleItemSearchBar
                                    key={right}
                                    handleSearchItemsChange={(e) => props.handleSearchArmorItemsChange(e, right)}
                                    searchedItems={props.searchedArmor[right]}
                                    options={armorTypes[right].options}
                                    placeholder={"Select equipped " + right + "..."}
                                />
                            </div>
                        )
                    } else {
                        return null;
                    }
                })}
            </div>
        </div>
    )
};