import React            from 'react';

import Statistics       from './statistics.react';
import Apps             from './apps.react';


export default class Overview extends React.Component {
    render() {
        return (
            <div id="component-overview">
                <h1>Statistics</h1>
                <Statistics statistics={this.props.statistics} />

                <h1>Apps</h1>
                <Apps apps={this.props.apps} />
            </div>
        );
    }
}