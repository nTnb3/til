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

    # Line #    Mem usage    Increment   Line Contents
    # ================================================
    #     18  37.1562 MiB  37.1562 MiB   @profile(precision=4)
    #     19                             def main():
    #     20  37.1602 MiB   0.0039 MiB       words = ['Python', 'CSS', 'HTML', 'JavaScript']
    #     21
    #     22                                 # test list append process & check memory
    #     23  37.1641 MiB   0.0000 MiB       for text in word_edit_list(words):
    #     24  37.1641 MiB   0.0039 MiB           print(text)
    #     25
    #     26                                 # test generator process & check memory
    #     27  37.1641 MiB   0.0000 MiB       for text in word_edit_gen(words):
    #     28  37.1641 MiB   0.0000 MiB           print(text)
