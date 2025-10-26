#!/usr/bin/env python3

import rpclib
import sys
import time
from zoodb import *
from debug import *
from auth_client import check_token

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_register(self, username):
        bankdb = bank_setup()
        person = bankdb.query(Bank).get(username)
        if person:
            return None
        newperson = Bank()
        newperson.username = username
        newperson.zoobars = 10
        bankdb.add(newperson)
        bankdb.commit()

    def rpc_transfer(self, sender, recipient, zoobars, token):
        if (check_token(sender, token) == False):
            raise ValueError()
        bankdb = bank_setup()
        senderp = bankdb.query(Bank).get(sender)
        recipientp = bankdb.query(Bank).get(recipient)
        sender_balance = senderp.zoobars - zoobars
        recipient_balance = recipientp.zoobars + zoobars
        if sender_balance < 0 or recipient_balance < 0:
            raise ValueError()
        senderp.zoobars = sender_balance
        recipientp.zoobars = recipient_balance
        bankdb.commit()
        transfer = Transfer()
        transfer.sender = sender
        transfer.recipient = recipient
        transfer.amount = zoobars
        transfer.time = time.asctime()
        transferdb = transfer_setup()
        transferdb.add(transfer)
        transferdb.commit()

    def rpc_profile_xfer(self, sender, recipient, zoobars):
        log(self.caller)
        if (self.caller != "profile"):
            raise ValueError()
        bankdb = bank_setup()
        senderp = bankdb.query(Bank).get(sender)
        recipientp = bankdb.query(Bank).get(recipient)
        sender_balance = senderp.zoobars - zoobars
        recipient_balance = recipientp.zoobars + zoobars
        if sender_balance < 0 or recipient_balance < 0:
            raise ValueError()
        senderp.zoobars = sender_balance
        recipientp.zoobars = recipient_balance
        bankdb.commit()
        transfer = Transfer()
        transfer.sender = sender
        transfer.recipient = recipient
        transfer.amount = zoobars
        transfer.time = time.asctime()
        transferdb = transfer_setup()
        transferdb.add(transfer)
        transferdb.commit()

    def rpc_balance(self, username):
        log(self.caller)
        db = bank_setup()
        person = db.query(Bank).get(username)
        return person.zoobars
    
    def rpc_get_log(self, username):
        db = transfer_setup()
        l = db.query(Transfer).filter(or_(Transfer.sender==username,
                                          Transfer.recipient==username))
        r = []
        for t in l:
           r.append({'time': t.time,
                     'sender': t.sender ,
                     'recipient': t.recipient,
                     'amount': t.amount })
        return r 

if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")

s = BankRpcServer()
bank_setup()
s.run_fork(sys.argv[1])


