import { saveRefund } from './refund-repository.js';

export function createRefund(input) {
  if (!input?.orderId || !input.reason) {
    throw new Error('orderId and reason are required');
  }

  return saveRefund({ orderId: input.orderId, reason: input.reason });
}
