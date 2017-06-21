import React            from 'react';


export default class Apps extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            visible: null
        };
    }

    toggleVisible(app) {
        if(this.state.visible === app) {
            this.setState({ visible: null });
        }
        else {
            this.setState({ visible: app });
        }
    }

    render() {
        if(this.props.apps.length > 0) {
            return (
                <div id="component-apps">
                    {
                        this.props.apps.map((app) => {
                            let visible = (app.name === this.state.visible) ? 'visible' : '';

                            return (
                                <div key={app.name} className={'apps-item ' + visible}>
                                    <div className="apps-head" onClick={() => this.toggleVisible(app.name)}>
                                        <h2>{app.name}</h2>
                                        <span className="apps-head-notices apps-head-warnings">{app.warnings.length}</span>
                                        <span className="apps-head-notices apps-head-errors">{app.errors.length}</span>
                                    </div>

                                    <div className="apps-body">
                                        <h4>Files</h4>
                                        <AppsFiles app={app}/>

                                        <h4>Warnings</h4>
                                        <AppsWarnings app={app}/>

                                        <h4>Errors</h4>
                                        <AppsErrors app={app}/>
                                    </div>
                                </div>
                            );
                        })
                    }
                </div>
            );
        }
        else {
            return ( <div>No apps have been found. Please try scanning first.</div> );
        }
    }
}


class AppsFiles extends React.Component {
    render() {
        return (
            <table>
                <thead>
                    <tr>
                        <th>File name</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                {
                    this.props.app.files.map((file) => {
                        return (
                            <tr key={file.name}>
                                <td>{file.name}</td>
                                <td>{file.status}</td>
                            </tr>
                        );
                    })
                }
                </tbody>
            </table>
        );
    }
}


class AppsWarnings extends React.Component {
    render() {
        if(this.props.app.warnings.length > 0) {
            return (
                <ul>
                    {
                        this.props.app.warnings.map((warning) => {
                            return (
                                <li key={this.props.app.name + warning}>{warning}</li>
                            );
                        })
                    }
                </ul>
            );
        }
        else {
            return ( <span className="notice">No warnings for this app.</span> );
        }
    }
}


class AppsErrors extends React.Component {
    render() {
        if(this.props.app.errors.length > 0) {
            return (
                <ul>
                    {
                        this.props.app.errors.map((error) => {
                            return (
                                <li key={this.props.app.name + error}>{error}</li>
                            );
                        })
                    }
                </ul>
            );
        }
        else {
            return ( <span className="notice">No errors for this app.</span> );
        }
    }
}