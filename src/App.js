import './App.css';
import FilterableWeaponTable from './FilterableWeaponTable';
import ContentPopup from './ContentPopup';

// TODO: add better styling like dark mode
// make multiselect boxes better and intuitive for multiselect
// slow if all weapons are loaded, optimize our json
// if no input for a field, get warning: Received NaN for the `children` attribute. If this is expected, cast the value to a string.
// add rune gain and hp regain passive
// add throwables and fists?
// searching a weapon and then selecting the class will make it appear twice
// add tracking on sort to see if i can remove anything from table
// load last used settings
// make trashcan red

function App() {
    return (
        <div className="App">
            <FilterableWeaponTable />
            <div>Elden Ring Data: v1.03.3 | Calculator Version 1.2.0</div>
            <ContentPopup
                buttonName='Privacy Policy'
                content={
                    <div>We use the open source Plausible Analytics to count website visits and is used to
                        see if people are using the site.
                        No cookies are used and no personal data such as an IP address is stored. It complies with
                        cookie laws and privacy regulations such as GDPR, CCPA and PECR. If you have any concerns,
                        please use the feedback tools below to leave a message. Thanks!
                        <br />
                        <br />
                        For more information, see the <a href="https://plausible.io/data-policy" rel="noreferrer">Plausible Data Policy</a>.
                        <br />
                        <br />
                        Last updated: 4/15/2022</div>
                } />
            <div>For feedback, bug reports or suggestions, use <a href="https://forms.gle/krzihsr22n5VPmDNA">Google Forms</a> or <a href="https://github.com/sleepybjr/elden-ring-ar-calculator/issues">GitHub</a>. Thanks!</div>
        </div>
    );
}

export default App;
