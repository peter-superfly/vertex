import React, {useState} from 'react';
import {ErrorMessage, Field, Form, Formik} from 'formik';
import {GetAccount, UpdateAccount, UpdateUsername} from "../../../lib/sharedQueries";
import {useMutation, useQuery} from "@apollo/client";
import _ from 'lodash';

function Product({profile, client: apolloClient, ...props}) {
    const [new_password, setNewPassword] = useState("");

    return (
        <div>
            <Formik
                className={"account-form"}
                initialValues={new_password}
                validate={async values => {
                    console.log(values)
                    const errors = {};

                    if (values.username !== profile.username) {
                        let variables = {
                            "username": values.username
                        }

                        let {data, loading, error} = await apolloClient.query({
                            query: GetAccount, variables
                        });

                        if (data['accounts_by_pk']) {
                            errors.username = "Username already exists"
                        }
                    }

                    if (!values.email) {
                        errors.email = 'Required';
                    } else if (
                        !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                    ) {
                        errors.email = 'Invalid email address';
                    }
                    return errors;
                }}
                onSubmit={async (values, {setSubmitting}) => {

                    if (profile.username !== values.username) {
                        let vars = {
                            username : values.username,
                            uid: profile['uid']
                        }
                        await updateUsername({variables : vars})
                    }

                    delete values['username']
                    values['uid'] = profile['uid']
                    updateProfile({variables : values})
                }}
            >
                {({isSubmitting}) => (
                    <Form className={"account-form"}>

                        <label htmlFor="password">Current Password</label>
                        <Field type="password" name="current_password"/>
                        <ErrorMessage name="username" component="div"/>

                        <label htmlFor="password">New Password</label>
                        <Field type="password" name="new_password"/>
                        <ErrorMessage name="fullname" component="div"/>

                        <label htmlFor="password">Confirm Password</label>
                        <Field type="password" name="confirm_password"/>
                        <ErrorMessage name="title" component="div"/>

                        <button type="submit" disabled={isSubmitting}>
                            Submit
                        </button>
                    </Form>
                )}
            </Formik>

        </div>
    );
}

export default Product;

