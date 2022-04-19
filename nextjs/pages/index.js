import { withApollo } from "../lib/withApollo";
import {getLS} from "../lib/ls";
import Layout from "../components/Layout";

const IndexPage = (props) => {
  return <Layout {...props} />;
};

export default withApollo({ ssr: true })(IndexPage);
