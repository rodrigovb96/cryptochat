import os

def create_file(file_path,data):
	dirname,filename = os.path.split(file_path)

	if(not os.path.isfile(file_path)):
		if (not os.path.isdir(dirname)):
			os.makedirs(dirname)

		with open(file_path,'w') as file:
			file.write(data)	
		
		return True
	
	return False

def read_file(file_path):
	if(not os.path.isfile(file_path)):
		return False
	else:
		with open(file_path,'r') as file:
			return file.read()
