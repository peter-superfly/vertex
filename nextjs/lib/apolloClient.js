import fetch from "isomorphic-unfetch";
import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client";
import { getLS, setLS, clearLS } from "./ls";
import { onError } from "apollo-link-error";
import { WebSocketLink } from "apollo-link-ws";
import { SubscriptionClient } from "subscriptions-transport-ws";

let user = getLS("user");
let accessToken = user ? user.token : null;

const requestAccessToken = async () => {
  if (accessToken) return;

  /*Fetch token here!*/
};

// remove cached token on 401 from the server
const resetTokenLink = onError(({ networkError }) => {
  if (
    networkError &&
    networkError.name === "ServerError" &&
    networkError.statusCode === 401
  ) {
    accessToken = null;
  }
});

const _createHttpLink = (headers) => {
  headers["x-hasura-admin-secret"] = "Grox2yRd8p9l49yq1tgfYY9yyP3gxhQhlXZhz3LUS3HjGRFO5SeZ5YYFMuVAzxPY"
  return createHttpLink({
    uri: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT,
    // credentials: "same-origin",
    headers,
    fetch,
  });
};

const createWSLink = () => {
  return new WebSocketLink(
    new SubscriptionClient("wss://superfly.hasura.app/v1/graphql", {
      lazy: true,
      reconnect: true,
      connectionParams: async () => {
        if (accessToken) {
          await requestAccessToken(); // happens on the client
          return {
            headers: {
              // authorization: accessToken ? `Bearer ${accessToken}` : "",
              // authorization: 'Grox2yRd8p9l49yq1tgfYY9yyP3gxhQhlXZhz3LUS3HjGRFO5SeZ5YYFMuVAzxPY',
              // "x-hasura-role": "seller",
              "x-hasura-admin-secret": "Grox2yRd8p9l49yq1tgfYY9yyP3gxhQhlXZhz3LUS3HjGRFO5SeZ5YYFMuVAzxPY",
            },
          };
        } else {
          return {
            headers: {
              "x-hasura-admin-secret": "Grox2yRd8p9l49yq1tgfYY9yyP3gxhQhlXZhz3LUS3HjGRFO5SeZ5YYFMuVAzxPY"
            },
          };
        }
      },
    })
  );
};

export default function createApolloClient(initialState, headers) {
  const ssrMode = typeof window === "undefined";
  let link;
  console.log(headers)
  if (ssrMode) {
    link = _createHttpLink(headers);
  } else {
    link = createWSLink();
  }
  return new ApolloClient({
    ssrMode,
    link,
    cache: new InMemoryCache().restore(initialState),
  });
}
