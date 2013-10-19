import os
import re
import shutil

from bs4 import BeautifulSoup
from gears.environment import Environment
from gears.finders import FileSystemFinder
from gears.processors import hexdigest_paths



#hack to exclude 3rd party css from external locations
hexdigest_paths.URL_RE = re.compile(r"""url\((?!//)(['"]?)\s*(.*?)\s*\1\)""")

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SOURCE_DIR = os.path.join(ROOT_DIR, '_public')
DEST_DIR = os.path.join(ROOT_DIR, '_out')


def delete_unused_files(manifest):
  for k, v in manifest.files.items():

    if k.endswith('css') or k.endswith('js'):
      #use the fingerprinted html files
      path = os.path.join(DEST_DIR, k)
    else:
      #don't use the fingerprinted html files
      path = os.path.join(DEST_DIR, v)

    os.remove(path)

  os.remove(os.path.join(DEST_DIR, '.manifest.json'))


def reference_fingerprinted_files(env):
  filename = os.path.join(env.root, 'index.html')

  # lxml does a better job of closing tags correctly when using jade
  # jade doesn't close meta, link tags, etc and the default BS HTML parser gets confused and produces unmatched tags
  soup = BeautifulSoup(open(filename), 'lxml')

  assets_to_rewrite = soup.findAll('script') + soup.findAll('link', {'rel': 'stylesheet'})

  for asset in assets_to_rewrite:
    path_type = 'src'
    path = asset.get(path_type)

    if not path:
      path_type = 'href'
      path = asset.get(path_type)

    #check if path exists - it might just be an inline style or script
    if path and not path.startswith('http'):
      fingerprint_path = env.manifest.files[path]

      asset[path_type] = fingerprint_path

  with open(filename, 'wb') as f:
    f.write(unicode(soup.prettify()))


def delete_dest():
  if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR)

if __name__ == '__main__':
  #clean slate
  delete_dest()

  #defines where files will be emitted
  env = Environment(DEST_DIR, public_assets=(
    lambda path: any(path.endswith(ext) for ext in ('.css', '.js', '.html')),
    lambda path: any(path.startswith(ext) for ext in ('fonts')))
  )

  env.finders.register(FileSystemFinder([SOURCE_DIR]))
  env.register_defaults()

  env.save()
  reference_fingerprinted_files(env)
  delete_unused_files(env.manifest)