/*!
 * UL4 JavaScript Library
 * http://www.livinglogic.de/Python/ul4c/
 *
 * Copyright 2011-2012 by LivingLogic AG, Bayreuth/Germany
 * Copyright 2011-2012 by Walter Dörwald
 *
 * All Rights Reserved
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/*jslint vars: true */
var ul4 = {
	version: "17",

	// REs for parsing JSON
	_rvalidchars: /^[\],:{}\s]*$/,
	_rvalidescape: /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,
	_rvalidtokens: /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,
	_rvalidbraces: /(?:^|:|,)(?:\s*\[)+/g,

	// Functions with the ``_op_`` prefix implement UL4 opcodes

	// Addition: num + num, string + string
	_op_add: function(obj1, obj2)
	{
		if (obj1 === null || obj2 === null)
			throw this._fu_type(obj1) + " + " + this._fu_type(obj2) + " not supported";
		return obj1 + obj2;
	},

	// Substraction: num - num
	_op_sub: function(obj1, obj2)
	{
		if (obj1 === null || obj2 === null)
			throw this._fu_type(obj1) + " - " + this._fu_type(obj2) + " not supported";
		return obj1 - obj2;
	},

	// Multiplication: num * num, int * str, str * int, int * list, list * int
	_op_mul: function(obj1, obj2)
	{
		if (obj1 === null || obj2 === null)
			throw this._fu_type(obj1) + " * " + this._fu_type(obj2) + " not supported";
		else if (this._fu_isint(obj1) || this._fu_isbool(obj1))
		{
			if (typeof(obj2) === "string")
			{
				if (obj1 < 0)
					throw "mul() repetition counter must be positive";
				return this._str_repeat(obj2, obj1);
			}
			else if (this._fu_islist(obj2))
			{
				if (obj1 < 0)
					throw "mul() repetition counter must be positive";
				return this._list_repeat(obj2, obj1);
			}
		}
		else if (this._fu_isint(obj2) || this._fu_isbool(obj2))
		{
			if (typeof(obj1) === "string")
			{
				if (obj2 < 0)
					throw "mul() repetition counter must be positive";
				return this._str_repeat(obj1, obj2);
			}
			else if (this._fu_islist(obj1))
			{
				if (obj2 < 0)
					throw "mul() repetition counter must be positive";
				return this._list_repeat(obj1, obj2);
			}
		}
		return obj1 * obj2;
	},

	// Truncating division
	_op_floordiv: function(obj1, obj2)
	{
		if (obj1 === null || obj2 === null)
			throw this._fu_type(obj1) + " // " + this._fu_type(obj2) + " not supported";
		return Math.floor(obj1 / obj2);
	},

	// "Real" division
	_op_truediv: function(obj1, obj2)
	{
		if (obj1 === null || obj2 === null)
			throw this._fu_type(obj1) + " / " + this._fu_type(obj2) + " not supported";
		return obj1 / obj2;
	},

	// Modulo (this is non-trivial, because it follows the Python semantic of ``-5 % 2`` being ``1``)
	_op_mod: function(obj1, obj2)
	{
		var div = Math.floor(obj1 / obj2);
		var mod = obj1 - div * obj2;

		if (mod !== 0 && ((obj2 < 0 && mod > 0) || (obj2 > 0 && mod < 0)))
		{
			mod += obj2;
			--div;
		}
		return obj1 - div * obj2;
	},

	// Negation
	_op_neg: function(obj)
	{
		return -obj;
	},

	// Not
	_op_not: function(obj)
	{
		return !obj;
	},

	// Containment test: string in string, obj in list, key in dict, value in rgb
	_op_contains: function(obj, container)
	{
		if (typeof(obj) === "string" && typeof(container) === "string")
		{
			return container.indexOf(obj) !== -1;
		}
		else if (this._fu_islist(container))
		{
			return container.indexOf(obj) !== -1;
		}
		else if (this._fu_isdict(container))
		{
			for (var key in container)
			{
				if (key === obj)
					return true;
			}
			return false;
		}
		else if (this._fu_iscolor(container))
		{
			return container.r === obj || container.g === obj || container.b === obj || container.a === obj;
		}
		throw "argument of type '" + this._fu_type(container) + "' is not iterable";
	},

	// Inverted containment test
	_op_notcontains: function(obj, container)
	{
		return !ul4._op_contains(obj, container);
	},

	// Comparison operator ==
	_op_eq: function(obj1, obj2)
	{
		return obj1 === obj2;
	},

	// Comparison operator !=
	_op_ne: function(obj1, obj2)
	{
		return obj1 !== obj2;
	},

	// Comparison operator <
	_op_lt: function(obj1, obj2)
	{
		return obj1 < obj2;
	},

	// Comparison operator <=
	_op_le: function(obj1, obj2)
	{
		return obj1 <= obj2;
	},

	// Comparison operator >
	_op_gt: function(obj1, obj2)
	{
		return obj1 > obj2;
	},

	// Comparison operator >=
	_op_ge: function(obj1, obj2)
	{
		return obj1 >= obj2;
	},

	// Item access: dict[key], list[index], string[index], color[index]
	_op_getitem: function(container, key)
	{
		if (typeof(container) === "string" || this._fu_islist(container))
		{
			var orgkey = key;
			if (key < 0)
				key += container.length;
			if (key < 0 || key >= container.length)
				throw "index " + this._fu_repr(orgkey) + " out of range";
			return container[key];
		}
		else if (this._fu_iscolor(container)) // test this before the generic object test
		{
			var orgkey = key;
			if (key < 0)
				key += 4;
			switch (key)
			{
				case 0:
					return container.r;
				case 1:
					return container.g;
				case 2:
					return container.b;
				case 3:
					return container.a;
				default:
					throw "index " + this._fu_repr(orgkey) + " out of range";
			}
		}
		else if (Object.prototype.toString.call(container) === "[object Object]")
		{
			var result = container[key];
			if (typeof(result) === "undefined")
				throw "key " + this._fu_repr(key) + " not found";
			return result;
		}
		throw "getitem() needs a sequence or dict";
	},

	// List/String slicing: string[start:stop], list[start:stop]
	_op_getslice: function(container, start, stop)
	{
		if (typeof(start) === "undefined" || start === null)
			start = 0;
		if (typeof(stop) === "undefined" || stop === null)
			stop = container.length;
		return container.slice(start, stop);
	},

	// Functions with the ``_fu_`` prefix implement UL4 functions

	// Check if ``obj`` is ``None``
	_fu_isnone: function(obj)
	{
		ul4._checkfuncargs("isnone", arguments, 1);

		return obj === null;
	},

	// Check if ``obj`` is a boolean
	_fu_isbool: function(obj)
	{
		ul4._checkfuncargs("isbool", arguments, 1);

		return typeof(obj) == "boolean";
	},

	// Check if ``obj`` is a int
	_fu_isint: function(obj)
	{
		ul4._checkfuncargs("isint", arguments, 1);

		return (typeof(obj) == "number") && Math.round(obj) == obj;
	},

	// Check if ``obj`` is a float
	_fu_isfloat: function(obj)
	{
		ul4._checkfuncargs("isfloat", arguments, 1);

		return (typeof(obj) == "number") && Math.round(obj) != obj;
	},

	// Check if ``obj`` is a string
	_fu_isstr: function(obj)
	{
		ul4._checkfuncargs("isstr", arguments, 1);

		return typeof(obj) == "string";
	},

	// Check if ``obj`` is a date
	_fu_isdate: function(obj)
	{
		ul4._checkfuncargs("isdate", arguments, 1);

		return Object.prototype.toString.call(obj) == "[object Date]";
	},

	// Check if ``obj`` is a color
	_fu_iscolor: function(obj)
	{
		ul4._checkfuncargs("iscolor", arguments, 1);

		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__iscolor__;
	},

	// Check if ``obj`` is a template
	_fu_istemplate: function(obj)
	{
		ul4._checkfuncargs("istemplate", arguments, 1);

		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__istemplate__;
	},

	// Check if ``obj`` is a list
	_fu_islist: function(obj)
	{
		ul4._checkfuncargs("islist", arguments, 1);

		return Object.prototype.toString.call(obj) == "[object Array]";
	},

	// Check if ``obj`` is a dict
	_fu_isdict: function(obj)
	{
		ul4._checkfuncargs("isdict", arguments, 1);

		return Object.prototype.toString.call(obj) == "[object Object]" && !obj.__iscolor__ && !obj.__istemplate__;
	},

	// Convert ``obj`` to bool, according to its "truth value"
	_fu_bool: function(obj)
	{
		ul4._checkfuncargs("bool", arguments, 1);

		if (obj === null || obj === false || obj === 0 || obj === "")
			return false;
		else
		{
			if (this._fu_islist(obj))
				return obj.length !== 0;
			else if (this._fu_isdict(obj))
			{
				for (var key in obj)
					return true;
				return false;
			}
			return true;
		}
	},

	// Create a color object from the red, green, blue and alpha values ``r``, ``g``, ``b`` and ``b``
	_fu_rgb: function(r, g, b, a)
	{
		ul4._checkfuncargs("rgb", arguments, 3, 4);

		return this.Color.create(255*r, 255*g, 255*b, typeof(a) == "undefined" ? 0xff : (255*a));
	},

	// Return the type of ``obj`` as a string
	_fu_type: function(obj)
	{
		ul4._checkfuncargs("type", arguments, 1);

		if (obj === null)
			return "none";
		else if (obj === false || obj === true)
			return "bool";
		else if (typeof(obj) === "string")
			return "str";
		else if (typeof(obj) === "number")
			return Math.round(obj) == obj ? "int" : "float";
		else if (this._fu_islist(obj))
			return "list";
		else if (obj instanceof Date)
			return "date";
		else if (this._fu_iscolor(obj))
			return "color";
		else if (this._fu_isdict(obj))
			return "dict";
		else if (this._fu_istemplate(obj))
			return "template";
		return null;
	},

	// Convert ``obj`` to a string
	_fu_str: function(obj)
	{
		ul4._checkfuncargs("str", arguments, 0, 1);

		if (typeof(obj) === "undefined")
			return "";

		if (typeof(obj) === "string")
			return obj;
		else if (obj === null)
			return "";
		else if (obj === false)
			return "False";
		else if (obj === true)
			return "True";
		else if (typeof(obj) === "number")
		{
			return obj.toString();
		}
		else if (this._fu_islist(obj))
		{
			var v = [];
			v.push("[");
			for (var i in obj)
			{
				if (i != 0)
					v.push(", ");
				v.push(this._fu_repr(obj[i]));
			}
			v.push("]");
			return v.join("");
		}
		else if (obj instanceof Date)
		{
			return this._date_str(obj);
		}
		else if (this._fu_iscolor(obj))
		{
			return this._color_str(obj);
		}
		else if (this._fu_isdict(obj))
		{
			var v = [];
			v.push("{");
			var i = 0;
			for (var key in obj)
			{
				if (i)
					v.push(", ");
				v.push(this._fu_repr(key));
				v.push(": ");
				v.push(this._fu_repr(obj[key]));
				++i;
			}
			v.push("}");
			return v.join("");
		}
		return "?";
	},

	// Convert ``obj`` to an integer (if ``base`` is given ``obj`` must be a string and ``base`` is the base for the conversion (default is 10))
	_fu_int: function(obj, base)
	{
		ul4._checkfuncargs("int", arguments, 0, 2);

		if (typeof(obj) === "undefined")
			return 0;
		var result;
		if (typeof(base) !== "undefined")
		{
			if (typeof(obj) !== "string" || !this._fu_isint(base))
				throw "int() requires a string and an integer";
			result = parseInt(obj, base);
			if (result.toString() == "NaN")
				throw "invalid literal for int()";
			return result;
		}
		else
		{
			if (typeof(obj) == "string")
			{
				result = parseInt(obj);
				if (result.toString() == "NaN")
					throw "invalid literal for int()";
				return result;
			}
			else if (typeof(obj) == "number")
				return Math.floor(obj);
			else if (obj === true)
				return 1;
			else if (obj === false)
				return 0;
			throw "int() argument must be a string or a number";
		}
	},

	// Convert ``obj`` to a float
	_fu_float: function(obj)
	{
		ul4._checkfuncargs("float", arguments, 0, 1);

		if (typeof(obj) === "undefined")
			return 0.0;
		if (typeof(obj) === "string")
			return parseFloat(obj);
		else if (typeof(obj) === "number")
			return obj;
		else if (obj === true)
			return 1.0;
		else if (obj === false)
			return 0.0;
		throw "float() argument must be a string or a number";
	},

	// Convert ``obj`` to a list
	_fu_list: function(obj)
	{
		ul4._checkfuncargs("list", arguments, 0, 1);

		if (typeof(obj) === "undefined")
			return [];
		if (typeof(obj) == "string" || this._fu_islist(obj))
		{
			var result = [];
			for (var key in obj)
				result.push(obj[key]);
			return result;
		}
		else if (this._fu_iscolor(obj))
		{
			return [obj.r, obj.g, obj.b, obj.a];
		}
		else if (this._fu_isdict(obj))
		{
			var result = [];
			for (var key in obj)
				result.push(key);
			return result;
		}
		else if (obj.__iter__)
		{
			var result = [];
			while (true)
			{
				var item = obj();
				if (item === null)
					break;
				result.push(item[0]);
			}
			return result;
		}
		throw "list() requires an iterable";
	},

	// Return the length of ``obj``
	_fu_len: function(obj)
	{
		ul4._checkfuncargs("len", arguments, 1);

		if (typeof(obj) == "string" || this._fu_islist(obj))
			return obj.length;
		else if (this._fu_isdict(obj))
		{
			var i = 0;
			for (var key in obj)
				++i;
			return i;
		}
		throw "object of type '" + this._fu_type(obj) + "' has no len()";
	},

	// Return a string representation of ``obj``: This should be an object supported by UL4
	_fu_repr: function(obj)
	{
		ul4._checkfuncargs("repr", arguments, 1);

		if (obj === null)
			return "None";
		else if (obj === false)
			return "False";
		else if (obj === true)
			return "True";
		else if (typeof(obj) === "string")
			return this._str_repr(obj);
		else if (typeof(obj) === "number")
		{
			return "" + obj;
		}
		else if (obj instanceof Date)
		{
			return this._date_repr(obj);
		}
		else if (this._fu_iscolor(obj))
		{
			return this._color_repr(obj);
		}
		else if (this._fu_islist(obj))
		{
			var v = [];
			v.push("[");
			for (var i = 0; i < obj.length; ++i)
			{
				if (i !== 0)
					v.push(", ");
				v.push(this._fu_repr(obj[i]));
			}
			v.push("]");
			return v.join("");
		}
		else if (this._fu_isdict(obj))
		{
			var v = [];
			v.push("{");
			var i = 0;
			for (var key in obj)
			{
				if (i)
					v.push(", ");
				v.push(this._fu_repr(key));
				v.push(": ");
				v.push(this._fu_repr(obj[key]));
				++i;
			}
			v.push("}");
			return v.join("");
		}
		return "?";
	},

	// Format ``obj`` using the format string ``format``
	_fu_format: function(obj, format)
	{
		ul4._checkfuncargs("format", arguments, 2);

		var weekdays1 = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
		var weekdays2 = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
		var months1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
		var months2 = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December'];
		var firstday;

		if (this._fu_isdate(obj))
		{
			var result = [];
			var inspec = false;
			for (var i in format)
			{
				var c = format[i];
				if (inspec)
				{
					switch (c)
					{
						case "a":
							c = weekdays1[obj.getDay()];
							break;
						case "A":
							c = weekdays2[obj.getDay()];
							break;
						case "b":
							c = months1[obj.getMonth()];
							break;
						case "B":
							c = months2[obj.getMonth()];
							break;
						case "c":
							c = weekdays1[obj.getDay()] + " " + months1[obj.getMonth()] + " " + this._lpad(obj.getDate(), " ", 2) + " " + this._lpad(obj.getHours(), "0", 2) + ":" + this._lpad(obj.getMinutes(), "0", 2) + ":" + this._lpad(obj.getSeconds(), "0", 2) + " " + obj.getFullYear();
							break;
						case "d":
							c = this._lpad(obj.getDate(), "0", 2);
							break;
						case "f":
							c = this._lpad(obj.getMilliseconds(), "0", 3) + "000";
							break;
						case "H":
							c = this._lpad(obj.getHours(), "0", 2);
							break;
						case "I":
							c = this._lpad(((obj.getHours()-1) % 12)+1, "0", 2);
							break;
						case "j":
							c = this._lpad(this._me_yearday(obj), "0", 3);
							break;
						case "m":
							c = this._lpad(obj.getMonth()+1, "0", 2);
							break;
						case "M":
							c = this._lpad(obj.getMinutes(), "0", 2);
							break;
						case "p":
							c = obj.getHours() < 12 ? "AM" : "PM";
							break;
						case "S":
							c = this._lpad(obj.getSeconds(), "0", 2);
							break;
						case "U":
							firstday = (new Date(obj.getFullYear(), 0, 1).getDay());
							c = this._lpad(Math.floor((this._me_yearday(obj) + firstday - 1) / 7), "0", 2);
							break;
						case "w":
							c = obj.getDay();
							break;
						case "W":
							firstday = (new Date(obj.getFullYear(), 0, 1).getDay());
							firstday = firstday ? firstday-1 : 6;
							c = this._lpad(Math.floor((this._me_yearday(obj) + firstday - 1) / 7), "0", 2);
							break;
						case "x":
							c = this._lpad(obj.getMonth() + 1, "0", 2) + "/" + this._lpad(obj.getDate(), "0", 2) + "/" + this._lpad(obj.getFullYear() % 100, "0", 2);
							break;
						case "X":
							c = this._lpad(obj.getHours(), "0", 2) + ":" + this._lpad(obj.getMinutes(), "0", 2) + ":" + this._lpad(obj.getSeconds(), "0", 2);
							break;
						case "y":
							c = (obj.getFullYear() % 100).toString();
							break;
						case "Y":
							c = obj.getFullYear().toString();
							break;
						case "z":
							// UTC offset in the form +HHMM or -HHMM
							c = "";
							break;
						case "Z":
							// Time zone name
							c = "";
							break;
					}
					result.push(c);
					inspec = false;
				}
				else
				{
					if (c == "%")
						inspec = true;
					else
						result.push(c);
				}
			}
			return result.join("");
		}
	},

	// Convert ``obj`` to a string and escape the characters ``&``, ``<``, ``>``, ``'`` and ``"`` with their XML character/entity reference
	_fu_xmlescape: function(obj)
	{
		ul4._checkfuncargs("xmlescape", arguments, 1);

		obj = this._fu_str(obj);
		obj = obj.replace(/&/g, "&amp;");
		obj = obj.replace(/</g, "&lt;");
		obj = obj.replace(/>/g, "&gt;");
		obj = obj.replace(/'/g, "&#39;");
		obj = obj.replace(/"/g, "&quot;");
		return obj;
	},

	// Convert ``obj`` to a string suitable for output into a CSV file
	_fu_csv: function(obj)
	{
		ul4._checkfuncargs("csv", arguments, 1);

		if (obj === null)
			return "";
		else if (typeof(obj) !== "string")
			obj = this._fu_repr(obj);
		if (obj.indexOf(",") !== -1 || obj.indexOf('"') !== -1 || obj.indexOf("\n") !== -1)
			obj = '"' + obj.replace(/"/g, '""') + '"';
		return obj;
	},

	// Return a string containing one charcter with the codepoint ``obj``
	_fu_chr: function(obj)
	{
		ul4._checkfuncargs("chr", arguments, 1);

		if (typeof(obj) != "number")
			throw "chr() requires an int";
		return String.fromCharCode(obj);
	},

	// Return the codepoint for the one and only character in the string ``obj``
	_fu_ord: function(obj)
	{
		ul4._checkfuncargs("ord", arguments, 1);

		if (typeof(obj) != "string" || obj.length != 1)
			throw "ord() requires a string of length 1";
		return obj.charCodeAt(0);
	},

	// Convert an integer to a hexadecimal string
	_fu_hex: function(obj)
	{
		ul4._checkfuncargs("hex", arguments, 1);

		if (typeof(obj) != "number")
			throw "hex() requires an int";
		if (obj < 0)
			return "-0x" + obj.toString(16).substr(1);
		else
			return "0x" + obj.toString(16);
	},

	// Convert an integer to a octal string
	_fu_oct: function(obj)
	{
		ul4._checkfuncargs("oct", arguments, 1);

		if (typeof(obj) != "number")
			throw "oct() requires an int";
		if (obj < 0)
			return "-0o" + obj.toString(8).substr(1);
		else
			return "0o" + obj.toString(8);
	},

	// Convert an integer to a binary string
	_fu_bin: function(obj)
	{
		ul4._checkfuncargs("bin", arguments, 1);

		if (typeof(obj) != "number")
			throw "bin() requires an int";
		if (obj < 0)
			return "-0b" + obj.toString(2).substr(1);
		else
			return "0b" + obj.toString(2);
	},

	// Return a sorted version of ``obj``
	_fu_sorted: function(obj)
	{
		ul4._checkfuncargs("sorted", arguments, 1);

		var result = this._fu_list(obj);
		result.sort();
		return result;
	},

	// Return a iterable object iterating from ``start`` upto (but not including) ``stop`` with a step size of ``step``
	_fu_range: function(start, stop, step)
	{
		ul4._checkfuncargs("range", arguments, 1, 3);

		if (typeof(step) == "undefined")
		{
			step = 1;
			if (typeof(stop) == "undefined")
			{
				stop = start;
				start = 0;
			}
		}
		var lower, higher;
		if (step === 0)
			throw "range() requires a step argument != 0";
		else if (step > 0)
		{
			lower = start;
			heigher = stop;
		}
		else
		{
			lower = stop;
			heigher = start;
		}
		var length = (lower < heigher) ? Math.floor((heigher - lower - 1)/Math.abs(step)) + 1 : 0;

		var i = 0;
		var result = function()
		{
			if (i >= length)
				return null;
			return [start + (i++) * step];
		};
		result.__iter__ = true;
		return result;
	},

	// Encodes ``obj`` in the Javascript Object Notation (see http://json.org/; with support for dates, colors and templates)
	_fu_asjson: function(obj)
	{
		ul4._checkfuncargs("asjson", arguments, 1);

		if (obj === null)
			return "null";
		else if (obj === false)
			return "false";
		else if (obj === true)
			return "true";
		else if (typeof(obj) === "string")
			return this._str_json(obj);
		else if (typeof(obj) === "number")
		{
			return "" + obj;
		}
		else if (this._fu_islist(obj))
		{
			var v = [];
			v.push("[");
			for (var i = 0; i < obj.length; ++i)
			{
				if (i != 0)
					v.push(", ");
				v.push(this._fu_asjson(obj[i]));
			}
			v.push("]");
			return v.join("");
		}
		else if (this._fu_isdict(obj))
		{
			var v = [];
			v.push("{");
			var i = 0;
			for (var key in obj)
			{
				if (i)
					v.push(", ");
				v.push(this._fu_asjson(key));
				v.push(": ");
				v.push(this._fu_asjson(obj[key]));
				++i;
			}
			v.push("}");
			return v.join("");
		}
		else if (this._fu_isdate(obj))
		{
			return "new Date(" + obj.getFullYear() + ", " + obj.getMonth() + ", " + obj.getDate() + ", " + obj.getHours() + ", " + obj.getMinutes() + ", " + obj.getSeconds() + ", " + obj.getMilliseconds() + ")";
		}
		else if (this._fu_iscolor(obj))
		{
			return "ul4.Color.create(" + obj.r + ", " + obj.g + ", " + obj.b + ", " + obj.a + ")";
		}
		else if (this._fu_istemplate(obj))
		{
			return "ul4.Template.loads(" + ul4._fu_repr(obj.dumps()) + ")";
		}
		throw "json() requires a serializable object";
	},

	// Decodes the string ``obj`` from the Javascript Object Notation (see http://json.org/) and returns the resulting object
	_fu_fromjson: function(obj)
	{
		ul4._checkfuncargs("fromjson", arguments, 1);

		// The following is from jQuery's parseJSON function
		obj = ul4._me_strip(obj);
		if (typeof(window) !== "undefined" && window.JSON && window.JSON.parse)
			return window.JSON.parse(obj);
		if (ul4._rvalidchars.test(obj.replace(ul4._rvalidescape, "@").replace(ul4._rvalidtokens, "]").replace(ul4._rvalidbraces, "")))
			return (new Function("return " + obj))();
		throw "invalid JSON";
	},

	// Encodes ``obj`` in the UL4 Object Notation format
	_fu_asul4on: function(obj)
	{
		ul4._checkfuncargs("asul4on", arguments, 1);

		return ul4on.dumps(obj);
	},

	// Decodes the string ``obj`` from the UL4 Object Notation format and returns the resulting decoded object
	_fu_fromul4on: function(obj)
	{
		ul4._checkfuncargs("fromul4on", arguments, 1);

		return ul4on.loads(obj);
	},

	// ``%`` escape unsafe characters in the string ``obj``
	_fu_urlquote: function(obj)
	{
		ul4._checkfuncargs("urlquote", arguments, 1);
		return encodeURIComponent(obj);
	},

	// The inverse function of ``urlquote``
	_fu_urlunquote: function(obj)
	{
		ul4._checkfuncargs("urlunquote", arguments, 1);
		return decodeURIComponent(obj);
	},

	// Return a reverse iterator over ``obj``
	_fu_reversed: function(obj)
	{
		ul4._checkfuncargs("reversed", arguments, 1);

		if (typeof(obj) != "string" && !this._fu_islist(obj)) // We don't have to materialize strings or lists
			obj = this._fu_list(obj);
		var i = obj.length-1;
		var result = function()
		{
			return i >= 0 ? [obj[i--]] : null;
		};
		result.__iter__ = true;
		return result;
	},

	// Returns a random number in the interval ``[0;1[``
	_fu_random: function()
	{
		ul4._checkfuncargs("random", arguments, 0);

		return Math.random();
	},

	// Return a randomly select item from ``range(start, stop, step)``
	_fu_randrange: function(start, stop, step)
	{
		ul4._checkfuncargs("randrange", arguments, 1, 3);

		if (typeof(step) === "undefined")
		{
			step = 1;
			if (typeof(stop) === "undefined")
			{
				stop = start;
				start = 0;
			}
		}
		var width = stop-start;

		var value = Math.random();

		var n;
		if (step > 0)
			n = Math.floor((width + step - 1) / step);
		else if (step < 0)
			n = Math.floor((width + step + 1) / step);
		else
			throw "randrange() requires a step argument != 0";
		return start + step*Math.floor(value * n);
	},

	// Return a random item/char from the list/string ``obj``
	_fu_randchoice: function(obj)
	{
		ul4._checkfuncargs("randchoice", arguments, 1);

		var iscolor = this._fu_iscolor(obj);
		if (typeof(obj) !== "string" && !this._fu_islist(obj) && !iscolor)
			throw "randchoice() requires a string or list";
		if (iscolor)
			obj = this._fu_list(obj);
		return obj[Math.floor(Math.random() * obj.length)];
	},

	// Return an iterator over ``[index, item]`` lists from the iterable object ``obj``. ``index`` starts at ``start`` (defaulting to 0)
	_fu_enumerate: function(obj, start)
	{
		ul4._checkfuncargs("enumerate", arguments, 1, 2);
		if (typeof(start) === "undefined")
			start = 0;

		var iter = this._iter(obj);
		var i = start;
		var result = function()
		{
			var inner = iter();
			return inner !== null ? [[i++, inner[0]]] : null;
		};
		result.__iter__ = true;
		return result;
	},

	// Return an iterator over ``[isfirst, item]`` lists from the iterable object ``obj`` (``isfirst`` is true for the first item, false otherwise)
	_fu_isfirst: function(obj)
	{
		ul4._checkfuncargs("isfirst", arguments, 1);

		var iter = this._iter(obj);
		var isfirst = true;
		var result = function()
		{
			var inner = iter();
			var result = inner !== null ? [[isfirst, inner[0]]] : null;
			isfirst = false;
			return result;
		};
		result.__iter__ = true;
		return result;
	},

	// Return an iterator over ``[islast, item]`` lists from the iterable object ``obj`` (``islast`` is true for the last item, false otherwise)
	_fu_islast: function(obj)
	{
		ul4._checkfuncargs("islast", arguments, 1);

		var iter = this._iter(obj);
		var lastitem = iter();
		var result = function()
		{
			if (lastitem === null)
				return null;
			var inner = iter();
			var result = [[inner === null, lastitem[0]]];
			lastitem = inner;
			return result;
		};
		result.__iter__ = true;
		return result;
	},

	// Return an iterator over ``[isfirst, islast, item]`` lists from the iterable object ``obj`` (``isfirst`` is true for the first item, ``islast`` is true for the last item. Both are false otherwise)
	_fu_isfirstlast: function(obj)
	{
		ul4._checkfuncargs("isfirstlast", arguments, 1);

		var iter = this._iter(obj);
		var isfirst = true;
		var lastitem = iter();
		var result = function()
		{
			if (lastitem === null)
				return null;
			var inner = iter();
			var result = [[isfirst, inner === null, lastitem[0]]];
			lastitem = inner;
			isfirst = false;
			return result;
		};
		result.__iter__ = true;
		return result;
	},

	// Return an iterator over ``[index, isfirst, islast, item]`` lists from the iterable object ``obj`` (``isfirst`` is true for the first item, ``islast`` is true for the last item. Both are false otherwise)
	_fu_enumfl: function(obj, start)
	{
		ul4._checkfuncargs("enumfl", arguments, 1, 2);
		if (typeof(start) === "undefined")
			start = 0;

		var iter = this._iter(obj);
		var i = start;
		var isfirst = true;
		var lastitem = iter();
		var result = function()
		{
			if (lastitem === null)
				return null;
			var inner = iter();
			var result = [[i++, isfirst, inner === null, lastitem[0]]];
			lastitem = inner;
			isfirst = false;
			return result;
		};
		result.__iter__ = true;
		return result;
	},

	// Return an iterator over lists, where the i'th list consists of all i'th items from the arguments (terminating when the shortest argument ends)
	_fu_zip: function()
	{
		var result;
		if (arguments.length)
		{
			var iters = [];
			for (var i = 0; i < arguments.length; ++i)
				iters.push(this._iter(arguments[i]));

			result = function()
			{
				var items = [];
				for (var i in iters)
				{
					var item = iters[i]();
					if (item === null)
						return null;
					items.push(item[0]);
				}
				return [items];
			};
		}
		else
		{
			result = function()
			{
				return null;
			}
		}
		result.__iter__ = true;

		return result;
	},

	// Return the absolute value for the number ``obj``
	_fu_abs: function(obj)
	{
		ul4._checkfuncargs("abs", arguments, 1);

		return Math.abs(obj);
	},

	// Return a ``Date`` object for the current time
	_fu_now: function()
	{
		ul4._checkfuncargs("now", arguments, 0);

		return new Date();
	},

	// Return a ``Date`` object for the current time in UTC
	_fu_utcnow: function()
	{
		ul4._checkfuncargs("utcnow", arguments, 0);

		var now = new Date();
		// FIXME: The timezone is wrong for the new ``Date`` object.
		return new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
	},

	// Return a ``Color`` object from the hue, luminescence, saturation and alpha values ``h``, ``l``, ``s`` and ``a`` (i.e. using the HLS color model)
	_fu_hls: function(h, l, s, a)
	{
		ul4._checkfuncargs("hls", arguments, 3, 4);

		if (typeof(a) === "undefined")
			a = 1;

		var _v = function(m1, m2, hue)
		{
			hue = hue % 1.0;
			if (hue < 1/6)
				return m1 + (m2-m1)*hue*6.0;
			else if (hue < 0.5)
				return m2;
			else if (hue < 2/3)
				return m1 + (m2-m1)*(2/3-hue)*6.0;
			return m1;
		};

		var m1, m2;
		if (typeof(a) === "undefined")
			a = 1;
		if (s === 0.0)
			return this._fu_rgb(l, l, l, a);
		if (l <= 0.5)
			m2 = l * (1.0+s);
		else
			m2 = l+s-(l*s);
		m1 = 2.0*l - m2;
		return this._fu_rgb(_v(m1, m2, h+1/3), _v(m1, m2, h), _v(m1, m2, h-1/3), a);
	},

	// Return a ``Color`` object from the hue, saturation, value and alpha values ``h``, ``s``, ``v`` and ``a`` (i.e. using the HSV color model)
	_fu_hsv: function(h, s, v, a)
	{
		ul4._checkfuncargs("hsv", arguments, 3, 4);
		if (typeof(a) === "undefined")
			a = 1;

		if (s === 0.0)
			return this._fu_rgb(v, v, v, a);
		var i = Math.floor(h*6.0);
		var f = (h*6.0) - i;
		var p = v*(1.0 - s);
		var q = v*(1.0 - s*f);
		var t = v*(1.0 - s*(1.0-f));
		switch (i%6)
		{
			case 0:
				return this._fu_rgb(v, t, p, a);
			case 1:
				return this._fu_rgb(q, v, p, a);
			case 2:
				return this._fu_rgb(p, v, t, a);
			case 3:
				return this._fu_rgb(p, q, v, a);
			case 4:
				return this._fu_rgb(t, p, v, a);
			case 5:
				return this._fu_rgb(v, p, q, a);
		}
	},

	_fu_get: function(vars, varname, defaultvalue)
	{
		if (arguments.length < 2 || arguments.length > 3)
			throw "function get() requires 1-2 arguments, " + (arguments.length-1) + " given";
		var result = vars[varname];
		if (typeof(result) === "undefined")
			result = defaultvalue;
		if (typeof(result) === "undefined")
			result = null;
		return result;
	},

	_fu_vars: function(vars)
	{
		if (arguments.length > 1)
			throw "function vars() requires 0 arguments, " + (arguments.length-1) + " given";
		return vars;
	},

	// Functions with the ``_me_`` prefix implement UL4 methods
	_me_replace: function(string, searchstring, replacestring, count)
	{
		ul4._checkmethargs("replace", arguments.length, 2, 3);
		if (typeof(count) === "undefined")
			count = string.length;

		var result = [];
		while (string.length)
		{
			var pos = string.indexOf(searchstring);
			if (pos === -1 || !count--)
			{
				result.push(string);
				break;
			}
			result.push(string.substr(0, pos));
			result.push(replacestring);
			string = string.substr(pos + searchstring.length);
		}
		return result.join("");
	},

	_me_strip: function(string, stripchars)
	{
		ul4._checkmethargs("strip", arguments.length, 1);
		if (typeof(string) !== "string")
			throw "strip() requires a string";
		if (typeof(stripchars) === "undefined")
			stripchars = " \r\n\t";
		else if (typeof(stripchars) !== "string")
			throw "strip() requires two strings";

		while (string && stripchars.indexOf(string[0]) >= 0)
			string = string.substr(1);
		while (string && stripchars.indexOf(string[string.length-1]) >= 0)
			string = string.substr(0, string.length-1);
		return string;
	},

	_me_lstrip: function(string, stripchars)
	{
		ul4._checkmethargs("lstrip", arguments.length, 1);
		if (typeof(string) !== "string")
			throw "lstrip() requires a string";
		if (typeof(stripchars) === "undefined")
			stripchars = " \r\n\t";
		else if (typeof(stripchars) !== "string")
			throw "lstrip() requires two strings";

		while (string && stripchars.indexOf(string[0]) >= 0)
			string = string.substr(1);
		return string;
	},

	_me_rstrip: function(string, stripchars)
	{
		ul4._checkmethargs("rstrip", arguments.length, 1);
		if (typeof(string) !== "string")
			throw "rstrip() requires a string";
		if (typeof(stripchars) === "undefined")
			stripchars = " \r\n\t";
		else if (typeof(stripchars) !== "string")
			throw "rstrip() requires two strings";

		while (string && stripchars.indexOf(string[string.length-1]) >= 0)
			string = string.substr(0, string.length-1);
		return string;
	},

	_me_split: function(string, sep, count)
	{
		ul4._checkmethargs("split", arguments.length, 0, 2);
		if (typeof(string) !== "string")
			throw "split() requires a string";
		if (typeof(sep) === "undefined")
			sep = null;
		else if (sep !== null && typeof(sep) !== "string")
			throw "split() requires a string";

		if (!count)
		{
			var result = string.split(sep !== null ? sep : /[ \n\r\t]+/);
			if (sep === null)
			{
				if (result.length && !result[0].length)
					result.splice(0, 1);
				if (result.length && !result[result.length-1].length)
					result.splice(-1);
			}
			return result;
		}
		else
		{
			if (sep !== null)
			{
				var result = [];
				while (string.length)
				{
					var pos = string.indexOf(sep);
					if (pos === -1 || !count--)
					{
						result.push(string);
						break;
					}
					result.push(string.substr(0, pos));
					string = string.substr(pos + sep.length);
				}
				return result;
			}
			else
			{
				var result = [];
				while (string.length)
				{
					string = this._me_lstrip(string);
					var part;
					if (!count--)
					 	part = string; // Take the rest of the string
					else
						part = string.split(/[ \n\r\t]+/, 1)[0];
					if (part.length)
						result.push(part);
					string = string.substr(part.length);
				}
				return result;
			}
		}
	},

	_me_rsplit: function(string, sep, count)
	{
		ul4._checkmethargs("rsplit", arguments.length, 0, 2);
		if (typeof(string) !== "string")
			throw "rsplit() requires a string as first argument";
		if (typeof(sep) === "undefined")
			sep = null;
		else if (sep !== null && typeof(sep) !== "string")
			throw "rsplit() requires a string as second argument";

		if (!count)
		{
			var result = string.split(sep !== null ? sep : /[ \n\r\t]+/);
			if (sep === null)
			{
				if (result.length && !result[0].length)
					result.splice(0, 1);
				if (result.length && !result[result.length-1].length)
					result.splice(-1);
			}
			return result;
		}
		else
		{
			if (sep !== null)
			{
				var result = [];
				while (string.length)
				{
					var pos = string.lastIndexOf(sep);
					if (pos === -1 || !count--)
					{
						result.unshift(string);
						break;
					}
					result.unshift(string.substr(pos+sep.length));
					string = string.substr(0, pos);
				}
				return result;
			}
			else
			{
				var result = [];
				while (string.length)
				{
					string = this._me_rstrip(string);
					var part;
					if (!count--)
					 	part = string; // Take the rest of the string
					else
					{
						part = string.split(/[ \n\r\t]+/);
						part = part[part.length-1];
					}
					if (part.length)
						result.unshift(part);
					string = string.substr(0, string.length-part.length);
				}
				return result;
			}
		}
	},

	_me_find: function(string, searchstring, start, stop)
	{
		ul4._checkmethargs("find", arguments.length, 1, 3);
		if (typeof(start) === "undefined" || start === null)
			start = 0;
		if (typeof(stop) === "undefined" || stop === null)
			stop = string.length;

		if (start !== 0 || stop !== string.length)
			string = string.substring(start, stop);
		var result = string.indexOf(searchstring);
		if (result !== -1)
			result += start;
		return result;
	},

	_me_rfind: function(string, searchstring, start, stop)
	{
		ul4._checkmethargs("rfind", arguments.length, 1, 3);
		if (typeof(start) === "undefined" || start === null)
			start = 0;
		if (typeof(stop) === "undefined" || stop === null)
			stop = string.length;

		if (start !== 0 || stop !== string.length)
			string = string.substring(start, stop);
		var result = string.lastIndexOf(searchstring);
		if (result !== -1)
			result += start;
		return result;
	},

	_me_lower: function(obj)
	{
		ul4._checkmethargs("lower", arguments.length, 0);
		if (typeof(obj) != "string")
			throw "lower() requires a string";

		return obj.toLowerCase();
	},

	_me_upper: function(obj)
	{
		ul4._checkmethargs("upper", arguments.length, 0);
		if (typeof(obj) != "string")
			throw "upper() requires a string";

		return obj.toUpperCase();
	},

	_me_capitalize: function(obj)
	{
		ul4._checkmethargs("capitalize", arguments.length, 0);
		if (typeof(obj) != "string")
			throw "capitalize() requires a string";

		if (obj.length)
			obj = obj[0].toUpperCase() + obj.slice(1).toLowerCase();
		return obj;
	},

	_me_get: function(container, key, defaultvalue)
	{
		ul4._checkmethargs("get", arguments.length, 1, 2);
		if (!this._fu_isdict(container))
			throw "get() requires a dict";

		var result = container[key];
		if (typeof(result) === "undefined")
		{
			if (typeof(defaultvalue) === "undefined")
				return null;
			return defaultvalue;
		}
		return result;
	},

	_me_items: function(obj)
	{
		ul4._checkmethargs("items", arguments.length, 0);
		if (!this._fu_isdict(obj))
			throw "items() requires a dict";

		var result = [];
		for (var key in obj)
			result.push([key, obj[key]]);
		return result;
	},

	_me_join: function(sep, container)
	{
		ul4._checkmethargs("join", arguments.length, 1);
		if (typeof(sep) !== "string")
			throw "join() requires a string";

		if (!this._fu_islist(container))
			container = this._fu_list(container);
		return container.join(sep);
	},

	_me_startswith: function(string, prefix)
	{
		ul4._checkmethargs("startswith", arguments.length, 1);
		if (typeof(string) !== "string" || typeof(prefix) !== "string")
			throw "startswith() requires two strings";

		return string.substr(0, prefix.length) === prefix;
	},

	_me_endswith: function(string, suffix)
	{
		ul4._checkmethargs("endswith", arguments.length, 1);
		if (typeof(string) !== "string" || typeof(suffix) !== "string")
			throw "endswith() requires two strings";

		return string.substr(string.length-suffix.length) === suffix;
	},

	_me_isoformat: function(obj)
	{
		ul4._checkmethargs("isoformat", arguments.length, 0);
		if (!this._fu_isdate(obj))
			throw "isoformat() requires a date";

		var result = obj.getFullYear() + "-" + this._lpad((obj.getMonth()+1).toString(), "0", 2) + "-" + this._lpad(obj.getDate().toString(), "0", 2);
		var hour = obj.getHours();
		var minute = obj.getMinutes();
		var second = obj.getSeconds();
		var ms = obj.getMilliseconds();
		if (hour || minute || second || ms)
		{
			result += "T" + this._lpad(hour.toString(), "0", 2) + ":" + this._lpad(minute.toString(), "0", 2) + ":" + this._lpad(second.toString(), "0", 2);
			if (ms)
				result += "." + this._lpad(ms.toString(), "0", 3) + "000";
		}
		return result;
	},

	_me_mimeformat: function(obj)
	{
		ul4._checkmethargs("mimeformat", arguments.length, 0);
		if (!this._fu_isdate(obj))
			throw "mimeformat() requires a date";

		var weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
		var monthname = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

		return weekdayname[this._me_weekday(obj)] + ", " + this._lpad(obj.getDate(), "0", 2) + " " + monthname[obj.getMonth()] + " " + obj.getFullYear() + " " + this._lpad(obj.getHours(), "0", 2) + ":" + this._lpad(obj.getMinutes(), "0", 2) + ":" + this._lpad(obj.getSeconds(), "0", 2) + " GMT";
	},

	_me_year: function(obj)
	{
		ul4._checkmethargs("year", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "year() requires a date";

		return obj.getFullYear();
	},

	_me_month: function(obj)
	{
		ul4._checkmethargs("month", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "month() requires a date";

		return obj.getMonth()+1;
	},

	_me_day: function(obj)
	{
		ul4._checkmethargs("day", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "day() requires a date";

		return obj.getDate();
	},

	_me_hour: function(obj)
	{
		ul4._checkmethargs("hour", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "hour() requires a date";

		return obj.getHours();
	},

	_me_minute: function(obj)
	{
		ul4._checkmethargs("mimute", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "minute() requires a date";

		return obj.getMinutes();
	},

	_me_second: function(obj)
	{
		ul4._checkmethargs("second", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "second() requires a date";

		return obj.getSeconds();
	},

	_me_microsecond: function(obj)
	{
		ul4._checkmethargs("microsecond", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "micosecond() requires a date";

		return obj.getMilliseconds() * 1000;
	},

	_me_weekday: function(obj)
	{
		ul4._checkmethargs("weekday", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "weekday() requires a date";

		var d = obj.getDay();
		return d ? d-1 : 6;
	},

	_isleap: function(obj)
	{
		ul4._checkmethargs("isleap", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "isleap() requires a date";

		return new Date(obj.getFullYear(), 1, 29).getMonth() === 1;
	},

	_me_yearday: function(obj)
	{
		ul4._checkmethargs("yearday", arguments, 0);
		if (!this._fu_isdate(obj))
			throw "yearday() requires a date";

		var leap = this._isleap(obj) ? 1 : 0;
		var day = obj.getDate();
		switch (obj.getMonth())
		{
			case 0:
				return day;
			case 1:
				return 31 + day;
			case 2:
				return 31 + 28 + leap + day;
			case 3:
				return 31 + 28 + leap + 31 + day;
			case 4:
				return 31 + 28 + leap + 31 + 30 + day;
			case 5:
				return 31 + 28 + leap + 31 + 30 + 31 + day;
			case 6:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + day;
			case 7:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + 31 + day;
			case 8:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + 31 + 31 + day;
			case 9:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + 31 + 31 + 30 + day;
			case 10:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + day;
			case 11:
				return 31 + 28 + leap + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + day;
		}
	},

	_me_renders: function(obj)
	{
		ul4._checkmethargs("renders", arguments, 0);
		return obj.renders({});
	},

	// Color methods
	_me_r: function(obj)
	{
		ul4._checkmethargs("r", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "r() requires a color";

		return obj.r;
	},

	_me_g: function(obj)
	{
		ul4._checkmethargs("g", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "g() requires a color";

		return obj.g;
	},

	_me_b: function(obj)
	{
		ul4._checkmethargs("b", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "b() requires a color";

		return obj.b;
	},

	_me_a: function(obj)
	{
		ul4._checkmethargs("a", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "a() requires a color";

		return obj.a;
	},

	_me_lum: function(obj)
	{
		ul4._checkmethargs("lum", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "lum() requires a color";

		return obj.lum();
	},

	_me_hls: function(obj)
	{
		ul4._checkmethargs("hls", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "hls() requires a color";

		return obj.hls();
	},

	_me_hlsa: function(obj)
	{
		ul4._checkmethargs("hlsa", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "hlsa() requires a color";

		return obj.hlsa();
	},

	_me_hsv: function(obj)
	{
		ul4._checkmethargs("hsv", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "hsv() requires a color";

		return obj.hsv();
	},

	_me_hsva: function(obj)
	{
		ul4._checkmethargs("hsva", arguments, 0);
		if (!this._fu_iscolor(obj))
			throw "hsva() requires a color";

		return obj.hsva();
	},

	_me_witha: function(obj, newa)
	{
		ul4._checkmethargs("witha", arguments, 1);
		if (!this._fu_iscolor(obj))
			throw "witha() requires a color";

		return obj.witha(newa);
	},

	_me_withlum: function(obj, newlum)
	{
		ul4._checkmethargs("withlum", arguments, 1);
		if (!this._fu_iscolor(obj))
			throw "withlum() requires a color";

		return obj.withlum(newlum);
	},

	// "Classes"
	Color: {
		__iscolor__: true,

		create: function(r, g, b, a)
		{
			var c = ul4._clone(this);
			c.r = typeof(r) !== "undefined" ? r : 0;
			c.g = typeof(g) !== "undefined" ? g : 0;
			c.b = typeof(b) !== "undefined" ? b : 0;
			c.a = typeof(a) !== "undefined" ? a : 255;
			return c;
		},

		lum: function()
		{
			return this.hls()[1];
		},

		hls: function()
		{
			var r = this.r/255.0;
			var g = this.g/255.0;
			var b = this.b/255.0;
			var maxc = Math.max(r, g, b);
			var minc = Math.min(r, g, b);
			var h, l, s;
			var rc, gc, bc;

			l = (minc+maxc)/2.0;
			if (minc == maxc)
				return [0.0, l, 0.0];
			if (l <= 0.5)
				s = (maxc-minc) / (maxc+minc);
			else
				s = (maxc-minc) / (2.0-maxc-minc);
			rc = (maxc-r) / (maxc-minc);
			gc = (maxc-g) / (maxc-minc);
			bc = (maxc-b) / (maxc-minc);
			if (r == maxc)
				h = bc-gc;
			else if (g == maxc)
				h = 2.0+rc-bc;
			else
				h = 4.0+gc-rc;
			h = (h/6.0) % 1.0;
			return [h, l, s];
		},

		hlsa: function()
		{
			var hls = this.hls();
			return hls.concat(this.a/255.0);
		},

		hsv: function()
		{
			var r = this.r/255.0;
			var g = this.g/255.0;
			var b = this.b/255.0;
			var maxc = Math.max(r, g, b);
			var minc = Math.min(r, g, b);
			var v = maxc;
			if (minc == maxc)
				return [0.0, 0.0, v];
			var s = (maxc-minc) / maxc;
			var rc = (maxc-r) / (maxc-minc);
			var gc = (maxc-g) / (maxc-minc);
			var bc = (maxc-b) / (maxc-minc);
			var h;
			if (r == maxc)
				h = bc-gc;
			else if (g == maxc)
				h = 2.0+rc-bc;
			else
				h = 4.0+gc-rc;
			h = (h/6.0) % 1.0;
			return [h, s, v];
		},

		hsva: function()
		{
			var hsv = this.hsv();
			return hsv.concat(this.a/255.0);
		},

		witha: function(a)
		{
			if (typeof(a) !== "number")
				throw "witha() requires a number";
			return ul4.Color.create(this.r, this.g, this.b, a);
		},

		withlum: function(lum)
		{
			if (typeof(lum) !== "number")
				throw "witha() requires a number";
			var hlsa = this.hlsa();
			return ul4._fu_hls(hlsa[0], lum, hlsa[2], hlsa[3]);
		}
	},

	/// Helper functions

	// Crockford style object creation
	_clone: function(obj)
	{
		function F(){};
		F.prototype = obj;
		var result = new F();
		result.__prototype__ = obj;
		result.__id__ = ul4.Proto._nextid++;
		return result;
	},

	// Clone an object and extend it
	_inherit: function(baseobj, attrs)
	{
		var newobj = ul4._clone(baseobj);
		attrs = attrs || {};
		for (var name in attrs)
			newobj[name] = attrs[name];
		return newobj;
	},

	// Return an iterator for ``obj``
	_iter: function(obj)
	{
		if (typeof(obj) === "string" || this._fu_islist(obj))
		{
			var i = 0;
			var result = function()
			{
				return (i < obj.length) ? [obj[i++]] : null;
			};
			result.__iter__ = true;
			return result;
		}
		else if (this._fu_isdict(obj))
		{
			var keys = [];
			for (var key in obj)
				keys.push(key);
			var i = 0;
			var result = function()
			{
				if (i >= keys.length)
					return null;
				return [keys[i++]];
			};
			result.__iter__ = true;
			return result;
		}
		else if (obj !== null && obj !== undefined && typeof(obj.__iter__) !== "undefined")
		{
			return obj;
		}
		throw "'" + this._fu_type(obj) + "' object is not iterable";
	},

	// Repeat string ``str`` ``rep`` times
	_str_repeat: function(str, rep)
	{
		var result = "";
		for (; rep>0; --rep)
			result += str;
		return result;
	},

	_list_repeat: function(list, rep)
	{
		var result = [];
		for (; rep>0; --rep)
			for (var i in list)
				result.push(list[i]);
		return result;
	},

	_date_repr: function(obj)
	{
		var year = obj.getFullYear();
		var month = obj.getMonth()+1;
		var day = obj.getDate();
		var hour = obj.getHours();
		var minute = obj.getMinutes();
		var second = obj.getSeconds();
		var ms = obj.getMilliseconds();
		var result = "@(" + year + "-" + this._lpad(month.toString(), "0", 2) + "-" + this._lpad(day.toString(), "0", 2);

		if (hour || minute || second || ms)
		{
			result += "T" + this._lpad(hour.toString(), "0", 2) + ":" + this._lpad(minute.toString(), "0", 2) + ":" + this._lpad(second.toString(), "0", 2);
			if (ms)
				result += "." + this._lpad(ms.toString(), "0", 3) + "000";
		}
		result += ")";

		return result;
	},

	_date_str: function(obj)
	{
		var year = obj.getFullYear();
		var month = obj.getMonth()+1;
		var day = obj.getDate();
		var hour = obj.getHours();
		var minute = obj.getMinutes();
		var second = obj.getSeconds();
		var ms = obj.getMilliseconds();
		var result = year + "-" + this._lpad(month.toString(), "0", 2) + "-" + this._lpad(day.toString(), "0", 2);

		if (hour || minute || second || ms)
		{
			result += " " + this._lpad(hour.toString(), "0", 2) + ":" + this._lpad(minute.toString(), "0", 2) + ":" + this._lpad(second.toString(), "0", 2);
			if (ms)
				result += "." + this._lpad(ms.toString(), "0", 3) + "000";
		}
		return result;
	},

	_color_repr: function(obj)
	{
		var r = this._lpad(obj.r.toString(16), "0", 2);
		var g = this._lpad(obj.g.toString(16), "0", 2);
		var b = this._lpad(obj.b.toString(16), "0", 2);
		var a = this._lpad(obj.a.toString(16), "0", 2);
		if (obj.a !== 0xff)
		{
			if (r[0] === r[1] && g[0] === g[1] && b[0] === b[1] && a[0] === a[1])
				return "#" + r[0] + g[0] + b[0] + a[0];
			else
				return "#" + r + g + b + a;
		}
		else
		{
			if (r[0] === r[1] && g[0] === g[1] && b[0] === b[1])
				return "#" + r[0] + g[0] + b[0];
			else
				return "#" + r + g + b;
		}
	},

	_color_str: function(obj)
	{
		if (obj.a !== 0xff)
		{
			return "rgba(" + obj.r + ", " + obj.g + ", " + obj.b + ", " + (obj.a/255) + ")";
		}
		else
		{
			var r = this._lpad(obj.r.toString(16), "0", 2);
			var g = this._lpad(obj.g.toString(16), "0", 2);
			var b = this._lpad(obj.b.toString(16), "0", 2);
			var a = this._lpad(obj.a.toString(16), "0", 2);
			if (r[0] === r[1] && g[0] === g[1] && b[0] === b[1])
				return "#" + r[0] + g[0] + b[0];
			else
				return "#" + r + g + b;
		}
	},

	_str_json: function(str)
	{
		var result = "";
		for (var i in str)
		{
			var c = str[i];
			switch (c)
			{
				case "\r":
					result += "\\r";
					break;
				case "\n":
					result += "\\n";
					break;
				case "\t":
					result += "\\t";
					break;
				case "\\":
					result += "\\\\";
					break;
				case '"':
					result += '\\"';
					break;
				default:
					var code = str.charCodeAt(i);
					if (code >= 32 && code < 128)
						result += c;
					else
						result += "\\u" + this._lpad(code.toString(16), "0", 4);
					break;
			}
		}
		return '"' + result + '"';
	},

	_str_repr: function(str)
	{
		var result = "";
		for (var i in str)
		{
			var c = str[i];
			switch (c)
			{
				case "\r":
					result += "\\r";
					break;
				case "\n":
					result += "\\n";
					break;
				case "\t":
					result += "\\t";
					break;
				case '"':
					result += '\\"';
					break;
				default:
					var code = str.charCodeAt(i);
					if (code >= 32 && code < 128)
						result += c;
					else
					{
						var prefix, length;
						if (code <= 0xFF)
						{
							prefix = "\\x";
							length = 2;
						}
						else if (code <= 0xFFFF)
						{
							prefix = "\\u";
							length = 4;
						}
						else
						{
							prefix = "\\U";
							length = 8;
						}
						result += prefix + this._lpad(code.toString(16), "0", length);
					}
					break;
			}
		}
		return '"' + result + '"';
	},

	_makedict: function()
	{
		var result = {};
		for (var i in arguments)
		{
			var item = arguments[i];
			if (item.length == 2)
				result[item[0]] = item[1];
			else
			{
				for (var key in item[0])
					result[key] = item[0][key];
			}
		}
		return result;
	},

	_lpad: function(string, pad, len)
	{
		if (typeof(string) === "number")
			string = string.toString();
		while (string.length < len)
			string = pad + string;
		return string;
	},

	_rpad: function(string, pad, len)
	{
		if (typeof(string) === "number")
			string = string.toString();
		while (string.length < len)
			string = string + pad;
		return string;
	},

	_checkfuncargs: function(funcname, args, min, max)
	{
		if (typeof(max) === "undefined")
			max = min;
		if (args.length < min || args.length > max)
		{
			if (min == max)
				throw "function " + funcname + "() requires " + min + " argument" + (min!==1 ? "s" : "") + ", " + args.length + " given";
			else
				throw "function " + funcname + "() requires " + min + "-" + max + " arguments, " + args.length + " given";
		}
	},

	_checkmethargs: function(methname, args, min, max)
	{
		if (typeof(max) === "undefined")
			max = min;
		if ((args.length-1) < min || (args.length-1) > max)
		{
			if (min == max)
				throw "method " + methname + "() requires " + min + " argument" + (min!==1 ? "s" : "") + ", " + (args.length-1) + " given";
			else
				throw "method " + methname + "() requires " + min + "-" + max + " arguments, " + (args.length-1) + " given";
		}
	}
};

ul4.Proto = {
	__prototype__: null,
	__id__: 0,
	_nextid: 1,
	isa: function(type)
	{
		if (this === type)
			return true;
		if (this.__prototype__ === null)
			return false;
		return this.__prototype__.isa(type);
	}
};

ul4.Location = ul4._inherit(
	ul4.Proto,
	{
		create: function(source, type, starttag, endtag, startcode, endcode)
		{
			var location = ul4._clone(this);
			location.source = source;
			location.type = type;
			location.starttag = starttag;
			location.endtag = endtag;
			location.startcode = startcode;
			location.endcode = endcode;
			// Unfortunately Javascript doesn't have what other languages call properties, so we must create real attributes here
			if (typeof(source) != "undefined")
			{
				location.tag = source.substring(starttag, endtag);
				location.code = source.substring(startcode, endcode);
			}
			else
			{
				location.tag = null;
				location.code = null;
			}
			return location;
		},
		ul4ondump: function(encoder)
		{
			encoder.dump(this.source);
			encoder.dump(this.type);
			encoder.dump(this.starttag);
			encoder.dump(this.endtag);
			encoder.dump(this.startcode);
			encoder.dump(this.endcode);
		},
		ul4onload: function(decoder)
		{
			this.source = decoder.load();
			this.type = decoder.load();
			this.starttag = decoder.load();
			this.endtag = decoder.load();
			this.startcode = decoder.load();
			this.endcode = decoder.load();

			this.tag = this.source.substring(this.starttag, this.endtag);
			this.code = this.source.substring(this.startcode, this.endcode);
		}
	}
);

ul4.Stack = ul4._inherit(
	ul4.Proto,
	{
		create: function()
		{
			var stack = ul4._clone(this);
			stack.stack = [];
			return stack;
		},
		push: function(obj)
		{
			this.stack.push(obj);
			return obj;
		},
		pop: function(obj)
		{
			var result = this.stack.pop();
			return (typeof(obj) === "undefined") ? result : obj;
		}
	}
);

ul4.AST = ul4._inherit(
	ul4.Proto,
	{
		create: function(location)
		{
			var ast = ul4._clone(this);
			ast.location = location;
			return ast;
		},
		_name: function()
		{
			var name = this.ul4onname.split(".");
			return name[name.length-1];
		},
		_line: function(indent, line)
		{
			return ul4._op_mul("\t", indent) + line + "\n";
		},
		_formatop: function(op)
		{
			if (op.precedence < this.precedence)
				return "(" + op.format(0) + ")";
			else if (op.precedence === this.precedence && (op.ul4onname !== this.ul4onname || !this.associative))
				return "(" + op.format(0) + ")";
			else
				return op.format(0);
		},
		_add2template: function(template)
		{
			template._asts[this.__id__] = this;
		},
		toString: function()
		{
			return this.format(0);
		},
		ul4ondump: function(encoder)
		{
			for (var i in this._ul4onattrs)
				encoder.dump(this[this._ul4onattrs[i]]);
		},
		ul4onload: function(decoder)
		{
			for (var i in this._ul4onattrs)
				this[this._ul4onattrs[i]] = decoder.load();
		},
		// used in ``format``/``_formatop`` to decide if we need brackets around an operator
		precedence: null,
		associative: true,
		// used in ul4ondump/ul4ondump to automatically dump these attributes
		_ul4onattrs: ["location"]
	}
);

ul4.Text = ul4._inherit(
	ul4.AST,
	{
		text: function()
		{
			return this.location.source.substring(this.location.startcode, this.location.endcode);
		},
		formatjs: function(indent)
		{
			return this._line(indent, "out.push(" + ul4._fu_asjson(this.text()) + ");");
		},
		format: function(indent)
		{
			return this._line(indent, "text " + ul4._fu_repr(this.text()));
		}
	}
);

ul4.LoadNone = ul4._inherit(
	ul4.AST,
	{
		formatjs: function(indent)
		{
			return "null";
		},
		format: function(indent)
		{
			return "None";
		},
		precedence: 11
	}
);

ul4.LoadTrue = ul4._inherit(
	ul4.AST,
	{
		formatjs: function(indent)
		{
			return "true";
		},
		format: function(indent)
		{
			return "True";
		},
		precedence: 11
	}
);

ul4.LoadFalse = ul4._inherit(
	ul4.AST,
	{
		formatjs: function(indent)
		{
			return "false";
		},
		format: function(indent)
		{
			return "False";
		},
		precedence: 11
	}
);

ul4.LoadConst = ul4._inherit(
	ul4.AST,
	{
		create: function(location, value)
		{
			var constant = ul4.AST.create.call(this, location);
			constant.value = value;
			return constant;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["value"]),
		formatjs: function(indent)
		{
			return ul4._fu_asjson(this.value);
		},
		format: function(indent)
		{
			return ul4._fu_repr(this.value);
		},
		precedence: 11
	}
);

ul4.LoadInt = ul4._inherit(ul4.LoadConst);

ul4.LoadFloat = ul4._inherit(ul4.LoadConst);

ul4.LoadStr = ul4._inherit(ul4.LoadConst);

ul4.LoadColor = ul4._inherit(ul4.LoadConst);

ul4.LoadDate = ul4._inherit(ul4.LoadConst);

ul4.List = ul4._inherit(
	ul4.AST,
	{
		create: function(location)
		{
			var list = ul4.AST.create.call(this, location);
			list.items = [];
			return list;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["items"]),
		formatjs: function(indent)
		{
			var v = [];
			for (var i in this.items)
				v.push(this.items[i].formatjs(indent));
			return "[" + v.join(", ") + "]";
		},
		format: function(indent)
		{
			var v = [];
			for (var i in this.items)
				v.push(this.items[i].format(indent));
			return "[" + v.join(", ") + "]";
		},
		precedence: 11
	}
);

ul4.Dict = ul4._inherit(
	ul4.AST,
	{
		create: function(location)
		{
			var dict = ul4.AST.create.call(this, location);
			dict.items = [];
			return dict;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["items"]),
		formatjs: function(indent)
		{
			var v = [];
			for (var i in this.items)
			{
				var item = this.items[i];
				if (item.length == 2)
					v.push("[" + item[0].formatjs(indent) + ", " + item[1].formatjs(indent) + "]");
				else
					v.push("[" + item[0].formatjs(indent) + "]");
			}
			return "ul4._makedict(" + v.join(", ") + ")";
		},
		format: function(indent)
		{
			var v = [];
			for (var i in this.items)
			{
				var item = this.items[i];
				if (item.length == 2)
					v.push(item[0].format(indent) + ": " + item[1].format(indent));
				else
					v.push("**" + item[0].format(indent));
			}
			return "{" + v.join(", ") + "}";
		},
		precedence: 11
	}
);

ul4.LoadVar = ul4._inherit(
	ul4.AST,
	{
		create: function(location, name)
		{
			var variable = ul4.AST.create.call(this, location);
			variable.name = name;
			return variable;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["name"]),
		formatjs: function(indent)
		{
			return "vars[" + ul4._fu_asjson(this.name) + "]";
		},
		format: function(indent)
		{
			return this.name;
		},
		precedence: 11
	}
);

ul4.Unary = ul4._inherit(
	ul4.AST,
	{
		create: function(location, obj)
		{
			var unary = ul4.AST.create.call(this, location);
			unary.obj = obj;
			return unary;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["obj"]),
		formatjs: function(indent)
		{
			return "ul4._op_" + this._name() + "(" + this.obj.formatjs(indent) + ")";
		}
	}
);

ul4.Neg = ul4._inherit(
	ul4.Unary,
	{
		format: function(indent)
		{
			return "-" + this._formatop(this.obj);
		},
		precedence: 7
	}
);

ul4.Not = ul4._inherit(
	ul4.Unary,
	{
		format: function(indent)
		{
			return "not " + this._formatop(this.obj);
		},
		precedence: 2
	}
);

ul4.Print = ul4._inherit(
	ul4.Unary,
	{
		formatjs: function(indent)
		{
			return this._line(indent, "out.push(ul4._fu_str(" + this.obj.formatjs(indent) + "));");
		},
		format: function(indent)
		{
			return this._line(indent, "print " + this.obj.format(indent));
		}
	}
);

ul4.PrintX = ul4._inherit(
	ul4.Unary,
	{
		formatjs: function(indent)
		{
			return this._line(indent, "out.push(ul4._fu_xmlescape(" + this.obj.formatjs(indent) + "));");
		},
		format: function(indent)
		{
			return this._line(indent, "printx " + this.obj.format(indent));
		}
	}
);

ul4.Binary = ul4._inherit(
	ul4.AST,
	{
		create: function(location, obj1, obj2)
		{
			var binary = ul4.AST.create.call(this, location);
			binary.obj1 = obj1;
			binary.obj2 = obj2;
			return binary;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["obj1", "obj2"]),
		formatjs: function(indent)
		{
			return "ul4._op_" + this._name() + "(" + this.obj1.formatjs(indent) + ", " + this.obj2.formatjs(indent) + ")";
		}
	}
);

ul4.GetItem = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + "[" + this.obj2.format(0) + "]";
		},
		precedence: 9,
		associative: false
	}
);

ul4.EQ = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " == " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.NE = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " != " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.LT = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " < " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.LE = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " <= " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.GT = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " > " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.GE = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " >= " + this._formatop(this.obj2);
		},
		precedence: 4,
		associative: false
	}
);

ul4.Contains = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " in " + this._formatop(this.obj2);
		},
		precedence: 3,
		associative: false
	}
);

ul4.NotContains = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " not in " + this._formatop(this.obj2);
		},
		precedence: 3,
		associative: false
	}
);

ul4.Add = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " + " + this._formatop(this.obj2);
		},
		precedence: 5
	}
);

ul4.Sub = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " - " + this._formatop(this.obj2);
		},
		precedence: 5,
		associative: false
	}
);

ul4.Mul = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " * " + this._formatop(this.obj2);
		},
		precedence: 6
	}
);

