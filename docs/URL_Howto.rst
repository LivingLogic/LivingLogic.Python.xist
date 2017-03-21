:mod:`ll.url` -- RFC 2396 compliant URLs
########################################

.. automodule:: ll.url


Special features of :mod:`ll.url`
=================================

The class :class:`ll.url.URL` supports many common schemes and one additional
special scheme named ``root`` that deserves an explanation.

A ``root`` URL is supposed to be an URL that is relative to a "project"
directory instead to a base URL of the document that contains the URL.

Suppose we have a document with the following base URL:

.. sourcecode:: pycon

	>>> from ll import url
	>>> base = url.URL("root:company/it/about/index.html")

Now, if we have the following relative URL in this document:

.. sourcecode:: pycon

	>>> url1 = url.URL("images/logos/spam.png")

the combined URL will be:

.. sourcecode:: pycon

	>>> base/url1
	URL('root:company/it/about/images/logos/spam.png')

Now it we use this combined URL and interpret it relative to the base URL we get
back our original relative URL:

.. sourcecode:: pycon

	>>> (base/url1).relative(base)
	URL('images/logos/spam.png')

Let's try a ``root`` URL now:

.. sourcecode:: pycon

	>>> url2 = url.URL("root:images/logos/spam.png")

Combining this URL with the base URL gives us the same as ``url2``:

.. sourcecode:: pycon

	>>> base/url2
	URL('root:images/logos/spam.png')

But if we interpret this result relative to ``base``, we'll get:

.. sourcecode:: pycon

	>>> (base/url2).relative(base)
	URL('../../../images/logos/spam.png')

I.e. this gives us a relative URL that references ``url2`` from ``base`` when
both URLs are relative to the same root directory.
