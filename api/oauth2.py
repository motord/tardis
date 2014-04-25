# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers.avatar import AvatarRequestHandler
from backends import db
import momoko
from oauthlib.oauth2 import RequestValidator, LegacyApplicationServer, BackendApplicationServer
import logging
import datetime
from tornado import web
from tornado import gen
from models import Box, Authorization
from cred import AvatarCredentailsChecker, BoxCredentialsChecker, BoxClientIdClientSecret, AvatarEmailPasswordBoxId

log = logging.getLogger(__name__)


class TardisRequestValidator(RequestValidator):
    @gen.coroutine
    def authenticate_client(self, request, *args, **kwargs):
        checker = BoxCredentialsChecker()
        request.client=checker.requestBox(request.extra_credentials)
        log.debug(request.client)
        return gen.Return(True) if request.client else gen.Return(False)

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return None

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        return None

    def is_within_original_scope(self, request_scopes, refresh_token, request, *args, **kwargs):
        return True

    @gen.coroutine
    def save_bearer_token(self, token, request, *args, **kwargs):
        authorization=Authorization(access_token=token['access_token'], refresh_token=token['refresh_token'],
                                    expires_at=token['expires_at'], avatar=request.avatar,
                                    created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        yield gen.Task(authorization.save)

    @gen.coroutine
    def validate_bearer_token(self, token, scopes, request):
        authorization=yield gen.Task(Authorization.select().where(Authorization.access_token==token).get)
        if datetime.datetime.now() > authorization.expires_at:
            raise gen.Return(False)
        request.access_token = authorization
        request.user = authorization.avatar
        request.client = authorization.avatar.box
        raise gen.Return(True)

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        return grant_type in ['password', 'client_credentials']

    @gen.coroutine
    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        authorization=yield gen.Task(Authorization.select().where(Authorization.refresh_token_token==refresh_token).get)
        if authorization and authorization.avatar.box.id==client.box_id:
            request.client = authorization.avatar.box
            request.avatar =authorization.avatar
            raise gen.Return(True)
        raise gen.Return(False)
    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        return True

    @gen.coroutine
    def validate_user(self, username, password, client, request, *args, **kwargs):
        credentials=AvatarEmailPasswordBoxId(username, password, client.box_id)
        request.avatar=AvatarCredentailsChecker.requestAvatar(credentials)
        return gen.Return(True) if request.avatar else gen.Return(False)

validator = TardisRequestValidator()
resourceOwnerPasswordCredentialsProvider=LegacyApplicationServer(validator)
clientCredentialsProvider=BackendApplicationServer(validator)


class TokenHandler(AvatarRequestHandler):
    @gen.coroutine
    def post(self):
        if self.get_argument('grant_type', default=None)=='password':
            headers, body, status=resourceOwnerPasswordCredentialsProvider.create_token_response(self.request.uri,
                                                                                  http_method=self.request.method,
                                                                                  body=self.request.body,
                                                                                  headers=self.request.headers,
                                                                                  credentials=BoxClientIdClientSecret(self.get_argument('client_id', default=None), self.get_argument('client_secret', default=None)))
        if self.get_argument('grant_type', default=None)=='client_credentials':
            headers, body, status=clientCredentialsProvider.create_token_response(self.request.uri,
                                                                   http_method=self.request.method,
                                                                   body=self.request.body,
                                                                   headers=self.request.headers,
                                                                   credentials=BoxClientIdClientSecret(self.get_argument('client_id', default=None), self.get_argument('client_secret', default=None)))
        self.set_status(status)
        self.write(body)
        for k, v in headers.items():
            self.set_header(k,v)
        self.finish()