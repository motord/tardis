# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from backends import db
from model import StorageModel
from tornado import gen


class Box(StorageModel):
    """A model base class that uses PostgreSQL for the storage backend. Uses the
    asynchronous momoko client.

    :param str item_id: The id for the data item

    """
    _saved = False

    def __init__(self, item_id=None, *args, **kwargs):
        # The parent will attempt to fetch the value if item_id is set
        super(Box, self).__init__(item_id, **kwargs)

    @gen.coroutine
    def delete(self):
        """Delete the item from storage

        :rtype: bool

        """
        result = gen.Task(db.delete, self._key)
        raise gen.Return(bool(result))

    @gen.coroutine
    def fetch(self):
        """Fetch the data for the model from Redis and assign the values.

        :rtype: bool

        """
        raw = yield gen.Task(db.get, self._key)
        if raw:
            self.loads(base64.b64decode(raw))
            raise gen.Return(True)
        raise gen.Return(False)

    @gen.coroutine
    def save(self):
        """Store the model in PostgreSQL.

        :rtype: bool

        """
        pipeline = db.pipeline()
        pipeline.set(self._key, base64.b64encode(self.dumps()))
        result = yield gen.Task(pipeline.execute)
        self._dirty, self._saved = not all(result), all(result)
        raise gen.Return(all(result))