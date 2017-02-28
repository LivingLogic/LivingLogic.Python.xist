import datetime

from ll import url


class File:
	def __init__(self, url):
		self.url = url
		name = url.file
		if name.endswith(".tar.gz") or name.endswith(".tar.bz2") or name.endswith(".zip"):
			self.type = "Source"
		elif name.endswith(".egg"):
			if "win32" in name:
				self.type = "Windows egg"
			elif "linux" in name:
				self.type = "Linux egg"
			else:
				self.type = "Egg"
			pos = name.rfind("py")
			if pos >= 0:
				version = name[pos+2:pos+5]
				self.type += " (Python %s)" % version
		elif name.endswith(".whl"):
			if "win32" in name or "win_amd64" in name:
				self.type = "Windows wheel"
			elif "linux" in name:
				self.type = "Linux wheel"
			elif "macosx" in name:
				self.type = "Mac wheel"
			else:
				self.type = "Wheel"
			pos = name.find("-cp")
			if pos >= 0:
				version = name[pos+3:].split("-")[0]
				version = ".".join(version)
				self.type += " (Python %s)" % version
		elif name.endswith(".exe"):
			self.type = "Windows installer"
			pos = name.rfind("py")
			if pos >= 0:
				version = name[pos+2:-4]
				self.type += " (Python %s)" % version
		elif name.endswith(".src.rpm"):
			self.type = "Source RPM"
		elif name.endswith(".rpm"):
			self.type = "Binary RPM"
		else:
			self.type = None
		self.size = url.size()
		self.url.scheme = "http"
		self.url.server = "ftp.livinglogic.de"

	def restfile(self):
		return "`{} <{}>`_".format(self.url.file, self.url)

	def restsize(self):
		return "{}K".format((self.size+511)//1024) # Round up


class Version:
	def __init__(self, version, date):
		self.version = version
		self.date = datetime.datetime.strptime(date, "%m/%d/%Y")
		u = url.URL("ssh://root@ftp.livinglogic.de/~ftp/pub/livinglogic/xist/")
		files = u/u.files("*-%s[-.][twpzc]*" % version)
		self.files = [File(f) for f in sorted(files, key=str)]

	def output(self, out):
		title = "{} (released {:%m/%d/%Y})".format(self.version, self.date)
		out()
		out()
		out(title)
		out("-" * len(title))
		out()
		if self.files:
			widthfile = max(len(f.restfile()) for f in self.files)
			widthtype = max(len(f.type or "") for f in self.files)
			widthsize = max(len(f.restsize()) for f in self.files)
			out(".. tabularcolumns:: |l|l|r|")
			out()
			out(".. rst-class:: download")
			out()
			out("=" * widthfile, "=" * widthtype, "=" * widthsize)
			out("{:{}} {:{}} {:{}}".format("File", widthfile, "Type", widthtype, "Size", widthsize))
			out("=" * widthfile, "=" * widthtype, "=" * widthsize)
			for f in self.files:
				out("{:{}} {:{}} {:{}}".format(f.restfile(), widthfile, f.type or "", widthtype, f.restsize(), widthsize))
			out("=" * widthfile, "=" * widthtype, "=" * widthsize)
		else:
			out("(no files for this version)")


with url.Context():
	versions = [
		Version("5.26", "02/28/2017"),
		Version("5.25.1", "02/15/2017"),
		Version("5.25", "02/13/2017"),
		Version("5.24", "02/12/2017"),
		Version("5.23", "12/16/2016"),
		Version("5.22.1", "11/02/2016"),
		Version("5.22", "10/18/2016"),
		Version("5.21", "09/19/2016"),
		Version("5.20.1", "08/04/2016"),
		Version("5.20", "07/29/2016"),
		Version("5.19.4", "06/30/2016"),
		Version("5.19.3", "06/29/2016"),
		Version("5.19.2", "06/21/2016"),
		Version("5.19.1", "06/20/2016"),
		Version("5.19", "06/14/2016"),
		Version("5.18", "05/17/2016"),
		Version("5.17.1", "05/10/2016"),
		Version("5.17", "05/04/2016"),
		Version("5.16", "04/13/2016"),
		Version("5.15.1", "03/21/2016"),
		Version("5.15", "03/18/2016"),
		Version("5.14.2", "03/02/2016"),
		Version("5.14.1", "12/04/2015"),
		Version("5.14", "12/02/2015"),
		Version("5.13.1", "06/12/2015"),
		Version("5.13", "12/18/2014"),
		Version("5.12.1", "12/09/2014"),
		Version("5.12", "11/07/2014"),
		Version("5.11", "10/29/2014"),
		Version("5.10", "10/09/2014"),
		Version("5.9.1", "09/29/2014"),
		Version("5.9", "09/22/2014"),
		Version("5.8.1", "06/18/2014"),
		Version("5.8", "05/05/2014"),
		Version("5.7.1", "02/13/2014"),
		Version("5.7", "01/30/2014"),
		Version("5.6", "01/28/2014"),
		Version("5.5.1", "01/27/2014"),
		Version("5.5", "01/23/2014"),
		Version("5.4.1", "12/18/2013"),
		Version("5.4", "11/29/2013"),
		Version("5.3", "10/28/2013"),
		Version("5.2.7", "10/15/2013"),
		Version("5.2.6", "10/15/2013"),
		Version("5.2.5", "10/09/2013"),
		Version("5.2.4", "10/09/2013"),
		Version("5.2.3", "10/09/2013"),
		Version("5.2.2", "10/07/2013"),
		Version("5.2.1", "10/02/2013"),
		Version("5.2", "10/01/2013"),
		Version("5.1", "08/02/2013"),
		Version("5.0", "06/04/2013"),
		Version("4.10", "03/04/2013"),
		Version("4.9.1", "01/17/2013"),
		Version("4.9", "01/17/2013"),
		Version("4.8", "01/15/2013"),
		Version("4.7", "01/11/2013"),
		Version("4.6", "12/18/2012"),
		Version("4.5", "11/29/2012"),
		Version("4.4", "11/08/2012"),
		Version("4.3.1", "11/06/2012"),
		Version("4.3", "11/02/2012"),
		Version("4.2", "10/22/2012"),
		Version("4.1.1", "10/04/2012"),
		Version("4.1", "10/02/2012"),
		Version("4.0", "08/08/2012"),
		Version("3.25", "08/12/2011"),
		Version("3.24.1", "08/10/2011"),
		Version("3.24", "08/09/2011"),
		Version("3.23.1", "07/28/2011"),
		Version("3.23", "07/20/2011"),
		Version("3.22", "07/14/2011"),
		Version("3.21", "06/03/2011"),
		Version("3.20.2", "05/23/2011"),
		Version("3.20.1", "05/18/2011"),
		Version("3.20", "05/05/2011"),
		Version("3.19", "04/26/2011"),
		Version("3.18.1", "04/13/2011"),
		Version("3.18", "04/08/2011"),
		Version("3.17.3", "03/02/2011"),
		Version("3.17.2", "02/25/2011"),
		Version("3.17.1", "02/25/2011"),
		Version("3.17", "02/24/2011"),
		Version("3.16", "01/21/2011"),
		Version("3.15.3", "11/26/2010"),
		Version("3.15.2", "11/25/2010"),
		Version("3.15.1", "11/24/2010"),
		Version("3.15", "11/09/2010"),
		Version("3.14", "11/05/2010"),
		Version("3.13", "10/22/2010"),
		Version("3.12.1", "10/21/2010"),
		Version("3.12", "10/21/2010"),
		Version("3.11.1", "10/18/2010"),
		Version("3.11", "10/15/2010"),
		Version("3.10.1", "10/13/2010"),
		Version("3.10", "09/24/2010"),
		Version("3.9", "08/04/2010"),
		Version("3.8.3", "07/29/2010"),
		Version("3.8.2", "06/21/2010"),
		Version("3.8.1", "06/17/2010"),
		Version("3.8", "06/15/2010"),
		Version("3.7.6", "05/14/2010"),
		Version("3.7.5", "04/19/2010"),
		Version("3.7.4", "03/25/2010"),
		Version("3.7.3", "02/27/2010"),
		Version("3.7.2", "02/26/2010"),
		Version("3.7.1", "02/08/2010"),
		Version("3.7", "09/10/2009"),
		Version("3.6.6", "07/09/2009"),
		Version("3.6.5", "06/02/2009"),
		Version("3.6.4", "03/19/2009"),
		Version("3.6.3", "03/02/2009"),
		Version("3.6.2", "02/16/2009"),
		Version("3.6.1", "01/27/2009"),
		Version("3.6", "12/31/2008"),
		Version("3.5", "12/05/2008"),
		Version("3.4.4", "09/16/2008"),
		Version("3.4.3", "09/09/2008"),
		Version("3.4.2", "09/03/2008"),
		Version("3.4.1", "08/29/2008"),
		Version("3.4", "08/19/2008"),
		Version("3.3.2", "07/15/2008"),
		Version("3.3.1", "07/14/2008"),
		Version("3.3", "07/11/2008"),
		Version("3.2.7", "05/16/2008"),
		Version("3.2.6", "05/07/2008"),
		Version("3.2.5", "04/11/2008"),
		Version("3.2.4", "04/02/2008"),
		Version("3.2.3", "03/04/2008"),
		Version("3.2.2", "02/25/2008"),
		Version("3.2.1", "02/05/2008"),
		Version("3.2", "02/01/2008"),
		Version("3.1", "01/18/2008"),
		Version("3.0", "01/07/2008"),
		Version("2.15.5", "07/17/2007"),
		Version("2.15.4", "07/16/2007"),
		Version("2.15.3", "07/16/2007"),
		Version("2.15.2", "01/24/2007"),
		Version("2.15.1", "09/25/2006"),
		Version("2.15", "09/24/2006"),
		Version("2.14.2", "07/04/2006"),
		Version("2.14.1", "06/29/2006"),
		Version("2.14", "06/28/2006"),
		Version("2.13", "10/31/2005"),
		Version("2.12", "10/13/2005"),
		Version("2.11", "07/29/2005"),
		Version("2.10", "05/20/2005"),
		Version("2.9", "04/21/2005"),
		Version("2.8.1", "03/22/2005"),
		Version("2.8", "01/03/2005"),
		Version("2.7", "11/24/2004"),
		Version("2.6.2", "06/06/2005"),
		Version("2.6.1", "11/02/2004"),
		Version("2.6", "10/26/2004"),
		Version("2.5", "06/30/2004"),
		Version("2.4.1", "01/05/2004"),
		Version("2.4", "01/02/2004"),
		Version("2.3", "12/08/2003"),
		Version("2.2", "07/31/2003"),
		Version("2.1.4", "06/13/2003"),
		Version("2.1.3", "05/07/2003"),
		Version("2.1.2", "02/27/2003"),
		Version("2.1.1", "02/11/2003"),
		Version("2.1", "12/09/2002"),
		Version("2.0.8", "11/20/2002"),
		Version("2.0.7", "11/12/2002"),
		Version("2.0.6", "11/11/2002"),
		Version("2.0.5", "11/11/2002"),
		Version("2.0.4", "11/08/2002"),
		Version("2.0.3", "10/30/2002"),
		Version("2.0.2", "10/21/2002"),
		Version("2.0.1", "10/17/2002"),
		Version("2.0", "10/16/2002"),
		Version("1.6.1", "08/25/2003"),
		Version("1.6", "07/02/2003"),
		Version("1.5.13", "07/01/2003"),
		Version("1.5.12", "06/17/2003"),
		Version("1.5.11", "06/13/2003"),
		Version("1.5.10", "06/13/2003"),
		Version("1.5.9", "04/30/2003"),
		Version("1.5.8", "02/27/2003"),
		Version("1.5.7", "11/12/2002"),
		Version("1.5.6", "11/11/2002"),
		Version("1.5.5", "11/11/2002"),
		Version("1.5.4", "09/30/2002"),
		Version("1.5.3", "09/25/2002"),
		Version("1.5.2", "09/19/2002"),
		Version("1.5.1", "09/17/2002"),
		Version("1.5", "08/27/2002"),
		Version("1.4.5", "06/18/2002"),
		Version("1.4.4", "06/16/2002"),
		Version("1.4.3", "04/29/2002"),
		Version("1.4.2", "03/22/2002"),
		Version("1.4.1", "03/21/2002"),
		Version("1.4", "03/18/2002"),
		Version("1.3.1", "03/14/2002"),
		Version("1.3", "02/12/2002"),
		Version("1.2.5", "12/03/2001"),
		Version("1.2.4", "11/23/2001"),
		Version("1.2.3", "11/22/2001"),
		Version("1.2.2", "11/16/2001"),
		Version("1.2.1", "10/08/2001"),
		Version("1.2", "10/03/2001"),
		Version("1.1.3", "09/17/2001"),
		Version("1.1.2", "08/21/2001"),
		Version("1.1.1", "08/01/2001"),
		Version("1.1", "07/19/2001"),
		Version("1.0", "06/18/2001"),
		Version("0.4.7", "11/24/2000"),
		Version("0.4.6", "11/03/2000"),
		Version("0.4.5", "11/01/2000"),
		Version("0.4.4", "10/27/2000"),
		Version("0.4.3", "10/19/2000"),
		Version("0.4.2", "09/24/2000"),
		Version("0.4.1", "09/21/2000"),
		Version("0.4", "09/19/2000"),
		Version("0.3.9", "08/10/2000"),
		Version("0.3.8", "07/14/2000"),
		Version("0.3.7", "07/06/2000"),
		Version("0.3.6", "07/04/2000"),
		Version("0.3.5", "07/02/2000"),
		Version("0.3.4", "05/31/2000"),
		Version("0.3.3", "05/30/2000"),
		Version("0.3.2", "05/26/2000"),
		Version("0.3.1", "05/25/2000"),
		Version("0.3", "05/25/2000"),
		Version("0.2", "05/17/2000"),
		Version("0.1.1", "05/16/2000"),
		Version("0.1", "05/15/2000"),
	]


def makedownloads():
	download = list(open("DOWNLOAD.rst", "r", encoding="utf-8"))

	newdownload = []

	def out(*args):
		newdownload.append(" ".join(str(part) for part in args))

	inauto = False

	for line in download:
		line = line.rstrip()
		if inauto:
			if line == ".. autogenerate end":
				for version in versions:
					version.output(out)
				out()
				out()
				out(line)
				inauto = False
			else:
				pass # Skip original content
		else:
			if line == ".. autogenerate start":
				inauto = True
			out(line)

	with open("DOWNLOAD.rst", "w", encoding="utf-8") as f:
		f.write("\n".join(newdownload))


if __name__ == "__main__":
	makedownloads()
