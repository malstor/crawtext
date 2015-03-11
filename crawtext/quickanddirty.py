#!/usr/bin/env python
# -*- coding: utf-8 -*-

__name__ = "crawtext"
__version__ = "4.3.1"
__doc__ = '''Crawtext.
Description:
A simple crawler in command line for targeted websearch.

Usage:
	crawtext.py (<name>)
	crawtext.py <name> --query=<query> --key=<key> [--nb=<nb>] [--lang=<lang>] [--user=<email>] [--depth=<depth>] [--debug]
	crawtext.py (<name>) delete
	crawtext.py (<name>) start
	crawtext.py (<name>) report
'''
import os, sys, re
import copy
from docopt import docopt
from datetime import datetime as dt
from database import *
from random import choice
import datetime
#from url import Link
from report import send_mail, generate_report
import hashlib
from article import Article, Page
from config_qd import *



ABSPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
RESULT_PATH = os.path.join(ABSPATH, "projects")
import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(file="crawtext.log", format=FORMAT, level=logging.DEBUG)
#search result nb from BING
MAX_RESULTS = 1000
#max depth
DEPTH = 100

class Worker(object):
	def __init__(self,user_input,debug=False):
		'''Job main config'''
		if type(user_input) == str:
			self.name = user_input
			self.show()
			sys.exit()
		else:
			self.db = TaskDB()
			self.coll = self.db.coll
			self.__parse__(user_input)
			if self.debug:
				logging.info("Debug activated")
			if self.delete is True:
				self.delete_project()
				sys.exit()
			if self.start is True:
				self.__run__()
				sys.exit()
				
			if self.__exists__():
				self.__show__(self.name)
				sys.exit()
			else:
				logging.info("creating")
				self.__create__()
				logging.info("RUN!!!!!!!!!!!!!!!!!!!")
				self.__run__()
					
			#
			# self.project_name = re.sub('[^0-9a-zA-Z]+', '_', self.name)
			# self.query = user_input['--query']
			# self.key = user_input['--key']
			#
			# if self.__exists__(self.name):
			#     self.__show__(self.name)
			# else:
			#     logging.info("create and run")
	def __parse__(self, user_input):
		for k, v in user_input.items():
			if v is not False or v is not None:
			# if k in ["--nb","--lang", "--user", "--depth", "--debug", '<name>', '--query', '--key']:
			#     if v is None:
			#         setattr(self, re.sub("--", "", k), False)
			#     else:
				setattr(self, re.sub("--|<|>", "", k), v)
			else:
				setattr(self, re.sub("--", "", k), False)
		if self.name is not False:
			self.project_name = re.sub('[^0-9a-zA-Z]+', '_', self.name)
		else:
			logging.warning("Invalid parameters")
			sys.exit()
		if self.query is False or self.key is False:
			logging.warning("Invalid parameters")
			sys.exit()
		self.report = bool(self.user is not None)
		if self.nb is False or self.nb is None:
			self.nb = MAX_RESULTS
		if self.depth is False or self.depth is None:
			self.depth = DEPTH
		self.date = dt.now()
	
	def __create_directory__(self, project_name):
			self.directory = os.path.join(ABSPATH, project_name)
			if not os.path.exists(self.directory):
				os.makedirs(self.directory)
				index = os.path.join(self.directory, 'index')
				try:
					self.index_dir = os.makedirs('index')
				except OSError, e:
					if e.errno != 17:
						raise   
				logging.info("A specific directory has been created to store your projects\n Location:%s"	%(self.directory))
				
			return self.directory
			
	def __create_db__(self, project_name=None):
		if project_name is not None:
			self.project_name = project_name
		self.project_db = Database(self.project_name)
		self.project_db.create_colls(["results", "logs", "sources", "queue"])
		
	def __create__(self):
		logging.info("creating a new task")
		new_task = self.__dict__.items()
		task = {}
		task["type"] = "crawl"
		task["action"] = ["Created"]


		for k, v in new_task:
			if k not in ["db", "coll"]:
				task[k] = v
		try:
			task["status"] = [True]
			task["msg"] = ["Sucessfully created"]
			task["date"] = [self.date]
			task["directory"] = self.__create_directory__(task["project_name"])
			self.coll.insert(task)
			self.__create_db__(self.project_name)
			logging.info("Task successfully created")
			return True
			
		except Exception as e:
			logging.warning("Task not created")
			logging.warning(e)
			return False
	def __config__(self):
		pass
		
	def __run__(self):
		if self.__exists__():
			if self.query is not False and self.key is not False:
				#put bing to sources and nexts urls to crawl
				if self.insert_into_sources():
					treated = self.push_to_queue()
					logging.info("%d urls put into queue" %len(treated))
					self.crawl(treated)
				
			else:
				logging.warning("Invalid parameter check your key and your query")
				sys.exit()

		else:
			logging.info("Exit")
			sys.exit()
	def insert_into_sources(self):
		check, bing_sources = self.get_bing_results(self.query, self.key, self.nb)
		logging.info(check)
		if check is True:
			
			total_bing_sources = len(bing_sources)
			logging.info("%d sources i n BING" %total_bing_sources)
			logging.info("Inserting %d into sources" %total_bing_sources)
			for i,url in enumerate(bing_sources):
				self.project_db.sources.insert({"url":url,
												"source_url": "https://api.datamarket.azure.com",
												"depth": 0, 
												"nb":i,
												"total":total_bing_sources,
												"msg":["inserted"],
												"code": [100],
												"status": [True]})
				return True
		else:
			logging.info(bing_sources)
			return False
	
	def crawl(self,treated):
		logging.info("Starting Crawl")
		print len(self.project_db.queue.distinct("url"))
		while self.project_db.queue.count() > 0:
			for item in self.project_db.queue.find(timeout=False):
				if item["url"] not in treated and self.project_db.logs.find_one({"url":item["url"]}) is None and self.project_db.results.find_one({"url":item["url"]}) is None:
					p = Page(item["url"], item["source_url"],item["depth"], item["date"], self.debug)
					if p.download():
						a = Article(p.url,p.html, p.source_url, p.depth,p.date, self.debug)
						if a.extract() and a.filter(self.query, self.directory):
							if a.check_depth(self.depth):
								a.fetch_links()
								if len(a.links) > 0:
									for url, domain, domain_id in zip(a.links, a.domains, a.domain_ids):	
										print url, domain
										self.project_db.queue.insert({"url": url, "source_url": item['url'], "depth": int(item['depth'])+1, "url_id": domain_id, "domain": domain, "date": a.date})
								if self.debug: logging.info("\t-inserted %d nexts url" %len(a.links))
								self.project_db.insert_result(a.export())
						else:
							self.project_db.insert_log(a.log())
					else:
						self.project_db.insert_log(a.log())
					treated.append(item["url"])
				self.project_db.queue.remove({"url":item["url"]})
				if self.project_db.queue.count() == 0:
					break
				if self.project_db.results.count() > 200000:
					for n in self.project_db.results.find({"depth":max(self.project_db.results.distinct("depth"))}, timeout=False):
						self.project_db.results.remove({"_id":n["_id"]})
					logging.info("Max results exceeeded %d results now" %self.project_db.results.count())
					self.project_db.queue.drop()
					break
			if self.project_db.queue.count() == 0:
				break
		return True

	def push_to_queue(self):
		treated = []
		logging.info("Treated %d" %len(treated))
		#put bing urls to crawl
		for item in self.project_db.sources.find():
			logging.info("in source "+item["url"])
			if item["url"] not in treated:
				logging.info("Treating %s" %item["url"])
				p = Page(item["url"], item["source_url"],item["depth"], self.date, self.debug)
				logging.info("Page "+p.url)
				if p.download():
					a = Article(p.url,p.html, p.source_url, p.depth,p.date, self.debug)
					if a.extract():
						a.fetch_links()
						logging.info("Treating next %d links" %len(a.links))
						for url, domain, id_url in zip(a.links, a.domains, a.domain_ids):
							
							if url not in treated:
								logging.info("sending %s into queue" %url)
								self.project_db.queue.insert({"url": url, "id_url":id_url, "source_url": item['url'], "depth": int(item['depth'])+1, "domain": domain, "date": self.date})
						self.project_db.insert_result(a.export())
						self.project_db.sources.update({"_id":item["_id"]}, {"$push":{"status": True, "msg":"Ok", "code": 100}})
					else:
						self.project_db.sources.update({"_id":item["_id"]}, {"$push":{"status": False, "msg":a.msg, "code": a.code}})
				else:
					logging.info("error downloading")
					self.project_db.sources.update({"_id":item["_id"]}, {"$push":{"status": False, "msg":p.msg, "code": p.code}})
				treated.append(item["url"])
		return treated

	def __exists__(self):
		self.task = self.coll.find_one({"name":self.name})
		if self.task is not None:
			logging.info("\nProject %s exists" %self.name)
			return True
		else:
			return False

	def __show__(self,name):
		print "\n===== Project : %s =====\n" %(self.name).capitalize()
		print "* Parameters"
		print "------------"
		for k, v in self.task.items():
			
			print k, ":", v
		project_db = Database(self.task["project_name"])
		project_db.create_colls(["sources", "queue", "results"])
		print "Sources nb:", project_db.sources.count()
		print "Queue nb:", project_db.queue.count()
		print "Results nb:", project_db.results.count()
		print "\n* Last Status"
		print "------------"
		print self.task["action"][-1], self.task["status"][-1],self.task["msg"][-1], dt.strftime(self.task["date"][-1], "%d/%m/%y %H:%M:%S")
		return
		
	def get_bing_results(self, query, key, nb):
		''' Method to extract results from BING API (Limited to 5000 req/month) return a list of url'''
		start = 0
		step = 50
		if nb > MAX_RESULTS:
			logging.warning("Maximum search results is %d results." %MAX_RESULTS)
			nb = MAX_RESULTS

		if nb%50 != 0:
			nb = nb - (nb%50)
		web_results = []
		new = []
		inserted = []
		for i in range(0,nb, 50):
			
			try:
				r = requests.get('https://api.datamarket.azure.com/Bing/Search/v1/Web',
					params={'$format' : 'json',
						'$skip' : i,
						'$top': step,
						'Query' : '\'%s\'' %query,
						},auth=(key, key)
						)
				# logging.info(r.status_code)
				msg = r.raise_for_status()
				if msg is None:
					web_results.extend([e["Url"] for e in r.json()['d']['results']])
					logging.info(len(web_results))
				else:
					logging.warning("Req :"+msg)
			except Exception as e:
				logging.warning("Exception: "+str(e))
				
				return (False, str(e))
		return (True, web_results)
	
	def delete_project(self):
		if self.__exists__():
			self.delete_db()
			self.delete_dir()
			self.coll.remove({"_id": self.task['_id']})
			print "Project %s: sucessfully deleted"%(self.name)
			return True
		else:
			print "No crawl job %s found" %self.name
			return False
			
	def delete_dir(self):
		import shutil
		directory = os.path.join(RESULT_PATH, self.project_name)
		if os.path.exists(directory):

			print "We will delete this directory now!"

			shutil.rmtree(directory)
			print "Directory %s: %s sucessfully deleted"    %(self.name,directory)
			return True
		else:
			print "No directory found for crawl project %s" %(str(self.name))
			return False

	def delete_db(self):
		db = Database(self.project_name)
		db.drop_db()
		logging.info("Database %s: sucessfully deleted" %self.project_name)
		return True

def uniq(seq):
	checked = []
	for e in seq:
		if e not in checked:
			checked.append(e)
	logging.info("remove duplicate %d" %len(duplicate))
	return checked

w = Worker(docopt(__doc__))
