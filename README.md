# weblocator
### Just a better dirbuster
```bash
 __          __  _     _                     _              
 \ \        / / | |   | |                   | |             
  \ \  /\  / /__| |__ | |     ___   ___ __ _| |_ ___  _ __  
   \ \/  \/ / _ \ '_ \| |    / _ \ / __/ _` | __/ _ \| '__| 
    \  /\  /  __/ |_) | |___| (_) | (_| (_| | || (_) | |    
     \/  \/ \___|_.__/|______\___/ \___\__,_|\__\___/|_|    
                                                            
weblocator.py - Just a better dirbuster
Version 0.9.1
David Tavarez (davidtavarez)
https://github.com/davidtavarez/weblocator

usage: weblocator.py [-h] -t TARGET -w WORDLIST [--validation VALIDATION]
                     [--extension EXTENSION] [--threads THREADS]
                     [--tor-host TOR_HOST] [--tor-port TOR_PORT]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The URL of the TARGET to scan.
  -w WORDLIST, --wordlist WORDLIST
                        The paths to locate.
  --validation VALIDATION
                        Try to find a string to validate the results.
  --extension EXTENSION
                        Add an extension.
  --threads THREADS     Number of threads [default=10].
  --tor-host TOR_HOST   Tor server.
  --tor-port TOR_PORT   Tor port server.
```
#### Installing weblocator
```bash
git clone git@github.com:davidtavarez/weblocator.git
cd weblocator
pip install -r requirements.txt
chmod +x weblocator.py
./weblocator.py
```
