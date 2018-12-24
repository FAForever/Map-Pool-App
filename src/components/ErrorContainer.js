import React, { Component } from 'react';
import '../App.css';

class ErrorContainer extends Component {
  render() {
    return (
      <div className="Error-container">
        <div>{this.props.error}</div>
      </div>
    );
  }
}

export default ErrorContainer;
