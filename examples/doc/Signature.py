__version__ = 0,1,2
__doc__ = """\
This module, Signature, contains a single class Signature. This class
permits the convenient examination of the call signatures of Python
callable objects.

Here's some examples of its use:

    >>> def foo(x, y, z=-1.0, *args, **kw):
    ...     return (x+y)**z
    ...
    >>> f = Signature(foo)
    
    >>> print 'ordinary arglist:', f.ordinary_args()
    ordinary arglist: ('x', 'y', 'z')
    
    >>> print 'special_args:', f.special_args()
    special_args: {'keyword': 'kw', 'positional': 'args'}
    
    >>> print 'full_arglist:', f.full_arglist()
    full_arglist: ['x', 'y', 'z', 'args', 'kw']
    
    >>> print 'defaults:', f.defaults()
    defaults: {'z': -1.0}
    
    >>> print 'signature:', str(f)
    signature: foo(x, y, z=-1.0, *args, **kw)

The methods of the Signature class are documented below:

o Signature(func)

  Arguments: func -- this is any callable object written in Python
  Returns:   a Signature instance
  Raises:    TypeError, ValueError

  Behavior:

  The Signature constructor returns a Signature instance for the callable
  object func. If func is not callable, then a TypeError is raised. If
  it is callable, but can't be handled, then a ValueError is raised. (At
  the moment, the latter category are any C builtins.)

o Signature.ordinary_args()

  Returns:   A tuple of strings containing the names of all 'normal'
             arguments.

  Behavior:

  If the callable object has no arguments, the empty tuple is returned.
  The definition of 'normal' includes explicit keyword arguments and the
  'self' argument for methods, but does not include the special arguments
  specified with the '*' or '**' syntax.

o Signature.special_args()

  Returns: A dictionary with the names of the special arguments.

  Behavior:

  This method returns a dictionary of 0, 1, or 2 arguments. An entry
  with a key of 'positional' has the name of the '*'-argument as its
  value, and an entry with a key of 'keyword' has the name of the
  '**'-argument as its value. If the dictionary is empty, then there
  are no special arguments.

o Signature.full_arglist()

  Returns:   A list of all the arguments to the function, whether special
             or not.

  Behavior:

  If there are no special arguments, Signature.full_arglist()'s returns
  a list with the same elements as Signature.ordinary_args(). If there
  are are special arguments, they appended to the end of the list, with
  the '*'-argument preceding the '**'-argument. No asterisks are added
  to the argument names in the returned list.

o Signature.defaults()

  Returns:   A dictionary containing the argument names (as a string) as
             the keys and the default objects as values.

  Behavior:

  If there are no arguments with default values, then an empty dictionary
  is returned. The special arguments specified with the '*' and '**'
  syntax are not considered. 


o Signature.__str__()

  Returns:   A string that should resemble the function or method
             declaration.

  Behavior:

  While it's impossible to exactly match the actual declaration, in most
  cases this should look pretty close. 
"""

import types, string

class Signature:
    def __init__(self, func):
        self.type = type(func)
        self.name, self.func = _getcode(func)
    def ordinary_args(self):
        n = self.func.func_code.co_argcount
        return _varnames(self.func)[0:n]
    def special_args(self):
        n = self.func.func_code.co_argcount
        x = {}
        #
        if _is_variadic(self.func):
            x['positional'] = _varnames(self.func)[n]
            if _has_keywordargs(self.func):
                x['keyword'] = _varnames(self.func)[n+1]
        elif _has_keywordargs(self.func):
            x['keyword'] = _varnames(self.func)[n]
        else:
            pass
        return x
    def full_arglist(self):
        base = list(self.ordinary_args())
        x = self.special_args()
        if x.has_key('positional'):
            base.append(x['positional'])
        if x.has_key('keyword'):
            base.append(x['keyword'])
        return base
    def defaults(self):
        defargs = self.func.func_defaults
        args = self.ordinary_args()
        mapping = {}
        if defargs is not None:
            for i in range(-1, -(len(defargs)+1), -1):
                mapping[args[i]] = defargs[i]
        else:
            pass
        return mapping
    def __str__(self):
        defaults = self.defaults()
        specials = self.special_args()
        l = []
        for arg in self.ordinary_args():
            if defaults.has_key(arg):
                l.append( arg + '=' + str(defaults[arg]) )
            else:
                l.append( arg )
        if specials.has_key('positional'):
            l.append( '*' + specials['positional'] )
        if specials.has_key('keyword'):
            l.append( '**' + specials['keyword'] )
        return "%s(%s)" % (self.name, string.join(l, ', '))

# Magic numbers: These are the bit masks in func_code.co_flags that
# reveal whether or not the function has a *arg or **kw argument.

_POS_LIST = 4
_KEY_DICT = 8

def _is_variadic(function):
    return function.func_code.co_flags & _POS_LIST

def _has_keywordargs(function):
    return function.func_code.co_flags & _KEY_DICT

def _varnames(function):
    return function.func_code.co_varnames

def _getcode(f):
    """_getcode(f)

    This function returns the name and function object of a callable
    object."""
    def method_get(f):
        return f.__name__, f.im_func
    def function_get(f):
        return f.__name__, f
    def instance_get(f):
        if hasattr(f, '__call__'):
            return ("%s%s" % (f.__class__.__name__, '__call__'),
                    f.__call__.im_func)
        else:
            s = ("Instance %s of class %s does not have a __call__ method" %
                 (f, f.__class__.__name__))
            raise TypeError, s
    def class_get(f):
        if hasattr(f, '__init__'):
            return f.__name__, f.__init__.im_func
        else:
            return f.__name__, lambda: None
    codedict = { types.UnboundMethodType: method_get,
                 types.MethodType       : method_get,
                 types.FunctionType     : function_get,
                 types.InstanceType     : instance_get,
                 types.ClassType        : class_get
                 }
    try:
        return codedict[type(f)](f)
    except KeyError:
        if callable(f): # eg, built-in functions and methods
            raise ValueError, "type %s not supported yet." % type(f)
        else:
            raise TypeError, ("object %s of type %s is not callable." %
                                     (f, type(f)))

if __name__ == '__main__':
    def foo(x, y, z=-1.0, *args, **kw):
        return (x+y)**z
    f = Signature(foo)
    print "ordinary arglist:", f.ordinary_args()
    print "special_args:", f.special_args()
    print "full_arglist:", f.full_arglist()
    print "defaults:", f.defaults()
    print "signature:", f
