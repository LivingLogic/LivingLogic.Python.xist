#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<dbl:para>&xist; is an &xml; based &html; generator written in Python. It was developed
as a replacement for an &html; preprocessor named
<a href="http://www.giga.or.at/~agi/hsc/">HSC</a>, and borrows some
features and ideas from it. It also borrows the basic ideas (&xml;/&html;
elements as Python objects) from 
<a href="http://starship.python.net/crew/friedrich/HTMLgen/html/main.html">HTMLgen</a> 
or <a href="http://dustman.net/andy/python/HyperText/">HyperText</a>.</dbl:para>

<dbl:section><dbl:title>Overview</dbl:title>
<dbl:para>&xist; can be used as a compiler that reads an input file
and generates a transformed output file, or it could be used for generating
&xml; dynamically inside a web server. In either case generating the final
&html; or &xml; output in the form of a file or a response sent from
the web server, requires the following three steps:
<ul>
<li>Generating a source &dom; tree: This can be done either by
parsing an &xml; file, or by directly constructing the
tree, as <application>HTMLgen</application> and <application>HyperText</application>
do, as a tree of Python objects. &xist; provides a very natural
and pythonic &api; for that.</li>
<li>Converting the source tree into a target tree: This target
tree can be a &html; tree or a &wml; tree or any other
&xml; object tree you like. Every node class provides a
<function>convert</function> method for performing the conversion. For
your own &xml; element types you have to define your
own element classes and implement an appropriate
<function>convert</function> method.</li>
<li>Publishing the target tree: For writing the final
output to a file or generating a string that can
be delivered as a response from a web server, all node classes
provide a <function>publish</function> method which
passes the string fragment to a publishing handler.</li>
</ul>
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Constructing &dom; trees</dbl:title>
<dbl:para>Like any other &dom; &api;, &xist; provides the 
usual classes:
<ul>
<li><dbl:pyref module="xist.xsc" class="Text">Text</dbl:pyref> for text data</li>
<li><dbl:pyref module="xist.xsc" class="Frag">Frag</dbl:pyref> for document fragments,
a <dbl:pyref module="xist.xsc" class="Frag">Frag</dbl:pyref> object is simply a list
of nodes,</li>
<li><dbl:pyref module="xist.xsc" class="Comment">Comment</dbl:pyref> for &xml; comments
(e.g. <markup>&lt;!-- the comment --&gt;</markup>)</li>
<li><dbl:pyref module="xist.xsc" class="DocType">DocType</dbl:pyref> for document type
declarations (e.g. <markup>&lt;!DOCTYPE html PUBLIC <replaceable>...</replaceable>&gt;</markup>),</li>
<li><dbl:pyref module="xist.xsc" class="ProcInst">ProcInst</dbl:pyref> for processing instructions
(e.g. <markup>&lt;?php echo $spam;?&gt;</markup>,</li>
<li><dbl:pyref module="xist.xsc" class="Element">Element</dbl:pyref> for &xml; elements,</li>
<li><dbl:pyref module="xist.xsc" class="Entity">Entity</dbl:pyref> for entities (e.g. <markup>&amp;eggs;</markup>) and</li>
<li><dbl:pyref module="xist.xsc" class="Attr">Attr</dbl:pyref> for attributes.</li>
</ul>
</dbl:para>

<dbl:section><dbl:title>&dom; trees as Python objects</dbl:title>
<dbl:para>&xist; works somewhat different from a normal &dom; &api;.
Instead of only one element class, &xist; has one class for every element
type. All the elements known to &xist; are defined in modules in
the <dbl:pyref module="xist.ns">xist.ns</dbl:pyref> subpackage. The definition of &html; can 
be found in <dbl:pyref module="xist.ns.html">xist.ns.html</dbl:pyref> for example.</dbl:para>

<dbl:para>Every element class has a constructor of the form
<programlisting>
__init__(self, *content, **attrs)
</programlisting>
Positional arguments (i.e. items in <parameter>content</parameter>)
will be the child nodes of the element node. Keyword arguments
will be attributes. You can pass most builtin types to such a constructor.
Strings and integers will be automatically converted to
<pyref module="xist.xsc" class="Text">Text</pyref> objects.
So constructing an &html; element works like this:
<dbl:example title="The first example">
<programlisting>
from xist.ns import html

node = html.div(
	"Hello ",
	html.a("Python", href="http://www.python.org/"),
	" world!"
)
</programlisting>
</dbl:example>
</dbl:para>

<dbl:para>For attribute names that collide with Python keywords
(most notably <markup>class</markup>) you can append an underscore to the
name:
<dbl:example title="Colliding attribute names">
<programlisting>
node = html.div(
	"Hello world!",
	class_="greeting"
)
</programlisting>
</dbl:example>
One trailing underscore will be stripped off of an attribute name in the
element constructor.
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Generating &dom; trees from &xml; files</dbl:title>
<dbl:para>Of course &dom; trees can also be generated by parsing
&xml; files. For this the module <dbl:pyref module="xist.parsers">xist.parsers</dbl:pyref>
provides four functions:
<programlisting>
parseString(text, parser=None,
	namespaces=None, defaultEncoding="utf-8")
parseFile(filename, parser=None,
	namespaces=None, defaultEncoding="utf-8")
parseURL(url, parser=None,
	namespaces=None, defaultEncoding="utf-8")
parseTidyURL(url, parser=None,
	namespaces=None, defaultEncoding="utf-8")
</programlisting>
<dbl:pyref module="xist.parsers" function="parseString">parseString</dbl:pyref> is for parsing strings 
(8bit and Unicode), <dbl:pyref module="xist.parsers" function="parseFile">parseFile</dbl:pyref> for 
parsing files. <dbl:pyref module="xist.parsers" function="parseURL">parseURL</dbl:pyref> allows to 
parse remote files via <pyref module="urllib">urllib</pyref> and 
<dbl:pyref module="xist.parsers" function="parseTidyURL">parseTidyURL</dbl:pyref> pipes remote files 
through <application>tidy</application> before parsing the result. The argument 
<dbl:pyref module="xist.parsers" function="parseString" arg="parser">parser</dbl:pyref>
specifies the parser to be used. Any SAX2 parser can be used. &xist; provides a
SAX2 parser for <application>sgmlop</application> named 
<dbl:pyref module="xist.parsers" class="SGMLOPParser">SGMLOPParser</dbl:pyref> (which
is the default if no argument is given) and an &html; parser named
<dbl:pyref module="xist.parsers" class="HTMLParser">HTMLParser</dbl:pyref>, that
tries to make sense of &html; sources.</dbl:para>

<dbl:para>All four functions call
<dbl:pyref module="xist.parsers" function="parse">parse(source, parser=None, namespaces=None)</dbl:pyref>
internally and pass an appropriate <dbl:pyref module="xist.parsers" function="parse" arg="source">source</dbl:pyref> argument,
which is a standard &sax; <dbl:pyref module="xml.sax.xmlreader" class="InputSource">InputSource</dbl:pyref>
object, so it's possible to extend the parsing machinery for different data sources.</dbl:para>
</dbl:section>
</dbl:section>

<dbl:section><dbl:title>Defining new elements, converting &dom; trees</dbl:title>
<dbl:para>To be able to parse an &xml; file, you have to provide an element class
for every element type that appears in the file. Defining an element class
for an element named <code>cool</code> works like this:
<dbl:example title="Defining a new element">
<dbl:programlisting>
class cool(xsc.Element):
	empty = 0

	def convert(self, converter):
		node = html.b(self.content, " is cool!")
		return node.convert(converter)
</dbl:programlisting>
</dbl:example>
You have to derive your new class from <pyref module="xist.xsc" class="Element">xsc.Element</pyref>.
The name of the class will be the element name. For element type names that are no valid Python
identifiers, you can use the class attribute <code>name</code> in the element class the overwrite
the element name.</dbl:para>
<dbl:para>To be able to convert an element of this type to something different (&html; in most cases),
you have to implement the <pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
method. In this method you can build a new &dom; tree from the content and attributes
of the object.</dbl:para>

<dbl:para>Using this new element is simple
<dbl:example title="Using the new element">
<dbl:programlisting>
&gt;&gt;&gt; node = cool("Python")
&gt;&gt;&gt; print node.conv().asBytes()
&lt;b&gt;Python is cool!&lt;/b&gt;
</dbl:programlisting>
</dbl:example>
(<dbl:pyref module="xist.xsc" class="Node" method="conv">conv</dbl:pyref> simply
calls
<dbl:pyref module="xist.xsc" class="Node" method="convert">convert</dbl:pyref>
with default <dbl:pyref module="xist.cnverters" class="Converter">converter</dbl:pyref>
argument. We'll come to converters in a minute. 
<dbl:pyref module="xist.xsc" class="Node" method="asBytes">asBytes</dbl:pyref>
is a method that converts the node to a string. This method will be explained
when we discuss the publishing interface.)
</dbl:para>

<dbl:para>Note that it is vital for your own <pyref method="convert">convert</pyref>
methods that you recursively call
<pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
on you own content, because otherwise some unconverted nodes
might remain in the tree. Lets define a new element:
<dbl:programlisting>
class python(xsc.Element):
	empty = 1

	def convert(self, converter):
		return html.a("Python", href="http://www.python.org/")
</dbl:programlisting>
Now we can do the following:
<dbl:programlisting>
&gt;&gt;&gt; node = cool(python())
&gt;&gt;&gt; print node.conv().asBytes()
&lt;b&gt;&lt;a href="http://www.python.org/"&gt;Python&lt;/a&gt; is cool!&lt;/b&gt;
</dbl:programlisting>
But if we forget to call
<pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
for our own content, i.e. if the element <pyref class="cool">cool</pyref> 
was written like this:
<dbl:programlisting>
class cool(xsc.Element):
	empty = 0

	def convert(self, converter):
		return html.b(self.content, " is cool!")
</dbl:programlisting>
we would get:
<dbl:programlisting>
&gt;&gt;&gt; node = cool(python())
&gt;&gt;&gt; print node.conv().asBytes()
&lt;b&gt;&lt;python /&gt; is cool!&lt;/b&gt;
</dbl:programlisting>
</dbl:para>

<dbl:section><dbl:title>Converters</dbl:title>
<dbl:para><dbl:pyref module="xist.xsc" class="Node" method="conv">conv</dbl:pyref> is a convenience
method that creates a default converter for you. You could also call the method
<dbl:pyref module="xist.xsc" class="Node" method="convert">convert</dbl:pyref> itself,
which would look like this:
<dbl:programlisting>
from xist import converters

node = cool(python())
node = node.convert(
	converters.Converter(None, "deliver", "html", None))
</dbl:programlisting>
You can pass the following four arguments to the
<dbl:pyref module="xist.converters" class="Converter">Converter</dbl:pyref> constructor
<ul>
<li><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="mode">mode</dbl:pyref>
(which defaults to <code>None</code>) works the same way as modes in &xslt;. You can use this
for implementing different conversion modes.</li>
<li><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="stage">stage</dbl:pyref>
(which defaults to <code>"deliver"</code>) allows you to implement multi stage conversion:
Suppose that you want to deliver a dynamically constructed web page with &xist; that contains
results from a database query and the current time. The data in the database changes
infrequently, so it doesn't make sense to do the query on every request. The query is done
every few minutes and the resulting &html; tree is stored in the servlet
(using any of the available Python servlet technologies). For this conversion the
<dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="stage">stage</dbl:pyref>
would be <code>"cache"</code> and your database &xml; element would do the
query when <code><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="stage">stage</dbl:pyref>=="cache"</code>.
Your time display element would do the conversion when
<code><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="stage">stage</dbl:pyref>=="deliver"</code>
and simply returns itself when 
<code><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="stage">stage</dbl:pyref>=="cache"</code>,
so it would still be part of the cached &dom; tree and would be converted to &html; on every request.</li>
<li><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="target">target</dbl:pyref>
(which defaults to <code>html</code>) specifies what the output should be. Values could
e.g. be <code>"html"</code>, <code>"wml"</code> or <code>"docbook"</code>.</li>
<li><dbl:pyref module="xist.converters" class="Converter" method="__init__" arg="lang">lang</dbl:pyref>
(which defaults to <code>None</code>) the language in which the result tree should be.
This can be used in the <pyref method="convert">convert</pyref> method
to implement different conversions for different languages, e.g.:
<programlisting>
class note(xsc.Element):
	empty = 0

	def convert(self, converter):
		if converter.lang=="de":
			title = "Anmerkung"
		elif converter.lang=="ja":
			title = u"???"
		elif converter.lang=="fr":
			title = "???"
		else:
			title = "Note"
		return xsc.Frag(
			html.h1(title),
			html.div(self.content.convert(converter)))
</programlisting>
and you can test for the language with the element
<pyref module="xist.ns.cond" class="If">xist.ns.cond.If</pyref>, e.g.:
<programlisting>
&lt;if lang="de"&gt;Anmerkung
&lt;elif lang="ja"&gt;???
&lt;elif lang="fr"&gt;???
&lt;else&gt;Note
&lt;if&gt;
</programlisting>
</li>
</ul>
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Attributes</dbl:title>
<dbl:para>Setting and accessing the attributes of an element work via
the dictionary interface. So if <code>node</code>
is an <pyref module="xist.xsc" class="Element">Element</pyref> that supports the
attribute <code>spam</code> the following can be
done:
<example title="Working with attributes">
<programlisting>
if node.hasAttr("spam"):
	del node["spam"]
else:
	node["spam"] = "eggs"
node["spam"].append("ham")
</programlisting>
</example>
</dbl:para>
<dbl:para>All attribute values are instances of subclasses of
the class <pyref module="xist.xsc" class="Attr">Attr</pyref>. Available
subclasses are:
<ul>
<li><pyref module="xist.xsc" class="TextAttr">TextAttr</pyref>, for normal text attributes;</li>
<li><pyref module="xist.xsc" class="URLAttr">URLAttr</pyref>, for attributes that are URLs;</li>
<li><pyref module="xist.xsc" class="BoolAttr">BoolAttr</pyref>, for boolean attributes (such an attribute
is either present or not, but it's value will be ignored);</li>
<li><pyref module="xist.xsc" class="IntAttr">IntAttr</pyref>, for integer attributes;</li>
<li><pyref module="xist.xsc" class="ColorAttr">ColorAttr</pyref>, for color attributes (e.g. <code>#ffffff</code>)</li>
</ul>
<pyref module="xist.xsc" class="Attr">Attr</pyref> itself is derived from
<pyref module="xist.xsc" class="Frag">Frag</pyref> so it is possible
to use all the sequence methods on an attribute. Unset attributes will be treated
like empty ones so the following is possible:
<example>
<programlisting>
del node["spam"]
node["spam"].append("ham")
</programlisting>
</example>
this also means that after
<example>
<programlisting>
del node["spam"][0]
</programlisting>
</example>
the attribute will be empty again and will be considered to be unset.
Such attributes will be ignored when publishing.
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Specifying content model and attributes</dbl:title>
<dbl:para>When you define a new element you have to specify two thing:
<ol>
<li>If the element has an empty content model (like <markup>&lt;br/&gt;</markup>
or <markup>&lt;img/&gt;</markup> do in &html;) or not.</li>
<li>what attributes the element supports and of which type they are.</li>
</ol>
</dbl:para>

<dbl:para>Specifying the content model is done with the class attribute <code>empty</code>.
Set it to <code>0</code>, when your element may have content and to <code>1</code>
if it may not.</dbl:para>

<dbl:para>To specify the attributes for the element, use the class
attribute <pyref>attrHandlers</pyref>, which must be a dictionary
mapping attribute names to attribute classes. We could extend our
example element in the following way:
<dbl:example title="Using attributes">
<dbl:programlisting>
class cool(xsc.Element):
	empty = 0
	attrHandlers = {"adj": xsc.TextAttr}

	def convert(self, converter):
		node = xsc.Frag(self.content, " is")
		if self.hasAttr("adj"):
			node.append(" ", html.em(self["adj"]))
		node.append(" cool!")
		return node.convert(converter)
</dbl:programlisting>
</dbl:example>
and use it like this
<dbl:programlisting>
&gt;&gt;&gt; node = cool(python(), adj="totally")
&gt;&gt;&gt; print node.conv().asBytes()
&lt;a href="http://www.python.org/"&gt;Python&lt;/a&gt; is &lt;em&gt;totally&lt;/em&gt; cool!
</dbl:programlisting>
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Namespace objects</dbl:title>
<dbl:para>Now that you've defined your own elements, you have to
tell the parser about them, so they can be instantiated when
a file is parsed. This is done with namespace objects. At the end
of your Python module after all the classes are defined, create a
namespace object, that collects all the class objects from the
local scope:
<example>
<programlisting>
namespace = xsc.Namespace(
	"foo",
	"http://www.foo.net/DTDs/foo.dtd",
	vars()
)
</programlisting>
</example>
Arguments for the <pyref module="xist.xsc" class="Namespace">Namespace</pyref>
constructor are:
<ul>
<li><pyref module="xist.xsc" class="Namespace" method="__init__" arg="prefix">prefix</pyref> is
the namespace prefix that can be used to disambiguate elements in different namespaces
with the same name.</li>
<li><pyref module="xist.xsc" class="Namespace" method="__init__" arg="uri">uri</pyref> is the
namespace URL for the namespace. This is currently unused. &xist; doesn't have real
namespace support where namespace prefixes can be bound to namespace URLs dynamically,
but uses fixed prefixes.</li>
<li><pyref module="xist.xsc" class="Namespace" method="__init__" arg="thing">thing</pyref> is
the object that should be registered in the namespace. To register all the element
classes (and entities and processing instruction classes) defined in the module, simply
use <code>vars()</code>.</li>
</ul>
</dbl:para>

<dbl:para>All namespace objects will automatically be registered with the
parser. Now all newly defined elements will be used when parsing
files.</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Entities and processing instructions</dbl:title>
<dbl:para>In the same way as defining new element types, you can define new
entities and processing instructions. But to be able to use the new entities
in an &xml; file you have to use a parser that supports reporting undefined
entities to the application via <pyref method="skippedEntity">skippedEntity</pyref>
(<pyref module="xist.parsers" class="SGMLOPParser">SGMLOPParser</pyref> in the
module <pyref module="xist.parsers">xist.parsers</pyref> does that).</dbl:para>
<dbl:para>In addition to the <pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
method you have to implement the method
<pyref module="xist.xsc" class="Node" method="asPlainString">asPlainString</pyref>,
which must return a unicode string value for the entity. The following
example is from the module <pyref module="xist.ns.abbr">xist.ns.abbr</pyref>:
<example title="Defining new entities">
<programlisting>
from xist import xsc
from xist.ns import html

class xml(xsc.Entity):
	def convert(self, converter):
		return html.abbr(
			"XML",
			title="Extensible Markup Language",
			lang="en")
	def asPlainString(self):
		return u"XML"
</programlisting>
</example>
Now you can use this new entity in your &xml; files:
<programlisting>
&lt;cool adj="very"&gt;&amp;xml;&lt;/cool&gt;
</programlisting>
</dbl:para>
<dbl:para>Defining processing instructions works the same way. Derive a
new class from <pyref module="xist.xsc" class="ProcInst">xist.xsc.ProcInst</pyref>
and implement <pyref module="xist.xsc" class="Node" method="convert">convert</pyref>.
The following example implements a processing instruction that returns an uppercase
version of it's content as a text node.
<example title="Defining new processing instructions">
<programlisting>
class upper(xsc.ProcInst):
	def convert(self, converter):
		return xsc.Text(self.content.upper())
</programlisting>
</example>
it can be used in an &xml; file as following:
<programlisting>
&lt;?upper foo?&gt;
</programlisting>
</dbl:para>
</dbl:section>
</dbl:section>

<dbl:section><dbl:title>Publishing &dom; trees</dbl:title>
<dbl:para>After creating the &dom; tree and converting the tree
into its final output form, you have to write the resulting text
into a file. This can be done with the publishing &api;. Two methods
that use the publishing &api; are
<pyref module="xist.xsc" class="Node" method="asBytes">asBytes</pyref>
and
<pyref module="xist.xsc" class="Node" method="write">write</pyref>.
<pyref module="xist.xsc" class="Node" method="asBytes">asBytes</pyref>
returns and 8bit &xml; string. You can specify the encoding with the
parameter <pyref module="xist.xsc" class="Node" method="asBytes" arg="encoding">encoding</pyref>
(with <code>"us-ascii"</code> being the default).
Unencodable characters will be escaped with numeric character references when possible
(i.e. inside text nodes, for comments or processing instructions you'll get
an exception):
<programlisting>
&gt;&gt;&gt; from xist.ns import xsc, html
&gt;&gt;&gt; print html.div(
...    u"äöü",
...    html.br(),
...    u"ÄÖÜ").asBytes(encoding="ascii")
&lt;div&gt;&amp;#228;&amp;#246;&amp;#252;&lt;br /&gt;&amp;#196;&amp;#214;&amp;#220;&lt;/div&gt;
&gt;&gt;&gt; print html.div(
...    u"äöü",
...    html.br(),
...    u"ÄÖÜ").asBytes(encoding="iso-8859-1")
&lt;div&gt;äöü&lt;br /&gt;ÄÖÜ&lt;/div&gt;
&gt;&gt;&gt; print xsc.Comment(u"äöü").asBytes()
Traceback (most recent call last):
  File "&lt;stdin&gt;", line 1, in ?
  File "~/pythonroot/xist/xsc.py", line 828, in asBytes
    return publisher.asBytes()
  File "~/pythonroot/xist/publishers.py", line 162, in asBytes
    return u"".join(self.texts).encode(self.encoding)
UnicodeError: ASCII encoding error: ordinal not in range(128)
</programlisting>
</dbl:para>
<dbl:para>Another useful parameter is
<pyref module="xist.xsc" class="Node" method="asBytes" arg="XHTML">XHTML</pyref>,
it specifies if you want pure &html; or &xhtml; as output:
<ul>
<li><code>XHTML==0</code> will give pure &html; as output, i.e. no final <markup>/</markup>
for element with an empty content model, so you'll get <markup>&lt;br&gt;</markup> in the output.
Elements that have no empty content model, but are empty will be published with a start and
end tag (i.e. <markup>&lt;div&gt;&lt;/div&gt;</markup>).</li>
<li><code>XHTML==1</code> gives &html; compatible &xhtml;. Elements with empty content
model will be published like this: <markup>&lt;br /&gt;</markup>.</li>
<li><code>XHTML==2</code> gives full &xml; output. Every empty element will be published with
an empty tag (without an additional space): <markup>&lt;br/&gt;</markup> or <markup>&lt;div/&gt;</markup>.</li>
</ul></dbl:para>
<dbl:para>Writing a node to a file can be done with the method
<pyref module="xist.xsc" class="Node" method="write">write</pyref>:
<programlisting>
&gt;&gt;&gt; from xist.ns import html
&gt;&gt;&gt; html.div(
...    u"äöü",
...    html.br(),
...    u"ÄÖÜ").write(open("foo.html", "wb"), encoding="ascii")
</programlisting>
</dbl:para>
</dbl:section>

<dbl:section><dbl:title>Miscellaneous</dbl:title>
<dbl:section><dbl:title>URLs</dbl:title>
<dbl:para>&xist; has a class for URLs (<pyref module="xist.url">xist.url</pyref>)
which is a thin wrapper around <pyref module="urlparse">urlparse</pyref>'s
features. You can add URLs via <code>+</code>, e.g.
<programlisting>
URL("http://www.foo.org/") + URL("/images/bar.png")
</programlisting>
yields an URL object equivalent to
<programlisting>
URL("http://www.foo.org/images/bar.png").
</programlisting>
</dbl:para>
<dbl:para>&xist; stores the URL from which an attribute was parsed is stored
by the parser in the <pyref>base</pyref></dbl:para>
</dbl:section>

<dbl:section><dbl:title>Automatic generation of image size attributes</dbl:title>
<dbl:para>The module special contains an element autoimg, that extends
html.img. When converted to HTML via the convert() method the
size of the image will be determined and the HEIGHT
and WIDTH attributes will be set accordingly.</dbl:para>

<dbl:para>This is not the whole truth. When the WIDTH or HEIGHT attribute
is already specified, the following happens:
%-formatting is used on the attribute value, the width and
height of the image is passed to the % operator as a dictionary
with the keys "width" and "height". The resulting string is
eval()uated and it's result is used for the attribute. So to make
an image twice as wide and high do the following:
<dbl:programlisting>
&lt;img src="foo.png" width="%(width)d*2" height="%(height)d*2"/&gt;
</dbl:programlisting></dbl:para>
</dbl:section>

<dbl:section><dbl:title>Embedding Python code</dbl:title>
<dbl:para>It's possible to embed Python code into &xist; &xml; files. For this
&xist; supports two new processing instructions: <markup>xsc:exec</markup> 
and <markup>xsc:eval</markup>. The content of <markup>xsc:exec</markup> will be 
executed when the processing instruction node is instantiated, i.e. when the 
&xml; file is parsed, so anything you do there will be available afterwards.</dbl:para>

<dbl:para>The result of a call to <pyref module="xist.xsc" class="Node" method="convert">convert</pyref> 
for a <markup>xsc:eval</markup> processing instruction is whatever the 
Python code in the content returns. This content is treated as the body
of a function, so you can put multiple return statements there.
The converter is available as the parameter <code>converter</code> inside
the processing instruction. For example, consider the following &xml; file:
<dbl:programlisting>
&lt;?xsc:exec
	# sum
	def gauss(top=100):
		sum = 0
		for i in xrange(top+1):
			sum += i
		return sum
?&gt;
&lt;b&gt;&lt;?xsc:eval return gauss()?&gt;&lt;/b&gt;
</dbl:programlisting>
Parsing this file and calling 
<pyref module="xist.xsc" class="Node" method="convert">convert</pyref> results in the following:
<dbl:programlisting>
&lt;b>5050&lt;/b>
</dbl:programlisting>
</dbl:para>

<dbl:para>For further information see the class <pyref module="xist.xsc" class="ProcInst">ProcInst</pyref> 
and it's two derived classes <pyref module="xist.xsc" class="Eval">Eval</pyref> and 
<pyref module="xist.xsc" class="Exec">Exec</pyref>.</dbl:para>
</dbl:section>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os, string, types, sys, stat, urllib, random

try:
	import Image
except ImportError:
	Image = None

import procinst, url, presenters, publishers, converters, errors, options, utils, helpers

###
### helpers
###

def ToNode(value):
	"""
	<par noindent>convert the <argref>value</argref> passed in to a XSC <classref>Node</classref>.</par>

	<par>If <argref>value</argref> is a tuple or list, it will be (recursively) converted
	to a <classref>Frag</classref>. Integers, strings, etc. will be converted to a <classref>Text</classref>.
	If <argref>value</argref> is a <classref>Node</classref> already, nothing will be done.
	In the case of <code>None</code> the XSC Null (<code>xsc.Null</code>) will be returned).
	Anything else raises an exception.</par>
	"""
	t = type(value)
	if t is types.InstanceType:
		if isinstance(value, Node):
			if isinstance(value, Attr):
				return Frag(*value) # repack the attribute in a fragment, and we have a valid XSC node
			return value
		elif isinstance(value, url.URL):
			return Text(value.asString())
	elif t in (types.StringType, types.UnicodeType, types.IntType, types.LongType, types.FloatType):
		return Text(value)
	elif t is types.NoneType:
		return Null
	elif t in (types.ListType, types.TupleType):
		return Frag(*value)
	raise errors.IllegalObjectError(value) # none of the above, so we throw and exception

class Node:
	"""
	base class for nodes in the document tree. Derived classes must
	implement <methodref>convert</methodref> and may implement
	<methodref>publish</methodref> and <methodref>asPlainString</methodref>.
	"""

	empty = 1

	# location of this node in the XML file (will be hidden in derived classes, but is
	# specified here, so that no special tests are required. In derived classes
	# this will be set by the parser)
	startLoc = None
	endLoc = None

	# specifies if a prefix should be presented or published. Can be 0 or 1 or None
	# which mean use the default
	presentPrefix = None
	publishPrefix = None

	# specifies that this class should be registered in a namespace
	# this won't be used for all the DOM classes (Element, ProcInst etc.) themselves but only for derived classes
	# i.e. Node, Element etc. will never be registered
	register = 1

	#def __repr__(self):
	#	return self.repr(presenters.defaultPresenterClass())

	def _str(self, content=None, brackets=1, slash=None, ansi=None):
		return _strNode(self.__class__, content, brackets, slash, ansi)

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		raise NotImplementedError("clone method not implemented in %s" % self.__class__.__name__)

	def repr(self, presenter=None):
		if presenter is None:
			presenter = presenters.defaultPresenterClass()
		presenter.beginPresentation()
		self.present(presenter)
		return presenter.endPresentation()

	def present(self, presenter):
		raise NotImplementedError("present method not implemented in %s" % self.__class__.__name__)

	def conv(self, converter=None):
		"""
		<par noindent>returns a version of this node and it's content converted to HTML,
		so when you define your own element classes you should overwrite <methodref>convert</methodref>.</par>

		<par>E.g. when you want to define an element that packs it's content into an HTML
		bold element, do the following:

		<pre>
		class foo(xsc.Element):
			empty = 0

			def convert(self, converter):
				return html.b(self.content).convert(converter)
		</pre>
		</par>
		"""
		if converter is None:
			converter = converters.Converter()
		return self.convert(converter)

	def convert(self, converter):
		"""
		<par noindent>implementation of the conversion method. Has to be overwritten in subclasses.</par>
		"""
		raise NotImplementedError("convert method not implemented in %s" % self.__class__.__name__)

	def asPlainString(self):
		"""
		<par noindent>returns this node as a (unicode) string without any character references.
		Comments and processing instructions will be filtered out.
		For elements you'll get the element content.</par>

		<par>It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:
		<pre>
		class caps(xsc.Element):
			empty = 0

			def convert(self, converter):
				return html.span(
					self.content.convert(converter),
					style="font-variant: small-caps;"
				)
		</pre>

		that renders its content in small caps, then it might be useful
		to define <methodref>asPlainString</methodref> in the following way:
		<pre>
		def asPlainString(self):
			return self.content.asPlainString().upper()
		</pre>

		<methodref>asPlainString</methodref> can be used everywhere, where
		a plain string representation of the node is required.
		<classref module="html">title</classref> uses this function on its content,
		so you can safely use HTML elements in your title elements (e.g. if your
		title is dynamically constructed from a DOM tree.)</par>
		"""
		raise NotImplementedError("asPlainString method not implemented in %s" % self.__class__.__name__)

	def asText(self, monochrome=1, squeezeBlankLines=0, lineNumbers=0, cols=80):
		"""
		<par noindent>Return the node as a formatted plain &ascii; string.
		Note that this really only make sense for &html; trees.</par>

		<par>This requires that w3m is installed.</par>
		"""

		options = ""
		if monochrome==1:
			options += " -M"
		if squeezeBlankLines==1:
			options += " -S"
		if lineNumbers==1:
			options += " -num"
		if cols!=80:
			options += " -cols %d" % cols

		text = self.asBytes(encoding="us-ascii")

		(stdin, stdout) = os.popen2("w3m %s -T text/html -dump" % options)

		stdin.write(text)
		stdin.close()
		text = stdout.read()
		stdout.close()
		text = "\n".join([ line.rstrip() for line in text.splitlines()])
		return text

	def __int__(self):
		"""
		returns this node converted to an integer.
		"""
		return int(self.asPlainString())

	def asInt(self):
		"""
		returns this node converted to an integer.
		"""
		return int(self)

	def asFloat(self, decimal=".", ignore=""):
		"""
		returns this node converted to a float. <argref>decimal</argref>
		specifies which decimal separator is used in the value
		(e.g. <code>"."</code> (the default) or <code>","</code>).
		<argref>ignore</argref>specifies which character will be ignored.
		"""
		s = self.asPlainString()
		for c in ignore:
			s = string.replace(s, c, "")
		if decimal != ".":
			s = string.replace(s, decimal, ".")
		return float(s)

	def __float__(self):
		"""
		returns this node converted to a float.
		"""
		return self.asFloat()

	def publish(self, publisher):
		"""
		<par noindent>generates unicode strings for the node, and passes
		the strings to the callable object <argref>publisher</argref>.</par>

		<par>The encoding and XHTML specification are taken from the <argref>publisher</argref>.</par>
		"""
		raise NotImplementedError("publish method not implemented in %s" % self.__class__.__name__)

	def asString(self, XHTML=None, publishPrefix=0):
		"""
		<par noindent>returns this element as a unicode string.</par>

		<par>For an explanation of <argref>XHTML</argref> and <argref>publishPrefix</argref> see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.StringPublisher(XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asString()

	def asBytes(self, base=None, encoding=None, XHTML=None, publishPrefix=0):
		"""
		<par noindent>returns this element as a byte string suitable for writing
		to an HTML file or printing from a CGI script.</par>

		<par>For the parameters see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.BytePublisher(base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asBytes()

	def write(self, file, base=None, encoding=None, XHTML=None, publishPrefix=0):
		"""
		<par noindent>writes the element to the file like
		object <argref>file</argref></par>

		<par>For the parameters see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.FilePublisher(file, base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		"""
		<par noindent>returns a fragment which contains child elements of this node.</par>

		<par>If you specify <argref>type</argref> as the class of an XSC node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</par>

		<par>If you set <argref>subtype</argref> to <code>1</code> nodes that are a
		subtype of <argref>type</argref> will be returned too.</par>

		<par>If you pass a dictionary as <argref>attrs</argref> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <code>asPlainString()</code> representation will
		be used. You can use <code>None</code> as the value to test that the attribute
		is set without testing the value.</par>

		<par>Additionally you can pass a test function in <argref>test</argref>, that
		returns <code>1</code>, when the node passed in has to be included in the
		result and <code>0</code> otherwise.</par>

		<par>If you set <argref>searchchildren</argref> to <code>1</code> not only the
		immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</par>

		<par>If you set <argref>searchattrs</argref> to <code>1</code> the attributes
		of the nodes (if <argref>type</argref> is <classref>Element</classref> or one
		of its subtypes) will be searched too.</par>

		<par>Note that the node has to be of type <classref>Element</classref>
		(or a subclass of it) to match <argref>attrs</argref>.</par>
		"""
		node = Frag()
		if self._matches(type, subtype, attrs, test):
			node.append(self)
		return node

	def compact(self):
		"""
		returns a version of <self/>, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		raise NotImplementedError("compact method not implemented in %s" % self.__class__.__name__)

	def _matchesAttrs(self, attrs):
		if attrs is None:
			return 1
		else:
			if isinstance(self, Element):
				for attr in attrs.keys():
					if (not self.hasAttr(attr)) or ((attrs[attr] is not None) and (self[attr].asPlainString() != attrs[attr])):
						return 0
				return 1
			else:
				return 0

	def _matches(self, type_, subtype, attrs, test):
		res = 1
		if type_ is not None:
			if type(type_) not in [types.ListType, types.TupleType]:
				type_ = (type_,)
			for t in type_:
				if subtype:
					if isinstance(self, t):
						res = self._matchesAttrs(attrs)
						break
				else:
					if self.__class__ == t:
						res = self._matchesAttrs(attrs)
						break
			else:
				res = 0
		else:
			res = self._matchesAttrs(attrs)
		if res and (test is not None):
			res = test(self)
		return res

	def _decorateNode(self, node):
		"""
		decorate the node <argref>node</argref> with the same location information as <self/>.
		"""

		node.startLoc = self.startLoc
		node.endLoc = self.endLoc
		return node

	def _publishName(self, publisher):
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		if publishPrefix and hasattr(self, "namespace"):
			publisher.publish(self.namespace.prefix) # must be registered to work
			publisher.publish(u":")
		if hasattr(self, "name"):
			publisher.publish(self.name)
		else:
			publisher.publish(self.__class__.__name__)

	def mapped(self, function):
		"""
		returns the node mapped through the function <pyref arg="function">function</pyref>.
		This call works recursively (for <pyref class="Frag">Frag</pyref> and <pyref class="Element">Element</pyref>.
		When you want an unmodified node you simply can return <self/>. <pyref method="mapped">mapped</mapped>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped.
		"""
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		return node

	def normalized(self):
		"""
		returns a normalized version of <self/>, which means, that consecutive
		<pyref class="Text">Text nodes</pyref> are merged.
		"""
		return self

class CharacterData(Node):
	"""
	provides nearly the same functionality as <classref>UserString</classref>, but omits
	a few methods (<code>__str__</code> etc.)
	"""
	def __init__(self, content=u""):
		self.content = helpers.unistr(content)

	def __iadd__(self, other):
		other = ToNode(other)
		return self.__class__(self.content+other.content)

	__add__ = __iadd__

	def __radd__(self, other):
		other = ToNode(other)
		return self.__class__(other.content+self.content)

	def __imul__(self, n):
		return self.__class__(self.content*n)

	__mul__ = __imul__

	def __cmp__(self, other):
		if isinstance(other, self.__class__):
			return cmp(self.content, other.content)
		else:
			return cmp(self.content, other)

	def __contains__(self, char):
		return helpers.unistr(char) in self.content

	def __hash__(self):
		return hash(self.content)

	def __len__(self):
		return len(self.content)

	def __getitem__(self, index):
		return self.content[index]

	def __getslice__(self, index1, index2):
		return self.__class__(self.content[index1:index2])

	def capitalize(self):
		return self.__class__(self.content.capitalize())

	def center(self, width):
		return self.__class__(self.content.center(width))

	def count(self, sub, start=0, end=sys.maxint):
		return self.content.count(sub, start, end)

	def endswith(self, suffix, start=0, end=sys.maxint):
		return self.content.endswith(helpers.unistr(suffix), start, end)

	# no find here def find(self, sub, start=0, end=sys.maxint):
	#	return self.content.find(helpers.unistr(sub), start, end)

	def index(self, sub, start=0, end=sys.maxint):
		return self.content.index(helpers.unistr(sub), start, end)

	def isalpha(self):
		return self.content.isalpha()

	def isalnum(self):
		return self.content.isalnum()

	def isdecimal(self):
		return self.content.isdecimal()

	def isdigit(self):
		return self.content.isdigit()

	def islower(self):
		return self.content.islower()

	def isnumeric(self):
		return self.content.isnumeric()

	def isspace(self):
		return self.content.isspace()

	def istitle(self):
		return self.content.istitle()

	def join(self, frag):
		return frag.withSeparator(self)

	def isupper(self):
		return self.content.isupper()

	def ljust(self, width):
		return self.__class__(self.content.ljust(width))

	def lower(self):
		return self.__class__(self.content.lower())

	def lstrip(self):
		return self.__class__(self.content.lstrip())

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self.content.replace(helpers.unistr(old), helpers.unistr(new), maxsplit))

	def rfind(self, sub, start=0, end=sys.maxint):
		return self.content.rfind(helpers.unistr(sub), start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self.content.rindex(helpers.unistr(sub), start, end)

	def rjust(self, width):
		return self.__class__(self.content.rjust(width))

	def rstrip(self):
		return self.__class__(self.content.rstrip())

	def split(self, sep=None, maxsplit=-1):
		return Frag(self.content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self.content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxint):
		return self.content.startswith(helpers.unistr(prefix), start, end)

	def strip(self):
		return self.__class__(self.content.strip())

	def swapcase(self):
		return self.__class__(self.content.swapcase())

	def title(self):
		return self.__class__(self.content.title())

	def translate(self, *args):
		return self.__class__(self.content.translate(*args))

	def upper(self):
		return self.__class__(self.content.upper())

class Text(CharacterData):
	"""
	text node. The characters <, >, & and " will be "escaped" with the
	appropriate character entities.
	"""

	def __init__(self, content=""):
		if isinstance(content, Text):
			content = content.content
		CharacterData.__init__(self, content)

	def convert(self, converter):
		return self

	def clone(self):
		return self

	def asPlainString(self):
		return self.content

	def publish(self, publisher):
		publisher.publishText(self.content)

	def present(self, presenter):
		presenter.presentText(self)

	def compact(self):
		if self.content.isspace():
			return Null
		else:
			return self

class Frag(Node):
	"""
	A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member content of an Element is a Frag.
	"""

	empty = 0

	def __init__(self, *content):
		self.__content = []
		for child in content:
			child = ToNode(child)
			if child is not Null:
				self.__content.append(child)

	def convert(self, converter):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		for child in self.__content:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object %r (type %r) when converting %r" % (convertedchild, type(convertedchild), self)
			if convertedchild is not Null:
				node.__content.append(convertedchild)
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		node.__content = [ child.clone() for child in self.__content ]
		return self._decorateNode(node)

	def present(self, presenter):
		presenter.presentFrag(self)

	def asPlainString(self):
		return u"".join([ child.asPlainString() for child in self.__content ])

	def publish(self, publisher):
		for child in self.__content:
			child.publish(publisher)

	def __getitem__(self, index):
		"""
		Return the <argref>index</argref>'th node for the content of the fragment.
		If <argref>index</argref> is a list <code>__getitem__</code> will work
		recursively. If <argref>index</argref> is empty, <self/> will be returned.
		"""
		if type(index) in (types.IntType, types.LongType):
			return self.__content[index]
		elif type(index) is types.ListType:
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		else:
			raise TypeError("index must be int, long or list not %s" % type(index).__name__)

	def __setitem__(self, index, value):
		"""
		Allows you to replace the <argref>index</argref>'th content node of the fragment
		with the new value <argref>value</argref> (which will be converted to a node).
		If  <argref>index</argref> is a list <code>__setitem__</code> will be applied
		to the innermost index after traversing the rest of <argref>index</argref> recursively.
		If <argref>index</argref> is empty the call will be ignored.
		"""
		value = ToNode(value)
		try:
			self.__content[index] = value
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				node[index[-1]] = value

	def __delitem__(self, index):
		"""
		Remove the <argref>index</argref>'th content node from the fragment.
		If <argref>index</argref> is a list, the innermost index will be deleted,
		after traversing the rest of <argref>index</argref> recursively.
		If <argref>index</argref> is empty the call will be ignored.
		"""
		try:
			del self.__content[index]
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				del node[index[-1]]

	def __getslice__(self, index1, index2):
		"""
		returns a slice of the content of the fragment
		"""
		node = self.__class__()
		node.__content = self.__content[index1:index2]
		return node

	def __setslice__(self, index1, index2, sequence):
		"""
		replaces a slice of the content of the fragment
		"""
		self.__content[index1:index2] = map(ToNode, sequence)

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the fragment
		"""
		del self.__content[index1:index2]

	def __nonzero__(self):
		"""
		return whether the fragment is not empty (this should be a little faster than defaulting to __len__)
		"""
		return len(self.__content)>0

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.__content)

	def append(self, *others):
		"""
		appends all items in <argref>others</argref> to <self/>.
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.append(newother)

	def insert(self, index, *others):
		"""
		inserts all items in <argref>others</argref> at the position <argref>index</argref>.
		(this is the same as <code><self/>[<argref>index</argref>:<argref>index</argref>] = <argref>others</argref></code>)
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.insert(index, newother)
				index += 1

	def extend(self, *others):
		"""
		extends this fragment by all items in <argref>others</argref>.
		"""
		for other in others:
			newother = ToNode(other)
			if isinstance(newother, Frag):
				self.__content.extend(newother)
			elif newother is not Null:
				self.__content.append(newother)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		for child in self.__content:
			if child._matches(type, subtype, attrs, test):
				node.append(child)
			if searchchildren:
				node.extend(child.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def compact(self):
		node = self.__class__()
		for child in self.__content:
			compactedchild = child.compact()
			assert isinstance(compactedchild, Node), "the compact method returned the illegal object %r (type %r) when compacting %r" % (compactedchild, type(compactedchild), child)
			if compactedchild is not Null:
				node.__content.append(compactedchild)
		return self._decorateNode(node)

	def withSeparator(self, separator, clone=0):
		"""
		returns a version of <self/> with a separator node between the nodes of <self/>.

		if <code><pyref arg="clone">clone</pyref>==0</code> one node will be inserted several times,
		if <code><pyref arg="clone">clone</pyref>==1</code> clones of this node will be used.
		"""
		node = Frag()
		newseparator = ToNode(separator)
		for child in self.__content:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(node1.asPlainString(), node2.asPlainString())):
		"""
		returns a sorted version of the <self/>. <argref>compare</argref> is
		a comparison function returning -1, 0, 1 respectively.
		"""
		node = Frag()
		node.__content = self.__content[:]
		node.__content.sort(compare)
		return node

	def reversed(self):
		"""
		returns a reversed version of the <self/>.
		"""
		node = Frag()
		node.__content = self.__content[:]
		node.__content.reverse()
		return node

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = Frag()
		node.__content = [ child for child in self.__content if function(child) ]
		return node

	def shuffled(self):
		"""
		return a shuffled version of <self/>.
		"""
		content = self.__content[:]
		node = Frag()
		while content:
			index = random.randrange(len(content))
			node.__content.append(content[index])
			del content[index]
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = Frag(*[ child.mapped(function) for child in self.__content])
		return node

	def normalized(self):
		node = Frag()
		lasttypeOK = 0
		for child in self.__content:
			normalizedchild = child.normalized()
			thistypeOK = isinstance(normalizedchild, Text)
			if thistypeOK and lasttypeOK:
				node.__content[-1] += normalizedchild
			else:
				node.__content.append(normalizedchild)
			lasttypeOK = thistypeOK
		return node

class Comment(CharacterData):
	"""
	a comment node
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentComment(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		if self.content.find(u"--")!=-1 or self.content[-1:]==u"-":
			raise errors.IllegalCommentContentError(self)
		publisher.publish(u"<!--")
		publisher.publish(self.content)
		publisher.publish(u"-->")

class DocType(CharacterData):
	"""
	a document type node
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentDocType(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.publish(u"<!DOCTYPE ")
		publisher.publish(self.content)
		publisher.publish(u">")

class ProcInst(CharacterData):
	"""
	<par noindent>There are two special targets available: <code>xsc:exec</code>
	and <code>xsc:eval</code> which will be handled by the
	special classes <classref>Exec</classref> and <classref>Eval</classref>
	derived from ProcInst.</par>

	<par>Processing instruction with the target <code>xml</code> will be 
	handled by the class <classref>XML</classref>.

	<par>All other processing instructions (PHP, etc.) will be handled
	by other classes derived from <code>ProcInst</code>.</par>
	"""

	# we don't need a constructor, because we don't have to store the target,
	# because the target is our classname

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentProcInst(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		if self.content.find(u"?>")!=-1:
			raise errors.IllegalProcInstFormatError(self)
		publisher.publish(u"<?")
		self._publishName(publisher)
		publisher.publish(u" ")
		publisher.publish(self.content)
		publisher.publish(u"?>")

class PythonCode(ProcInst):
	"""
	helper class
	"""

	register = 0 # don't register the class
	presentPrefix = 1
	publishPrefix = 1

class Exec(PythonCode):
	"""
	<par noindent>here the content of the processing instruction is executed
	as Python code, so you can define and register XSC elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to HTML such a node will result
	in an empty Null node.</par>

	<par>XSC processing instructions will be evaluated and executed in the
	namespace of the module procinst.</par>
	"""
	name = u"exec"
	register = 1

	def __init__(self, content=u""):
		ProcInst.__init__(self, content)
		code = utils.Code(self.content, 1)
		exec code.asString() in procinst.__dict__ # requires Python 2.0b2 (and doesn't really work)

	def convert(self, converter):
		return Null # has been executed at construction time already, so we don't have to do anything here

class Eval(PythonCode):
	"""
	<par noindent>here the code will be executed when the node is converted to HTML
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to HTML.</par>

	<par>XSC processing instructions will be evaluated and executed in the
	namespace of the module <moduleref>procinst</moduleref>.</par>

	<par>Note that you should not define the symbol <code>__</code> in any of your XSC
	processing instructions, as it is used by XSC for internal purposes.</par>
	"""

	name = u"eval"
	register = 1

	def convert(self, converter):
		"""
		Evaluates the code. The <argref>converter</argref> argument will be available
		under the name <code>converter</code> as an argument.
		"""
		code = utils.Code(self.content, 1)
		code.funcify()
		exec code.asString() in procinst.__dict__ # requires Python 2.0b2 (and doesn't really work)
		return ToNode(procinst.__(converter)).convert(converter)

class XML(ProcInst):
	"""
	XML header
	"""

	name = u"xml"
	presentPrefix = 0
	publishPrefix = 0

	def publish(self, publisher):
		encodingfound = utils.findAttr(self.content, u"encoding")
		versionfound = utils.findAttr(self.content, u"version")
		standalonefound = utils.findAttr(self.content, u"standalone")
		if publisher.encoding != encodingfound: # if self has the wrong encoding specification (or none), we construct a new XML ProcInst and publish that (this doesn't lead to infinite recursion, because the next call will skip it)
			node = XML(u"version='" + versionfound + u"' encoding='" + publisher.encoding + u"'")
			if standalonefound is not None:
				node += u" standalone='" + standalonefound + u"'"
			node.publish(publisher)
			return
		ProcInst.publish(self, publisher)

class XML10(XML):
	"""
	XML header version 1.0
	"""
	register = 0 # don't register this ProcInst, because it will never be parsed from a file, this is just a convenience class

	def __init__(self):
		XML.__init__(self, 'version="1.0"')

class XMLStyleSheet(ProcInst):
	"""
	XML stylesheet declaration
	"""

	name = u"xml-stylesheet"
	presentPrefix = 0
	publishPrefix = 0

class Element(Node):
	"""
	<par noindent>This class represents XML/XSC elements. All elements
	implemented by the user must be derived from this class.</par>

	<par>If you not only want to construct a DOM tree via a Python script
	(by directly instantiating these classes), but to read an XML/XSC file
	you must register the element class with the parser, this can be done
	by passing the class object to the function
	<functionref>registerElement</functionref>.</par>

	<par>Every element class should have two class variables:
	<code>empty</code>: this is either <code>0</code> or <code>1</code>
	and specifies whether the element type is allowed to have content
	or not. Note that the parser does not use this as some sort of
	static DTD, i.e. you still must write your empty tags
	like this: <code>&lt;foo/&gt;</code>.</par>

	<par><code>attrHandlers</code> is a dictionary that maps attribute
	names to attribute classes, which are all derived from <classref>Attr</classref>.
	Assigning to an attribute with a name that is not in <code>attrHandlers.keys()</code>
	is an error.</par>
	"""

	empty = 1 # 0 => element with content; 1 => stand alone element
	attrHandlers = {} # maps attribute names to attribute classes

	def __init__(self, *content, **attrs):
		"""
		positional arguments are treated as content nodes.

		keyword arguments are treated as attributes.
		"""
		self.content = Frag(*content)
		self.attrs = {}
		for (attrname, attrvalue) in attrs.items():
			self[attrname] = attrvalue

	def append(self, *items):
		"""
		append(self, *items)

		appends to the content (see Frag.append for more info)
		"""

		self.content.append(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def insert(self, index, *items):
		"""
		insert(self, index, *items)

		inserts into the content (see Frag.insert for more info)
		"""
		self.content.insert(index, *items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def extend(self, *items):
		"""
		extend(self, items)

		extends the content (see Frag.extend for more info)
		"""
		self.content.extend(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		for attrname in self.attrs.keys():
			attr = self.attrs[attrname]
			convertedattr = attr.convert(converter)
			assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node.attrs[attrname] = convertedattr
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
		for attr in self.attrs.keys():
			node.attrs[attr] = self.attrs[attr].clone()
		return self._decorateNode(node)

	def asPlainString(self):
		return self.content.asPlainString()

	def _addImageSizeAttributes(self, converter, imgattr, widthattr=None, heightattr=None):
		"""
		<par noindent>add width and height attributes to the element for the image that can be found in the attribute
		<argref>imgattr</argref>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <code>"width"</code> and <code>"height"</code>,
		i.e. you could make your image twice as wide with <code>width="%(width)d*2"</code>.</par>

		<par>Passing <code>None</code> as <argref>widthattr</argref> or <argref>heightattr</argref> will
		prevent the repsective attributes from being touched in any way.</par>
		"""

		if self.hasAttr(imgattr):
			size = self[imgattr].convert(converter).ImageSize()
			if size is not None: # the size was retrieved so we can use it
				sizedict = {"width": size[0], "height": size[1]}
				for attr in (heightattr, widthattr):
					if attr is not None: # do something to the width/height
						if self.hasAttr(attr):
							try:
								s = self[attr].convert(converter).asPlainString() % sizedict
								s = str(eval(s))
								s = helpers.unistr(s)
								self[attr] = s
							except TypeError: # ignore "not all argument converted"
								pass
							except:
								raise errors.ImageSizeFormatError(self, attr)
						else:
							self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def _publishAttrs(self, publisher):
		"""
		publishes the attributes. Factored out, so that it
		can be reused.
		"""
		for (attrname, attrvalue) in self.attrs.items():
			if not len(attrvalue): # skip empty attributes
				continue
			publisher.publish(u" ")
			publisher.publish(attrname)
			if isinstance(attrvalue, BoolAttr):
				if publisher.XHTML>0:
					publisher.publish(u"=\"")
					publisher.publish(attrname)
					publisher.publish(u"\"")
			else:
				publisher.publish(u"=\"")
				attrvalue.publish(publisher)
				publisher.publish(u"\"")

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.publish(u"<")
		self._publishName(publisher)
		self._publishAttrs(publisher)
		if len(self):
			if self.empty:
				raise errors.EmptyElementWithContentError(self)
			publisher.publish(u">")
			self.content.publish(publisher)
			publisher.publish(u"</")
			self._publishName(publisher)
			publisher.publish(u">")
		else:
			if publisher.XHTML in (0, 1):
				if self.empty:
					if publisher.XHTML==1:
						publisher.publish(u" /")
					publisher.publish(u">")
				else:
					publisher.publish(u"></")
					self._publishName(publisher)
					publisher.publish(u">")
			elif publisher.XHTML == 2:
				publisher.publish(u"/>")

	def __getitem__(self, index):
		"""
		returns an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list
		(i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			# we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
			try:
				attr = self.attrs[index]
			except KeyError: # if the attribute is not there generate an empty one ...
				try:
					attr = self.attrHandlers[index]()
				except KeyError: # ... if we can
					raise errors.IllegalAttrError(self, index)
				self.attrs[index] = attr
			return attr
		else:
			return self.content[index]

	def __setitem__(self, index, value):
		"""
		sets an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			# values are constructed via the attribute classes specified in the attrHandlers dictionary, which do the conversion
			try:
				attr = self.attrHandlers[index]() # create an empty attribute of the right type
			except KeyError:
				raise errors.IllegalAttrError(self, index)
			attr.extend(value) # put the value into the attribute
			self.attrs[index] = attr # put the attribute in our dict
		else:
			self.content[index] = value

	def __delitem__(self, index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			try:
				del self.attrs[index]
			except KeyError: # ignore non-existing attributes (even if the name is not in self.attrHandlers.keys()
				pass
		else:
			del self.content[index]

	def hasAttr(self, attrname):
		"""
		return whether <self/> has an attribute named <argref>attr</argref>.
		"""
		try:
			attr = self.attrs[attrname]
		except KeyError:
			return 0
		return len(attr)>0

	def getAttr(self, attrname, default=None):
		"""
		works like the method <code>get()</code> of dictionaries,
		it returns the attribute with the name <argref>attr</argref>,
		or if <self/> has no such attribute, <argref>default</argref>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.)
		"""
		attr = self[attrname]
		if attr:
			return attr
		else:
			return self.attrHandlers[attrname](default) # pack the attribute into an attribute object

	def setDefaultAttr(self, attrname, default=None):
		"""
		works like the method <code>setdefault()</code> of dictionaries,
		it returns the attribute with the name <argref>attr</argref>,
		or if <self/> has no such attribute, <argref>default</argref>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.). In this case <argref>default</argref> will be
		kept as the attribute value.
		"""
		attr = self[attrname]
		if not attr:
			attr = self.attrHandlers[attrname](default) # pack the attribute into an attribute object
			self.attrs[index] = attr
		return attr

	def attrKeys(self):
		"""
		return a list with all the attribute names of <self/>.
		"""
		return [ attrname for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

	def attrValues(self):
		"""
		return a list with all the attribute values of <self/>.
		"""
		return [ attrvalue for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

	def attrItems(self):
		"""
		return a list with all the attribute name/value tuples of <self/>.
		"""
		return [ (attrname, attrvalue) for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

	def __getslice__(self, index1, index2):
		"""
		returns a copy of the element that contains a slice of the content
		"""
		return self.__class__(self.content[index1:index2], self.attrs)

	def __setslice__(self, index1, index2, sequence):
		"""
		modifies a slice of the content of the element
		"""
		self.content[index1:index2] = sequence

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the element
		"""
		del self.content[index1:index2]

	def __nonzero__(self):
		"""
		return whether the element is not empty (this should be a little faster than defaulting to __len__)
		"""
		return self.content.__nonzero__()

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		for attr in self.attrs.keys():
			convertedattr = self.attrs[attr].compact()
			assert isinstance(convertedattr, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node.attrs[attr] = convertedattr
		return self._decorateNode(node)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if searchattrs:
			for attr in self.attrs.keys():
				node.extend(self[attr].find(type, subtype, attrs, test, searchchildren, searchattrs))
		node.extend(self.content.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def copyDefaultAttrs(self, fromDict=None):
		"""
		Sets attributes that are not set <self/> to the default
		values taken from the fromDict dictionary.
		If fromDict is omitted, defaults are taken from self.defaults.

		Note: Boolean attributes may savely be set to zero or one (integer).
		as only the fact that a boolean attribte exists matters.
		"""

		if fromDict is None:
			fromDict = self.defaults
		for (attrname, attrvalue) in fromDict.items():
			if not self.hasAttr(attrname):
				self[attrname] = attrvalue

	def withSeparator(self, separator, clone=0):
		"""
		returns a version of <self/> with a separator node between the child nodes of <self/>.

		for more info see <pyref module="xist.xsc" class="Frag" method="withSeparator">Frag.withSeparator</pyref>.
		"""
		node = self.__class__(**self.attrs)
		node.content = self.content.withSeparator(separator, clone)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(node1.asPlainString(), node2.asPlainString())):
		"""
		returns a sorted version of <self/>.
		"""
		node = self.__class__(**self.attrs)
		node.content = self.content.sorted(compare)
		return node

	def reversed(self):
		"""
		returns a reversed version of <self/>.
		"""
		node = self.__class__(**self.attrs)
		node.content = self.content.reversed()
		return node

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = self.__class__()
		node.content = self.content.filtered(function)
		node.attrs = self.attrs
		return node

	def shuffled(self):
		"""
		returns a shuffled version of the <self/>.
		"""
		node = self.__class__()
		node.content = self.content.shuffled()
		node.attrs = self.attrs
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self.__class__(*self.content.mapped(function))
			node.attrs = self.attrs.copy()
		return node

	def normalized(self):
		node = self.__class__()
		node.content = self.content.normalized()
		for (attrname, attrvalue) in self.attrs.items():
			node[attrname] = attrvalue.normalized()
		return node

class Entity(Node):
	"""
	<par noindent>Class for entities. Derive your own entities from
	it and implement <code>convert()</code> and <code>asPlainString()</code>.</par>
	"""

	def compact(self):
		return self

	clone = compact

	def present(self, presenter):
		presenter.presentEntity(self)

	def publish(self, publisher):
		publisher.publish(u"&")
		self._publishName(publisher)
		publisher.publish(u";")

class CharRef(Entity):
	"""
	<par>A simple character reference, the codepoint is in the class attribute
	<pyref attribute="codepoint">codepoint</pyref>.</par>
	"""

	def convert(self, converter):
		node = Text(unichr(self.codepoint))
		return self._decorateNode(node)

	def compact(self):
		return self

	clone = compact

	def asPlainString(self):
		return unichr(self.codepoint)

class Null(Node):
	"""
	node that does not contain anything.
	"""

	def convert(self, converter):
		return self

	def clone(self):
		pass

	compact = clone

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

Null = Null() # Singleton, the Python way

class Attr(Frag):
	"""
	<par noindent>Base classes of all attribute classes.</par>

	<par>The content of an attribute may be any other XSC node. This is different from
	a normal DOM, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements) to be put into attributes.</par>

	<par>Of course, this dynamic content when finally converted to HTML will normally result in
	a fragment consisting only of text and character references.</par>
	"""

	def present(self, presenter):
		presenter.presentAttr(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.inAttr = 1
		Frag.publish(self, publisher)
		publisher.inAttr = 0

class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""

class NumberAttr(Attr):
	"""
	Attribute class that is used for normal number attributes.
	"""

class IntAttr(NumberAttr):
	"""
	Attribute class that is used for normal integer attributes.
	"""

class FloatAttr(NumberAttr):
	"""
	Attribute class that is used for normal float attributes.
	"""

class BoolAttr(Attr):
	"""
	Attribute class that is used for boolean attributes.
	"""

class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs.

	XSC has one additional feature, path markers (these are directory names starting with *).
	An URL starting with a path marker is relative to the directory marked with the same path
	marker in the appropriate base URL.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify a file from everywhere via "*/dir/to/file.xsc". XSC will change this to an URL
	that correctly locates the file (e.g. "../../../dir/to/file.xsc", when you're currenty nested three levels
	deep in a different directory than "dir".

	Server relative URLs will be shown with the pseudo scheme "server". For checking these URLs
	for image or file size, a http request will be made to the server specified in the server
	option (options.server).

	For all other URLs a normal request will be made corresponding to the specified scheme
	(http, ftp, etc.)
	"""

	def __init__(self, *content):
		self.base = url.URL()
		Attr.__init__(self, *content)

	def _str(self, content=None, brackets=None, slash=None, ansi=None):
		attr = " %s=%s%s%s" % (strAttrName("base", ansi), strQuote(ansi=ansi), strURL(self.base.asString(), ansi=ansi), strQuote(ansi=ansi))
		return Attr._str(self, content=attr, brackets=brackets, slash=slash, ansi=ansi)

	def present(self, presenter):
		presenter.presentURLAttr(self)

	def publish(self, publisher):
		u = self.asURL()
		if u.scheme is None:
			return Text(u.asPlainString()).publish(publisher)
		else:
			return Text(u.relativeTo(publisher.base).asPlainString()).publish(publisher)

	def convert(self, converter):
		node = Attr.convert(self, converter)
		node.base = self.base.clone()
		return node

	def clone(self):
		node = Attr.clone(self)
		node.base = self.base.clone()
		return node

	def compact(self):
		node = Attr.compact(self)
		node.base = self.base.clone()
		return node

	def asURL(self):
		return url.URL(Attr.asPlainString(self))

	def asPlainString(self):
		return self.asURL().asString()

	def forInput(self):
		u = self.base + self.asURL()
		if u.scheme == "server":
			u = url.URL(scheme="http", server=options.server) + u
		return u

	def ImageSize(self):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""

		size = None
		if Image is not None:
			url = self.forInput()
			if url.isRetrieve():
				try:
					(filename, headers) = url.retrieve()
					if headers.maintype == "image":
						img = Image.open(filename)
						size = img.size
						del img
					urllib.urlcleanup()
				except IOError:
					urllib.urlcleanup()
					raise errors.FileNotFoundError(url)
		return size

	def FileSize(self):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""

		url = self.forInput()

		size = None
		if url.isRetrieve():
			try:
				(filename, headers) = url.retrieve()
				size = os.stat(filename)[stat.ST_SIZE]
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise errors.FileNotFoundError(url)
		return size

	def open(self):
		"""
		opens the URL via urllib
		"""
		return self.forInput().open()

###
###
###

class Namespace:
	"""
	an XML namespace, contains the classes for the elements, entities and processing instructions
	in the namespace.
	"""

	def __init__(self, prefix, uri, thing=None):
		self.prefix = helpers.unistr(prefix)
		self.uri = helpers.unistr(uri)
		self.elementsByName = {} # dictionary for mapping element names to classes
		self.entitiesByName = {} # dictionary for mapping entity names to classes
		self.procInstsByName = {} # dictionary for mapping processing instruction target names to classes
		self.charrefsByName = {} # dictionary for mapping character reference names to classes
		self.charrefsByNumber = {} # dictionary for mapping character reference code points to classes
		self.register(thing)
		namespaceRegistry.register(self)

	def register(self, thing):
		"""
		<par noindent>this function lets you register <argref>thing</argref> in the namespace.
		If <argref>thing</argref> is a class derived from <classref>Element</classref>,
		<classref>Entity</classref> or <classref>ProcInst</classref> it will be registered
		in the following way: The class <argref>thing</argref> will be registered under it's
		class name (<code><argref>thing</argref>.__name__</code>). If you want to change this
		behaviour, do the following: set a class variable <code>name</code> to the name you
		want to be used. If you don't want <argref>thing</argref> to be registered at all,
		set <code>name</code> to <code>None</code>.

		<par>After the call <argref>thing</argref> will have two class attributes:
		<code>name</code>, which is the name under which the class is registered and
		<code>namespace</code>, which is the namespace itself (i.e. <self/>).</par>

		<par>If <argref>thing</argref> already has an attribute <code>namespace</code>, it
		won't be registered again.</par>

		<par>If <argref>thing</argref> is a dictionary, every object in the dictionary
		will be registered.</par>

		<par>All other objects are ignored.</par>
		"""

		t = type(thing)
		if t is types.ClassType:
			iselement = thing is not Element and issubclass(thing, Element)
			isentity = thing is not Entity and issubclass(thing, Entity)
			if isentity:
				ischarref = thing is not CharRef and issubclass(thing, CharRef)
				if ischarref:
					isentity = 0
			else:
				ischarref = 0
			isprocinst = thing is not ProcInst and issubclass(thing, ProcInst)
			if iselement or isentity or ischarref or isprocinst:
				# if the class attribute register is 0, the class won't be registered
				# and if the class already has a namespace attribute, it is already registered, so it won't be registered again
				# (we're accessing __dict__ here, because we don't want the attribute from the base class object)
				if thing.register and (not thing.__dict__.has_key("namespace")):
					try:
						name = thing.__dict__["name"] # no inheritance, otherwise we might get the name attribute from an already registered base class
					except KeyError:
						name = thing.__name__
					thing.namespace = self # this creates a cycle
					if name is not None:
						name = helpers.unistr(name)
						thing.name = name
						if iselement:
							self.elementsByName[name] = thing
						elif isentity:
							self.entitiesByName[name] = thing
						elif ischarref:
							self.charrefsByName[name] = thing
							self.charrefsByNumber.setdefault(thing.codepoint, []).append(thing)
						else: # if isprocinst:
							self.procInstsByName[name] = thing
		elif t is types.DictionaryType:
			for key in thing.keys():
				self.register(thing[key])

	def __repr__(self):
		return "<%s.%s instance prefix=%r uri=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.prefix, self.uri, id(self))

class NamespaceRegistry:
	"""
	global registry for all namespaces
	"""
	def __init__(self):
		self.byPrefix = {}
		self.byURI = {}

	def register(self, namespace):
		self.byPrefix[namespace.prefix] = namespace
		self.byURI[namespace.uri] = namespace

namespaceRegistry = NamespaceRegistry()

class Namespaces:
	"""
	list of namespaces to be searched in a specific order
	to instantiate elements, entities and procinsts.
	"""
	def __init__(self, *namespaces):
		self.namespaces = []
		self.pushNamespace(namespace) # always include the namespace object from our own modules with &gt; etc.
		self.pushNamespace(*namespaces)

	def pushNamespace(self, *namespaces):
		"""
		pushes the namespaces onto the stack in this order,
		i.e. the last one in the list will be the first
		one to be searched.

		items in namespaces can be:
			1. namespace objects,
			2. Module objects, in which case module.namespace
			   will be used as the Namespace object
			3. strings, which specify the namespace
			   prefix, i.e. namespaceRegistry.byPrefix[string]
			   will be used.
		"""
		for namespace in namespaces:
			if type(namespace) is types.ModuleType:
				namespace = namespace.namespace
			elif type(namespace) in (types.StringType, types.UnicodeType):
				namespace = namespaceRegistry.byPrefix[namespace]
			self.namespaces.insert(0, namespace) # built in reverse order, so a simple "for in" finds the most recent entry.

	def popNamespace(self, count=1):
		del self.namespaces[:count]

	def __splitName(self, name):
		"""
		split a qualified name into a namespace,name pair
		"""
		name = name.split(":")
		if len(name) == 1: # no namespace specified
			name.insert(0, None)
		return name

	def __allNamespaces(self):
		"""
		returns a list of all namespaces to be searched in this order
		"""
		return self.namespaces+namespaceRegistry.byPrefix.values()

	def elementFromName(self, name):
		"""
		returns the element class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.elementsByName[name[1]]
				except KeyError: # no element in this namespace with this name
					pass
		raise errors.IllegalElementError(name) # elements with this name couldn't be found

	def entityFromName(self, name):
		"""
		returns the entity or charref class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		namespaces = self.__allNamespaces()
		# try the charrefs first
		for namespace in namespaces:
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.charrefsByName[name[1]]
				except KeyError: # no charref in this namespace with this name
					pass
		# no charrefs => try the entities now
		for namespace in namespaces:
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.entitiesByName[name[1]]
				except KeyError: # no entity in this namespace with this name
					pass
		raise errors.IllegalEntityError(name) # entities with this name couldn't be found

	def procInstFromName(self, name):
		"""
		returns the processing instruction class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.procInstsByName[name[1]]
				except KeyError: # no processing instruction in this namespace with this name
					pass
		raise errors.IllegalProcInstError(name) # processing instructions with this name couldn't be found

	def charrefFromNumber(self, number):
		"""
		returns the first charref class for the codepoint number.
		"""
		for namespace in self.__allNamespaces():
			try:
				return namespace.charrefsByNumber[number][0]
			except KeyError:
				pass
		return None

# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62

namespace = Namespace("xsc", "", vars())

defaultNamespaces = Namespaces()

###
###
###

class Location:
	"""
	Represents a location in an XML entity.
	"""

	def __init__(self, locator=None, sysID=None, pubID=None, lineNumber=-1, columnNumber=-1):
		"""
		Initialized by being passed a locator, from which it reads off the current location,
		which is then stored internally. In addition to that the systemID, public ID, line number
		and column number can be overwritten by explicit arguments.
		"""
		if locator is None:
			self.__sysID = None
			self.__pubID = None
			self.__lineNumber = -1
			self.__columnNumber = -1
		else:
			self.__sysID = locator.getSystemId()
			self.__pubID = locator.getPublicId()
			self.__lineNumber = locator.getLineNumber()
			self.__columnNumber = locator.getColumnNumber()
		if self.__sysID is None:
			self.__sysID = sysID
		if self.__pubID is None:
			self.__pubID = pubID
		if self.__lineNumber == -1:
			self.__lineNumber = lineNumber
		if self.__columnNumber == -1:
			self.__columnNumber = columnNumber

	def getColumnNumber(self):
		"Return the column number of this location."
		return self.__columnNumber

	def getLineNumber(self):
		"Return the line number of this location."
		return self.__lineNumber

	def getPublicId(self):
		"Return the public identifier for this location."
		return self.__pubID

	def getSystemId(self):
		"Return the system identifier for this location."
		return self.__sysID

	def offset(self, offset):
		"""
		returns a location where the line number is incremented by offset
		(and the column number is reset to 1).
		"""
		if offset==0:
			columnNumber = -1
		else:
			columnNumber = 1
		return Location(sysID=self.__sysID, pubID=self.__pubID, lineNumber=self.__lineNumber+offset, columnNumber=columnNumber)

	def __str__(self):
		# get and format the system ID
		sysID = self.getSystemId()
		if sysID is None:
			sysID = "???"

		# get and format the line number
		line = self.getLineNumber()
		if line==-1:
			line = "?"
		else:
			line = str(line)

		# get and format the column number
		column = self.getColumnNumber()
		if column==-1:
			column = "?"
		else:
			column = str(column)

		# now we have the parts => format them
		return "%s:%s:%s" % (presenters.strURL(sysID), presenters.strNumber(line), presenters.strNumber(column))

	def __repr__(self):
		return "<%s object sysID=%r, pubID=%r, lineNumber=%r, columnNumber=%r at %08x>" % \
			(self.__class__.__name__, self.getSystemId(), self.getPublicId(), self.getLineNumber(), self.getColumnNumber(), id(self))
