#-*- coding:utf-8 -*-s = u’示例’
# Copyright (C) 2016, Philsong <songbohr@gmail.com>

from .broker import Broker, TradeException
import time
import base64
import hmac
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import sys
import json
from lib.exchange import exchange
from lib.settings import HUOBI_API_URL
import sys
import traceback
import config
import logging

class BrokerHuobiCNY(Broker):
    def __init__(self,HUOBI_API_KEY=None, HUOBI_SECRET_TOKEN=None):
        super().__init__()
        if HUOBI_API_KEY == None:
            HUOBI_API_KEY = config.HUOBI_API_KEY
            HUOBI_SECRET_TOKEN = config.HUOBI_SECRET_TOKEN
        self.broker = exchange(HUOBI_API_URL, HUOBI_API_KEY, HUOBI_SECRET_TOKEN, 'huobi')
        self.currency = "CNY"
        self.get_info()

    def _buy(self, amount, price):
        """Create a buy limit order"""
        response = self.broker.buy(amount, price)
        if response and "code" in response:
            logging.warn("buy ex:%s", response)
            return False

        if not response:
            return response

        return response['id']

    def _sell(self, amount, price):
        """Create a sell limit order"""
        response = self.broker.sell(amount, price)
        if response and "code" in response:
            logging.warn("sell ex:%s", response)
            return False
        if not response:
            return response

        return response['id']


    def _get_order(self, order_id):
        try:
            response = self.broker.orderInfo(order_id)
        except  Exception as ex:
            logging.warn("orderInfo failed :%s" % ex)
            traceback.print_exc()
            return False

        if not response:
            return response

        if "code" in response:
            logging.warn (response)
            return False

        resp = {}
        resp['order_id'] = response['id']
        resp['amount'] = float(response['order_amount'])
        resp['price'] = float(response['order_price'])
        resp['deal_size'] = float(response['processed_amount'])
        resp['avg_price'] = float(response['processed_price'])

        status = response['status']
        if status == 3 or status == 6:
            resp['status'] = 'CANCELED'
        elif status == 2:
            resp['status'] = 'CLOSE'
        else:
            resp['status'] = 'OPEN'
        return resp

    def _cancel_order(self, order_id):
        try:
            response = self.broker.cancel(order_id)
        except  Exception as ex:
            logging.warn("cancel failed :%s" % ex)
            traceback.print_exc()
            return False

        if not response:
            return response
        if "code" in response:
            logging.warn ('%s', str(response))
            return False
        if response['result'] == 'success':
            return True
        return False

    def get_info(self):
        """Get balance"""
        try:
            response = self.broker.accountInfo()
            if response and "code" in response:
                logging.warn(response)
                return False
                raise TradeException(response["message"])
            if response:
                self.btc_balance = float(response["available_btc_display"])
                self.cny_balance = float(response["available_cny_display"])
                self.btc_frozen = float(response["frozen_btc_display"])
                self.cny_frozen = float(response["frozen_cny_display"])
        except  Exception as ex:
            logging.warn("get_info failed :%s" % ex)
            traceback.print_exc()

            return False

