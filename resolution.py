import copy
import time

class Parameter:
variable_count = 1

def __init__(self, name=None):
if name:
self.type = &quot;Constant&quot;
self.name = name
else:
self.type = &quot;Variable&quot;
self.name = &quot;v&quot; + str(Parameter.variable_count)
Parameter.variable_count += 1

def isConstant(self):
return self.type == &quot;Constant&quot;

def unify(self, type_, name):
self.type = type_
self.name = name

def __eq__(self, other):
return self.name == other.name

def __str__(self):
return self.name

class Predicate:
def __init__(self, name, params):
self.name = name
self.params = params

def __eq__(self, other):
return self.name == other.name and all(a == b for a, b in zip(self.params, other.params))

def __str__(self):
return self.name + &quot;(&quot; + &quot;,&quot;.join(str(x) for x in self.params) + &quot;)&quot;

def getNegatedPredicate(self):
return Predicate(negatePredicate(self.name), self.params)

class Sentence:
sentence_count = 0

def __init__(self, string):
self.sentence_index = Sentence.sentence_count
Sentence.sentence_count += 1

self.predicates = []
self.variable_map = {}
local = {}

for predicate in string.split(&quot;|&quot;):
name = predicate[:predicate.find(&quot;(&quot;)]
params = []

for param in predicate[predicate.find(&quot;(&quot;) + 1: predicate.find(&quot;)&quot;)].split(&quot;,&quot;):
if param[0].islower():
if param not in local: # Variable
local[param] = Parameter()
self.variable_map[local[param].name] = local[param]
new_param = local[param]
else:
new_param = Parameter(param)
self.variable_map[param] = new_param

params.append(new_param)

self.predicates.append(Predicate(name, params))

def getPredicates(self):
return [predicate.name for predicate in self.predicates]

def findPredicates(self, name):
return [predicate for predicate in self.predicates if predicate.name == name]

def removePredicate(self, predicate):

self.predicates.remove(predicate)
for key, val in self.variable_map.items():
if not val:
self.variable_map.pop(key)

def containsVariable(self):
return any(not param.isConstant() for param in self.variable_map.values())

def __eq__(self, other):
if len(self.predicates) == 1 and self.predicates[0] == other:
return True
return False

def __str__(self):
return &quot;&quot;.join([str(predicate) for predicate in self.predicates])

class KB:
def __init__(self, inputSentences):
self.inputSentences = [x.replace(&quot; &quot;, &quot;&quot;) for x in inputSentences]
self.sentences = []
self.sentence_map = {}

def prepareKB(self):
self.convertSentencesToCNF()
for sentence_string in self.inputSentences:
sentence = Sentence(sentence_string)
for predicate in sentence.getPredicates():
self.sentence_map[predicate] = self.sentence_map.get(

predicate, []) + [sentence]

def convertSentencesToCNF(self):
for sentenceIdx in range(len(self.inputSentences)):
# Do negation of the Premise and add them as literal
if &quot;=&gt;&quot; in self.inputSentences[sentenceIdx]:
self.inputSentences[sentenceIdx] = negateAntecedent(
self.inputSentences[sentenceIdx])

def askQueries(self, queryList):
results = []

for query in queryList:
negatedQuery = Sentence(negatePredicate(query.replace(&quot; &quot;, &quot;&quot;)))
negatedPredicate = negatedQuery.predicates[0]
prev_sentence_map = copy.deepcopy(self.sentence_map)
self.sentence_map[negatedPredicate.name] = self.sentence_map.get(
negatedPredicate.name, []) + [negatedQuery]
self.timeLimit = time.time() + 40

try:
result = self.resolve([negatedPredicate], [
False]*(len(self.inputSentences) + 1))
except:
result = False

self.sentence_map = prev_sentence_map

if result:

results.append(&quot;TRUE&quot;)
else:
results.append(&quot;FALSE&quot;)

return results

def resolve(self, queryStack, visited, depth=0):
if time.time() &gt; self.timeLimit:
raise Exception
if queryStack:
query = queryStack.pop(-1)
negatedQuery = query.getNegatedPredicate()
queryPredicateName = negatedQuery.name
if queryPredicateName not in self.sentence_map:
return False
else:
queryPredicate = negatedQuery
for kb_sentence in self.sentence_map[queryPredicateName]:
if not visited[kb_sentence.sentence_index]:
for kbPredicate in kb_sentence.findPredicates(queryPredicateName):

canUnify, substitution = performUnification(
copy.deepcopy(queryPredicate), copy.deepcopy(kbPredicate))

if canUnify:
newSentence = copy.deepcopy(kb_sentence)
newSentence.removePredicate(kbPredicate)
newQueryStack = copy.deepcopy(queryStack)

if substitution:
for old, new in substitution.items():
if old in newSentence.variable_map:
parameter = newSentence.variable_map[old]
newSentence.variable_map.pop(old)
parameter.unify(
&quot;Variable&quot; if new[0].islower() else &quot;Constant&quot;, new)
newSentence.variable_map[new] = parameter

for predicate in newQueryStack:
for index, param in enumerate(predicate.params):
if param.name in substitution:
new = substitution[param.name]
predicate.params[index].unify(
&quot;Variable&quot; if new[0].islower() else &quot;Constant&quot;, new)

for predicate in newSentence.predicates:
newQueryStack.append(predicate)

new_visited = copy.deepcopy(visited)
if kb_sentence.containsVariable() and len(kb_sentence.predicates) &gt; 1:
new_visited[kb_sentence.sentence_index] = True

if self.resolve(newQueryStack, new_visited, depth + 1):
return True
return False
return True

def performUnification(queryPredicate, kbPredicate):
substitution = {}
if queryPredicate == kbPredicate:
return True, {}
else:
for query, kb in zip(queryPredicate.params, kbPredicate.params):
if query == kb:
continue
if kb.isConstant():
if not query.isConstant():
if query.name not in substitution:
substitution[query.name] = kb.name
elif substitution[query.name] != kb.name:
return False, {}
query.unify(&quot;Constant&quot;, kb.name)
else:
return False, {}
else:
if not query.isConstant():
if kb.name not in substitution:
substitution[kb.name] = query.name
elif substitution[kb.name] != query.name:
return False, {}
kb.unify(&quot;Variable&quot;, query.name)
else:
if kb.name not in substitution:
substitution[kb.name] = query.name
elif substitution[kb.name] != query.name:
return False, {}

return True, substitution

def negatePredicate(predicate):
return predicate[1:] if predicate[0] == &quot;~&quot; else &quot;~&quot; + predicate

def negateAntecedent(sentence):
antecedent = sentence[:sentence.find(&quot;=&gt;&quot;)]
premise = []

for predicate in antecedent.split(&quot;&amp;&quot;):
premise.append(negatePredicate(predicate))

premise.append(sentence[sentence.find(&quot;=&gt;&quot;) + 2:])
return &quot;|&quot;.join(premise)

def getInput(filename):
with open(filename, &quot;r&quot;) as file:
noOfQueries = int(file.readline().strip())
inputQueries = [file.readline().strip() for _ in range(noOfQueries)]
noOfSentences = int(file.readline().strip())
inputSentences = [file.readline().strip()
for _ in range(noOfSentences)]
return inputQueries, inputSentences

def printOutput(filename, results):
print(results)
with open(filename, &quot;w&quot;) as file:
for line in results:
file.write(line)
file.write(&quot;\n&quot;)
file.close()

if __name__ == &#39;__main__&#39;:
inputQueries_, inputSentences_ =
getInput(&#39;/home/ubuntu/environment/255/resolution.txt&#39;)
knowledgeBase = KB(inputSentences_)
knowledgeBase.prepareKB()
results_ = knowledgeBase.askQueries(inputQueries_)
printOutput(&quot;output.txt&quot;, results_)word
