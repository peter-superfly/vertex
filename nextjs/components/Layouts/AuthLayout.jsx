import React, { Fragment } from "react";

const AuthLayout = ({ children }) => {

    return (
        <Fragment>
            <div className={'pulsing-colors-bg'}>
                <div className="pulse-layer-1"></div>
                <div className="pulse-layer-2"></div>
                <div className="pulse-layer-3"></div>
                <div className="auth-screen-content">{children}</div>
            </div>
        </Fragment>
    );
};

export default AuthLayout;