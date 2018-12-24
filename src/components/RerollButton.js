import React, { Component } from 'react';
import '../App.css';

class RerollButton extends Component {
  render() {
    return (
        <button type="button" onClick={this.props.updater} className="btn btn-reroll">Reroll</button>
    );
  }
}

export default RerollButton;
