TASK: Process e-commerce order
ACTION: Validate, process payment, and fulfill
GOAL: Complete customer purchase successfully

CLASS Order
  order_id: string
  customer_id: string
  total_amount: float
  items: array
  shipping_address: string

CLASS Customer
  customer_id: string
  name: string
  email: string
  is_premium: bool
  loyalty_points: int

DEFINE FUNCTION validate_order(order)
  TASK: Check order validity
  ACTION: Verify items, prices, and customer info
  GOAL: Ensure order can be processed

DEFINE FUNCTION process_payment(order, customer)
  TASK: Charge customer account
  ACTION: Call payment gateway API
  GOAL: Secure payment for order

DEFINE FUNCTION update_inventory(order)
  TASK: Reduce stock levels
  ACTION: Update database inventory
  GOAL: Maintain accurate stock counts

DEFINE FUNCTION send_confirmation(order, customer)
  TASK: Notify customer of successful order
  ACTION: Send email with order details
  GOAL: Provide excellent customer experience

CALL validate_order(current_order)

IF order_valid = true THEN
  TASK: Proceed with payment
  ACTION: Process customer payment
  GOAL: Complete financial transaction
  
  CALL process_payment(current_order, current_customer)
  
  IF payment_successful = true THEN
    TASK: Fulfill order
    ACTION: Update inventory and ship
    GOAL: Complete order fulfillment
    
    CALL update_inventory(current_order)
    CALL send_confirmation(current_order, current_customer)
    
    TASK: Update loyalty program
    ACTION: Add points to customer account
    GOAL: Reward customer loyalty
    
    CALL API loyalty_service.add_points WITH {
      customer_id: current_customer.customer_id,
      points: calculate_points(current_order.total_amount)
    }
  ELSE
    TASK: Handle payment failure
    ACTION: Notify customer and retry
    GOAL: Recover from payment error
    
    CALL API notification_service.send WITH {
      to: current_customer.email,
      subject: "Payment Failed",
      template: "payment_failed"
    }
  END IF
ELSE
  TASK: Handle invalid order
  ACTION: Notify customer of issues
  GOAL: Help customer fix order problems
  
  CALL API notification_service.send WITH {
    to: current_customer.email,
    subject: "Order Issues",
    template: "order_invalid"
  }
END IF

FOR EACH item IN current_order.items
  TASK: Check item availability
  ACTION: Verify stock for each item
  GOAL: Ensure all items are available
  
  CALL API inventory_service.check_stock WITH {
    sku: item.sku,
    quantity: item.quantity
  }
END FOR

ON ERROR
  TASK: Handle system errors
  ACTION: Log error and notify admin
  GOAL: Maintain system reliability
  
  CALL API logging_service.log_error WITH {
    error_type: "order_processing",
    order_id: current_order.order_id,
    error_message: error.message
  }
  
  CALL API notification_service.send_admin WITH {
    subject: "Order Processing Error",
    message: "Order " + current_order.order_id + " failed to process"
  }

LOOPGUARD {
  max_depth: 5,
  allow_repeat: false
} 