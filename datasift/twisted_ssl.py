from OpenSSL import SSL

class ClientContextFactory:
        """A context factory for SSL clients."""

        isClient = 1

        def getContext(self):
		return SSL.Context(SSL.TLSv1_METHOD)
