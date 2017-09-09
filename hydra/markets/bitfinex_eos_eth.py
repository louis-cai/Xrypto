# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex


class Bitfinex_EOS_ETH(Bitfinex):

    def __init__(self):
        super().__init__("ETH", "EOS", "eoseth")

