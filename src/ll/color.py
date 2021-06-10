# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2004-2021 by LivingLogic AG, Bayreuth/Germany
## Copyright 2004-2021 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.color` provides classes and functions for handling RGBA colors.
"""


import colorsys

from ll import ul4c


from typing import *
OptStr = Optional[str]
Number = Union[int, str]


__docformat__ = "reStructuredText"


def _interpolate(lower:float, upper:float, factor:float) -> float:
	return factor*upper + (1-factor) * lower


class Color(tuple):
	"""
	A :class:`Color` object represents a color with 8-bit red, green and blue
	components and transparency.
	"""

	ul4_type = ul4c.InstantiableType("color", "Color", "An RGBA color object with 8-bit red, green and blue components and transparency.")
	ul4_attrs = {"r", "g", "b", "a", "hsv", "hsva", "hls", "hlsa", "hue", "invert", "sat", "lum", "luma", "withhue", "withsat", "withlum", "withluma", "witha", "abslum", "rellum", "absluma", "relluma", "combine", "invert"}

	def __new__(cls, r:int=0x0, g:int=0x0, b:int=0x0, a:int=0xff):
		"""
		Create a :class:`!Color` with the 8 bit red, green, blue and alpha
		components ``r``, ``g``, ``b`` and ``a``. Values will be
		clipped to the range [0; 255].
		"""
		return tuple.__new__(cls, (max(0, min(int(r), 255)), max(0, min(int(g), 255)), max(0, min(int(b), 255)), max(0, min(int(a), 255))))

	@classmethod
	def fromrepr(cls, s:str) -> "Color":
		try:
			if len(s) == 9:
				return cls(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), int(s[7:], 16))
			elif len(s) == 7:
				return cls(int(s[1:3], 16), int(s[3:5], 16), int(s[5:], 16))
			elif len(s) == 5:
				return cls(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16), 17*int(s[4], 16))
			elif len(s) == 4:
				return cls(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16))
		except ValueError:
			pass
		raise ValueError(f"can't interpret {s!r} as color repr value")

	@classmethod
	def fromcss(cls, s:str) -> "Color":
		"""
		Create a :class:`Color` object from the CSS__ color string ``s``.
		All formats from CSS2 are supported (i.e. ``'#xxx'``, ``'#xxxxxx'``,
		``rgb(r, g, b)``, ``rgb(r%, g%, b%)``, ``rgba(r, g, b, a)``,
		``rgba(r%, g%, b%, a)``  and color names like ``'red'``).

		__ http://www.w3.org/TR/css3-color/#colorunits
		"""
		if s.startswith("#"):
			if len(s) == 4:
				return cls(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16))
			elif len(s) == 5:
				return cls(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16), 17*int(s[4], 16))
			elif len(s) == 7:
				return cls(int(s[1:3], 16), int(s[3:5], 16), int(s[5:], 16))
			elif len(s) == 9:
				return cls(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), int(s[7:], 16))
		elif s.startswith("rgb(") and s.endswith(")"):
			channels = []
			for x in s[4:-1].split(","):
				x = x.strip()
				if x.endswith("%"):
					v = float(x[:-1])*0xff/100
				else:
					v = int(x)
				channels.append(v)
			return cls(*channels)
		elif s.startswith("rgba(") and s.endswith(")"):
			channels = []
			for x in s[5:-1].split(","):
				x = x.strip()
				if x.endswith("%"):
					v = float(x[:-1])*0xff/100
				elif len(channels) == 3: # alpha value
					v = float(x)*0xff
				else:
					v = int(x)
				channels.append(v)
			return cls(*channels)
		elif s in csscolors:
			return csscolors[s]
		raise ValueError(f"can't interpret {s!r} as css value")

	@classmethod
	def fromrgb(cls, r:Number, g:Number, b:Number, a:Number=1.0) -> "Color":
		"""
		Create a :class:`Color` object from the red, green, blue and alpha values
		``r``, ``g``, ``b`` and ``a``. All values will be clipped to the range
		[0; 1].
		"""
		return cls(255*r, 255*g, 255*b, 255*a)

	@classmethod
	def fromhsv(cls, h:Number, s:Number, v:Number, a:Number=1.0) -> "Color":
		"""
		Create a :class:`Color` object from the hue, saturation and value values
		``h``, ``s`` and ``v`` and the alpha value ``a``. The hue value will be
		used modulo 1.0, saturation, value and alpha will be clipped to the range
		[0; 1].
		"""
		rgb = colorsys.hsv_to_rgb(h % 1.0, max(0., min(s, 1.)), max(0., min(v, 1.)))
		return cls.fromrgb(*(rgb + (a,)))

	@classmethod
	def fromhls(cls, h:Number, l:Number, s:Number, a:Number=1.0) -> "Color":
		"""
		Create a :class:`Color` object from the hue, luminance and saturation
		values ``h``, ``l`` and ``s`` and the alpha value ``a``. The hue value
		will be used modulo 1.0, luminance, saturation and alpha will be clipped
		to the range [0; 1].
		"""
		rgb = colorsys.hls_to_rgb(h % 1.0, max(0., min(l, 1.)), max(0., min(s, 1.)))
		return cls.fromrgb(*(rgb + (a,)))

	def __repr__(self) -> str:
		if self[3] != 0xff:
			return f"Color({self[0]:#04x}, {self[1]:#04x}, {self[2]:#04x}, {self[3]:#04x})"
		else:
			return f"Color({self[0]:#04x}, {self[1]:#04x}, {self[2]:#04x})"

	def __str__(self) -> str:
		"""
		``self`` formatted as a CSS color string.
		"""
		if self[3] != 0xff:
			return f"rgba({self[0]},{self[1]},{self[2]},{self[3]/255.:.3f})"
		else:
			s = f"#{self[0]:02x}{self[1]:02x}{self[2]:02x}"
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6]:
				s = f"#{s[1]}{s[3]}{s[5]}"
		return s

	def r(self) -> int:
		"""
		The red value as an int between 0 and 255.
		"""
		return self[0]

	def g(self) -> int:
		"""
		The green value as an int between 0 and 255.
		"""
		return self[1]

	def b(self) -> int:
		"""
		The blue value as an int between 0 and 255.
		"""
		return self[2]

	def a(self) -> int:
		"""
		The alpha value as an int between 0 and 255.
		"""
		return self[3]

	def rgb(self) -> Tuple[float, float, float]:
		"""
		The red, green and blue value as a float tuple with values between
		0.0 and 1.0.
		"""
		return (self[0]/255., self[1]/255., self[2]/255.)

	def rgba(self) -> Tuple[float, float, float, float]:
		"""
		The red, green, blue and alpha value as a float tuple with values between
		0.0 and 1.0.
		"""
		return (self[0]/255., self[1]/255., self[2]/255., self[3]/255.)

	def hsv(self) -> Tuple[float, float, float]:
		"""
		``self`` as a HSV tuple ("hue, saturation, value").
		All three values are between 0.0 and 1.0.
		"""
		return colorsys.rgb_to_hsv(self[0]/255., self[1]/255., self[2]/255.)

	def hsva(self) -> Tuple[float, float, float, float]:
		"""
		``self`` as a HSV+alpha tuple ("hue, saturation, value, alpha").
		All four values are between 0.0 and 1.0.
		"""
		return self.hsv() + (self[3]/255.,)

	def hls(self) -> Tuple[float, float, float]:
		"""
		``self`` as a HLS tuple ("hue, luminance, saturation"). All three
		values are between 0.0 and 1.0.
		"""
		return colorsys.rgb_to_hls(self[0]/255., self[1]/255., self[2]/255.)

	def hlsa(self) -> Tuple[float, float, float, float]:
		"""
		``self`` as a HLS+alpha tuple ("hue, luminance, saturation, alpha").
		All four values are between 0.0 and 1.0.
		"""
		return self.hls() + (self[3]/255.,)

	def hue(self) -> float:
		"""
		The hue value from :meth:`hls`.
		"""
		return self.hls()[0]

	def lum(self) -> float:
		"""
		The luminance value from :meth:`hls`.
		"""
		return self.hls()[1]

	def sat(self) -> float:
		"""
		The saturation value from :meth:`hls`.
		"""
		return self.hls()[2]

	def luma(self) -> float:
		"""
		Luma according to sRGB:

		.. sourcecode:: python

			(0.2126*r + 0.7152*g + 0.0722*b)/255
		"""
		return (0.2126 * self[0] + 0.7152 * self[1] + 0.0722 * self[2])/255.

	def withhue(self, hue:Number) -> "Color":
		"""
		Return a copy of ``self`` with the hue replaced with ``hue``.
		"""
		(h, l, s, a) = self.hlsa()
		return self.fromhls(hue, l, s, a)

	def withsat(self, sat:Number) -> "Color":
		"""
		Return a copy of ``self`` with the saturation replaced with ``sat``.
		"""
		(h, l, s, a) = self.hlsa()
		return self.fromhls(h, l, sat, a)

	def withlum(self, lum:Number) -> "Color":
		"""
		Return a copy of ``self`` with the luminosity replaced with ``lum``.
		"""
		(h, l, s, a) = self.hlsa()
		return self.fromhls(h, lum, s, a)

	def withluma(self, luma:Number) -> "Color":
		"""
		Return a copy of ``self`` where the luma value has been replace with ``luma``.
		"""
		luma_old = self.luma()
		if luma_old == 0.0 or luma_old == 1.0:
			v = luma*255
			return Color(v, v, v, self[3])
		elif luma > luma_old:
			f = (luma-luma_old)/(1-luma_old)
			return Color(
				_interpolate(self[0], 255, f),
				_interpolate(self[1], 255, f),
				_interpolate(self[2], 255, f),
				self[3],
			)
		elif luma < luma_old:
			f = luma/luma_old
			return Color(
				_interpolate(0, self[0], f),
				_interpolate(0, self[1], f),
				_interpolate(0, self[2], f),
				self[3],
			)
		else:
			return self

	def witha(self, a:int) -> "Color":
		"""
		Return a copy of ``self`` with the alpha value replaced with ``a``.
		"""
		(r, g, b, olda) = self
		return self.__class__(r, g, b, a)

	def abslum(self, f:Number) -> "Color":
		"""
		Return a copy of ``self`` with ``f`` added to the luminocity.
		"""
		(h, l, s, a) = self.hlsa()
		return self.fromhls(h, l+f, s, a)

	def rellum(self, f:Number) -> "Color":
		"""
		Return a copy of ``self`` where the luminocity has been modified:
		If ``f`` if positive the luminocity will be increased, with ``f==1``
		giving a luminocity of 1. If ``f`` is negative, the luminocity will be
		decreased with ``f==-1`` giving a luminocity of 0. ``f==0`` will leave
		the luminocity unchanged.
		"""
		(h, l, s, a) = self.hlsa()
		if f > 0:
			l += (1-l)*f
		elif f < 0:
			l += l*f
		return self.fromhls(h, l, s, a)

	def absluma(self, f:Number) -> "Color":
		"""
		Return a copy of ``self`` where ``f`` has been added to the luma value.
		"""
		return self.withluma(self.luma() + f)

	def relluma(self, f:Number) -> "Color":
		"""
		Return a copy of ``self`` where the luma value has been modified:
		If ``f`` if positive the luma value will be increased, with ``f==1``
		giving a luma value of 1. If ``f`` is negative, the luma value will be
		decreased with ``f==-1`` giving a luma value of 0. ``f==0`` will leave
		the luma value unchanged.
		"""
		luma = self.luma()
		if f > 0:
			luma += (1-luma)*f
		elif f < 0:
			luma += luma*f
		return self.withluma(luma)

	def combine(self, r:Number=None, g:Number=None, b:Number=None, a:Number=None) -> "Color":
		"""
		Return a copy of ``self`` with some of the values replaced by the
		arguments.
		"""
		channels = list(self)
		if r is not None:
			channels[0] = r
		if g is not None:
			channels[1] = g
		if b is not None:
			channels[2] = b
		if a is not None:
			channels[3] = a
		return self.__class__(*channels)

	def invert(self, f:Number=1.0) -> "Color":
		"""
		Return an inverted version of ``self``. ``f`` specifies the amount
		of inversion, with 1 returning a complete inversion, and 0 returning
		the original color. Values between 0 and 1 return an interpolation
		of both extreme values. (And 0.5 always returns medium grey).
		"""
		invf = 1.0 - f
		return self.__class__(
			invf * self[0] + f * (255-self[0]),
			invf * self[1] + f * (255-self[1]),
			invf * self[2] + f * (255-self[2]),
			self[3],
		)

	def __add__(self, other):
		raise NotImplementedError

	def __mul__(self, factor:Number) -> "Color":
		return self.__class__(factor*self[0], factor*self[1], factor*self[2], self[3])

	def __rmul__(self, factor:Number) -> "Color":
		return self.__class__(factor*self[0], factor*self[1], factor*self[2], self[3])

	def __truediv__(self, factor:Number) -> "Color":
		return self.__class__(self[0]/factor, self[1]/factor, self[2]/factor, self[3])

	def __floordiv__(self, factor:Number) -> "Color":
		return self.__class__(self[0]//factor, self[1]//factor, self[2]//factor, self[3])

	def __mod__(self, other:"Color") -> "Color":
		"""
		Blends ``self`` with the background color ``other`` according to the
		`CSS specification`__

		__ https://www.w3.org/TR/2013/WD-compositing-1-20131010/#simplealphacompositing
		"""
		# Scale our values to the range [0, 1]
		rt = self[0]/255.
		gt = self[1]/255.
		bt = self[2]/255.
		at = self[3]/255.

		# Convert to premultiplied alpha
		rt *= at
		gt *= at
		bt *= at

		# Scale other values to the range [0, 1]
		ro = other[0]/255.
		go = other[1]/255.
		bo = other[2]/255.
		ao = other[3]/255.

		# Convert to premultiplied alpha
		ro *= ao
		go *= ao
		bo *= ao

		# Blend colors
		rf = rt + ro * (1 - at)
		gf = gt + go * (1 - at)
		bf = bt + bo * (1 - at)
		af = at + ao * (1 - at)

		# Unmultiply alpha
		if af:
			rf /= af
			gf /= af
			bf /= af

		# Scale back to [0, 255]
		r = int(255*rf)
		g = int(255*gf)
		b = int(255*bf)
		a = int(255*af)

		# create final color
		return self.__class__(r, g, b, a)


###
### CSS color constants (see http://www.w3.org/TR/css3-color/#html4)
###

maroon = Color(0x80, 0x00, 0x00)
red = Color(0xff, 0x00, 0x00)
orange = Color(0xff, 0xa5, 0x00)
yellow = Color(0xff, 0xff, 0x00)
olive = Color(0x80, 0x80, 0x00)
purple = Color(0x80, 0x00, 0x80)
fuchsia = Color(0xff, 0x00, 0xff)
white = Color(0xff, 0xff, 0xff)
lime = Color(0x00, 0xff, 0x00)
green = Color(0x00, 0x80, 0x00)
navy = Color(0x00, 0x00, 0x80)
blue = Color(0x00, 0x00, 0xff)
aqua = Color(0x00, 0xff, 0xff)
teal = Color(0x00, 0x80, 0x80)
black = Color(0x00, 0x00, 0x00)
silver = Color(0xc0, 0xc0, 0xc0)
gray = Color(0x80, 0x80, 0x80)

# aliases
magenta = purple
cyan = aqua

transparent = Color(0, 0, 0, 0)


csscolors = {
	"maroon": maroon,
	"red": red,
	"orange": orange,
	"yellow": yellow,
	"olive": olive,
	"purple": purple,
	"fuchsia": fuchsia,
	"white": white,
	"lime": lime,
	"green": green,
	"navy": navy,
	"blue": blue,
	"aqua": aqua,
	"teal": teal,
	"black": black,
	"silver": silver,
	"gray": gray,
	"magenta": magenta,
	"cyan": cyan,
}


_missing = object()

def css(value:str, default:OptStr=_missing, /) -> "Color":
	"""
	Create a :class:`Color` object from the CSS__ color string ``value`` via
	:meth:`Color.fromcss`.

	If ``value`` is no valid CSS color string and ``default`` is given,
	return ``default`` instead.

		__ http://www.w3.org/TR/css3-color/#colorunits
	"""
	if default is _missing:
		return Color.fromcss(value)
	else:
		try:
			return Color.fromcss(value)
		except ValueError:
			return default


def dist(c1:"Color", c2:"Color", /) -> float:
	"""
	Return the distance between two colors.
	"""

	d0 = c1[0]-c2[0]
	d1 = c1[1]-c2[1]
	d2 = c1[2]-c2[2]
	return d0*d0+d1*d1+d2*d2


def multiply(c1:"Color", c2:"Color", /) -> "Color":
	"""
	Multiplies the colors ``c1`` and ``c2``.
	"""
	return Color(c1[0]*c2[0], c1[1]*c2[1], c1[2]*c2[2], 1.-(1.-c1[3])*(1.-c2[3]))


def screen(c1:"Color", c2:"Color", /) -> "Color":
	"""
	Does a negative multiplication of the colors ``c1`` and ``c2``.
	"""
	return Color(*(1.-(1.-x)*(1.-y) for (x, y) in zip(c1, c2)))


def mix(*args) -> "Color":
	"""
	Calculates a weighted mix of the colors from ``args``. Items in
	``args`` are either colors or weights. The following example mixes
	two parts black with one part white::

		>>> from ll import color
		>>> color.mix(2, color.black, 1, color.white)
		Color(0x55, 0x55, 0x55)
	"""
	channels = [0., 0., 0., 0.]
	weight = 1.
	sumweights = 0.
	for arg in args:
		if isinstance(arg, Color):
			sumweights += weight
			for i in range(3):
				channels[i] += weight*arg[i]
			channels[3] += weight*(255-arg[3])
		elif isinstance(arg, tuple):
			sumweights += arg[1]
			for i in range(3):
				channels[i] += arg[1]*arg[0][i]
			channels[3] += weight*(255-arg[0][3])
		else:
			weight = arg
	if not sumweights:
		raise ValueError("at least one of the arguments must be a color and at least one of the weights must be >0")
	return Color(channels[0]/sumweights, channels[1]/sumweights, channels[2]/sumweights, 255-sumweights*channels[3])
