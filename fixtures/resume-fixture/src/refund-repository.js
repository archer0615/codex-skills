const refunds = [];

export function saveRefund(refund) {
  const saved = { id: `refund-${refunds.length + 1}`, ...refund };
  refunds.push(saved);
  return saved;
}
