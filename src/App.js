import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// add input validation
// add debuff for insufficient required stats, add buff if eligible after two-handing
// make multiselect boxes better and intuitive (such as adding select all and deselect all and using checkboxes?)
// sort weapon names by actual weapon name and not full weapon name
// add ability to remove / add columns to table, scroll horizontal wheel for large column table?
// add passives
function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
        </div>
    );
}

export default App;
