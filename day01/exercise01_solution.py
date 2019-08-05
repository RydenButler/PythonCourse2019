## Fibonacci sequence
## X_[i] = X_[i-1] + X_[i-2], where X_1 = 1, X_2 = 1
## 1,1,2,3,5,8,....

## Write a for loop, while loop, or function (or all three!) to create a
## list of the first 10 numbers of the fibonacci sequence

fibonacci = []
for i in range(1, 11):
    if i  == 1 or i == 2: fibonacci.append(1)
    else: fibonacci.append(sum([fibonacci[i - 2], fibonacci[i - 3]]))

fibonacci

fibonacci = [1, 1]
while len(fibonacci) < 10:
    fibonacci.append(fibonacci[-1] + fibonacci[-2])
    
fibonacci

def findn(n):
    fibonacci = []
    while len(fibonacci) < n:
        if len(fibonacci) < 2: fibonacci.append(1)
        else: fibonacci.append(sum(fibonacci[-2:]))
    return fibonacci

findn(10)




"""return true if there is no e in 'word', else false"""
def has_no_e(word):
    return 'e' not in word

[has_no_e('abcd'), has_no_e('abcde')]
	


"""return true if there is e in 'word', else false"""
def has_e(word):
    return not has_no_e(word)

[has_e('abcd'), has_e('abcde')]


"""return true if word1 contains only letters from word2, else false"""
def uses_only(word1, word2):
    return not False in [i in word2 for i in [j for j in word1]]

[uses_only('abcd', 'abcde'), uses_only('abcde', 'abcd')]


"""return true if word1 uses all the letters in word2, else false"""
def uses_all(word1, word2):
    return not False in [i in word1 for i in [j for j in word2]]

[uses_all('abcd', 'abcde'), uses_all('abcde', 'abcd')]


"""true/false is the word in alphabetical order?"""
def is_abecedarian(word):
    original = [i for i in word]
    return sorted(original) == original

[is_abecedarian('abcde'), is_abecedarian('adcbe')]
