import { configureStore } from '@reduxjs/toolkit';
import allLevelsReducer from '../levels/allLevelsSlice';
import userBuildSlice from '../weapons/userBuildSlice';

export default configureStore({
  reducer: {
    allLevels: allLevelsReducer,
    userBuild: userBuildSlice,
  },
});