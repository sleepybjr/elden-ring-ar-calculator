import { configureStore } from '@reduxjs/toolkit';
import allLevelsReducer from '../levels/allLevelsSlice';

export default configureStore({
  reducer: {
    allLevels: allLevelsReducer,
  },
});