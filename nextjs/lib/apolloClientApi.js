import fetch from "isomorphic-unfetch";
import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client";

export function getApolloClient() {
  console.log(process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT);
  return new ApolloClient({
    link: createHttpLink({
      uri: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT,
      credentials: "same-origin",
      headers: {
        "X-Hasura-Admin-Secret": "Grox2yRd8p9l49yq1tgfYY9yyP3gxhQhlXZhz3LUS3HjGRFO5SeZ5YYFMuVAzxPY",
      },
      fetch,
    }),
    cache: new InMemoryCache(),
  });
}
