# adbp
A python script to make working with proxies on your Android devices _much_ easier!

----

# Installation

Pre-Requisites:

*  [Python 3](https://www.python.org/downloads/)
*  [Click](https://click.palletsprojects.com/en/8.0.x/) - `pip install click`

# Usage


```
Usage: adbp.py [OPTIONS] COMMAND [ARGS]...

  A tool to add/remove proxies on Android devices via adb

Options:
  --help  Show this message and exit.

Commands:
  add     Adds a proxy
  remove  Removes any proxy
```

## Add a proxy

```
Usage: adbp.py add [OPTIONS]

  Enables a proxy on connected devices via adb

Options:
  --serial TEXT   Device Serial
  --ip TEXT       IP Address
  --port INTEGER  Proxy Port
  --help          Show this message and exit.
```

**Examples:**

`python3 adbp.py add` - Adds proxy with default ip address and port 8888 to **all** connected devices

`python3 adbp.py add --serial 1234` - Adds proxy with default ip address and port 8888 to connected device with serial id 1234

`python3 adbp.py add --serial 1234 --ip 192.168.0.1 --port 8080` - Adds proxy of 192.168.0.1:8080 to connected device with serial id 1234

## Remove a proxy

```
Usage: adbp.py remove [OPTIONS]

  Removes any proxy on connected devices via adb

Options:
  --serial TEXT  Device Serial
  --help         Show this message and exit.
```

**Examples:**

`python3 adbp.py remove` - Removes any configured proxy on **all** connected devices

`python3 adbp.py remove --serial 1234` - Removes any configured proxy on connected device with serial id 1234

## Contributing 🛠

I welcome contributions and discussion for new features or bug fixes. It is recommended to file an issue first to prevent unnecessary efforts, but feel free to put in pull requests in the case of trivial changes. In any other case, please feel free to open discussion and I will get back to you when possible.
