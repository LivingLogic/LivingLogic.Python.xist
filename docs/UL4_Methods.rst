Methods
#######

Objects in :mod:`ll.ul4c` support some methods too (depending on the type of the
object).


``str``
=======

Strings support the following methods:

``upper()``
-----------

The ``upper`` method of strings returns an uppercase version of the string for
which it's called:

.. sourcecode:: ul4

	<?print 'foo'.upper()?>

prints ``FOO``.


``lower()``
-----------

The ``lower`` method of strings returns an lowercase version of the string for
which it's called.


``capitalize()``
----------------

The ``capitalize`` method of strings returns a copy of the string with its first
letter capitalized.


``startswith(prefix, /)``
-------------------------

``x.startswith(y)`` returns ``True`` if the string ``x`` starts with the string
``y`` and ``False`` otherwise. ``y`` may also be a list of string. In this case
``x.startswith(y)`` returns ``True`` if ``x`` starts with any of the strings in
``y``.


``endswith(suffix, /)``
-----------------------

``x.endswith(y)`` returns ``True`` if the string ``x`` ends with the string
``y`` and ``False`` otherwise. ``y`` may also be a list of string. In this case
``x.endswith(y)`` returns ``True`` if ``x`` ends with any of the strings in
``y``.


``strip(chars=None, /)``
------------------------

The string method ``strip`` returns a copy of the string with leading and
trailing whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``lstrip(chars=None, /)``
-------------------------

The string method ``lstrip`` returns a copy of the string with leading
whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``rstrip(chars=None, /)``
-------------------------

The string method ``rstrip`` returns a copy of the string with trailing
whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``removeprefix(prefix, /)``
-------------------------

Remove the prefix ``prefix`` from the string. If the string doesn't start with
``prefix`` the string is returned unodified.


``removesuffix(suffix, /)``
-------------------------

Remove the suffix ``suffix`` from the string. If the string doesn't start with
``suffix`` the string is returned unodified.


``split(sep=None, maxsplit=None)``
----------------------------------

The string method ``split`` splits the string into separate "words" and returns
the resulting list. Without any arguments, the string is split on whitespace
characters. With one argument the argument specifies the separator to use. The
second optional argument specifies the maximum number of splits to do.


``rsplit(sep=None, maxsplit=None)``
-----------------------------------

The string method ``rsplit`` works like ``split``, except that splitting starts
from the end (which is only relevant when the maximum number of splits is
given).


``splitlines(keepends=False)``
------------------------------

The string method ``splitlines`` splits the string into a list of lines,
using Unicode line ending characters, i.e. the following character sequences
terminate a line:  ``"\n"``, ``"\r"``, ``"\r\n"``, ``"\x0b"``, ``"\x0c"``,
``"\x1c"``, ``"\x1d"``, ``"\x1e"``, ``"\x85"``, ``"\u2028"`` and ``"\u2029"``.
Line breaks are not included in the resulting list unless a second parameter is
given and true.


``count(sub, start=None, end=None, /)``
---------------------------------------

This method counts non-overlapping occurrences of a substring in a string.
For example ``"abababa".count("aba")`` returns 2. The optional second and third
argument specify the start and end position for the search.


``find(sub, start=None, end=None, /)``
--------------------------------------

This method searches for a substring of the string and returns the position of
the first appearance of the substring or -1 if the substring can't be found.
For example ``"foobar".find("bar")`` returns 3. The optional second and third
argument specify the start and end position for the search.


``rfind(sub, start=None, end=None, /)``
---------------------------------------

This method works like ``find`` but searches from the end.


``replace(old, new, count=-1, /)``
----------------------------------

The string method ``replace`` has two arguments. It returns a new string where
each occurrence of the first argument is replaced by the second argument, i.e.
``"abracadabra".replace("ab", "ba")`` returns ``"baracadbara"``. If the third
argument ``count`` non-negative is specifies the maximum number of replacements.


``join(iterable, /)``
---------------------

``join`` is a string method. It returns a concatentation of the strings in the
argument sequence with the string itself as the separator, i.e.:

.. sourcecode:: ul4

	<?print "+".join("1234")?>

outputs ``1+2+3+4``.


``isdigit()``
-------------

``s.isdigit()`` returns ``True`` if all characters in the string ``s`` are
digits and there is at least one character, ``False`` otherwise.


``isasciidigit()``
------------------

``s.isasciidigit()`` returns ``True`` if all characters in the string ``s`` are
ASCII digits and there is at least one character, ``False`` otherwise.


``list``
========

List objects support the following methods:

``count(sub, start=None, end=None, /)``
---------------------------------------

This method counts occurrences of an item in a list. The optional second and
third argument specify the start and end position for the search.


``find(sub, start=None, end=None, /)``
--------------------------------------

This method searches for an item in a list and returns the position of the first
appearance of the item or -1 if the item can't be found. The optional second and
third argument specify the start and end position for the search.


``rfind(sub, start=None, end=None, /)``
---------------------------------------

