from bitstring import BitArray
import re

# Python3 program to print 1's and 2's 
# complement of a binary number 

# Returns '0' for '1' and '1' for '0' 
def flip(c): 
	return '1' if (c == '0') else '0'

# Print 1's and 2's complement of 
# binary number represented by "bin" 

def onesComplement(bin): 

	n = len(bin) 
	ones = "" 
	twos = "" 
	
	# for ones complement flip every bit 
	for i in range(n): 
		ones += flip(bin[i]) 

	# for two's complement go from right 
	# to left in ones complement and if 
	# we get 1 make, we make them 0 and 
	# keep going left when we get first 
	# 0, make that 1 and go out of loop 
	ones = list(ones.strip("")) 
	twos = list(ones) 
	for i in range(n - 1, -1, -1): 
	
		if (ones[i] == '1'): 
			twos[i] = '0'
		else:		 
			twos[i] = '1'
			break

	i -= 1	
	# If No break : all are 1 as in 111 or 11111 
	# in such case, add extra 1 at beginning 
	if (i == -1): 
		twos.insert(0, '1') 

	# print("1's complement: ", *ones, sep = "") 
	# print("2's complement: ", *twos, sep = "") 
	return "".join(ones)

def twosComplement(bin): 

	n = len(bin) 
	ones = "" 
	twos = "" 
	
	# for ones complement flip every bit 
	for i in range(n): 
		ones += flip(bin[i]) 

	# for two's complement go from right 
	# to left in ones complement and if 
	# we get 1 make, we make them 0 and 
	# keep going left when we get first 
	# 0, make that 1 and go out of loop 
	ones = list(ones.strip("")) 
	twos = list(ones) 
	for i in range(n - 1, -1, -1): 
	
		if (ones[i] == '1'): 
			twos[i] = '0'
		else:		 
			twos[i] = '1'
			break

	i -= 1	
	# If No break : all are 1 as in 111 or 11111 
	# in such case, add extra 1 at beginning 
	if (i == -1): 
		twos.insert(0, '1') 

	# print("1's complement: ", *ones, sep = "") 
	# print("2's complement: ", *twos, sep = "") 
	return "".join(twos)

def equality(one, two):
	if one == two:
		return True 
	else:
		return False
	
# Driver Code 
# if __name__ == '__main__': 
# 	bin = "1100"
# 	print(printOneAndTwosComplement(bin.strip("")))
	
# This code is contributed 
# by SHUBHAMSINGH10 


# Python Solution for above problem:

# This function adds two binary 
# strings return the resulting string
def add_binary_nums(x, y):
		max_len = max(len(x), len(y))

		x = x.zfill(max_len)
		y = y.zfill(max_len)
		
		# initialize the result
		result = ''
		
		# initialize the carry
		carry = 0

		# Traverse the string
		for i in range(max_len - 1, -1, -1):
			r = carry
			r += 1 if x[i] == '1' else 0
			r += 1 if y[i] == '1' else 0
			result = ('1' if r % 2 == 1 else '0') + result
			carry = 0 if r < 2 else 1	 # Compute the carry.
		
		if carry !=0 : result = '1' + result

		return result.zfill(max_len)[-max_len:]

def left_shift(num, rot):
	value = BitArray(bin=num).int
	res = (value << rot) & 0xFFFFFFFF
	return format(res, 'b')

def righ_shift(num, rot):
	res = num[:len(num)-rot]
	res = res.zfill(len(num))
	return res

def XOR(a,b):
	res = ''
	for i in range(len(a)):
		if (a[i] == '1' and b[i] == '1') or (a[i] == '0' and b[i] == '0'):
			res += '0'
		else:
			res += '1'
	return res

def XOR3(a,b,c):
	a1 = BitArray(bin=a).int
	b1 = BitArray(bin=b).int
	c1 = BitArray(bin=c).int
	res = a1 ^ b1 ^ c1
	res = format(res, 'b')
	res = re.sub('-', '1', res)
	return res.zfill(len(a))

def AND(a,b):
	res = ''
	for i in range(len(a)):
		if a[i] == '1' and b[i] == '1':
			res += '1'
		else:
			res += '0'
	return res

def NOT(a):
	a1 = BitArray(bin=a).int
	res = ~a1
	return format(res, 'b')

INT_BITS = 32

def rightRotate(s, d):
	res = s[-d:]+s[:len(s)-d]
	return res

def getChoice(e,f,g):
	res = ''
	for i in range(len(e)):
		if e[i] == '1':
			res += f[i]
		else:
			res += g[i]
	return res
	




# Driver code 
#print(add_binary_nums('1101', '100'))

# This code is contributed 
# by Anand Khatri

# d12comps = printOneAndTwosComplement("10100101010011111111010100111010")
# print(d12comps)
# print(add_binary_nums('00001000001100000000001100001111', d12comps))


