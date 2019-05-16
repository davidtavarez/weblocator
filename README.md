# WebLocator
### Just another DirBuster
```bash
 __          __  _     _                     _              
 \ \        / / | |   | |                   | |             
  \ \  /\  / /__| |__ | |     ___   ___ __ _| |_ ___  _ __  
   \ \/  \/ / _ \ '_ \| |    / _ \ / __/ _` | __/ _ \| '__| 
    \  /\  /  __/ |_) | |___| (_) | (_| (_| | || (_) | |    
     \/  \/ \___|_.__/|______\___/ \___\__,_|\__\___/|_|    
                                                            
weblocator.py - Just another DirBuster
Version 1.0
David Tavarez (davidtavarez)
https://github.com/davidtavarez/weblocator

usage: weblocator.py [-h] -t TARGET -w WORDSLIST -p PORT -o PROTOCOL -s
                     STARTING [--validation VALIDATION]
                     [--extension EXTENSION] [--threads THREADS]
                     [--tor-host TOR_HOST] [--tor-port TOR_PORT]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The URL of the TARGET to scan.
  -w WORDSLIST, --wordslist WORDSLIST
                        The words list path.
  -p PORT, --port PORT  The words list path.
  -o PROTOCOL, --protocol PROTOCOL
                        Protocol (http or https).
  -s STARTING, --starting STARTING
                        Starting point (/).
  --validation VALIDATION
                        Try to find a string to validate the results.
  --extension EXTENSION
                        Add an extension.
  --threads THREADS     Number of threads [default=1].
  --tor-host TOR_HOST   Tor server.
  --tor-port TOR_PORT   Tor port server.
```
#### Installing weblocator
```bash
git clone git@github.com:davidtavarez/weblocator.git
cd weblocator
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x weblocator.py
./weblocator.py
```