ul4.FloorDiv = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " // " + this._formatop(this.obj2);
		},
		precedence: 6,
		associative: false
	}
);

ul4.TrueDiv = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " / " + this._formatop(this.obj2);
		},
		precedence: 6,
		associative: false
	}
);

ul4.Mod = ul4._inherit(
	ul4.Binary,
	{
		format: function(indent)
		{
			return this._formatop(this.obj1) + " % " + this._formatop(this.obj2);
		},
		precedence: 6,
		associative: false
	}
);

ul4.And = ul4._inherit(
	ul4.Binary,
	{
		formatjs: function(indent)
		{
			return "ul4._fu_bool(stack.push(" + this.obj2.formatjs(indent) + ")) ? stack.pop(" + this.obj1.formatjs(indent) + ") : stack.pop()";
		},
		format: function(indent)
		{
			return this._formatop(this.obj1) + " and " + this._formatop(this.obj2);
		},
		precedence: 1
	}
);

ul4.Or = ul4._inherit(
	ul4.Binary,
	{
		formatjs: function(indent)
		{
			return "ul4._fu_bool(stack.push(" + this.obj1.formatjs(indent) + ")) ? stack.pop() : stack.pop(" + this.obj2.formatjs(indent) + ")";
		},
		format: function(indent)
		{
			return this._formatop(this.obj1) + " or " + this._formatop(this.obj2);
		},
		precedence: 0
	}
);

