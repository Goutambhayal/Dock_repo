from celery import shared_task
from django.shortcuts import render
from datetime import datetime, timedelta,time
from django.db import connection;
from .angel_one_services import AngelOneService  # Import your service class
from django.views.decorators.csrf import csrf_exempt
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from django.http import JsonResponse, HttpResponse
import json,requests,redis
import traceback
#from .models import Order
import logging,threading
# from .consumers import send_order_update
import pytz
from .celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




# Set up logging
logger = logging.getLogger(__name__)
# Global WebSocket instance
sws1 = None

# Initialize Redis for sharing data between tasks
redis_client = redis.Redis(host='redis', port=6379, db=0,decode_responses=True)
r=redis_client

# Initialize Angel One service
angel_services = AngelOneService.get_instance()
API_KEY = angel_services.API_KEY
CLIENT_ID = angel_services.CLIENT_CODE

def get_tokens():
    """Get tokens from the Angel One service"""
    service = angel_services
    if not service._validate_tokens():
        raise Exception("Invalid or missing tokens. Please check if Django server is running.")
    return {
        'auth_token': str(service.jwt_token),
        'feed_token': str(service.feed_token),
        'api_key': str(service.API_KEY),
        'client_code': str(service.CLIENT_CODE)
    }

#subscribed_tokens = {'11956','277','11377','2142','13270','1406','14592'}
subscribed_tokens={'8727', '30108', '5385', '27061', '23729', '7', '5578', '756843', '757336', '25977', '11343', '1467', '25328', '11703', '163', '5378', '212', '11618', '14418', '5610', '757645', '263', '275', '19913', '368', '395', '17279', '19585', '757102', '383', '438', '10604', '23489', '11373', '19686', '8311', '2203', '15254', '628', '760', '20329', '8866', '685', '5049', '11543', '342', '18060', '4421', '1901', '811', '772', '827', '9599', '10940', '21690', '29452', '916', '919', '21154', '14450', '9383', '24398', '25162', '1041', '12032', '16783', '13528', '1186', '1153', '13409', '10099', '10925', '13560', '13750', '13197', '13966', '4244', '21951', '9819', '2056', '3417', '5622', '20988', '10726', '20261', '11262', '29135', '20607', '7852', '5926', '1633', '4986', '1726', '11655', '13637', '11236', '2783', '3637', '13260', '14912', '13310', '5108', '1949', '1814', '2955', '12092', '20936', '24948', '2606', '10440', '13285', '2031', '19061', '15380', '10999', '7242', '9581', '22308', '31181', '23650', '3918', '14672', '17433', '2406', '15815', '357', '18721', '10637', '6705', '29224', '756802', '6656', '25358', '16682', '13147', '9741', '18365', '14552', '2664', '11571', '25718', '9590', '11403', '20302', '8825', '940', '9553', '18566', '14255', '18883', '3273', '27052', '27839', '4892', '31238', '17186', '756871', '13332', '4684', '7083', '17105', '3351', '3339', '3345', '3363', '12018', '27095', '10793', '8479', '3721', '6445', '7105', '3475', '19196', '14198', '15414', '3506', '3518', '11287', '14154', '8840', '15362', '28847', '27969', '14366', '756038', '7506', '3812', '7508', '27144', '7929', '758858', '4481', '1134', '9111', '15058', '3149', '5142', '757850', '11423', '758563', '27213', '20322', '13710', '1267', '29731', '1485', '21062', '22663', '25643', '8054', '14972', '18944', '199', '756324', '2972', '5911', '19631', '14922', '29711', '13414', '2816', '6643', '21501', '3387', '28805', '19184', '757965', '3324', '10945', '21828', '3703', '14766', '14602', '17738', '18608', '13061', '474', '13', '22', '25780', '21238', '17903', '10217', '25', '3563', '15083', '17388', '6066', '21614', '1270', '757885', '157', '5435', '236', '5900', '16669', '16675', '317', '305', '25270', '335', '2263', '4668', '11377', '17927', '404', '2144', '422', '526', '6435', '2181', '24814', '547', '757', '10794', '3906', '595', '21740', '5701', '20374', '21508', '15141', '4749', '739', '17094', '14732', '8075', '910', '18822', '958', '5097', '1023', '1008', '11573', '14592', '4717', '13337', '277', '7406', '11956', '23799', '1181', '17875', '1232', '7229', '757772', '1333', '1348', '29666', '1363', '2303', '1406', '1394', '1424', '18457', '20825', '25844', '4963', '21770', '18652', '1476', '11184', '1491', '29251', '1660', '14309', '1512', '1624', '9348', '13611', '2029', '5258', '13751', '1594', '11195', '28125', '13270', '17869', '19020', '11723', '6733', '18143', '18096', '19126', '1196', '18581', '1922', '13816', '18564', '1997', '1979', '17818', '11483', '19234', '9480', '1627', '17313', '3220', '2277', '2283', '4067', '2142', '22377', '509', '8596', '14947', '4503', '17400', '15332', '27176', '11630', '11840', '6364', '17963', '5426', '20242', '2475', '17438', '24777', '10738', '24184', '14413', '17029', '11351', '14299', '14977', '25049', '2535', '21001', '15355', '10990', '9552', '2885', '3761', '17971', '21808', '4204', '1011', '3103', '4306', '3150', '13826', '3045', '2963', '9617', '27066', '11536', '3432', '3411', '1621', '3456', '3426', '3499', '13538', '2043', '13786', '1964', '312', '11223', '11532', '10753', '16713', '10447', '18921', '3063', '3718', '25907', '3787', '11915', '1076', '15179', '11868', '13086', '8110', '625', '6018', '25984', '40', '8124', '24308', '100', '7145', '13620', '324', '2829', '11491', '193', '203', '1508', '15034', '14501', '371', '3834', '11966', '6994', '759291', '495', '380', '15184', '11452', '14937', '7603', '14966', '583', '5407', '1250', '14894', '14982', '13305', '8546', '637', '17945', '2854', '5748', '7358', '19943', '5373', '18086', '20551', '11654', '13643', '928', '937', '13517', '4907', '5382', '676', '3744', '1038', '14304', '5054', '1127', '1085', '5475', '1576', '144', '11778', '11971', '20534', '13776', '1235', '8828', '10599', '5204', '3892', '14334', '17939', '13072', '11809', '15313', '3329', '1675', '23693', '1515', '220', '4751', '28378', '1630', '15266', '13491', '11860', '11880', '11763', '5633', '2331', '3024', '20224', '15146', '21334', '13359', '15283', '9683', '1808', '758558', '4847', '18321', '25807', '29482', '17534', '2085', '18226', '31415', '2319', '8585', '4014', '2987', '399', '1164', '27097', '21469', '30089', '2649', '18908', '11355', '2643', '2705', '13496', '18391', '31163', '2431', '15337', '9408', '7401', '13451', '27297', '25073', '2859', '758551', '20323', '128', '18026', '3186', '18614', '18359', '25222', '1442', '5751', '17758', '757014', '17271', '3078', '10530', '12026', '4693', '9428', '13631', '21091', '9309', '13404', '2183', '3348', '10243', '1581', '23740', '29008', '3405', '20293', '14223', '17032', '9117', '15174', '28714', '757545', '9685', '25584', '527', '3724', '20188', '2073', '8167', '17364', '11821', '11580', '18011', '16915', '17635'}
all_tokens={}
default_price_data = {
    "initial_price":0,
    "final_price":0,
    "temp_high":0,
    "temp_low": 0,
    "high": 0,
    "low": 0,
    "L_temp_low":0,
    "L_temp_high":0,
    "L_low":0,
    "L_high":0,
    "d_high":0,
    "d_low":0,

}
price_data= {token: default_price_data.copy() for token in subscribed_tokens}

