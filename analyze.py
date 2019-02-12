from __future__ import print_function
import re
from sets import Set
import heapq
import random

#preprocess textfile, remove non alpha char's, convert to lower case, returns list of all words
def preprocessfile(text_file):
	list_words = []

	for line in text_file:
		words_in_line = line.split()
		for word in words_in_line:
			list_words.append(re.sub("[^a-zA-Z ]+", "", word).lower())

	return list_words


#get total number of words
def getTotalNumberOfWords(bag_of_words):

	total_words = len(bag_of_words)
	return total_words


#getTotalUniqueWords
def getTotalUniqueWords(bag_of_words):

	mySet = Set()

	for word in bag_of_words:
		if word not in mySet:
			mySet.add(word)
	return len(mySet)



#get20MostFrequentWords
def getWordToCount(words):
    
    word_to_count = {}
    
    for word in words:
        if word not in word_to_count:
            word_to_count[word] = 1
        else:
            word_to_count[word] += 1
            
    return word_to_count

def get20MostFrequentWords(words):
    word_to_count = getWordToCount(words)
    
    count_words = []
    for word in word_to_count.keys():
        count_words.append((-word_to_count[word], word))
    
    heapq.heapify(count_words)

    most_frequent = []
    
    for i in range(20):
    	currentCount, currentWord = heapq.heappop(count_words)
        most_frequent.append([currentWord, -1*currentCount])
        
    return most_frequent

def removeStopWords(bag_of_words, k):

	file_stopwords = open("stopwords.txt", 'r')
	stopwords_list = preprocessfile(file_stopwords)

	topKstopwords = set(stopwords_list[:k])
	refinedBagWords = []

	for word in bag_of_words:
		if word not in topKstopwords:
			refinedBagWords.append(word)

	return refinedBagWords

def get20MostInterestingFrequentWords(bag_of_words):

	refinedBagWords = removeStopWords(bag_of_words, 1000)

	return get20MostFrequentWords(refinedBagWords)

# get20LeastFrequentWords
def get20LeastFrequentWords(words):
    word_to_count = getWordToCount(words)
    
    count_words = []
    for word in word_to_count.keys():
        count_words.append((word_to_count[word], word))
    
    heapq.heapify(count_words)

    most_frequent = []
    
    for i in range(20):
    	currentCount, currentWord = heapq.heappop(count_words)
        most_frequent.append([currentWord, currentCount])
        
    return most_frequent




#getFrequencyOfWord() 

def getFrequencyOfWord(word):
	list_chapters = ["chap1","chap2","chap3","chap4","chap5","chap6","chap7","chap8","chap9","chap10","chap11","chap12"]
	count_chapterwise = []

	for chap in list_chapters:
		chap_to_list = preprocessfile(open(chap, 'r'))
		myDict = getWordToCount(chap_to_list)
		if word in myDict:
			count_chapterwise.append(myDict[word])
		else:
			count_chapterwise.append(0)

	return count_chapterwise

# getChapterQuoteAppears()

def chapToString(chap):

	file_chap = open(chap, 'r')
	result = ""

	for line in file_chap:

		result += " " + re.sub("[^a-zA-Z ]+", "", line).lower()

	return result

def getChapterQuoteAppears(quote):

	processQuote = re.sub("[^a-zA-Z ]+", "", quote).lower()
	# print(processQuote)
	list_chapters = ["chap1","chap2","chap3","chap4","chap5","chap6","chap7","chap8","chap9","chap10","chap11", "chap12"]

	i = 0
	while i < len(list_chapters):
		chap = list_chapters[i]
		chapString = chapToString(chap)
		# print(chapString)
		if(chapString.find(processQuote) != -1):
			return i + 1
		# print("\n")
		i+=1

	return -1
	
#generate sentences
def getNextWord(currentWord, bag_of_words):

	potentialNextWords = Set()

	i = 0

	while i < len(bag_of_words) - 1:
		if(bag_of_words[i] == currentWord):
			if bag_of_words[i+1] not in potentialNextWords:
				potentialNextWords.add(bag_of_words[i+1])
		i +=1

	# print(potentialNextWords)
	return list(potentialNextWords)[random.randint(0, len(potentialNextWords)-1)]


def generateSentence(startWord, bag_of_words):

	length = 20
	result = startWord
	lastWord = startWord
	while length >= 0 :
		currentWord = getNextWord(lastWord, bag_of_words)
		result += " " + currentWord
		lastWord = currentWord
		length -= 1

	return result


# driver code

file_sherlock_holmes = open("The-Adventures-of-Sherlock-Holmes.txt", 'r')
bag_of_words = preprocessfile(file_sherlock_holmes)

print("Text Analysis: The Adventure of Sherlock Holmes")

print("\nTotal Number of Words: ", getTotalNumberOfWords(bag_of_words))

print("\nTotal Unique Words: ", getTotalUniqueWords(bag_of_words))

print("\n20 most_frequent: ", get20MostFrequentWords(bag_of_words))

# print("\n\n\nAfter Removing top 100 most frequent words:")
# refinedBagWords = removeStopWords(bag_of_words, 1000)
# # print("interesting", refinedBagWords)
# print("\nTotal Number of Words: ", getTotalNumberOfWords(refinedBagWords))

# print("\nTotal Unique Words: ", getTotalUniqueWords(refinedBagWords))

# print("\n20 most_frequent: ", get20MostFrequentWords(refinedBagWords))

print("\n20 most interesting frequent words", get20MostInterestingFrequentWords(bag_of_words))

print("\n20 least frequent", get20LeastFrequentWords(bag_of_words))

searchWord = "pipe"
print("\ncount chapterwise", getFrequencyOfWord(searchWord.lower()))

print("\nFind Quote in chapter:", getChapterQuoteAppears("It is my belief, Watson, founded upon my experience, that the lowest and vilest alleys in London do not present a more dreadful record of sin than does the smiling and beautiful countryside."))

print("\nRandom Sentence:")
print(generateSentence("the", bag_of_words))