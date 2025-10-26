from debug import *
from zoodb import *
import rpclib
import sys

sys.path.append(os.getcwd())
import readconf

@catch_err
def login(username, password):
    host = readconf.read_conf().lookup_host('auth')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('login', username=username, password=password)
        return ret

@catch_err
def register(username, password):
    host = readconf.read_conf().lookup_host('auth')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        log("Conectado")
        ret = c.call('register', username=username, password=password)
        return ret

@catch_err
def check_token(username, token):
    host = readconf.read_conf().lookup_host('auth')
    log(f"host = {host}")
    with rpclib.client_connect(host) as c:
        ret = c.call('check_token', username=username, token=token)
        return ret
