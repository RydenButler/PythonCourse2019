#### Syntax

## Strings ------------------------------------------------

s1 = "hi my name is ryden" ## double quotes

s2 = 'how are you?' ## single quotes

s3 = """ a string can even span
multiple lines""" ## triple quotes

name = "ryden"
age = "26"
intro = "Hi, I'm " + name + ", I'm " + age

## call characters w/in string
print(name[0])
print(name[1])
print(name[2])

## strings are immutable, variables can change
name[0] = "a"
name = "nebuchadnezzar"

## splitting strings is useful
word_list = intro.split()
print(word_list)

phrase_list = intro.split(",")
print(phrase_list)

letters_list = [letter for letter in name]
print([i for i in name])

## concatenating strings is useful, too
rename = "".join(letters_list)
print(" ".join(letters_list))
print("\n".join(letters_list))

## Indexing is flexible in python
## What's happening here?
num_string = "0123456789"
print(num_string[2:]) ## index 2 through end
print(num_string[-2:]) ## index -2 through end
print(num_string[:2]) ## up to index 2
print(num_string[:-2]) ## up to index -2
print(num_string[::2]) ## sequence, every other
print(num_string[::-2]) ## sequence, every other from the end
print(num_string[::3]) ## sequence, every third from beginning


## Integers ------------------------------------------------

## the usual operators
print(5 + 2)
print(5 - 2)
print(5 * 2)
print(5 ** 2) 
print(5 / 2) ## in python2, this is floor division
print(5 // 2)

whole = 5//3
remainder = 5%3
"Five divded by three is %d and %d fifths" % (whole, remainder)

## assignment is flexible
five = 5
five += 1
print(five)
five /= 3
print(five)
five -= 1
print(five)
five *= 2
print(five)


## Floats ------------------------------------------------

## Real numbers
## Add decimal to integer
## Be careful with the distinction here!

print(12//5)
print(12.0/5)
print(float(12)/5)



## Lists ------------------------------------------------

## A collection of any type of objects -- even lists -- like in R
## Lists will probably be your goto storage in Python, like vectors in R

cohort = ["Oswald", "Jordan"]
cohort.append("Ryan") ## add one element
print(cohort)

cohort.extend(["Ben", "Crystal"]) ## add a list
print(cohort)

## NOT like this...
#cohort = cohort.append()

## remember our indexing... starts at 0!!
print(cohort[0]) ## first
print(cohort[-1]) ## last
print(cohort[len(cohort)]) ## !!!

## lists are mutable
cohort[0] = "Alexandra"
print(cohort)

## Insert by index
cohort.insert(2, "Lucas")
print(cohort)

## Remove, but be careful
last_element = cohort.pop()
print(cohort)
print(last_element)

third_element = cohort.pop(2)
print(cohort)

list_of_lists = [cohort, ["JB", "Ryden", "David", "Erin"]]
print(list_of_lists)



## Tuples ------------------------------------------------

## Like lists, but immutable
## Not super common....

tup = (1,6,5, "Apple", ["python", "R"])
print(tup[1])

tup[1] = 10000 ## !!!

tup.append(10000) ## !!!



## Dictionary ------------------------------------------------

## Like a list, but two key differences:
## - elements not ordered
## - elements are named with keys
## Therefore, you have to index with key names
## 
## Dictionaries are super useful!

ryden_info = {"name" : "Ryden", "age" : 26, "research" : ["social media", "methods"]}

print(ryden_info.keys())
print(ryden_info.values())

ryden_info[0] ##!!!
ryden_info["research"]

ryden_info["last_name"] = "Butler"
print(ryden_info)





## Booleans and Conditionals ------------------------------------------------

t = True
f = False
print(t == f)
print(t != f)


## Perform operation(s) if condition is met 
x = 2
if x == 1:
	print("x is one")
elif x == 2:
	print("x is two")
else:
	print("x is neither one or two")

if x == 2 or x == 3:
	print("Yay!")

if x == 2 and x < 5:
	print("Yay!")

## Note: indentation matters in python, but ipython can help
x = 2
if x == 1:
          print("x is one")





## Loops ------------------------------------------------

even_nums = []
for i in range(1,10):
	if i%2 == 0:
		even_nums.append(i)

hi = []
for i in "hello":
	hi.append(i)

## more succinct way to write simple loop
bye = [i for i in "goodbye"]


while len(even_nums) > 1:
	print(even_nums.pop())

print(even_nums)



## Functions ------------------------------------------------

## Write cleaner code
## Allow for easy testing
## Allow for easier trouble-shooting

## Input, output
def add_squares(x, y):
	return x**2 + y**2

print(add_squares(3,4))
print(add_squares(2,2))



