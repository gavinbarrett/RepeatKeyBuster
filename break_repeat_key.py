#!/usr/bin/env python3
from os import path
from sys import argv, exit
from base64 import b64decode
from collections import defaultdict

freq_table = [8.12,1.49,2.71,4.32,12.02,2.30,2.03,5.92,7.31,0.10,0.69,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.10,2.88,1.11,2.09,0.17,2.11,0.07,18.29]

def compute_exp(c, n_obs, l):
	if ((c > 96) and (c < 123)):
		c -= 97
		return freq_table[c] * l
	elif ((c > 64) and (c < 91)):
		c -= 65
		return freq_table[c] * l
	elif (c == 32):
		c -= 6
		return freq_table[c]
	else:
		return n_obs

def compute_obs(c, string):
	sz = len(string)
	acc = 0.0
	for i in string:
		if (i == c):
			acc+=1
	return acc / sz

def score_code(newcode):
	sz = len(newcode)
	acc = 0.0
	for i in newcode:
		n_obs = compute_obs(i, newcode)
		n_exp = compute_exp(ord(i), n_obs, len(newcode))
		if (n_exp == 0):
			continue
		n = (n_obs - n_exp)
		acc += ((n*n)/n_exp)
	return acc

def break_cipher(code):
	clen = len(code)
	score = 0.0
	sc = 0.0
	plaintext = ''
	key = 0
	for i in range(0, 255):
		newcode = []
		for j in range(clen):
			newcode += chr(code[j] ^ i)
		sc = score_code(newcode)
		if sc > score:
			score = sc
			plaintext = newcode
			key = chr(i)
	return plaintext, key, score

def pop_count(c):
	count = 0
	while (c > 0):
		if (c & 0x01) == 1:
			count += 1
		c >>= 1
	return count

def hamming(str1, str2):
	count = 0
	for i in range(len(str1)):
		count += pop_count(str1[i] ^ str2[i])
	return (count * 1.0)

def solve_blocks(blocks):
	keys = []
	sc = 0
	for block in blocks:
		plaintext, key, score = break_cipher(block)
		keys += [key]
		sc += score
	return ''.join(keys), sc

def get_hamming(base, size):
	bs = [base[i:i+size] for i in range(0,len(base),size)]
	if not all(len(b) == size for b in bs):
		bs = bs[:-1]
	ham = 0
	ham += hamming(bs[0],bs[1])/size
	ham += hamming(bs[1],bs[2])/size
	ham += hamming(bs[2],bs[3])/size
	ham += hamming(bs[3],bs[4])/size
	return ham/size

def get_file_contents(fi):
	with open(fi, 'r') as f:
		b64 = ""
		for line in f:
			b64 += line[:-1]
		return b64decode(b64)

def get_key_sizes(base):
	inf = float('inf')
	key_sizes = []
	for i in range(2,40):
		h = get_hamming(base, i)
		if (h < inf):
			inf = h
			key = i
			key_sizes += [i]
	return key_sizes

def decrypt(base, repeat_key):
	a = 0
	print(f'Ciphertext:\n')
	for i in base:
		c = bytes([i ^ ord(repeat_key[a])])
		a = (a + 1) % len(repeat_key)
		print(c.decode(), end='')

def crack_xor(arg):
	# decode file contents
	base = get_file_contents(arg)
	
	# find the best key sizes
	key_sizes = get_key_sizes(base)
	key_sizes = key_sizes[len(key_sizes)-7:]
	# try each key
	sc = 0
	key = ''
	for k in key_sizes:
		
		# split the ciphertexts into size k blocks
		cipherblocks = [list(base[j:j+k]) for j in range(0,len(base),k)]
		
		# remove the last block if it is less than k in length
		if not all(len(c) == k for c in cipherblocks):
			cipherblocks = cipherblocks[:-1]
		
		# transpose the blocks
		transposed_blocks = list(zip(*cipherblocks))
		
		# solve each block as a single byte xor
		repeat_key, score = solve_blocks(transposed_blocks)
		#print(f'repeat_key: {repeat_key} score: {score}\n')
		if score > sc:
			sc = score
			key = repeat_key
	# decrypt the ciphertext with the key	
	print(f'Key:\n{key}\n')
	decrypt(base, key)
	

def main():
	if (len(argv) != 2):
		print('Incorrect number of arguments.\nUsage: ./break_repeat_key.py <enrypted_text_file>')
		exit()
	if (path.exists(argv[1]) and path.isfile(argv[1])):
		crack_xor(argv[1])
	else:
		print('Cannot open input file.')
		exit()

if __name__ == "__main__":
	main()
