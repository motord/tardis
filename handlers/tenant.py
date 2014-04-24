# -*- coding: utf-8 -*-
__author__ = 'peter'

from base import BaseHandler


class TenantRequestHandler(BaseHandler):
    def get_current_tenant(self):
        return self.get_secure_cookie("tenantname")

    def get_tenant_login_url(self):
        """Override to customize the tenant login URL based on the request.

        By default, we use the ``tenant_login_url`` application setting.
        """
        self.require_setting("tenant_login_url", "@decorators.tenant_authenticated")
        return self.application.settings["tenant_login_url"]

    @property
    def current_tenant(self):
        """The authenticated tenant for this request.

        This is a cached version of `get_current_tenant`, which you can
        override to set the current based on, e.g., a cookie. If that
        method is not overridden, this method always returns None.

        We lazy-load the current tenant the first time this method is called
        and cache the result after that.
        """
        if not hasattr(self, "_current_tenant"):
            self._current_tenant = self.get_current_tenant()
        return self._current_tenant
