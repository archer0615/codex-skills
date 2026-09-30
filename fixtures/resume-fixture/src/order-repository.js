const orders = [];

export function saveOrder(order) {
  const saved = { id: `order-${orders.length + 1}`, ...order };
  orders.push(saved);
  return saved;
}
