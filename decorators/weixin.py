# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from logging import debug
from hashlib import sha1


def signature_verified(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        signature=self.request.get_argument('signature')
        timestamp=self.request.get_argument('timestamp')
        nonce=self.request.get_argument('nonce')
        echostr=self.request.get_argument('echostr')
        channel=kwargs['channel']
        q=Channel.gql("WHERE id = :1", channel)
        c=q.get()
        if c:
            kwargs['channel']=c
            token=c.token
            if sha1(''.join(sorted([token, timestamp, nonce]))).hexdigest()==signature:
                if self.request.method=='GET':
                    return echostr
                else:
                    return func(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper