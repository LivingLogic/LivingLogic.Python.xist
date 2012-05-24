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

	// Functions with the ``_op_`` prefix implement UL4 opcodes

	// Addition: num + num, string + string
	_op_add: function(obj1, obj2)
	{
		return obj1 + obj2;
	},

	// Substraction: num - num
	_op_sub: function(obj1, obj2)
	{
		return obj1 - obj2;
	},

	// Multiplication: num * num, int * str, str * int, int * list, list * int
	_op_mul: function(obj1, obj2)
	{
		if (this._fu_isint(obj1) || this._fu_isbool(obj1))
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
		return Math.floor(obj1 / obj2);
	},

	// "Real" division
	_op_truediv: function(obj1, obj2)
	{
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
		if (this._fu_isdict(container))
		{
			var result = container[key];
			if (typeof(result) === "undefined")
				throw "key " + this._fu_repr(key) + " not found";
			return result;
		}
		else if (typeof(container) === "string" || this._fu_islist(container))
		{
			var orgkey = key;
			if (key < 0)
				key += container.length;
			if (key < 0 || key >= container.length)
				throw "index " + this._fu_repr(orgkey) + " out of range";
			return container[key];
		}
		else if (this._fu_iscolor(container))
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
		if (arguments.length != 1)
			throw "isnone() requires 1 argument, " + arguments.length + " given";

		return obj === null;
	},

	// Check if ``obj`` is a boolean
	_fu_isbool: function(obj)
	{
		if (arguments.length != 1)
			throw "isbool() requires 1 argument, " + arguments.length + " given";

		return typeof(obj) == "boolean";
	},

	// Check if ``obj`` is a int
	_fu_isint: function(obj)
	{
		if (arguments.length != 1)
			throw "isint() requires 1 argument, " + arguments.length + " given";

		return (typeof(obj) == "number") && Math.round(obj) == obj;
	},

	// Check if ``obj`` is a float
	_fu_isfloat: function(obj)
	{
		if (arguments.length != 1)
			throw "isfloat() requires 1 argument, " + arguments.length + " given";

		return (typeof(obj) == "number") && Math.round(obj) != obj;
	},

	// Check if ``obj`` is a string
	_fu_isstr: function(obj)
	{
		if (arguments.length != 1)
			throw "isstr() requires 1 argument, " + arguments.length + " given";

		return typeof(obj) == "string";
	},

	// Check if ``obj`` is a date
	_fu_isdate: function(obj)
	{
		if (arguments.length != 1)
			throw "isdate() requires 1 argument, " + arguments.length + " given";

		return Object.prototype.toString.call(obj) == "[object Date]";
	},

	// Check if ``obj`` is a color
	_fu_iscolor: function(obj)
	{
		if (arguments.length != 1)
			throw "iscolor() requires 1 argument, " + arguments.length + " given";

		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__iscolor__;
	},

	// Check if ``obj`` is a template
	_fu_istemplate: function(obj)
	{
		if (arguments.length != 1)
			throw "istemplate() requires 1 argument, " + arguments.length + " given";

		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__istemplate__;
	},

	// Check if ``obj`` is a list
	_fu_islist: function(obj)
	{
		if (arguments.length != 1)
			throw "list() requires 1 argument, " + arguments.length + " given";

		return Object.prototype.toString.call(obj) == "[object Array]";
	},

	// Check if ``obj`` is a dict
	_fu_isdict: function(obj)
	{
		if (arguments.length != 1)
			throw "isdict() requires 1 argument, " + arguments.length + " given";

		return Object.prototype.toString.call(obj) == "[object Object]" && !obj.__iscolor__ && !obj.__istemplate__;
	},

	// Convert ``obj`` to bool, according to its "truth value"
	_fu_bool: function(obj)
	{
		if (arguments.length != 1)
			throw "bool() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length < 3 || arguments.length > 4)
			throw "rgb() requires 3-4 argument, " + arguments.length + " given";

		return this.Color.create(255*r, 255*g, 255*b, typeof(a) == "undefined" ? 0xff : (255*a));
	},

	// Return the type of ``obj`` as a string
	_fu_type: function(obj)
	{
		if (arguments.length != 1)
			throw "type() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "str() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length < 1 || arguments.length > 2)
			throw "int() requires 1-2 arguments, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "float() requires 1 argument, " + arguments.length + " given";

		if (typeof(obj) == "string")
			return parseFloat(obj);
		else if (typeof(obj) == "number")
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
		if (arguments.length != 1)
			throw "list() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "len() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "repr() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 2)
			throw "format() requires 2 arguments, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "xmlescape() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "csv() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "chr() requires 1 argument, " + arguments.length + " given";

		if (typeof(obj) != "number")
			throw "chr() requires an int";
		return String.fromCharCode(obj);
	},

	// Return the codepoint for the one and only character in the string ``obj``
	_fu_ord: function(obj)
	{
		if (arguments.length != 1)
			throw "ord() requires 1 argument, " + arguments.length + " given";

		if (typeof(obj) != "string" || obj.length != 1)
			throw "ord() requires a string of length 1";
		return obj.charCodeAt(0);
	},

	// Convert an integer to a hexadecimal string
	_fu_hex: function(obj)
	{
		if (arguments.length != 1)
			throw "hex() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "oct() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "bin() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "sorted() requires 1 argument, " + arguments.length + " given";

		var result = this._fu_list(obj);
		result.sort();
		return result;
	},

	// Return a iterable object iterating from ``start`` upto (but not including) ``stop`` with a step size of ``step``
	_fu_range: function(start, stop, step)
	{
		if (arguments.length < 1 || arguments.length > 3)
			throw "range() requires 1-3 arguments, " + arguments.length + " given";

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
	_fu_json: function(obj)
	{
		if (arguments.length != 1)
			throw "json() requires 1 argument, " + arguments.length + " given";

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
			for (var i in obj)
			{
				if (i !== 0)
					v.push(", ");
				v.push(this._fu_json(obj[i]));
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
				v.push(this._fu_json(key));
				v.push(": ");
				v.push(this._fu_json(obj[key]));
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
			return "ul4.Color.create(" + obj.value.r + ", " + obj.value.g + ", " + obj.value.b + ", " + obj.value.a + ")";
		}
		else if (this._fu_istemplate(obj))
		{
			return "ul4.Template.loads(" + ul4._fu_repr(obj.dumps()) + ")";
		}
		throw "json() requires a serializable object";
	},

	// Return a reverse iterator over ``obj``
	_fu_reversed: function(obj)
	{
		if (arguments.length != 1)
			throw "reversed() requires 1 argument, " + arguments.length + " given";

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

	// Return a randomly select item from ``range(start, stop, step)``
	_fu_randrange: function(start, stop, step)
	{
		if (arguments.length < 1 || arguments.length > 3)
			throw "randrange() requires 1-3 arguments, " + arguments.length + " given";

		if (typeof(step) === "undefined")
		{
			step =-1;
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
		if (arguments.length != 1)
			throw "randchoice() requires 1 argument, " + arguments.length + " given";

		var iscolor = this._fu_iscolor(obj);
		if (typeof(obj) !== "string" && !this._fu_islist(obj) && !iscolor)
			throw "randchoice() requires a string or list";
		if (iscolor)
			obj = this._fu_list(obj);
		return obj[Math.floor(Math.random() * obj.length)];
	},

	// Return an iterator over ``[index, item]`` lists from the iterable object ``obj``
	_fu_enumerate: function(obj)
	{
		if (arguments.length != 1)
			throw "enumerate() requires 1 argument, " + arguments.length + " given";

		var iter = this._iter(obj);
		var i = 0;
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
		if (arguments.length != 1)
			throw "isfirst() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "islast() requires 1 argument, " + arguments.length + " given";

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
		if (arguments.length != 1)
			throw "isfirstlast() requires 1 argument, " + arguments.length + " given";

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
	_fu_enumfl: function(obj)
	{
		if (arguments.length != 1)
			throw "enumfl() requires 1 argument, " + arguments.length + " given";

		var iter = this._iter(obj);
		var i = 0;
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
		if (arguments.length != 1)
			throw "abs() requires 1 argument, " + arguments.length + " given";

		return Math.abs(obj);
	},

	// Return a ``Date`` object for the current time
	_fu_now: function()
	{
		if (arguments.length != 0)
			throw "now() requires 0 arguments, " + arguments.length + " given";

		return new Date();
	},

	// Return a ``Date`` object for the current time in UTC
	_fu_utcnow: function()
	{
		if (arguments.length != 0)
			throw "utcnow() requires 0 arguments, " + arguments.length + " given";

		var now = new Date();
		// FIXME: The timezone is wrong for the new ``Date`` object.
		return new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
	},

	// Return a ``Color`` object from the hue, luminescence, saturation and alpha values ``h``, ``l``, ``s`` and ``a`` (i.e. using the HLS color model)
	_fu_hls: function(h, l, s, a)
	{
		if (arguments.length < 3 || arguments.length > 4)
			throw "hls() requires 3-4 arguments, " + arguments.length + " given";

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
		if (arguments.length < 3 || arguments.length > 4)
			throw "hsv() requires 3-4 arguments, " + arguments.length + " given";

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

	// Functions with the ``_me_`` prefix implement UL4 methods
	_me_replace: function(string, searchstring, replacestring, count)
	{
		var result = [];
		if (typeof(count) === "undefined")
			count = string.length;
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
		if (typeof(string) !== "string")
			throw "split() requires a string as first argument";
		if (sep !== null && typeof(sep) !== "string")
			throw "split() requires a string as second argument";
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
		if (typeof(string) !== "string")
			throw "rsplit() requires a string as first argument";
		if (sep !== null && typeof(sep) !== "string")
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
		if (start === null)
			start = 0;
		if (stop === null)
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
		if (start === null)
			start = 0;
		if (stop === null)
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
		if (typeof(obj) != "string")
			throw "lower() requires a string";
		return obj.toLowerCase();
	},

	_me_upper: function(obj)
	{
		if (typeof(obj) != "string")
			throw "upper() requires a string";
		return obj.toUpperCase();
	},

	_me_capitalize: function(obj)
	{
		if (typeof(obj) != "string")
			throw "capitalize() requires a string";
		if (obj.length)
			obj = obj[0].toUpperCase() + obj.slice(1).toLowerCase();
		return obj;
	},

	_me_get: function(container, key, defaultvalue)
	{
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
		if (!this._fu_isdict(obj))
			throw "items() requires a dict";
		var result = [];
		for (var key in obj)
			result.push([key, obj[key]]);
		return result;
	},

	_me_join: function(sep, container)
	{
		if (typeof(sep) !== "string")
			throw "join() requires a string";
		if (!this._fu_islist(container))
			container = this._fu_list(container);
		return container.join(sep);
	},

	_me_startswith: function(string, prefix)
	{
		if (typeof(string) !== "string" || typeof(prefix) !== "string")
			throw "startswith() requires two strings";

		return string.substr(0, prefix.length) === prefix;
	},

	_me_endswith: function(string, suffix)
	{
		if (typeof(string) !== "string" || typeof(suffix) !== "string")
			throw "endswith() requires two strings";

		return string.substr(string.length-suffix.length) === suffix;
	},

	_me_isoformat: function(obj)
	{
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
		var weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
		var monthname = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

		if (!this._fu_isdate(obj))
			throw "mimeformat() requires a date";

		return weekdayname[this._me_weekday(obj)] + ", " + this._lpad(obj.getDate(), "0", 2) + " " + monthname[obj.getMonth()] + " " + obj.getFullYear() + " " + this._lpad(obj.getHours(), "0", 2) + ":" + this._lpad(obj.getMinutes(), "0", 2) + ":" + this._lpad(obj.getSeconds(), "0", 2) + " GMT";
	},

	_me_year: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "year() requires a date";
		return obj.getFullYear();
	},

	_me_month: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "month() requires a date";
		return obj.getMonth()+1;
	},

	_me_day: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "day() requires a date";
		return obj.getDate();
	},

	_me_hour: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "hour() requires a date";
		return obj.getHours();
	},

	_me_minute: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "minute() requires a date";
		return obj.getMinutes();
	},

	_me_second: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "second() requires a date";
		return obj.getSeconds();
	},

	_me_microsecond: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "micosecond() requires a date";
		return obj.getMilliseconds() * 1000;
	},

	_me_weekday: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "weekday() requires a date";
		var d = obj.getDay();
		return d ? d-1 : 6;
	},

	_isleap: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "isleap() requires a date";
		return new Date(obj.getFullYear(), 1, 29).getMonth() === 1;
	},

	_me_yearday: function(obj)
	{
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

	// Color methods
	_me_r: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "r() requires a color";
		return obj.r;
	},

	_me_g: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "g() requires a color";
		return obj.g;
	},

	_me_b: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "b() requires a color";
		return obj.b;
	},

	_me_a: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "a() requires a color";
		return obj.a;
	},

	_me_lum: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "lum() requires a color";
		return obj.lum();
	},

	_me_hls: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hls() requires a color";
		return obj.hls();
	},

	_me_hlsa: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hlsa() requires a color";
		return obj.hlsa();
	},

	_me_hsv: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hsv() requires a color";
		return obj.hsv();
	},

	_me_hsva: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hsva() requires a color";
		return obj.hsva();
	},

	_me_witha: function(obj, newa)
	{
		if (!this._fu_iscolor(obj))
			throw "witha() requires a color";
		return obj.witha(newa);
	},

	_me_withlum: function(obj, newlum)
	{
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
			c.r = r;
			c.g = g;
			c.b = b;
			c.a = a;
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

	InterpretedTemplate_old_unused_deleteme: {
		__istemplate__: true,
		version: "16",

		// A class for reading a template object from a string containing the template in binary format
		_reader: {
			// Creates a new reader for reading from the string ``data``
			create: function(data)
			{
				var reader = ul4._clone(this);
				reader.data = data;
				reader.pos = 0;
				return reader;
			},

			// Read a line from buffer
			readline: function()
			{
				var s = "";
				for (;;)
				{
					var c = this.data.charAt(this.pos++);
					s += c;
					if (!c || (c === "\n"))
						return s;
				}
			},

			// Read a character from the buffer
			readchar: function()
			{
				return this.data.charAt(this.pos++);
			},

			// Read a character from the buffer and ensure that it is a carriage return
			readcr: function()
			{
				var c = this.readchar();
				if (c !== "\n")
					throw "invalid linefeed " + ul4._fu_repr(c) + " at position " + this.pos;
			},

			// Read a character from the buffer and ensure that it is '|'
			readsep: function()
			{
				var c = this.readchar();
				if (c !== "|")
					throw "invalid separator, expected " + ul4._fu_repr("|") + ", got " + ul4._fu_repr(c) + " at position " + this.pos;
			},

			// Read an integer from the buffer (prefixed with ``prefix`` (if ``prefix`` is not ``null``))
			readint: function(prefix)
			{
				if (prefix !== null)
				{
					var c = this.data.substr(this.pos, prefix.length);
					this.pos += prefix.length;
					if (c != prefix)
						throw "invalid prefix, expected " + ul4._fu_repr(prefix) + ", got " + ul4._fu_repr(c) + " at position " + this.pos;
				}
				var i = null;
				for (;;)
				{
					var c = this.readchar();
					if (c === "|")
						return i;
					var cc = c.charCodeAt(0);
					if ((cc >= 48) && (cc <= 57))
					{
						if (i === null)
							i = 0;
						i = 10*i + (cc-48);
					}
					else
						throw "invalid separator, expected " + ul4._fu_repr("|") + ", got " + ul4._fu_repr(c) + " at position " + this.pos;
				}
			},

			// Read a string from the buffer (prefixed with ``prefix`` (if ``prefix`` is not ``null``))
			readstr: function(prefix)
			{
				if (prefix !== null)
				{
					var c = this.data.substr(this.pos, prefix.length);
					this.pos += prefix.length;
					if (c !== prefix)
						throw "invalid prefix, expected " + ul4._fu_repr(prefix) + ", got " + ul4._fu_repr(c) + " at position " + this.pos;
				}
				var i = null;
				for (;;)
				{
					var c = this.readchar();
					if (c === "|")
					{
						if (i === null)
							return null;
						break;
					}
					var cc = c.charCodeAt(0);
					if ((cc >= 48) && (cc <= 57))
					{
						if (i === null)
							i = 0;
						i = 10*i + (cc-48);
					}
					else
						throw "invalid separator, expected " + ul4._fu_repr("|") + ", got " + ul4._fu_repr(c) + " at position " + this.pos;
				}
				var result = this.data.substr(this.pos, i);
				this.pos += i;
				if (result.length !== i)
					throw "short read";
				this.readsep();
				return result;
			}
		},

		// Create a new sub template object from ``this`` for the opcodes starting at the index ``start`` and ending at the index ``stop-1`` the the opcodes in ``this``
		createinner: function(start, stop)
		{
			var template = ul4._clone(this);
			// The attributes ``startdelim``, ``enddelim``, ``source``, and ``opcodes`` will be inherited from this.
			template.name = this.opcodes[start].arg;
			template.startindex = start+1;
			template.stopindex = stop-1;
			template._makefunction();
			return template;
		},

		// A "class method" that returns a new ``Template`` object loaded from the binary format in ``data``
		loads: function(data)
		{
			var template = ul4._clone(this);
			template._data = data;
			var reader = this._reader.create(data);
			var header = reader.readline();
			if (header.trim() != "ul4")
				throw "invalid header, expected " + ul4._fu_repr("ul4") + ", got " + ul4._fu_repr(header) + " at position " + this.pos;
			var version = reader.readline();
			if (version.trim() != this.version)
				throw "invalid version, expected " + ul4._fu_repr(this.version) + ", got " + ul4._fu_repr(header) + " at position " + this.pos;
			template.name = reader.readstr("N");
			var defnames = [ template.name ];
			reader.readcr();
			template.startdelim = reader.readstr("SD");
			reader.readcr();
			template.enddelim = reader.readstr("ED");
			reader.readcr();
			template.source = reader.readstr("SRC");
			reader.readcr();
			template.opcodes = [];
			var opcodecount = reader.readint("n");
			reader.readcr();

			var location = null;
			while (opcodecount--)
			{
				var r1 = reader.readint(null);
				var r2 = reader.readint(null);
				var r3 = reader.readint(null);
				var r4 = reader.readint(null);
				var r5 = reader.readint(null);
				var code = reader.readstr("C");
				var arg = reader.readstr("A");
				var locspec = reader.readchar();
				if (locspec === "^")
				{
					if (location === null)
						throw "no previous location at position" + reader.pos;
				}
				else if (locspec === "*")
				{
					reader.readsep();
					location = {
						source: template.source,
						name: defnames[defnames.length-1],
						type: reader.readstr("T"),
						starttag: reader.readint("st"),
						endtag: reader.readint("et"),
						startcode: reader.readint("sc"),
						endcode: reader.readint("ec")
					};
				}
				else
					throw "invalid location spec " + ul4._fu_repr(locspec) + " at position " + reader.pos;
				reader.readcr();
				template.opcodes.push({code: code, r1: r1, r2: r2, r3: r3, r4: r4, r5: r5, arg: arg, location: location});
				if (code === "def")
					defnames.push(arg);
				else if (code === "enddef")
					defnames.pop();
			}
			template.startindex = 0;
			template.stopindex = template.opcodes.length;
			template._makefunction();
			return template;
		},

		// A class for converting a template object into binary format
		_writer: {
			// Create a new writer object
			create: function()
			{
				var writer = ul4._clone(this);
				writer.data = [];
				return writer;
			},

			// Write the string ``string`` to the buffer
			write: function(string)
			{
				if (string !== null)
					this.data.push(string);
			},

			// Write the number ``number`` to the buffer (prefixed with ``prefix`` if it is not ``null``)
			writeint: function(prefix, number)
			{
				if (prefix !== null)
					this.data.push(prefix);
				if (number !== null)
					this.data.push("" + number);
				this.data.push("|");
			},

			// Write the string ``string`` to the buffer (prefixed with ``prefix`` if it is not ``null``)
			writestr: function(prefix, string)
			{
				this.data.push(prefix);
				if (string !== null)
				{
					this.data.push("" + string.length);
					this.data.push("|");
					this.data.push(string);
				}
				this.data.push("|");
			},

			// Returned the complete string written to the buffer
			finish: function()
			{
				return this.data.join("");
			}
		},

		// Return the binary format for the ``Template`` object ``this``
		dumps: function()
		{
			var writer = this._writer.create();

			var startpos = this.opcodes[this.startindex].location.starttag;
			var stoppos = this.opcodes[this.stopindex-1].location.endtag;

			writer.write("ul4\n");
			writer.write(this.version + "\n");
			writer.writestr("N", this.name);
			writer.write("\n");
			writer.writestr("SD", this.startdelim);
			writer.write("\n");
			writer.writestr("ED", this.enddelim);
			writer.write("\n");
			writer.writestr("SRC", this.source.substring(startpos, stoppos));
			writer.write("\n");
			writer.writeint("n", this.stopindex-this.startindex);
			writer.write("\n");
			var lastlocation = null;
			for (var i = this.startindex; i < this.stopindex; ++i)
			{
				var opcode = this.opcodes[i];
				writer.writeint(null, opcode.r1);
				writer.writeint(null, opcode.r2);
				writer.writeint(null, opcode.r3);
				writer.writeint(null, opcode.r4);
				writer.writeint(null, opcode.r5);
				writer.writestr("C", opcode.code);
				writer.writestr("A", opcode.arg);
				if (opcode.location !== lastlocation)
				{
					lastlocation = opcode.location;
					writer.write("*|");
					writer.writestr("T", lastlocation.type);
					writer.writeint("st", lastlocation.starttag-startpos);
					writer.writeint("et", lastlocation.endtag-startpos);
					writer.writeint("sc", lastlocation.startcode-ostartpos);
					writer.writeint("ec", lastlocation.endcode-startpos);
				}
				else
					writer.write("^");
				writer.write("\n");
			}
			return writer.finish();
		},

		// Render the template ``this`` using ``vars`` as the template variables and return the rendered string
		renders: function(vars)
		{
			return this.render(vars).join("");
		},

		// Render the template ``this`` using ``vars`` as the template variables and return the the output as a string array
		render: function(vars)
		{
			if (typeof(vars) == "undefined")
				vars = {};
			return this._jsfunction(vars);
		},

		// Convert the template to Javascript source code, create a function for it and attach it to the ``_jsfunction`` attribute
		_makefunction: function()
		{
			var lines = [];
			var indent = 0;
			var opendefs = []; // currently active nested inner templates (i.e. the index of their def opcode)
			var loopvarcounter = 0;

			var startpos = this.opcodes[this.startindex].location.starttag;
			var stoppos = this.opcodes[this.stopindex-1].location.endtag;

			function line(source)
			{
				for (var i = 0; i < indent; ++i)
					lines.push("\t");
				lines.push(source);
				lines.push("\n");
			}

			line("(function(vars)");
			line("{");
			indent++;

			// Include template source as a comment
			line("//@@@ BEGIN template source");
			var sourcelines = this.source.substring(startpos, stoppos).split("\n");
			var width = ("" + (sourcelines.length+1)).length;
			for (var i = 0; i < sourcelines.length; ++i)
				line("// " + ul4._lpad(""+(i+1), " ", width) + ": " + sourcelines[i]);

			// Initialize output buffer and registers
			line("//@@@ BEGIN template code");
			line("var out = [];");
			line("var r0 = null, r1 = null, r2 = null, r3 = null, r4 = null, r5 = null, r6 = null, r7 = null, r8 = null, r9 = null;");

			var lastloc = null;

			// Loop over opcodes
			for (var i = this.startindex; i < this.stopindex; ++i)
			{
				var opcode = this.opcodes[i];

				if (opcode.code === "def")
				{
					// Remember where the subtemplate started and its name
					opendefs.push({index: i, name: opcode.arg});
				}
				else if (opcode.code === "enddef")
				{
					var def = opendefs.pop();
					// Have we returned to the outermost nesting level?
					if (!opendefs.length)
					{
						line("// <?def?>/<?end def?> tags at positions " + (this.opcodes[def.index].location.starttag-startpos) + ":" + (opcode.location.endtag-startpos) + " (template " + this.name + ")");
						// Create a template from the opcodes between the matching ``def`` and ``enddef`` opcodes
						line("vars[" + ul4._fu_json(def.name) + "] = this.createinner(" + def.index + ", " + (i+1) + ");");
					}
				}
				else if (!opendefs.length) // only produce source code for the outermost level of template nesting
				{
					// Opcode is from a new tag -> show the location as a comment
					if (opcode.code !== null && opcode.location != lastloc)
					{
						lastloc = opcode.location;

						var s = lastloc.source.substring(lastloc.starttag, lastloc.endtag);
						s = ul4._fu_repr(s);
						s = s.substring(1, s.length-1);
						line("// <?" + lastloc.type + "?> tag at positions " + (lastloc.starttag-startpos) + ":" + (lastloc.endtag-startpos) + " (template " + this.name + "): " + s);
					}

					// Output Javascript code for opcode
					switch (opcode.code)
					{
						case null:
							line("out.push(" + ul4._fu_json(opcode.location.source.substring(opcode.location.startcode, opcode.location.endcode)) + ");");
							break;
						case "loadstr":
							line("r" + opcode.r1 + " = " + ul4._fu_json(opcode.arg) + ";");
							break;
						case "loadint":
						case "loadfloat":
							line("r" + opcode.r1 + " = " + opcode.arg + ";");
							break;
						case "loadnone":
							line("r" + opcode.r1 + " = null;");
							break;
						case "loadfalse":
							line("r" + opcode.r1 + " = false;");
							break;
						case "loadtrue":
							line("r" + opcode.r1 + " = true;");
							break;
						case "loaddate":
							var args = opcode.arg.split(/[-:T.]/);
							line("r" + opcode.r1 + " = new Date(" + parseInt(args[0]) + ", " + (parseInt(args[1])-1) + ", " + parseInt(args[2]) + ", " + parseInt(args[3]) + ", " + parseInt(args[4]) + ", " + parseInt(args[5]) + ", " + (parseInt(args[6])/1000) + ");");
							break;
						case "loadcolor":
							line("r" + opcode.r1 + " = ul4.Color.create(0x" + opcode.arg.substring(0, 2) + ", 0x" + opcode.arg.substring(2, 4) + ", 0x" + opcode.arg.substring(4, 6) + ", 0x" + opcode.arg.substring(6, 8) + ");");
							break;
						case "buildlist":
							line("r" + opcode.r1 + " = [];");
							break;
						case "builddict":
							line("r" + opcode.r1 + " = {};");
							break;
						case "addlist":
							line("r" + opcode.r1 + ".push(r" + opcode.r2 + ");");
							break;
						case "adddict":
							line("r" + opcode.r1 + "[r" + opcode.r2 + "] = r" + opcode.r3 + ";");
							break;
						case "updatedict":
							line("for (var key in r" + opcode.r2 + ")");
							indent++;
							line("r" + opcode.r1 + "[key] = r" + opcode.r2 + "[key];");
							indent--;
							break;
						case "loadvar":
							line("r" + opcode.r1 + " = ul4._op_getitem(vars, " + ul4._fu_json(opcode.arg) + ");");
							break;
						case "storevar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = r" + opcode.r1 + ";");
							break;
						case "addvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_add(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "subvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_sub(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "mulvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_mul(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "truedivvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_truediv(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "floordivvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_floordiv(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "modvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = ul4._op_mod(vars[" + ul4._fu_json(opcode.arg) + "], r" + opcode.r1 + ");");
							break;
						case "delvar":
							line("vars[" + ul4._fu_json(opcode.arg) + "] = undefined;");
							break;
						case "getattr":
							line("r" + opcode.r1 + " = ul4._op_getitem(r" + opcode.r2 + ", " + ul4._fu_json(opcode.arg) + ");");
							break;
						case "getitem":
							line("r" + opcode.r1 + " = ul4._op_getitem(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "getslice12":
							line("r" + opcode.r1 + " = ul4._op_getslice(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ");");
							break;
						case "getslice1":
							line("r" + opcode.r1 + " = ul4._op_getslice(r" + opcode.r2 + ", r" + opcode.r3 + ", null);");
							break;
						case "getslice2":
							line("r" + opcode.r1 + " = ul4._op_getslice(r" + opcode.r2 + ", null, r" + opcode.r3 + ");");
							break;
						case "getslice":
							line("r" + opcode.r1 + " = ul4._op_getslice(r" + opcode.r2 + ", null, null);");
							break;
						case "print":
							line("out.push(ul4._fu_str(r" + opcode.r1 + "));");
							break;
						case "printx":
							line("out.push(ul4._fu_xmlescape(r" + opcode.r1 + "));");
							break;
						case "for":
							loopvarcounter++;
							line("for (var iter" + loopvarcounter + " = ul4._iter(r" + opcode.r2 + ");;)");
							line("{");
							indent++;
							line("r" + opcode.r1 + " = iter" + loopvarcounter + "();");
							line("if (r" + opcode.r1 + " === null)");
							indent++;
							line("break;");
							indent--;
							line("r" + opcode.r1 + " = r" + opcode.r1 + "[0];");
							break;
						case "endfor":
							indent--;
							line("}");
							break;
						// ``def`` and ``enddef`` opcodes are handled outside the switch statement
						// case "def":
						// case "enddef":
						case "break":
							line("break;");
							break;
						case "continue":
							line("continue;");
							break;
						case "not":
							line("r" + opcode.r1 + " = !ul4._fu_bool(r" + opcode.r2 + ");");
							break;
						case "neg":
							line("r" + opcode.r1 + " = ul4._op_neg(r" + opcode.r2 + ");");
							break;
						case "contains":
							line("r" + opcode.r1 + " = ul4._op_contains(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "notcontains":
							line("r" + opcode.r1 + " = !ul4._op_contains(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "eq":
							line("r" + opcode.r1 + " = ul4._op_eq(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "ne":
							line("r" + opcode.r1 + " = !ul4._op_eq(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "lt":
							line("r" + opcode.r1 + " = ul4._op_lt(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "le":
							line("r" + opcode.r1 + " = ul4._op_le(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "gt":
							line("r" + opcode.r1 + " = !ul4._op_le(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "ge":
							line("r" + opcode.r1 + " = !ul4._op_lt(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "add":
							line("r" + opcode.r1 + " = ul4._op_add(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "sub":
							line("r" + opcode.r1 + " = ul4._op_sub(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "mul":
							line("r" + opcode.r1 + " = ul4._op_mul(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "floordiv":
							line("r" + opcode.r1 + " = ul4._op_floordiv(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "truediv":
							line("r" + opcode.r1 + " = ul4._op_truediv(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "mod":
							line("r" + opcode.r1 + " = ul4._op_mod(r" + opcode.r2 + ", r" + opcode.r3 + ");");
							break;
						case "and":
							line("r" + opcode.r1 + " = ul4._fu_bool(r" + opcode.r3 + ") ? r" + opcode.r2 + " : r" + opcode.r3 + ");");
							break;
						case "or":
							line("r" + opcode.r1 + " = ul4._fu_bool(r" + opcode.r2 + ") ? r" + opcode.r2 + " : r" + opcode.r3 + ");");
							break;
						case "callfunc0":
							switch (opcode.arg)
							{
								case "now":
									line("r" + opcode.r1 + " = new Date();");
									break;
								case "utcnow":
									line("r" + opcode.r1 + " = ul4._fu_utcnow();");
									break;
								case "random":
									line("r" + opcode.r1 + " = Math.random();");
									break;
								case "vars":
									line("r" + opcode.r1 + " = vars;");
									break;
								default:
									throw "function named " + opcode.arg + " unknown";
							}
							break;
						case "callfunc1":
							switch (opcode.arg)
							{
								case "xmlescape":
								case "csv":
								case "repr":
								case "enumerate":
								case "chr":
								case "ord":
								case "hex":
								case "oct":
								case "bin":
								case "sorted":
								case "type":
								case "json":
								case "reversed":
								case "randchoice":
								case "str":
								case "int":
								case "float":
								case "bool":
								case "len":
								case "isstr":
								case "isint":
								case "isfloat":
								case "isbool":
								case "isdate":
								case "islist":
								case "isdict":
								case "istemplate":
								case "iscolor":
								case "abs":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ");");
									break;
								case "range":
								case "randrange":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(0, r" + opcode.r2 + ", 1);");
									break;
								case "isnone":
									line("r" + opcode.r1 + " = (r" + opcode.r2 + " === null);");
									break;
								case "get":
									line("r" + opcode.r1 + " = ul4._me_get(vars, r" + opcode.r2 + ");");
									break;
								default:
									throw "function named " + opcode.arg + " unknown";
							}
							break;
						case "callfunc2":
							switch (opcode.arg)
							{
								case "format":
								case "zip":
								case "int":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ");");
									break;
								case "range":
								case "randrange":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", 1);");
									break;
								case "get":
									line("r" + opcode.r1 + " = ul4._me_get(vars, r" + opcode.r2 + ", r" + opcode.r3 + ");");
									break;
								default:
									throw "function named " + opcode.arg + " unknown";
							}
							break;
						case "callfunc3":
							switch (opcode.arg)
							{
								case "range":
								case "zip":
								case "randrange":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ");");
									break;
								case "rgb":
								case "hls":
								case "hsv":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ", 1.0);");
									break;
								default:
									throw "function named " + opcode.arg + " unknown";
							}
							break;
						case "callfunc4":
							switch (opcode.arg)
							{
								case "rgb":
								case "hls":
								case "hsv":
									line("r" + opcode.r1 + " = ul4._fu_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ", r" + opcode.r5 + ");");
									break;
								default:
									throw "function named " + opcode.arg + " unknown";
							}
							break;
						case "callmeth0":
							switch (opcode.arg)
							{
								case "strip":
								case "lstrip":
								case "rstrip":
								case "upper":
								case "lower":
								case "capitalize":
								case "items":
								case "isoformat":
								case "mimeformat":
								case "day":
								case "month":
								case "year":
								case "hour":
								case "minute":
								case "second":
								case "microsecond":
								case "weekday":
								case "yearday":
								case "r":
								case "g":
								case "b":
								case "a":
								case "lum":
								case "hls":
								case "hlsa":
								case "hsv":
								case "hsva":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ");");
									break;
								case "split":
								case "rsplit":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", null, null);");
									break;
								case "render":
									line("r" + opcode.r1 + " = " + opcode.r2 + ".renders({});");
									break;
								default:
									throw "method named " + opcode.arg + " unknown";
							}
							break;
						case "callmeth1":
							switch (opcode.arg)
							{
								case "join":
								case "strip":
								case "lstrip":
								case "rstrip":
								case "startswith":
								case "endswith":
								case "withlum":
								case "witha":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ");");
									break;
								case "split":
								case "rsplit":
								case "get":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", null);");
									break;
								case "find":
								case "rfind":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", null, null);");
									break;
								default:
									throw "method named " + opcode.arg + " unknown";
							}
							break;
						case "callmeth2":
							switch (opcode.arg)
							{
								case "split":
								case "rsplit":
								case "replace":
								case "get":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ");");
									break;
								case "find":
								case "rfind":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ", null);");
									break;
								default:
									throw "method named " + opcode.arg + " unknown";
							}
							break;
						case "callmeth3":
							switch (opcode.arg)
							{
								case "find":
								case "rfind":
									line("r" + opcode.r1 + " = ul4._me_" + opcode.arg + "(r" + opcode.r2 + ", r" + opcode.r3 + ", r" + opcode.r4 + ", r" + opcode.r5 + ");");
									break;
								default:
									throw "method named " + opcode.arg + " unknown";
							}
							break;
						case "callmethkw":
							switch (opcode.arg)
							{
								case "render":
									line("r" + opcode.r1 + " = r" + opcode.r2 + ".renders(r" + opcode.r3 + ");");
									break;
								default:
									throw "method named " + opcode.arg + " unknown";
							}
							break;
						case "if":
							line("if (ul4._fu_bool(r" + opcode.r1 + "))");
							line("{");
							indent++;
							break;
						case "else":
							indent--;
							line("}");
							line("else");
							line("{");
							indent++;
							break;
						case "end if":
							indent--;
							line("}");
							break;
						case "render":
							line("out = out.concat(r" + opcode.r1 + ".render(r" + opcode.r2 + "));");
							break;
						default:
							throw "opcode named " + opcode.type + " unknown";
					}
				}
			}

			// Return completed output
			line("return out;");
			line("//@@@ END template code");

			indent--;
			line("})");
			this._jsfunction = eval(lines.join(""));
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
			return (typeof(ob) === "undefined") ? result : obj;
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
		toString: function()
		{
			return this.format(0);
		},
		ul4ondump: function(encoder)
		{
			encoder.dump(this.location);
		},
		ul4onload: function(decoder)
		{
			this.location = decoder.load();
		},
		// used in ``format``/``_formatop`` to decide if we need brackets around an operator
		precedence: null,
		associative: true
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
			return this._line(indent, "output.push(" + ul4._fu_json(this.text()) + ");");
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.value);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.value = decoder.load();
		},
		formatjs: function(indent)
		{
			return ul4._fu_json(this.value);
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
			list.content = [];
			return list;
		},
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.content);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.content = decoder.load();
		},
		formatjs: function(indent)
		{
			var v= [];
			for (var i in this.content)
				v.push(this.content[i].formatjs(indent));
			return "[" + v.join(", ") + "]";
		},
		format: function(indent)
		{
			var v= [];
			for (var i in this.content)
				v.push(this.content[i].format(indent));
			return "[" + v.join(", ") + "]";
		},
		precedence: 11
	}
);

