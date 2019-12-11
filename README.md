## Setting up token
Copy the `tokenfile.example.py` to `tokenfile.py` and edit your `tokenfile.py`

## Setting up python instance
```sh
# Execute this first with virtual environment (recommended)
# Skip to next label if you're not using venv
virtualenv -p /usr/bin/python3 env
source env/bin/activate

# Do this step instead if you're not using venv
pip3 install -r requirements.txt
```

## Entering/exiting virtual environment
```sh
# Start venv
source env/bin/activate

# Exit venv
deactivate
```

## Starting up bot as non-daemon and killing bot
```sh
python3 main.py
```

To kill, press Ctrl+C and start it up again

## Starting up pm2 (daemon)
Without virtual environment
```sh
pm2 start ./main.py --interpreter /usr/bin/python3 --name discordbot
```

With virtual environment
```sh
# There is no need to enter virtual environment with pm2, but use the path to python3 bin in env
# Reminder that this is relative path, not absolute. Use your path properly
# ./env/bin/python3 will run the path relative to your current working directory
pm2 start ./main.py --interpreter ./env/bin/python3 --name discordbot
```

You can run your python instance as a service, but it is not advised. pm2 is easier to handle

## Refresh bot
Without pm2: kill and start the process

With pm2
```sh
pm2 restart discordbot
```

-----

## To convert stuff from windows to linux
Execute `convert.sh`
