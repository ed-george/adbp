#!/usr/bin/env python3

import click
import socket

from ppadb.client import Client as AdbClient

# Globals #
ADB_HOST = "127.0.0.1"
ADB_PORT = 5037

####################################################################

@click.group()
def adbp():
    """A tool to add/remove proxies on Android devices via adb"""

@adbp.command('remove', short_help='Removes any proxy')
@click.option('--serial', default='', help='Device Serial')
def remove(serial):
    """Removes any proxy on connected devices via adb"""
    apply_rule(serial, '', 0)

@adbp.command('add', short_help='Adds a proxy')
@click.option('--serial', default='', help='Device Serial')
@click.option('--ip', default='', help='IP Address')
@click.option('--port', default=8888, help='Proxy Port')
def add(serial, ip, port):
    """Enables a proxy on connected devices via adb"""
    if ip == '':
        ip = get_local_ip(lambda: click.echo('Using default IP'))
    apply_rule(serial, ip, port)

##################################################################### 

# Applies proxy rule to selected device(s) with supplied ip and port
def apply_rule(serial, ip, port):
    if serial != '':
        # Single rule
        create_proxy(serial, ip, port)
    else:
        # Multi-device rule
        for device in get_devices():
            create_proxy(device.serial, ip, port)


# Return a sanitised list of connected devices
def get_devices():
    client = AdbClient(host=ADB_HOST, port=ADB_PORT)
    return client.devices()

# Create proxy via adb
def create_proxy(serial, ip, port):
    click.echo('Creating proxy rule for %s %s:%d' % (serial, ip, port))
    cmd = 'settings put global http_proxy %s:%d' % (ip, port)
    return run_cmd(cmd, serial, lambda: click.echo('Success'))

# Run a term command
def run_cmd(cmd, serial, func = lambda: ()):
    client = AdbClient(host=ADB_HOST, port=ADB_PORT)
    device = client.device(serial)
    output = device.shell(cmd)
    
    if output != '':
        show_error(output)
    else:
        func()

    return output 

def show_error(msg):
    click.echo('*** Error %s ***' % msg)

def get_local_ip(func = lambda: ()):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
        show_error("Local IP Address is set to localhost(%s)" % (local_ip))
    finally:
        s.close()
        func()
    return local_ip

if __name__ == '__main__':
    adbp()

