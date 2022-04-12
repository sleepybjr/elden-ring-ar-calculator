import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';

// TODO: add better styling
// make multiselect boxes better and intuitive for multiselect
// slow if all weapons are loaded
// if no input for a field, get warning: Received NaN for the `children` attribute. If this is expected, cast the value to a string.
// add search field

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
            <div>Elden Ring Data: v1.03.3</div>
        </div>
    );
}

export default App;
