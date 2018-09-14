How to make an XIST release
===========================


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

Tag the release (with something like `rel-xx-yy` or `rel-xx-yy-zz`).

Push the result to all repos::

	git push; git push --tags; git push github; git push --tags github

(``github`` is ``git@github.com:LivingLogic/LivingLogic.Python.xist.git``)

Create the release on the external and internal download server (do this
in the root directory)::

	make dist livinglogic


Creating and deploying the documenation
---------------------------------------

Recreate the documentation in ``docs/`` via (do this in the ``docs/``
subdirectory) and deploy it to ``python.livinglogic.de``::

	make clean download html deploy

As this has changed ``docs/DOWNLOAD.rst`` you need to check in the result and
push it to all repos.


Uploading the release to the cheeseshop
---------------------------------------

Upload the release to the chesseshop via (do this in the root directory)::

	make upload


Creating the Windows packages
-----------------------------

Tell the Windows people that there's a new XIST release and wait until they've
finished their release dance.

Go to the ``docs/`` subdirectory, recreate the documentation and deploy it::

	make clean download html deploy

Check in the result and push it to all repos.
