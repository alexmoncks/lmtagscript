
TASK: Process purchase
ACTION: Validate user and stock
GOAL: Complete the order

IF stock_available = true THEN
  TASK: Proceed to payment
  ACTION: Call payment API
  GOAL: Finish transaction
ELSE
  TASK: Notify user
  ACTION: Send out-of-stock message
  GOAL: Inform and retain user

FOR EACH item IN cart
  TASK: Check availability
  ACTION: Query inventory system
  GOAL: Determine stock level

CALL API purchase_api.finalize WITH {
  user_id: "12345"
}
ON ERROR
  TASK: Fallback to manual
  ACTION: Log the failed purchase
  GOAL: Prevent loss of order

LOOPGUARD {
  max_depth: 3,
  allow_repeat: false
}
