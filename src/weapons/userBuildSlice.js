import { createSlice } from '@reduxjs/toolkit';

export const userBuildSlice = createSlice({
  name: 'userBuild',
  initialState: {
    weaponRight1: "",
    weaponRight2: "",
    weaponRight3: "",
    weaponLeft1: "",
    weaponLeft2: "",
    weaponLeft3: "",

  },
  reducers: {
    handleWeaponRight1Change: (state, action) => {
        state.weaponRight1 = action.payload;
    },
    handleWeaponRight2Change: (state, action) => {
        state.weaponRight2 = action.payload;
    },
    handleWeaponRight3Change: (state, action) => {
        state.weaponRight3 = action.payload;
    },
    handleWeaponLeft1Change: (state, action) => {
        state.weaponLeft1 = action.payload;
    },
    handleWeaponLeft2Change: (state, action) => {
        state.weaponLeft2 = action.payload;
    },
    handleWeaponLeft3Change: (state, action) => {
        state.weaponLeft3 = action.payload;
    },
  },
})

// Action creators are generated for each case reducer function
export const { 
    handleWeaponRight1Change, 
    handleWeaponRight2Change, 
    handleWeaponRight3Change, 
    handleWeaponLeft1Change,
    handleWeaponLeft2Change,
    handleWeaponLeft3Change,
} = userBuildSlice.actions;

export default userBuildSlice.reducer;