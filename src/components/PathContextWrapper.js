import React, { Component } from 'react';
import { Context } from '../App';
import Header from './Header';
import '../App.css';


class PathContextWrapper extends Component {
  render() {
    return (
      <Context.Consumer>
        {context =>
          <Header context={ context }/>
        }
      </Context.Consumer>
    );
  }
}

export default PathContextWrapper;