ul4.LoadVar = ul4._inherit(
	ul4.AST,
	{
		create: function(location, varname)
		{
			var variable = ul4.AST.create.call(this, location);
			variable.varname = varname;
			return variable;
		},
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.varname);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.varname = decoder.load();
		},
		formatjs: function(indent)
		{
			return "vars[" + ul4._fu_json(this.varname) + "]";
		},
		format: function(indent)
		{
			return this.varname;
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.obj);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.obj = decoder.load();
		},
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
			return this._line(indent, "output.push(ul4._fu_str(" + this.obj.formatjs(indent) + "));");
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
			return this._line(indent, "output.push(ul4._fu_xmlescape(" + this.obj.formatjs(indent) + "));");
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.obj1);
			encoder.dump(this.obj2);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.obj1 = decoder.load();
			this.obj2 = decoder.load();
		},
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.obj);
			encoder.dump(this.attrname);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.obj = decoder.load();
			this.attrname = decoder.load();
		},
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.funcname);
			encoder.dump(this.args);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.funcname = decoder.load();
			this.args = decoder.load();
		},
		formatjs: function(indent)
		{
			if (this.funcname === "vars")
				return "vars";
			var v = [];
			for (var i in this.args)
				v.push(this.args[i].formatjs(indent));
			return "ul4._fu_" + this.funcname + "(" + v.join(", ") + ")";
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.methname);
			encoder.dump(this.obj);
			encoder.dump(this.args);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.methname = decoder.load();
			this.obj = decoder.load();
			this.args = decoder.load();
		},
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.varname);
			encoder.dump(this.value);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.varname = decoder.load();
			this.value = decoder.load();
		}
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
			return this._line(indent, "vars[" + ul4._fu_json(this.varname) + "] = " + this.value.formatjs(indent) + ";");
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
			var varname = ul4._fu_json(this.varname);
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
			var varname = ul4._fu_json(this.varname);
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
			var varname = ul4._fu_json(this.varname);
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
			var varname = ul4._fu_json(this.varname);
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
			var varname = ul4._fu_json(this.varname);
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
			var varname = ul4._fu_json(this.varname);
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
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.varname);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.varname = decoder.load();
		},
		format: function(indent)
		{
			return this._line(indent, "del " + this.varname);
		},
		formatjs: function(indent)
		{
			return this._line(indent, "vars[" + ul4._fu_json(this.varname) + "] = null;");
		}
	}
);

