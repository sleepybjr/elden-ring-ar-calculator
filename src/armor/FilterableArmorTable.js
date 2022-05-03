import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import ArmorTable from './ArmorTable';
import { getPhyCalcData } from '../weapons/FilterableWeaponTable';

import Weapon_Reqs from '../json/weapons/weapon_reqs.json';

import Armor_Data from '../json/armor/armor_data.json';

import Talisman_Data from '../json/talismans/talisman_data.json';

import { FaSpinner } from 'react-icons/fa';

import RollTypes from './RollTypes';
import WeaponSearch from './WeaponSearch';
import ArmorSearch from './ArmorSearch';
import TalismanSearch from './TalismanSearch';
import DisplayMultipliers from './DisplayMultipliers';
import DisplayMinimums from './DisplayMinimums';

const startArmorResistances = {
    physical_absorption: 0,
    strike_absorption: 0,
    slash_absorption: 0,
    thrust_absorption: 0,
    magic_absorption: 0,
    fire_absorption: 0,
    lightning_absorption: 0,
    holy_absorption: 0,
    immunity: 0,
    robustness: 0,
    focus: 0,
    vitality: 0,
    poise: 0,
}

const startArmorResistancesMultiplier = {
    physical_absorption: 1,
    strike_absorption: 1,
    slash_absorption: 1,
    thrust_absorption: 1,
    magic_absorption: 1,
    fire_absorption: 1,
    lightning_absorption: 1,
    holy_absorption: 1,
    immunity: 1,
    robustness: 1,
    focus: 1,
    vitality: 1,
    poise: 1,
}

// needed because javascript uses floats weird
function roundNumber(number, decimals) {
    return parseFloat(number.toFixed(decimals));
}

const NORMAL_ROLL_DEFAULT = 69.9;

const IS_WEARING = 0;
const IS_NOT_WEARING = 1;

const MAX_LEVEL = 99;

// const worker = new Worker(new URL('./worker.js', import.meta.url)); // renders twice but only in strict mode