def add_company():     #we have to run this function  if we add any new token to our subscribed token list 
    for token in subscribed_tokens:
        r.hset(f"price_data:{token}", mapping=default_price_data)


@app.task
def place_order(symbol_token, details):
    try:
        service = angel_services
        service.ensure_login()

        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": details["symbol"],
            "symboltoken": symbol_token,
            "transactiontype": details["transaction_type"],
            "exchange": "NSE",
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": details["limit_price"],
            "quantity": details["quantity"]
        }

        logger.info(f"Placing order: {order_params}")
        order_id = service.smartApi.placeOrder(order_params)
        logger.info(f"Order placed for {details['symbol']} - ID: {order_id}")
       
        

        return order_id
        
    except Exception as e:
        logger.error(f"Error placing order for {details['symbol']}: {str(e)}")
        return None
@shared_task
def main1():
    global sws1

    # Initial setup
    tokens = get_tokens()
    sws1 = SmartWebSocketV2(
        auth_token=tokens['auth_token'],
        api_key=tokens['api_key'],
        client_code=tokens['client_code'],
        feed_token=tokens['feed_token']
    )

    def on_data(wsapp, message):
        try:
            symbol_token = str(message.get("token"))
            # pd=price_data[symbol_token]
            r.set("ws_last_seen", datetime.now().timestamp())
            if "last_traded_price" in message:
                ltp = float(message["last_traded_price"]) / 100.0
                now = datetime.now().time()
                r.hset("all_tokens",symbol_token,ltp)
                update_prices(symbol_token,now,ltp)
                                
        except Exception as e:
            logger.error(f"Error in on_data: {str(e)}")

    def on_open(wsapp):
        logger.info("WebSocket connected. Subscribing to initial tokens.")
        
        token_list = [{"exchangeType": 1, "tokens": list(subscribed_tokens)}]
        print("hello1")
        sws1.subscribe("order", 1, token_list)
        print("hello2")

    def on_error(wsapp, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(wsapp, *args):
        logger.info("WebSocket closed.")

    sws1.on_data = on_data
    sws1.on_open = on_open
    sws1.on_error = on_error
    sws1.on_close = lambda wsapp, *args: on_close(wsapp)

    logger.info("Connecting WebSocket...")
    #sws1.connect()
    # 🟢 RUN IN BACKGROUND THREAD
    threading.Thread(target=sws1.connect, daemon=True).start()
    logger.info("WebSocket thread started")
    return "WebSocket started in background thread"

@shared_task
def update_prices(symbol_token,now,ltp):
    # calculating one day high and low
    d_high=float(r.hget(f"price_data:{symbol_token}", "d_high"))
    d_low=float(r.hget(f"price_data:{symbol_token}", "d_low"))
    if d_high<ltp:
        r.hset(f"price_data:{symbol_token}","d_high",ltp)
    if d_low>ltp:
        r.hset(f"price_data:{symbol_token}","d_low",ltp)

    # storing all parameter of price_data:{symbol_token} in dumy array data
    pd=  r.hgetall(f"price_data:{symbol_token}")
    data = {}
    for token, price in pd.items():
        data[token] = float(price)

    #updating parameters of price_data:{symbol_token} in redis database 
    if time(9, 16) <= now <= time(15, 10):
        if (data["initial_price"]==0):
            r.hset(f"price_data:{symbol_token}",mapping={
                "initial_price":ltp,
                "final_price":ltp,
                "temp_high":ltp,
                "temp_low": ltp,
                "high": ltp,
                "low": ltp,
                "L_temp_low":ltp,
                "L_temp_high":ltp,
                "L_low":ltp,
                "L_high":ltp,
                
            })
        # Always update final_price
        r.hset(f"price_data:{symbol_token}", "final_price", ltp)
        update_prices_part1(data,symbol_token,ltp)
        update_prices_part2(data,symbol_token,ltp)
        # pd=  r.hgetall(f"price_data:{symbol_token}")
        # dat = {}
        # for token, price in pd.items():
        #     dat[token] = float(price)
        # print(dat)   

@shared_task
def update_prices_part1(data,symbol_token,ltp):
    if( data["temp_high"] < ltp):
        r.hset(f"price_data:{symbol_token}", mapping={"temp_high": ltp, "temp_low": ltp})
    elif (data["temp_low"] > ltp):
        r.hset(f"price_data:{symbol_token}", "temp_low", ltp)
    temp_high = float(r.hget(f"price_data:{symbol_token}", "temp_high"))
    temp_low = float(r.hget(f"price_data:{symbol_token}", "temp_low"))
    high = float(r.hget(f"price_data:{symbol_token}", "high"))
    low = float(r.hget(f"price_data:{symbol_token}", "low"))
    if( temp_high - temp_low > high - low):
        r.hset(f"price_data:{symbol_token}", mapping={"high": temp_high, "low": temp_low})
        print(f'Higher price flucatuation is updated for {symbol_token}')

@shared_task
def update_prices_part2(data,symbol_token,ltp):
    if(data["L_temp_low"]>ltp):
        r.hset(f"price_data:{symbol_token}",mapping={"L_temp_low":ltp,"L_temp_high":ltp})
    elif(data["L_temp_high"]<ltp):
        r.hset(f"price_data:{symbol_token}","L_temp_high",ltp)
    L_temp_low=float(r.hget(f"price_data:{symbol_token}","L_temp_low"))
    L_temp_high=float(r.hget(f"price_data:{symbol_token}","L_temp_high"))
    L_low=float(r.hget(f"price_data:{symbol_token}", "L_low"))
    L_high=float(r.hget(f"price_data:{symbol_token}", "L_high"))
    if(L_temp_high-L_temp_low > L_high-L_low):
        r.hset(f"price_data:{symbol_token}", mapping={"L_high": L_temp_high, "L_low": L_temp_low})
        print(f'Lower price flucatuation is updated for {symbol_token}')
@shared_task
def insert_data_from_redis():
    now = datetime.now().time()
    today_date = datetime.now().date()
    print("Task running at:", now)

    # --- 1) Store initial price at market open ---
    if time(9, 0) <= now <= time(9, 6):
        try:
            all_tokens = r.hgetall("all_tokens")
            for token, price in all_tokens.items():
                initial_price = float(price)

                # Insert initial price once per day (prevent duplicates)
                with connection.cursor() as cursor:
                    query = """
                        INSERT INTO price_fluctuation_data (date, token, initial_price)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE initial_price = VALUES(initial_price)
                    """
                    cursor.execute(query, [today_date, token, initial_price])

                # Run add_company only between 9:00–9:04
                if time(9, 0) <= now <= time(9, 4):
                    add_company()

                # Initialize Redis daily highs/lows
                r.hset(f"price_data:{token}", mapping={
                    "d_high": price,
                    "d_low": price
                })

        except Exception as e:
            print("Error in initial price block:", e)
            traceback.print_exc()

    # --- 2) Store intraday price data for charts ---
    if time(9, 15) <= now <= time(15, 30):
        try:
            price_time = datetime.now().strftime("%H:%M")
            all_tokens = r.hgetall("all_tokens")

            for token, price in all_tokens.items():
                price = float(price)
                with connection.cursor() as cursor:
                    query = """
                        INSERT INTO chart_price_data (company_token, price_time, price)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE price = VALUES(price)
                    """
                    cursor.execute(query, [token, price_time, price])

        except Exception as e:
            print("Error in chart update block:", e)
            traceback.print_exc()

count=0
@shared_task
def watchdog():
    try:           
        last_seen = float(r.get("ws_last_seen") or 0)
        t=datetime.now().time()
        
        now = datetime.now().timestamp()
        if time(9,15)<=t<=time(15,40):
            if now - last_seen > 90:   # no data for 30      
                main1.delay()
                
                  
                return "WebSocket inactive → Restarted main1"  
            return f"WebSocket healthy "
        return "WebSocket healthy 2"  
    except Exception as e:           
        return f"Watchdog error: {str(e)}"
@shared_task
def last_day_price():
    all_tokens=r.hgetall("all_tokens")
    for token, price in all_tokens.items():
        initial_price=float(price)
        cursor = connection.cursor()
        query="UPDATE company_data SET last_day_price= %s where symbol_token=%s"
        cursor.execute(query,[initial_price,token])






import time as t

@shared_task
def publish_live_prices_snapshot():
    """
    Read the Redis hash 'all_tokens' and publish it to the channel layer group 'live_prices_group'.
    Schedule this task (via celery beat) at the frequency you need (1s, 2s, etc).
    """
    try:
        raw = r.hgetall("all_tokens")  # { token: "price_str", ... }
        prices = {}
        for token, price in raw.items():
            try:
                prices[token] = float(price)
            except Exception:
                prices[token] = price  # fallback

        channel_layer = get_channel_layer()
        event = {
                "type": "prices_update",  # triggers consumer.user_prices_update
                "prices": prices,
            }
        async_to_sync(channel_layer.group_send)(
            "live_prices_group",
            event,
        )
        return len(prices)
    except Exception as e:
        # log or re-raise per your logging strategy
        print("publish_live_prices_snapshot error:", e)
        raise
@shared_task
def update_trades():
    user_id_list=[]
    i=0
    with connection.cursor() as cursor:
        query=""" select id from active_bot_users where is_active=%s """
        cursor.execute(query,[True,])
        rows=cursor.fetchall()
        print(rows)
        for row in rows:
            user_id_list.append(row[0])
        print(user_id_list)
    
    for id in user_id_list:
        try:
            trade_data = r.hget("user_trades",id)  
            channel_layer = get_channel_layer()
            event = {
                    "type": "send_user_trades_data",  # triggers consumer.user_prices_update
                    "prices": trade_data,
                }
            async_to_sync(channel_layer.group_send)(
                id,
                event,
            )
            return len(trade_data)
        except Exception as e:
            # log or re-raise per your logging strategy
            print("publish_live_prices_snapshot error:", e)
            raise
@shared_task
def update_price_fluctuation():
        now = datetime.now().time()
        today_date = datetime.now().date()
        try:
            all_tokens = r.hgetall("all_tokens")

            for token, price in all_tokens.items():
                final_price = float(price)

                # Update last day price
                with connection.cursor() as cursor:
                    query = "UPDATE company_data SET last_day_price=%s WHERE symbol_token=%s"
                    cursor.execute(query, [final_price, token])

                # Fetch initial price
                with connection.cursor() as cursor:
                    query = "SELECT initial_price FROM price_fluctuation_data WHERE token=%s AND date=%s"
                    cursor.execute(query, [token, today_date])
                    row = cursor.fetchone()

                if not row:
                    print(f"⚠️ No initial price found for token {token} on {today_date}")
                    continue

                i_p = float(row[0])  # Initial price from DB
                pd = r.hgetall(f"price_data:{token}")

                try:
                    high = float(pd.get("high", i_p))
                    low = float(pd.get("low", i_p))
                    L_low = float(pd.get("L_low", i_p))
                    L_high = float(pd.get("L_high", i_p))
                    d_high = float(pd.get("d_high", i_p))
                    d_low = float(pd.get("d_low", i_p))
                except Exception:
                    print(f"⚠️ Missing Redis data for token {token}")
                    continue

                # Calculate percentages
                day_high = round((d_high - i_p) * 100 / i_p, 2)
                day_low = round((d_low - i_p) * 100 / i_p, 2)
                g_up_h = round((high - i_p) * 100 / i_p, 2)
                g_up_l = round((low - i_p) * 100 / i_p, 2)
                up_gap = round((g_up_h - g_up_l), 2)
                g_down_h = round((L_high - i_p) * 100 / i_p, 2)
                g_down_l = round((L_low - i_p) * 100 / i_p, 2)
                down_gap = round((g_down_h - g_down_l), 2)
                final_percent_gain = round((final_price - i_p) * 100 / i_p, 2)
                print(f"{token} | i_p={i_p} | gain={final_percent_gain}% | up_gap={up_gap}% | down_gap={down_gap}%")
                # Update DB
                with connection.cursor() as cursor:
                    query = """
                        UPDATE price_fluctuation_data
                        SET g_up_h=%s, g_up_l=%s, up_gap=%s,
                            g_down_h=%s, g_down_l=%s, down_gap=%s,
                            final_percent_gain=%s, d_high=%s, d_low=%s
                        WHERE token=%s AND date=%s
                    """
                    cursor.execute(query, [
                        g_up_h, g_up_l, up_gap,
                        g_down_h, g_down_l, down_gap,
                        final_percent_gain, day_high, day_low,
                        token, today_date
                    ])
                t.sleep(0.5)
                

        except Exception as e:
            print("Error in final price block:", e)
            traceback.print_exc()    
        
        


        