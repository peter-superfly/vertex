import React, {useState, useEffect} from 'react';
import Arena from './Arena';
import MainMenu from './Common/MainMenu';
import Link from 'next/link'
import _ from 'lodash';
import { useRouter } from "next/router";
import {getLS} from "../lib/ls";
import {searchClient, search} from "../lib/typesense";

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

function Layout(props) {
    console.log(searchClient)

    const router = useRouter();

    const navToCase = (case_id) => {
        console.log("case-id", case_id)
        router.push(`/u/${case_id}`);
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
        return (<div className={"person-card"} onClick={() => navToCase(hit['id'])}>
                <h4>{hit.citation}</h4>
                <p>{hit.case_number}</p>
                <img width={'100px'} height={'100px'} src={"https://images.unsplash.com/photo-1596365481115-79cb80ea517b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=854&q=80"} />
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

                <Hits class-name={'people-hit-container'} hitComponent={Hit}/>
            </div>
        </InstantSearch>
    </div>);
}

export default Layout;
