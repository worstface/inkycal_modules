These are third-party modules for the [Inkycal project](https://github.com/aceisace/Inky-Calendar)

# Inkycal Stocks Module
<p align="center">
            <img src="https://raw.githubusercontent.com/worstface/inkycal_stocks/master/Gallery/inkycal_stocks.jpg" width="800">
</p>

The stocks-module conveniently displays a list of selected stocks, currencies or indices with their current prices and total/procentual daily change.

It depends on [yfinance](https://github.com/ranaroussi/yfinance) which uses the [Yahoo! Finance](https://finance.yahoo.com/) data. 

You can display any information by using the respective symbols that are used by [Yahoo! Finance](https://finance.yahoo.com/).

It's easily setup with a list of symbols like this e.g.: 
`tickers = ["TSLA", "AMD", "NVDA", "^DJI", "BTC-USD", "EURUSD=X"]`

# Inkycal Tweets Module
<p align="center">
            <img src="https://raw.githubusercontent.com/worstface/inkycal_stocks/master/Gallery/inkycal_tweets.jpg" width="800">
</p>

The tweets-module displays a tweet from twitter by using the [Twint library](https://github.com/twintproject/twint).
It shows the chronologically last tweet defined by a filter which can contain a username, a search term, a location and a minimum of likes.
The tweet is displayed whith a header, which contains the name, username and timestamp. It contains the text including a QR-code with a link to the tweet. 
Below the tweet a footer is drawn, which shows the number of comments, retweets and likes.

The current git state of Twint is needed for this module (the current package doesn't work):  
'pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint'

Recommended settings: moduleHeight >= 1/4 display

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

4) Register this module in Inkycal
Manual steps for Inkycal 2.0.0:

```python3
>>> # In python, type the following commands:
>>> from inkycal import Inkycal
>>> Inkycal.add_module('/full/path/to/inkycal_stocks.py') # usually '/home/pi/Inkycal/inkycal/modules/inkycal_stocks.py'
>>> # If everything went well, you should see a printed message without red lines
```

# Configuring this module
Once the module is registered, navigate to `Inkycal/server` and run the flask-server with:
`flask run --host=0.0.0.0`

The web-UI should now be available at `http://raspberrypi.local:5000/`. If this does not work, you can manually use the IP address instead, e.g. `http://192.168.1.142:5000/`

Copy the generated settings.json file to your raspberry Pi (VNC/ WinSCP). 
If you don't have access to the Raspberry Pi via VNC/ WinSCP, you can copy the settings.json file to the microSD card instead. After inkycal starts, it will use the new settings.json file.

# How to remove this module
```python3
>>> # In python, run the following commands:
>>> from inkycal import Inkycal
>>> Inkycal.remove_module('inkycal_stocks.py')
```
