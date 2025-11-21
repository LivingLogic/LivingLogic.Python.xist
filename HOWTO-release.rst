How to make an XIST release
===========================


Requirements
------------

For the release process to work you need to install :mod:`wheel` and
:mod:`twine`::

	pip install wheel twine

Also for building the PDF version of the documentation you needs a TeX
installation suitable for :mod:`sphinx`.


Preparing for the release
-------------------------

Bump the version number in ``setup.py``.

Document the changes in ``NEWS.rst`` and specify the version number and release
date there.

If the release includes any backwards incompatible changes, document how to
update old code in ``MIGRATION.rst``.

Document any new features in the Sphinx documentation contained in the ``docs/``
directory and/or in the docstrings of the new or changed modules, classes and
functions.

Make sure that the tests pass by running::

	python -mpytest

Add the new version in ``docs/makedownloads.py`` and run (in ``docs/``)::

	LL_URL_SSH_PYTHON=python3 python makedownloads.py


Creating the packages
---------------------

Commit everything up to now.

Tag the release (with something like `rel-xx-yy` or `rel-xx-yy-zz`)::

	git tag rel-xx-yy-zz

Push the resulting commit and the tag::

	git push; git push --tags

Create the release on the external and internal download server (do this
in the root directory)::

	LL_URL_SSH_PYTHON=python3 make dist livinglogic


Creating and deploying the documentation
----------------------------------------

Recreate the list of downloads in ``docs/`` via (do this in the ``docs/``
subdirectory)::

	make clean download

As this has changed ``docs/DOWNLOAD.rst`` you need to check in the result and
push the resulting commit.

Wait for Gitlab to finish building the container image, and then click the
"deploy" button to deploy it to ``python.livinglogic.de``.


Uploading the release to the cheeseshop
---------------------------------------

Upload the release to the cheeseshop via (do this in the root directory)::

	make upload


Creating the Windows packages
-----------------------------

Tell the Windows people that there's a new XIST release and wait until they've
finished their release dance.

Go to the ``docs/`` subdirectory and recreate the download list::

	make clean download

Check in the result and push it to all repos.

Wait for Gitlab to finish building the container image, and then click the
"deploy" button to deploy it to ``python.livinglogic.de``.
