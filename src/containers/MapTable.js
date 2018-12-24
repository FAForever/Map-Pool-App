import React, { Component } from 'react';
import Map from '../components/Map';
import MapHeader from '../components/MapHeader';
import '../App.css';

class PoolTable extends Component {
  constructor(props) {
    super(props);
    this.groupingHeader = this.groupingHeader.bind(this);
    this.mapReturn = this.mapReturn.bind(this);
  }
  componentDidMount() {
    this.props.updater();
  }

  groupingHeader(map) {
    return (<MapHeader
      key={map.id}
      id={map.id}
      name={map.name}
      size={map.size}
      category={map.category}
      score={map.Tscore}
    />);
  }

  mapReturn(map) {
    return (<Map
      key={map.id}
      id={map.id}
      name={map.name}
      size={map.size}
      category={map.category}
      score={map.Tscore}
    />);
  }

  populateTable() {
    switch(this.props.grouping) {
      case "none":
      default:
        return this.props.maps.map(map => this.mapReturn(map));

      case "size":
        const x5 = this.props.maps.filter(map => {
          return map.size === "5x5"
        });
        const x10 = this.props.maps.filter(map => {
          return map.size === "10x10"
        });
        const x20 = this.props.maps.filter(map => {
          return map.size === "20x20" || map.size === "40x40"
        });

        const mapsBySize = x5.concat(x10, x20);
        return mapsBySize.map(map => this.mapReturn(map));

      case "category":
        const new_ = this.props.maps.filter(map => {
          return map.category === "new"
        });
        const exp = this.props.maps.filter(map => {
          return map.category === "experimental"
        });
        const com = this.props.maps.filter(map => {
          return map.category === "common"
        });
        const cls = this.props.maps.filter(map => {
          return map.category === "classic"
        });
        const mapsByCat = new_.concat(exp, com, cls);
        return mapsByCat.map(map => this.mapReturn(map));
    }
  }

  render() {
    return (
      <div className="Table-wrapper">
        <table className="Map-table">
          <thead>
            <tr>
              <th className="Map-table-num">#</th>
              <th className="Map-table-name">Name</th>
              <th className="Map-table-size">Size</th>
              <th className="Map-table-cat">Category</th>
              <th className="Map-table-score">Total Score</th>
            </tr>
          </thead>
          <tbody>
            {this.populateTable()}
          </tbody>
        </table>
      </div>
    );
  }
}

export default PoolTable;