ul4.GetAttr = ul4._inherit(
	ul4.AST,
	{
		create: function(location, obj, attrname)
		{
			var getattr = ul4.AST.create.call(this, location);
			getattr.obj = obj;
			getattr.attrname = attrname;
			return getattr;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["obj", "attrname"]),
		formatjs: function(indent)
		{
			return "ul4._op_getitem(" + this.obj.formatjs(indent) + ", " + ul4._fu_repr(this.attrname) + ")";
		},
		format: function(indent)
		{
			return this._formatop(this.obj) + "." + this.attrname;
		},
		precedence: 9,
		associative: false
	}
);

ul4.CallFunc = ul4._inherit(
	ul4.AST,
	{
		create: function(location, funcname, args)
		{
			var callfunc = ul4.AST.create.call(this, location);
			callfunc.funcname = funcname;
			callfunc.args = args;
			return callfunc;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["funcname", "args"]),
		formatjs: function(indent)
		{
			if (this.funcname === "vars" || this.funcname === "get")
			{
				var v = [];
				for (var i in this.args)
					v.push(", " + this.args[i].formatjs(indent));
				return "ul4._fu_" + this.funcname + "(vars" + v.join("") + ")";
			}
			else
			{
				var v = [];
				for (var i in this.args)
					v.push(this.args[i].formatjs(indent));
				return "ul4._fu_" + this.funcname + "(" + v.join(", ") + ")";
			}
		},
		format: function(indent)
		{
			var v = [];
			for (var i in this.args)
				v.push(this.args[i].format(indent));
			return this.funcname + "(" + v.join(", ") + ")";
		},
		precedence: 10,
		associative: false
	}
);

