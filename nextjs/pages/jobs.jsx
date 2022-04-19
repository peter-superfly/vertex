import People from "../components/People";
import {withApollo} from "../lib/withApollo";

const HomePage = (props) => {
    let {profile, query, bg_colors, social_accounts_types, block_types, blocks, ...rest} = props

    return <People className={'theme-verde'} {...props} />
};

HomePage.getInitialProps = async (ctx) => {

    const {req, query, res, asPath, pathname} = ctx;
};

export default withApollo({ssr: true})(HomePage);
