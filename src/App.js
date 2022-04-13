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
            <div>Elden Ring Data: v1.03.3 | Calculator Version 1.0.1</div>
            <div>For feedback, bug reports or suggestions, use <a href="https://forms.gle/krzihsr22n5VPmDNA">Google Forms</a> or <a href="https://github.com/sleepybjr/elden-ring-ar-calculator/issues">GitHub</a>. Thanks!</div>
        </div>
    );
}

export default App;
