# Inkycal Stocks Module
This is third-party module for the [Inkycal project](https://github.com/aceisace/Inky-Calendar)

<p align="center">
<img src="https://github.com/worstface/inkycal_stocks/blob/master/Gallery/inkycal_stocks.jpg" width="800">
</p>

The stocks-module conveniently displays a list of selected stocks, currencies or indices with their current prices and total/procentual daily change.
It depends on yfinance (https://github.com/ranaroussi/yfinance) which uses the yahoo!-finance data.
It's easily setup with a list of stock symbols like this example: tickers = ["TSLA", "AMD", "NVDA", "^DJI", "BTC-USD", "EURUSD=X"]

Status: this is WIP and destined for the Inkycal 2.0 release.


# Installation instructions
How to install the module.

1) Navigate to the modules directory
`cd Inkycal/inkycal/modules`

2) Download the third-party module:
```bash
# The URL is the rawfile url. e.g. open mymodule.py, then click on [raw] to see the rawfile-url
wget https://raw.githubusercontent.com/aceisace/inkycal_template/master/mymodule.py
```

3) Register this module in Inkycal
```python3
# In python, type the following commands:
from inkycal import Inkycal
inkycal._add_module('/full/path/to/your/module.py', 'Classname_inside_module')
# If everything went well, you should see a printed message without red lines
```

4) Add the following in your `settings.json` file, inside the `panels` section
```
		{
			"location": "top/middle/bottom",
			"type": "Stocks",
                        "height": Null,
			"config": {
				"tickers": ["TSLA", "AMD", "NVDA", "^DJI", "BTC-USD", "EURUSD=X"]
			}
		},
```

# How to remove this module
```python3
# In python, run the following commands:
from inkycal import Inkycal
Inkycal._remove_module('Stocks')
# Where classname is the name of the Class inside file
```