ul4.Block = ul4._inherit(
	ul4.AST,
	{
		create: function(location)
		{
			var block = ul4.AST.create.call(this, location);
			block.content = [];
			return block;
		},
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.content);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.content = decoder.load();
		}
	}
);

ul4.Block = ul4._inherit(
	ul4.AST,
	{
		create: function(location)
		{
			var block = ul4.AST.create.call(this, location);
			block.content = [];
			return block;
		},
		ul4ondump: function(encoder)
		{
			ul4.AST.ul4ondump.call(this, encoder);
			encoder.dump(this.content);
		},
		ul4onload: function(decoder)
		{
			ul4.AST.ul4onload.call(this, decoder);
			this.content = decoder.load();
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
		ul4ondump: function(encoder)
		{
			ul4.Block.ul4ondump.call(this, encoder);
			encoder.dump(this.container);
			encoder.dump(this.varname);
		},
		ul4onload: function(decoder)
		{
			ul4.Block.ul4onload.call(this, decoder);
			this.container = decoder.load();
			this.varname = decoder.load();
		},
		formatjs: function(indent)
		{
			var v = [];
			v.push(this._line(indent, "for (var iter" + this.__id__ + " = ul4._iter(" + this.container.formatjs(indent) + ");;)"));
			v.push(this._line(indent, "{"));
			++indent;
			v.push(this._line(indent, "var item" + this.__id__ + " = iter" + this.__id__ + "();"));
			v.push(this._line(indent, "if (item" + this.__id__ + " === null)"));
			v.push(this._line(indent+1, "break;"));
			v.push(this._line(indent, "vars[" + ul4._fu_json(this.varname) + "] = item" + this.__id__ + "[0];"));
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
		ul4ondump: function(encoder)
		{
			ul4.Block.ul4ondump.call(this, encoder);
			encoder.dump(this.container);
			encoder.dump(this.varnames);
		},
		ul4onload: function(decoder)
		{
			ul4.Block.ul4onload.call(this, decoder);
			this.container = decoder.load();
			this.varnames = decoder.load();
		},
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
				v.push(this._line(indent, "vars[" + ul4._fu_json(this.varnames[i]) + "] = items" + this.__id__ + "[" + i + "];"));
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
		ul4ondump: function(encoder)
		{
			ul4.Block.ul4ondump.call(this, encoder);
			encoder.dump(this.condition);
		},
		ul4onload: function(decoder)
		{
			ul4.Block.ul4onload.call(this, decoder);
			this.condition = decoder.load();
		},
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
			template.source = source;
			template.name = name;
			template.startdelim = startdelim;
			template.enddelim = enddelim;
			template._function = null;
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
			var v = [];
			v.push(this._line(indent, "vars[" + ul4._fu_json(this.name) + "] = function(vars)"));
			v.push(this._line(indent, "{"));
			v.push(this._line(indent+1, "var stack = ul4.Stack.create();"));
			v.push(this._line(indent+1, "var output = [];"));
			v.push(this._formatjs_content(indent+1));
			v.push(this._line(indent, "};"));
			return v.join("");
		},
		format: function(indent)
		{
			return this._line(indent, "def " + (this.name !== null ? this.name : "unnamed")) + ul4.Block.format.call(this, indent);
		},
		_makefunction: function()
		{
			var v = [];
			v.push(this._line(0, "(function(vars)"));
			v.push(this._line(0, "{"));
			v.push(this._line(1, "var stack = ul4.Stack.create();"));
			v.push(this._line(1, "var output = [];"));
			v.push(this._formatjs_content(1));
			v.push(this._line(1, "return output;"));
			v.push(this._line(0, "})"));
			var source = v.join("");
			return eval(source);
		},
		render: function(vars)
		{
			vars = vars || {};
			if (this._function === null)
				this._function = this._makefunction();
			return this._function(vars);
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

ul4on.register("de.livinglogic.ul4.location", ul4.Location);
ul4on.register("de.livinglogic.ul4.text", ul4.Text);
ul4on.register("de.livinglogic.ul4.null", ul4.LoadNone);
ul4on.register("de.livinglogic.ul4.false", ul4.LoadFalse);
ul4on.register("de.livinglogic.ul4.true", ul4.LoadTrue);
ul4on.register("de.livinglogic.ul4.int", ul4.LoadInt);
ul4on.register("de.livinglogic.ul4.float", ul4.LoadFloat);
ul4on.register("de.livinglogic.ul4.str", ul4.LoadStr);
ul4on.register("de.livinglogic.ul4.color", ul4.LoadColor);
ul4on.register("de.livinglogic.ul4.date", ul4.LoadDate);
ul4on.register("de.livinglogic.ul4.list", ul4.List);
ul4on.register("de.livinglogic.ul4.var", ul4.LoadVar);
ul4on.register("de.livinglogic.ul4.not", ul4.Not);
ul4on.register("de.livinglogic.ul4.neg", ul4.Neg);
ul4on.register("de.livinglogic.ul4.print", ul4.Print);
ul4on.register("de.livinglogic.ul4.printx", ul4.PrintX);
ul4on.register("de.livinglogic.ul4.getitem", ul4.GetItem);
ul4on.register("de.livinglogic.ul4.eq", ul4.EQ);
ul4on.register("de.livinglogic.ul4.ne", ul4.NE);
ul4on.register("de.livinglogic.ul4.lt", ul4.LT);
ul4on.register("de.livinglogic.ul4.le", ul4.LE);
ul4on.register("de.livinglogic.ul4.gt", ul4.GT);
ul4on.register("de.livinglogic.ul4.ge", ul4.GE);
ul4on.register("de.livinglogic.ul4.notcontains", ul4.NotContains);
ul4on.register("de.livinglogic.ul4.contains", ul4.Contains);
ul4on.register("de.livinglogic.ul4.add", ul4.Add);
ul4on.register("de.livinglogic.ul4.sub", ul4.Sub);
ul4on.register("de.livinglogic.ul4.mul", ul4.Mul);
ul4on.register("de.livinglogic.ul4.floordiv", ul4.FloorDiv);
ul4on.register("de.livinglogic.ul4.truediv", ul4.TrueDiv);
ul4on.register("de.livinglogic.ul4.mod", ul4.Mod);
ul4on.register("de.livinglogic.ul4.and", ul4.And);
ul4on.register("de.livinglogic.ul4.or", ul4.Or);
ul4on.register("de.livinglogic.ul4.getattr", ul4.GetAttr);
ul4on.register("de.livinglogic.ul4.callfunc", ul4.CallFunc);
ul4on.register("de.livinglogic.ul4.callmeth", ul4.CallMeth);
ul4on.register("de.livinglogic.ul4.storevar", ul4.StoreVar);
ul4on.register("de.livinglogic.ul4.addvar", ul4.AddVar);
ul4on.register("de.livinglogic.ul4.subvar", ul4.SubVar);
ul4on.register("de.livinglogic.ul4.mulvar", ul4.MulVar);
ul4on.register("de.livinglogic.ul4.truedivvar", ul4.TrueDivVar);
ul4on.register("de.livinglogic.ul4.floordivvar", ul4.FloorDivVar);
ul4on.register("de.livinglogic.ul4.modvar", ul4.ModVar);
ul4on.register("de.livinglogic.ul4.delvar", ul4.DelVar);
ul4on.register("de.livinglogic.ul4.for", ul4.ForNormal);
ul4on.register("de.livinglogic.ul4.foru", ul4.ForUnpack);
ul4on.register("de.livinglogic.ul4.break", ul4.Break);
ul4on.register("de.livinglogic.ul4.continue", ul4.Continue);
ul4on.register("de.livinglogic.ul4.ieie", ul4.IfElIfElse);
ul4on.register("de.livinglogic.ul4.if", ul4.If);
ul4on.register("de.livinglogic.ul4.elif", ul4.ElIf);
ul4on.register("de.livinglogic.ul4.else", ul4.Else);
ul4on.register("de.livinglogic.ul4.template", ul4.Template);
