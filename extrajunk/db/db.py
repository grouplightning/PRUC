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
		self.cur.close() #
		self.conn.close() #close the database connection

	def query(self,query): #execute a query on the database and provide the cursor for result data iteration
		self.cur.execute(query)
		return self.cur

	def escape(self,value): # escape a string for safe use in a query (quotation marks, etc)
		return self.conn.escape(value)

	def getSensor(self,id): # get all information about a particular sensor
		results = self.query("SELECT * FROM sensors WHERE id="+self.escape(id)+" LIMIT 1")
		for row in results:
			return row

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

	def createSensor(self,id,name):
		id = self.escape(id)
		name = self.escape(name)
		self.query("INSERT INTO sensors (id,name) VALUES ("+id+","+name+")")
		self.conn.commit()
		return self.cur.lastrowid # return the internal sensorid number

	def deleteSensor(self,id):
		id = self.escape(id)
		self.query("DELETE FROM sensors WHERE id="+id)
		self.conn.commit()

	def updateSensor(self,id,name):
		id = self.escape(id)
		name = self.escape(name)
		self.query("UPDATE sensors SET name="+name+" WHERE id="+id)
		self.conn.commit()


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
