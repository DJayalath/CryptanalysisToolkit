from analyse import indice_coincidence
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


def freqanalysis(text):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Initialize the dictionary of letter counts: {'A': 0, 'B': 0, ...}
    lcount = dict([(l, 0) for l in letters])

    # Read in the text and count the letter occurences
    for l in text:
        lcount[l.upper()] += 1
    # The total number of letters
    norm = sum(lcount.values())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # The bar chart, with letters along the horizontal axis and the calculated
    # letter frequencies as percentages as the bar height
    x = range(26)
    ax.bar(x, [lcount[l] / norm * 100 for l in letters], width=0.8,
           color='g', alpha=0.5, align='center')
    ax.set_xticks(x)
    ax.set_xticklabels(letters)
    ax.tick_params(axis='x', direction='out')
    ax.set_xlim(-0.5, 25.5)
    ax.yaxis.grid(True)
    ax.set_ylabel('Letter frequency, %')
    plt.suptitle('Letter Frequency Analysis')
    plt.show()

def icgraph(xtext):
    print(xtext)
    print("Whole text IC: ", indice_coincidence(xtext))

    average = []
    for j in range(2, 21):
        sequence = []
        for k in range(j):
            text = list(xtext[k:])
            n = j
            period = int(int(len(text)) // int(n))
            output = []
            i = 0
            while i < len(text):
                output.append(text[i])
                i = i + int(n)
            phrase = "".join(output)
            sequence.append(indice_coincidence(phrase))  # Calculate each index of coincidence
            if j == 15:
                print(sequence[k])
                print(phrase)
        average.append(sum(sequence) / len(sequence))
    print(average)

    names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    values = average
    plt.xticks(names, size="small")
    plt.bar(names, values)

    plt.suptitle('Periodic Index of Coincidence')

    plt.show()