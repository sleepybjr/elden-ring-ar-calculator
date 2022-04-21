import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { handleWeaponLevelChange, handleLevelChange, handleTwoHandedChange, handleAllWeaponLevelChange, calculateTotalLevel} from './allLevelsSlice';

import Levels from './Levels';
import WeaponLevels from './WeaponLevels';
import OtherLevels from './OtherLevels';
import Saves from './Saves';

export default function InputStats() {
    const levels = useSelector((state) => state.allLevels.levels);
    const weaponLevels = useSelector((state) => state.allLevels.weaponLevels);
    const twoHanded = useSelector((state) => state.allLevels.twoHanded);

    const dispatch = useDispatch();

    useEffect(() => {
        // need to handle if get returns nothing
        const windowUrl = window.location.search;
        const params = new URLSearchParams(windowUrl);

        let newLevels = { };

        const strength = params.get('str');
        const dexterity = params.get('dex');
        const intelligence = params.get('int');
        const faith = params.get('fai');
        const arcane = params.get('arc');
        const vigor = params.get('vig');
        const mind = params.get('min');
        const endurance = params.get('end');
        const somber = params.get('somber');
        const smithing = params.get('smith');
        let newTwoHanded = params.get('twoHanded');


        if (strength !== null) {
            newLevels.strength = strength;
            newLevels.twohand_strength = Math.trunc(strength * 1.5);
        }
        if (dexterity !== null) {
            newLevels.dexterity = dexterity;
        }
        if (intelligence !== null) {
            newLevels.intelligence = intelligence;
        }
        if (faith !== null) {
            newLevels.faith = faith;
        }
        if (arcane !== null) {
            newLevels.arcane = arcane;
        }
        if (vigor !== null) {
            newLevels.vigor = vigor;
        }
        if (mind !== null) {
            newLevels.mind = mind;
        }
        if (endurance !== null) {
            newLevels.endurance = endurance;
        }

        newLevels.total_level = calculateTotalLevel(newLevels);

        let newWeaponLevels = { };

        if (somber !== null) {
            newWeaponLevels.somber = somber;
        }
        if (smithing !== null) {
            newWeaponLevels.smithing = smithing;
        }
        if (newTwoHanded === null) {
            newTwoHanded = false;
        } else {
            newTwoHanded = newTwoHanded === 'true';
        }
        dispatch(handleLevelChange(newLevels));
        dispatch(handleAllWeaponLevelChange(newWeaponLevels));
        dispatch(handleTwoHandedChange(newTwoHanded));

        window.history.pushState(null, "", window.location.href.split("?")[0]);
      }, [dispatch]);

    function handleLoadSave(save) {
        // i can filter out what actually gets loaded here
        dispatch(handleLevelChange(save.levels));
        dispatch(handleAllWeaponLevelChange(save.weaponLevels));
        dispatch(handleTwoHandedChange(save.twoHanded));
    };

    return (
        <div>
            <Levels
                handleLevelChange={(newLevels) => dispatch(handleLevelChange(newLevels))}
                handleTwoHandedChange={(isTwoHanded) => dispatch(handleTwoHandedChange(isTwoHanded))}
                levels={levels}
                twoHanded={twoHanded}
            />

            <OtherLevels
                handleLevelChange={(newLevels) => dispatch(handleLevelChange(newLevels))}
                levels={levels}
            />

            <WeaponLevels
            handleWeaponLevelChange={(inputWeaponLevel, isSomber) => dispatch(handleWeaponLevelChange({inputWeaponLevel, isSomber}))}
            weaponLevels={weaponLevels}
            />
            
            <Saves
                handleLoadSave={handleLoadSave}
                levels={levels}
                weaponLevels={weaponLevels}
                twoHanded={twoHanded}
            />
        </div>
    );
}