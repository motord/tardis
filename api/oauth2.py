# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers.avatar import AvatarRequestHandler
from backends import db
import momoko
from oauthlib.oauth2 import RequestValidator, LegacyApplicationServer, BackendApplicationServer
import logging
from tornado import web
import tornado.gen
from models import Box
from cred import AvatarCredentailsChecker, BoxCredentialsChecker, BoxIdKey, AvatarEmailPasswordBoxId

log = logging.getLogger(__name__)


class TardisRequestValidator(RequestValidator):
    def authenticate_client(self, request, *args, **kwargs):
        checker = BoxCredentialsChecker()
        request.client=checker.requestBox(request.extra_credentials)
        request.client_id=request.client.box_id
        return True if request.client else False

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return None

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        return None

    def is_within_original_scope(self, request_scopes, refresh_token, request, *args, **kwargs):
        return True

    def save_bearer_token(self, token, request, *args, **kwargs):
        raise NotImplementedError('Subclasses must implement this method.')

    def validate_bearer_token(self, token, scopes, request):
        raise NotImplementedError('Subclasses must implement this method.')

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        return grant_type in ['password', 'client_credentials']

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        raise NotImplementedError('Subclasses must implement this method.')

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        return True

    def validate_user(self, username, password, client, request, *args, **kwargs):
        credentials=AvatarEmailPasswordBoxId(username, password, client.box_id)
        return True if AvatarCredentailsChecker.requestAvatar(credentials) else False

validator = TardisRequestValidator()
resourceOwnerPasswordCredentialsProvider=LegacyApplicationServer(validator)
clientCredentialsProvider=BackendApplicationServer(validator)


class TokenHandler(AvatarRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        if self.get_argument('grant_type', default=None)=='password':
            return resourceOwnerPasswordCredentialsProvider.create_token_response(self.request.url,
                                                                                  http_method=self.request.method,
                                                                                  body=self.request.body,
                                                                                  headers=self.request.headers,
                                                                                  credentials=BoxIdKey(self.get_argument('client_id', default=None), self.get_argument('client_secret', default=None)))
        if self.get_argument('grant_type', default=None)=='client_credentials':
            return clientCredentialsProvider.create_token_response(self.request.url,
                                                                   http_method=self.request.method,
                                                                   body=self.request.body,
                                                                   headers=self.request.headers,
                                                                   credentials=BoxIdKey(self.get_argument('client_id', default=None), self.get_argument('client_secret', default=None)))