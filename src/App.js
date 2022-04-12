import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// make multiselect boxes better and intuitive (such as adding select all and deselect all and using checkboxes?)
// slow if all weapons are loaded
// add +10 or +25 to weapons to show level? or show if somber vs smithing type weapon
// if no input for a field, get warning: Received NaN for the `children` attribute. If this is expected, cast the value to a string.

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
            <div>Elden Ring Data: v1.03.3</div>
        </div>
    );
}

export default App;
