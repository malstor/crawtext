<<<<<<< HEAD
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
#import os, sys, shutil
from datetime import datetime as dt
from ..database import Database
from ..database import TaskDB
from utils import *

#import datetime as dt
#from database import *
# from page import Page
# from utils.url import *
# from query import Query
# #from scrapper.article import Article		
# from utils import *
# from packages.subprocess import subprocess

# import requests
# from page import Source
=======

import re
from datetime import datetime as dt
from ..database import Database
from ..database import TaskDB
# from .crawl_job import Crawl
# from .archive_job import Archive
# from .report_job import Report
# from .export_job import Export
# from .user_job import User
# from .debug_job import Debug
# from .list_job import List

>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215

class Job(object):
	'''defaut job class for worker'''
	DB = TaskDB()
	__COLL__ = DB.coll
	
<<<<<<< HEAD
	def __init__(self, doc): 
		
		self.name = doc['name']
		self.action = doc["action"]
=======
	def __init__(self, doc, debug):
		self.debug = debug
		if type(doc) == str:
			self.name = doc
		else:	
			self.name = doc["name"]
			self.action = doc["action"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		self.__data__ = self.__COLL__.find_one({"name":self.name})		
		self.project_name = re.sub('[^0-9a-zA-Z]+', '_', self.name)
		now = dt.now()
		self.date = now.replace(second=0, microsecond=0)
<<<<<<< HEAD
		for k,v in doc.items():
			setattr(self, k, v)
=======
		
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		#value from db
		self.__db__ = Database(self.project_name)
		self.__db__.create_colls(["results","sources", "logs", "queue", "treated"])
		self.active = True
		self.date = dt.now()
<<<<<<< HEAD
		# self._doc = doc
		self._logs = {}
		self._logs["msg"] = ""
		self._logs["date"] = self.date
		#self.active = True
		
	def __update_logs__(self):
=======
		self._doc = doc
		self._logs = {}
		self._logs["date"] = [self.date]
		self.active = True
	
	def get_values(self):
		self.__data__ = self.__COLL__.find_one({"name":self.name})
		if self.__data__ is not None:
			for n in self.__data__.items():
				setattr(self,k,v)

	def __update_logs__(self):	
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		if self.__data__ is None:
			if self._logs["status"] is True:
				self._logs["msg"]  = "No active '%s' job for project '%s'found" %(self.action, self.name)
				self.create()
<<<<<<< HEAD
=======
			
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		try:		
			_id = self.__data__['_id']
			self.__COLL__.update({"_id":_id}, {"$set":{"active":self._logs["status"]}})
			self.__COLL__.update({"_id":_id}, {"$push":{"status":self._logs}})
		except KeyError:
			pass
<<<<<<< HEAD
=======
		if self.debug is True:
			print self._logs["msg"]

>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		return self._logs["status"]
		
										
	def create(self):
		self._logs['step'] = "creation"
		question = "Do you want to create a new project with a %s job?" %self.action
		if ask_yes_no(question):
			
<<<<<<< HEAD
			for k,v in self.__dict__.items():
=======
			for k,v in self._doc.items():
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
				 if k[0] != "_" and k[0] != "-" and k not in ["add", "delete", "expand"]:
					 setattr(self,k,v)
			_id = self.__COLL__.insert(self.__repr__())
			self.__data__ = self.__COLL__.find_one({"_id":_id})
			self._logs['status'] = True
			self._logs["msg"] = "Sucessfully created project %s with task %s" %(self.name,self.action)
<<<<<<< HEAD
=======
			if self.debug is True:
				print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
			return self.__update_logs__()
		
	def update(self):
		if self.__data__ is None:
			self._logs["msg"]  = "No active '%s' job for project '%s'found" %(self.action, self.name)
			self.create()
		else:	
<<<<<<< HEAD
			self._logs["msg"] = "Updating %s job of project %s"%(self.action, self.name)
			print self._logs["msg"]
		
		updated_value = []	
		for k,v in self.__dict__.items():
			if k[0] != "_" and v not in self.__data__.values():
				updated_value.append(k)
				self.__COLL__.update({"_id":self.__data__["_id"]}, {"$set":{k:v}})
			elif k[0] == "date":
				self.__COLL__.update({"_id":self.__data__["_id"]}, {"$push":{"date":v}})
		
		if len(updated_value) == 0:
			self._logs["msg"] = "No change for '%s' job project %s. Parameters given are the same." %(self.action, self.name)
			self._logs["status"] = False

		else:	
			self._logs["status"] = True
			self._logs["msg"] = "Successfully updated '%s' job  for project '%s' with parameters: %s" %(self.action, self.name, ", ".join(updated_value))
			updated_value = []
		print self._logs["msg"]	
		self.__update_logs__()	
=======
			self._logs["step"] = "Updating %s job of project %s"%(self.action, self.name)
			
		self.updated_value = []	
		for k,v in self._doc.items():
			if k[0] != "_" and v not in self.__data__.values():
				self.updated_value.append(k)
				self.__COLL__.update({"_id":self.__data__["_id"]}, {"$set":{k:v}})
		if len(self.updated_value) == 0:
			self._logs["msg"] = "No change for '%s' job project %s. Parameters given are the same." %(self.action, self.name)
			self._logs["status"] = False
		else:	
			self._logs["status"] = True
			self._logs["msg"] = "Successfully updated '%s' job  for project '%s' with parameters: %s" %(self.action, self.name, ", ".join(self.updated_value))
		self.__update_logs__()
		if self.debug is True:
			print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		return self._logs['status']
	
	def start(self):
		if self.__data__ is None:
<<<<<<< HEAD
			print "No project %s found: job %s could not be started"%(self.name, self.action)
			return False
		else:
			_class = (self.action).capitalize()
			print "start", _class
			instance = globals()[_class]
			job = instance(self.__data__)
			return job.start()
			
	def stop(self):
		self._logs["step"] = "Stopping execution of job"
		self.__COLL__.update({"name":self.name, "action":self.action}, {"$push": {"status": self._logs}})
		for doc in self.job_list:
=======
			self._logs["msg"] = "No project %s found: job %s could not be started"%(self.name, self.action)
			print self._logs["msg"]
			return False
		else:
			_class = (self.action).capitalize()
			if self.debug is True:
				print self._logs["msg"]
			instance = globals()[_class]
			job = instance(self.__data__)
			return job.start()

	def stop(self):
		
		self._logs["step"] = "Stopping execution of job"
		self.__COLL__.update({"name":self.name, "action":self.action}, {"$push": {"status": self._logs}})
		for doc in self.__COLL__.find({"name": self.name}):
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
			func = doc["action"].capitalize()
			instance = globals()[func]
			job = instance(self.name)		
			self.__get_config__(job)
			job.stop()
			self.COLL.update({"name":self.name, "action":self.action}, {"$push": {"status": job.logs}})
			print (job.logs["msg"])
			self.COLL.update({"name":self.name}, {"$set": {"active": "False"}})	
			return self.COLL.update({"name":self.name, "action":self.action}, {"$push": {"status": self._logs}})
			
	def schedule(self):
		self._logs["step"] = "Scheduling project"
		if self.update():
			
			self._logs["status"] = True
			self._logs["msg"] = "Sucessfully schedule project"
<<<<<<< HEAD
		
		else:
			self._logs["status"] = True
			self._logs["msg"] = "No schedule done for project"
=======
		else:
			self._logs["status"] = True
			self._logs["msg"] = "No schedule done for project"
		if self.debug is True:
			print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		return self.__update_logs__()
		
	def unschedule(self):
		self._logs["step"] = "Unscheduling job"
<<<<<<< HEAD
		
		
=======
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		if self.name in self.__COLL__.distinct("name"):
			for n in self.__COLL__.find({"name": self.name}):
				self.__COLL__.remove({"name":n['name']})
			self._logs["msg"] = "All tasks of project %s has been sucessfully unscheduled." %(self.name)
			self._logs["status"] = False
			
		else:
			self._logs["msg"] = "No project %s found" %(self.name)	
			self._logs["status"] = False
<<<<<<< HEAD
		
=======
		if self.debug is True:
			print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		return self.__update_logs__()
	
	
	def delete(self):
		'''delete project and archive results'''
		self._logs["step"] = "Deleting job"
		self.active = False
		print self._logs["step"]
		if self.__data__ is None:
<<<<<<< HEAD
			print "No project %s found. check the name of your project" %(self.name)
=======
			self._logs["msg"] = "No project %s found. check the name of your project" %(self.name)
			print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
			return
		
		
		if self.__db__.use_coll("results").count() > 0 or self.__db__.use_coll("sources").count()> 0 or self.__db__.use_coll("logs").count()> 0:
			
			if ask_yes_no("Do you want to export first all data from project?"):
				job = Export(self.__repr__())
				job.start()
			if ask_yes_no("Do you want to delete all data from project?"):
				self.__db__.drop("collection", "results")
				self.__db__.drop("collection", "logs")
				self.__db__.drop("collection", "sources")
				self.__db__.client.drop_database(self.name)
			if ask_yes_no("Do you want to delete directory of the project?"):
				try:
					shutil.rmtree("%s") %("/"+self._project_name)
				except OSError:
					print "No directory for project found"
		else:
<<<<<<< HEAD
			print "No data found for project %s"%(self.name)
			try:
				shutil.rmtree(self.project_name)
				print "Deleting directory %s" %(self.project_name)
			except OSError:
				print "No directory %s for project found" %(self.project_name)
=======
			self._logs["msg"] = "No data found for project %s" %(self.name)
			try:
				shutil.rmtree(self.project_name)
				self._logs["msg"] = "Deleting directory %s" %(self.project_name)
			except OSError:
				self._logs["msg"] = "No directory %s for project found" %(self.project_name)
		if self.debug is True:
				print self._logs["msg"]
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		self.unschedule()
		#self.__COLL__.update({"name":self.name}, {"$set": {"active": "False"}})	
		self._logs["msg"] = "Project %s sucessfully deleted." %self.project_name
		self._logs["status"] = False
<<<<<<< HEAD
		self.__update_logs__()
=======
		if self.debug is True:
			print self._logs["msg"]
		self.__update_logs__()

>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
		return
	
	def show(self):
		
		print "\n===================="
		print (self.name.upper())
		print "===================="
		
		print "Activated job:%i\n" %(self.__COLL__.find({"name": self.name, "active":True}).count())
		for i, job in enumerate(self.__COLL__.find({"name": self.name})):
			i = i+1
			print "%i) Job: %s"%(i, job["action"])
			print "--------------"
			for k,v in job.items():
				if k == '_id' or k == 'status':
					continue
				if v is not False or v is not None:
					print k+":", v			
			print "--------------"
		
		print "____________________\n"
		return 
		
	
	def __repr__(self):
		'''representing public info'''
		self.__data__ = {}
		for k,v in self.__dict__.items():
			if k.startswith("_"):
				pass
			else:
				self.__data__[k] = v
		print self.__data__	
		return self.__data__
		
	def list(self):
		for doc in self.__COLL__.find({"name":self.project_name}):
			print doc['name'], doc['action'], doc['active']
<<<<<<< HEAD

		
				


			

		

			
=======
>>>>>>> 7285a69bf6a75db664c11c40a08cf2fe84d18215
