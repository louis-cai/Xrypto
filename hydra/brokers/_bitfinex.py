
from .broker import Broker
import logging
import bitfinex
import config
# python3 hydra/cli.py -m Bitfinex_BCH_BTC get-balance


class Bitfinex(Broker):  # pylint: disable=W0223

    def __init__(self, base_currency, market_currency, pair_code, api_key=None, api_secret=None):
        assert isinstance(base_currency, str)
        assert isinstance(market_currency, str)
        assert isinstance(pair_code, str)
        super().__init__(base_currency, market_currency, pair_code)
        # pylint:disable=e1101
        self.client = bitfinex.TradeClient(api_key if api_key else config.Bitfinex_API_KEY,
                                           api_secret if api_secret else config.Bitfinex_SECRET_TOKEN)

    def _buy_limit(self, amount, price):
        """Create a buy limit order"""
        res = self.client.place_order(
            str(amount),
            str(price),
            'buy',
            'exchange limit',
            symbol=self.pair_code)
        return res['order_id']

    def _sell_limit(self, amount, price):
        """Create a sell limit order"""
        res = self.client.place_order(
            str(amount),
            str(price),
            'sell',
            'exchange limit',
            symbol=self.pair_code)
        return res['order_id']

    def _order_status(self, res):
        # print(res)

        resp = {}
        resp['order_id'] = res['id']
        resp['amount'] = float(res['original_amount'])
        resp['price'] = float(res['price'])
        resp['deal_size'] = float(res['executed_amount'])
        resp['avg_price'] = float(res['avg_execution_price'])

        if res['is_live']:
            resp['status'] = 'OPEN'
        else:
            resp['status'] = 'CLOSE'

        return resp

    def _get_order(self, order_id):
        res = self.client.status_order(int(order_id))
        logging.info('get_order: %s', res)

        assert str(res['id']) == str(order_id)
        return self._order_status(res)

    def _cancel_order(self, order_id):
        res = self.client.delete_order(int(order_id))
        assert str(res['id']) == str(order_id)

        resp = self._order_status(res)
        if resp:
            return True
        else:
            return False

    def _get_balances(self):
        """Get balance"""
        res = self.client.balances()

        logging.debug("bitfinex get_balances response: %s", res)

        for entry in res:
            if entry['type'] != 'exchange':
                continue

            currency = entry['currency'].upper()
            if currency not in ('BTC', 'BCH', 'USD', 'EOS', 'ETH'):
                continue

            if currency == 'BCH':
                self.bch_available = float(entry['available'])
                self.bch_balance = float(entry['amount'])
            elif currency == 'BTC':
                self.btc_available = float(entry['available'])
                self.btc_balance = float(entry['amount'])
            elif currency == 'USD':
                self.usd_available = float(entry['available'])
                self.usd_balance = float(entry['amount'])
            elif currency == 'EOS':
                self.eos_available = float(entry['available'])
                self.eos_balance = float(entry['amount'])
            elif currency == 'ETH':
                self.eth_available = float(entry['available'])
                self.eth_balance = float(entry['amount'])
        return res
