# Check string is a number
def str_is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False