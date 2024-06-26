import React, { Component } from "react";

class Header extends Component {
  render() {
    return (
      <div className="text-center">
        <img
          src="/battery.svg"
          width="300"
          className="img-thumbnail"
          alt="Body battery"
          style={{ marginTop: "20px" }}
        />
        <hr />
        <h1>Body Battery</h1>
      </div>
    );
  }
}

export default Header;