ul4.GetSlice = ul4._inherit(
	ul4.AST,
	{
		create: function(location, obj, index1, index2)
		{
			var getslice = ul4.AST.create.call(this, location);
			getslice.obj = obj;
			getslice.index1 = index1;
			getslice.index2 = index2;
			return getslice;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["obj", "index1", "index2"]),
		format: function(indent)
		{
			return this._formatop(this.obj) + "[" + (this.index1 !== null ? this.index1.format(indent) : "") + ":" + (this.index2 !== null ? this.index2.format(indent) : "") + "]";
		},
		formatjs: function(indent)
		{
			return "ul4._op_getslice(" + this.obj.formatjs(indent) + ", " + (this.index1 !== null ? this.index1.formatjs(indent) : "null") + ", " + (this.index2 !== null ? this.index2.formatjs(indent) : "null") + ")";
		},
		precedence: 8,
		associative: false
	}
);

ul4.CallMeth = ul4._inherit(
	ul4.AST,
	{
		create: function(location, methname, obj, args)
		{
			var callfunc = ul4.AST.create.call(this, location);
			callfunc.methname = methname;
			callfunc.obj = obj;
			callfunc.args = args;
			return callfunc;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["methname", "obj", "args"]),
		formatjs: function(indent)
		{
			var v = [this.obj.formatjs(indent)];
			for (var i in this.args)
				v.push(this.args[i].formatjs(indent));
			return "ul4._me_" + this.methname + "(" + v.join(", ") + ")";
		},
		format: function(indent)
		{
			var v = [];
			for (var i in this.args)
				v.push(this.args[i].format(indent));
			return this._formatop(this.obj) + "." + this.methname + "(" + v.join(", ") + ")";
		},
		precedence: 10,
		associative: false
	}
);

