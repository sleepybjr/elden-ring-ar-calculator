import UserBuild from "../userBuild/UserBuild";// eslint-disable-line no-unused-vars

import { Link } from "react-router-dom";

export default function Home() {

    return (
        <div className='extra-spacing'>
            <br />
            <br />
            Check out the header above to get to the weapon AR calculator.
            <br />
            <br />
            There is also a new armor optimizer calculator.
            <br />
            <br />
            <Link to="/elden-ring-ar-calculator">Click here</Link> to get to the weapon AR calculator.
            <br />
            <br />
            <Link to="/armor-optimizer">Click here</Link> to get to the armor optimizer.
            <br />
            <br />
            <br/>
            <br/>

            {/* <UserBuild/> */}
        </div>
    );
}