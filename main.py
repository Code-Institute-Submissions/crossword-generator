from asyncore import write
from logging.config import dictConfig


def main():
    word_dict = {}
    # load_large_dictionary()
    
    # load_word_frequencies()
    
    compare_dict_against_frequencies()
    
    """ with open('large_dict_words_only.txt', 'r') as file:
        for word in file:
            word = word.replace('\n', '')
            length = len(word)
            if length in word_dict.keys():
                word_dict[length].append(word)
            else:
                word_dict[length] = []
                word_dict[length].append(word)
    for key, value in word_dict.items():
        print(f"Number of {key}-letter words is {len(value)}")
    print(word_dict[6][0])
    find_matches("abacus", word_dict) """

def compare_dict_against_frequencies():
    word_list = []
    freq_list = []
    with open('large_dict_words_only.txt', 'r') as dictionary_file:
        for line in dictionary_file:
            word_list.append(line.replace('\n', ''))    
    with open('wiki-words-freq100+.txt', 'r') as frequency_file:
        for line in frequency_file:
            elements = line.split(' ')
            word = elements[0]
            freq_list.append(word)
    counter = 0
    matches = []
    while counter < 10000:
        if word_list[counter] in freq_list:
            matches.append(word_list[counter])
        counter += 1
    print(matches)
    print(len(matches))


def load_word_frequencies():
    freq_tuple_list = []
    with open('enwiki-20210820-words-frequency.txt', 'r') as infile:
        for line in infile:
            elements = line.split(' ')
            frequency = int(elements[1].replace('\n', ''))
            if (frequency >= 100):
                freq_tuple = (elements[0], frequency)
                freq_tuple_list.append(freq_tuple)
    with open('wiki-words-freq100+.txt', 'w') as outfile:
        for freq_tuple in freq_tuple_list:
            outfile.writelines(f"{freq_tuple[0]} {freq_tuple[1]}\n")

def load_large_dictionary():
    word_set = set()
    with open('large_dictionary.txt', 'r') as file:
        for line in file:
            comma_sep_value = line.split(',')[0]
            word = comma_sep_value.split(' ')[0]
            if word[0].isalpha():
                word_set.add(word.lower())
    word_list = sorted(word_set)
    with open('large_dict_words_only.txt', 'w') as write_file:
        for word in word_list:
            write_file.writelines(word + '\n')
    print(len(word_list))
            

def find_matches(word, word_dict):
    known_chars = []
    for i, char in enumerate(word):
        if char != '_':
            known_chars.append((i, char))
    potential_matches = word_dict[len(word)]
    matches = []
    for potential_match in potential_matches:
        match = True
        for char_tuple in known_chars:
            index, char = char_tuple
            if potential_match[index] != char:
                match = False
        if match:
            matches.append(potential_match)
    print(f"Words matching {word} : {matches}")


if __name__ == '__main__':
    main()