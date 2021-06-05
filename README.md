These are third-party modules for the [Inkycal project](https://github.com/aceisace/Inky-Calendar)

# Inkycal Stocks Module
<p align="center">
            <img src="https://raw.githubusercontent.com/worstface/inkycal_stocks/master/Gallery/inkycal_stocks.jpg" width="800">
</p>

The stocks-module conveniently displays a list of selected stocks, currencies or indices with their current prices and total/procentual daily change.

It depends on [yfinance](https://github.com/ranaroussi/yfinance) which uses the [Yahoo! Finance](https://finance.yahoo.com/) data. 

You can display any information by using the respective symbols that are used by [Yahoo! Finance](https://finance.yahoo.com/).

It's easily setup with a string of comma separated symbols like this e.g.: 
`tickers = "TSLA, AMD, NVDA, ^DJI, BTC-USD, EURUSD=X"`

# Installation instructions
1) Navigate to the modules directory
`cd Inkycal/inkycal/modules`

2) Download the third-party module:
```bash
wget https://raw.githubusercontent.com/worstface/inkycal_stocks/master/inkycal_stocks.py
```

3) Install yfinance:
```bash
pip3 install yfinance
```
4) Add module to Inkycal/inkycal/__init__.py and Inkycal/inkycal/modules/__init__.py

# Inkycal Tweets Module
<p align="center">
            <img src="https://raw.githubusercontent.com/worstface/inkycal_stocks/master/Gallery/inkycal_tweets.jpg" width="800">
</p>

The tweets-module displays a tweet from twitter by using the [Twint library](https://github.com/twintproject/twint).
It shows the chronologically last tweet defined by a filter which can contain a username, a search term, a location and a minimum of likes.
The tweet is displayed whith a header, which contains the name, username and timestamp. It contains the text including a QR-code with a link to the tweet. 
Below the tweet a footer is drawn, which shows the number of comments, retweets and likes.

Needs material-icons font (fonts folder), qrcode and Twint >v2.1.21

The current git dev state of Twint is needed for this module (the current pip package doesn't work):  
`pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint`

Recommended settings: moduleHeight >= 1/4 display

# Inkycal XKCD Module
<p align="center">
            <img src="https://raw.githubusercontent.com/worstface/inkycal_stocks/master/Gallery/inkycal_xkcd.jpg" width="800">
</p>

# Installation instructions
1) Navigate to the modules directory
`cd Inkycal/inkycal/modules`

2) Download the third-party module:
```bash
wget https://raw.githubusercontent.com/worstface/inkycal_stocks/master/inkycal_xkcd.py
```

3) Install xkcd lib:
```bash
pip3 install xkcd
```
4) Add module to Inkycal/inkycal/__init__.py and Inkycal/inkycal/modules/__init__.py

```