ul4.CallMethKeywords = ul4._inherit(
	ul4.AST,
	{
		create: function(location, methname, obj, args)
		{
			var callfunc = ul4.AST.create.call(this, location);
			callfunc.methname = methname;
			callfunc.obj = obj;
			callfunc.args = args;
			return callfunc;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["methname", "obj", "args"]),
		format: function(indent)
		{
			var v = [];
			for (var i in this.args)
			{
				var arg = this.args[i];
				if (arg.length == 2)
					v.push(arg[0] + "=" + arg[1].format(indent));
				else
					v.push("**" + arg[0].format(indent));
			}
			return this._formatop(this.obj) + "." + this.methname + "(" + v.join(", ") + ")";
		},
		formatjs: function(indent)
		{
			var v = [];
			for (var i in this.args)
			{
				var arg = this.args[i];
				if (arg.length == 2)
					v.push("[" + ul4._fu_asjson(arg[0]) + ", " + arg[1].formatjs(indent) + "]");
				else
					v.push("[" + arg[0].formatjs(indent) + "]");
			}
			if (this.methname === "renders")
				return this.obj.formatjs(indent) + ".renders(ul4._makedict(" + v.join(", ") + "))";
			else if (this.methname === "render")
				return "out.push.apply(out, " + this.obj.formatjs(indent) + ".render(ul4._makedict(" + v.join(", ") + ")))";
			else
				return "";
		},
		precedence: 9,
		associative: false
	}
);

