# Python string formatting

from math import log
try:
    import locale
except:
    locale = None
try:
    import fpformat
except:
    fpformat = None

# Except for errors in the format string.
class FormatError(StandardError):
    pass

strict_format_errors = False

class ConversionTypes:
    Binary      = 'b'   # Base-2
    Character   = 'c'   # Print as character
    Decimal     = 'd'   # Decimal integer
    Exponent    = 'e'   # Exponential notation
    ExponentUC  = 'E'   # Exponential notation with upper case 'E'
    Fixed       = 'f'   # Fixed-point
    FixedUC     = 'F'   # Fixed-point with upper case
    General     = 'g'   # General number notation
    GeneralUC   = 'G'   # General number notation with upper case 'E'
    Number      = 'n'   # Number in locale-specific format
    Octal       = 'o'   # Octal
    Repr        = 'r'   # In repr() format
    String      = 's'   # Convert using str()
    Hex         = 'x'   # Base 16
    HexUC       = 'X'   # Base 16 upper case
    Percentage  = '%'   # As percentage

ConversionTypes.All = set(ConversionTypes.__dict__.values())

# Parse the standard conversion spec. Note that I don't use
# regex here because I'm trying to eliminate external dependencies
# as much as possible.
def parse_std_conversion(spec):
    length = None
    precision = None
    ctype = None
    align = None
    fill_char = None
    sign = None

    index = 0
    spec_len = len(spec)

    # If the second char is an alignment token,
    # then parse the fill char
    if spec_len >=2 and spec[ 1 ] in '<>=^':
        fill_char = spec[ 0 ]
        align = spec[ 1 ]
        index = 2
    # Otherwise, parse the alignment token
    elif spec_len >= 1 and spec[ 0 ] in '<>=^':
        align = spec[ 0 ]
        index = 1

    # Parse the various sign options
    if index < spec_len and spec[ index ] in ' +-(':
        sign = spec[ index ]
        index += 1
        if index < spec_len and spec[ index ] == ')':
            index += 1

    # The special case for 0-padding (backwards compat)
    if fill_char == None and index < spec_len and spec[ index ] == '0':
        fill_char = '0'
        if align == None:
            align = '='
        index += 1

    # Parse field width
    saveindex = index
    while index < spec_len and spec[index].isdigit():
        index += 1

    if index > saveindex:
        length = int(spec[saveindex : index])

    # Parse field precision
    if index < spec_len and spec[index] == '.':
        index += 1
        saveindex = index
        while index < spec_len and spec[index].isdigit():
            index += 1
        if index > saveindex:
            precision = int(spec[saveindex:index])

    # Finally, parse the type field
    remaining = spec_len - index
    if remaining > 1:
        return None     # Invalid conversion spec

    if remaining == 1:
        ctype = spec[index]
        if ctype not in ConversionTypes.All:
            return None

    return (fill_char, align, sign, length, precision, ctype)

# Convert to int, and split into sign part and magnitude part
def to_int(val):
    val = int(val)
    if val < 0: return '-', -val
    return '+', val

# Convert to float, and split into sign part and magnitude part
def to_float(val):
    val = float(val)
    if val < 0: return '-', -val
    return '+', val

# Pure python implementation of the C printf 'e' format specificer
def sci(val,precision,letter='e'):
    # Split into sign and magnitude (not really needed for formatting
    # since we already did this part. Mainly here in case 'sci'
    # ever gets split out as an independent function.)
    sign = ''
    if val < 0:
        sign = '-'
        val = -val

    # Calculate the exponent
    exp = int(floor(log(val,10)))

    # Normalize the value
    val *= 10**-exp

    # If the value is exactly an integer, then we don't want to
    # print *any* decimal digits, regardless of precision
    if val == floor(val):
        val = int(val)
    else:
        # Otherwise, round it based on precision
        val = round(val,precision)
        # The rounding operation might have increased the
        # number to where it is no longer normalized, if so
        # then adjust the exponent.
        if val >= 10.0:
            exp += 1
            val = val * 0.1

    # Convert the exponent to a string using only str().
    # The existing C printf always prints at least 2 digits.
    esign = '+'
    if exp < 0:
        exp = -exp
        esign = '-'
    if exp < 10: exp = '0' + str(exp)
    else: exp = str(exp)

    # The final result
    return sign + str(val) + letter + esign + exp

