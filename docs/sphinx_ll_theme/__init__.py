"""
LivingLogic Sphinx theme.

Based on Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""
from os import path

from sphinx.writers import html5

__version__ = '0.2'
__version_full__ = __version__


class HTML5Translator(html5.HTML5Translator):
	def visit_desc_returns(self, node):
		self.body.append(' <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint">')

	def depart_desc_returns(self, node):
		self.body.append('</span></span>')


def get_html_theme_path() -> str:
	"""
	Return list of HTML theme paths.
	"""
	cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
	return cur_dir


# See https://www.sphinx-doc.org/en/master/development/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
	app.require_sphinx("3.5")
	app.add_html_theme('sphinx_ll_theme', path.abspath(path.dirname(__file__)))
	app.set_translator("html", HTML5Translator, True)