export default function FilterableArmorTable() {
    // const worker = React.useMemo(() => new WorkerBuilder(Worker), []); // renders twice but only in strict mode
    const worker = React.useMemo(() => new Worker(new URL('./ArmorOptimizerWorker.js', import.meta.url)), []); // renders twice but only in strict mode

    const levels = useSelector((state) => state.allLevels.levels);

    const [rollTypeChoice, setRollTypeChoice] = useState(NORMAL_ROLL_DEFAULT);

    const [searchedWeapons, setSearchedWeapons] = useState({});
    const [searchedArmor, setSearchedArmor] = useState({});
    const [searchedTalismans, setSearchedTalismans] = useState([]);

    const [currEquippedArmor, setCurrEquippedArmor] = useState([]);

    const [maxEquip, setMaxEquip] = useState(0);
    const [maxMultiplier, setMaxMultiplier] = useState(1);
    const [levelModifier, setLevelModifier] = useState(0);
    const [currEquip, setCurrEquip] = useState(0);
    const [loadRemaining, setLoadRemaining] = useState(0);

    const [vykes, setVykes] = useState(false);

    const [preppedData, setPreppedData] = useState([]);
    const [errors, setErrors] = useState("");

    const [resistances, setResistances] = useState({ ...startArmorResistances });
    const [resistancesMultiplier, setResistancesMultiplier] = useState({ ...startArmorResistancesMultiplier });

    const [spinner, setSpinner] = useState(null);
    const [disabledButton, setDisabledButton] = useState(false);

    useEffect(() => {
        worker.onmessage = ({ data: { output, equippedArmor } }) => {
            if (output === -1) {
                setErrors("Incorrect input, unable to find an answer.");
                setPreppedData([]);
                setSpinner(null);
                setDisabledButton(false);
                return;
            }

            if (output.length === 0) {
                setErrors("No results");
                setPreppedData([]);
                setSpinner(null);
                setDisabledButton(false);
                return;
            }

            // // get pre status armor and add it here too.

            const trueOutput = [];
            for (const row of output) {
                const newRow = {
                    helm_name: "-",
                    chest_name: "-",
                    gauntlet_name: "-",
                    leg_name: "-",
                    weight: 0,
                    physical_absorption: 0,
                    strike_absorption: 0,
                    slash_absorption: 0,
                    thrust_absorption: 0,
                    magic_absorption: 0,
                    fire_absorption: 0,
                    lightning_absorption: 0,
                    holy_absorption: 0,
                    immunity: 0,
                    robustness: 0,
                    focus: 0,
                    vitality: 0,
                    poise: 0,
                }

                for (const armor of row.armorSet) {
                    if (armor.equipment_type === "Head") {
                        newRow.helm_name = armor.name;
                    } else if (armor.equipment_type === "Body") {
                        newRow.chest_name = armor.name;
                    } else if (armor.equipment_type === "Arm") {
                        newRow.gauntlet_name = armor.name;
                    } else if (armor.equipment_type === "Leg") {
                        newRow.leg_name = armor.name;
                    }

                    newRow['physical_absorption' + armor.equipment_type] = (1 - armor.physical_absorption);
                    newRow['strike_absorption' + armor.equipment_type] = (1 - armor.strike_absorption);
                    newRow['slash_absorption' + armor.equipment_type] = (1 - armor.slash_absorption);
                    newRow['thrust_absorption' + armor.equipment_type] = (1 - armor.thrust_absorption);
                    newRow['magic_absorption' + armor.equipment_type] = (1 - armor.magic_absorption);
                    newRow['fire_absorption' + armor.equipment_type] = (1 - armor.fire_absorption);
                    newRow['lightning_absorption' + armor.equipment_type] = (1 - armor.lightning_absorption);
                    newRow['holy_absorption' + armor.equipment_type] = (1 - armor.holy_absorption);

                    newRow.weight += armor.weight;
                    newRow.immunity += armor.immunity;
                    newRow.robustness += armor.robustness;
                    newRow.focus += armor.focus;
                    newRow.vitality += armor.vitality;
                    newRow.poise += armor.poise;
                }

                trueOutput.push(newRow);
            }

            for (const row of trueOutput) {
                for (const armor of equippedArmor) {
                    if (armor.equipment_type === "Head") {
                        row.helm_name = armor.name;
                    } else if (armor.equipment_type === "Body") {
                        row.chest_name = armor.name;
                    } else if (armor.equipment_type === "Arm") {
                        row.gauntlet_name = armor.name;
                    } else if (armor.equipment_type === "Leg") {
                        row.leg_name = armor.name;
                    }

                    row['physical_absorption' + armor.equipment_type] = (1 - armor.physical_absorption);
                    row['strike_absorption' + armor.equipment_type] = (1 - armor.strike_absorption);
                    row['slash_absorption' + armor.equipment_type] = (1 - armor.slash_absorption);
                    row['thrust_absorption' + armor.equipment_type] = (1 - armor.thrust_absorption);
                    row['magic_absorption' + armor.equipment_type] = (1 - armor.magic_absorption);
                    row['fire_absorption' + armor.equipment_type] = (1 - armor.fire_absorption);
                    row['lightning_absorption' + armor.equipment_type] = (1 - armor.lightning_absorption);
                    row['holy_absorption' + armor.equipment_type] = (1 - armor.holy_absorption);

                    row.weight += armor.weight;

                    row.immunity += armor.immunity;
                    row.robustness += armor.robustness;
                    row.focus += armor.focus;
                    row.vitality += armor.vitality;
                    row.poise += armor.poise;
                }
            }

            for (const row of trueOutput) {
                row.physical_absorption = 1 - row.physical_absorptionHead * row.physical_absorptionBody * row.physical_absorptionArm * row.physical_absorptionLeg;
                row.strike_absorption = 1 - row.strike_absorptionHead * row.strike_absorptionBody * row.strike_absorptionArm * row.strike_absorptionLeg;
                row.slash_absorption = 1 - row.slash_absorptionHead * row.slash_absorptionBody * row.slash_absorptionArm * row.slash_absorptionLeg;
                row.thrust_absorption = 1 - row.thrust_absorptionHead * row.thrust_absorptionBody * row.thrust_absorptionArm * row.thrust_absorptionLeg;
                row.magic_absorption = 1 - row.magic_absorptionHead * row.magic_absorptionBody * row.magic_absorptionArm * row.magic_absorptionLeg;
                row.fire_absorption = 1 - row.fire_absorptionHead * row.fire_absorptionBody * row.fire_absorptionArm * row.fire_absorptionLeg;
                row.lightning_absorption = 1 - row.lightning_absorptionHead * row.lightning_absorptionBody * row.lightning_absorptionArm * row.lightning_absorptionLeg;
                row.holy_absorption = 1 - row.holy_absorptionHead * row.holy_absorptionBody * row.holy_absorptionArm * row.holy_absorptionLeg;
            }

            setSpinner(null);
            setDisabledButton(false);
            setPreppedData(trueOutput);
        };
        return () => worker.terminate();
    }, [worker]);

    function handleClickCalculateArmor(event) {
        if (disabledButton === true) {
            return;
        }
        setSpinner(<FaSpinner className="icon_pulse" />);
        setErrors("");
        setDisabledButton(true);

        const equippedArmor = {
            Head: searchedArmor.hasOwnProperty("helmet") && searchedArmor.helmet !== null ? IS_WEARING : IS_NOT_WEARING,
            Body: searchedArmor.hasOwnProperty("chest") && searchedArmor.chest !== null ? IS_WEARING : IS_NOT_WEARING,
            Arm: searchedArmor.hasOwnProperty("gauntlets") && searchedArmor.gauntlets !== null ? IS_WEARING : IS_NOT_WEARING,
            Leg: searchedArmor.hasOwnProperty("legs") && searchedArmor.legs !== null ? IS_WEARING : IS_NOT_WEARING,
        };


        if (equippedArmor.Head === IS_WEARING && equippedArmor.Body === IS_WEARING && equippedArmor.Arm === IS_WEARING && equippedArmor.Leg === IS_WEARING) {
            const singleArmorRow = {
                helm_name: "-",
                chest_name: "-",
                gauntlet_name: "-",
                leg_name: "-",
                weight: 0,
                physical_absorption: 0,
                strike_absorption: 0,
                slash_absorption: 0,
                thrust_absorption: 0,
                magic_absorption: 0,
                fire_absorption: 0,
                lightning_absorption: 0,
                holy_absorption: 0,
                immunity: 0,
                robustness: 0,
                focus: 0,
                vitality: 0,
                poise: 0,
            }

            for (const armor of currEquippedArmor) {
                if (armor.equipment_type === "Head") {
                    singleArmorRow.helm_name = armor.name;
                } else if (armor.equipment_type === "Body") {
                    singleArmorRow.chest_name = armor.name;
                } else if (armor.equipment_type === "Arm") {
                    singleArmorRow.gauntlet_name = armor.name;
                } else if (armor.equipment_type === "Leg") {
                    singleArmorRow.leg_name = armor.name;
                }

                singleArmorRow['physical_absorption' + armor.equipment_type] = (1 - armor.physical_absorption);
                singleArmorRow['strike_absorption' + armor.equipment_type] = (1 - armor.strike_absorption);
                singleArmorRow['slash_absorption' + armor.equipment_type] = (1 - armor.slash_absorption);
                singleArmorRow['thrust_absorption' + armor.equipment_type] = (1 - armor.thrust_absorption);
                singleArmorRow['magic_absorption' + armor.equipment_type] = (1 - armor.magic_absorption);
                singleArmorRow['fire_absorption' + armor.equipment_type] = (1 - armor.fire_absorption);
                singleArmorRow['lightning_absorption' + armor.equipment_type] = (1 - armor.lightning_absorption);
                singleArmorRow['holy_absorption' + armor.equipment_type] = (1 - armor.holy_absorption);

                singleArmorRow.weight += armor.weight;

                singleArmorRow.immunity += armor.immunity;
                singleArmorRow.robustness += armor.robustness;
                singleArmorRow.focus += armor.focus;
                singleArmorRow.vitality += armor.vitality;
                singleArmorRow.poise += armor.poise;
            }

            singleArmorRow.physical_absorption = 1 - singleArmorRow.physical_absorptionHead * singleArmorRow.physical_absorptionBody * singleArmorRow.physical_absorptionArm * singleArmorRow.physical_absorptionLeg;
            singleArmorRow.strike_absorption = 1 - singleArmorRow.strike_absorptionHead * singleArmorRow.strike_absorptionBody * singleArmorRow.strike_absorptionArm * singleArmorRow.strike_absorptionLeg;
            singleArmorRow.slash_absorption = 1 - singleArmorRow.slash_absorptionHead * singleArmorRow.slash_absorptionBody * singleArmorRow.slash_absorptionArm * singleArmorRow.slash_absorptionLeg;
            singleArmorRow.thrust_absorption = 1 - singleArmorRow.thrust_absorptionHead * singleArmorRow.thrust_absorptionBody * singleArmorRow.thrust_absorptionArm * singleArmorRow.thrust_absorptionLeg;
            singleArmorRow.magic_absorption = 1 - singleArmorRow.magic_absorptionHead * singleArmorRow.magic_absorptionBody * singleArmorRow.magic_absorptionArm * singleArmorRow.magic_absorptionLeg;
            singleArmorRow.fire_absorption = 1 - singleArmorRow.fire_absorptionHead * singleArmorRow.fire_absorptionBody * singleArmorRow.fire_absorptionArm * singleArmorRow.fire_absorptionLeg;
            singleArmorRow.lightning_absorption = 1 - singleArmorRow.lightning_absorptionHead * singleArmorRow.lightning_absorptionBody * singleArmorRow.lightning_absorptionArm * singleArmorRow.lightning_absorptionLeg;
            singleArmorRow.holy_absorption = 1 - singleArmorRow.holy_absorptionHead * singleArmorRow.holy_absorptionBody * singleArmorRow.holy_absorptionArm * singleArmorRow.holy_absorptionLeg;

            setSpinner(null);
            setPreppedData([singleArmorRow]);
            setDisabledButton(false);
            return;
        }

        if (loadRemaining <= 0) {
            setErrors("The load remaining cannot be less than 0.");
            setSpinner(null);
            setDisabledButton(false);
            return;
        }

        const adjustedResistances = { damage_negation: {}, resistance: {} }
        for (const key of Object.keys(resistances)) {
            if (resistances[key] === "") {
                setErrors("All minimums must have a value. Default: 0.");
                setSpinner(null);
                setDisabledButton(false);
                return;
            }

            if (new Set(['physical_absorption', 'strike_absorption', 'slash_absorption', 'thrust_absorption', 'magic_absorption', 'fire_absorption', 'lightning_absorption', 'holy_absorption']).has(key)) {
                adjustedResistances.damage_negation[key] = resistances[key] / 100;
            } else {
                adjustedResistances.resistance[key] = resistances[key];
            }
        }

        for (const key of Object.keys(resistancesMultiplier)) {
            if (resistancesMultiplier[key] === "") {
                setErrors("All multipliers must have a value. Default: 1.");
                setSpinner(null);
                setDisabledButton(false);
                return;
            }
        }

        worker.postMessage({
            equippedArmor: equippedArmor,
            loadRemaining: loadRemaining,
            adjustedResistances: adjustedResistances,
            resistancesMultiplier: resistancesMultiplier,
            currEquippedArmor: currEquippedArmor,
        });
    };

    function handleChangeRollTypes(value) {
        setRollTypeChoice(value);
    };

    function handleSearchWeaponItemsChange(searchedWeapon, weaponHand) {
        const newSearchedWeapons = { ...searchedWeapons };

        newSearchedWeapons[weaponHand] = searchedWeapon;

        setSearchedWeapons(newSearchedWeapons);
    };

    function handleSearchArmorItemsChange(armorPiece, armorType) {
        const newSearchedArmor = { ...searchedArmor };

        newSearchedArmor[armorType] = armorPiece;

        setSearchedArmor(newSearchedArmor);
    };

    function handleSearchTalismansItemsChange(searchedTalisman) {
        setSearchedTalismans(searchedTalisman);
    };

    function handleResistanceChange(event) {
        const newValue = event.target.value;
        const newId = event.target.id;

        let newResistances = { ...resistances };

        newResistances[newId] = newValue ? parseFloat(newValue) : "";

        // need to limit length as well
        if (newResistances[newId] > 300) {
            newResistances[newId] = 300;
        }

        setResistances(newResistances);
    };

    function resetResistanceClick() {
        setResistances({ ...startArmorResistances });
    }

    function handleResistanceMultiplierChange(event) {
        const newValue = event.target.value;
        const newId = event.target.id.replace('_multiplier', '');

        let newResistances = { ...resistancesMultiplier };

        newResistances[newId] = newValue ? parseFloat(newValue) : "";

        // need to limit length as well
        if (newResistances[newId] > 100) {
            newResistances[newId] = 100;
        }

        setResistancesMultiplier(newResistances);
    };

    function resetResistanceMultiplierClick() {
        setResistancesMultiplier({ ...startArmorResistancesMultiplier });
    }

    useEffect(() => {
        // i thought levels are strings, not ints
        let currentEnduranceLevel = parseInt(levels.endurance) + levelModifier;
        if (currentEnduranceLevel > MAX_LEVEL) {
            currentEnduranceLevel = MAX_LEVEL;
        }

        const newMaxLoad = getPhyCalcData(220, currentEnduranceLevel);
        setMaxEquip(newMaxLoad * maxMultiplier);
    }, [levels.endurance, maxMultiplier, levelModifier]);

    useEffect(() => {
        // count the amount of weapons
        const searchedWeaponsMap = {};
        for (const hand of Object.keys(searchedWeapons)) {
            const weaponInHand = searchedWeapons[hand];
            if (weaponInHand !== null) {
                if (searchedWeaponsMap.hasOwnProperty(weaponInHand.label))
                    searchedWeaponsMap[weaponInHand.label]++;
                else
                    searchedWeaponsMap[weaponInHand.label] = 1;
            }
        }

        const searchedTalismansSet = new Set();
        for (const talisman of searchedTalismans) {
            searchedTalismansSet.add(talisman.label);
        }

        let newCurrentLoad = 0;

        // get weapon weight values from amount of weapons
        for (let element of Weapon_Reqs) {
            if (searchedWeaponsMap.hasOwnProperty(element.weaponname)) {
                newCurrentLoad += (element.weight * searchedWeaponsMap[element.weaponname]);
                delete searchedWeaponsMap[element.weaponname]; // need to remove due to multiple weapon names
            }
        }

        for (let element of Talisman_Data) {
            if (searchedTalismansSet.has(element.name)) {
                newCurrentLoad += element.weight;
                newCurrentLoad = roundNumber(newCurrentLoad, 1);
            }
        }

        // get list of armor names that were searched
        const valuesSearchedArmor = new Set(Object.entries(searchedArmor).flatMap(([key, value]) => value !== null ? value.label : []));

        let newCurrEquippedArmor = [];
        for (let element of Armor_Data) {
            if (valuesSearchedArmor.has(element.name)) {
                newCurrentLoad += element.weight;
                newCurrentLoad = roundNumber(newCurrentLoad, 1);
                newCurrEquippedArmor.push(element);
            }
        }

        setCurrEquippedArmor(newCurrEquippedArmor);
        setCurrEquip(newCurrentLoad);
    }, [searchedWeapons, searchedArmor, searchedTalismans]);

    useEffect(() => {
        const searchedTalismansSet = new Set();
        for (const talisman of searchedTalismans) {
            searchedTalismansSet.add(talisman.label);
        }

        let currentMultiplier = 1;
        let currentLevelModifier = 0

        for (let element of Talisman_Data) {
            if (searchedTalismansSet.has(element.name)) {
                if (element.passive_1.equip_load_percent !== undefined) {
                    currentMultiplier *= (1 + element.passive_1.equip_load_percent);
                }
                if (element.passive_1.endurance !== undefined) {
                    currentLevelModifier += element.passive_1.endurance;
                }
            }
        }

        if (vykes === true) {
            currentMultiplier *= 1.15; // amount of armor increase from vykes dragonbolt
        }

        setLevelModifier(currentLevelModifier);
        setMaxMultiplier(currentMultiplier);
    }, [searchedTalismans, vykes]);

    useEffect(() => {
        const loadLeft = roundNumber((maxEquip * (rollTypeChoice / 100)) - currEquip, 2);
        setLoadRemaining(loadLeft);

    }, [maxEquip, rollTypeChoice, currEquip]);

    return (
        <div className='large-spacing'>
            <WeaponSearch handleSearchWeaponItemsChange={handleSearchWeaponItemsChange} searchedWeapons={searchedWeapons} />
            <ArmorSearch handleSearchArmorItemsChange={handleSearchArmorItemsChange} searchedArmor={searchedArmor} />
            <TalismanSearch handleSearchTalismansItemsChange={handleSearchTalismansItemsChange} searchedTalismans={searchedTalismans} />
            <div className="small-spacing">
                <label htmlFor="vykes">Vyke's Dragonbolt</label>
                <input type="checkbox" id="vykes" name="vykes" checked={vykes} onChange={() => setVykes(!vykes)} />
            </div>
            <RollTypes handleChangeRollTypes={handleChangeRollTypes} rollTypeChoice={rollTypeChoice} />

            <div className="large-spacing">
                <div className="tiny-spacing">
                    <label htmlFor="curr-equip">Current Equipment Weight</label>
                    <input
                        type="number"
                        id="curr-equip"
                        name="curr-equip"
                        value={currEquip}
                        disabled={true}
                    />
                </div>
                <div className="tiny-spacing">
                    <label htmlFor="max-equip">Max Equipment Weight</label>
                    <input
                        type="number"
                        id="max-equip"
                        name="max-equip"
                        value={maxEquip}
                        disabled={true}
                    />
                </div>
                <div className="tiny-spacing important-field">
                    Weight Remaining {loadRemaining}
                </div>
            </div>

            <DisplayMinimums
                handleResistanceChange={handleResistanceChange}
                resistances={resistances}
                resetResistanceClick={resetResistanceClick}
            />

            <DisplayMultipliers
                handleResistanceMultiplierChange={handleResistanceMultiplierChange}
                resistancesMultiplier={resistancesMultiplier}
                resetResistanceMultiplierClick={resetResistanceMultiplierClick}
            />

            <div className="large-spacing spacing">
                <div className="text-description-spacing">
                    Displays up to 1,000 sets of best matching armor.
                </div>
                <div>
                    <div className="error">{errors}</div>
                    <div className="in-progress">
                        <button className="all-button-style all-button-style-bg" disabled={disabledButton} onClick={handleClickCalculateArmor}>Calculate Best Armor</button>
                        <span>{spinner}</span>
                    </div>
                </div>
            </div>

            <ArmorTable preppedData={preppedData} />
        </div>
    );
}