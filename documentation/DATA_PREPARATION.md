# Data Collection and Preperation
A description of the process used to prepare a dictionary for generating crossword puzzles and clues

## Collection

A short list of words was used for initial development purposes. This list had the 10000 most common English words in it. The list was sourced from the following Github repo -
[github.com/first20hours/google-10000-english](github.com/first20hours/google-10000-english)

In order to provide a larger collection of words for the crosswords, I used a larger list extracted from a sql database. [https://sourceforge.net/projects/mysqlenglishdictionary/](https://sourceforge.net/projects/mysqlenglishdictionary/) I've left the code for the extraction out of the repo, because it contains
my hardcoded credentials for my local MYSQL instance.
. This longer list also contained the part of speech description and definitions for each word. The definitions are useful for generating the clues for each word in the crossword.

Finally, I found and downloaded a list of all the words found on Wikipedia, listed along with their respective frequencies on that website -
[https://github.com/IlyaSemenov/wikipedia-word-frequency](https://github.com/IlyaSemenov/wikipedia-word-frequency). This was necessary to allow me to associate a word with both its definition and frequency, so as to prefer more common words when more than one word would fit in a particular group of cells in the puzzle.

## Preparation

### Cleaning the data
- All words with a frequency of more than 1000 were loaded from the wikipedia word frequency file, and saved to another file 'data/wiki-words-freq1000+.txt'
- Words and their definitions were loaded from the source file 'large_dictionary.txt' and saved without the part-of-speech specifier, then returned as a list of tuples - each tuple contains the word, and the definition.
- As words in this list are repeated with differing definitions, a python dictionary was created with words as keys. The value associated with each key is a list, which has 2 elements. The first is the frequency with which the word occurs (on Wikipedia), and the second is a further list of the definitions
- This dictionary is then saved to a file in json format. This file is accessed by the crossword generator when creating a new crossword
