import React, { Component, Fragment } from "react";
import Header from "./components/Header";
import Battery from "./components/Battery";
import './App.css';

class App extends Component {
  render() {
    return (
      <Fragment>
        <Header />
        <Battery />
      </Fragment>
    );
  }
}

export default App;
