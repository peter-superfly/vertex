import React, { useState, Fragment } from "react";
import { Formik, Form, Field } from "formik";
import Link from "next/link";
import { useRouter } from "next/router";
import { setLS } from "../../lib/ls";
const axios = require("axios");
import AuthLayout from "../Layouts/AuthLayout";

export default () => {
    let [user, setUser] = useState({});
    let [loading, setLoading] = useState(false);
    let [error, setError] = useState(null);

    const router = useRouter();

    const loginUser = (values) => {
        if (!loading && values) {
            setLoading(true);
            setError(null);

            try {
                axios
                    .post("https://api.dropshop.cc/login/", values)
                    .then((response) => {
                        setLS("user", response.data);
                        setLoading(false);
                        router.push("/");
                    })
                    .catch((error) => {
                        if (error.response) {
                            console.error(error.response);
                            const { data } = error.response;
                            setError(data.error);
                            toaster.notify(data.error);
                        } else {
                            toaster.notify(error.message);
                            console.log(error.message);
                        }
                        setLoading(false);
                    });
            } catch (error) {
                setLoading(false);
                console.error(error);
            }
        }
    };

    const validateEmail = (value) => {
        setError(null);
        let error;
        if (!value) {
            error = "Please enter your email address";
        } else if (value.length < 4) {
            error = "Invalid value";
        }
        return error;
    };

    const validatePassword = (value) => {
        setError(null);
        let error;
        if (!value) {
            error = "Please enter your password";
        } else if (value.length < 8) {
            error = "Password must have at least 8 characters";
        }
        return error;
    };

    return (
        <Fragment>
            <AuthLayout>
                <div className="auth-card">
                    <div className="card-content">
                        <Formik initialValues={user} onSubmit={loginUser}>
                            {({ setFieldValue, errors, touched, handleSubmit }) => (
                                <Form className="av-tooltip tooltip-label-bottom">
                                    <Field
                                        className="form-control input"
                                        name="user_id"
                                        validate={validateEmail}
                                    />
                                    {errors.email && touched.email && (
                                        <div className="invalid-feedback d-block">
                                            {errors.email}
                                        </div>
                                    )}
                                    <Field
                                        className="form-control input"
                                        type="password"
                                        name="password"
                                        validate={validatePassword}
                                    />
                                    {errors.password && touched.password && (
                                        <div className="invalid-feedback d-block">
                                            {errors.password}
                                        </div>
                                    )}
                                    <div className="d-flex flex-column justify-content-between align-items-center">
                                        {/*<Button*/}
                                        {/*    type="submit"*/}
                                        {/*    marginY={8}*/}
                                        {/*    width={"100%"}*/}
                                        {/*    marginRight={12}*/}
                                        {/*    iconAfter={ArrowRightIcon}*/}
                                        {/*    background="black"*/}
                                        {/*    onClick={() => {*/}
                                        {/*        loginUser();*/}
                                        {/*    }}*/}
                                        {/*>*/}
                                        {/*    Login*/}
                                        {/*</Button>*/}
                                        <Link href="/login" className="login-footer">
                                            <p>Login</p>
                                        </Link>
                                        <Link href="/register" className="login-footer">
                      <span className="userpages-navlink create-account-instead">
                        Create a new seller account
                      </span>
                                        </Link>

                                    </div>
                                </Form>
                            )}
                        </Formik>
                    </div>
                </div>
            </AuthLayout>
        </Fragment>
    );
};