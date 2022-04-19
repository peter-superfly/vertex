import { useState, useEffect } from "react";
const axios = require("axios");
import { getLS, setLS, clearLS } from "./ls";
import { globalApolloClient } from "./withApollo";

export async function logoutUser() {
  clearLS();
  globalApolloClient.clearStore();
}

export async function getCurrentUserToken(req) {
  let is_server_side = typeof window === "undefined";

  let user = null;

  if (is_server_side) {
    user = null;
  } else {
    user = getLS("user") || null;
  }

  const res = await axios.post("https://api.dropshop.cc/authorized/", req);

  return null;
}

export function useFetchUser() {
  let is_server_side = typeof window === "undefined";

  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(() => {
    if (is_server_side) {
      return null;
    } else {
      return getLS("user") || null;
    }
  });

  useEffect(
    () => {
      if (loading || is_server_side) {
        return;
      }

      setLoading(true);
      let isMounted = true;

      if (user) {
        setLoading(false);
        try {
          axios
            .post("https://api.dropshop.cc/authorized/", {
              token: user.token,
            })
            .then(function (response) {
              setLoading(false);

              if (response.data.valid) {
                setUser(user);
              } else {
                logoutUser();
              }
            })
            .catch(function (error) {
              clearLS();
              setUser(null);
              setLoading(false);
              console.error(error);
            });
        } catch (error) {
          setLoading(false);
          console.error(error);
        }
      } else {
        setLoading(false);
        console.log("No user to verify");
      }

      return () => {
        isMounted = false;
      };
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return { user, loading };
}
