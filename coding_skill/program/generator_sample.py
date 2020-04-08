from memory_profiler import profile


def word_edit_list(word_list):
    new_words = []
    for word in word_list:
        new_word = word.lower()
        new_words.append(new_word)

    return new_words


def word_edit_gen(word_list):
    for word in word_list:
        yield word.lower()


@profile(precision=4)
def main():
    words = ['Python', 'CSS', 'HTML', 'JavaScript']

    # test list append process & check memory
    for text in word_edit_list(words):  # wordsの数だけ全ての要素分のメモリを確保
        print(text)

    # test generator process & check memory
    for text in word_edit_gen(words):   # 要素一つ分のみメモリ確保
        print(text)


if __name__ == '__main__':
    main()

