import pymysql as sql






class DB:

	def __init__(self): #create db resources when the program starts using the db
		#connect to our database server and select the PARKS database
		# 3306 = default mysql port
		print("Connecting to database...")
		self.conn = sql.connect(host='127.0.0.1', port=3306, user='lightning', passwd='wichita', db='hubdb')
		self.cur = self.conn.cursor() #

	def __del__(self): #cleanup database resources when the program stops using db
		print("Freeing database...")
		try:
			self.cur.close() #
			self.conn.close() #close the database connection
		except:
			pass

	def query(self,query): #execute a query on the database and provide the cursor for result data iteration
		self.cur.execute(query)
		return self.cur

	def escape(self,value): # escape a string for safe use in a query (quotation marks, etc)
		return self.conn.escape(value)

	def getSensor(self,id): # get all information about a particular sensor
		results = self.query("SELECT * FROM sensors WHERE id="+self.escape(id)+" LIMIT 1")
		for row in results:
			return row

	def addCounts(self,sensor,time,people,horses,dogs,vehicles,bicycles,unknown):
		sensor = self.escape(sensor)
		time = self.escape(time) #time is entered as a date string, and so must be escaped
		dogs = self.escape(dogs)
		people = self.escape(people)
		horses = self.escape(horses)
		vehicles = self.escape(vehicles)
		bicycles = self.escape(bicycles)
		unknown = self.escape(unknown)
		#print("UPDATE counts SET count_people=%s, count_horses=%s, count_dogs=%s, count_vehicles=%s, count_bicycles=%s, count_unknown=%s WHERE sensor=%s and time=%s" % (people,horses,dogs,vehicles,bicycles,unknown,sensor,time) )
		self.query("UPDATE counts SET count_people=count_people+%s, count_horses=count_horses+%s, count_dogs=count_dogs+%s, count_vehicles=count_vehicles+%s, count_bicycles=count_bicycles+%s, count_unknown=count_unknown+%s WHERE sensor=%s and time=%s LIMIT 1" % (people,horses,dogs,vehicles,bicycles,unknown,sensor,time) )
		self.conn.commit()
		return self.cur.lastrowid

	def createCountsStub(self,sensor,time):
		sensor = self.escape(sensor)
		time = self.escape(time) #time is entered as a date string, and so must be escaped
		self.query("INSERT INTO counts (sensor,time,count_people,count_horses,count_dogs,count_vehicles,count_bicycles,count_unknown) VALUES (%s,%s,0,0,0,0,0,0)" % (sensor,time))
		self.conn.commit()
		return self.cur.lastrowid

	def doesCountsExist(self, sensor, time):
		sensor = self.escape(sensor)
		time = self.escape(time) #time is entered as a date string, and so must be escaped
		results = self.query("SELECT * FROM counts WHERE sensor=%s and time=%s LIMIT 1" % (sensor,time))
		for row in results:
			return True
		return False

	def createCounts(self, sensor, time, people, horses, dogs, vehicles, bicycles, unknown): #add new counts instance for a given time to the database
		sensor = self.escape(sensor)
		time = self.escape(time) #time is entered as a date string, and so must be escaped
		dogs = self.escape(dogs)
		people = self.escape(people)
		horses = self.escape(horses)
		vehicles = self.escape(vehicles)
		bicycles = self.escape(bicycles)
		unknown = self.escape(unknown)
		self.query("INSERT INTO counts (sensor,time,count_people,count_horses,count_dogs,count_vehicles,count_bicycles,count_unknown) VALUES ("+sensor+","+time+","+people+","+horses+","+dogs+","+vehicles+","+bicycles+","+unknown+")");
		self.conn.commit() # make the changes we specify
		return self.cur.lastrowid # return the id of the count record added

	def pruneCounts(self,time_before): #delete old counts before a specified date
		time_before = self.escape(time_before)
		self.query("DELETE FROM counts WHERE time<"+time_before)
		self.conn.commit()

	#outdated method - can be used to create a temporary sensor entry to be updated later
	def createSensor(self, id, name):
		"""
		Create a temporary sensor entry to have data identifying the sensor added later.
		:param id: the internal id of the sensor
		:param name: the user-set name of the sensor
		:return: row id added
		"""
		id = self.escape(id)
		name = self.escape(name)
		self.query("INSERT INTO sensors (id,name) VALUES (%s,%s)" % (id, name))
		self.conn.commit()
		return self.cur.lastrowid # return the internal row number (sensorid when using autoincrement)
		#TODO: need to check lastrowid behavior / choose id type in our sensor table (autoincrement int would be easiest)

	def createSensor(self,id,name,mac,ip):
		"""
		Create a sensor database entry that has fully denied information (name,mac,ip)
		:param id: the internal id of the sensor
		:param name: the user-set name of the sensor
		:param mac: the MAC address of the sensor
		:param ip: the IP address of the sensor
		:return: row id added
		"""
		id = self.escape(id)
		name = self.escape(name)
		self.query("INSERT INTO sensors (id,name,mac,ip) VALUES (%s,%s,%s,%s)" % (id,name,mac,ip) )
		self.conn.commit()
		return self.cur.lastrowid # return the internal row number (sensorid when using autoincrement)
		#TODO: need to check lastrowid behavior / choose id type in our sensor table (autoincrement int would be easiest)

	def deleteSensor(self,id):
		id = self.escape(id)
		self.query("DELETE FROM sensors WHERE id="+id)
		self.conn.commit()

	def updateSensor(self,id,name,mac,ip):
		id = self.escape(id)
		name = self.escape(name)
		self.query("UPDATE sensors SET name=%s, mac=%s, ip=%s WHERE id=%s" % (name,mac,ip,id))
		self.conn.commit()

"""
db = DB();
result = db.getSensor(7)
print(result)



db.createCounts(7,"2019-01-01 01:02:03",1,2,3,4,5,6)
db.createSensor(7,"west")


#db.deleteSensor(9)
db.updateSensor(7,"northwest")
#sensor_id = db.createSensor("north")

#print(sensor_id)
#db.pruneCounts("2019-04-05 01:02:03");

results = db.query("SELECT * FROM sensors")
for row in results:
	print(row)

"""