This method works like ``find`` but searches from the end.


``append(*items)``
------------------

``append`` its arguments to the end of the list for which it is called:

.. sourcecode:: ul4

	<?code v = [1, 2]?>
	<?code v.append(3, 4)?>
	<?print v?>

prints ``[1, 2, 3, 4]``.


``insert(pos, *items)``
-----------------------

``insert``\s first argument in the insert position, the remaining arguments are
the items that will be inserted at that position, so:

.. sourcecode:: ul4

	<?code v = [1, 4]?>
	<?code v.insert(1, 2, 3)?>
	<?print v?>

prints ``[1, 2, 3, 4]``.


``dict``
========

Dictionaries have the following methods:


``keys()``
----------

Return an iterator over the keys ob the dictionary (this is the same as iterating
over the dictionary itself).


``items()``
-----------

Return an iterator over entries of the dictionary as (key, value) pairs.


``values()``
------------

Return an iterator over values of the dictionary.


``get(key, default=None, /)``
-----------------------------

``get`` is a dictionary method. ``d.get(k, v)`` returns ``d[k]`` if the key
``k`` is in ``d``, else ``v`` is returned. If ``v`` is not given, it defaults
to ``None``.


``update(*args, **kwargs)``
---------------------------

``update`` supports an arbitrary number of positional and keyword arguments.
Each positional argument may be a dictionary, all the items in the dictionary
will be copied to the target dictionary. A positional argument may also be an
iterable of ``(key, value)`` pairs. These will also be copied to the target
dictionary. After each positional argument is copied over in a last step the
keyword arguments will be copied to the target dictionary.


``clear()``
-----------

``clear()`` makes a dictionary empty.


``set``
=======

Set object have the following methods:


``add(*items)``
---------------

``add()`` adds all arguments to the set.


``clear()``
-----------

``clear()`` makes a set empty.


``pop(pos=-1)``
---------------

``pop`` removes the last item of the list and returns it. If an index is passed
the item at that position is removed and returned. A negative index is treated
as relative to the end of the list.


Templates
=========

Templates have the following method:


``renders(...)``
----------------

The ``renders`` method of template objects renders the template and returns the
output as a string. Parameters can be passed via keyword arguments or via the
``**`` syntax:

.. sourcecode:: ul4

	<?code output = template.renders(a=17, b=23)?>
	<?code data = {'a': 17, 'b': 23)?>
	<?code output = template.renders(**data)?>

(Also if the template has a signature, positional arguments and the ``*`` syntax
are supported.)


``date`` and ``datetime``
=========================

``date`` and ``datetime`` objects have the following methods:

``isoformat()``
---------------

``isoformat`` returns the date/datetime object in ISO 8601 format, i.e.:

.. sourcecode:: ul4

	<?print now().isoformat()?>

might output ``2010-02-22T18:30:29.569639``,

and:

.. sourcecode:: ul4

	<?print today().isoformat()?>

might output ``2010-02-22``.


``mimeformat()``
----------------

``mimeformat`` returns the date/datetime object in MIME format (assuming the
object is in UTC), i.e.:

.. sourcecode:: ul4

	<?print utcnow().mimeformat()?>

might output ``Mon, 22 Feb 2010 17:38:40 GMT``,

and:

.. sourcecode:: ul4

	<?print today().mimeformat()?>

might output ``Mon, 22 Feb 2010``.


``day()``, ``month()``, ``year()``, ``hour()``, ``minute()``, ``second()``, ``microsecond()`` and ``weekday()``
---------------------------------------------------------------------------------------------------------------

Those methods return a specific attribute of a date or datetime object.
For example the following reproduces the ``mimeformat`` output from above
(except for the linefeeds of course):

.. sourcecode:: ul4

	<?code weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']?>
	<?code months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']?>
	<?code t = @(2010-02-22T17:38:40.123456)?>
	<?print weekdays[t.weekday()]?>,
	<?print format(t.day(), '02')?>
	<?print months[t.month()-1]?>
	<?print format(t.year(), '04')?>
	<?print format(t.hour(), '02')?>:
	<?print format(t.minute(), '02')?>:
	<?print format(t.second(), '02')?>.
	<?print format(t.microsecond(), '06')?> GMT


``date()``
----------

For date objects ``date()`` returns the object unmodified, for datetime objects
a date object containing the date portion of the object is returned, so:

.. sourcecode:: ul4

	<?print @(2000-02-29T12:34:56.987654).date()?>

prints ``2000-02-29``.


``timestamp()``
---------------

The method ``timestamp()`` of date and datetime objects returns the number of
seconds (with microseconds precision) between this date and 1970-01-01T00:00:00.


``calendar(firstweekday=0, mindaysinfirstweek=4)``
-------------------------------------------------------

``d.calendar()`` returns a list containing:

1. the calendar year ``d`` belongs to;
2. the calendar week number of ``d``;
3. the weekday of ``d``

(A day might belong to a different calender year, if it is in week 1 but before
January 1, or if belongs to week 1 of the following year).

