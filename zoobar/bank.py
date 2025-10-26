from debug import *
from zoodb import *
import rpclib
import sys

sys.path.append(os.getcwd())
import readconf

@catch_err
def register(username):
    host = readconf.read_conf().lookup_host('bank')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('register', username=username)
        return ret
    
@catch_err
def transfer(sender, recipient, zoobars, token):
    host = readconf.read_conf().lookup_host('bank')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars, token=token)
        return ret

@catch_err
def profile_xfer(sender, recipient, zoobars):
    host = readconf.read_conf().lookup_host('bank')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('profile_xfer', sender=sender, recipient=recipient, zoobars=zoobars)
        return ret

@catch_err
def balance(username):
    host = readconf.read_conf().lookup_host('bank')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('balance', username=username)
        return ret

@catch_err
def get_log(username):
    host = readconf.read_conf().lookup_host('bank')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('get_log', username=username)
        return ret