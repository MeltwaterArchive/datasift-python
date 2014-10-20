from OpenSSL import SSL

class ClientContextFactory:
        """A context factory for SSL clients."""

        isClient = 1

        # SSLv23_METHOD allows SSLv2, SSLv3, and TLSv1.  We disable SSLv2 and SSLv3 below,
        # though.
        method = SSL.SSLv3_METHOD

        _contextFactory = SSL.Context

        def getContext(self):
                ctx = self._contextFactory(self.method)
                ctx.set_options(SSL.OP_NO_SSLv3)
                ctx.set_options(SSL.OP_NO_SSLv2)
                return ctx
