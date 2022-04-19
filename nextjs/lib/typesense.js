import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import instantsearch from 'instantsearch.js'

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
    server: {
        apiKey: process.env.NEXT_PUBLIC_TS_API_KEY, // Be sure to use the search-only-api-key
        nodes: [
            {
                host: process.env.NEXT_PUBLIC_TS_HOST,
                port: "443",
                protocol: "https"
            }
        ]
    },
    // The following parameters are directly passed to Typesense's search API endpoint.
    //  So you can pass any parameters supported by the search endpoint below.
    //  queryBy is required.
    additionalSearchParameters: {
        queryBy: "citation,case_number,court_name"
    }
});

export const searchClient = typesenseInstantsearchAdapter.searchClient;

export const search = instantsearch({
    searchClient,
    indexName: "books"
});