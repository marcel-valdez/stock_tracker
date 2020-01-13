# Stock Tracker

Simple stock tracker that currently only works with Robinhood.

There are many other "stock tracking python projects", but they do a lot of things
which I am probably not interested in.

This project will grow organically as my needs from it grow.

# How to use


## To install it

```sh
$ cd ~
$ git clone https://github.com/marcel-valdez/stock_tracker.git
$ cd stock_tracker
$ pipenv install
```

## Use it: Setup credentials

Create a new file with your robinhood credentials, for example create a file named "auth_data.json" with the contents:

```json
{
  "account": {
    "user": "my-user",
    "password": "my-password",
    "device_token": "my-computer-identifier",
  }
}
```

Yes, this is pretty bad. The credentials should be encrypted or requested via command-line every time they're needed using a non-echo input.


## Use it: Fetch all of your orders from Robinhood

Execute the command:

```sh
$ pipenv run python main.py --auth_config_file $(pwd)/auth_data.json --csv_file $(pwd)/my_orders.csv
```

This will create entries in CSV format with all of your orders.
