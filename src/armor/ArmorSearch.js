import SingleItemSearchBar from '../component/SingleItemSeachBar';
import Collapsible from 'react-collapsible';

import Helmets_Select from '../json/armor/head_group.json';
import Chest_Select from '../json/armor/body_group.json';
import Gauntlets_Select from '../json/armor/arm_group.json';
import Legs_Select from '../json/armor/leg_group.json';

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
                        There are over 300 million combinations to check when searching for a complete armor set (all four pieces of armor), which can take hours to do.
                        <br />
                        <br />
                        We are reducing the combinations by picking the "optimal" armor piece by weight based on multipliers. For example, there are twenty helmets at 5.1 
                        weight. Rather than using all twenty helmets, we pick the best helmet based on your multipliers and helmet stats, then use that while searching for 
                        optimizations. For example, if all multipliers are set to 1, this would use the Greathood helmet. We are still looking into more ways to get 
                        better optimized equipment.
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