import Product from "../../components/account/info";
import {initApolloClient, withApollo} from "../../lib/withApollo";
import {GetAccount} from "../../lib/sharedQueries";
import {getLS} from "../../lib/ls";
import { useRouter } from "next/router";
import Link from 'next/link'

const HomePage = ({profile, ...rest}) => {
    let logged_in_user = getLS('user')
    console.log(profile, logged_in_user)
    let can_edit_profile = logged_in_user && (logged_in_user['uid'] === profile['uid'])

    const router = useRouter();

    if (!can_edit_profile) {
        return <div>User Not logged in
            <Link  href={"/"}>
                <img src="/logo.svg"/>
            </Link>
        </div>
    }


    // return <div></div>
    return <Product profile={profile} {...rest} />;
};

HomePage.getInitialProps = async (ctx) => {
    const {req, query, res, asPath, pathname} = ctx;

    console.log(query)

    let pageProps = {}

    if (query.username) {
        const {username} = query;
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
                profile,
                block_types,
                bg_colors,
                social_accounts_types,
                blocks: profile['blocks']
            };
        }
    } else {
        console.log("query.username null", query)

        const username = 'peter'
        const apolloClient = ctx.apolloClient || initApolloClient(null, {});
        const {data} = await apolloClient.query({
            query: GetAccount, variables: {username},
        });
        let {accounts: profile, bg_colors, social_accounts_types, block_types} = data;
        profile=profile[0]

        pageProps = {...pageProps, profile, block_types};
    }

    return {...pageProps};
};

export default withApollo({ ssr: true })(HomePage);
