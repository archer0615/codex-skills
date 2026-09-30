import express from 'express';
import { createOrder } from './order-service.js';
import { createRefund } from './refund-service.js';

export const app = express();
app.use(express.json());

app.post('/orders', (request, response) => {
  response.status(201).json(createOrder(request.body));
});

app.post('/refunds', (request, response) => {
  response.status(201).json(createRefund(request.body));
});
