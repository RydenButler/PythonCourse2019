## Trick and explanation of base conversion
## http://www.purplemath.com/modules/base_why.htm

"""convert positive integer to base 2"""
def binarify(num):
	result = []
	while num != 0:
		result.append(num%2)
		num //= 2
	return ''.join(str(i) for i in result[::-1])


"""convert positive integer to a string in any base"""
def int_to_base(num, base):
	result = []
	while num != 0:
		result.append(num%base)
		num //= base
	return ''.join(str(i) for i in result[::-1])


"""take a string-formatted number and its base and return the base-10 integer"""
def base_to_int(string, base):
	powers = [int(i) for i in list(string)][::-1]
	answer = 0
	for i in range(len(powers)):
		answer += powers[i]*base**i
	return answer


"""add two numbers of different bases and return the sum"""
def flexibase_add(str1, str2, base1, base2):
	return base_to_int(str1, base1) + base_to_int(str2, base2)


"""multiply two numbers of different bases and return the product"""
def flexibase_multiply(str1, str2, base1, base2):
	return base_to_int(str1, base1) * base_to_int(str2, base2)


"""given an integer, return the Roman numeral version"""
def romanify(num):
	numerals = {1 : 'I', 4 : 'IV', 5 : 'V', 9: 'IX', 10 : 'X', 40 : 'XL', 50 : 'L', 90 : 'XC', 100 : 'C', 400 : 'CD', 500 : 'D', 900 : 'CM', 1000 : 'M'}
	required = []
	for i in sorted(numerals.keys())[::-1]:
		while num >= i:
			required.append(i)
			num -= i
	return ''.join(numerals[i] for i in required)

romanify(1234)
  
# Copyright (c) 2014 Matt Dickenson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.