import React, { Component } from 'react';
import '../App.css';

class Map extends Component {
  render() {
    const { id, name, size, category, score } = this.props;
    return (
      <tr>
        <td>{id}</td>
        <td>{name}</td>
        <td>{size}</td>
        <td>{category}</td>
        <td>{score}</td>
      </tr>
    );
  }
}

export default Map;
