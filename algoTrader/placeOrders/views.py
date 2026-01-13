from django.shortcuts import render
from pprint import pprint
import requests
from algoTrader.angel_one_services import AngelOneService  # Import your service class
from django.views.decorators.csrf import csrf_exempt
import json,csv,os
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.db import connection; 
angel_services=AngelOneService.get_instance()
API_KEY = angel_services.API_KEY
CLIENT_ID = angel_services.CLIENT_CODE
FEED_TOKEN = angel_services.feed_token

# def home(request):
#     return render(request,"index.html")
def companies_data(request):
    try:
        if request.method =='POST':
            company_name=request.POST.get('company_name')
            symbol_name=request.POST.get('symbol_name')
            symbol_token=request.POST.get('symbol_token')
            market_cap=request.POST.get('mkt_cap')
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO company_data (company_name, symbol_name, symbol_token, market_capitalization) VALUES (%s, %s, %s, %s)",
                       [company_name, symbol_name, symbol_token, market_cap])
        connection.commit()
        cursor.close()
         

    except:
        pass
    return render(request,"placeOrders.html")
def get_symbol_tokens():
    cursor = connection.cursor()
    cursor.execute("SELECT company_name ,symbol_token FROM company_data")
    # fetchall() returns a list of tuples → [(token1,), (token2,), ...]
    rows = cursor.fetchall()
    cursor.close()
    
    
    company_name=[row[0] for row in rows]
    symbol_tokens = [row[1] for row in rows]
    print(company_name)
    print(symbol_tokens)
     


def place_order(request):
    print(f"Request method: {request.method}")

    if request.method == 'POST':
        data = json.loads(request.body)
        symbol = data.get('symbol')
        limit_price = data.get('limit_price')

        print(f"Received order for {symbol} at limit price {limit_price}")

        return JsonResponse({"message": f"Order placed for {symbol} at {limit_price}"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def top_30_last_day_losers(request):
    with connection.cursor() as cursor:
        query = """
            SELECT DISTINCT date 
            FROM price_fluctuation_data
            WHERE final_percent_gain IS NOT NULL 
            AND date != CURDATE()
            ORDER BY date DESC 
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()  # returns a tuple, e.g. (datetime.date(2025, 10, 31),)
        if result:
            latest_date = result[0]  # extract the actual date object
            formatted_date = latest_date.strftime('%Y-%m-%d')  # convert to string for SQL
            print(formatted_date)  # output → '2025-10-31'
        query1=""" SELECT  distinct c.company_name ,p.g_up_h,p.g_up_l,p.up_gap,p.g_down_h,p.g_down_l,p.down_gap,p.final_percent_gain 
                    FROM company_data as c join price_fluctuation_data as p ON c.symbol_token = p.token WHERE (p.d_high<%s and p.d_high>%s and p.d_low>%s and p.d_low<%s)  and date=%s order by p.final_percent_gain asc limit %s"""
        cursor.execute(query1,[25,-10,-20,25,formatted_date,30])
        rows=cursor.fetchall()
        columns = ['g_up_h', 'g_up_l', 'up_gap', 'g_down_h', 'g_down_l', 'down_gap', 'final_percent_gain']
        data = {}
        for row in rows:
            company_name = row[0]           # first column
            values = row[1:]                # rest of the columns
            company_data = dict(zip(columns, values))  # make dict
            data[company_name] = company_data

    return JsonResponse(data)

def top_30_last_day_gainers(request):

    with connection.cursor() as cursor:
        query = """
            SELECT DISTINCT date 
            FROM price_fluctuation_data
            WHERE final_percent_gain IS NOT NULL 
            AND date != CURDATE()
            ORDER BY date DESC 
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()  # returns a tuple, e.g. (datetime.date(2025, 10, 31),)
        if result:
            latest_date = result[0]  # extract the actual date object
            formatted_date = latest_date.strftime('%Y-%m-%d')  # convert to string for SQL
            print(formatted_date)  # output → '2025-10-31'
        query1=""" SELECT  distinct c.company_name ,p.g_up_h,p.g_up_l,p.up_gap,p.g_down_h,p.g_down_l,p.down_gap,p.final_percent_gain 
                    FROM company_data as c join price_fluctuation_data as p ON c.symbol_token = p.token WHERE (p.d_high<%s and p.d_high>%s and p.d_low>%s and p.d_low<%s)  and date=%s order by p.final_percent_gain desc limit %s"""
        cursor.execute(query1,[25,-10,-20,25,formatted_date,30])
        rows=cursor.fetchall()
        columns = ['g_up_h', 'g_up_l', 'up_gap', 'g_down_h', 'g_down_l', 'down_gap', 'final_percent_gain']
        data = {}
        for row in rows:
            company_name = row[0]           # first column
            values = row[1:]                # rest of the columns
            company_data = dict(zip(columns, values))  # make dict
            data[company_name] = company_data

    return JsonResponse(data)

    

def last_day_gainers(request):
    return render(request, 'templates/last_day_gainers.html')

def news(request):
    return render(request, 'templates/news.html')
def trading_bot(request):
    return render(request , 'templates/trading_bot.html')




            

        

                         
                          
                   
