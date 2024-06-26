import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";

import axios from "axios";

import { API_URL } from "../constants";

class NewEnergyForm extends React.Component {
  state = {
    pk: 0,
    wellbeing: "",
    mental_stress: "",
    physical_stress: "",
    date_added: "",
  };

  componentDidMount() {
    if (this.props.energy) {
      const { pk, wellbeing, mental_stress, physical_stress } =
        this.props.energy;
      this.setState({ pk, wellbeing, mental_stress, physical_stress });
    }
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createEnergy = (e) => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editEnergy = (e) => {
    e.preventDefault();
    axios.put(API_URL + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = (value) => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form
        onSubmit={this.props.energy ? this.editEnergy : this.createEnergy}
      >
        {" "}
        <FormGroup>
          <Label for="wellbeing">Wellbeing (1-10):</Label>
          <div className="text-center">{this.state.wellbeing}</div>
          <input
            type="number"
            name="wellbeing"
            id="wellbeing"
            min="1"
            max="10"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.wellbeing)}
            className="custom-slider"
          />
        </FormGroup>
        <FormGroup>
          <Label for="mental_stress">Mental Stress (1-10):</Label>
          <div className="text-center">{this.state.mental_stress}</div>
          <input
            type="number"
            name="mental_stress"
            id="mental_stress"
            min="1"
            max="10"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.mental_stress)}
            className="custom-slider"
          />
        </FormGroup>
        <FormGroup>
          <Label for="physical_stress">Physical Stress (1-10):</Label>
          <div className="text-center">{this.state.physical_stress}</div>
          <input
            type="number"
            name="physical_stress"
            id="physical_stress"
            min="1"
            max="10"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.physical_stress)}
            className="custom-slider"
          />
        </FormGroup>
        <Button type="submit">Save</Button>
      </Form>
    );
  }
}
export default NewEnergyForm;
