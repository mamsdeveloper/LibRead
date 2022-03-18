"""Get metadata, info and content from book"""


import base64
from io import BytesIO
import os
import re
from time import time

import bs4
from PIL import Image


def get_images(fb2_text: str, ids: list[str] = None) -> dict[str, bytes]:
	"""get images binaries from fb2 file and return their ids and content in bytes

	Args:
		fb2_text (str): entity of fb2 file
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


if __name__ == '__main__':
	successful = 0
	failed = 0

	for file_name in os.listdir('test_files/fb2'):
		file_path = os.path.join('test_files/fb2', file_name)
		print(file_name)
		with open(file_path, 'rb') as f:
			head = f.readline()

			encoding = re.findall(bytes(r'(?<=encoding=").+?(?=")', 'utf-8'), head)[0]
			encoding = encoding.decode('utf-8')

		with open(file_path, 'r', encoding=encoding) as f:		
			st = time()
			text = f.read()
			imgs = get_images(text)
			for img in imgs:
				try:
					img_content = imgs[img]
					pil_img = Image.open(BytesIO(img_content))
					# pil_img.show()

					# with open(f'test_files/test_imgs/{time()}.png', 'wb') as img_file:
					# 	img_file.write(img_content)
						
					successful += 1
					print('\t', img)
				except:
					failed += 1
		print(time() - st)

	print(f'Images scanned: {successful + failed} Success: {successful} Failed: {failed}')
