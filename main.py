import json

def main():
    """Assembles the word list and the frequency list, and uses these to
       create a dictionary keyed by word, with a list of frequency and
       definitions as values"""
    word_list = load_large_dictionary()
    print(f"Word_list loaded with {len(word_list)} entries")

    frequency_dict = load_word_frequencies()
    frequency_keys = frequency_dict.keys()
    print(f"Frequency dict loaded with {len(frequency_keys)} entries")
    
    # Words in the word_list are often duplicated, with differing definitions.
    # Create a dictionary with words as keys, and a list (containing both the
    # frequency of the word and a list of its definitions) as the value

    word_dict = {}
    previous_word = ""
    total_count = 0
    unique_count = 0
    not_in_freq_dict_count = 0
    for item in word_list:
        word = item[0]
        definition = item[1]
        if word not in frequency_keys:
            not_in_freq_dict_count += 1
            continue
        if word != previous_word:
            word_dict[word] = []
            frequency = frequency_dict[word]
            word_dict[word].append(frequency)
            word_dict[word].append([])
            word_dict[word][1].append(definition)
            unique_count += 1
            total_count += 1
            
        else:
            word_dict[word][1].append(definition)
            total_count += 1
        previous_word = word

    print(f"Dictionary created : {unique_count} unique, {total_count} total, {not_in_freq_dict_count} not in frequency dict")

    with open('data/crossword_dictionary.json', 'x', encoding='utf-8') as outfile:
        outfile.write(json.dumps(word_dict, indent=4))
    
def load_word_frequencies():
    """Loads the wikipedia word frequency file and reads all the entries that
       have a frequency of more than 500, then saves these entries to a new
       file."""
    freq_dict = {}
    with open('data/enwiki-20210820-words-frequency.txt', 'r', encoding='utf-8') as infile:
        for line in infile:
            elements = line.split(' ')
            frequency = int(elements[1].replace('\n', ''))
            if frequency >= 1000:
                freq_dict[elements[0]] = frequency
            else:
                break

    try:
        with open('data/wiki-words-freq1000+.txt', 'x', encoding='utf-8') as outfile:
            for key, value in freq_dict.items():
                outfile.writelines(f"{key} {value}\n")
    except FileExistsError:
        print("Skipping file creation - 'data/wiki-words-freq1000+.txt' already exists")

    
    return freq_dict

def load_large_dictionary():
    """Loads the source dictionary and removes illegal words. Saves the
       dictionary to a new file without including the part-of-speech"""
    word_list = []
    with open('data/large_dictionary.txt', 'r', encoding='utf-8') as file:
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
            definition = definition.replace('"', '')
            definition = definition.replace('\n', '')
            
            # Ensure that the words contain the letters a-z only
            if word[0].isalpha() and '-' not in word[0]:
                word_list.append((word.lower(), definition))
    word_list.sort()

    # Write the sorted list of tuples to a new file. In order to avoid confusion,
    # use the pipe '|' instead of the comma ',' as separator.
    try:
        with open('data/large_dict_words_only.txt', 'x', encoding='utf-8') as write_file:
            for word in word_list:
                write_file.writelines(f"{word[0]}|{word[1]}\n")
    except FileExistsError:
        print("Skipping file creation - 'data/large_dictionary.txt' already exists")

    return word_list

if __name__ == '__main__':
    main()