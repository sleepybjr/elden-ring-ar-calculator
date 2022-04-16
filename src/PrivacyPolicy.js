import React, { Component } from 'react';
import Popup from 'reactjs-popup';

export default class PrivacyPolicy extends Component {
    render() {
        return (
            <div>
                <Popup
                trigger={<button className="all-button-style"> Privacy Policy </button>}
                modal
                nested
            >
                {close => (
                    <div className="modal">
                        <button className="close" onClick={close}>
                            &times;
                        </button>
                        <div className="header"> Privacy Policy </div>
                        <div className="content">
                            {' '}
                            We use the open source Plausible Analytics to count website visits and is used to 
                            see if people are using the site. 
                            No cookies are used and no personal data such as an IP address is stored. It complies with 
                            cookie laws and privacy regulations such as GDPR, CCPA and PECR. If you have any concerns, 
                            please use the feedback tools below to leave a message. Thanks! 
                            <br/>
                            <br/>
                            For more information, see the <a href="https://plausible.io/data-policy" rel="noreferrer">Plausible Data Policy</a>.
                            <br/>
                            <br/>
                            Last updated: 4/15/2022
                        </div>
                        <div className="actions">
                            <button
                                className="button"
                                onClick={() => {
                                    close();
                                }}
                            >
                                Close Window
                            </button>
                        </div>
                    </div>
                )}
            </Popup>
            </div>
        )
    };
}