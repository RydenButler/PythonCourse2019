### Regular Expressions
import re

## https://pythex.org/

## Load example text --------------------------------------------------------

## read in example text
## remember, readlines makes a list of each line break in file
with open("obama-nh.txt", "r") as f:
	text = f.readlines()

## How is this file structured?
## How does it impact our 'text' object?
print(text[0:3])
print(text[0])
print(text[1])
print(text[2])

## Join into one string
## What could we have done at the outset instead?
alltext = ''.join(text)


## Regular Expressions --------------------------------------------------------
## Help us find patterns in the string.

# re.findall
# re.split
# re.match
# re.search
# re.compile


## Can find a string


re.findall(r"Yes we can", alltext)
re.findall(r"American", alltext)
re.findall(r"\n", alltext)


## Basic special characters

re.findall(r"\d", alltext) ##\d digits
re.findall(r"\D", alltext) ##\D non-digits
re.findall(r"[a]", alltext) ## any chars in []
re.findall(r"[a-d]", alltext) ## any chars in []
re.findall(r"[^a-d]", alltext) ## ^ except
re.findall(r"[a-zA-Z0-9]", alltext)
re.findall(r"\w", alltext) ## \w alphanumeric
re.findall(r"\W", alltext) ## \W non-alphanumeric
re.findall(r"\s", alltext) ## \s whitespace
re.findall(r"\S", alltext) ## \S non-whitespace
re.findall(r".", alltext) ## . any char
re.findall(r"\.", alltext) ## \ is escape


## Now, how much of these things?

re.findall(r"\d", alltext)
re.findall(r"\d*", alltext) ## * 0 or more 
re.findall(r"\d+", alltext) ## + 1 or more
re.findall(r"\d?", alltext) ## ? 0 or 1
re.findall(r"\d{3}", alltext) ## {x} exactly x times
re.findall(r"\d{1,3}", alltext) ## {x, y} from x to y times


## Parentheses give us just that portion

re.findall(r"Yes we can", alltext)
re.findall(r"(Yes) we can", alltext)


## Exercise: How would we grab 01/10 as it appears in text?
x = "Hi 10/10 hello 9/18 asdf 9/9"
re.findall(r"\d{2}/\d{2}", x)



## Explain what's happening:
x = "American's lov\we McDonalds"
re.findall(r"\w", x)
re.findall(r"America[a-z]*", x)
re.findall(r"([A-Z]+\w*)\W*", alltext)



## 'r' means raw string -- read string literally
## used instead of escape character "\" 
"\n"
print("\n")

"\\n"
print("\\n")

r"\n"
print(r"\n")



## We can split too

re.split(r'\d', alltext) ## splits at digits, deletes digits

## What is this doing?
re.split(r'\.', alltext) 
re.split(r'(\.)', alltext) ## () splits and keeps separator



## compile the regular expression as an object
## then the regular expression has methods!
keyword = re.compile(r"America[a-z]*")

## search file for keyword in line by line version
for i, line in enumerate(text):
  if keyword.search(line):
  	print(i)
    print(line) 


pattern = re.compile(r'\d') #Create a regex object

pattern.findall(alltext)
pattern.split(alltext)


## Can also search across lines in single strings
## with re.MULTILINE

mline = 'bin\nban\ncan'

## ^ is start of the string
## looking for b
pattern = re.compile(r'^b\w*')
pattern.findall(mline)

pattern = re.compile(r'^b\w*', re.MULTILINE)
pattern.findall(mline)

## Now back to the speech as a single string...
## Explain the difference between thes two lines
re.findall(r'^b\w*', alltext, re.MULTILINE)
re.findall(r'^b\w*', alltext)


## Exercise
## Check if a line ends in a period
## How is this working?
re.findall(r'^.*\.$', alltext, re.MULTILINE)



## search, match, and groups
t = '12 twelve'

pattern = re.compile(r'(\d*)\s(\w*)')
tsearch = pattern.search(t)
tsearch.groups() #tuple of all groups
tsearch.group(0) #the complete match
tsearch.group(1) #the first group
tsearch.group(2) #the second group


