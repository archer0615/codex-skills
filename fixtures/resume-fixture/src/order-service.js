import { saveOrder } from './order-repository.js';

export function createOrder(input) {
  if (!input?.customerId || !Array.isArray(input.items) || input.items.length === 0) {
    throw new Error('customerId and at least one item are required');
  }

  return saveOrder({ customerId: input.customerId, items: input.items });
}
