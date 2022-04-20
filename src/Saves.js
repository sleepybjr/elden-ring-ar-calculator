import React, { Component } from 'react';
import Collapsible from 'react-collapsible';
import Popup from 'reactjs-popup';
import AcknowledgePopup from './AcknowledgePopup';
import { FiTrash2, FiSave } from "react-icons/fi";
import { RiShareForward2Fill } from "react-icons/ri";
import { CgSoftwareUpload } from "react-icons/cg";

const saveName = "saves";

export default class Saves extends Component {
    constructor(props) {
        super(props);
        this.state = {
            savedName: '',
            saves: new Set(),
            loadedSave: '',
            queryString: '',
            error: '',
        };
    }

    componentDidMount() {
        if (window.localStorage.getItem(saveName) !== null) {
            const loadedJSON = JSON.parse(window.localStorage.getItem(saveName));
            const loadedSaves = new Set(loadedJSON);
            this.setState({ saves: loadedSaves });
        }
    }

    // load in the first saved build but there is no ordering?

    handleSaveNameChange = (event) => {
        this.setState({ savedName: event.target.value });
    };

    handleOverwriteSave = (value) => (event) => {
        // needs warning for overwrite
        localStorage.setItem(value, JSON.stringify(this.props));
    };

    handleNewSave = (event) => {
        const trimmedSavedName = this.state.savedName.trim();
        if (this.state.saves.has(trimmedSavedName)) {
            this.setState({ error: "Name already exists." });
            return;
        }
        if (trimmedSavedName.length === 0) {
            this.setState({ error: "You must input a name." });
            return;
        }
        localStorage.setItem(trimmedSavedName, JSON.stringify(this.props));
        const newSaves = new Set(this.state.saves).add(trimmedSavedName);
        localStorage.setItem(saveName, JSON.stringify([...newSaves]));
        this.setState({ saves: newSaves, error: '' });
    };

    handleDeleteSave = (value) => (event) => {
        localStorage.removeItem(value);
        let newSaves = new Set(this.state.saves);
        newSaves.delete(value);
        localStorage.setItem(saveName, JSON.stringify([...newSaves]));
        this.setState({ saves: newSaves });
    };

    handleLoadSave = (value) => (event) => {
        // need to load all the values into the 
        const save = JSON.parse(window.localStorage.getItem(value));
        this.props.handleLoadSave(save);
        this.setState({ loadedSave: value });
    };

    handleShareSave = (value) => (event) => {
        const save = JSON.parse(window.localStorage.getItem(value));
        const data = {
            str: save.levels.strength,
            dex: save.levels.dexterity,
            int: save.levels.intelligence,
            fai: save.levels.faith,
            arc: save.levels.arcane,
            vig: save.levels.vigor,
            min: save.levels.mind,
            end: save.levels.endurance,
            somber: save.weaponLevels.somber,
            smith: save.weaponLevels.smithing,
            twoHanded: save.twoHanded,
        };

        const searchParams = new URLSearchParams(data);
        const URL = window.location.protocol + '//' + window.location.host + window.location.pathname;
        const URLWithParams = URL + "?" + searchParams.toString();

        if (navigator.clipboard) {
            navigator.clipboard.writeText(URLWithParams);
            this.setState({ queryString: "Copied!" });
        } else {
            // only if not in https, display the URL
            this.setState({ queryString: <a href={URLWithParams}>{URLWithParams}</a> });
        }
    };

    render() {
        return (
            <div className="build-collapsible">
                <Collapsible
                    trigger="Saved Builds"
                >
                    <div className="underline">
                        <div className='rowC small-spacing'>
                            <input type="text" id="saved-name" name="saved-name" maxLength="15" placeholder='Input save name...' value={this.state.savedName} onChange={this.handleSaveNameChange} />
                            <button className="all-button-style all-button-style-bg middle-spacing" onClick={this.handleNewSave}>Save</button>
                        </div>
                        <div className='error'>
                            {this.state.error}
                        </div>
                    </div>
                    <table>
                        <tbody className="remove-border no-padding">
                            {[...this.state.saves].map((val, key) => {
                                return (
                                    <tr key={key} className={val === this.state.loadedSave ? "highlight-load" : "" }>
                                        <td className="name">{val}</td>
                                        <td className="button">
                                            <AcknowledgePopup
                                                styleName="all-button-style-bg-red all-button-style-icon"
                                                buttonName={<FiTrash2 title="Delete" />}
                                                handleYesClick={this.handleDeleteSave(val)}
                                                content={<div>
                                                    Are you sure you want to delete <strong>{val}</strong>?
                                                </div>}
                                            />
                                        </td>
                                        <td className="button">
                                            <AcknowledgePopup
                                                styleName="all-button-style-bg all-button-style-icon"
                                                buttonName={<FiSave title="Overwrite" />}
                                                handleYesClick={this.handleOverwriteSave(val)}
                                                content={<div>
                                                    Are you sure you want to overwrite <strong>{val}</strong> with your current input?
                                                </div>}
                                            />
                                        </td>
                                        <td className="button"><button className="all-button-style all-button-style-bg all-button-style-icon" onClick={this.handleLoadSave(val)}>{<CgSoftwareUpload title="Load" />}</button></td>
                                        <td className="button">
                                            <Popup
                                                trigger={<button className="all-button-style all-button-style-bg all-button-style-icon">{<RiShareForward2Fill title="Share" />}</button>
                                                }
                                                position="center center"
                                                closeOnDocumentClick
                                                onOpen={this.handleShareSave(val)}
                                            >
                                                <div>
                                                    <span>{this.state.queryString}</span>
                                                </div>
                                            </Popup>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </Collapsible>
            </div>
        );
    }
}