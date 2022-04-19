import { withApollo } from "../lib/withApollo";
import Register from "../components/Auth/Register";

const IndexPage = (props) => {
    return <Register/>;
};

export default withApollo({ ssr: true })(IndexPage);
