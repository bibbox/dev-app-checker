import React            from 'react';
import ReactDOM         from 'react-dom';

import Loading          from './loading.react';
import Overview         from './overview.react';


const URL = '';

class Root extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            view: 'loading',
            apps: [],
            statistics: {
                errors: 0,
                flawed: 0,
                flawless: 0,
                last_scanned: 0,
                missing_installers:0,
                new_installers: 0,
                old_installers: 0,
                total_apps: 0,
                warnings: 0
            }
        };
    }

    clear() {
        fetch(URL +'/clear')
            .then((response) => response.text())
            .then((message) => {alert(message)})
            .catch((error) => {
                alert("Could not call clear API");
                console.log(error);
            });
    }

    scan() {
        this.setState({ view: 'loading' });

        fetch(URL + '/scan')
            .then((response) => response.json())
            .then((json) => {
                console.log(json);
                this.getAll();
            })
            .catch((error) => {
                alert("Could not call scan API");
                console.log(error);
            });
    }

    getAll() {
        fetch(URL + '/get')
            .then((response) => response.json())
            .then((json) => {
                console.log(json);

                this.setState({
                    view: 'overview',
                    apps: json.apps,
                    statistics: {
                        errors: json.errors,
                        flawed: json.flawed,
                        flawless: json.flawless,
                        last_scanned: json.last_scanned,
                        missing_installers: json.missing_installers,
                        new_installers: json.new_installers,
                        old_installers: json.old_installers,
                        total_apps: json.total_apps,
                        warnings: json.warnings
                    }
                });
            })
            .catch((error) => {
                alert("Could not call scan API");
                console.log(error);
            });
    }

    getOne(app) {
        fetch(URL + '/get/' + app)
            .then((response) => response.json())
            .then((json) => {console.log(json)})
            .catch((error) => {
                alert("Could not call scan API");
                console.log(error);
            });
    }

    componentDidMount() {
        this.scan();
    }

    render() {
        let view;

        switch(this.state.view) {
            case 'loading':
                view = <Loading />;
                break;
            case 'overview':
                view = <Overview
                    statistics={this.state.statistics}
                    apps={this.state.apps} />;
                break;
            default:
                view = <Loading />;
        }

        return (
            <div id="component-root">
                <div id="header">
                    <span id="title">App Analyzer</span>

                    <button type="button" onClick={() => this.clear()}>Clear</button>
                    <button type="button" onClick={() => this.scan()}>Scan</button>
                    {/* <button type="button" onClick={() => this.getAll()}>Overview</button> */}
                    {/* <button type="button" onClick={() => this.getOne("app-openspecimen")}>Get Open Specimen</button> */}
                </div>

                {view}
            </div>
        );
    }
}


/* Renders the application in the DOM */
ReactDOM.render(<Root />, document.getElementById('root'));