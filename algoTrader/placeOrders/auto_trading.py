from django.test import TestCase
from users.models import CustomUser
import pyotp,copy,time
import threading
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from cryptography.fernet import Fernet
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import StartTrading
from django.db import connection;
from django.http import JsonResponse
from SmartApi.smartConnect import SmartConnect
import logging
from algoTrader.utils.redis_client import RedisClient
import threading
from  algoTrader.tasks import redis_client
from datetime import datetime, timedelta,date

logger = logging.getLogger(__name__)
today_date = datetime.now().date()
r=redis_client
all_company_prices=r.hgetall("all_tokens")


def start_condition():
    default_condition = {
        "initial_price": 0,
        "total_quantity": 0,
        "last_trade_percent": 0,
        "amount_used": 0,
        "average_price": 0,
        "profit": 0,
    }
    # list of tokens (strings). Use list or set — final dict keys will be strings.
    token_list = [
        "757772","756038","547","5258","5097","509","4749","383","3787","3761",
        "3063","3024","2955","29251","27176","27097","2303","220","18143",
        "17433","14366","14334","1363","12018","11536","10440"
    ]
    trading_dictionary = {token: default_condition.copy() for token in token_list}
    return trading_dictionary
def check_credentials(request):
    user=request.user
    id=str(user.id)+user.client_code
    with connection.cursor() as cursor:
        query="""select count(id),is_active from active_bot_users where id=%s """
        cursor.execute(query,[id,])
        rows=cursor.fetchone()
        user_id=rows[0]
        is_active=rows[1]
        if(is_active!=1):
            # view=start_trading()
            # response=view.get(request)
            # return response
            return JsonResponse({"status":False,"data":'activate trading bot '})
        else:
            return JsonResponse({"status":True,'data':'trading bot activated'})
    print(user)
    print(id)
    return JsonResponse({'data':'I am ready to send data'})
def deactivate(request):
    user=request.user
    id=str(user.id)+user.client_code
    with connection.cursor() as cursor:
        query="""Update active_bot_users set is_active=%s where  id=%s """
        cursor.execute(query,[False,id])
    return JsonResponse({"status":'Trading bot is deactivated'})
