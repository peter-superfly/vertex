export async function fetchStoreAndProductsAndValidate(
  storeId,
  products,
  apolloClient,
  res
) {
  const { data } = await apolloClient.query({
    query: gql`
      query StoreAndProducts($storeId: uuid, $productIds: [uuid!]) {
        store: merchant_store(where: { uid: { _eq: $storeId } }) {
          ig_username
          uid
          products(where: { uid: { _in: $productIds } }) {
            uid
            status
            price
            inventory_count
            display_name
            description
            discount_amount
            discount_percent
          }
          country {
            iso_2
            iso_3
            id
            currency {
              ISO_code
              id
              symbol
            }
          }
        }
      }
    `,
    variables: {
      storeId,
      productIds: products.map((product) => product.id),
    },
  });
  if (!data.store[0]) {
    return res.status(404).json({ success: false, error: "Store not found" });
  }
  const {
    store: [store],
  } = data;
  if (!(store.products.length === products.length)) {
    return res
      .status(404)
      .json({ success: false, error: "Products not found" });
  }
  let { products: storeProducts } = store;
  storeProducts = storeProducts.map((product) => ({
    ...product,
    purchaseCount: products.find((p) => p.id === product.uid).quantity,
  }));
  const unavailableProducts = storeProducts.filter(
    (product) => product.inventory_count < product.purchaseCount
  );
  if (unavailableProducts.length > 0) {
    return res.status(400).json({
      success: false,
      error: `${unavailableProducts
        .map((product) => product.display_name)
        .join(", ")} product(s) out of stock`,
    });
  }
  return {
    store,
    storeProducts,
  };
}