# The standard formatter
def format_builtin_type(value, spec):

    # Parse the conversion spec
    conversion = parse_std_conversion(spec)
    if conversion is None:
        raise FormatError("Invalid conversion spec: " + spec)

    # Unpack the conversion spec
    fill_char, align, sign_char, length, precision, ctype = conversion

    # Choose a default conversion type
    if ctype == None:
        if isinstance(value, int) or isinstance(value, long):
            ctype = ConversionTypes.Decimal
        elif isinstance(value, float):
            ctype = ConversionTypes.General
        else:
            ctype = ConversionTypes.String

    sign = None

    # Conversion types that resolve to other types
    if ctype == ConversionTypes.Percentage:
        ctype = ConversionTypes.Fixed
        value = float(value) * 100.0

    if ctype == ConversionTypes.Binary:
        result = ''
        sign, value = to_int(value)
        while value:
            if value & 1: result = '1' + result
            else: result = '0' + result
            value >>= 1
        if len(result) == 0:
            result = '0'
    elif ctype == ConversionTypes.Octal:
        sign, value = to_int(value)
        result = oct(value)
    elif ctype == ConversionTypes.Hex:
        sign, value = to_int(value)
        result = hex(value)
    elif ctype == ConversionTypes.HexUC:
        sign, value = to_int(value)
        result = hex(value).upper()
    elif ctype == ConversionTypes.Character:
        result = chr(int( value) )
    elif ctype == ConversionTypes.Decimal:
        sign, value = to_int(value)
        result = str(value)
    elif ctype == ConversionTypes.Fixed or ctype == ConversionTypes.FixedUC:
        sign, value = to_float(value)
        if fpformat and precision is not None:
            result = fpformat.fix(value, precision)
        else:
            result = str(value)
    elif ctype == ConversionTypes.General or ctype == ConversionTypes.GeneralUC:
        #Same as "e" if exponent is less than -4 or greater than precision, "f" otherwise.
        sign, value = to_float(value)
        if fpformat and precision is not None:
            if value < 0.0001 or value > 10**precision:
                result = fpformat.sci(value, precision)
            else:
                result = fpformat.fix(value, precision)
            if ctype == ConversionTypes.GeneralUC:
                result = result.upper()
        else:
            result = str(value)
    elif ctype == ConversionTypes.Exponent or ctype == ConversionTypes.ExponentUC:
        sign, value = to_float(value)
        if precision is None: precision = 5 # Duh, I dunno
        result = sci(value, precision, ctype)
    elif ctype == ConversionTypes.Number:
        sign, value = to_float(value)
        if locale:
            # For some reason, this is not working the way I would
            # expect
            result = locale.format("%f", float( value) )
        else:
            result = str(value)
    elif ctype == ConversionTypes.String:
        result = str(value)
    elif ctype == ConversionTypes.Repr:
        result = repr(value)

    # Handle the sign logic
    prefix = ''
    suffix = ''
    if sign == '-':
        if sign_char == '(': prefix, suffix = '(', ')'
        else: prefix = '-'
    elif sign == '+':
        if sign_char == '+': prefix = '+'
        elif sign_char == ' ': prefix = ' '

    # Handle the padding logic
    if length is not None:
        padding = length - len(result) - len(prefix) - len(suffix)
        if fill_char is None:
            fill_char = ' '
        if padding > 0:
            if align == '>' or align == '^':
                return fill_char * padding + prefix + result + suffix
            elif align == '=':
                return prefix + fill_char * padding + result + suffix
            else:
                return prefix + result + suffix + fill_char * padding

    return prefix + result + suffix