class start_trading(View):
    @method_decorator(ensure_csrf_cookie, name='dispatch')
    def get(self, request):
        print(request.user.username)
        print(request.user.id)
        form = StartTrading()
        # return render(request, 'templates/trading_bot.html', {'form': form})
        # Render just the form HTML as string
        html = render_to_string('templates/trading_bot.html', {'form': form}, request=request)
        return JsonResponse({'html': html})
        

    def post(self, request):
        print('i got request ')
        form = StartTrading(request.POST)
        print('from form i got the datas')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            trad_type=form.cleaned_data.get('trading_type')
            print(trad_type)

            try:
                user = CustomUser.objects.get(username=username, email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid credentials.")
                return render(request, 'templates/trading_bot.html', {'form': form})

            if not user.check_password(password):
                messages.error(request, "Invalid password.")
                return render(request, 'templates/trading_bot.html', {'form': form})

            if not user.is_email_verified:
                messages.error(request, "Email not verified. Please verify your OTP.")
                request.session['pending_user_id'] = user.id
                return redirect('verify_otp')

            # login user
            login(request, user)
            messages.success(request, "Login successful!")

            # ✅ Fetch and decrypt AngelOne credentials
            api_key = user.get_decrypted_field('api_key')
            secret_key = user.get_decrypted_field('secret_key')
            client_code = user.client_code  # (this one isn't encrypted)
            angelone_password = user.get_decrypted_field('angelone_password')
            user_id=str(request.user.id)+request.user.client_code
            with connection.cursor() as cursor:
                query="""select count(id),is_active from active_bot_users where id=%s """
                cursor.execute(query,[user_id,])
                rows=cursor.fetchone()
                count=rows[0]
                is_active=rows[1]
                if(count==0):
                    user_id_id=request.user.id
                    query2=""" insert into active_bot_users(id,date_of_activation,activation_time,is_active,user_id_id) values (%s,%s,%s,%s,%s);"""
                    cursor.execute(query2,[user_id,date.today(),datetime.now().time(),True,user_id_id])
                else:
                    user_id_id=request.user.id
                    query3="""update active_bot_users set date_of_activation=%s, activation_time=%s,is_active=%s where id=%s;"""
                    cursor.execute(query3,[date.today(),datetime.now().time(),True,user_id])
                self.tokens = copy.deepcopy(start_condition())

            print("API Key:", api_key)
            print("Secret Key:", secret_key)
            print("Client Code:", client_code)
            print("AngelOne Password:", angelone_password)
            # user=activate_trading_bot(api_key,secret_key,client_code,angelone_password)
            # return redirect('home')
            return JsonResponse({'success': True, 'message': "Trading bot activated!"})

        return render(request, 'templates/trading_bot.html', {'form': form})

# Create your tests here.
class activate_trading_bot:
    def __init__(self, API_KEY, TOTP_SECRET, CLIENT_CODE, PASSWORD):
        # SmartAPI login (unchanged)
        self.smartApi = SmartConnect(api_key=API_KEY)
        self.totp = pyotp.TOTP(TOTP_SECRET)
        self.totp_code = self.totp.now()
        self.data = self.smartApi.generateSession(CLIENT_CODE, PASSWORD, self.totp_code)
        if not self.data.get('status'):
            raise RuntimeError("Failed to login to Angel One: " + str(self.data))
        self.jwt_token = self.data['data']['jwtToken']
        self.refresh_token = self.data['data']['refreshToken']
        self.feed_token = self.smartApi.getfeedToken()
        self.last_login = datetime.now()
        logger.info("Successfully logged in to Angel One")

        # local tokens copy (independent)
        self.tokens = copy.deepcopy(start_condition())
        print("calling set initial method ")
        self.set_initial_price(self.tokens)
        print("called set initial method ")
        self._thread=threading.Thread(target=self.call_check_requirements,args=(self.tokens,),daemon=True)
        self._thread.start()
    
    def call_check_requirements(self,tokens):
        while True:
            self.check_requirements(tokens,all_company_prices)
            time.sleep(1)

    def set_initial_price(self, tokens):
        """Populate initial_price from DB for each token (run once)."""
        for token, values in tokens.items():
            with connection.cursor() as cursor:
                query = "SELECT initial_price FROM price_fluctuation_data WHERE token=%s AND date=%s"
                cursor.execute(query, [token, '2025-10-17'])
                row = cursor.fetchall()
            if not row:
                logger.warning("No initial price found for token %s on %s", token,today_date )
                continue
            try:
                values['initial_price'] = float(row[0][0])
            except Exception:
                logger.exception("Invalid DB value for token %s: %s", token, row)
        # return tokens or leave in-place

    def check_requirements(self, tokens, all_company_prices):
        """
        tokens: dict[token] -> values dict
        all_company_prices: mapping from token string to string price from Redis
        """
        print("i called and its working")
        for token, values in tokens.items():
            try:
                # fetch final price from redis snapshot
                final_price_str = all_company_prices.get(str(token))
                if final_price_str is None:
                    logger.debug("No price in redis for token %s", token)
                    continue
                final_price = float(final_price_str)

                initial_price = float(values.get('initial_price', 0))
                if initial_price == 0:
                    # skip tokens without an initial price
                    continue

                per_change = ((final_price - initial_price) / initial_price) * 100

                # CASE A: first entry (no quantity)
                if values["total_quantity"] == 0 and per_change >= 5:
                    ip = initial_price
                    if ip <= 50:
                        qty = 10
                    elif ip <= 100:
                        qty = 6
                    elif ip <= 150:
                        qty = 4
                    elif ip <= 200:
                        qty = 3
                    elif ip <= 300:
                        qty = 2
                    elif ip <= 600:
                        qty = 1
                    elif ip <= 1000 and per_change >= 6:
                        qty = 1
                    elif ip <= 1500 and per_change >= 6.5:
                        qty = 1
                    elif ip <= 2000 and per_change >= 6.5:
                        qty = 1
                    else:
                        qty = 0

                    if qty > 0:
                        values['total_quantity'] = qty
                        values['average_price'] = final_price
                        values['last_trade_percent'] = per_change
                        values['amount_used'] = final_price * qty
                        logger.info("Token %s initial buy qty=%s at price=%s", token, qty, final_price)
                        print(token,values)

                # CASE B: already have quantity -> check for further scaling
                elif values["total_quantity"] != 0 and (per_change - values['last_trade_percent']) >= 1.1:
                    # small rebalancing rule
                    if per_change <= 10:
                        # updating average price: current average weighted with existing quantity and new price*existing quantity?
                        # NOTE: fix logic to compute new average properly — currently unclear; example below:
                        prev_qty = values['total_quantity']
                        prev_avg = values['average_price']
                        # if doubling quantity by adding same quantity, new avg = (prev_avg*prev_qty + final_price*prev_qty) / (prev_qty*2)
                        new_qty = prev_qty * 2
                        new_avg = (prev_avg * prev_qty + final_price * prev_qty) / new_qty
                        values['average_price'] = new_avg
                        values['last_trade_percent'] = per_change
                        values['amount_used'] = values['amount_used'] + final_price * prev_qty
                        values['total_quantity'] = new_qty
                        logger.info("Token %s scaled to qty=%s avg_price=%s", token, new_qty, new_avg)
                    elif per_change > 10 and per_change <= 16 and (per_change - values['last_trade_percent']) >= 1.5:
                        # similar handling for this band
                        prev_qty = values['total_quantity']
                        new_qty = prev_qty * 2
                        prev_avg = values['average_price']
                        new_avg = (prev_avg * prev_qty + final_price * prev_qty) / new_qty
                        values['average_price'] = new_avg
                        values['last_trade_percent'] = per_change
                        values['amount_used'] = values['amount_used'] + final_price * prev_qty
                        values['total_quantity'] = new_qty
                        logger.info("Token %s scaled (band) to qty=%s", token, new_qty)
                # else: nothing to do for this token this tick
            except Exception:
                logger.exception("Error processing token %s", token)

def call_check_requirements(tokens):
        while True:
            check_requirements(tokens,all_company_prices)
            time.sleep(1)
def set_initial_price(user_id, tokens):
        """Populate initial_price from DB for each token (run once)."""
        for token, values in tokens.items():
            with connection.cursor() as cursor:
                query = "SELECT initial_price FROM price_fluctuation_data WHERE token=%s AND date=%s"
                cursor.execute(query, [token, '2025-10-17'])
                row = cursor.fetchall()
            if not row:
                logger.warning("No initial price found for token %s on %s", token,today_date )
                continue
            try:
                values['initial_price'] = float(row[0][0])
            except Exception:
                logger.exception("Invalid DB value for token %s: %s", token, row)

def check_requirements(user_id, tokens, all_company_prices):
    """
    tokens: dict[token] -> values dict
    all_company_prices: mapping from token string to string price from Redis
    """
    print("i called and its working")
    for token, values in tokens.items():
        try:
            # fetch final price from redis snapshot
            final_price_str = all_company_prices.get(str(token))
            if final_price_str is None:
                logger.debug("No price in redis for token %s", token)
                continue
            final_price = float(final_price_str)

            initial_price = float(values.get('initial_price', 0))
            if initial_price == 0:
                # skip tokens without an initial price
                continue

            per_change = ((final_price - initial_price) / initial_price) * 100

            # CASE A: first entry (no quantity)
            if values["total_quantity"] == 0 and per_change >= 5:
                ip = initial_price
                if ip <= 50:
                    qty = 10
                elif ip <= 100:
                    qty = 6
                elif ip <= 150:
                    qty = 4
                elif ip <= 200:
                    qty = 3
                elif ip <= 300:
                    qty = 2
                elif ip <= 600:
                    qty = 1
                elif ip <= 1000 and per_change >= 6:
                    qty = 1
                elif ip <= 1500 and per_change >= 6.5:
                    qty = 1
                elif ip <= 2000 and per_change >= 6.5:
                    qty = 1
                else:
                    qty = 0

                if qty > 0:
                    values['total_quantity'] = qty
                    values['average_price'] = final_price
                    values['last_trade_percent'] = per_change
                    values['amount_used'] = final_price * qty
                    logger.info("Token %s initial buy qty=%s at price=%s", token, qty, final_price)
                    print(token,values)

            # CASE B: already have quantity -> check for further scaling
            elif values["total_quantity"] != 0 and (per_change - values['last_trade_percent']) >= 1.1:
                # small rebalancing rule
                if per_change <= 10:
                    # updating average price: current average weighted with existing quantity and new price*existing quantity?
                    # NOTE: fix logic to compute new average properly — currently unclear; example below:
                    prev_qty = values['total_quantity']
                    prev_avg = values['average_price']
                    # if doubling quantity by adding same quantity, new avg = (prev_avg*prev_qty + final_price*prev_qty) / (prev_qty*2)
                    new_qty = prev_qty * 2
                    new_avg = (prev_avg * prev_qty + final_price * prev_qty) / new_qty
                    values['average_price'] = new_avg
                    values['last_trade_percent'] = per_change
                    values['amount_used'] = values['amount_used'] + final_price * prev_qty
                    values['total_quantity'] = new_qty
                    logger.info("Token %s scaled to qty=%s avg_price=%s", token, new_qty, new_avg)
                elif per_change > 10 and per_change <= 16 and (per_change - values['last_trade_percent']) >= 1.5:
                    # similar handling for this band
                    prev_qty = values['total_quantity']
                    new_qty = prev_qty * 2
                    prev_avg = values['average_price']
                    new_avg = (prev_avg * prev_qty + final_price * prev_qty) / new_qty
                    values['average_price'] = new_avg
                    values['last_trade_percent'] = per_change
                    values['amount_used'] = values['amount_used'] + final_price * prev_qty
                    values['total_quantity'] = new_qty
                    logger.info("Token %s scaled (band) to qty=%s", token, new_qty)
            # else: nothing to do for this token this tick
        except Exception:
            logger.exception("Error processing token %s", token)




