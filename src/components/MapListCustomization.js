import React, { Component } from 'react';
import react_foxgirl from "../img/react_foxgirl.png";
import '../App.css';

class MapListCustomization extends Component {
  sort = event => {
    if (event.target.value === "Name") {
      this.props.updater("?ordering=name");
    }
    else if (event.target.value === "Size") {
      this.props.updater("?ordering=size");
    }
    else if (event.target.value === "Category") {
      this.props.updater("?ordering=-category");
    }
    else if (event.target.value === "Rating") {
      this.props.updater("?ordering=-Tscore");
    }
  }

  render() {
    return (
      <div className="Map-list-csm">
        <form className="Map-list-csm__form">
          <label htmlFor="Map-sort-input" className="Map-sort-input">Sort by:</label>
          <select className="Map-sort-input Form__content" id="Map-sort-input" onChange={this.sort}>
            <option value="Name">Name</option>
            <option value="Size">Size</option>
            <option value="Category">Category</option>
            <option value="Rating">Rating</option>
          </select>
        </form>
        <figure>
          <img src={react_foxgirl} alt="Cute foxgirl here" id="Foxgirl" width="380"/>
          <figcaption id="Foxgirl-caption">There isn't anything to put here so have a cute foxgirl.</figcaption>
        </figure>
      </div>
    );
  }
}

export default MapListCustomization;
