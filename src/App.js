import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// make multiselect boxes better and intuitive (such as adding select all and deselect all and using checkboxes?)
// slow if all weapons are loaded
// add somber and smithing checkbox filter
// add hide unable to use weapon filter
// add +10 or +25 to weapons to show level? or show if somber vs smithing type weapon
// add fextralife link to weapon name? or on hover?

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
            <div>Elden Ring Data: v1.03.3</div>
        </div>
    );
}

export default App;
