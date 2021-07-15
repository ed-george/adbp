import click
import subprocess

##################################################################### 

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
        ip = run_cmd('ipconfig getifaddr en0', lambda: click.echo('Using default IP'))[1]
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
            create_proxy(device, ip, port)


# Return a sanitised list of connected devices
def get_devices():
    cmd = 'adb devices | grep device | grep -v devices | awk \'{print$1}\''
    result_code, output = run_cmd(cmd)
    return output.split("\n")

# Create proxy via adb
def create_proxy(serial, ip, port):
    click.echo('Creating proxy rule for %s %s:%d' % (serial, ip, port))
    cmd = 'adb -s %s shell settings put global http_proxy %s:%d' % (serial, ip, port)
    return run_cmd(cmd, lambda: click.echo('Success'))

# Run a term command
def run_cmd(cmd, func = lambda: ()):
    result_code, output = subprocess.getstatusoutput(cmd)
    if result_code != 0:
        show_error(output)
    else:
        func()
    return result_code, output

def show_error(msg):
    click.echo('*** Error %s ***' % msg)

if __name__ == '__main__':
    adbp()