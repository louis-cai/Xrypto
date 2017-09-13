# Copyright (C) 2017, Philsong <songbohr@gmail.com>

from ._bitfinex import Bitfinex


class Bitfinex_BCH_USD(Bitfinex):

    def __init__(self):
        super().__init__("USD", "BCH", "bchusd")

if __name__ == "__main__":
    market = Bitfinex_BCH_USD()
    print(market.get_ticker())
