import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// add input validation
// make multiselect boxes better and intuitive (such as adding select all and deselect all and using checkboxes?)
// sort weapon names by actual weapon name and not full weapon name?
// add passives

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
        </div>
    );
}

export default App;
