import HTTPServlet
from xist import xsc

class Servlet(HTTPServlet.HTTPServlet):
	encoding = "utf-8"

	def respondToGet(self, trans):
		trans._response.write(self.content(trans).asHTML().asBytes(encoding=self.encoding))

	def content(self, trans):
		return xsc.Null
