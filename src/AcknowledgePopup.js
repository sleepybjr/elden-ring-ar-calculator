import React, { Component } from 'react';
import Popup from 'reactjs-popup';

export default class AcknowledgePopup extends Component {
    render() {
        return (
            <div>
                <Popup
                    trigger={<button className={`all-button-style ${ this.props.styleName }`}> {this.props.buttonName} </button>}
                    modal
                >
                    {close => (
                        <div className="modal">
                            <button className="close" onClick={close}>
                                &times;
                            </button>
                            <div className="content center-content">
                                {' '}
                                {this.props.content}
                            </div>
                            <div className="actions">
                                <button
                                    className="button middle-spacing"
                                    onClick={() => {
                                        this.props.handleYesClick();
                                        close();
                                    }}
                                >
                                    Yes
                                </button>
                                <button
                                    className="button middle-spacing"
                                    onClick={() => {
                                        close();
                                    }}
                                >
                                    No
                                </button>
                            </div>
                        </div>
                    )}
                </Popup>
            </div>
        )
    };
}