import { getLS } from "./ls";
import { v1 as uuidv1 } from "uuid";

export function get_site_info({ host }) {
  let isSSR = typeof window === "undefined";
  let hostname = isSSR ? host : window.location.hostname;
  let is_dropshop_domain = hostname.match(/seller.dropshop.(cc|dev)/g);
  let is_seller = false;

  if (!isSSR) {
    is_seller =
      is_dropshop_domain || window.location.origin === "http://localhost:3000";
  }

  return { isSSR, is_seller };
}