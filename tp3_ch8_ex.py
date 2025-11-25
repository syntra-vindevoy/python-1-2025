#Excercise 8.12.2
"""
See if you can write a function that does the same thing as the shell command !head.
It should take as arguments the name of a file to read, the number of lines to read,
and the name of the file to write the lines into. If the third parameter is None,
it should display the lines rather than write them to a file.
"""
def read_file(filename_read:str, lines_read:int, filename_write:str):
    read_to_write = ""
    with open(f"{filename_read}", "r") as file:
        for i in range(lines_read):
            read_to_write += file.readline(i) + "\n"

    if filename_write is None or filename_write == "":
        print(read_to_write)
    else:
        with open(f"{filename_write}", "w") as file:
            file.write(read_to_write)

#Excercise 8.12.3
"""
“Wordle” is an online word game where the objective is to guess a five-letter word in six or fewer attempts.
Each attempt has to be recognized as a word, not including proper nouns. After each attempt,
you get information about which of the letters you guessed appear in the target word,
and which ones are in the correct position.

For example, suppose the target word is MOWER and you guess TRIED.
You would learn that E is in the word and in the correct position, R is in the word but not in the correct position,
and T, I, and D are not in the word.

As a different example, suppose you have guessed the words SPADE and CLERK, and you’ve learned that E is in the word,
but not in either of those positions, and none of the other letters appear in the word. Of the words in the word list,
how many could be the target word? Write a function called check_word that takes a five-letter word and checks whether
it could be the target word, given these guesses.

You can use any of the functions from the previous chapter, like uses_any.
"""


#Excercise 8.12.4
"""
Continuing the previous exercise, suppose you guess the work TOTEM and learn that the E
is still not in the right place, but the M is. How many words are left?
"""


#Excercise 8.12.5
"""
The Count of Monte Cristo is a novel by Alexandre Dumas that is considered a classic.
Nevertheless, in the introduction of an English translation of the book, the writer Umberto Eco confesses
that he found the book to be “one of the most badly written novels of all time”.

In particular, he says it is “shameless in its repetition of the same adjective,” and mentions in particular
the number of times “its characters either shudder or turn pale.”

To see whether his objection is valid, let’s count the number number of lines that contain the word pale in any form,
including pale, pales, paled, and paleness, as well as the related word pallor.
Use a single regular expression that matches any of these words. As an additional challenge,
make sure that it doesn’t match any other words, like impale – you might want to ask a virtual assistant for help.
"""

