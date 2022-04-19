export async function createInitialOrderAndOrderItems(
  apolloClient,
  createOrderInput,
  products
) {
  // Create order in DB
  const { data: orderData } = await apolloClient.mutate({
    mutation: gql`
      mutation InsertOrder($inputObject: order_insert_input = {}) {
        insert_order_one(object: $inputObject) {
          uid
        }
      }
    `,
    variables: {
      inputObject: createOrderInput,
    },
  });
  const {
    insert_order_one: { uid: orderId },
  } = orderData;
  const { data: orderProductsData } = await apolloClient.mutate({
    query: gql`
      mutation InsertOrderProducts($items: [order_product_insert_input!] = {}) {
        insert_order_product(objects: $items) {
          affected_rows
          returning {
            order_uid
            product_uid
            quantity
          }
        }
      }
    `,
    variables: {
      items: products.map((product) => ({
        order_uid: orderId,
        product_uid: product.uid,
        quantity: product.purchaseCount,
      })),
    },
  });
  return {
    orderId,
    orderProductsData,
  };
}
