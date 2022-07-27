import json

def main():

    word_list = load_large_dictionary()
    print(f"Word_list loaded with {len(word_list)} entries")
    
    frequency_list = load_word_frequencies()
    
    # Words in the word_list are often duplicated, with differing definitions.
    # Create a dictionary with words as keys, and definitions as a list of
    # values

    word_dict = {}
    previous_word = ""
    total_count = 0
    unique_count = 0
    for item in word_list:
        item_as_list = item.split('|')
        if len(item_as_list) > 2:
            print("Something odd - more than 2 values separated by '|'")
        word = item_as_list[0]
        definition = item_as_list[1]
        if word != previous_word:
            word_dict[word] = []
            word_dict[word].append(definition)
            unique_count += 1
            total_count += 1
        else:
            word_dict[word].append(definition)
            total_count += 1
        previous_word = word

    print(f"Dictionary created : {unique_count} unique, {total_count} total")
    

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
    """Loads the wikipedia word frequency file and reads all the entries that
       have a frequency of more than 500, then saves these entries to a new
       file."""
    freq_tuple_list = []
    with open('data/enwiki-20210820-words-frequency.txt', 'r') as infile:
        for line in infile:
            elements = line.split(' ')
            frequency = int(elements[1].replace('\n', ''))
            if frequency >= 500:
                freq_tuple = (elements[0], frequency)
                freq_tuple_list.append(freq_tuple)
            else: 
                break

    try:
        with open('data/wiki-words-freq500+.txt', 'x') as outfile:
            for freq_tuple in freq_tuple_list:
                outfile.writelines(f"{freq_tuple[0]} {freq_tuple[1]}\n")
    except FileExistsError:
        print("Skipping file creation - 'data/wiki-words-freq500+.txt' already exists")

    
    return freq_tuple_list

def load_large_dictionary():
    word_set = set()
    with open('data/large_dictionary.txt', 'r') as file:
        for line in file:
            # Separate out all the comma separated values
            split_line = line.split(',')

            # If a line has less than three elements after splitting,
            # reject it
            if len(split_line) < 3:
                continue
            comma_sep_value = split_line[0]
            word = comma_sep_value.split(' ')[0]

            # Reassemble all the values after the first 2, as many of
            # the definitions themselves contain commas!
            definition = ','.join(split_line[2:])

            # Ensure that the words contain the letters a-z only
            if word[0].isalpha() and '-' not in word[0]:
                word_set.add((word.lower(), definition))
    word_list = sorted(word_set)

    # Write the sorted list of tuples to a new file. In order to avoid confusion,
    # use the pipe '|' instead of the comma ',' as separator.
    try:
        with open('data/large_dict_words_only.txt', 'x') as write_file:
            for word in word_list:
                write_file.writelines(f"{word[0]}|{word[1]}\n")
    except FileExistsError:
        print("Skipping file creation - 'data/large_dictionary.txt' already exists")
    
    

    return word_list            

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