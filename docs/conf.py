from pathlib import Path
import sys


sys.path.append(Path(__file__).parent.parent)


project = 'HPOS Seed'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.asciinema',
    'sphinxcontrib.mermaid',
]


html_favicon = 'favicon.ico'
html_show_copyright = False
html_show_sourcelink = False
html_theme = 'alabaster'
html_theme_options = {
    'description': 'Wormhole-based <code>hpos-config.json</code> transfer '
                   'library, CLI, and desktop app',
    'github_user': 'Holo-Host',
    'github_repo': 'hpos-seed',
    'show_powered_by': False,
}


intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7', 'python-3.7.inv'),
    'twisted': ('https://twistedmatrix.com/documents/19.7.0/api',
                'twisted-19.7.0.inv'),
}
