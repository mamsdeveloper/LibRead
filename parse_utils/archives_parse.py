"""Finding books in library`s archives"""

import os
from time import time
from typing import Generator
from zipfile import BadZipFile, ZipFile


def get_books_pathes(archives_path: str) -> Generator[tuple[str, str], None, None]:
	"""Return path to fb2 file in archive for each book.
	Result may be unordered.
	
	Args:
		archives_path (str): path to folder, where archives with books located

	Yields:
		Generator[tuple[str, str], None, None]: file name without extention 
												and path to it in archive 
	"""

	archives = os.listdir(archives_path)
	for arch_name in archives:
		arch_path = os.path.join(archives_path, arch_name)
		try:
			with ZipFile(arch_path, 'r') as arch:
				for file in arch.filelist:
					file_name = os.path.splitext(file.filename)[0]
					file_path = os.path.join(arch_path, file.filename)
					yield (file_name, file_path)
		except BadZipFile:
			yield None, arch_path


def get_book(book_path: str) -> str:
	"""Get entity of book from library

	Args:
		book_path (str): path to book (from get_books_pathes)

	Returns:
		_type_: unzipped book text
	"""
	arch_path, file_name = os.path.split(book_path)
	with ZipFile(arch_path, 'r') as arch:
		with arch.open(file_name) as file:
			return file.read()


if __name__ == '__main__':
	path = 'test_files/books'

	k = 0
	st = time()
	for name, path in get_books_pathes(path):
		k += 1
		if name is not None:
			get_book(path)

	print(time() - st, k)
