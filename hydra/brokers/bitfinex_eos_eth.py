# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex
# python3 hydra/cli.py -m Bitfinex_EOS_ETH get-balance


class BrokerBitfinex_EOS_ETH(Bitfinex):  # pylint: disable=W0223

    def __init__(self, api_key=None, api_secret=None):
        super().__init__("ETH", "EOS", "eoseth", api_key, api_secret)
