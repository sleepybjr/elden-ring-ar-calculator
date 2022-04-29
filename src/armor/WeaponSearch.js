import SingleItemSearchBar from '../component/SingleItemSeachBar';

import Weapons_Select from '.././json/weapon_groups.json';

const weaponHands = [
    "LH1",
    "LH2",
    "LH3",
    "RH1",
    "RH2",
    "RH3",
];

export default function WeaponSearch(props) {
    return (
        // need to change this to something that allows the boxes to collapse on smaller screens
        <div>
            {weaponHands.map((hand, index) => {
                if (index % 3 === 0) {
                    const hand1 = weaponHands[index];
                    const hand2 = weaponHands[index + 1];
                    const hand3 = weaponHands[index + 2];
                    return (
                        <div key={index}>
                            <SingleItemSearchBar
                                key={hand1}
                                handleSearchItemsChange={(e) => props.handleSearchWeaponItemsChange(e, hand1)}
                                searchedItems={props.searchedWeapons[hand1]}
                                options={Weapons_Select}
                                placeholder={"Select equipped " + hand1 + " weapon..."}
                            />
                            <SingleItemSearchBar
                                key={hand2}
                                handleSearchItemsChange={(e) => props.handleSearchWeaponItemsChange(e, hand2)}
                                searchedItems={props.searchedWeapons[hand2]}
                                options={Weapons_Select}
                                placeholder={"Select equipped " + hand2 + " weapon..."}
                            />
                            <SingleItemSearchBar
                                key={hand3}
                                handleSearchItemsChange={(e) => props.handleSearchWeaponItemsChange(e, hand3)}
                                searchedItems={props.searchedWeapons[hand3]}
                                options={Weapons_Select}
                                placeholder={"Select equipped " + hand3 + " weapon..."}
                            />
                        </div>
                    )
                } else {
                    return null;
                }
            })}
        </div>
    )
};