import Layout from "../components/Layout";
import {initApolloClient, withApollo} from "../lib/withApollo";
import {GetAccount, SubscribeToAccount, SubscribeToBlocks} from "../lib/sharedQueries";
import {useSubscription} from "@apollo/client";

const HomePage = (props) => {
    let {profile, query, bg_colors, social_accounts_types, block_types, blocks, ...rest} = props
    if (!profile) {
        const {username} = query;
        return <div>Account {username} not found. Claim yours today.</div>
    }
    if (typeof window === 'undefined') {
        console.log("SSR: Not subscribing to graphql mutations")
    } else {
        let variables = {
            "username": profile['username']
        }
        let {
            data,
            loading,
            error
        } = useSubscription(SubscribeToAccount, {variables});

        if (data) {
            profile = data['accounts_by_pk'];
        }

        variables = {
            "owner_uid": profile['uid']
        }
        let {
            data: d,
            loading: l,
            error: e
        } = useSubscription(SubscribeToBlocks, {variables});

        if (d) {
            blocks = d['blocks']
        }
    }
    if (profile) {
        return <Layout className={'theme-verde'} {...props} />;
    } else {
        return <div>Bikozulu</div>;
    }
};

HomePage.getInitialProps = async (ctx) => {

    const {req, query, res, asPath, pathname} = ctx;


    let pageProps = {query}

    if (query.username) {
        let {username} = query;
        username = username.toLowerCase();
        console.log("getInitialProps username", username)
        const apolloClient = ctx.apolloClient || initApolloClient(null, {});
        const {data} = await apolloClient.query({
            query: GetAccount, variables: {username},
        });

        let {accounts: profile, bg_colors, social_accounts_types, block_types} = data;
        profile=profile[0]

        if (profile) {

            pageProps = {
                ...pageProps,
                ...data,
                profile,
                blocks: profile['blocks']
            };
        }
    } else {
        console.log("query.username null", query)
    }
    return {...pageProps};
};

export default withApollo({ssr: true})(HomePage);