ul4.Render = ul4._inherit(
	ul4.Unary,
	{
		format: function(indent)
		{
			return this._line(indent, "render " + this.obj.format(indent));
		},
		formatjs: function(indent)
		{
			if (this.obj.isa(ul4.CallMeth) || this.obj.isa(ul4.CallMethKeywords) && this.obj.methname === "render")
				return this._line(indent, this.obj.formatjs(indent));
			else
				return this._line(indent, "out.push(ul4._fu_str(" + this.obj.formatjs(indent) + "))");
		}
	}
);

ul4.ChangeVar = ul4._inherit(
	ul4.AST,
	{
		create: function(location, varname, value)
		{
			var changevar = ul4.AST.create.call(this, location);
			changevar.varname = varname;
			changevar.value = value;
			return changevar;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["varname", "value"])
	}
);

ul4.StoreVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " = " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			return this._line(indent, "vars[" + ul4._fu_asjson(this.varname) + "] = " + this.value.formatjs(indent) + ";");
		}
	}
);

ul4.AddVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " += " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_add(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.SubVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " -= " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_sub(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.MulVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " *= " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_mul(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.TrueDivVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " /= " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_truediv(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.FloorDivVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " //= " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_floordiv(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.ModVar = ul4._inherit(
	ul4.ChangeVar,
	{
		format: function(indent)
		{
			return this._line(indent, this.varname + " %= " + this.value.format(indent));
		},
		formatjs: function(indent)
		{
			var varname = ul4._fu_asjson(this.varname);
			return this._line(indent, "vars[" + varname + "] = ul4._op_mod(vars[" + varname + "], " + this.value.formatjs(indent) + ");");
		}
	}
);

ul4.DelVar = ul4._inherit(
	ul4.AST,
	{
		create: function(location, varname)
		{
			var delvar = ul4.AST.create.call(this, location);
			delvar.varname = varname;
			return delvar;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["varname"]),
		format: function(indent)
		{
			return this._line(indent, "del " + this.varname);
		},
		formatjs: function(indent)
		{
			return this._line(indent, "vars[" + ul4._fu_asjson(this.varname) + "] = null;");
		}
	}
);

ul4.Block = ul4._inherit(
	ul4.AST,
	{
		create: function(location)
		{
			var block = ul4.AST.create.call(this, location);
			block.endlocation = null;
			block.content = [];
			return block;
		},
		_ul4onattrs: ul4.AST._ul4onattrs.concat(["endlocation", "content"]),
		_add2template: function(template)
		{
			ul4.AST._add2template.call(this, template);
			for (var i in this.content)
				this.content[i]._add2template(template);
		},
		_formatjs_content: function(indent)
		{
			var v = [];
			for (var i in this.content)
				v.push(this.content[i].formatjs(indent));
			return v.join("");
		},
		format: function(indent)
		{
			var v = [];
			v.push(this._line(indent, "{"));
			++indent;
			for (var i in this.content)
				v.push(this.content[i].format(indent));
			--indent;
			v.push(this._line(indent, "}"));
			return v.join("");
		}
	}
);

ul4.ForNormal = ul4._inherit(
	ul4.Block,
	{
		create: function(location, container, varname)
		{
			var fornormal = ul4.Block.create.call(this, location);
			fornormal.container = container;
			fornormal.varname = varname;
			return fornormal;
		},
		_ul4onattrs: ul4.Block._ul4onattrs.concat(["container", "varname"]),
		formatjs: function(indent)
		{
			var v = [];
			v.push(this._line(indent, "for (var iter" + this.__id__ + " = ul4._iter(" + this.container.formatjs(indent) + ");;)"));
			v.push(this._line(indent, "{"));
			++indent;
			v.push(this._line(indent, "var item" + this.__id__ + " = iter" + this.__id__ + "();"));
			v.push(this._line(indent, "if (item" + this.__id__ + " === null)"));
			v.push(this._line(indent+1, "break;"));
			v.push(this._line(indent, "vars[" + ul4._fu_asjson(this.varname) + "] = item" + this.__id__ + "[0];"));
			v.push(this._formatjs_content(indent));
			--indent;
			v.push(this._line(indent, "}"));
			return v.join("");
		},
		format: function(indent)
		{
			return this._line(indent, "for " + this.varname + " in " + this.container.format(indent)) + ul4.Block.format.call(this, indent);
		}
	}
);

ul4.ForUnpack = ul4._inherit(
	ul4.Block,
	{
		create: function(location, container, varnames)
		{
			var fornormal = ul4.Block.create.call(this, location);
			fornormal.container = container;
			fornormal.varnames = varnames;
			return fornormal;
		},
		_ul4onattrs: ul4.Block._ul4onattrs.concat(["container", "varnames"]),
		formatjs: function(indent)
		{
			var v = [];
			v.push(this._line(indent, "for (var iter" + this.__id__ + " = ul4._iter(" + this.container.formatjs(indent) + ");;)"));
			v.push(this._line(indent, "{"));
			++indent;
			v.push(this._line(indent, "var item" + this.__id__ + " = iter" + this.__id__ + "();"));
			v.push(this._line(indent, "if (item" + this.__id__ + " === null)"));
			v.push(this._line(indent+1, "break;"));
			v.push(this._line(indent, "var items" + this.__id__ + " = ul4._fu_list(item" + this.__id__ + "[0]);"));
			v.push(this._line(indent, "if (items" + this.__id__ + ".length != " + this.varnames.length + ")"));
			v.push(this._line(indent+1, "throw 'mismatched for loop unpacking: " + this.varnames.length + " varnames, ' + items" + this.__id__ + ".length + ' items';"));
			for (var i = 0; i < this.varnames.length; ++i)
				v.push(this._line(indent, "vars[" + ul4._fu_asjson(this.varnames[i]) + "] = items" + this.__id__ + "[" + i + "];"));
			v.push(this._formatjs_content(indent));
			--indent;
			v.push(this._line(indent, "}"));
			return v.join("");
		},
		format: function(indent)
		{
			return this._line(indent, "for (" + this.varnames.join(", ") + ") in " + this.container.format(indent)) + ul4.Block.format.call(this, indent);
		}
	}
);

ul4.Break = ul4._inherit(
	ul4.AST,
	{
		formatjs: function(indent)
		{
			return this._line(indent, "break;");
		},
		format: function(indent)
		{
			return this._line(indent, "break");
		}
	}
);

ul4.Continue = ul4._inherit(
	ul4.AST,
	{
		formatjs: function(indent)
		{
			return this._line(indent, "continue;");
		},
		format: function(indent)
		{
			return this._line(indent, "continue");
		}
	}
);

ul4.IfElIfElse = ul4._inherit(
	ul4.Block,
	{
		formatjs: function(indent)
		{
			return this._formatjs_content(indent);
		},
		format: function(indent)
		{
			var v = [];
			for (var i in this.content)
				v.push(this.content[i].format(indent));
			return v.join("");
		}
	}
);

ul4.ConditionalBlock = ul4._inherit(
	ul4.Block,
	{
		create: function(location, condition)
		{
			var block = ul4.Block.create.call(this, location);
			block.condition = condition;
			return block;
		},
		_ul4onattrs: ul4.Block._ul4onattrs.concat(["condition"]),
		formatjs: function(indent)
		{
			var v = [];
			v.push(this._line(indent, this._sourcejs + " (ul4._fu_bool(" + this.condition.formatjs(indent) + "))"));
			v.push(this._line(indent, "{"));
			v.push(this._formatjs_content(indent+1));
			v.push(this._line(indent, "}"));
			return v.join("");
		},
		format: function(indent)
		{
			return this._line(indent, this._name() + " " + this.condition.format(indent)) + ul4.Block.format.call(this, indent);
		}
	}
);

ul4.If = ul4._inherit(
	ul4.ConditionalBlock,
	{
		_sourcejs: "if"
	}
);

ul4.ElIf = ul4._inherit(
	ul4.ConditionalBlock,
	{
		_sourcejs: "else if"
	}
);

ul4.Else = ul4._inherit(
	ul4.Block,
	{
		formatjs: function(indent)
		{
			var v = [];
			v.push(this._line(indent, "else"));
			v.push(this._line(indent, "{"));
			v.push(this._formatjs_content(indent+1));
			v.push(this._line(indent, "}"));
			return v.join("");
		},
		format: function(indent)
		{
			return this._line(indent, "else") + ul4.Block.format.call(this, indent);
		}
	}
);

ul4.Template = ul4._inherit(
	ul4.Block,
	{
		create: function(location, source, name, startdelim, enddelim)
		{
			var template = ul4.Block.create.call(this, location);
			template.endlocation = null;
			template.source = source;
			template.name = name;
			template.startdelim = startdelim;
			template.enddelim = enddelim;
			template._jssource = null;
			template._jsfunction = null;
			template._asts = null;
			return template;
		},
		ul4ondump: function(encoder)
		{
			encoder.dump(ul4.version);
			encoder.dump(this.source);
			encoder.dump(this.name);
			encoder.dump(this.startdelim);
			encoder.dump(this.enddelim);
			ul4.Block.ul4ondump.call(this, encoder);
		},
		ul4onload: function(decoder)
		{
			var version = decoder.load();
			if (version !== ul4.version)
				throw "invalid version, expected " + ul4.version + ", got " + version;
			this.source = decoder.load();
			this.name = decoder.load();
			this.startdelim = decoder.load();
			this.enddelim = decoder.load();
			ul4.Block.ul4onload.call(this, decoder);
		},
		formatjs: function(indent)
		{
			return this._line(indent, "vars[" + ul4._fu_asjson(this.name) + "] = self._getast(" + this.__id__ + ");");
		},
		format: function(indent)
		{
			return this._line(indent, "def " + (this.name !== null ? this.name : "unnamed")) + ul4.Block.format.call(this, indent);
		},
		_getast: function(id)
		{
			if (this._asts === null)
			{
				this._asts = {};
				this._add2template(this);
			}
			return this._asts[id];
		},
		jssource: function()
		{
			if (this._jssource === null)
			{
				var v = [];
				v.push(this._line(0, "(function(self, vars)"));
				v.push(this._line(0, "{"));
				v.push(this._line(1, "var stack = ul4.Stack.create();"));
				v.push(this._line(1, "var out = [];"));
				v.push(this._formatjs_content(1));
				v.push(this._line(1, "return out;"));
				v.push(this._line(0, "})"));
				this._jssource = v.join("");
			}
			return this._jssource;
		},
		render: function(vars)
		{
			vars = vars || {};
			if (this._jsfunction === null)
				this._jsfunction = eval(this.jssource());
			return this._jsfunction(this, vars);
		},
		renders: function(vars)
		{
			return this.render(vars).join("");
		},
		loads: function(string)
		{
			return ul4on.loads(string);
		},
		__istemplate__: true // used by ``istemplate()``
	}
);

(function(){
	var register = function(name, object)
	{
		object.type = name;
		ul4on.register("de.livinglogic.ul4." + name, object);
	};
	register("location", ul4.Location);
	register("text", ul4.Text);
	register("none", ul4.LoadNone);
	register("false", ul4.LoadFalse);
	register("true", ul4.LoadTrue);
	register("int", ul4.LoadInt);
	register("float", ul4.LoadFloat);
	register("str", ul4.LoadStr);
	register("color", ul4.LoadColor);
	register("date", ul4.LoadDate);
	register("list", ul4.List);
	register("dict", ul4.Dict);
	register("var", ul4.LoadVar);
	register("not", ul4.Not);
	register("neg", ul4.Neg);
	register("print", ul4.Print);
	register("printx", ul4.PrintX);
	register("getitem", ul4.GetItem);
	register("eq", ul4.EQ);
	register("ne", ul4.NE);
	register("lt", ul4.LT);
	register("le", ul4.LE);
	register("gt", ul4.GT);
	register("ge", ul4.GE);
	register("notcontains", ul4.NotContains);
	register("contains", ul4.Contains);
	register("add", ul4.Add);
	register("sub", ul4.Sub);
	register("mul", ul4.Mul);
	register("floordiv", ul4.FloorDiv);
	register("truediv", ul4.TrueDiv);
	register("mod", ul4.Mod);
	register("and", ul4.And);
	register("or", ul4.Or);
	register("getslice", ul4.GetSlice);
	register("getattr", ul4.GetAttr);
	register("callfunc", ul4.CallFunc);
	register("callmeth", ul4.CallMeth);
	register("callmethkw", ul4.CallMethKeywords);
	register("render", ul4.Render);
	register("storevar", ul4.StoreVar);
	register("addvar", ul4.AddVar);
	register("subvar", ul4.SubVar);
	register("mulvar", ul4.MulVar);
	register("truedivvar", ul4.TrueDivVar);
	register("floordivvar", ul4.FloorDivVar);
	register("modvar", ul4.ModVar);
	register("delvar", ul4.DelVar);
	register("for", ul4.ForNormal);
	register("foru", ul4.ForUnpack);
	register("break", ul4.Break);
	register("continue", ul4.Continue);
	register("ieie", ul4.IfElIfElse);
	register("if", ul4.If);
	register("elif", ul4.ElIf);
	register("else", ul4.Else);
	register("template", ul4.Template);
})();
