import ID3
import parse
import random
from matplotlib import pyplot as plt


def main(file_name):
    data = parse.parse(file_name)
    with_pruning_averages = []
    without_pruning_averages = []

    for length in range(10, 300, 10):
        print('training set size:', length)
        withPruning = []
        withoutPruning = []
        for i in range(100):
            random.shuffle(data)

            train = data[: 3*length//4]
            valid = data[3*length//4 : length]
            test = data[length : len(data)]

            tree = ID3.ID3(train, 'democrat')
            ID3.prune(tree, valid)
            acc = ID3.test(tree, test)
            withPruning.append(acc)

            tree = ID3.ID3(train + valid, 'democrat')
            acc = ID3.test(tree, test)
            withoutPruning.append(acc)

        average_with_pruning = sum(withPruning) / len(withPruning)
        average_without_pruning = sum(withoutPruning) / len(withoutPruning)
        with_pruning_averages.append(average_with_pruning)
        without_pruning_averages.append(average_without_pruning)
        print("average with pruning:", average_with_pruning, "without:", average_without_pruning)

    plt.plot(range(10, 300, 10), with_pruning_averages, label='with pruning')
    plt.plot(range(10, 300, 10), without_pruning_averages, label='without pruning')
    plt.xlabel('number of training examples')
    plt.ylabel('accuracy on test data')
    plt.grid(True)
    plt.title('Learning Curves on house_votes_84.data')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    inFile = 'house_votes_84.data'
    main(inFile)
