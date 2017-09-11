# Copyright (C) 2017, Phil Song <songbohr@gmail.com>

# pylint: disable=E0401,E1101,W1201
# python3 hydra/cli.py -m Bitfinex_EOS_USD,Bitfinex_EOS_ETH,Bitfinex_ETH_USD t-watch -v
# python3 hydra/cli.py -m Bitfinex_EOS_USD,Bitfinex_EOS_ETH,Bitfinex_ETH_USD t-watch-bitfinex-eos -v
import logging
import time
import config
from arbitrer import Arbitrer
from brokers import bitfinex_eos_usd, bitfinex_eos_eth, bitfinex_eth_usd


class TrigangularArbitrer_Bitfinex(Arbitrer):

    def __init__(self, base_pair, pair1, pair2, monitor_only=True):
        super().__init__()
        self.base_pair = base_pair or 'Bitfinex_EOS_USD'
        self.pair_1 = pair1 or 'Bitfinex_EOS_ETH'
        self.pair_2 = pair2 or 'Bitfinex_ETH_USD'

        self.monitor_only = monitor_only

        t_api_key = config.t_Bitfinex_API_KEY
        t_secret_token = config.t_Bitfinex_SECRET_TOKEN

        self.clients = {
            self.base_pair: bitfinex_eos_usd.BrokerBitfinex_EOS_USD(t_api_key, t_secret_token),
            self.pair_1: bitfinex_eos_eth.BrokerBitfinex_EOS_ETH(t_api_key, t_secret_token),
            self.pair_2: bitfinex_eth_usd.BrokerBitfinex_ETH_USD(t_api_key, t_secret_token),
        }

        self.last_trade = 0

    def update_balance(self):
        self.clients[self.base_pair].get_balances()

    def tickers(self):
        pass

    def observer_tick(self):
        # logging.verbose('%s' % str({"usd_balance": self.clients[self.base_pair].usd_balance,
        #                             "usd_available": self.clients[self.base_pair].usd_available,
        #                             "eos_balance": self.clients[self.base_pair].eos_balance,
        #                             "eos_available": self.clients[self.base_pair].eos_available,
        #                             "eth_balance": self.clients[self.base_pair].eth_balance,
        #                             "eth_available": self.clients[self.base_pair].eth_available}))
        self.forward()
        self.reverse()

    def forward(self):
        logging.verbose("------------------- t3 forward: -------------------")
        base_pair_ask_amount = self.depths[self.base_pair]["asks"][0]["amount"]
        base_pair_ask_price = self.depths[self.base_pair]["asks"][0]["price"]

        logging.verbose("base_pair: %s ask_price:%s" % (self.base_pair, base_pair_ask_price))

        pair1_bid_amount = self.depths[self.pair_1]["bids"][0]["amount"]
        pair1_bid_price = self.depths[self.pair_1]["bids"][0]["price"]

        pair2_bid_amount = self.depths[self.pair_2]["bids"][0]["amount"]
        pair2_bid_price = self.depths[self.pair_2]["bids"][0]["price"]

        if pair1_bid_price == 0:
            return

        pair_2to1_eos_amount = pair2_bid_amount / pair1_bid_price
        # print(pair2_bid_amount, pair1_bid_price, pair_2to1_eos_amount)

        max_trade_amount = config.eos_max_tx_volume
        hedge_eos_amount = min(base_pair_ask_amount, pair1_bid_amount)
        hedge_eos_amount = min(hedge_eos_amount, pair_2to1_eos_amount)
        hedge_eos_amount = min(hedge_eos_amount, max_trade_amount)

        if hedge_eos_amount < 0.002:
            logging.verbose('hedge_ EOS _amount is too small! %0.5f' % hedge_eos_amount)
            logging.verbose('base_pair_ask_amount @%s pair1_bid_amount @%s pair_2to1_eos_amount @%s max_trade_amount @%s' %
                            (base_pair_ask_amount, pair1_bid_amount, pair_2to1_eos_amount, max_trade_amount))
            return

        hedge_eth_amount = hedge_eos_amount * pair1_bid_price
        if hedge_eth_amount < 0.01:
            logging.verbose('hedge_ ETH _amount is too small! @%0.5f:%s' % (hedge_eth_amount, pair1_bid_price))
            logging.verbose('base_pair_ask_amount @%s pair1_bid_amount @%s pair_2to1_eos_amount @%s max_trade_amount @%s' %
                            (base_pair_ask_amount, pair1_bid_amount, pair_2to1_eos_amount, max_trade_amount))
            return

        synthetic_bid_price = round(pair1_bid_price * pair2_bid_price, 4)

        t_price = round(base_pair_ask_price * config.TFEE * config.Diff, 4)
        logging.verbose("synthetic_bid_price: %s t_price:%s" % (synthetic_bid_price, t_price))

        p_diff = synthetic_bid_price - t_price
        profit = p_diff * hedge_eos_amount

        if profit > 0:
            logging.info('[forward] profit=%0.4f, p_diff=%0.4f, EOS @%s' % (profit, p_diff, hedge_eos_amount))
            logging.info("[forward] synthetic_bid_price: %s  base_pair_ask_price: %s t_price: %s" % (
                synthetic_bid_price, 
                base_pair_ask_price,
                t_price))

            logging.info('[forward] --buy %s EOS @%s, sell ETH @synthetic: %s' % (self.base_pair, hedge_eos_amount, hedge_eth_amount))
            if profit < 1:
                logging.warning('profit should >= 1 USD')
                return

            current_time = time.time()
            if current_time - self.last_trade < 5:
                logging.warning("Can't automate this trade, last trade " +
                                "occured %.2f seconds ago" %
                                (current_time - self.last_trade))
                return

            if not self.monitor_only:
                self.clients[self.base_pair].buy_limit(hedge_eos_amount, base_pair_ask_price)
                self.clients[self.pair_1].sell_limit(hedge_eos_amount, pair1_bid_price)
                self.clients[self.pair_2].sell_limit(hedge_eth_amount, pair2_bid_price)

            self.last_trade = time.time()

    def reverse(self):
        logging.verbose("------------------- t3 reverse: -------------------")

        base_pair_bid_amount = self.depths[self.base_pair]["bids"][0]["amount"]
        base_pair_bid_price = self.depths[self.base_pair]["bids"][0]["price"]

        logging.verbose("base_pair: %s bid_price:%s" % (self.base_pair, base_pair_bid_price))

        pair1_ask_amount = self.depths[self.pair_1]["asks"][0]["amount"]
        pair1_ask_price = self.depths[self.pair_1]["asks"][0]["price"]

        pair2_ask_amount = self.depths[self.pair_2]["asks"][0]["amount"]
        pair2_ask_price = self.depths[self.pair_2]["asks"][0]["price"]

        if pair1_ask_price == 0 or pair2_ask_price == 0:
            return

        pair_2to1_eos_amount = pair2_ask_amount / pair1_ask_price
        # print(pair2_bid_amount, pair1_bid_price, pair_2to1_eos_amount)

        max_trade_amount = config.eos_max_tx_volume
        hedge_eos_amount = min(base_pair_bid_amount, pair1_ask_amount)
        hedge_eos_amount = min(hedge_eos_amount, pair_2to1_eos_amount)
        hedge_eos_amount = min(hedge_eos_amount, max_trade_amount)

        if hedge_eos_amount < 0.002:
            logging.verbose('hedge_ EOS _amount is too small! %s' % hedge_eos_amount)
            logging.verbose('base_pair_bid_amount @%s pair1_ask_amount @%s pair_2to1_eos_amount @%s max_trade_amount @%s' %
                            (base_pair_bid_amount, pair1_ask_amount, pair_2to1_eos_amount, max_trade_amount))
            return

        hedge_eth_amount = hedge_eos_amount * pair1_ask_price
        if hedge_eth_amount < 0.001:
            logging.verbose('hedge_ ETH _amount is too small! @%s:%s' % (hedge_eth_amount, pair1_ask_price))
            logging.verbose('base_pair_bid_amount @%s pair1_ask_amount @%s pair_2to1_eos_amount @%s max_trade_amount @%s' %
                            (base_pair_bid_amount, pair1_ask_amount, pair_2to1_eos_amount, max_trade_amount))
            return

        synthetic_ask_price = round(pair1_ask_price * pair2_ask_price, 4)

        t_price = round(base_pair_bid_price * config.TFEE * config.Diff, 4)
        logging.verbose("synthetic_ask_price: %s t_price:%s" % (synthetic_ask_price, t_price))

        p_diff = synthetic_ask_price - t_price
        profit = round(p_diff * hedge_eos_amount, 4)

        if profit > 0:
            logging.info('[reverse] profit=%0.4f, p_diff=%0.4f, EOS @%s' % (profit, p_diff, hedge_eos_amount))
            logging.info("[reverse] find t!!!: p_diff:%s synthetic_ask_price: %s  base_pair_bid_price: %s t_price: %s" % (
                p_diff,
                synthetic_ask_price, 
                base_pair_bid_price,
                t_price))

            logging.info('[reverse] sell %s EOS @%s, buy @synthetic: %s' % (self.base_pair, hedge_eos_amount, hedge_eth_amount))
            if profit < 1:
                logging.warning('profit should >= 1 USD')
                return

            current_time = time.time()
            if current_time - self.last_trade < 10:
                logging.warning("Can't automate this trade, last trade " +
                                "occured %.2f seconds ago" %
                                (current_time - self.last_trade))
                return

            self.clients[self.base_pair].sell_limit(hedge_eos_amount, base_pair_bid_price)
            self.clients[self.pair_2].buy_limit(hedge_eth_amount, pair2_ask_price)
            self.clients[self.pair_1].buy_limit(hedge_eos_amount, pair1_ask_price)

            self.last_trade = time.time()



