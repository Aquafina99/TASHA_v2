import io, json, os.path, sys
# This file is used to check if temp files exist.  If they exist, then they are opened for reading; if they do not exist, they will be open and write a new file

# Check if the exists
# Input: filename(String)
# Output: The file in read mode
def fileCheck(filename):
	if(os.path.isfile(filename)):
		try:
			with open(filename, 'r') as data_file:
				response = json.load(data_file)
				return response
		except IOError, ex:
			return "ERROR"
	return False

# Attempt to create and write to a new temp file.
# Input: filename(string), response(JSON object)
def fileWrite(filename, response):
	try:
		with open(filename, 'w+') as outfile:
			json.dump(response, outfile)
		return
	except IOError, ex:
		return "ERROR"

# Iterates through the temp folder and deletes all the temporary JSON files that were made.
def deleteTemps():
	for file in os.listdir("temp/"):
		if file.endswith(".txt"):
			file_string = "temp/" + file
			os.remove(file_string)
	
	return 
