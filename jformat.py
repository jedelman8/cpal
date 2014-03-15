import json
import pandums

def pretty(data):
	print json.dumps(data,indent=5)

def createRow(device,headings):
	
	row = []

	for header in headings:
		check = header.split('.')
		num = len(check)
		a = 1
		temp = device.facts
		for c in check:
			if a == num:
				final = temp[check[a-1]]
				row.append(final)
			else:
				temp = temp[check[a-1]]
			a = a + 1

	return row

def createDict(devices,headings):
	diction = {}
	for device in devices:
		local = {}
		
		for header in headings:
			check = header.split('.')
			num = len(check)
			a = 1
			temp = device.facts
			for c in check:
				if a == num:
					final = temp[c]
					local[c] = final
				else:
					temp = temp[c]
				a = a + 1
			
		diction[device.facts['var_name']] = local

	return diction

def f_old(devices,headings):
	
	upper_head = []

	#converting headings into an array to allow for the requesting of values that are more than 1 deep in the dictionary
	for heading in headings:
		if '.' in heading:
			check = heading.split('.')
			upper_head.append(check[-1].upper())
		else:
			upper_head.append(heading.upper())


	
	table = []	
	table.append(upper_head)	# titles of each column
	for device in devices:

		table.append(createRow(device,headings))  #every ohter row

	pandums.pprint_table(table) 

	return createDict(devices,headings)  #while it prints a table, it returns a dictionary
def c2(device,headings):
	
	row = []

	for header in headings:
		check = header.split('.')
		num = len(check)
		a = 1
		temp = device.facts
		for c in check:
			if a == num:
				final = temp[check[a-1]]
				row.append(final)
			else:
				temp = temp[check[a-1]]
			a = a + 1

	return row

def facts_table(devices,headings):

	uppercase_headings = []
	headings_no_equal = []
	exact_match_elements = []
	match_values = []
	c = 0
	for heading in headings:
		if '=' in heading:
			exact_match_elements.append(c)
			strip = heading.split('=')
			match_values.append(strip[-1])
			if '.' in strip[0]:
				again = strip[0].split('.')
				uppercase_headings.append(again[1].upper())
				headings_no_equal.append(strip[0])
			else:
				uppercase_headings.append(strip[0].upper())
				headings_no_equal.append(strip[0])
		elif '.' in heading:
			strip = heading.split('.')
			uppercase_headings.append(strip[1].upper())
			headings_no_equal.append(heading)
		else:
			uppercase_headings.append(heading.upper())
			headings_no_equal.append(heading)
		c = c + 1

	table = []
	table.append(uppercase_headings)
	matches = len(exact_match_elements)

	for device in devices:
		row = c2(device,headings_no_equal)
		c = 0

		if matches == 0:
			table.append(row)
		elif matches == 1:
			if row[exact_match_elements[0]] == match_values[0]:
				table.append(row)
		elif matches == 2:
			if row[exact_match_elements[0]] == match_values[0] and row[exact_match_elements[1]] == match_values[1]:
				table.append(row)
		else:
			if matches == 3:
				if row[exact_match_elements[0]] == match_values[0] and row[exact_match_elements[1]] == match_values[1] and row[exact_match_elements[2]] == match_values[2]:
					table.append(row)
			
	print ''
	pandums.pprint_table(table)
	print ''

