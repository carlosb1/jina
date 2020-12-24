class BaseRuntime:
    """A Jina Runtime is a procedure that blocks the main process once running (i.e. :meth:`serve_forever`),
    therefore must be put into a separated thread/process. Any program/library/package/module that blocks the main
    process, can be formulated into a :class:`BaseRuntime` class and then be used in :class:`BasePea`.

     In the sequel, we call the main process/thread as ``M``, the process/thread blocked :class:`Runtime` as ``S``.

     In Jina, a :class:`BasePea` object is used to manage a :class:`Runtime` object's lifecycle. A :class:`BasePea`
     is a subclass of :class:`multiprocessing.Process` or :class:`threading.Thread`, it starts from ``M`` and once the
     ``S`` is spawned, it calls :class:`Runtime` methods in the following order:

        1. :meth:`setup` in ``S``

        2. :meth:`serve_forever` in ``S``. Note that this will block ``S``, step 3 won't be
        reached until it is unblocked by :meth:`cancel`

        3. :meth:`teardown` in ``S``. Note that ``S`` is blocked by
        :meth:`serve_forever`, this step won't be reached until step 2 is unblocked by :meth:`cancel`

     The :meth:`setup` and :meth:`teardown` pair together, which defines instructions that will be executed before
     and after. In subclasses, they are optional.

     The :meth:`serve_forever` and :meth:`cancel` pair together, which introduces blocking to ``S`` and then
     unblocking from it. They are mandatory for all subclasses.

     Note that, there is no "exclusive" relation between :meth:`serve_forever` and :meth:`teardown`, :meth:`teardown`
     is not about "cancelling", it is about "cleaning".

     Unlike other three methods that get invoked inside ``S``, the :meth:`cancel` is invoked in ``M`` to unblock ``S``.
     Therefore, :meth:`cancel` usually requires some special communication between ``M`` and ``S``, e.g.

        - Use :class:`threading.Event` or `multiprocessing.Event`, while :meth:`serve_forever` polls for this event
        - Use ZMQ to send a message, while :meth:`serve_forever` polls for this message
        - Use HTTP/REST to send a request, while :meth:`serve_forever` listens to this request

     Note, another way to jump out from :meth:`serve_forever` is raise exceptions from it. This will immediately move to
     :meth:`teardown`.

     .. seealso::

        :class:`BasePea` for managing a :class:`Runtime` object's lifecycle.

     """

    def serve_forever(self):
        """ Running the blocking procedure inside ``S``. Note, once this method is called,
        ``S`` is blocked.

        .. note::

            If this method raises any exception, :meth:`teardown` will be called.

        .. seealso::

            :meth:`cancel` for cancelling the forever loop.
        """
        raise NotImplementedError

    def cancel(self):
        """ Cancelling :meth:`serve_forever` from ``M``. :meth:`cancel` usually requires some special communication
        between ``M`` and ``S``, e.g.

        - Use :class:`threading.Event` or `multiprocessing.Event`, while :meth:`serve_forever` polls for this event
        - Use ZMQ to send a message, while :meth:`serve_forever` polls for this message
        - Use HTTP/REST to send a request, while :meth:`serve_forever` listens to this request

        .. seealso::

            :meth:`serve_forever` for blocking the process/thread.
        """
        raise NotImplementedError

    def setup(self):
        """Method called to prepare the runtime. Optional in subclasses. The default implementation does nothing.

        .. note::

            If this method raises any exception, then :meth:`serve_forever` and :meth:`teardown` won't be called.
        """
        pass

    def teardown(self):
        """Method called immediately after :meth:`serve_forever` is unblocked.
        You can tidy up things here.  Optional in subclasses. The default implementation does nothing.

        .. note::

            This method will only be called if the :meth:`setup` succeeds.
        """
        pass
