import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import EnergyJournal from "./EnergyJournal";
import NewEnergyModal from "./NewEnergyModal";

import axios from "axios";

import { API_URL } from "../constants";

class Battery extends Component {
  state = {
    energies: []
  };

  componentDidMount() {
    this.resetState();
  }

  getEnergies = () => {
    axios.get(API_URL).then(res => this.setState({ energies: res.data }));
  };

  resetState = () => {
    this.getEnergies();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <EnergyJournal
              energies={this.state.energies}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <NewEnergyModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Battery;
