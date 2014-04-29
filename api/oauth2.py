# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers.avatar import AvatarRequestHandler
from backends import db
import momoko
from oauthlib.oauth2 import RequestValidator, LegacyApplicationServer, BackendApplicationServer
import logging
from datetime import datetime, timedelta
from tornado import web
from tornado import gen
from models import Box, Authorization
from cred import AvatarCredentailsChecker, BoxCredentialsChecker, BoxClientIdClientSecret, AvatarEmailPasswordBoxId

log = logging.getLogger(__name__)


class TardisRequestValidator(RequestValidator):
    def __init__(self, client, authorization, avatar):
        super(TardisRequestValidator, self).__init__()
        self.client=client
        self.authorization=authorization
        self.avatar=avatar

    def authenticate_client(self, request, *args, **kwargs):
        request.client=self.client
        if request.client:
            return True
        return False

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return None

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        return None

    def is_within_original_scope(self, request_scopes, refresh_token, request, *args, **kwargs):
        return True

    def save_bearer_token(self, token, request, *args, **kwargs):
        authorization=Authorization(access_token=token['access_token'], refresh_token=token['refresh_token'],
                                    expires_at=datetime.utcnow() + timedelta(seconds=100), avatar=request.avatar,
                                    created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        self.authorization.save()

    def validate_bearer_token(self, token, scopes, request):
        if datetime.utcnow() > self.authorization.expires_at:
            return False
        request.access_token = self.authorization.access_token
        request.user = self.authorization.avatar
        request.client = self.authorization.avatar.box
        return True

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        return grant_type in ['password', 'client_credentials']

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        if self.authorization and self.authorization.avatar.box.id==client.box_id:
            request.client = self.authorization.avatar.box
            request.avatar =self.authorization.avatar
            return True
        return False

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        return True

    def validate_user(self, username, password, client, request, *args, **kwargs):
        request.avatar=self.avatar
        if request.avatar:
            return True
        return False


class TokenHandler(AvatarRequestHandler):
    @gen.coroutine
    def post(self):
        checker = BoxCredentialsChecker()
        client=yield gen.Task(checker.requestBox, BoxClientIdClientSecret(self.get_argument('client_id', default=None), self.get_argument('client_secret', default=None)))
        authorization=None

        access_token=self.get_argument('access_token', default=None)
        if access_token:
            authorization=yield gen.Task(Authorization.select().where(Authorization.access_token==access_token).get)

        refresh_token=self.get_argument('refresh_token', default=None)
        if refresh_token:
            authorization=yield gen.Task(Authorization.select().where(Authorization.refresh_token_token==refresh_token).get)

        credentials=AvatarEmailPasswordBoxId(self.get_argument('username', default=None),
                                             self.get_argument('password', default=None),
                                             client.id)
        checker=AvatarCredentailsChecker()
        avatar=checker.requestAvatar(credentials)

        validator = TardisRequestValidator(client, authorization, avatar)

        if self.get_argument('grant_type', default=None)=='password':
            resourceOwnerPasswordCredentialsProvider=LegacyApplicationServer(validator)
            headers, body, status=resourceOwnerPasswordCredentialsProvider.create_token_response(self.request.uri,
                                                                                  http_method=self.request.method,
                                                                                  body=self.request.body,
                                                                                  headers=self.request.headers)
        if self.get_argument('grant_type', default=None)=='client_credentials':
            clientCredentialsProvider=BackendApplicationServer(validator)
            headers, body, status=clientCredentialsProvider.create_token_response(self.request.uri,
                                                                   http_method=self.request.method,
                                                                   body=self.request.body,
                                                                   headers=self.request.headers)
        self.set_status(status)
        self.write(body)
        for k, v in headers.items():
            self.set_header(k,v)
        self.finish()