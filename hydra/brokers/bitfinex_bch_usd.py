# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex
# python3 hydra/cli.py -m Bitfinex_BCH_USD get-balance


class BrokerBitfinex_BCH_USD(Bitfinex):  # pylint: disable=W0223

    def __init__(self, api_key=None, api_secret=None):
        super().__init__("USD", "BCH", "bccusd", api_key, api_secret)
