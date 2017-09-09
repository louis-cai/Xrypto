# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex


class Bitfinex_EOS_USD(Bitfinex):

    def __init__(self):
        super().__init__("USD", "EOS", "eosusd")