def cformat(template, format_hook, args, kwargs):
    # Using array types since we're going to be growing
    # a lot.
    from array import array
    array_type = 'c'

    # Use unicode array if the original string is unicode.
    if isinstance(template, unicode): array_type = 'u'
    buffer = array(array_type)

    # Track which arguments actuallly got used
    unused_args = set(kwargs.keys())
    unused_args.update(range(0, len(args)))

    # Inner function to format a field from a value and
    # conversion spec. Most details missing.
    def format_field(value, cspec):

        # See if there's a hook
        if format_hook:
            v = format_hook(value, cspec)
            if v is not None:
                return str(v)

        # See if there's a __format__ method
        elif hasattr(value, '__format__'):
            return value.__format__(cspec)

        # Default formatting
        return format_builtin_type(value, cspec)

    # Parse a field specification. Returns True if it was a valid
    # field, False if it was merely an escaped brace. (We do it
    # this way to avoid lookahead.)
    def parse_field(buffer):

        # A separate array for the field spec.
        fieldspec = array(array_type)

        # Consume from the template iterator.
        for index, ch in template_iter:
            # A sub-field. We just interpret it like a normal field,
            # and append to the fieldspec.
            if ch == '{':
                # If the very first character is an open brace, then
                # assume its an escaped (doubled) brace.
                if len(fieldspec) == 0:
                    return False

                # Here's where we catch that doubled brace
                if not parse_field(fieldspec):
                    buffer.extend('{')
                    return True

            # End of field. Now interpret it.
            elif ch == '}':
                # Convert the array to string or uni
                if array_type == 'u':
                  fieldspec = fieldspec.tosunicode()
                else:
                  fieldspec = fieldspec.tostring()

                # Check for conversion spec
                name = fieldspec
                conversion = ''
                parts = fieldspec.split(':', 1)
                if len(parts) > 1:
                    name, conversion = parts

                try:
                    first_time = True
                    # Split the field name into subfields
                    for namepart in name.split('.'):
                        # Split that part by open bracket chars
                        keyparts = namepart.split('[')
                        # The first part is just a bare name
                        key = keyparts[0]

                        # Empty strings are not allowed as field names
                        if key == '':
                            raise FormatError("empty field name at char " + str(index))

                        # The first name in the sequence is used to index
                        # the args/kwargs arrays. Subsequent names are used
                        # on the result of the previous operation.
                        if first_time:
                            first_time = False

                            # Attempt to coerce key to integer
                            try:
                                key = int(key)
                                value = args[key]
                            except ValueError:
                                # Keyword args are strings, not uni (so far)
                                value = kwargs[key]

                            # If we got no exception, then remove from
                            # unused args
                            unused_args.remove(key)
                        else:
                            # This is not the first time, so get
                            # an attribute
                            value = getattr(value, key)

                        # Now process any bracket expressions which followed
                        # the first part.
                        for key in keyparts[1:]:
                            endbracket = key.find(']')
                            if endbracket < 0 or endbracket != len(key) - 1:
                                raise FormatError("Invalid field syntax at position " + str(index))

                            # Strip off the closing bracket and try to coerce to int
                            key = key[:-1]
                            try:
                                key = int(key)
                            except ValueError:
                                pass

                            # Get the attribute
                            value = value[key]

                except (AttributeError,KeyError,IndexError), e:
                    if strict_format_errors: raise
                    buffer.extend('?' + e.__class__.__name__ + '?')
                    return True

                buffer.extend(format_field(value, conversion))
                return True
            else:
                fieldspec.append(ch)

        raise FormatError("unmatched open brace at position " + str(index))

    # Construct an iterator from the template
    template_iter = enumerate(template)
    prev = None
    for index, ch in template_iter:
        if prev == '}':
            if ch != '}':
                raise FormatError("unmatched close brace")
            else:
                buffer.append('}')
                prev = None
                continue

        if ch == '{':
            # It's a field
            if not parse_field(buffer):
                buffer.extend('{')
        elif ch != '}':
            buffer.append(ch)
        prev = ch

    if prev == '}':
        raise FormatError("unmatched close brace")

    # Complain about unused args
    if unused_args and strict_format_errors:
        raise FormatError(
            "Unused arguments: "
            + ",".join(str(x) for x in unused_args))

    # Convert the array to its proper type
    if isinstance(template, unicode):
        return buffer.tounicode()
    else:
        return buffer.tostring()

def format(template, *args, **kwargs):
    return cformat(template, None, args, kwargs)
