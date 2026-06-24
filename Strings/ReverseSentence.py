sentence = "Java is awesome"
reversed_sentence = ""
for word in sentence.split():
    reversed_sentence = word + " " + reversed_sentence
print("Reversed sentence:", reversed_sentence)
