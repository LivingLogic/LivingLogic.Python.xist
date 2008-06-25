#  Copyright (c) 1998-2002 John Aycock
#  
#  Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions:
#  
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__version__ = 'SPARK-0.7 (pre-alpha-7)'

import re, collections


def token(pattern, *modes):
	def decorator(func):
		if not hasattr(func, 'spark'):
			func.spark = {}
		for mode in modes:
			if mode not in func.spark:
				func.spark[mode] = []
			func.spark[mode].append(pattern)
		return func
	return decorator


def rule(pattern):
	def decorator(func):
		if not hasattr(func, 'spark'):
			func.spark = []
		func.spark.append(pattern)
		return func
	return decorator


def _sparknames(cls):
	names = set()
	for c in cls.__mro__:
		for meth in sorted((m for m in c.__dict__.itervalues() if hasattr(m, 'spark')), key=lambda m:m.func_code.co_firstlineno):
			name = meth.func_name
			if name not in names:
				yield name
				names.add(name)


class Scanner(object):
	reflags = 0

	class __metaclass__(type):
		def __new__(mcl, name, bases, dict_):
			cls = type.__new__(mcl, name, bases, dict_)
			cls.reflect()
			return cls

	@classmethod
	def reflect(cls):
		res = {}
		for name in _sparknames(cls):
			func = getattr(cls, name)
			for (mode, patterns) in func.spark.iteritems():
				pattern = '(?P<%s>%s)' % (name, '|'.join(patterns))
				if mode not in res:
					res[mode] = []
				res[mode].append(pattern)
		for (mode, patterns) in res.iteritems():
			pattern = re.compile('|'.join(patterns), re.VERBOSE|cls.reflags)
			index2func = dict((number-1, getattr(cls, name)) for (name, number) in pattern.groupindex.iteritems())
			res[mode] = (pattern, index2func)
		cls.res = res

	def error(self, s, pos):
		print "Lexical error at position %s" % pos
		raise SystemExit

	def tokenize(self, s):
		start = 0
		self.mode = "default"
		n = len(s)
		while start < n:
			(pattern, index2func) = self.res[self.mode]
			m = pattern.match(s, start)
			if m is None:
				self.error(s, start)

			end = m.end()
			for (i, group) in enumerate(m.groups()):
				if group is not None and i in index2func:
					index2func[i](self, start, end, group)
			start = end

	@token(r'( . | \n )+')
	def default(self, start, end, s):
		print "Specification error: unmatched input"
		raise SystemExit

#
#  Extracted from Parser and made global so that [un]picking works.
#
class _State:
	def __init__(self, stateno, items):
		self.T, self.complete, self.items = [], [], items
		self.stateno = stateno

