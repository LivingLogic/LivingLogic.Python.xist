import datetime

from ll import url


class File:
	def __init__(self, url_):
		self.url = url_
		name = url_.file
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
				self.type += f" (Python {version})"
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
				version = f"{version[0]}.{version[1:]}"
				self.type += f" (Python {version})"
		elif name.endswith((".exe", ".msi")):
			self.type = "Windows installer"
			pos = name.rfind("py")
			if pos >= 0:
				version = name[pos+2:-4]
				self.type += f" (Python {version})"
		elif name.endswith(".src.rpm"):
			self.type = "Source RPM"
		elif name.endswith(".rpm"):
			self.type = "Binary RPM"
		else:
			self.type = None
		self.size = url_.size()
		# Use the official http download URL (instead of the ssh one)
		self.url = url.URL(f"http://python-downloads.livinglogic.de/download/xist/{self.url.file}")

	def restfile(self):
		return f"`{self.url.file} <{self.url}>`_"

	def restsize(self):
		size = (self.size+511)//1024 # Round up
		return f"{size}K"


class Version:
	def __init__(self, version, date):
		self.version = version
		self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
		u = url.URL("ssh://livpython@python-downloads.livinglogic.de/~/public_downloads/xist/")
		files = u/u.files(f"*-{version}[-.][twpzc]*")
		self.files = [File(f) for f in sorted(files, key=str)]

	def output(self, out):
		title = f"{self.version} (released {self.date:%m/%d/%Y})"
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
			out(f"{'File':{widthfile}} {'Type':{widthtype}} Size")
			out("=" * widthfile, "=" * widthtype, "=" * widthsize)
			for f in self.files:
				out(f"{f.restfile():{widthfile}} {f.type or '':{widthtype}} {f.restsize()}")
			out("=" * widthfile, "=" * widthtype, "=" * widthsize)
		else:
			out("(no files for this version)")


