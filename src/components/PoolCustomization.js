import React, { Component } from 'react';
import FormMessage from './FormMessage';
import RerollButton from './RerollButton';
import '../App.css';

const descriptions = {
  sizeControl: "Whether to use specified proportions of map sizes.",
  catControl: "Whether to use specified proportions of map categories.",
  spreadType: "Evenly spread categories over sizes. If this is off pool for example\
  could end up with 6 experimental maps for 5x5 and none for 10x10 and 20x20.\
  Due to limited amount of maps this introduces a factor of pseudo-random and increases\
  the chance of lower rated maps being picked but its still recommended to leave it on and\
  tweak threshold and random type instead.",
  brokenIgnore: "Whether to ignore broken maps when building a pool.",
  randomType: "How algorithm will weigh maps. Stronger curve means maps with higher rating\
  have more chance to be picked. However due to limited amount of maps lower rated ones will\
  still get in, especially with 'Evenly spread categories over sizes' on.",
  poolSize: "Size of the pool. Has to be above 0.",
  minRating: "Any maps below this rating will be cut off. Has to be between 0 and 5.",
  x5percent: "Percentage of 5x5 maps in the pool. Sum of percents has to be 100.",
  x10percent: "Percentage of 10x10 maps in the pool. Sum of percents has to be 100.",
  x20percent: "Percentage of 20x20 maps in the pool. Sum of percents has to be 100.",
  newPercent: "Percentage of new maps in the pool. Sum of percents has to be 100.",
  expPercent: "Percentage of experimental maps in the pool. Sum of percents has to be 100.",
  comPercent: "Percentage of common maps in the pool. Sum of percents has to be 100.",
  clsPercent: "Percentage of classic maps in the pool. Sum of percents has to be 100."
}

