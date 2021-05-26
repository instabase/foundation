#!/usr/bin/env python3

"""Package Blueprint for Instabase Marketplace distribution."""

import datetime
import json
import os
import shutil

from pathlib import Path


def sanitize_for_path(s: str) -> str:
  """Sanitize a string for use as part of a path.

  Deletes slashes, spaces, etc.
  """
  s = s.replace(' ', '_')
  s = s.replace('/', '_')
  s = s.replace(':', '-')
  return s

TIMESTAMP = sanitize_for_path(str(datetime.datetime.now()))

FOUNDATION_VERSION = '0.0.14'

# Configure paths
# ===============

SCRIPT_DIR = Path(__file__).absolute().parent
BLUEPRINT_DIR = SCRIPT_DIR / '../py/foundation'

STATIC_RESOURCES_DIR = SCRIPT_DIR / 'static_resources'
ICON_PATH = STATIC_RESOURCES_DIR / 'icon.png'

OUTPUT_DIR = SCRIPT_DIR / 'output' / f'{TIMESTAMP}-{FOUNDATION_VERSION}'
IBSOLUTION_FILENAME = f'foundation-{FOUNDATION_VERSION}.ibsolution'
IBSOLUTION_PATH = OUTPUT_DIR / IBSOLUTION_FILENAME

# We put everything into this package directory, and then zip its contents to
# make the .ibsolution file.
PACKAGE_DIR = OUTPUT_DIR / 'package_contents'

# Filenames to use in the package zip file's folder structure. These are
# hard-coded in the IB source. (September 15, 2020.)
IB_PACKAGE_JSON_FILENAME = 'package.json'
IB_ICON_FILENAME = 'icon.png'
IB_SRC_DIRNAME = 'src'

# Populate PACKAGE_DIR
# ====================

os.makedirs(PACKAGE_DIR)

package_json = {
  'name': 'foundation', # This is also the name of the Python library
                        # you call `import` on in UDFs.
  'version': FOUNDATION_VERSION,
  'icon_url': IB_ICON_FILENAME, # The docs say this has to be here even though
                                # it is only allowed to have one value?
  'keywords': 'extraction, internal',
  'solution_type': 'pypkg',
  'short_description': 'Foundation',
  'long_description': 'Foundation',
  'category': 'extraction',
  'authors': ['Instabase'],
}
(PACKAGE_DIR / IB_PACKAGE_JSON_FILENAME).write_text(
  json.dumps(package_json, indent=4, separators=(',', ': ')))

shutil.copy(ICON_PATH, PACKAGE_DIR / IB_ICON_FILENAME)

for root, dirs, files in os.walk(BLUEPRINT_DIR):
  for filename in files:
    _, extension = os.path.splitext(filename)
    if extension == '.py':
      full_path = os.path.join(root, filename)
      rel_path = os.path.relpath(full_path, BLUEPRINT_DIR)
      target = PACKAGE_DIR / IB_SRC_DIRNAME / rel_path
      target.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy(full_path, target)

# Make the .ibsolution
# ====================

shutil.make_archive(IBSOLUTION_PATH, 'zip', PACKAGE_DIR)
Path(str(IBSOLUTION_PATH) + '.zip').rename(IBSOLUTION_PATH)

# Instabase eats shit when it encounters a folder in a zip file.
from zipfile import ZipFile
IBSOLUTION_HACK = Path(str(IBSOLUTION_PATH) + '.hack')
with ZipFile(IBSOLUTION_PATH) as original:
  with ZipFile(IBSOLUTION_HACK, mode='w') as hack:
    for entry in original.infolist():
      if not entry.is_dir():
        hack.writestr(entry.filename, original.read(entry.filename))
    hack.close()
  original.close()
IBSOLUTION_HACK.rename(IBSOLUTION_PATH)
# ...

print(OUTPUT_DIR) # Makes it easy to open the folder where output is written.
