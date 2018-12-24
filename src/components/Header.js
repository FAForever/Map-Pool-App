import React, { Component } from 'react';
import { Context } from '../App';
import '../App.css';
import GitHub from '../img/GitHub.png';


class Header extends Component {
  constructor(props) {
    super(props);
    this.Pool = React.createRef();
    this.List = React.createRef();
  }

  componentDidMount() {
    const url = window.location.href
    if (url.includes(this.props.context.paths.maplist)) {
      this.List.current.className += " Header-link-active";
    }
    else {
      this.Pool.current.className += " Header-link-active";
    }
  }

  render() {
    return (
      <Context.Consumer>
        {context =>
          <header className="App-header">
            <nav className="Main-nav" role="navigation">
              <ul>
                <li>
                  <a href={context.paths.pool} className="Header-link" ref={this.Pool}>Build Pool</a>
                </li>
                <li>
                  <a href={context.paths.maplist} className="Header-link" ref={this.List}>Map List</a>
                </li>
                <li>
                  <a href="https://voting.faforever.com/vote" rel="external" className="Header-link">Vote on Maps</a>
                </li>
                <li>
                  <a href="https://github.com/Petricpwnz/Map-Pool-App" rel="external" className="Header-link">
                    <img src={ GitHub } alt="GitHub" height="50" width="50"/>
                  </a>
                </li>
              </ul>
            </nav>
          </header>
        }
      </Context.Consumer>
    );
  }
}

export default Header;
