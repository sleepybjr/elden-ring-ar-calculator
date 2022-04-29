import './App.css';
import "./css/fontawesome-free-6.1.1-web/css/all.min.css";

import React from 'react';
import ContentPopup from './component/ContentPopup';
import DarkModeToggle from './component/DarkModeToggle';
import { Link, Outlet } from "react-router-dom";
import InputStats from './levels/InputStats';

// TODO: add better/modern styling
// make multiselect boxes better and intuitive for multiselect
// slow if all weapons are loaded, optimize our json
// if no input for a field, get warning: Received NaN for the `children` attribute. If this is expected, cast the value to a string.
// add rune gain and hp regain passive
// add throwables and fists?
// searching a weapon and then selecting the class will make it appear twice
// add tracking on sort to see if i can remove anything from table
// load last used settings
// refactor to use react hooks / functional components rather than class components
// blue highlight in selects (class and weapon / affinity filter) are browser specific and i cant change the color

// save table state across routes
// remove selection from build
// react-window use for table, should i switch to react table?

function App() {
    return (
        <div className="App">
            <Link to="/">Home</Link> |{" "}
            <Link to="/elden-ring-ar-calculator">Weapons</Link> |{" "}
            <Link to="/armor-optimizer">Armor Optimizer</Link>
            <InputStats />
            <Outlet />
            <div className='extra-spacing'>
                <div>Elden Ring Version: v1.04.0 | Calculator Version 1.4.0</div>
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
                <div className='small-spacing'>
                    Dark Mode
                    <DarkModeToggle />
                </div>
            </div>
        </div>
    );
}

export default App;
