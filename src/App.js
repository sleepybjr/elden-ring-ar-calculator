import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// make multiselect boxes better and intuitive (such as adding select all and deselect all and using checkboxes?)
// add passives

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
            <div>Elden Ring Data: v1.03.3</div>
        </div>
    );
}

export default App;
