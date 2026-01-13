from django.http import HttpResponse, JsonResponse;
from django.shortcuts import render,redirect;
from django.db import connection;
from users.views import RegisterView, LoginView
from celery import shared_task
import requests,json,csv,os
import pandas as pd  
import matplotlib.pyplot as plt
import plotly.express as px
from .angel_one_services import AngelOneService
from datetime import datetime,time,timedelta
from .tasks import redis_client
from collections import defaultdict
r = redis_client


def homePage(request):
    return render(request,'index.html')
    
def holdings(request):
    return render(request,'Holdings.html')


def download_csv(request):
    url = "https://margincalculator.angelone.in/OpenAPI_File/files/OpenAPIScripMaster.json"
    file_path = "filtered_scrip_master.csv"  # Save file in Django root directory

    # Check if the file exists and its last modified time
    if os.path.exists(file_path):
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"Last modified: {last_modified_time}")

    print("Downloading OpenAPIScrip...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        # Filter the required data
        filtered_data = [
            row for row in json_data
            if row.get("exch_seg") in ["NSE", "BSE"] and row.get("instrumenttype") == "" and row.get("expiry") == ""
        ]

        # Save or update the file
        with open(file_path, mode="w", newline="") as file:
            csv_writer = csv.writer(file)

            # Write header
            if filtered_data:
                csv_writer.writerow(filtered_data[0].keys())

            # Write filtered data rows
            for row in filtered_data:
                csv_writer.writerow(row.values())
        message=f"File updated successfully at {file_path}"
        data={'message':message,'status':"200"}
        return JsonResponse(data)

    except requests.exceptions.RequestException as e:
        message=f"Error fetching data: {e}"
        data={'message':f"Error fetching data: {e}",'status':"500"}
        return JsonResponse(data)
    
def search_scrips(request):
    if request.method == "POST":
        search_query = request.POST.get("search_queries", "").strip().lower()  # Get a single input
        file_path = "filtered_scrip_master.csv"
        results = []

        if not search_query:  # Ensure input is not empty
            return render(request, "placeOrders.html", {"error": "Please enter a valid stock symbol or name."})

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    symbol = row.get("symbol", "").lower()
                    name = row.get("name", "").lower()
                    token = row.get("token", "")

                    if search_query in symbol or search_query in name:
                        results.append({"symbol": row["symbol"], "name": row["name"], "token": token, "exch_seg": row.get("exch_seg", "")})

            return render(request, "placeOrders.html", {"results": results})

        except FileNotFoundError:
            return render(request, "placeOrders.html", {"error": "CSV file not found. Please upload it first."})
        except Exception as e:
            return render(request, "placeOrders.html", {"error": f"An error occurred: {str(e)}"})

    return render(request, "placeOrders.html")
def live_price_loop(request):
         
   # Get all token-price pairs stored in Redis hash "all_tokens"
    # Example result: {'24308': '510.75', '27052': '314.20'}
    all_tokens = r.hgetall("all_tokens")
    # Create a new dictionary with prices converted from string to float
    prices = {}
    for token, price in all_tokens.items():
        prices[token] = float(price)
    # Return the prices as a JSON response
    return JsonResponse(prices)






def get_token_price_lists1():
    cursor = connection.cursor()
    query = """
        SELECT company_token, price_time, price
        FROM chart_price_data
        WHERE price_time BETWEEN '09:15' AND '15:30'
        ORDER BY company_token, price_time
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    token_data = defaultdict(list)

    for token, price_time, price in rows:
        token_data[token].append(float(price))
    
    for i, (token, prices) in enumerate(token_data.items()):
        if i >= 5:
            break
        print(f"Token: {token}, Prices: {prices}")


def update_chart_array(request, token):
    # Define trading session range
    start_time = time(9, 15)
    end_time = time(15, 30)

    # Build all minute slots (from 09:15 → 15:30)
    slots = []
    t = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    while t <= end_dt:
        slots.append(t.strftime("%H:%M"))
        t += timedelta(minutes=1)

    # Fetch prices for given token
    cursor = connection.cursor()
    query = """
        SELECT price_time, price
        FROM chart_price_data
        WHERE company_token = %s
        ORDER BY price_time
    """
    cursor.execute(query, [token])
    rows = cursor.fetchall()

    # ✅ Normalize price_time to string format ("HH:MM") for consistency
    price_dict = {pt.strftime("%H:%M"): float(price) for pt, price in rows}

    # Fill list with price till now, and null for remaining
    now = datetime.now().strftime("%H:%M")
    price_list = []
    for slot in slots:
        if slot <= now:
            price_list.append(price_dict.get(slot, None))  # price if exists, else None
        else:
            price_list.append(None)
    
# 🔹 Fetch today's initial price
    
    cursor.execute("""
        SELECT last_day_price
        FROM company_data
        WHERE symbol_token = %s 
        LIMIT 1
    """, [token, ])
    row = cursor.fetchone()
    if row:
        price_list[0] = float(row[0])
    return JsonResponse({
        "token": token,
        "prices": price_list
    })

def check_price_update():
    prices=r.hget("all_tokens","8727")
    print("new Price after 0.5 second")
    print(prices,end=" ")
import time as t
def call_in():
    i=1
    while i<2:
        check_price_update()
        t.sleep(0.5)
    

           
        
      