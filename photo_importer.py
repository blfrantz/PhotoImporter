"""
A simple script for importing photos from a memory card
to a computer.  Source/destinations are configured via constants
to make the CLI dead-simple under the assumption that these 
won't change much, but an argparse interface could be added
for improved flexibility.
"""

import os
from datetime import datetime
import shutil
import argparse

from tqdm import tqdm

SONY_TASKS = [
  {
    'src': 'K:\\DCIM\\100MSDCF',
    'ext': 'ARW',
    'dest': 'O:\\Personal Data\\Pictures'
  },
  {
    'src': 'K:\\PRIVATE\\M4ROOT\\CLIP',
    'ext': 'MP4',
    'dest': 'O:\\Video Editing\\Raw'
  }
]

PANA_TASKS = [
  {
    'src': 'K:\\DCIM\\120_PANA',
    'ext': 'RW2',
    'dest': 'O:\\Personal Data\\Pictures'
  },
  {
    'src': 'K:\\DCIM\\121_PANA',
    'ext': 'RW2',
    'dest': 'O:\\Personal Data\\Pictures'
  },
  {
    'src': 'K:\\PRIVATE\\AVCHD\\BDMV\\STREAM',
    'ext': 'MTS',
    'dest': 'O:\\Video Editing\\Raw'
  }
]

DATE_FMT = '%Y%m%d'
INC_FMT = '{:0>3d}'
DELETE_AFTER_COPY = True


class PhotoImporter:

  def __init__(self, tasks, delete=DELETE_AFTER_COPY):
    self._tasks = tasks
    self._delete = delete

    self._last_date = ''
    self._date_count = 0

  def run(self):
    i = 1
    for task in self._tasks:
      print('Running task {} of {}'.format(i, len(self._tasks)))
      for f in tqdm(os.listdir(task['src'])):
        file_path = os.path.join(task['src'], f)
        if os.path.isfile(file_path) and f.endswith(task['ext']):
            self.import_file(file_path, task['dest'])
      i = i + 1

  def import_file(self, file_path, dest):
    new_name = self.rename(file_path)
    new_path = os.path.join(dest, new_name)

    try:
      self.transfer(file_path, new_path)
    except IOError as e:
      os.makedirs(os.path.dirname(new_path))
      self.transfer(file_path, new_path)

  def transfer(self, src, dest):
    if os.path.exists(dest):
      split_path = os.path.splitext(dest)
      new_dest = split_path[0] + 'b' + split_path[1]
      self.transfer(src, new_dest)
    else:
      if self._delete:
        shutil.move(src, dest)
      else:
        shutil.copy2(src, dest)

  def rename(self, file_path):
    """ Define your rename logic here."""

    file_ext = os.path.splitext(os.path.basename(file_path))[1]
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    date_str = mod_time.strftime(DATE_FMT)

    if date_str != self._last_date:
      self._date_count = 0
      self._last_date = date_str
    else:
      self._date_count = self._date_count + 1

    count_str = INC_FMT.format(self._date_count)

    year = mod_time.strftime('%Y')
    month = mod_time.strftime('%B')
    new_name = date_str + '-' + count_str + file_ext

    return  os.path.join(year, month, new_name)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Import photos and videos.')
  parser.add_argument('--cam', required=True)
  args = parser.parse_args()

  if args.cam == 'sony':
    PhotoImporter(SONY_TASKS).run()
  elif args.cam =='pana' or args.cam == 'panasonic':
    PhotoImporter(PANA_TASKS).run()
  else:
    'Camera not recognized.'