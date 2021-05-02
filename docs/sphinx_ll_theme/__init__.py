"""
LivingLogic Sphinx theme.

Based on Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""
from os import path

__version__ = '0.2'
__version_full__ = __version__


def get_html_theme_path() -> str:
	"""
	Return list of HTML theme paths.
	"""
	cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
	return cur_dir


# See https://www.sphinx-doc.org/en/master/development/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
	app.add_html_theme('sphinx_ll_theme', path.abspath(path.dirname(__file__)))
