import React, { Component } from "react";
import { Table } from "reactstrap";
import NewEnergyModal from "./NewEnergyModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class EnergyJournal extends Component {
  render() {
    const energies = this.props.energies;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>Wellbeing</th>
            <th>mental Stress</th>
            <th>Physical Stress</th>
            <th>Date Added</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!energies || energies.length <= 0 ? (
            <tr>
              <td colSpan="5" align="center">
                <b>Oops, no one here yet</b>
              </td>
            </tr>
          ) : (
            energies.map(energy => (
              <tr key={energy.pk}>
                <td>{energy.wellbeing}</td>
                <td>{energy.mental_stress}</td>
                <td>{energy.physical_stress}</td>
                <td>{energy.date_added}</td>
                <td align="center">
                  <NewEnergyModal
                    create={false}
                    energy={energy}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={energy.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default EnergyJournal;
