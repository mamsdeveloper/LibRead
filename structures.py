from typing import NamedTuple
from datetime import datetime


class Book(NamedTuple):
	"""Represents a book"""
	authors: list[str]
	genres: list[str]
	title: str
	series: str
	series_num: int
	file_name: str
	size: int
	index: int
	deleted: bool
	extension: str
	date: datetime
	lang: str
	rate: int
	keywords: list[str]

	@classmethod
	def from_inp(cls, line_items: list[str]):
		"""Get values from splitted line of inp file

		Args:
			line_items (list[str]): items from one inp file line
		"""
		# unpacking values from splitted inp row
		# incorrect data must be caught later
		(
			authors, genres, title,
			series, series_num, file_name,
			size, index, deleted,
			extension, date, lang,
			rate, keywords
		) = line_items

		authors = [' '.join(a.split(',')) for a in authors[:-1].split(':')]
		genres = genres[:-1].split(':')
		series_num = int(series_num) if series_num.isdigit() else 0
		size = int(size) if size.isdigit() else 0
		index = int(index)
		deleted = bool(deleted)
		date = datetime.strptime(date, '%Y-%m-%d')
		rate = int(rate) if rate.isdigit() else 0
		keywords = keywords.split(', ')

		book = cls(authors, genres, title, series, series_num, file_name,
		           size, index, deleted, extension, date, lang, rate, keywords)

		return book


class BookDescription(NamedTuple):
	"""Book information such as encoding, title, publicher and etc"""
	encoding: str
	title_info: dict[str, str]
	document_info: dict[str, str]
	document_info: dict[str, str]
	publish_info: dict[str, str]


if __name__ == '__main__':
	data = [
            ['Киселев,Сергей,Владимирович', 'Пригорницкий,Юрий,Григорьевич'],
            ['sf'],
            'Стріла Всесвіту',
            'Пригоди. Фантастика',
            '1985',
            '168183',
            '2141253',
            '168183',
            '0',
            'fb2',
            '2009-10-16',
            'uk',
            '2',
            ['Науково-фантастичні оповідання']
        ]

	book = Book(*data)

	print(book.title, book.date)
