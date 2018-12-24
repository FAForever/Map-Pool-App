import React, { Component } from 'react';
import '../App.css';

class FormMessage extends Component {
  render() {
    return (
      <div id="Form-message">
        {this.props.message}
        <button className="btn" type="button" onClick={this.props.closeFormMessage}>OK</button>
      </div>
    );
  }
}

export default FormMessage;
