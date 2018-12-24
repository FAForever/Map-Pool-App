import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';
import MapTable from './MapTable';
import ErrorContainer from '../components/ErrorContainer';
import Customization from './Customization';
import { Context } from '../App';
import '../App.css';

class Body extends Component {
  constructor(props) {
    super(props);
    this.state = {
      maps: [],
      extraInfo: {
        "Average rating": 0,
        "5x5 count": 0,
        "10x10 count": 0,
        "20x20 count": 0,
        "New count": 0,
        "Exp count": 0,
        "Common count": 0,
        "Classic count": 0,
      },
      errorResponse: undefined,
      poolGrouping: localStorage.getItem("Pool-grouping") || "none"
    };
    this.fetchPool = this.fetchPool.bind(this);
    this.fetchMapList = this.fetchMapList.bind(this);
    this.setGroupingState = this.setGroupingState.bind(this);
  }

fetchPool() {
  let params = {
    brokenIgnore: localStorage.getItem("Broken-ignore"),
    catControl: localStorage.getItem("Cat-control"),
    clsPercent: localStorage.getItem("Cls-percent-input"),
    comPercent: localStorage.getItem("Com-percent-input"),
    expPercent: localStorage.getItem("Exp-percent-input"),
    minRating: localStorage.getItem("Min-rating-input"),
    newPercent: localStorage.getItem("New-percent-input"),
    poolSize: localStorage.getItem("Pool-size-input"),
    randomType: localStorage.getItem("Random-type"),
    sizeControl: localStorage.getItem("Size-control"),
    spreadType: localStorage.getItem("Spread-type"),
    x10percent: localStorage.getItem("x10-percent-input"),
    x20percent: localStorage.getItem("x20-percent-input"),
    x5percent: localStorage.getItem("x5-percent-input")
  }
  let queryString = "?";
  if (params != null) {
    Object.entries(params).forEach(param => {
      if (param[1] !== "" && param[1] !== null) {
        queryString += `${param[0]}=${param[1]}&`
      }
    });
    queryString = queryString.slice(0, -1);
    axios.get(`https://fluffypoolapp.herokuapp.com/api/map_pool/${queryString}`)
    .then(response => {
      if (response.data.error_response) {
        this.setState({errorResponse: response.data.error_response});
      }
      else {
        this.setState({
          maps: response.data.pool,
          extraInfo: response.data.extra_info,
          errorResponse: undefined
        });
      }
    });
  }
}

setGroupingState() {
  this.setState({poolGrouping: localStorage.getItem('Pool-grouping')});
}

fetchMapList(query) {
  if (query != null) {
    axios.get('https://fluffypoolapp.herokuapp.com/api/maps/' + query)
    .then(response => {
      this.setState({
        maps: response.data
      });
    });
  }
  else {
    axios.get('https://fluffypoolapp.herokuapp.com/api/maps/')
    .then(response => {
      this.setState({
        maps: response.data
      });
    });
  }
}

  render() {
    const { maps, poolGrouping, extraInfo, errorResponse } = this.state;
    return (
      <Context.Consumer>
        {context => (
          <>
          <div className="Body-container" role="main">
          <Customization updaterPool={this.fetchPool} updaterList={this.fetchMapList}
          groupingUpdater={this.setGroupingState}extraInfo={extraInfo}/>
            <Router>
              <Switch>
                    <Route exact path={context.paths.pool} render={(props) =>
                      errorResponse ?
                      <ErrorContainer {...props} error={errorResponse}/>
                      :
                      <MapTable {...props} maps={maps} updater={this.fetchPool} context={context} grouping={poolGrouping}/>}/>
                    <Route exact path={context.paths.maplist} render={(props) =>
                      <MapTable {...props} maps={maps} updater={this.fetchMapList}/>}/>
              </Switch>
            </Router>
          </div>
          </>)}
      </Context.Consumer>
    );
  }
}

export default Body;