class Parser(object):
	#
	#  An Earley parser, as per J. Earley, "An Efficient Context-Free
	#  Parsing Algorithm", CACM 13(2), pp. 94-102.  Also J. C. Earley,
	#  "An Efficient Context-Free Parsing Algorithm", Ph.D. thesis,
	#  Carnegie-Mellon University, August 1968.  New formulation of
	#  the parser according to J. Aycock, "Practical Earley Parsing
	#  and the SPARK Toolkit", Ph.D. thesis, University of Victoria,
	#  2001, and J. Aycock and R. N. Horspool, "Practical Earley
	#  Parsing", unpublished paper, 2001.
	#

	def __init__(self, start):
		self.rules = {}
		self.rule2func = {}
		self.rule2name = {}
		self.collectRules()
		self.augment(start)
		self.ruleschanged = 1

	_NULLABLE = '\e_'
	_START = 'START'
	_BOF = '|-'

	def addRule(self, func):
		for rule in func.spark:
			rule = rule.strip().split()
			lhs = rule[0]
			rhs = rule[2:]
			rule = (lhs, tuple(rhs))

			if lhs in self.rules:
				self.rules[lhs].append(rule)
			else:
				self.rules[lhs] = [ rule ]
			self.rule2func[rule] = func
			self.rule2name[rule] = func.__name__
		self.ruleschanged = 1

	def collectRules(self):
		for name in _sparknames(self.__class__):
			self.addRule(getattr(self, name))

	def augment(self, start):
		@rule('%s ::= %s %s' % (self._START, self._BOF, start))
		def _rule(args):
			return args[1]
		self.addRule(_rule)

	def computeNull(self):
		self.nullable = {}
		tbd = []

		for rulelist in self.rules.values():
			lhs = rulelist[0][0]
			self.nullable[lhs] = 0
			for rule in rulelist:
				rhs = rule[1]
				if len(rhs) == 0:
					self.nullable[lhs] = 1
					continue
				#
				#  We only need to consider rules which
				#  consist entirely of nonterminal symbols.
				#  This should be a savings on typical
				#  grammars.
				#
				for sym in rhs:
					if sym not in self.rules:
						break
				else:
					tbd.append(rule)
		changes = 1
		while changes:
			changes = 0
			for lhs, rhs in tbd:
				if self.nullable[lhs]:
					continue
				for sym in rhs:
					if not self.nullable[sym]:
						break
				else:
					self.nullable[lhs] = 1
					changes = 1

	def makeState0(self):
		s0 = _State(0, [])
		for rule in self.newrules[self._START]:
			s0.items.append((rule, 0))
		return s0

	def finalState(self, tokens):
		#
		#  Yuck.
		#
		if len(self.newrules[self._START]) == 2 and len(tokens) == 0:
			return 1
		start = self.rules[self._START][0][1][1]
		return self.goto(1, start)

	def makeNewRules(self):
		worklist = []
		for rulelist in self.rules.values():
			for rule in rulelist:
				worklist.append((rule, 0, 1, rule))

		for rule, i, candidate, oldrule in worklist:
			lhs, rhs = rule
			n = len(rhs)
			while i < n:
				sym = rhs[i]
				if sym not in self.rules or not self.nullable[sym]:
					candidate = 0
					i += 1
					continue

				newrhs = list(rhs)
				newrhs[i] = self._NULLABLE+sym
				newrule = (lhs, tuple(newrhs))
				worklist.append((newrule, i+1,
						 candidate, oldrule))
				candidate = 0
				i += 1
			else:
				if candidate:
					lhs = self._NULLABLE+lhs
					rule = (lhs, rhs)
				if lhs in self.newrules:
					self.newrules[lhs].append(rule)
				else:
					self.newrules[lhs] = [ rule ]
				self.new2old[rule] = oldrule
	
	def typestring(self, token):
		return None

	def error(self, token):
		print "Syntax error at or near `%s' token" % token
		raise SystemExit

	def parse(self, tokens):
		sets = [ [(1,0), (2,0)] ]
		self.links = {}
		
		if self.ruleschanged:
			self.computeNull()
			self.newrules = {}
			self.new2old = {}
			self.makeNewRules()
			self.ruleschanged = 0
			self.edges, self.cores = {}, {}
			self.states = { 0: self.makeState0() }
			self.makeState(0, self._BOF)

		for i in xrange(len(tokens)):
			sets.append([])

			if sets[i] == []:
				break
			self.makeSet(tokens[i], sets, i)
		else:
			sets.append([])
			self.makeSet(None, sets, len(tokens))

		#_dump(tokens, sets, self.states)

		finalitem = (self.finalState(tokens), 0)
		if finalitem not in sets[-2]:
			if len(tokens) > 0:
				self.error(tokens[i-1])
			else:
				self.error(None)

		return self.buildTree(self._START, finalitem,
				      tokens, len(sets)-2)

	def isnullable(self, sym):
		#
		#  For symbols in G_e only.
		#
		return sym.startswith(self._NULLABLE)

	def skip(self, (lhs, rhs), pos=0):
		n = len(rhs)
		while pos < n:
			if not self.isnullable(rhs[pos]):
				break
			pos += 1
		return pos

	def makeState(self, state, sym):
		assert sym is not None
		#
		#  Compute \epsilon-kernel state's core and see if
		#  it exists already.
		#
		kitems = []
		for rule, pos in self.states[state].items:
			lhs, rhs = rule
			if rhs[pos:pos+1] == (sym,):
				kitems.append((rule, self.skip(rule, pos+1)))
		tcore = tuple(sorted(kitems))

		if tcore in self.cores:
			return self.cores[tcore]
		#
		#  Nope, doesn't exist.  Compute it and the associated
		#  \epsilon-nonkernel state together; we'll need it right away.
		#
		k = self.cores[tcore] = len(self.states)
		K, NK = _State(k, kitems), _State(k+1, [])
		self.states[k] = K
		predicted = set()

		edges = self.edges
		rules = self.newrules
		for X in K, NK:
			worklist = X.items
			for item in worklist:
				rule, pos = item
				lhs, rhs = rule
				if pos == len(rhs):
					X.complete.append(rule)
					continue

				nextSym = rhs[pos]
				key = (X.stateno, nextSym)
				if nextSym not in rules:
					if key not in edges:
						edges[key] = None
						X.T.append(nextSym)
				else:
					edges[key] = None
					if nextSym not in predicted:
						predicted.add(nextSym)
						for prule in rules[nextSym]:
							ppos = self.skip(prule)
							new = (prule, ppos)
							NK.items.append(new)
			#
			#  Problem: we know K needs generating, but we
			#  don't yet know about NK.  Can't commit anything
			#  regarding NK to self.edges until we're sure.  Should
			#  we delay committing on both K and NK to avoid this
			#  hacky code?  This creates other problems..
			#
			if X is K:
				edges = {}

		if NK.items == []:
			return k

		#
		#  Check for \epsilon-nonkernel's core.  Unfortunately we
		#  need to know the entire set of predicted nonterminals
		#  to do this without accidentally duplicating states.
		#
		tcore = tuple(sorted(predicted))
		if tcore in self.cores:
			self.edges[(k, None)] = self.cores[tcore]
			return k

		nk = self.cores[tcore] = self.edges[(k, None)] = NK.stateno
		self.edges.update(edges)
		self.states[nk] = NK
		return k

	def goto(self, state, sym):
		key = (state, sym)
		if key not in self.edges:
			#
			#  No transitions from state on sym.
			#
			return None

		rv = self.edges[key]
		if rv is None:
			#
			#  Target state isn't generated yet.  Remedy this.
			#
			rv = self.makeState(state, sym)
			self.edges[key] = rv
		return rv

	def gotoT(self, state, t):
		return [self.goto(state, t)]

	def gotoST(self, state, st):
		rv = []
		for t in self.states[state].T:
			if st == t:
				rv.append(self.goto(state, t))
		return rv

	def add(self, set, item, i=None, predecessor=None, causal=None):
		if predecessor is None:
			if item not in set:
				set.append(item)
		else:
			key = (item, i)
			if item not in set:
				self.links[key] = []
				set.append(item)
			self.links[key].append((predecessor, causal))

	def makeSet(self, token, sets, i):
		cur, next = sets[i], sets[i+1]

		ttype = token is not None and self.typestring(token) or None
		if ttype is not None:
			fn, arg = self.gotoT, ttype
		else:
			fn, arg = self.gotoST, token

		for item in cur:
			ptr = (item, i)
			state, parent = item
			add = fn(state, arg)
			for k in add:
				if k is not None:
					self.add(next, (k, parent), i+1, ptr)
					nk = self.goto(k, None)
					if nk is not None:
						self.add(next, (nk, i+1))

			if parent == i:
				continue

			for rule in self.states[state].complete:
				lhs, rhs = rule
				for pitem in sets[parent]:
					pstate, pparent = pitem
					k = self.goto(pstate, lhs)
					if k is not None:
						why = (item, i, rule)
						pptr = (pitem, parent)
						self.add(cur, (k, pparent),
							 i, pptr, why)
						nk = self.goto(k, None)
						if nk is not None:
							self.add(cur, (nk, i))

	def makeSet_fast(self, token, sets, i):
		#
		#  Call *only* when the entire state machine has been built!
		#  It relies on self.edges being filled in completely, and
		#  then duplicates and inlines code to boost speed at the
		#  cost of extreme ugliness.
		#
		cur, next = sets[i], sets[i+1]
		ttype = token is not None and self.typestring(token) or None

		for item in cur:
			ptr = (item, i)
			state, parent = item
			if ttype is not None:
				k = self.edges.get((state, ttype), None)
				if k is not None:
					#self.add(next, (k, parent), i+1, ptr)
					#INLINED --v
					new = (k, parent)
					key = (new, i+1)
					if new not in next:
						self.links[key] = []
						next.append(new)
					self.links[key].append((ptr, None))
					#INLINED --^
					#nk = self.goto(k, None)
					nk = self.edges.get((k, None), None)
					if nk is not None:
						#self.add(next, (nk, i+1))
						#INLINED --v
						new = (nk, i+1)
						if new not in next:
							next.append(new)
						#INLINED --^
			else:
				add = self.gotoST(state, token)
				for k in add:
					if k is not None:
						self.add(next, (k, parent), i+1, ptr)
						#nk = self.goto(k, None)
						nk = self.edges.get((k, None), None)
						if nk is not None:
							self.add(next, (nk, i+1))

			if parent == i:
				continue

			for rule in self.states[state].complete:
				lhs, rhs = rule
				for pitem in sets[parent]:
					pstate, pparent = pitem
					#k = self.goto(pstate, lhs)
					k = self.edges.get((pstate, lhs), None)
					if k is not None:
						why = (item, i, rule)
						pptr = (pitem, parent)
						#self.add(cur, (k, pparent),
						#	 i, pptr, why)
						#INLINED --v
						new = (k, pparent)
						key = (new, i)
						if new not in cur:
							self.links[key] = []
							cur.append(new)
						self.links[key].append((pptr, why))
						#INLINED --^
						#nk = self.goto(k, None)
						nk = self.edges.get((k, None), None)
						if nk is not None:
							#self.add(cur, (nk, i))
							#INLINED --v
							new = (nk, i)
							if new not in cur:
								cur.append(new)
							#INLINED --^

	def predecessor(self, key, causal):
		for p, c in self.links[key]:
			if c == causal:
				return p
		assert 0

	def causal(self, key):
		links = self.links[key]
		if len(links) == 1:
			return links[0][1]
		choices = []
		rule2cause = {}
		for p, c in links:
			rule = c[2]
			choices.append(rule)
			rule2cause[rule] = c
		return rule2cause[self.ambiguity(choices)]

	def deriveEpsilon(self, nt):
		if len(self.newrules[nt]) > 1:
			rule = self.ambiguity(self.newrules[nt])
		else:
			rule = self.newrules[nt][0]
		#print rule

		rhs = rule[1]
		attr = [None] * len(rhs)

		for i in range(len(rhs)-1, -1, -1):
			attr[i] = self.deriveEpsilon(rhs[i])
		return self.rule2func[self.new2old[rule]](attr)

	def buildTree(self, nt, item, tokens, k):
		state, parent = item

		choices = []
		for rule in self.states[state].complete:
			if rule[0] == nt:
				choices.append(rule)
		rule = choices[0]
		if len(choices) > 1:
			rule = self.ambiguity(choices)
		#print rule

		rhs = rule[1]
		attr = [None] * len(rhs)

		for i in range(len(rhs)-1, -1, -1):
			sym = rhs[i]
			if sym not in self.newrules:
				if sym != self._BOF:
					attr[i] = tokens[k-1]
					key = (item, k)
					item, k = self.predecessor(key, None)
			#elif self.isnullable(sym):
			elif sym.startswith(self._NULLABLE):
				attr[i] = self.deriveEpsilon(sym)
			else:
				key = (item, k)
				why = self.causal(key)
				attr[i] = self.buildTree(sym, why[0],
							 tokens, why[1])
				item, k = self.predecessor(key, why)
		return self.rule2func[self.new2old[rule]](attr)

	def ambiguity(self, rules):
		#
		#  XXX - problem here and in collectRules() if the same rule
		#	 appears in >1 method.  Also undefined results if rules
		#	 causing the ambiguity appear in the same method.
		#
		sortlist = []
		name2index = {}
		for i in range(len(rules)):
			lhs, rhs = rule = rules[i]
			name = self.rule2name[self.new2old[rule]]
			sortlist.append((len(rhs), name))
			name2index[name] = i
		sortlist.sort()
		list = map(lambda (a,b): b, sortlist)
		return rules[name2index[self.resolve(list)]]

	def resolve(self, list):
		#
		#  Resolve ambiguity in favor of the shortest RHS.
		#  Since we walk the tree from the top down, this
		#  should effectively resolve in favor of a "shift".
		#
		return list[0]
