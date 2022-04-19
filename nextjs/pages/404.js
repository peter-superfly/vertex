import { useRouter } from "next/router";

import { withApollo } from "../lib/withApollo";

const ErrorPage = () => {
  let isSSR = typeof window === "undefined";

  if (isSSR) {
    return (
      <div>
        <h2>Error</h2>
        <h3>Create an Instagram Store in Less than a minute</h3>
      </div>
    );
  }

  let is_seller = window.location.hostname === "seller.dropshop.cc";

  const router = useRouter();
  router.push("/");
  return null;
};

export default withApollo({ ssr: false })(ErrorPage);
