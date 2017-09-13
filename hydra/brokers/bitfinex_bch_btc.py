# Copyright (C) 2017, Philsong <songbohr@gmail.com>
from ._bitfinex import Bitfinex
# python3 hydra/cli.py -m Bitfinex_BCH_BTC get-balance


class BrokerBitfinex_BCH_BTC(Bitfinex):  # pylint: disable=W0223

    def __init__(self, api_key=None, api_secret=None):
        super().__init__("BTC", "BCH", "bccbtc", api_key, api_secret)
