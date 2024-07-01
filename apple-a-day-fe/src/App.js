import React, { Component, Fragment } from "react";
import Header from "./components/Header";
import Battery from "./components/Battery";
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="bg-dark text-light">
      <Fragment>
        <Header />
        <Battery />
      </Fragment>
      </div>
    );
  }
}

export default App;
