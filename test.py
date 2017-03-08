import re

m = re.search(r'(\d)_\d*.png','D:\\CaptchaSingle\\0_13165.png')
print(m.group(1))