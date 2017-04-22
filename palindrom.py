def is_palindrome(s):
	i = 0
	j = len(s) - 1
	while(i < j):
		if s[i] != s[j]:
			return False
		i = i+1
		j = j-1
	return True

s = [
	'thissiht',
	'one',
	'noon',
	'moon',
]
for si in s:
	print '{} is {} palindrome'.format(si, '' if is_palindrome(si) else 'not')