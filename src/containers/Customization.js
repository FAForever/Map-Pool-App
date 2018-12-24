import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PoolCustomization from '../components/PoolCustomization';
import MapListCustomization from '../components/MapListCustomization';
import { Context } from '../App';
import menu_icon from '../img/menu_icon.png';
import '../App.css';

class Customization extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showMenu: true,
      width: undefined
    };
    this.customization = React.createRef();
    this.handleSidebarToggle = this.handleSidebarToggle.bind(this);
  }

  handleSidebarToggle(event) {
    this.setState({showMenu: !this.state.showMenu});
  }

  handleResize = () => {
    if (window.innerWidth >= 700) {
      this.setState({showMenu: true});
    }
  }

  componentDidMount() {
    this.handleResize();
    window.addEventListener('resize', this.handleResize)
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize)
  }



  render() {
    return (
      <>
      <button className="Sidebar-toggle" type="button" onClick={this.handleSidebarToggle}>
        <img src={menu_icon} alt="Menu" width="50" height="50"/>
      </button>
      { this.state.showMenu ?
        <aside className="Cstm-sidebar">
          <div className="Sidebar-wrapper">
            <Router>
              <Switch>
                <Context.Consumer>
                  {context =>
                    <>
                    <Route exact path={ context.paths.pool } render={(props) => <PoolCustomization {...props} updater={this.props.updaterPool}
                    ref={this.customization} context={context} groupingUpdater={this.props.groupingUpdater} extraInfo={this.props.extraInfo} />}/>
                    <Route exact path={ context.paths.maplist } render={(props) => <MapListCustomization {...props} updater={this.props.updaterList}
                    ref={this.customization} />}/>
                    </>
                  }
                </Context.Consumer>
              </Switch>
            </Router>
          </div>
        </aside> : null
      }
      </>
    );
  }
}

export default Customization;
