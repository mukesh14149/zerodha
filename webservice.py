import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# GET CURRENT DIRECTORY
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env=Environment(loader=FileSystemLoader(CUR_DIR),
trim_blocks=True)


class ShowStockInfo(object):
	@cherrypy.expose
	def index(self):
		template = env.get_template('stock.html')
		stocklist = []
		for i in range(10):
			stock = []
			stock.append(r.lindex('SC_CODE', i))
			stock.append(r.lindex('SC_NAME', i))
			stock.append(r.lindex('OPEN', i))
			stock.append(r.lindex('HIGH', i))
			stock.append(r.lindex('LOW', i))
			stock.append(r.lindex('CLOSE', i))
			stocklist.append(stock)
		# RENDER TEMPLATE PASSING IN DATA
		return template.render(stocklist=stocklist)

	@cherrypy.expose
	def search(self, name):
		template = env.get_template('stock.html')
		pos = -1
		for i in range(r.llen('SC_NAME')):
			if(r.lindex('SC_NAME',i).strip()==name.strip()):
				pos=i
		stocklist = []
		stock = []
		stock.append(r.lindex('SC_CODE', pos))
		stock.append(r.lindex('SC_NAME', pos))
		stock.append(r.lindex('OPEN', pos))
		stock.append(r.lindex('HIGH', pos))
		stock.append(r.lindex('LOW', pos))
		stock.append(r.lindex('CLOSE', pos))
		stocklist.append(stock)
		if(pos==-1):
			return "DATA NOT FOUND"
		return template.render(stocklist=stocklist)

if __name__ == '__main__':

	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		
		"/css": {"tools.staticdir.on": True,
		 	"tools.staticdir.dir": os.path.abspath("./css"),
		 },
	}
	cherrypy.quickstart(ShowStockInfo(), '/', conf)
