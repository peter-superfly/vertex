import React from 'react';
import {ErrorMessage, Field, Form, Formik} from 'formik';
import Link from 'next/link'
import {GetAccount, UpdateAccount, UpdateUsername} from "../../lib/sharedQueries";
import Password from "./tabs/password";
import {useMutation, useQuery} from "@apollo/client";
import _ from 'lodash';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import "react-tabs/style/react-tabs.css";
import Head from 'next/head'
import { useRouter } from "next/router";

import {
    IoSearchOutline
} from 'react-icons/io5';

import Select from 'react-select'
import {getLS} from "../../lib/ls";

const options = [
    { value: 'chocolate', label: 'Chocolate' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'vanilla', label: 'Vanilla' }
]

function MainLogo({}) {
    let logged_in_user = getLS('user')

    return (<div className={'main-logo'}>
        <Link  href={logged_in_user ? `/${logged_in_user['username']}` : "/"}>
            <img src="/logo.svg"/>
        </Link></div>)
}

function Product(props) {
    const {profile, client: apolloClient, themes, ...rest} = props;

    const [updateProfile] = useMutation(UpdateAccount);
    const [updateUsername] = useMutation(UpdateUsername);

    let theme_key = _.find(themes, ['id', profile['theme']])
    if (theme_key) {
        theme_key = theme_key['key']
    }

    return (

        <div className={"layout-parent jura " + `${theme_key}`}>
            <Head>
                <title>{profile.fullname} • @{profile.username} • Superfly 🦋 </title>
                <meta property="og:url" content={`https://superfly.so/${profile.username}`}/>
                <meta property="og:type" content="article"/>
                <meta property="og:title" content={profile.title}/>
                <meta property="og:description" content={profile.bio}/>
                <meta property="og:image" content={profile['banner_url']}/>
                <meta name="viewport" content="initial-scale=1.0, width=device-width"/>
            </Head>
            <div className="layout-left">
                <div className="main-menu">
                    <MainLogo/>
                    <hr className="rounded"/>
                    <div className={'main-menu-icons'}>
                        <IoSearchOutline/>
                    </div>

                    <Link href={"/login"}>
                        <div className={'main-menu-icons'}>
                            <IoSearchOutline/><span>Login</span>
                        </div>
                    </Link>

                </div>
            </div>
            <div className="layout-right">
                <div>
                    <Tabs>
                        <TabList>
                            <Tab>
                                <p>Profile Information</p>
                            </Tab>
                            <Tab>
                                <p>Password</p>
                            </Tab>
                            <Tab>
                                <p>Social Accounts</p>
                            </Tab>
                            <Tab>
                                <p>Privacy</p>
                            </Tab>
                        </TabList>
                        <TabPanel>
                            <div className="panel-content">
                                <Formik
                                    className={"account-form"}
                                    initialValues={_.pick(profile, ['username', 'email', 'fullname', 'bio', 'title', 'phone'])}
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

                                            <label htmlFor="email">Username</label>
                                            <Field type="text" name="username"/>
                                            <ErrorMessage name="username" component="div"/>

                                            <label htmlFor="email">Full Name</label>
                                            <Field type="text" name="fullname"/>
                                            <ErrorMessage name="fullname" component="div"/>

                                            <label htmlFor="email">Title</label>
                                            <Field type="text" name="title"/>
                                            <ErrorMessage name="title" component="div"/>

                                            <label htmlFor="email">Email Address</label>
                                            <Field type="email" name="email"/>
                                            <ErrorMessage name="email" component="div"/>

                                            <label htmlFor="email">Phone Number</label>
                                            <Field type="text" name="phone"/>
                                            <ErrorMessage name="phone" component="div"/>

                                            <label htmlFor="email">Bio</label>
                                            <Field type="textarea" name="bio"/>
                                            <ErrorMessage name="bio" component="div"/>

                                            <button type="submit" disabled={isSubmitting}>
                                                Submit
                                            </button>
                                        </Form>
                                    )}
                                </Formik>
                            </div>
                        </TabPanel>
                        <TabPanel>
                            <div className="panel-content">
                                <Password {...props} />
                            </div>
                        </TabPanel>
                        <TabPanel>
                            <div className="panel-content">
                                <Select options={options} />
                            </div>
                        </TabPanel>
                        <TabPanel>
                            <div className="panel-content">
                                <h2>Any content 1</h2>
                            </div>
                        </TabPanel>
                    </Tabs>

                </div>
            </div>
        </div>


    );
}

export default Product;

