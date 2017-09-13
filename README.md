# opportunity detector and automated trading


It gets order books from supported exchanges and calculate arbitrage and triangular-arbitrage
opportunities between each markets. It takes market depth into account.

Currently supported exchanges to get/feed data:
 - Bitfinex (BCH_BTC)
 - Bitfinex (BTC_USD)
 - Bittrex (BCH_BTC)
 - Viabtc (BCH_BTC)
 - Viabtc (BTC_CNY)
 - Viabtc (BCH_CNY)
 - Bitstamp (USD)
 - BTC-e (USD)
 - OkCoin (CNY)
 - Huobi (CNY)
 - Broker (CNY)
 - Bitstar (Future)
 - OKEx (Future)
 - Yunbi (CNY)
 - Jubi (CNY)
 - Binance

Currently supported exchanges to automate trade:
 - Bitfinex (BCH_BTC)
 - Bitfinex (BTC_USD)
 - Bittrex (BCH_BTC)
 - Viabtc (BCH_BTC)
 - Viabtc (BTC_CNY)
 - Viabtc (BCH_CNY)
 - Bitstamp (USD)
 - OkCoin (CNY)
 - Huobi (CNY)
 - Bitstar (Future)
 - OkEx (Future)
 - Yunbi (CNY)
 - Jubi (CNY)
 - Binance

# WARNING

**Real trading bots are included. Don't put your API keys in config.py
  if you don't know what you are doing.**

# Installation And Configuration

Create and edit local_config.py file to setup your preferences: watched markets
and observers and keys.The config field in local_config.py will override those keys in config.py

You need Python3 to run this program. To install on Debian, Ubuntu, or
variants of them, use:

    sudo apt-get install python3 python3-pip python-nose
    pip3 install -r requirements.txt

You need market broker service, please read its README to install then run it. 
  
    https://github.com/philsong/bitcoin-broker 

To connect the broker server you will need to install thriftpy:

    pip3 install cython thriftpy

To use the observer XMPPMessager you will need to install sleekxmpp:

    pip3 install sleekxmpp

# Debug

    python3 hydra/cli.py watch -d

# Run

To run the opportunity watcher:

    python3 hydra/cli.py watch -v

To check your balance on an exchange (also a good way to check your accounts configuration):

    python3 hydra/cli.py -m HaobtcCNY get-balance
    python3 hydra/cli.py -m Viabtc_BCH_CNY get-balance
    python3 hydra/cli.py -m Bitfinex_BCH_BTC get-balance
    python3 hydra/cli.py -m Bitfinex_BCH_BTC,Bittrex_BCH_BTC,Viabtc_BCH_BTC get-balance
    python3 hydra/cli.py -m HaobtcCNY,OkCoinCNY,HuobiCNY get-balance

Run t-arbitrage

    python3 hydra/cli.py -m Viabtc_BCH_CNY,Viabtc_BCH_BTC,Viabtc_BTC_CNY t-watch-viabtc-bcc -v
    python3 hydra/cli.py -m Binance_WTC_BTC,Binance_WTC_ETH,Binance_ETH_BTC t-watch-binance-wtc -v
    python3 hydra/cli.py -m Binance_BNB_BTC,Binance_BNB_ETH,Binance_ETH_BTC t-watch-binance-bnb -v
    python3 hydra/cli.py -m Binance_LRC_BTC,Binance_LRC_ETH,Binance_ETH_BTC t-watch-binance-lrc -v
    python3 hydra/cli.py -m Binance_MCO_BTC,Binance_MCO_ETH,Binance_ETH_BTC t-watch-binance-mco -v
    python3 hydra/cli.py -m Binance_QTUM_BTC,Binance_QTUM_ETH,Binance_ETH_BTC t-watch-binance-qtum -v

Run in background

    python3 hydra/cli.py -m Binance_WTC_BTC,Binance_WTC_ETH,Binance_ETH_BTC t-watch-binance-wtc  &
    python3 hydra/cli.py -m Binance_BNB_BTC,Binance_BNB_ETH,Binance_ETH_BTC t-watch-binance-bnb  &
    python3 hydra/cli.py -m Binance_LRC_BTC,Binance_LRC_ETH,Binance_ETH_BTC t-watch-binance-lrc  &
    python3 hydra/cli.py -m Binance_MCO_BTC,Binance_MCO_ETH,Binance_ETH_BTC t-watch-binance-mco  &
    python3 hydra/cli.py -m Binance_QTUM_BTC,Binance_QTUM_ETH,Binance_ETH_BTC t-watch-binance-qtum  &

# Alternative usage

List supported public markets:

      python3 hydra/cli.py list-public-markets

Test public market:
      
        python3 hydra/cli.py test_pub -m OKEx_Future_Quarter
        python3 hydra/cli.py test_pub -m KKEX_BCH_BTC
        python3 hydra/cli.py test_pub -m KKEX_ETH_BTC

Test Broker market:
      
      python3 hydra/cli.py test_pri -m Viabtc_BCH_BTC
      python3 hydra/cli.py test_pri -m Jubi_EOS_CNY
      python3 hydra/cli.py test_pri -m KKEX_BCH_BTC
      python3 hydra/cli.py test_pri -m KKEX_ETH_BTC

Run tests

    nosetests arbitrage/

Help
      
      python3 hydra/cli.py -h

# Example

liquid in kkex

    python3 hydra/cli.py -mKKEX_BCH_BTC,Viabtc_BCH_BTC -oMM

arbitrage in haobtc, huobi or okcoin

    python3 hydra/cli.py -oTraderBot -mHaobtcCNY,HuobiCNY
    python3 hydra/cli.py -oTraderBot -mHaobtcCNY,OKCoinCNY

bch bcc arbitrage in Bitfinex_BCH_BTC, Bittrex_BCH_BTC

    python3 hydra/cli.py -o BCH_BTC_Arbitrage -m Bitfinex_BCH_BTC,Bittrex_BCH_BTC
    python3 hydra/cli.py -o BCH_BTC_Arbitrage -m Bitfinex_BCH_BTC,Bittrex_BCH_BTC,Viabtc_BCH_BTC


balance statatistic 

    python3 hydra/cli.py -oBalanceDumper -mHaobtcCNY
    
price diff:

    python3 hydra/cli.py -oPriceMonitor -mOKCoin_BTC_CNY,OKEx_Future_Quarter,Bitfinex_BTC_USD


bistar test

    python3 hydra/bitstar_test.py

    
# TODO

 * Tests
 * Write documentation
 * Better history handling for observer "HistoryDumper" (Redis ?)
 * Move EUR / USD from a market to an other:
   * Coupons
   * Negative Operations

# LICENSE


MIT

Copyright (c) 2016-2017 Phil Song <songbohr@gmail.com>


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Donate

If for some reason you feel like donating a few micro btc to future development, those should go here:

`1NDnnWCUu926z4wxA3sNBGYWNQD3mKyes8`

## Credits

* @[Maxime Biais](https://github.com/maxme) for [the original work on **bitcoin-arbitrage**](https://github.com/maxme/https://github.com/maxme/bitcoin-arbitrage)

![Join Us](docs/xmq.jpg)

