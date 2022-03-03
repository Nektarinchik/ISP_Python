def repeat_of_words(text: str):

    list_of_words = text.split(" ")
    new_word = ""
    dict_of_words = dict()

    for word in list_of_words:
        for i in range(len(word)):
            if "A" <= word[i] <= "Z" or "a" <= word[i] <= "z":
                new_word += word[i]
        if new_word in dict_of_words.keys():
            dict_of_words[new_word] += 1
        else:
            dict_of_words[new_word] = 1
        new_word = ""
    return dict_of_words


def average_number_of_words(text: str):

    amount_of_sentences = 0
    for i in range(len(text)):
        if text[i] in [".", "?", "!"]:
            amount_of_sentences += 1
    list_of_words = text.split(" ")
    return len(list_of_words) / amount_of_sentences


def median_number_of_words(text: str):

    sentence = ""
    list_of_words = list()
    sentence_lens = list()
    for i in range(len(text)):
        if "A" <= text[i] <= "Z" or "a" <= text[i] <= "z" \
                or text[i] in [" ", ";", ",", "-"]:
            if text[i] == " ":
                if sentence:
                    sentence += text[i]
            else:
                sentence += text[i]
        else:
            if text[i] in [".", "?", "!"]:
                list_of_words = sentence.split(" ")
                sentence_lens.append(len(list_of_words))
            sentence = ""
            list_of_words.clear()
    sentence_lens.sort()
    length = len(sentence_lens)
    if length % 2:
        return sentence_lens[int((length - 1) / 2)]
    else:
        return (sentence_lens[int(length / 2)] + sentence_lens[int(length / 2 - 1)]) / 2


def find_n_grams(text: str, n: int):

    n_gram = ""
    dict_of_n_grams = dict()
    dict_of_words = repeat_of_words(text)
    for word in dict_of_words.keys():
        if len(word) < n:
            continue
        elif len(word) == n:
            if word in dict_of_n_grams.keys():
                dict_of_n_grams[word] += 1 * dict_of_words[word]
            else:
                dict_of_n_grams[word] = 1 * dict_of_words[word]
        else:
            for i in range(0, len(word) - n + 1):
                for j in range(i, i + n):
                    n_gram += word[j]
                if n_gram in dict_of_n_grams.keys():
                    dict_of_n_grams[n_gram] += 1 * dict_of_words[word]
                else:
                    dict_of_n_grams[n_gram] = 1 * dict_of_words[word]
                n_gram = ""
    sorted_dict_of_n_grams = dict(sorted(dict_of_n_grams.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict_of_n_grams


if __name__ == '__main__':

    # from sys import argv
    #
    # script, text, K, N = argv
    #
    # if not K:
    #     K = 10
    # else:
    #     K = int(K)
    # if not N:
    #     N = 4
    # else:
    #     N = int(N)

    text = input("Please enter a text: ")

    K = int(input("Please enter number of top N-grams, K: "))
    N = int(input("Please enter N: "))
    dict_of_words = repeat_of_words(text)
    print(dict_of_words)

    print(f"Average number of words in sentence: {average_number_of_words(text)}")

    print(f"Median number of words in sentence: {median_number_of_words(text)}")

    dict_of_n_grams = find_n_grams(text, N)

    if K > len(dict_of_n_grams):
        print("K is too big!")
    else:
        print("Top of N-grams:\n")
        counter = 0
        for key in dict_of_n_grams.keys():
            if counter == K:
                break
            print(f"{key} - {dict_of_n_grams[key]}")
            counter += 1