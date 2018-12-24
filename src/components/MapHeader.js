import React, { Component } from 'react';
import '../App.css';

class MapHeader extends Component {
  render() {
    const { id, name, size, category, score } = this.props;
    return (
      <tr>
        <th className="Map-header-styled">{id}</th>
        <th className="Map-header-styled">{name}</th>
        <th className="Map-header-styled">{size}</th>
        <th className="Map-header-styled">{category}</th>
        <th className="Map-header-styled">{score}</th>
      </tr>
    );
  }
}

export default MapHeader;
