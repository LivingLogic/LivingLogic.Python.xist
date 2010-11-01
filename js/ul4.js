var ul4 = {
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

	Color: {
		__iscolor__: true,

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
			return ul4._fu_rgb(this.r, this.g, this.b, a);
		},

		withlum: function(lum)
		{
			if (typeof(lum) !== "number")
				throw "witha() requires a number";
			var hlsa = this.hlsa();
			return ul4._hls(hlsa[0], lum, hlsa[2], hlsa[3]);
		}
	},

	_fu_rgb: function(r, g, b, a)
	{
		var c = this._clone(this.Color);
		c.r = r;
		c.g = g;
		c.b = b;
		c.a = a;
		return c;
	},

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

	_op_contains: function(obj1, obj2)
	{
		if (typeof(obj1) === "string" && typeof(obj2) === "string")
		{
			return obj2.indexOf(obj1) != -1;
		}
		else if (this._fu_islist(obj2))
		{
			return obj2.indexOf(obj1) != -1;
		}
		else if (this._fu_isdict(obj2))
		{
			for (var key in obj2)
			{
				if (key === obj1)
					return true;
			}
			return false;
		}
		// FIXME: Color
	},

	_op_equals: function(obj1, obj2)
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

	_fu_int: function(obj1, obj2)
	{
		var result;
		if (typeof(obj2) !== "undefined")
		{
			if (typeof(obj1) !== "string" || !this._fu_isint(obj2))
				throw "int() requires a string and an integer";
			result = parseInt(obj1, obj2);
			if (result.toString() == "NaN")
				throw "invalid literal for int()";
			return result;
		}
		else
		{
			if (typeof(obj1) == "string")
			{
				result = parseInt(obj1);
				if (result.toString() == "NaN")
					throw "invalid literal for int()";
				return result;
			}
			else if (typeof(obj1) == "number")
				return Math.floor(obj1);
			else if (obj1 === true)
				return 1;
			else if (obj1 === false)
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
		throw "len() requires a sequence or dict";
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

	_op_getitem: function(obj1, obj2)
	{
		if (typeof(obj1) === "string")
		{
			var org = obj2;
			if (obj2 < 0)
				obj2 += obj1.length;
			if (obj2 < 0 || obj2 > obj1.length)
				throw "index " + this._fu_repr(org) + " out of range";
			return obj1[obj2];
		}
		else if (this._fu_isdict(obj1))
		{
			var result = obj1[obj2];
			if (typeof(result) === "undefined")
				throw "key " + this._fu_repr(obj2) + " not found";
			return result;
		}
		else if (this._fu_islist(obj1))
		{
			var org = obj2;
			if (obj2 < 0)
				obj2 += obj1.length;
			if (obj2 < 0 || obj2 > obj1.length)
				throw "index " + this._fu_repr(org) + " out of range";
			return obj1[obj2];
		}
		else if (this._fu_iscolor(obj1))
		{
			var org = obj2;
			if (obj2 < 0)
				obj2 += 4;
			switch (obj2)
			{
				case 0:
					return obj1.r;
				case 1:
					return obj1.g;
				case 2:
					return obj1.b;
				case 3:
					return obj1.a;
				default:
					throw "index " + this._fu_repr(org) + " out of range";
			}
		}
		throw "getitem() needs a sequence or dict";
	},

	_op_getslice: function(obj1, obj2, obj3)
	{
		if (obj2 === null)
			obj2 = 0;
		if (obj3 === null)
			obj3 = obj1.length;
		return obj1.slice(obj2, obj3);
	},

	get: function(obj1, obj2, obj3)
	{
		if (this._fu_isdict(obj1))
		{
			if (typeof(obj3) === "undefined")
				obj3 = null;
			var result = obj1[obj2];
			return (typeof(result) !== "undefined") ? result : obj3;
		}
		throw "get() needs a dict";
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

	replace: function(obj1, obj2, obj3, obj4)
	{
		var result = [];
		if (typeof(obj4) === "undefined")
			obj4 = obj1.length;
		while (obj1.length)
		{
			var pos = obj1.indexOf(obj2);
			if (pos === -1 || !obj4--)
			{
				result.push(obj1);
				break;
			}
			result.push(obj1.substr(0, pos));
			result.push(obj3);
			obj1 = obj1.substr(pos + obj2.length);
		}
		return result.join("");
	},

	strip: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string")
			throw "strip() requires a string";
		if (typeof(obj2) === "undefined")
			obj2 = " \r\n\t";
		else if (typeof(obj2) !== "string")
			throw "strip() requires two strings";
		while (obj1 && obj2.indexOf(obj1[0]) >= 0)
			obj1 = obj1.substr(1);
		while (obj1 && obj2.indexOf(obj1[obj1.length-1]) >= 0)
			obj1 = obj1.substr(0, obj1.length-1);
		return obj1;
	},

	lstrip: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string")
			throw "lstrip() requires a string";
		if (typeof(obj2) === "undefined")
			obj2 = " \r\n\t";
		else if (typeof(obj2) !== "string")
			throw "lstrip() requires two strings";
		while (obj1 && obj2.indexOf(obj1[0]) >= 0)
			obj1 = obj1.substr(1);
		return obj1;
	},

	rstrip: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string")
			throw "rstrip() requires a string";
		if (typeof(obj2) === "undefined")
			obj2 = " \r\n\t";
		else if (typeof(obj2) !== "string")
			throw "rstrip() requires two strings";
		while (obj1 && obj2.indexOf(obj1[obj1.length-1]) >= 0)
			obj1 = obj1.substr(0, obj1.length-1);
		return obj1;
	},

	split: function(obj1, obj2, obj3)
	{
		if (typeof(obj1) !== "string")
			throw "split() requires a string as first argument";
		if (obj2 !== null && typeof(obj2) !== "undefined")
		{
			if (typeof(obj2) !== "string")
				throw "split() requires a string as second argument";
		}
		else
			obj2 = /[ \n\r\t]+/;
		var result = obj1.split(obj2, obj3);
		if (result.length && !result[0].length)
			result.splice(0, 1);
		if (result.length && !result[result.length-1].length)
			result.splice(-1);
		return result;
	},

	lower: function(obj)
	{
		if (typeof(obj) != "string")
			throw "lower() requires a string";
		return obj.toLowerCase();
	},

	upper: function(obj)
	{
		if (typeof(obj) != "string")
			throw "upper() requires a string";
		return obj.toUpperCase();
	},

	capitalize: function(obj)
	{
		if (typeof(obj) != "string")
			throw "capitalize() requires a string";
		if (obj.length)
			obj = obj[0].toUpperCase() + obj.slice(1).toLowerCase();
		return obj;
	},

	items: function(obj)
	{
		if (!this._fu_isdict(obj))
			throw "items() requires a dict";
		var result = [];
		for (var key in obj)
			result.push([key, obj[key]]);
		return result;
	},

	join: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string")
			throw "join() requires a string";
		if (!this._fu_islist(obj2))
			obj2 = this._fu_list(obj2);
		return obj2.join(obj1);
	},

	startswith: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string" || typeof(obj2) !== "string")
			throw "startswith() requires two strings";

		return obj1.substr(0, obj2.length) === obj2;
	},

	endswith: function(obj1, obj2)
	{
		if (typeof(obj1) !== "string" || typeof(obj2) !== "string")
			throw "endswith() requires two strings";

		return obj1.substr(obj1.length-obj2.length) === obj2;
	},

	isoformat: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "isoformat() requires a date";
		var result = obj.getFullYear() + "-" + this._lpad((obj.getMonth()+1).toString(), "0", 2) + "-" + this._lpad(obj.getDate().toString(), "0", 2) + "T" + this._lpad(obj.getHours().toString(), "0", 2) + ":" + this._lpad(obj.getMinutes().toString(), "0", 2) + ":" + this._lpad(obj.getSeconds().toString(), "0", 2)
		var ms = obj.getMilliseconds();
		if (ms)
			result += "." + this._lpad(ms.toString(), "0", 3) + "000";
		return result;
	},

	mimeformat: function(obj)
	{
		var weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
		var monthname = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

		if (!this._fu_isdate(obj))
			throw "mimeformat() requires a date";

		return weekdayname[this.weekday(obj)] + ", " + this._lpad(obj.getDate(), "0", 2) + " " + monthname[obj.getMonth()] + " " + obj.getFullYear() + " " + this._lpad(obj.getHours(), "0", 2) + ":" + this._lpad(obj.getMinutes(), "0", 2) + ":" + this._lpad(obj.getSeconds(), "0", 2) + " GMT";
	},

	_fu_utcnow: function()
	{
		var now = new Date();
		// FIXME: The timezone is wrong for the new ``Date`` object.
		return new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
	},

	year: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "year() requires a date";
		return obj.getFullYear();
	},

	month: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "month() requires a date";
		return obj.getMonth()+1;
	},

	day: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "day() requires a date";
		return obj.getDate();
	},

	hour: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "hour() requires a date";
		return obj.getHours();
	},

	minute: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "minute() requires a date";
		return obj.getMinutes();
	},

	second: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "second() requires a date";
		return obj.getSeconds();
	},

	microsecond: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "micosecond() requires a date";
		return obj.getMilliseconds() * 1000;
	},

	weekday: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "weekday() requires a date";
		var d = obj.getDay();
		return d ? d-1 : 6;
	},

	isleap: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "isleap() requires a date";
		return new Date(obj.getFullYear(), 1, 29).getMonth() === 1;
	},

	yearday: function(obj)
	{
		if (!this._fu_isdate(obj))
			throw "yearday() requires a date";
		var leap = this.isleap(obj) ? 1 : 0;
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
	r: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "r() requires a color";
		return obj.r;
	},

	g: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "g() requires a color";
		return obj.g;
	},

	b: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "b() requires a color";
		return obj.b;
	},

	a: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "a() requires a color";
		return obj.a;
	},

	lum: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "lum() requires a color";
		return obj.lum();
	},

	hls: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hls() requires a color";
		return obj.hls();
	},

	hlsa: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hlsa() requires a color";
		return obj.hlsa();
	},

	hsv: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hsv() requires a color";
		return obj.hsv();
	},

	hsva: function(obj)
	{
		if (!this._fu_iscolor(obj))
			throw "hsva() requires a color";
		return obj.hsva();
	},

	witha: function(obj1, obj2)
	{
		if (!this._fu_iscolor(obj1))
			throw "witha() requires a color";
		return obj1.witha(obj2);
	},

	_hls: function(h, l, s, a)
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
		    return this._fu_rgb(l*255, l*255, l*255, a*255);
		if (l <= 0.5)
		    m2 = l * (1.0+s);
		else
		    m2 = l+s-(l*s);
		m1 = 2.0*l - m2;
		return this._fu_rgb(_v(m1, m2, h+1/3)*255, _v(m1, m2, h)*255, _v(m1, m2, h-1/3)*255, a*255);
	},

	withlum: function(obj1, obj2)
	{
		if (!this._fu_iscolor(obj1))
			throw "withlum() requires a color";
		return obj1.withlum(obj2);
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
		if (obj.__iter__)
		{
			return obj;
		}
		else if (typeof(obj) === "string" || this._fu_islist(obj))
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
		return null;
	},

	// Repeat string ``str`` ``rep`` times
	_str_repeat: function(str, rep)
	{
		var result = "";
		for (;rep>0;--rep)
			result += str;
		return result;
	},

	_list_repeat: function(list, rep)
	{
		var result = [];
		for (;rep>0;--rep)
			for (var i in list)
				result.push(list[i]);
		return result;
	},

	_date_repr: function(obj)
	{
		var year = obj.getFullYear();
		var month = obj.getMonth()+1;
		var day = obj.getDate();
		var hours = obj.getHours();
		var minutes = obj.getMinutes();
		var seconds = obj.getSeconds();
		var milliseconds = obj.getMilliseconds();
		var result = year + "-" + this._lpad(month, "0", 2) + "-" + this._lpad(day, "0", 2) + "T" + this._lpad(hours, "0", 2) + ":" + this._lpad(minutes, "0", 2) + ":" + this._lpad(seconds, "0", 2);
		if (milliseconds)
			result += "." + this._lpad(milliseconds, "0", 3) + "000";
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

	_lpad: function(str, pad, len)
	{
		if (typeof(str) === "number")
			str = str.toString();
		while (str.length < len)
			str = pad + str;
		return str;
	},

	_rpad: function(str, pad, len)
	{
		if (typeof(str) === "number")
			str = str.toString();
		while (str.length < len)
			str = str + pad;
		return str;
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
	}
}
