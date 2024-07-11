

def getdate():
	import datetime

	d=str(datetime.datetime.now())
	d=d.split(".")[0].split()[0].strip()



	print(d)
	return d
if __name__ == '__main__':
	getdate()

