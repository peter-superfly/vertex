import { withApollo } from "../lib/withApollo";
import Login from "../components/Auth/Login";

const IndexPage = (props) => {
    return <Login {...props}/>;
};

export default withApollo({ ssr: true })(IndexPage);
