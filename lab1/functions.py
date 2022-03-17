import copy
import re


def print_median_number_of_words(median_number):
    def print_info(text: str):
        print(f"Median number of words in sentence: "
              f"{median_number(text)}")

    return print_info


def print_average_number_of_words(average_number):
    def print_info(text: str):
        print("Average number of words in sentence: "
              f"{average_number(text)}")

    return print_info


def print_repeated_words(rep_words):
    def print_info(text: str):
        dict_of_words = rep_words(text)

        print("Repeated words: ")

        for key in dict_of_words.keys():
            print(f"{key} - {dict_of_words[key]}")

    return print_info


def print_top_n_grams(n_grams):
    def print_info(text: str, n: int, k: int):
        dict_of_n_grams = n_grams(text, n)
        if k > len(dict_of_n_grams):
            print("K is too big!")
        else:

            print("Top of N-grams:")
            counter = 0
            for key in dict_of_n_grams.keys():

                if counter == k:
                    break

                print(f"{key} - {dict_of_n_grams[key]}")
                counter += 1
    return print_info


def repeat_of_words(text: str):
    list_of_words = text.split()
    dict_of_words = dict()
    for word in list_of_words:

        new_word = ""
        word_parts = ["'", "-"]
        for i in range(len(word)):

            if word[i].isalpha() or word[i] in word_parts:
                new_word += word[i].lower()

        if new_word:

            if new_word in dict_of_words.keys():
                dict_of_words[new_word] += 1
            else:
                dict_of_words[new_word] = 1

    return dict_of_words


def average_number_of_words(text: str):
    list_of_sentences = split_text_to_sent(text)
    list_of_words = text.split()
    average_number = len(list_of_words) / len(list_of_sentences)

    return average_number


def median_number_of_words(text: str):
    list_of_sentences = split_text_to_sent(text)
    sentence_lens = list()
    for sent in list_of_sentences:
        sentence_lens.append(len(sent.split()))

    sentence_lens.sort()

    length = len(sentence_lens)
    if length % 2:
        median_number = sentence_lens[int((length - 1) / 2)]
        return median_number
    else:
        median_number = (sentence_lens[int(length / 2)] +
                         sentence_lens[int(length / 2 - 1)]) / 2
        return median_number


def split_text_to_sent(text: str):
    text += " A"
    prefixes_up = r'(Mr|Mrs|Ms|Dr|St)[.] [A-Z]'
    prefixes_low = r'[.] (mr|mrs|ms|dr|st)'
    split_text_to_sentences = r'(?<=[?!.] )[A-Z][,.\-"; \'a-z]+(?=[?!.] [A-Z])'
    split_text_to_one_sent = r'([A-Z][,.\-"; \'a-z]+)(?=[?!.])'
    get_first_sent_in_text = r'([A-Z][,.\-"; \'a-z]+)(?=[?!.] [A-Z])'

    for match in re.finditer(prefixes_up, text):
        text = text[:match.start(0)] + \
               text[match.start(0)].lower() + \
               text[match.start(0) + 1:match.end(0) - 1] + \
               text[match.end(0) - 1].lower() + \
               text[match.end(0):]

    for match in re.finditer(prefixes_low, text):
        text = text[:match.start(1)] + \
               text[match.start(1)].upper() + \
               text[match.start(1) + 1:]

    list_of_sentences = re.findall(split_text_to_sentences, text)
    if not len(list_of_sentences):
        list_of_sentences = re.findall(split_text_to_one_sent, text)
    else:
        list_of_sentences.append(re.match(get_first_sent_in_text, text).group(1))

    return list_of_sentences


def find_n_grams(text: str, n: int):
    dict_of_n_grams = dict()
    dict_of_words = repeat_of_words(text)
    word_parts = r'[\-\']'
    for word in dict_of_words.keys():

        if len(word) < n:
            continue

        elif len(word) == n:

            if re.search(word_parts, word) is not None:
                continue
            else:

                if word in dict_of_n_grams.keys():
                    dict_of_n_grams[word] += 1 * dict_of_words[word]
                else:
                    dict_of_n_grams[word] = 1 * dict_of_words[word]

        else:

            for i in range(len(word) - n + 1):
                n_gram = word[i: i + n]

                if re.search(r'[\-\']', word) is not None:
                    continue

                if n_gram in dict_of_n_grams.keys():
                    dict_of_n_grams[n_gram] += 1 * dict_of_words[word]
                else:
                    dict_of_n_grams[n_gram] = 1 * dict_of_words[word]

    sorted_dict_of_n_grams = dict(sorted(dict_of_n_grams.items(), key=lambda x: x[1], reverse=True))

    return sorted_dict_of_n_grams


def get_info_about_text(text: str, n: int, k: int):
    get_info = print_repeated_words(repeat_of_words)
    get_info(copy.deepcopy(text))
    get_info = print_average_number_of_words(average_number_of_words)
    get_info(copy.deepcopy(text))
    get_info = print_median_number_of_words(median_number_of_words)
    get_info(copy.deepcopy(text))
    get_info = print_top_n_grams(find_n_grams)
    get_info(copy.deepcopy(text), n, k)


