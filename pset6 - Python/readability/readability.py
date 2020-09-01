from cs50 import get_string


def main():

    # Get text from user
    text = get_text()
    
    # Print grade level using Coleman-Liau index
    classify(text)


# function to get text from user

def get_text():

    text = get_string("Text: ")
    
    # Keep asking for text until character entered
    while (len(text) < 1 or (ord(text[0]) < 65 or (ord(text[0]) > 90 and ord(text[0]) < 97) or ord(text[0]) > 122)):
        text = get_string("Text: ")
    
    return text

# function to find number of letters in a string (omits punctuation or spaces)


def letters(text):

    # initialise variable to count letters
    letters = int(0)
    
    # iterate until end of string
    for i in range(len(text)):
    
        # cast individual character into decimal integer according to ASCII
        c = ord(text[i])
        
        # check if integer value corresponds to upper/lowercase letter
        if ((c > 64 and c < 91) or (c > 96 and c < 123)):
        
            # if letter add one to counter
            letters += 1
    
    return letters
    

def words(text):

    # initialise variable to count words
    words = int(1)
    
    # iterate until end of string
    for i in range(len(text)):
        
        # cast individual character into decimal integer according to ASCII
        c = ord(text[i])
        
        # check if integer value corresponds to space
        if (c == 32):
        
            # if space add one to counter
            words += 1
    
    return words


# function to determine number of sentences ignoring full stops in special cases eg 'Mr.'


def sentences(text):

    # initialise variable to count sentences
    sentences = int(0)
    
    # iterate until end of string
    for i in range(len(text)):
    
        # cast individual character into decimal integer according to ASCII
        c = ord(text[i])
        
        # check if integer value corresponds to full stop or question or exclamation marks
        if (c == 46 or c == 33 or c == 63):
        
            # if space add one to counter
            sentences += 1
    
    return sentences


# function to calculate Coleman-Liau index


def CL_index(text):

    # initialise variables
    let = int(letters(text))
    wor = int(words(text))
    sen = int(sentences(text))
    
    # calculate parameters
    L = (float(let) / float(wor)) * 100
    S = (float(sen) / float(wor)) * 100
    
    # calculate precise index
    index = 0.0588 * L - 0.296 * S - 15.8
    
    # find index rounded to nearest whole number
    index_round = round(index)
    
    return index_round


# function to print grade based on text


def classify(text):

    # calculate Coleman-Liau index
    index = int(CL_index(text))
    
    # classify grade
    if (index >= 16):
    
        print("Grade 16+")
        
    elif (index < 1):
        
        print("Before Grade 1")
        
    else:
        
        print(f"Grade " + str(index))


main()