with url.Context():
	versions = [
		Version("5.82", "2025-12-01"),
		Version("5.81", "2025-11-21"),
		Version("5.80.1", "2025-07-22"),
		Version("5.80", "2025-07-14"),
		Version("5.79", "2025-04-11"),
		Version("5.78", "2025-03-17"),
		Version("5.77", "2024-11-13"),
		Version("5.76", "2024-07-08"),
		Version("5.75.1", "2024-04-11"),
		Version("5.75", "2023-11-21"),
		Version("5.74", "2023-03-01"),
		Version("5.73.2", "2022-08-16"),
		Version("5.73.1", "2022-08-10"),
		Version("5.73", "2022-08-10"),
		Version("5.72", "2022-08-04"),
		Version("5.71", "2022-07-08"),
		Version("5.70", "2022-03-11"),
		Version("5.69.1", "2021-12-13"),
		Version("5.69", "2021-11-17"),
		Version("5.68.1", "2021-09-23"),
		Version("5.68", "2021-08-04"),
		Version("5.67.2", "2021-06-30"),
		Version("5.67.1", "2021-06-28"),
		Version("5.67", "2021-06-25"),
		Version("5.66.1", "2021-06-24"),
		Version("5.66", "2021-06-15"),
		Version("5.65", "2021-01-13"),
		Version("5.64", "2020-10-30"),
		Version("5.63.1", "2020-10-26"),
		Version("5.63", "2020-09-08"),
		Version("5.62", "2020-07-13"),
		Version("5.61.2", "2020-07-09"),
		Version("5.61.1", "2020-07-09"),
		Version("5.61", "2020-07-07"),
		Version("5.60", "2020-07-03"),
		Version("5.59", "2020-06-30"),
		Version("5.58", "2020-06-12"),
		Version("5.57", "2020-04-14"),
		Version("5.56", "2019-12-12"),
		Version("5.55", "2019-11-11"),
		Version("5.54.1", "2019-10-24"),
		Version("5.54", "2019-10-24"),
		Version("5.53", "2019-09-30"),
		Version("5.52.1", "2019-09-05"),
		Version("5.52", "2019-07-29"),
		Version("5.51", "2019-07-26"),
		Version("5.50", "2019-07-16"),
		Version("5.49", "2019-07-04"),
		Version("5.48", "2019-07-03"),
		Version("5.47", "2019-07-01"),
		Version("5.46", "2019-06-26"),
		Version("5.45", "2019-06-24"),
		Version("5.44", "2019-06-07"),
		Version("5.43", "2019-05-07"),
		Version("5.42.1", "2019-04-29"),
		Version("5.42", "2019-04-26"),
		Version("5.41", "2019-03-29"),
		Version("5.40.2", "2019-03-26"),
		Version("5.40.1", "2019-03-25"),
		Version("5.40", "2019-03-25"),
		Version("5.39", "2019-01-30"),
		Version("5.38", "2018-11-15"),
		Version("5.37.1", "2018-11-13"),
		Version("5.37", "2018-11-08"),
		Version("5.36", "2018-10-31"),
		Version("5.35", "2018-09-14"),
		Version("5.34", "2018-06-03"),
		Version("5.33", "2018-05-15"),
		Version("5.32", "2018-02-20"),
		Version("5.31", "2018-01-29"),
		Version("5.30", "2018-01-17"),
		Version("5.29", "2017-11-29"),
		Version("5.28.2", "2017-08-03"),
		Version("5.28.1", "2017-08-02"),
		Version("5.28", "2017-08-01"),
		Version("5.27", "2017-03-21"),
		Version("5.26.1", "2017-03-03"),
		Version("5.26", "2017-02-28"),
		Version("5.25.1", "2017-02-15"),
		Version("5.25", "2017-02-13"),
		Version("5.24", "2017-02-12"),
		Version("5.23", "2016-12-16"),
		Version("5.22.1", "2016-11-02"),
		Version("5.22", "2016-10-18"),
		Version("5.21", "2016-09-19"),
		Version("5.20.1", "2016-08-04"),
		Version("5.20", "2016-07-29"),
		Version("5.19.4", "2016-06-30"),
		Version("5.19.3", "2016-06-29"),
		Version("5.19.2", "2016-06-21"),
		Version("5.19.1", "2016-06-20"),
		Version("5.19", "2016-06-14"),
		Version("5.18", "2016-05-17"),
		Version("5.17.1", "2016-05-10"),
		Version("5.17", "2016-05-04"),
		Version("5.16", "2016-04-13"),
		Version("5.15.1", "2016-03-21"),
		Version("5.15", "2016-03-18"),
		Version("5.14.2", "2016-03-02"),
		Version("5.14.1", "2015-12-04"),
		Version("5.14", "2015-12-02"),
		Version("5.13.1", "2015-06-12"),
		Version("5.13", "2014-12-18"),
		Version("5.12.1", "2014-12-09"),
		Version("5.12", "2014-11-07"),
		Version("5.11", "2014-10-29"),
		Version("5.10", "2014-10-09"),
		Version("5.9.1", "2014-09-29"),
		Version("5.9", "2014-09-22"),
		Version("5.8.1", "2014-06-18"),
		Version("5.8", "2014-05-05"),
		Version("5.7.1", "2014-02-13"),
		Version("5.7", "2014-01-30"),
		Version("5.6", "2014-01-28"),
		Version("5.5.1", "2014-01-27"),
		Version("5.5", "2014-01-23"),
		Version("5.4.1", "2013-12-18"),
		Version("5.4", "2013-11-29"),
		Version("5.3", "2013-10-28"),
		Version("5.2.7", "2013-10-15"),
		Version("5.2.6", "2013-10-15"),
		Version("5.2.5", "2013-10-09"),
		Version("5.2.4", "2013-10-09"),
		Version("5.2.3", "2013-10-09"),
		Version("5.2.2", "2013-10-07"),
		Version("5.2.1", "2013-10-02"),
		Version("5.2", "2013-10-01"),
		Version("5.1", "2013-08-02"),
		Version("5.0", "2013-06-04"),
		Version("4.10", "2013-03-04"),
		Version("4.9.1", "2013-01-17"),
		Version("4.9", "2013-01-17"),
		Version("4.8", "2013-01-15"),
		Version("4.7", "2013-01-11"),
		Version("4.6", "2012-12-18"),
		Version("4.5", "2012-11-29"),
		Version("4.4", "2012-11-08"),
		Version("4.3.1", "2012-11-06"),
		Version("4.3", "2012-11-02"),
		Version("4.2", "2012-10-22"),
		Version("4.1.1", "2012-10-04"),
		Version("4.1", "2012-10-02"),
		Version("4.0", "2012-08-08"),
		Version("3.25", "2011-08-12"),
		Version("3.24.1", "2011-08-10"),
		Version("3.24", "2011-08-09"),
		Version("3.23.1", "2011-07-28"),
		Version("3.23", "2011-07-20"),
		Version("3.22", "2011-07-14"),
		Version("3.21", "2011-06-03"),
		Version("3.20.2", "2011-05-23"),
		Version("3.20.1", "2011-05-18"),
		Version("3.20", "2011-05-05"),
		Version("3.19", "2011-04-26"),
		Version("3.18.1", "2011-04-13"),
		Version("3.18", "2011-04-08"),
		Version("3.17.3", "2011-03-02"),
		Version("3.17.2", "2011-02-25"),
		Version("3.17.1", "2011-02-25"),
		Version("3.17", "2011-02-24"),
		Version("3.16", "2011-01-21"),
		Version("3.15.3", "2010-11-26"),
		Version("3.15.2", "2010-11-25"),
		Version("3.15.1", "2010-11-24"),
		Version("3.15", "2010-11-09"),
		Version("3.14", "2010-11-05"),
		Version("3.13", "2010-10-22"),
		Version("3.12.1", "2010-10-21"),
		Version("3.12", "2010-10-21"),
		Version("3.11.1", "2010-10-18"),
		Version("3.11", "2010-10-15"),
		Version("3.10.1", "2010-10-13"),
		Version("3.10", "2010-09-24"),
		Version("3.9", "2010-08-04"),
		Version("3.8.3", "2010-07-29"),
		Version("3.8.2", "2010-06-21"),
		Version("3.8.1", "2010-06-17"),
		Version("3.8", "2010-06-15"),
		Version("3.7.6", "2010-05-14"),
		Version("3.7.5", "2010-04-19"),
		Version("3.7.4", "2010-03-25"),
		Version("3.7.3", "2010-02-27"),
		Version("3.7.2", "2010-02-26"),
		Version("3.7.1", "2010-02-08"),
		Version("3.7", "2009-09-10"),
		Version("3.6.6", "2009-07-09"),
		Version("3.6.5", "2009-06-02"),
		Version("3.6.4", "2009-03-19"),
		Version("3.6.3", "2009-03-02"),
		Version("3.6.2", "2009-02-16"),
		Version("3.6.1", "2009-01-27"),
		Version("3.6", "2008-12-31"),
		Version("3.5", "2008-12-05"),
		Version("3.4.4", "2008-09-16"),
		Version("3.4.3", "2008-09-09"),
		Version("3.4.2", "2008-09-03"),
		Version("3.4.1", "2008-08-29"),
		Version("3.4", "2008-08-19"),
		Version("3.3.2", "2008-07-15"),
		Version("3.3.1", "2008-07-14"),
		Version("3.3", "2008-07-11"),
		Version("3.2.7", "2008-05-16"),
		Version("3.2.6", "2008-05-07"),
		Version("3.2.5", "2008-04-11"),
		Version("3.2.4", "2008-04-02"),
		Version("3.2.3", "2008-03-04"),
		Version("3.2.2", "2008-02-25"),
		Version("3.2.1", "2008-02-05"),
		Version("3.2", "2008-02-01"),
		Version("3.1", "2008-01-18"),
		Version("3.0", "2008-01-07"),
		Version("2.15.5", "2007-07-17"),
		Version("2.15.4", "2007-07-16"),
		Version("2.15.3", "2007-07-16"),
		Version("2.15.2", "2007-01-24"),
		Version("2.15.1", "2006-09-25"),
		Version("2.15", "2006-09-24"),
		Version("2.14.2", "2006-07-04"),
		Version("2.14.1", "2006-06-29"),
		Version("2.14", "2006-06-28"),
		Version("2.13", "2005-10-31"),
		Version("2.12", "2005-10-13"),
		Version("2.11", "2005-07-29"),
		Version("2.10", "2005-05-20"),
		Version("2.9", "2005-04-21"),
		Version("2.8.1", "2005-03-22"),
		Version("2.8", "2005-01-03"),
		Version("2.7", "2004-11-24"),
		Version("2.6.2", "2005-06-06"),
		Version("2.6.1", "2004-11-02"),
		Version("2.6", "2004-10-26"),
		Version("2.5", "2004-06-30"),
		Version("2.4.1", "2004-01-05"),
		Version("2.4", "2004-01-02"),
		Version("2.3", "2003-12-08"),
		Version("2.2", "2003-07-31"),
		Version("2.1.4", "2003-06-13"),
		Version("2.1.3", "2003-05-07"),
		Version("2.1.2", "2003-02-27"),
		Version("2.1.1", "2003-02-11"),
		Version("2.1", "2002-12-09"),
		Version("2.0.8", "2002-11-20"),
		Version("2.0.7", "2002-11-12"),
		Version("2.0.6", "2002-11-11"),
		Version("2.0.5", "2002-11-11"),
		Version("2.0.4", "2002-11-08"),
		Version("2.0.3", "2002-10-30"),
		Version("2.0.2", "2002-10-21"),
		Version("2.0.1", "2002-10-17"),
		Version("2.0", "2002-10-16"),
		Version("1.6.1", "2003-08-25"),
		Version("1.6", "2003-07-02"),
		Version("1.5.13", "2003-07-01"),
		Version("1.5.12", "2003-06-17"),
		Version("1.5.11", "2003-06-13"),
		Version("1.5.10", "2003-06-13"),
		Version("1.5.9", "2003-04-30"),
		Version("1.5.8", "2003-02-27"),
		Version("1.5.7", "2002-11-12"),
		Version("1.5.6", "2002-11-11"),
		Version("1.5.5", "2002-11-11"),
		Version("1.5.4", "2002-09-30"),
		Version("1.5.3", "2002-09-25"),
		Version("1.5.2", "2002-09-19"),
		Version("1.5.1", "2002-09-17"),
		Version("1.5", "2002-08-27"),
		Version("1.4.5", "2002-06-18"),
		Version("1.4.4", "2002-06-16"),
		Version("1.4.3", "2002-04-29"),
		Version("1.4.2", "2002-03-22"),
		Version("1.4.1", "2002-03-21"),
		Version("1.4", "2002-03-18"),
		Version("1.3.1", "2002-03-14"),
		Version("1.3", "2002-02-12"),
		Version("1.2.5", "2001-12-03"),
		Version("1.2.4", "2001-11-23"),
		Version("1.2.3", "2001-11-22"),
		Version("1.2.2", "2001-11-16"),
		Version("1.2.1", "2001-10-08"),
		Version("1.2", "2001-10-03"),
		Version("1.1.3", "2001-09-17"),
		Version("1.1.2", "2001-08-21"),
		Version("1.1.1", "2001-08-01"),
		Version("1.1", "2001-07-19"),
		Version("1.0", "2001-06-18"),
		Version("0.4.7", "2000-11-24"),
		Version("0.4.6", "2000-11-03"),
		Version("0.4.5", "2000-11-01"),
		Version("0.4.4", "2000-10-27"),
		Version("0.4.3", "2000-10-19"),
		Version("0.4.2", "2000-09-24"),
		Version("0.4.1", "2000-09-21"),
		Version("0.4", "2000-09-19"),
		Version("0.3.9", "2000-08-10"),
		Version("0.3.8", "2000-07-14"),
		Version("0.3.7", "2000-07-06"),
		Version("0.3.6", "2000-07-04"),
		Version("0.3.5", "2000-07-02"),
		Version("0.3.4", "2000-05-31"),
		Version("0.3.3", "2000-05-30"),
		Version("0.3.2", "2000-05-26"),
		Version("0.3.1", "2000-05-25"),
		Version("0.3", "2000-05-25"),
		Version("0.2", "2000-05-17"),
		Version("0.1.1", "2000-05-16"),
		Version("0.1", "2000-05-15"),
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
