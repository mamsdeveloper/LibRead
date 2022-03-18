"""That module provides parsing of inpx and inp files 
that contain information about books in library

"""

import os
import re
import sys
from typing import Generator
from zipfile import ZipFile


# fix relative import  of workspace packages
try:
	sys.path.insert(1, os.getcwd())
	from structures import Book
except ImportError:
	pass


def get_inpx_entities(inpx_path: str) -> Generator[str, None, None]:
	"""Yield entity of inp files that contains in inpx files

	Args:
		inpx_path (str): path to inpx file

	Yields:
		Generator[str]: entities of inp files in utf-8 codec
	"""

	with ZipFile(inpx_path, 'r') as inpx:
		for inp_info in inpx.filelist:
			if inp_info.filename.endswith('.inp'):
				with inpx.open(inp_info, 'r') as inp:
					yield inp.read().decode('utf-8')


def get_inp_data(inp_text: str) -> Generator[Book, None, None]:
	"""Get list of books information from text in inp format

	Args:
		inp (str): text in inp format

	Returns:
		list[Book]: information about each book in file
	"""

	inp_text = inp_text.replace('\r', '')
	lines = inp_text.split('\n')
	for line in lines:
		if line:
			columns = re.split(r'', line)
			book = Book.from_inp(columns)
			yield book


if __name__ == '__main__':
	path = 'test_files/inpx/flibusta_fb2_local.inpx'
	# path = 'tets_files/inpx/librusec_local_fb2.inpx'
	for inp in get_inpx_entities(path):
		for book in get_inp_data(inp):
			print(book.title, book.date)


	# Books
	# Authors
	# Genres
	# Series
