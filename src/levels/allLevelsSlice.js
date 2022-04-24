import { createSlice } from '@reduxjs/toolkit';

export function calculateTotalLevel(newLevels) {
    const newLevel = 1 +
        Number(newLevels.strength) +
        Number(newLevels.dexterity) +
        Number(newLevels.intelligence) +
        Number(newLevels.faith) +
        Number(newLevels.arcane) +
        Number(newLevels.vigor) +
        Number(newLevels.mind) +
        Number(newLevels.endurance) -
        80;
    return newLevel;
}

export const allLevelsSlice = createSlice({
  name: 'allLevels',
  initialState: {
    weaponLevels: {
        'somber': 10,
        'smithing': 25,
    },
    levels: {
        'strength': 99,
        'twohand_strength': Math.trunc(99 * 1.5),
        'dexterity': 99,
        'intelligence': 99,
        'faith': 99,
        'arcane': 99,
        'vigor': 99,
        'mind': 99,
        'endurance': 99,
        'total_level': 713,
    },
    twoHanded: false,
  },
  reducers: {
    handleWeaponLevelChange: (state, action) => {
        const isSomber = action.payload.isSomber;
        const inputWeaponLevel = action.payload.inputWeaponLevel;

        let newWeaponLevels = { ...state.weaponLevels };
        if (isSomber === true) {
            newWeaponLevels.somber = inputWeaponLevel;
        } else {
            newWeaponLevels.smithing = inputWeaponLevel;
        }
        state.weaponLevels = newWeaponLevels;
    },
    handleAllWeaponLevelChange: (state, action) => {
        let newWeaponLevels = { ...state.weaponLevels };
        const inputWeaponLevels = action.payload;

        if ('somber' in inputWeaponLevels) {
            newWeaponLevels.somber = inputWeaponLevels.somber;
        }
        if ('smithing' in inputWeaponLevels) {
            newWeaponLevels.smithing = inputWeaponLevels.smithing;
        }
        state.weaponLevels = newWeaponLevels;
    },
    handleLevelChange: (state, action) => {
        let newLevels = { ...state.levels };

        const type = action.payload;

        if ('strength' in type) {
            newLevels.strength = type.strength;
            newLevels.twohand_strength = Math.trunc(type.strength * 1.5);
        }
        if ('dexterity' in type) {
            newLevels.dexterity = type.dexterity;
        }
        if ('intelligence' in type) {
            newLevels.intelligence = type.intelligence;
        }
        if ('faith' in type) {
            newLevels.faith = type.faith;
        }
        if ('arcane' in type) {
            newLevels.arcane = type.arcane;
        }
        if ('vigor' in type) {
            newLevels.vigor = type.vigor;
        }
        if ('mind' in type) {
            newLevels.mind = type.mind;
        }
        if ('endurance' in type) {
            newLevels.endurance = type.endurance;
        }

        newLevels.total_level = calculateTotalLevel(newLevels);

        state.levels = newLevels;
    },
    handleTwoHandedChange: (state, action) => {
        state.twoHanded = action.payload;
    },
  },
})

// Action creators are generated for each case reducer function
export const { handleWeaponLevelChange, handleLevelChange, handleTwoHandedChange, handleAllWeaponLevelChange } = allLevelsSlice.actions

export default allLevelsSlice.reducer