/*!
 * UL4ON JavaScript Library
 * http://www.livinglogic.de/Python/ul4on/
 *
 * Copyright 2012 by LivingLogic AG, Bayreuth/Germany
 * Copyright 2012 by Walter Dörwald
 *
 * This library provides functions for encoding and decoding a lightweight
 * machine-readable format for serializing the object types supported by UL4.
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
var ul4on = {
	// Return a string that contains the object ``obj`` in the UL4ON serialization format
	dumps: function(obj)
	{
		var writer = this._writer.create();
		this._dump(obj, writer);
		return writer.finish();
	},

	// Load an object from the string ``data``. ``data`` must contain the object in the UL4ON serialization format
	loads: function(data)
	{
		return this._load(this._reader.create(data));
	},

	// Internal helper for ``dumps``: output the object ``obj`` to the writer ``writer``
	_dump: function(obj, writer)
	{
		if (obj === null)
			writer.write("n");
		else if (typeof(obj) == "boolean")
			writer.write(obj ? "bT" : "bF");
		else if (typeof(obj) == "number")
			writer.writenumber((Math.round(obj) == obj) ? "i" : "f", obj);
		else if (typeof(obj) == "string")
		{
			writer.writenumber("s", obj.length);
			writer.write(obj);
		}
		else if (ul4._fu_iscolor(obj))
		{
			writer.write("c", obj.length);
			if (obj.r < 0x10)
				writer.write("0");
			writer.write(obj.r.toString(16));
			if (obj.g < 0x10)
				writer.write("0");
			writer.write(obj.g.toString(16));
			if (obj.b < 0x10)
				writer.write("0");
			writer.write(obj.b.toString(16));
			if (obj.a < 0x10)
				writer.write("0");
			writer.write(obj.a.toString(16));
		}
		else if (ul4._fu_isdate(obj))
			writer.write(ul4._fu_format(obj, "d%Y%m%d%H%M%S%f"))
		else if (ul4._fu_istemplate(obj))
		{
			var output = obj.dumps();
			writer.writenumber("t", output.length);
			writer.write(output);
		}
		else if (ul4._fu_islist(obj))
		{
			writer.write("[");
			for (var i in obj)
				this._dump(obj[i], writer);
			writer.write("]");
		}
		else if (ul4._fu_isdict(obj))
		{
			writer.write("{");
			for (var key in obj)
			{
				this._dump(key, writer);
				this._dump(obj[key], writer);
			}
			writer.write("}");
		}
		else
			throw "can't handle object";
	},

	// Helper function for ``loads``: Read the next object from ``reader``.
	_load: function(reader)
	{
		debugger;
		var typecode = reader.readchar();

		switch (typecode)
		{
			case "n":
				return null;
			case "b":
				var value = reader.readchar();
				if (value == "T")
					return true;
				else if (value == "F")
					return false;
				else
					throw "wrong value for boolean, expected " + ul4._fu_repr("T") + " or " + ul4._fu_repr("F") + ", got " + ul4._fu_repr(value) + " at position " + reader.pos;
			case "i":
			case "f":
				return reader.readnumber();
			case "s":
				var size = reader.readnumber();
				return reader.read(size);
			case "c":
				var value = reader.read(8);
				return ul4.Color.create(parseInt(value.substring(0, 2), 16), parseInt(value.substring(2, 4), 16), parseInt(value.substring(4, 6), 16), parseInt(value.substring(6, 8), 16));
			case "d":
				var value = reader.read(20);
				return new Date(parseInt(value.substring(0, 4)), parseInt(value.substring(4, 6)) + 1, parseInt(value.substring(6, 8)), parseInt(value.substring(8, 10)), parseInt(value.substring(10, 12)), parseInt(value.substring(12, 14)), parseInt(value.substring(14, 17)));
			case "t":
				var size = reader.readnumber();
				return ul4.Templates.loads(reader.read(size));
			case "[":
				var result = [];
				for (;;)
				{
					typecode = reader.readchar();
					if (typecode == "]")
						return result;
					reader.backup();
					var value = this._load(reader);
					result.push(value);
				}
			case "{":
				var result = {};
				for (;;)
				{
					typecode = reader.readchar();
					if (typecode == "}")
						return result;
					reader.backup();
					var key = this._load(reader);
					var value = this._load(reader);
					result[key] = value;
				}
			default:
				throw "unknown typecode " + ul4._fu_repr(typecode) + " at position " + reader.pos;
		}
	},

	// Helper "class" for output
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
			this.data.push(string);
		},

		// Write the number ``number`` to the buffer (prefixed with ``prefix``)
		writenumber: function(prefix, number)
		{
			this.data.push(prefix);
			if (number !== null)
				this.data.push("" + number);
			this.data.push("|");
		},

		// Returned the complete string written to the buffer
		finish: function()
		{
			return this.data.join("");
		}
	},

	// Helper "class" for reading
	_reader: {
		// Creates a new reader for reading from the string ``data``
		create: function(data)
		{
			var reader = ul4._clone(this);
			reader.data = data;
			reader.pos = 0;
			return reader;
		},

		// Read a character from the buffer
		readchar: function()
		{
			return this.data.charAt(this.pos++);
		},

		// Read ``size`` characters from the buffer
		read: function(size)
		{
			if (this.pos+size > this.length)
				size = this.length-this.pos;
			var result = this.data.substring(this.pos, this.pos+size);
			this.pos += size;
			return result;
		},

		// "unread" one character
		backup: function()
		{
			this.pos--;
		},

		// Read a number from the buffer
		readnumber: function()
		{
			var value = "";
			for (;;)
			{
				var c = this.readchar();
				if (c === "|")
				{
					var result = parseFloat(value);
					if (result == NaN)
						throw "invalid number, got " + ul4._fu_repr("value") + " at position " + this.pos;
					return result;
				}
				else
					value += c;
			}
		},
	}
}
