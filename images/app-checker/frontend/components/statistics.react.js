import React            from 'react';


export default class Overview extends React.Component {
    render() {
        return (
            <div id="component-statistics">
                <table>
                    <tbody>
                        <tr>
                            <td>Last scanned:</td>
                            <td>{this.props.statistics.last_scanned}</td>
                        </tr>
                        <tr>
                            <td>Total Apps:</td>
                            <td>{this.props.statistics.total_apps}</td>
                        </tr>
                        <tr>
                            <td>Flawless Apps:</td>
                            <td>{this.props.statistics.flawless}</td>
                        </tr>
                        <tr>
                            <td>Flawed Apps:</td>
                            <td>{this.props.statistics.flawed}</td>
                        </tr>
                        <tr>
                            <td>Flawed Apps:</td>
                            <td>{this.props.statistics.flawed}</td>
                        </tr>
                        <tr>
                            <td>New installers:</td>
                            <td>{this.props.statistics.new_installers}</td>
                        </tr>
                        <tr>
                            <td>Old installers:</td>
                            <td>{this.props.statistics.old_installers}</td>
                        </tr>
                        <tr>
                            <td>Missing installers:</td>
                            <td>{this.props.statistics.missing_installers}</td>
                        </tr>
                        <tr>
                            <td>Total warnings:</td>
                            <td>{this.props.statistics.warnings}</td>
                        </tr>
                        <tr>
                            <td>Total errors:</td>
                            <td>{this.props.statistics.errors}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}