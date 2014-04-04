"""
Base Tinman RequestHandlers

"""
import datetime
import json
import logging

from tornado import gen
from tornado import escape
from tornado import web

from tinman import config
from tinman import session


LOGGER = logging.getLogger(__name__)

HEAD = 'HEAD'
GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
PATCH = 'PATCH'
PUT = 'PUT'
OPTIONS = 'OPTIONS'


class BaseHandler(web.RequestHandler):
    """A base RequestHandler that adds the following functionality:

    - If sending a dict, checks the user-agent string for curl and sends an
      indented, sorted human-readable JSON snippet
    - Toggles the ensure_ascii flag in json.dumps
    - Overrides the default behavior for unimplemented methods to instead set
    the status and look to the allow object attribute for methods that can be
    allowed. This is useful for when using NewRelic since the newrelic agent
    will catch the normal exceptions thrown as errors and trigger false alerts.

    To use, do something like::

        from tinman import handlers

        class Handler(handlers.RequestHandler):

            ALLOW = [handlers.GET, handlers.POST]

            def get(self, *args, **kwargs):
                self.write({'foo': 'bar'})

            def post(self, *args, **kwargs):
                self.write({'message': 'Saved'})

    """
    ALLOW = []
    JSON = 'application/json'

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def _method_not_allowed(self):
        self.set_header('Allow', ', '.join(self.ALLOW))
        self.set_status(405, 'Method Not Allowed')
        self.finish()

    @web.asynchronous
    def head(self, *args, **kwargs):
        """Implement the HTTP HEAD method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def get(self, *args, **kwargs):
        """Implement the HTTP GET method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def post(self, *args, **kwargs):
        """Implement the HTTP POST method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def delete(self, *args, **kwargs):
        """Implement the HTTP DELETE method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def patch(self, *args, **kwargs):
        """Implement the HTTP PATCH method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def put(self, *args, **kwargs):
        """Implement the HTTP PUT method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self._method_not_allowed()

    @web.asynchronous
    def options(self, *args, **kwargs):
        """Implement the HTTP OPTIONS method

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.set_header('Allow', ', '.join(self.ALLOW))
        self.set_status(204)
        self.finish()

    def prepare(self):
        """Prepare the incoming request, checking to see the request is sending
        JSON content in the request body. If so, the content is decoded and
        assigned to the json_arguments attribute.

        """
        super(BaseHandler, self).prepare()
        if self.request.headers.get('content-type', '').startswith(self.JSON):
            self.request.body = escape.json_decode(self.request.body)

    def write(self, chunk):
        """Writes the given chunk to the output buffer. Checks for curl in the
        user-agent and if set, provides indented output if returning JSON.

        To write the output to the network, use the flush() method below.

        If the given chunk is a dictionary, we write it as JSON and set
        the Content-Type of the response to be ``application/json``.
        (if you want to send JSON as a different ``Content-Type``, call
        set_header *after* calling write()).

        :param mixed chunk: The string or dict to write to the client

        """
        if self._finished:
            raise RuntimeError("Cannot write() after finish().  May be caused "
                               "by using async operations without the "
                               "@asynchronous decorator.")
        if isinstance(chunk, dict):
            options = {'ensure_ascii': False}
            if 'curl' in self.request.headers.get('user-agent'):
                options['indent'] = 2
                options['sort_keys'] = True
            chunk = json.dumps(chunk, **options).replace("</", "<\\/") + '\n'
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(web.utf8(chunk))

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            LOGGER.debug(msg)
            raise web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                LOGGER.debug(msg)
                raise web.HTTPError(400, msg)
            LOGGER.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        LOGGER.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def get_current_tenant(self):
        return self.get_secure_cookie("tenantname")

    def get_tenant_login_url(self):
        """Override to customize the tenant login URL based on the request.

        By default, we use the ``tenant_login_url`` application setting.
        """
        self.require_setting("tenant_login_url", "@decorators.tenant_authenticated")
        return self.application.settings["tenant_login_url"]

    @property
    def db(self):
        return self.application.db

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


class SessionRequestHandler(BaseHandler):
    """A RequestHandler that adds session support. For configuration details
    see the tinman.session module.

    """
    SESSION_COOKIE_NAME = 'session'
    SESSION_DURATION = 3600

    @gen.coroutine
    def on_finish(self):
        """Called by Tornado when the request is done. Update the session data
        and remove the session object.

        """
        super(SessionRequestHandler, self).on_finish()
        LOGGER.debug('Entering SessionRequestHandler.on_finish: %s',
                     self.session.id)
        self.session.last_request_at = self.current_epoch()
        self.session.last_request_uri = self.request.uri
        if self.session.dirty:
            result = yield self.session.save()
            LOGGER.debug('on_finish yield save: %r', result)
        self.session = None
        LOGGER.debug('Exiting SessionRequestHandler.on_finish: %r',
                     self.session)

    def current_epoch(self):
        return int(datetime.datetime.now().strftime('%s'))

    @gen.coroutine
    def start_session(self):
        """Start the session. Invoke in your @gen.coroutine wrapped prepare
        method like::

            result = yield gen.Task(self.start_session)

        :rtype: bool

        """
        self.session = self._session_start()
        result = yield gen.Task(self.session.fetch)
        self._set_session_cookie()
        if not self.session.get('ip_address'):
            self.session.ip_address = self.request.remote_ip
        self._last_values()
        raise gen.Return(result)

    @gen.coroutine
    def prepare(self):
        """Prepare the session, setting up the session object and loading in
        the values, assigning the IP address to the session if it's an new one.

        """
        super(SessionRequestHandler, self).prepare()
        result = yield gen.Task(self.start_session)
        LOGGER.debug('Exiting SessionRequestHandler.prepare: %r', result)

    @property
    def _cookie_expiration(self):
        """Return the expiration timestamp for the session cookie.

        :rtype: datetime

        """
        value = (datetime.datetime.utcnow() +
                 datetime.timedelta(seconds=self._session_duration))
        LOGGER.debug('Cookie expires: %s', value.isoformat())
        return value

    @property
    def _cookie_settings(self):
        return self.settings['session'].get('cookie', dict())

    def _last_values(self):
        """Always carry last_request_uri and last_request_at even if the last_*
        values are null.

        """
        if not self.session.get('last_request_uri'):
            self.session.last_request_uri = None
        self.session.last_request_at = self.session.get('last_request_at', 0)

    @property
    def _session_class(self):
        if self._session_settings.get('name') == config.FILE:
            return session.FileSession
        elif self._session_settings.get('name') == config.REDIS:
            return session.RedisSession
        else:
            raise ValueError('Unknown adapter type')

    @property
    def _session_cookie_name(self):
        """Return the session cookie name, defaulting to the class default

        :rtype: str

        """
        return self._cookie_settings.get(config.NAME, self.SESSION_COOKIE_NAME)

    @property
    def _session_duration(self):
        """Return the session duration from config or the default value

        :rtype: int

        """
        return self._cookie_settings.get(config.DURATION, self.SESSION_DURATION)

    @property
    def _session_id(self):
        """Returns the session id from the session cookie.

        :rtype: str

        """
        return self.get_secure_cookie(self._session_cookie_name, None)

    @property
    def _session_settings(self):
        return self.settings['session'].get('adapter', dict())

    def _session_start(self):
        """Return an instance of the proper session object.

        :rtype: Session

        """
        return self._session_class(self._session_id,
                                   self._session_duration,
                                   self._session_settings)
    def _set_session_cookie(self):
        """Set the session data cookie."""
        LOGGER.debug('Setting session cookie for %s', self.session.id)
        self.set_secure_cookie(name=self._session_cookie_name,
                               value=self.session.id,
                               expires=self._cookie_expiration)
