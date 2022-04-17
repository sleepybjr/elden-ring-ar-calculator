import React, { Component } from 'react';
import Popup from 'reactjs-popup';

export default class ContentPopup extends Component {
    render() {
        return (
            <div>
                <Popup
                    trigger={<button className="all-button-style"> {this.props.buttonName} </button>}
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
                                {this.props.content}
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