``firstweekday`` defines what a week is (i.e. which weekday is considered
the start of the week, ``0`` is Monday and ``6`` is Sunday).
``mindaysinfirstweek`` defines how many days must be in a week to be
considered the first week in the year.

For example for the ISO week number (according to
https://en.wikipedia.org/wiki/ISO_week_date) the week starts on Monday
(i.e. ``firstweekday == 0``) and a week is considered the first week if
it's the first week that contains a Thursday (which means that this week
contains at least four days in January, so ``mindaysinfirstweek == 4``).

For the US ``firstweekday == 6`` and ``mindaysinfirstweek == 1``, i.e.
the week starts on Sunday and January the first is always in week 1.

There's also the convention that the week 1 is the first complete week
in January. For this ``mindaysinfirstweek == 7``.


``week(firstweekday=0, mindaysinfirstweek=4)``
----------------------------------------------

``week`` returns the calendar week number of the date for which it is called.
For more information see the method ``calendar``.


``yearday()``
-------------

``yearday`` returns the number of days since the beginning of the year, so:

.. sourcecode:: ul4

	<?print @(2010-01-01).yearday()?>

prints ``1`` and:

.. sourcecode:: ul4

	<?print @(2010-12-31).yearday()?>

prints ``365``.


``color``
=========

Color objects support the following methods:

``r()``
	Return the red component of the color (as an 8-bit integer).

``g()``
	Return the green component of the color (as an 8-bit integer).

``b()``
	Return the blue component of the color (as an 8-bit integer).

``a()``
	Return the alpha (opacity) component of the color (as an 8-bit integer).

``hsv()``
	Return the color as an HSV tuple ("hue", "saturation", "value"). All three
	values are between 0.1 and 1.0.

``hsva()``
	Similar to ``hsv()``, but returns the alpha (opacity) as the fourth tuple
	item.

``hls()``
	Return the color as an HLS tuple ("hue", "saturation", "lightness"). All
	three values are between 0.1 and 1.0.

``hlsa()``
	Similar to ``hls()``, but returns the alpha (opacity) as the fourth tuple
	item.

	For more info about the HSV and HSV color models see Wikipedia__.

	__ https://en.wikipedia.org/wiki/HSL_and_HSV

``hue()``
	Return the hue value of the HLS color tuple.

``sat()``
	Return the saturation value of the HLS color tuple.

``light()``
	Return the lightness value of the HLS color tuple.

``lum()``
	Return the luminance value of the color tuple, which is similar to lightness
	but is the following **weighted** sum of the components:

	.. sourcecode:: python

		(0.2126 * r() + 0.7152 * g() + 0.0722 * b())/255

``withhue(hue)``
	Return a new color with the HLS hue replaced by ``hue``.

``withlight(light)``
	Return a new color with the HLS lightness replaced by ``light``.

``withsat(sat)``
	Return a new color with the HLS saturation replaced by ``sat``.

``witha(a)``
	Return a new color with the alpha (opacity) component replaced by ``a``.

``withlum(lum)``
	Return a new color with the luminance replaced by ``lum``.

``abslight(f)``
	Return a new color with ``f`` added to the HLS lightness of the original color.

``rellight(f)``
	Return a new color where the HLS lightness of the original color has been
	modified.

	If ``f`` is positive the lightness will be increased, with ``f==1``
	giving a lightness of 1. If ``f`` is negative, the lightness will be
	decreased with ``f==-1`` giving a lightness of 0. ``f==0`` will leave
	the lightness unchanged. All other values return a linear interpolation.

``abslum(f)``
	Return a new color with ``f`` added to the luminance of the original color.
	I.e. for a color ``c`` the following should always print ``True``:

	.. sourcecode:: ul4

		<?print c.abslum(f).lum() == c.lum() + f?>

	(except for rounding errors and when the modified luminance would be smaller
	than 0 or larger than 1).

``rellum(f)``
	Return a new color with ``f`` used to modify the luminance of the original
	color.

	If ``f`` is positive the luminance will be increased, with ``f==1`` giving
	a luminance of 1. If ``f`` is negative, the luminance will be decreased
	with ``f==-1`` giving a luminance of 0. ``f==0`` will leave the luminance
	unchanged. All other values return a linear interpolation.

``combine(r=None, g=None, b=None, a=None)``
	Return a new color with some of its components replaced by the arguments.
	If a component is not passed (or the value ``None`` is given) the component
	will be unchanged in the resulting color.

``invert(f=1.0)``
	Return an inverted version of the original color, i.e. for each color ``c``
	the following prints ``True`` three times:

	.. sourcecode:: ul4

		<?print c.invert().r() == 255 - c.r()?>
		<?print c.invert().g() == 255 - c.g()?>
		<?print c.invert().b() == 255 - c.b()?>

	``f`` specifies the amount of inversion, with 1 returning a complete
	inversion, and 0 returning the original color. Values between 0 and 1 return
	an interpolation of both extreme values. (So 0.5 always returns medium grey).
