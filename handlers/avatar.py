# -*- coding: utf-8 -*-
__author__ = 'peter'

from base import BaseHandler


class AvatarRequestHandler(BaseHandler):
    @property
    def current_avatar(self):
        """The authenticated avatar for this request.

        This is a cached version of `get_current_avatar`, which you can
        override to set the current based on, e.g., a cookie. If that
        method is not overridden, this method always returns None.

        We lazy-load the current avatar the first time this method is called
        and cache the result after that.
        """
        return self._current_avatar

    @property
    def grant_type(self):
        return self._grant_type

    def prepare(self):
        super(AvatarRequestHandler, self).prepare()
        self._grant_type=self.request.headers.get('grant_type', default=None)
        self._grant_type=self._grant_type if self._grant_type else self.get_argument('grant_type', default=None)

