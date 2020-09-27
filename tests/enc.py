from base64 import b64encode

key = "rocket"

with open('test.txt', 'r') as fi:
	lines = fi.readlines()
	lines = [line[:-1] for line in lines]

i = 0
with open('outfile.txt', 'wb') as outfi:
	for line in lines:
		enc = b""
		for char in line:
			enc += bytes([(ord(char) ^ ord(key[i]))])
			i = (i + 1) % len(key)
		enced = b64encode(enc)
		outfi.write(enced)
		outfi.write(b'\n')
