"""Get metadata, info and content from book"""


import base64
import os
import re
import sys
from time import time

import bs4

# fix relative import  of workspace packages
try:
	sys.path.insert(1, os.getcwd())
	from structures import BookDescription
except ImportError:
	pass


def get_images(fb2_text: str, ids: list[str] = None) -> dict[str, bytes]:
	"""get images binaries from fb2 file and return their ids and content in bytes

	Args:
		fb2_text (str): entity of fb2 file. Better if entities is bytes due to encodings error
		ids (list[str], optional): images ids for finding, 
			if None find all images in file. Defaults to None.

	Returns:
		dict[str, bytes]: images id and content
	"""

	parsed_data = bs4.BeautifulSoup(fb2_text, 'lxml')
	if ids is None:
		imgs_binaries = parsed_data.find_all('binary')
	else:
		imgs_binaries = parsed_data.find_all('binary', {'id': ids})

	imgs = {
            img['id']: base64.b64decode(img.text)
            for img in imgs_binaries
	}

	return imgs


def get_description(fb2_text: str) -> BookDescription:
	"""Parse description of book such as encoding, title, cover, translators and etc.

	Args:
		fb2_text (str): entity of fb2 file. Better if entities is bytes due to encodings error

	Returns:
		BookMetaData: hidden book data. See in structures.BookMetaData
	
	"""
	description = {}

	try:
		metadata = re.findall(bytes(r'<\?.+?\?>', 'utf-8'), fb2_text)[0]
		encoding = re.findall(
			bytes(r'(?<=encoding=").+?(?=")', 'utf-8'),
			metadata
		)[0]
		description['encoding'] = encoding.decode()
	except IndexError:
		description['encoding'] = None

	parsed_data = bs4.BeautifulSoup(fb2_text, 'lxml')
	title_block = parsed_data.find('title-info')
	document_block = parsed_data.find('document-info')
	publish_block = parsed_data.find('publish-info')
	blocks = {
		'title_info': title_block,
		'document_info': document_block,
		'publish_info': publish_block
	}
	
	for block_name, block in blocks.items():
		if block is None:
			description[block_name] = None
			continue

		tags = set(el.name for el in block.children if el.name)
		block_info = {}
		for tag in tags:
			elements = [el.text for el in block.find_all(tag)]
			elements = [el.strip() for el in elements]
			if elements:
				block_info[tag] = elements
		
		description[block_name] = block_info

	book_descr = BookDescription(**description)
	return book_descr
	

if __name__ == '__main__':
	successful = 0
	failed = 0

	for file_name in os.listdir('test_files/fb2'):
		file_path = os.path.join('test_files/fb2', file_name)
		print(file_name)
		with open(file_path, 'rb') as f:
			book_descr = get_description(f.read())
			encoding = book_descr.encoding

		with open(file_path, 'r', encoding=encoding) as f:
			st = time()
			text = f.read()
			imgs = get_images(text)
			for img in imgs:
				try:
					img_content = imgs[img]

					with open(f'test_files/test_imgs/{img}', 'wb') as img_file:
						img_file.write(img_content)

					successful += 1
					print('\t', img)
				except:
					failed += 1
		print(time() - st)

	print(
		f'Images scanned: {successful + failed} Success: {successful} Failed: {failed}')
