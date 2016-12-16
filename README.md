# CloudBase.py

A simple python script for estimating forecast cloud base for a location.

!['Screenshot of python script output'](cloudbase.jpg)

## Instructions
1. Clone this repo
1. Install the requirements `pip install -r requirements.txt`
1. Get a DarkSkies API key from [https://darksky.net/dev/](https://darksky.net/dev/)
1. Run the script with `python cloudbase.py [API Key] [lat] [lng] [day]` e.g.
`python cloudbase.py myapikeymyapikeymyapikey 52.518342 -2.871176 0`

##Thanks
[Christopher Blunck](http://pydoc.net/Python/weather/0.9.1/weather.units.temp/)
for the temperature conversion functions I've used in this script.
