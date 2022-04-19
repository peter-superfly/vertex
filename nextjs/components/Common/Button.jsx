import React, { Component } from "react";

import { string, bool } from "prop-types";
import styled from "styled-components";

const ButtonStyled = styled.button`
  width: 100%;
  border-radius: 1px;
  padding: 0 1rem;
  height: 40px;
`;
class ButtonComponent extends Component {
  render() {
    const { showSpinner, disabled, buttonText, icon, design, ...rest } =
      this.props;
    return (
      <ButtonStyled
        disabled={disabled}
        color={rest.color}
        className={`btn-shadow btn-multiple-state ${design} ${
          showSpinner ? "show-spinner" : ""
        }`}
        {...rest}
      >
        <span className="spinner d-inline-block">
          <span className="bounce1" />
          <span className="bounce2" />
          <span className="bounce3" />
        </span>
        {icon ? <i className={`${icon} pr-2`} /> : ""}
        <span className="label">{buttonText}</span>
      </ButtonStyled>
    );
  }
}
ButtonComponent.defaultProps = {
  color: "primary",
  showSpinner: false,
};

ButtonComponent.propTypes = {
  buttonText: string.isRequired,
  showSpinner: bool.isRequired,
  color: string,
};

export default ButtonComponent;
