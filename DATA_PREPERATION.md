# Data Collection and Preperation
A description of the process used to prepare a dictionary for generating crossword puzzles and clues

## Collection

A short list of words was used for initial development purposes. This list had the 10000 most common English words in it. The list was sourced from the following Github repo -
[github.com/first20hours/google-10000-english](github.com/first20hours/google-10000-english)

In order to provide a larger collection of words for the crosswords, I used a larger list containing 176,047 words from another Github repo -
[https://github.com/benjihillard/English-Dictionary-Database](https://github.com/benjihillard/English-Dictionary-Database). This longer list also contained the part of speech description and definitions for each word. The definitions are useful for generating the clues for each word in the crossword.

Finally, I found and downloaded a list of all the words found on Wikipedia, listed along with their respective frequencies on that website -
[https://github.com/IlyaSemenov/wikipedia-word-frequency](https://github.com/IlyaSemenov/wikipedia-word-frequency). This was necessary to allow me to associate a word with both its definition and frequency, so as to prefer more common words when more than one word would fit in a particular group of cells in the puzzle.

## Preparation

### Cleaning the data
- All words with a frequency of more than 500 were loaded from the wikipedia word frequency file, and saved to another file 'data/wiki-words-freq500+.txt'
- 
