Delimiters
##########

It is possible to specify alternative delimiters for the template tags::

	>>> from ll import ul4c
	>>> t = ul4c.Template(
	... 	"{{for i in range(10)}}{{print i}};{{end for}}",
	... 	startdelim="{{",
	... 	enddelim="}}"
	... )
	>>> t.renders()
	'0;1;2;3;4;5;6;7;8;9;'
