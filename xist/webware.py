from Webware import WebKit
from xist import xsc

class Servlet(WebKit.HTTPServlet):
	encoding = "utf-8"

	def respondToGet(self, trans):
		trans._response.write(self.content().asBytes(encoding=self.encoding))

	def content(self, trans):
		return xsc.Null
