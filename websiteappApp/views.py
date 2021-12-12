from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import requests
import json
from binance import Client
import datetime

def index(request):
    return render(request, 'index.html')

def trades(request):
    return render(request, 'trades.html')

def account(request):
    return render(request, 'account.html', {"data": 123})

def getAllPairs(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['all_pairs']
    res = collection.find({})
    pairs = []
    for i in res:
        pairs.append({"coin": i['coin'], "pair": i['pair']})
    return HttpResponse(json.dumps(pairs))

def postOrder(request, coin, pair, price, dec, amount, dec2, event):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['open_orders']
    coin = str({coin})
    coin = coin.strip("{}'")
    pair = str({pair})
    pair = pair.strip("{}'")
    price = str({price})
    price = price.strip("{}'")
    amount = str({amount})
    amount = amount.strip("{}'")
    dec = dec/100
    dec2 = dec2/100
    res = collection.find({})
    timeVar = datetime.datetime.now()
    ms = timeVar.strftime("%d/%m %H:%M:%S")
    index = -1
    for i in res:
        index = i['_id']
    if(event == "buy"):
        collection.insert_one({"_id": index+1, "pair": coin+pair, "price": float(price)+dec, "amount": float(amount)+dec2, "time": ms, "event": "buy"})
    else:
        collection.insert_one({"_id": index+1, "pair": coin+pair, "price": float(price)+dec, "amount": float(amount)+dec2, "time": ms, "event": "sell"})
    return render(request, 'trades.html')

def getBalance(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['balance']
    res = collection.find_one({"_id": 0})
    return HttpResponse(json.dumps(res))

def fetchTable(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['watchlist']
    api_key = '0aerC4IeFAwP8eauUrDUeDhTRk26m8i3hjsoBWavTYQzvWFLxY8ja7EjlwzCqZ7F'
    api_secret = 'eAokMAhVWEhO4eJ7j1yL91iuMfeI4gd43eKZWtHwBlijrx3SUAAU2meTun9Hawry'
    client = Client(api_key, api_secret)
    res = collection.find({})
    data = []
    for i in res:
        klines = client.get_historical_klines(i['coin']+i['pair'], Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
        for j in klines:
            data.append({"id": i['_id'], "coin": i['coin'], "pair": i['pair'], "price": "{:.3f}".format(float(j[4])), "changePrc": "{:.2f}".format(changePercent(j[1], j[4])), "changePrice": "{:.2f}".format(changePrice(j[1], j[4]))})
    return HttpResponse(json.dumps(data))

def changePercent(open, close):
    open = float(open)
    close = float(close)
    change = close - open
    ans = (change/open)*100
    return ans

def changePrice(open, close):
    open = float(open)
    close = float(close)
    return close-open

def removeTable(request, id):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['watchlist']
    id = int(id)
    try:
        collection.delete_one({"_id": id})
        return HttpResponse(True)
    except:
        return HttpResponse(False)

def fetchOpenOrders(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['open_orders']
    res = collection.find({})
    data = []
    for i in res:
        data.append({"id": i['_id'], "pair": i['pair'], "price": "{:.3f}".format(i['price']),"amount": i['amount'], "time": i['time'], "event": i['event']})
    return HttpResponse(json.dumps(data))

def removeOrders(request, id):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['open_orders']
    id = int(id)
    try:
        collection.delete_one({"_id": id})
        return HttpResponse(True)
    except:
        return HttpResponse(False)

def addFav(request,coin, pair):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['watchlist']
    api_key = '0aerC4IeFAwP8eauUrDUeDhTRk26m8i3hjsoBWavTYQzvWFLxY8ja7EjlwzCqZ7F'
    api_secret = 'eAokMAhVWEhO4eJ7j1yL91iuMfeI4gd43eKZWtHwBlijrx3SUAAU2meTun9Hawry'
    client = Client(api_key, api_secret)
    res = collection.find({})
    index = -1
    for i in res:
        index = i['_id']
    klines = client.get_historical_klines(coin+pair, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
    for i in klines:
        collection.insert_one({"_id": index+1, "coin": coin, "pair": pair, "price": "{:.3f}".format(float(i[4])), "changePrc": "{:.2f}".format(changePercent(i[1], i[4])), "changePrice": "{:.2f}".format(changePrice(i[1], i[4]))})
    return HttpResponse(0)

def updateBalance(request, tot, tal, event):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['balance']
    res = collection.find({})
    bal = 0
    for i in res:
        bal = float(i['balance'])
    tot = int(tot)
    tal = int(tal)/100
    total = tot + tal
    if(event == "buy"):
        collection.update_one({"_id": 0}, {"$set": {"balance": bal-total}})
    else:
        collection.update_one({"_id": 0}, {"$set": {"balance": bal+total}})
    return HttpResponse(True)

def checkPortfolio(request, tot, tal, coin, pair):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['portfolio']
    tot = float(tot)
    tal = float(tal)/100
    total = tot + tal
    res = collection.find({})
    for i in res:
        if(i['pair'] == coin+pair):
            if(i['amount'] >= total):
                return HttpResponse(True)
            else:
                return HttpResponse(False)
    return HttpResponse(False)

def fetchPortfolio(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['portfolio']
    api_key = '0aerC4IeFAwP8eauUrDUeDhTRk26m8i3hjsoBWavTYQzvWFLxY8ja7EjlwzCqZ7F'
    api_secret = 'eAokMAhVWEhO4eJ7j1yL91iuMfeI4gd43eKZWtHwBlijrx3SUAAU2meTun9Hawry'
    client = Client(api_key, api_secret)
    res = collection.find({})
    data = []
    for i in res:
        klines = client.get_historical_klines(i['pair'], Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
        priceNow = 0
        for j in klines:
            priceNow = j[4]
        changePrc = changePercent(i['price'], priceNow)
        changeP = changePrice(i['price'], priceNow)
        data.append({"time": i['time'], "pair": i['pair'], "price": i['price'], "amount": i['amount'], "changePrc": "{:.2f}".format(changePrc), "changeP": "{:.2f}".format(changeP)})
    return HttpResponse(json.dumps(data))

def fetchHistory(request):
    client = pymongo.MongoClient('mongodb+srv://fivosvardis:123.456.789@cluster0.74bck.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client['binVirt']
    collection = db['history_trades']
    res = collection.find({})
    data = []
    for i in res:
        data.append({"time": i['time'], "pair": i['pair'], "price": i['price'], "amount": i['amount'], "event": i['event']})
    return HttpResponse(json.dumps(data))