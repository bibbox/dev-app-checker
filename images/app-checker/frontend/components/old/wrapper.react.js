import React            from 'react';
import ReactDOM         from 'react-dom';
import Store            from './old/store.react';
import Instances        from './old/instances.react';
import Instance         from './old/instance.react';
import Install          from './old/install.react';
import ActivityHistory  from './old/activity-history.react';


/**
 * Wrapping component for calling the different page components depending on url params
 */
var Wrapper = React.createClass({
    render: function() {
        let Component = Instances;
        
        switch(this.props.params.param1) {
            case 'store':       Component = Store;              break;
            case 'install':     Component = Install;            break;
            case 'instances':   Component = Instances;          break;
            case 'instance':    Component = Instance;           break;
            case 'activities':  Component = ActivityHistory;    break;
            default:            Component = Instances;
        }
        
        return (
            <div id="component-wrapper">
                <img id="loader" src={datastore + '/js/images/loading_dark.gif'} />
                <Component params={this.props.params} />
            </div>
        );
    }
});

/* Renders the application in the DOM */

ReactDOM.render(
  <Wrapper params={params} />,
  document.getElementById('bibbox-wrapper')
);