class MapListCustomization extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showFormMessage: false,
      formMessage: "Saved successfully!",
      sizeCheckbox: this.getCheckedValue(localStorage.getItem("Size-control")),
      catCheckbox: this.getCheckedValue(localStorage.getItem("Cat-control")),
      spreadCheckbox: this.getCheckedValue(localStorage.getItem("Spread-type")),
      brokenCheckbox: this.getCheckedValue(localStorage.getItem("Broken-ignore")),
      currentConfig: {
        brokenIgnore: localStorage.getItem("Broken-ignore") || "on",
        catControl: localStorage.getItem("Cat-control") || "on",
        clsPercent: localStorage.getItem("Cls-percent-input") || 40,
        comPercent: localStorage.getItem("Com-percent-input") || 33,
        expPercent: localStorage.getItem("Exp-percent-input") || 13,
        minRating: localStorage.getItem("Min-rating-input") || 2.0,
        newPercent: localStorage.getItem("New-percent-input") || 14,
        poolSize: localStorage.getItem("Pool-size-input") || 30,
        randomType: localStorage.getItem("Random-type") || 3,
        sizeControl: localStorage.getItem("Size-control") || "on",
        spreadType: localStorage.getItem("Spread-type") || "on",
        x10percent: localStorage.getItem("x10-percent-input") || 55,
        x20percent: localStorage.getItem("x20-percent-input") || 20,
        x5percent: localStorage.getItem("x5-percent-input") || 25,
        poolGrouping: localStorage.getItem("Pool-grouping") || "none"
      }
    };
    this.resetToDefault = this.resetToDefault.bind(this);
    this.saveConfig = this.saveConfig.bind(this);
    this.closeFormMessage = this.closeFormMessage.bind(this);
  }

  handleFormMessage(message) {
    this.setState({formMessage: message,
                   showFormMessage: true});
  }
  // Triggers on shitty button press, couldnt figure out a way to use timer without aids since setState is async
  closeFormMessage() {
    this.setState({showFormMessage: false});
  }

  // lol fuck reacts defaultchecked
  getCheckedValue(checkboxData) {
    return (checkboxData == 'true' || checkboxData == undefined) ? true:false;
  }

  saveConfig(event) {
    event.preventDefault();
    for (let i = event.target.length - 3; i >= 0; i--) {  // -3 to skip the button values
      if (event.target[i].value || event.target[i].type == "checkbox") {
        localStorage.setItem(event.target[i].name, event.target[i].value);
      }
    }
    this.handleFormMessage("Saved successfully!");

  }

  handleCheckbox = event => {
    let convertToBool = (event.target.value == "false");
    this.setState({[event.target.id]: convertToBool});
  }

  resetToDefault(event) {
    localStorage.clear();
    this.handleFormMessage("Reset successfully!");
  }

  groupMaps = event => {
    switch (event.target.value) {
      case "none":
      default:
        localStorage.setItem("Pool-grouping", "none");
        this.props.groupingUpdater();
        break;
      case "size":
        localStorage.setItem("Pool-grouping", "size");
        this.props.groupingUpdater();
        break;
      case "category":
        localStorage.setItem("Pool-grouping", "category");
        this.props.groupingUpdater();
        break;
    }
  }

  render() {
    let { poolGrouping, clsPercent, comPercent, expPercent, minRating,
          newPercent, poolSize, randomType, x10percent, x20percent, x5percent } = this.state.currentConfig;
    const { extraInfo } = this.props;
    return (
      <>
        <form className="Form" onSubmit={this.saveConfig} style={this.props.style}>
          <label htmlFor="sizeCheckbox">Specific size proportions</label>
          <input type="checkbox" className="Form__content checkbox" id="sizeCheckbox" name="Size-control" value={this.state.sizeCheckbox}
          onChange={this.handleCheckbox} defaultChecked={this.state.sizeCheckbox} title={descriptions.sizeControl}/>
          <label htmlFor="catCheckbox">Specific category proportions</label>
          <input type="checkbox" className="Form__content checkbox" id="catCheckbox" name="Cat-control" value={this.state.catCheckbox}
          onChange={this.handleCheckbox} defaultChecked={this.state.catCheckbox} title={descriptions.catControl}/>
          <label htmlFor="spreadCheckbox">Evenly spread categories over sizes</label>
          <input type="checkbox" className="Form__content checkbox" id="spreadCheckbox" name="Spread-type" value={this.state.spreadCheckbox}
          onChange={this.handleCheckbox} defaultChecked={this.state.spreadCheckbox} title={descriptions.spreadType}/>
          <label htmlFor="brokenCheckbox">Ignore broken maps</label>
          <input type="checkbox" className="Form__content checkbox" id="brokenCheckbox" name="Broken-ignore" value={this.state.brokenCheckbox}
          onChange={this.handleCheckbox} defaultChecked={this.state.brokenCheckbox} title={descriptions.brokenIgnore}/>
          <label htmlFor="Random-type">Type of random selection</label>
          <select className="Form__content" id="randType" name="Random-type" title={descriptions.randomType} defaultValue={randomType}>
            <option value="0">No weighing</option>
            <option value="1">Linear</option>
            <option value="2">Slight curve</option>
            <option value="3" >Optimal curve</option>
            <option value="4">Strong curve</option>
            <option value="5">Extreme curve</option>
            <option value="6">Take me to the moon</option>
          </select>
          <label htmlFor="Pool-size-input">Pool size</label>
          <input className="Form__content" step="1" type="number" name="Pool-size-input" placeholder={poolSize}
          id="Pool-size-input"title={descriptions.poolSize}/>
          <label htmlFor="Min-rating-input">Minimal rating</label>
          <input className="Form__content" step="0.1" type="number" name="Min-rating-input" placeholder={minRating}
          id="Min-rating-input" title={descriptions.minRating}/>
          <label htmlFor="x5-percent-input">Percent of 5x5 maps</label>
          <input className="Form__content" step="1" type="number" name="x5-percent-input" placeholder={x5percent}
          id="x5-percent-input" title={descriptions.x5percent}/>
          <label htmlFor="x10-percent-input">Percent of 10x10 maps</label>
          <input className="Form__content" step="1" type="number" name="x10-percent-input" placeholder={x10percent}
          id="x10-percent-input" title={descriptions.x10percent}/>
          <label htmlFor="x20-percent-input">Percent of 20x20 maps</label>
          <input className="Form__content" step="1" type="number" name="x20-percent-input" placeholder={x20percent}
          id="x20-percent-input" title={descriptions.x20percent}/>
          <label htmlFor="New-percent-input">Percent of new maps</label>
          <input className="Form__content" step="1" type="number" name="New-percent-input" placeholder={newPercent}
          id="New-percent-input" title={descriptions.newPercent}/>
          <label htmlFor="Exp-percent-input">Percent of experimental maps</label>
          <input className="Form__content" step="1" type="number" name="Exp-percent-input" placeholder={expPercent}
          id="Exp-percent-input" title={descriptions.expPercent}/>
          <label htmlFor="Com-percent-input">Percent of common maps</label>
          <input className="Form__content" step="1" type="number" name="Com-percent-input" placeholder={comPercent}
          id="Com-percent-input" title={descriptions.comPercent}/>
          <label htmlFor="Cls-percent-input">Percent of classic maps</label>
          <input className="Form__content" step="1" type="number" name="Cls-percent-input" placeholder={clsPercent}
          id="Cls-percent-input" title={descriptions.clsPercent}/>
          <input className="btn btn-submit" type="button" name="Reset-btn"value="Reset to default" onClick={this.resetToDefault}/>
          <input className="btn btn-submit" type="submit" name="Submit-btn" value="Save configuration"/>
        </form>
          {this.state.showFormMessage ? <FormMessage closeFormMessage={this.closeFormMessage} message={this.state.formMessage}/> : null}
        <RerollButton updater={this.props.updater} context={this.props.context}/>
        <form className="Form">
          <label htmlFor="Grouping">Group by:</label>
          <select name="Grouping" className="Form__content" defaultValue={poolGrouping} onChange={this.groupMaps}>
            <option value="none">No grouping</option>
            <option value="size">Size</option>
            <option value="category">Category</option>
          </select>
          <span>Average rating:</span>
          <span>{extraInfo["Average rating"]}</span>
          <span>5x5 count:</span>
          <span>{extraInfo["5x5 count"]}</span>
          <span>10x10 count:</span>
          <span>{extraInfo["10x10 count"]}</span>
          <span>20x20 count:</span>
          <span>{extraInfo["20x20 count"]}</span>
          <span>New count:</span>
          <span>{extraInfo["New count"]}</span>
          <span>Experimental count:</span>
          <span>{extraInfo["Exp count"]}</span>
          <span>Common count:</span>
          <span>{extraInfo["Common count"]}</span>
          <span>Classic count:</span>
          <span>{extraInfo["Classic count"]}</span>
        </form>
      </>
    );
  }
}

export default MapListCustomization;
