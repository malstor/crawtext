from scheduler import Scheduler

if __name__ == "__main__":
	s = Scheduler()
	for n in s.get_list():
		print n
		if n["action"] == "crawl":
			s.run_job(n)
	
	
		
	
	
	
	
