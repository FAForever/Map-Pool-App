import React, { Component } from 'react';
import { CookiesProvider } from 'react-cookie';
import PathContextWrapper from './components/PathContextWrapper';
import Body from './containers/Body';
import './App.css';

const Context = React.createContext();

class App extends Component {
  state = {
    context: {
      paths: {
        pool: "/",
        maplist: "/maplist"
      }
    }
  };

  render() {
    return (
      <CookiesProvider>
        <Context.Provider value={this.state.context}>
          <div className="App">
            <PathContextWrapper/>
            <Body/>
          </div>
        </Context.Provider>
      </CookiesProvider>
    );
  }
}

export default App;
export { Context };

// TODO add grouping headers for better UX
// TODO clear values of customization on reset/save
// TODO make ids change on sort to keep order?
// TODO add current pool page?
// TODO fancy preview pics?