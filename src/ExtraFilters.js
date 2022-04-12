import React, { Component } from 'react'

export default class ExtraFilters extends Component {
    constructor(props) {
        super(props);
        this.handleChangeExtraFilter = this.handleChangeExtraFilter.bind(this);
    }
    
    handleChangeExtraFilter = (event) => {
        this.props.handleExtraFilterChange(event.target.checked, event.target.id);
    };

    render() {
        return (
            <div>
                <div className="rowC small-spacing">
                    <label htmlFor="somber-weapons">Show Somber</label>
                    <input type="checkbox" id="somber-weapons" name="somber-weapons" defaultChecked={this.props.somberFilter} onChange={this.handleChangeExtraFilter} />
                    <label htmlFor="smithing-weapons">Show Smithing</label>
                    <input type="checkbox" id="smithing-weapons" name="smithing-weapons" defaultChecked={this.props.smithingFilter} onChange={this.handleChangeExtraFilter} />
                </div>
                <div className="small-spacing">
                    <label htmlFor="missing-req-weapons">Show Insufficient Req</label>
                    <input type="checkbox" id="missing-req-weapons" name="missing-req-weapons" defaultChecked={this.props.hideNoReqWeapons} onChange={this.handleChangeExtraFilter} />
                </div>
            </div>
        );
    }
}