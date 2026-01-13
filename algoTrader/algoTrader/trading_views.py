from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
#from .tasks import add_company
#from .models import Order
import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_protect
def trading_interface(request):
    """Render the trading interface page with recent orders"""
    # Get the 10 most recent orders
    #recent_orders = Order.objects.all()[:10]
    #{'recent_orders': recent_orders}
    return render(request, 'trading.html', )

@csrf_protect
def handle_place_order(request):
    """Handle the place order form submission"""
    if request.method == 'POST':
        try:
            # Log each field individually
            logger.info("Extracting form fields...")
            symbol = request.POST.get('symbol')
            logger.info(f"Symbol: {symbol}")
            
            quantity = request.POST.get('quantity')
            logger.info(f"Quantity (before conversion): {quantity}")
            quantity = int(quantity) if quantity else None
            logger.info(f"Quantity (after conversion): {quantity}")
            
            symbol_token = request.POST.get('symbol_token')
            logger.info(f"Symbol Token: {symbol_token}")
            
            transaction_type = request.POST.get('transaction_type')
            logger.info(f"Transaction Type: {transaction_type}")
            
            limit_price = request.POST.get('limit_price')
            logger.info(f"Limit Price (before conversion): {limit_price}")
            limit_price = float(limit_price) if limit_price else None
            logger.info(f"Limit Price (after conversion): {limit_price}")

            # Validate all required fields are present
            if not all([symbol, quantity, symbol_token, transaction_type, limit_price]):
                error_msg = "Missing required fields"
                logger.error(error_msg)
                messages.error(request, error_msg)
                return redirect('trading_interface')
            
            # Then call the Celery task with the correct parameter order
            logger.info("Attempting to call add_company.delay with parameters:")
            logger.info(f"symbol={symbol}, quantity={quantity}, symbol_token={symbol_token}, transaction_type={transaction_type}, limit_price={limit_price}")
            
            # try:
                # task = add_company.delay(
                #     symbol,
                #     quantity,
                #     symbol_token,
                #     transaction_type,
                #     limit_price,
                # )
                # print("📢 add_company.delay() called")
            #     logger.info(f"Task created successfully with ID: {task.id}")
            # except Exception as task_error:
            #     logger.error(f"Error creating task: {str(task_error)}", exc_info=True)
            #     raise
            
            # Create success message
            # success_msg = f'Order placement task initiated. Task ID: {task.id}'
            # messages.success(request, success_msg)
            # logger.info(f"Success message created: {success_msg}")
            
        except Exception as e:
            error_msg = f'Error placing order: {str(e)}'
            logger.error(f"Exception in handle_place_order: {str(e)}", exc_info=True)
            messages.error(request, error_msg)
            logger.error(f"Error message created: {error_msg}")
    
    return redirect('trading_interface')

@csrf_protect
def handle_exit_order(request):
    """Handle the exit order form submission"""
    if request.method == 'POST':
        try:
            logger.info(f"Received exit order request: {request.POST}")
            
            symbol = request.POST.get('symbol')
            limit_price = float(request.POST.get('limit_price'))

            # Call the Celery task
            #task = exit_order.delay(symbol, limit_price)
            
            # Create order record
            # Order.objects.create(
            #    # task_id=task.id,
            #     symbol=symbol,
            #     price=limit_price,
            #     quantity=0,  # Will be updated when we get position details
            #     transaction_type='SELL',  # Exit is always SELL
            #     order_type='EXIT',
            #     status='PENDING'
            # )
            
            #success_msg = f'Exit order task initiated. Task ID: {task.id}'
           # messages.success(request, success_msg)
            #logger.info(f"Success message created: {success_msg}")
            
        except Exception as e:
            error_msg = f'Error exiting order: {str(e)}'
            messages.error(request, error_msg)
            logger.error(f"Error message created: {error_msg}")
    
    return redirect('trading_interface')

# @csrf_protect
# def handle_modify_order(request):
#     """Handle the modify order form submission"""
#     if request.method == 'POST':
#         try:
#             logger.info(f"Received modify order request: {request.POST}")
            
#             order_id = request.POST.get('order_id')
#             new_price = float(request.POST.get('new_price'))
#             new_quantity = int(request.POST.get('new_quantity'))

#             # Call the Celery task
#             task = modify_exit_order.delay(order_id, new_price, new_quantity)
            
#             # Create order record
#             Order.objects.create(
#                 task_id=task.id,
#                 order_id=order_id,
#                 price=new_price,
#                 quantity=new_quantity,
#                 order_type='MODIFY',
#                 status='PENDING'
#             )
            
#             success_msg = f'Order modification task initiated. Task ID: {task.id}'
#             messages.success(request, success_msg)
#             logger.info(f"Success message created: {success_msg}")
            
#         except Exception as e:
#             error_msg = f'Error modifying order: {str(e)}'
#             messages.error(request, error_msg)
#             logger.error(f"Error message created: {error_msg}")
    
#     return redirect('trading_interface')

# @csrf_protect
# def handle_delete_order(request, order_id):
#     """Handle the deletion of an order"""
#     if request.method == 'POST':
#         try:
#             logger.info(f"Received delete order request for order ID: {order_id}")
            
#             # Get the order
#             order = Order.objects.get(id=order_id)
            
#             # Delete the order
#             order.delete()
            
#             success_msg = f'Order {order_id} has been deleted successfully.'
#             messages.success(request, success_msg)
#             logger.info(f"Success message created: {success_msg}")
            
#         except Order.DoesNotExist:
#             error_msg = f'Order with ID {order_id} not found.'
#             messages.error(request, error_msg)
#             logger.error(f"Error message created: {error_msg}")
#         except Exception as e:
#             error_msg = f'Error deleting order: {str(e)}'
#             messages.error(request, error_msg)
#             logger.error(f"Error message created: {error_msg}")
    
#     return redirect('trading_interface') 
