# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex


class Bitfinex_ETH_USD(Bitfinex):

    def __init__(self):
        super().__init__("USD", "ETH", "ethusd")

