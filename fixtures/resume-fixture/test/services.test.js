import test from 'node:test';
import assert from 'node:assert/strict';
import { createOrder } from '../src/order-service.js';
import { createRefund } from '../src/refund-service.js';

test('creates an order through the order service and repository', () => {
  const order = createOrder({ customerId: 'customer-1', items: ['book'] });
  assert.equal(order.id, 'order-1');
  assert.equal(order.customerId, 'customer-1');
});

test('creates a refund through the refund service and repository', () => {
  const refund = createRefund({ orderId: 'order-1', reason: 'duplicate' });
  assert.equal(refund.id, 'refund-1');
  assert.equal(refund.orderId, 'order-1');
});
