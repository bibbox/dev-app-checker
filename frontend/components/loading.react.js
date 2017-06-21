import React            from 'react';


export default class Loading extends React.Component {
    render() {
        return (
            <div id="component-loading">
                <span id="loading-head">Scanning...</span>
                <span id="loading-sub">This might take a while</span>
            </div>
        );
    }
}