## Similar to using () alone, but the text
## matched by the group is then accessible
pattern = re.compile(r'(?P<number>\d*)\s(?P<name>\w*)')
tsearch = pattern.search(t)
tsearch.groups()
tsearch.groupdict()



mytext = '12 24'
pattern = re.compile(r'(\d*)\s(\d*)')
pattern.search(mytext).groups()
pattern.search(mytext).group(0)
pattern.search(mytext).group(1)
pattern.search(mytext).group(2)


## match starts search at beginning of string
## like an invisible ^
pattern.match(r"12 24").groups()
pattern.match(r"a12 24").groups()





### Naive Bayes

# pip install nltk

import nltk
nltk.download('names')
from nltk.corpus import names
import random

names = ([(name, 'male') for name in names.words('male.txt')] +
  [(name, 'female') for name in names.words('female.txt')])

random.shuffle(names)

## Define training and test set sizes
len(names)
train_size = 5000

train_names = names[:train_size]
test_names = names[train_size:]

## A simple feature
def g_features1(word):
  return {'last_letter': word[-1]}

## Msc:
def return_two():
  return 5, 10

x, y = return_two()

## Loop over names, return tuple of dictionary and label
train_set = [(g_features1(n), g) for (n,g) in train_names]
test_set = [(g_features1(n), g) for (n,g) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)

classifier.classify(g_features1('Neo'))
classifier.classify(g_features1('Trinity'))
classifier.classify(g_features1('Max'))
classifier.classify(g_features1('Lucy'))
classifier.prob_classify(g_features1('Lucy')).prob("female")

## Check the overall accuracy with test set
print(nltk.classify.accuracy(classifier, test_set))

## Lets see what is driving this
classifier.show_most_informative_features(5)


## Lets be smarter
## What all are we including now?
def g_features2(name):
  features = {}
  features["firstletter"] = name[0].lower()
  features["lastletter"] = name[-1].lower()
  for letter in 'abcdefghijklmnopqrstuvwxyz':
      features["count(%s)" % letter] = name.lower().count(letter)
      features["has(%s)" % letter] = (letter in name.lower())
  return features

train_set = [(g_features2(n), g) for (n,g) in train_names]
test_set = [(g_features2(n), g) for (n,g) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))


classifier.show_most_informative_features(100)


## Worse? Better? How can we refine?
## Lets look at the errors from this model
## and see if we can do better
errors = []
for (name, label) in test_names:
  guess = classifier.classify(g_features2(name))
  if guess != label:
    prob = classifier.prob_classify(g_features2(name)).prob(guess)
    errors.append((label, guess, prob, name))


for (label, guess, prob, name) in sorted(errors):
  print 'correct=%-10s guess=%-10s prob=%-10s name=%-10s' % (label, guess, prob, name)




## What should we do here?
def g_features3(name):
  features = {}
  if name[-2:] == "ie" or name[-1] == "y":
    features["last_ie"] = True
  else:
    features["last_ie"] = False

  if name[-1] == "k":
    features["last_k"] = True
  else:
    features["last_k"] = False

  return features



train_set = [(g_features3(n), g) for (n,g) in train_names]
test_set = [(g_features3(n), g) for (n,g) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)





# Now lets look at some bigger documents
from nltk.corpus import movie_reviews
nltk.download('movie_reviews')

## list of tuples
## ([words], label)
documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

documents[0]

## Dictionary of words and number of instances
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
len(all_words)
word_features = [k for k in all_words.keys() if all_words[k] > 5]


for w in word_features:
  print(all_words[w])

def document_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
  return features

print(document_features(movie_reviews.words('pos/cv957_8737.txt')))

## Now we have tuple of ({features}, label)
train_docs = documents[:500]
test_docs = documents[1000:1500]
train_set = [(document_features(d), c) for (d,c) in train_docs]
test_set = [(document_features(d), c) for (d,c) in test_docs]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set[:50]))

classifier.show_most_informative_features(1000)

# Copyright (c) 2014 Matt Dickenson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.




