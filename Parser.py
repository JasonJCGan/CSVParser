import os, json, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument(dest="file_Name")
args = parser.parse_args()

def filter_Commas(data, isHeader):
	quotations = 0
	commaCounter = 0

	for index, char in enumerate(data):
		# Check for headers that contain  ',' inside quotations
		if char == '"' and quotations == 0:
			quotations = 1
			continue
		if char == '"' and quotations == 1:
			quotations = 0
			continue

		if char == ',' and quotations == 1:
			commaCounter += 1
			data =  data[:index] + "_" + data[index+1:]
			if (isHeader):
				# +1 for 0 base index, +1 for n-1 number of commas per word
				print("Header #" + str(commaCounter + 2) + " Contains a comma delimiter, it will be replaced by '_'.")

	return data

def filter_Headers(file):
	# Strip special lead/trail characters, then filter unwanted commas

	headers = file.readline().lstrip().rstrip()
	headers = filter_Commas(headers, 1).split(',')
	invalid_Indices = []

	for i, key in enumerate(headers):

		# Remove double quotes to avoid escape characters

		headers[i] = headers[i].replace('"','')

		# Check for headers that are empty ''

		if key == "":
			invalid_Indices.append(i)

	return (invalid_Indices, headers)

def convert_CSV(file_Name):
	# file extension check
	if (not file_Name.endswith('csv')): 
		sys.exit("Failed to parse. Please provide a .csv file !")

	print("Begin Parsing : " + file_Name)
	print("------------------------------")

	try:
		file = open(file_Name, 'r')
	except:
		print("Unable to open file, " + file_Name + " may be corrupted")
		
	invalid_Indices, headers = filter_Headers(file)
	data_Entries = []

	for line in file:
		this_Object = {}
		line_Empty = 1
		this_Line = filter_Commas(line.lstrip().rstrip(), 0).split(',')
		print(this_Line)

		for index, key in enumerate(headers):
			if index in invalid_Indices:
				continue
			if this_Line[index] != '':
				line_Empty = 0
				this_Object[key] = this_Line[index].replace('"','')
			else:
				this_Object[key] = ""

		# Make data entry only if theres atleast 1 column of input

		if line_Empty != 1:
			data_Entries.append(this_Object)

	# Write out results
	nf = open(file_Name.replace('.csv', '.json'), 'w')
	nf.write(json.dumps(data_Entries))
	print ("Finished Parsing CSV to : " + file_Name.replace('.csv', '.json'))

convert_CSV(args.file_Name)