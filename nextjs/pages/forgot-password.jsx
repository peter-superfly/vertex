import { withApollo } from "../lib/withApollo";
import ForgotPassword from "../components/Auth/ForgotPassword";

const IndexPage = (props) => {
    return <ForgotPassword/>;
};

export default withApollo({ ssr: true })(IndexPage);
