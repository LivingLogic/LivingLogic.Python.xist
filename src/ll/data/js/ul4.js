var ul4 = {
	// Functions with the ``_op_`` prefix implement UL4 opcodes
	_op_add: function(obj1, obj2)
	{
		return obj1 + obj2;
	},

	_op_sub: function(obj1, obj2)
	{
		return obj1 - obj2;
	},

	_op_mul: function(obj1, obj2)
	{
		if (this._fu_isint(obj1))
		{
			if (typeof(obj2) === "string")
			{
				if (obj1 <= 0)
					throw "mul() repetition counter must be positive";
				return this._str_repeat(obj2, obj1)
			}
			else if (this._fu_islist(obj2))
			{
				if (obj1 <= 0)
					throw "mul() repetition counter must be positive";
				return this._list_repeat(obj2, obj1)
			}
		}
		else if (this._fu_isint(obj2))
		{
			if (typeof(obj1) === "string")
			{
				if (obj2 <= 0)
					throw "mul() repetition counter must be positive";
				return this._str_repeat(obj1, obj2)
			}
			else if (this._fu_islist(obj1))
			{
				if (obj2 <= 0)
					throw "mul() repetition counter must be positive";
				return this._list_repeat(obj1, obj2)
			}
		}
		return obj1 * obj2;
	},

	_op_floordiv: function(obj1, obj2)
	{
		return Math.floor(obj1 / obj2);
	},

	_op_truediv: function(obj1, obj2)
	{
		return obj1 / obj2;
	},

	_op_mod: function(obj1, obj2)
	{
		return obj1 % obj2;
	},

	_op_neg: function(obj)
	{
		return -obj;
	},

	_op_contains: function(obj, container)
	{
		if (typeof(obj) === "string" && typeof(container) === "string")
		{
			return container.indexOf(obj) != -1;
		}
		else if (this._fu_islist(container))
		{
			return container.indexOf(obj) != -1;
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
			return container.r == obj || container.g == obj || container.b == obj || container.a == obj;
		}
		throw "argument of type '" + this._fu_type(container) + "' is not iterable";
	},

	_op_eq: function(obj1, obj2)
	{
		return obj1 === obj2;
	},

	_op_lt: function(obj1, obj2)
	{
		return obj1 < obj2;
	},

	_op_le: function(obj1, obj2)
	{
		return obj1 <= obj2;
	},

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

	_op_getslice: function(container, start, stop)
	{
		if (start === null)
			start = 0;
		if (stop === null)
			stop = container.length;
		return container.slice(start, stop);
	},

	// Functions with the ``_fu_`` prefix implement UL4 functions
	_fu_isnone: function(obj)
	{
		return obj === null;
	},

	_fu_isbool: function(obj)
	{
		return typeof(obj) == "boolean";
	},

	_fu_isint: function(obj)
	{
		return (typeof(obj) == "number") && Math.round(obj) == obj;
	},

	_fu_isfloat: function(obj)
	{
		return (typeof(obj) == "number") && Math.round(obj) != obj;
	},

	_fu_isstr: function(obj)
	{
		return typeof(obj) == "string";
	},

	_fu_isdate: function(obj)
	{
		return Object.prototype.toString.call(obj) == "[object Date]";
	},

	_fu_iscolor: function(obj)
	{
		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__iscolor__;
	},

	_fu_istemplate: function(obj)
	{
		return Object.prototype.toString.call(obj) == "[object Object]" && !!obj.__istemplate__;
	},

	_fu_islist: function(obj)
	{
		return Object.prototype.toString.call(obj) == "[object Array]";
	},

	_fu_isdict: function(obj)
	{
		return Object.prototype.toString.call(obj) == "[object Object]" && !obj.__iscolor__ && !obj.__istemplate__;
	},

	_fu_bool: function(obj)
	{
		if (obj === null || obj === false || obj === 0 || obj === "")
			return false;
		else
		{
			if (this._fu_islist(obj))
				return obj.length != 0;
			else if (this._fu_isdict(obj))
			{
				for (var key in obj)
					return true;
				return false;
			}
			return true;
		}
	},

	_fu_rgb: function(r, g, b, a)
	{
		return this.Color.create(255*r, 255*g, 255*b, typeof(a) == "undefined" ? 0xff : (255*a));
	},

	_fu_type: function(obj)
	{
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

	_fu_str: function(obj)
	{
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
			return this._date_repr(obj);
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

	_fu_int: function(obj, base)
	{
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

	_fu_float: function(obj)
	{
		if (typeof(obj) == "string")
			return parseFloat(obj);
		else if (typeof(obj) == "number")
			return obj;
		else if (obj === true)
			return 1.;
		else if (obj === false)
			return 0.;
		throw "float() argument must be a string or a number";
	},

	_fu_list: function(obj)
	{
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

	_fu_len: function(obj)
	{
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

	_fu_repr: function(obj)
	{
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
			for (var i in obj)
			{
				if (i != 0)
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

	_fu_xmlescape: function(obj)
	{
		obj = this._fu_str(obj);
		obj = obj.replace(/&/g, "&amp;");
		obj = obj.replace(/</g, "&lt;");
		obj = obj.replace(/>/g, "&gt;");
		obj = obj.replace(/'/g, "&#39;");
		obj = obj.replace(/"/g, "&quot;");
		return obj;
	},

	_fu_csv: function(obj)
	{
		if (obj === null)
			return "";
		else if (typeof(obj) !== "string")
			obj = this._fu_repr(obj);
		if (obj.indexOf(",") !== -1 || obj.indexOf('"') !== -1 || obj.indexOf("\n") !== -1)
			obj = '"' + obj.replace(/"/g, '""') + '"';
		return obj;
	},

	_fu_chr: function(obj)
	{
		if (typeof(obj) != "number")
			throw "chr() requires an int";
		return String.fromCharCode(obj)
	},

	_fu_ord: function(obj)
	{
		if (typeof(obj) != "string" || obj.length != 1)
			throw "ord() requires a string of length 1";
		return obj.charCodeAt(0);
	},

	_fu_hex: function(obj)
	{
		if (typeof(obj) != "number")
			throw "hex() requires an int";
		if (obj < 0)
			return "-0x" + obj.toString(16).substr(1);
		else
			return "0x" + obj.toString(16);
	},

	_fu_oct: function(obj)
	{
		if (typeof(obj) != "number")
			throw "oct() requires an int";
		if (obj < 0)
			return "-0o" + obj.toString(8).substr(1);
		else
			return "0o" + obj.toString(8);
	},

	_fu_bin: function(obj)
	{
		if (typeof(obj) != "number")
			throw "bin() requires an int";
		if (obj < 0)
			return "-0b" + obj.toString(2).substr(1);
		else
			return "0b" + obj.toString(2);
	},

	_fu_sorted: function(obj)
	{
		var result = this._fu_list(obj);
		result.sort();
		return result;
	},

	_fu_range: function(start, stop, step)
	{
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
		}
		result.__iter__ = true;
		return result;
	},

	_fu_json: function(obj)
	{
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
				if (i != 0)
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
			return "ul4._fu_rgb(" + obj.r + ", " + obj.g + ", " + obj.b + ", " + obj.a + ")";
		}
		else if (this.istemplate(obj))
		{
			return "ul4.Template.create(" + obj.render.toString() + ")";
		}
		throw "json() requires a serializable object";
	},

	_fu_reversed: function(obj)
	{
		if (typeof(obj) != "string" && !this._fu_islist(obj)) // We don't have to materialize strings or lists
			obj = this._fu_list(obj);
		var i = obj.length-1;
		var result = function()
		{
			return i >= 0 ? [obj[i--]] : null;
		}
		result.__iter__ = true;
		return result;
	},

	_fu_randrange: function(start, stop, step)
	{
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

	_fu_randchoice: function(obj)
	{
		var iscolor = this._fu_iscolor(obj);
		if (typeof(obj) !== "string" && !this._fu_islist(obj) && !iscolor)
			throw "randchoice() requires a string or list";
		if (iscolor)
			obj = this._fu_list(obj);
		return obj[Math.floor(Math.random() * obj.length)];
	},

	_fu_enumerate: function(obj)
	{
		var iter = this._iter(obj);
		var i = 0;
		var result = function()
		{
			var inner = iter();
			return inner !== null ? [[i++, inner[0]]] : null;
		}
		result.__iter__ = true;
		return result;
	},

	_fu_zip: function()
	{
		var iters = [];
		for (var i = 0; i < arguments.length; ++i)
			iters.push(this._iter(arguments[i]));

		var result = function()
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
		}
		result.__iter__ = true;
		return result;
	},

	_fu_abs: function(obj)
	{
		return Math.abs(obj);
	},

	_fu_utcnow: function()
	{
		var now = new Date();
		// FIXME: The timezone is wrong for the new ``Date`` object.
		return new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
	},

	_fu_hls: function(h, l, s, a)
	{
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
		if (s == 0.0)
		    return this._fu_rgb(l, l, l, a);
		if (l <= 0.5)
		    m2 = l * (1.0+s);
		else
		    m2 = l+s-(l*s);
		m1 = 2.0*l - m2;
		return this._fu_rgb(_v(m1, m2, h+1/3), _v(m1, m2, h), _v(m1, m2, h-1/3), a);
	},

	_fu_hsv: function(h, s, v, a)
	{
		if (typeof(a) === "undefined")
			a = 1;
		if (s == 0.0)
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

	_me_format: function(obj, format)
	{
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
							c = Math.floor((this._me_yearday(obj) + firstday - 1) / 7);
							break;
						case "w":
							c = obj.getDay();
							break;
						case "W":
							firstday = (new Date(obj.getFullYear(), 0, 1).getDay());
							firstday = firstday ? firstday-1 : 6;
							c = Math.floor((this._me_yearday(obj) + firstday - 1) / 7);
							break;
						case "x":
							c = this._lpad(obj.getMonth() + 1, "0", 2) + "/" + this._lpad(obj.getDate(), "0", 2) + "/" + this._lpad(obj.getFullYear() % 100, "0", 2);
							break;
						case "X":
							c = this._lpad(obj.getHours(), "0", 2) + "/" + this._lpad(obj.getMinutes(), "0", 2) + "/" + this._lpad(obj.getSeconds(), "0", 2);
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
			var r = this.r/255.;
			var g = this.g/255.;
			var b = this.b/255.;
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
			return hls.concat(this.a/255.);
		},

		hsv: function()
		{
			var r = this.r/255.;
			var g = this.g/255.;
			var b = this.b/255.;
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
			return hsv.concat(this.a/255.);
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


	Template: {
		__istemplate__: true,

		create: function(render)
		{
			var template = ul4._clone(this);
			template.render = render;
			return template;
		},

		renders: function(vars)
		{
			return this.render(vars).join("");
		}
	},

		/// Helper functions

	// Crockford style object creation
	_clone: function(obj)
	{
		function F(){};
		F.prototype = obj;
		var result = new F();
		return result;
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
			}
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
			}
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
		var result = "@" + year + "-" + this._lpad(month.toString(), "0", 2) + "-" + this._lpad(day.toString(), "0", 2) + "T";

		if (hour || minute || second || ms)
		{
			result += this._lpad(hour.toString(), "0", 2) + ":" + this._lpad(minute.toString(), "0", 2) + ":" + this._lpad(second.toString(), "0", 2);
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
}
