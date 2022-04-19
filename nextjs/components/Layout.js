import React, {useState, useEffect} from 'react';
import MainMenu from './Common/MainMenu';
import Link from 'next/link'
import _ from 'lodash';
import { useRouter } from "next/router";
import {getLS} from "../lib/ls";
import {searchClient, search} from "../lib/typesense";
import { ReactComponent as Logo } from '../public/logo.svg';

import {
    InstantSearch,
    SearchBox,
    Hits,
    HierarchicalMenu,
    RefinementList,
    ToggleRefinement,
    RatingMenu,
    ClearRefinements,
    FacetList,
    Stats,
    connectHighlight,
    HitsPerPage,
    SortBy,
    Pagination,
} from 'react-instantsearch-dom'


import Head from 'next/head'

function MainLogo({}) {
    let logged_in_user = getLS('user')

    return (<div className={'main-logo'}>
        <Link href={logged_in_user ? `/${logged_in_user['username']}` : "/"}>
            <Logo fill='red' stroke='green'/>
        </Link></div>)
}

function Layout(props) {
    console.log(searchClient)

    const router = useRouter();

    const navToCase = (case_id) => {
        console.log("case-id", case_id)
        router.push(`/case/${case_id}`);
    }

    const CustomHighlight = connectHighlight(({highlight, attribute, hit}) => {
        const parsedHit = highlight({
            highlightProperty: '_highlightResult', attribute, hit
        });

        return (<div>
            {parsedHit.map(part => (part.isHighlighted ? <mark>{part.value}</mark> : part.value))}
        </div>);
    });

    const Hit = ({hit}) => {
        console.log(hit)
        return (<div className={"case-card"} onClick={() => navToCase(hit['id'])}>
            <h3>{hit.citation}</h3>
            <p>{hit.case_number}</p>
            <p><span>{hit.case_class}</span> | {hit.court_name}</p>

            <CustomHighlight attribute="name" hit={hit}/>
        </div>);
    }

    return (<div className={"layout-parent jura"}>
        <Head>
        </Head>
        <div className="layout-left">
            <MainMenu/>
        </div>

        <InstantSearch
            indexName="cases-main"
            searchClient={searchClient}
        >
            <div className="layout-center">
                <RefinementList
                    className="mt-3"
                    attribute="court_name"
                    limit={10}
                    showMore={true}
                    showMoreLimit={50}
                    searchable={true}
                />
                <RefinementList
                    className="mt-3"
                    attribute="case_class"
                    limit={10}
                    showMoreLimit={50}
                    transformItems={items => items.sort((a, b) => a.label > b.label ? 1 : -1)}
                />
            </div>
            <div className="layout-right">

                <SearchBox/>

                <Hits hitComponent={Hit}/>
            </div>
        </InstantSearch>
    </div>);
}

export default Layout;
