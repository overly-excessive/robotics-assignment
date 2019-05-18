class Akin:

    def __init__(self):
        # read in data
        self.animals = []
        with open("awa/classes.txt") as an_file:
            for line in an_file:
                self.animals.append(line[7:-1].replace('+',' '))

        self.attributes = []
        with open("awa/predicates.txt") as at_file:
            for line in at_file:
                self.attributes.append(line[7:-1])

        self.matrix = []
        with open("awa/predicate-matrix-binary.txt") as m_file:
            for line in m_file:
                line = line.split(' ')
                self.matrix.append(line)

        self.questions = []
        with open("awa/questions.txt") as qu_file:
            for line in qu_file:
                self.questions.append(line[:-1])


        # to store attributes not asked yet (all of them at the beginning)
        self.not_asked = self.attributes[:]
        # store previous answers. Each item corresponds to an animal and stores the number answers fitting this animal.
        self.answers = [0]*len(self.animals) # all zeroes list by default, because no user answers yet
        # store guesses made so far
        self.guesses = []

    def get_question(self):
        # Returns the attribute to be asked about next, deletes it from the not asked yet list

        # first get a list of animal indices that fit the answers so far
        animal_indices = [i for i in range(len(self.answers)) if self.answers[i] == max(self.answers)]
        # get the indices of the attributes not asked yet
        attribute_indices = [i for i in range(len(self.attributes)) if self.attributes[i] in self.not_asked]

        # next get the attribute from the attributes not asked yet, that splits these animals the most equally
        best_split = 0
        best_attribute_index = attribute_indices[0]
        for at_index in attribute_indices:
            yeses = 0.0
            for an_index in animal_indices:
                yeses += int(self.matrix[an_index][at_index])
            split = yeses/len(animal_indices)
            if abs(split - 0.5) < abs(best_split - 0.5):
                best_split = split
                best_attribute_index = at_index

        # assume we are gonna ask this one and delete it from the not asked yet list
        del self.not_asked[self.not_asked.index(self.attributes[best_attribute_index])]

        # return the attribute to be asked
        return self.attributes[best_attribute_index]

    def user_answer(self, attribute, answer):
        # To be called when the user answers a question. Attribute must be one of self.attributes not in
        # self.already_asked. Possible answers are "yes", "no" or "dontknow".

        at_index = self.attributes.index(attribute)

        if answer == "dontknow":
            # no need to do anything in this case
            pass
        elif answer == "yes":
            for an_index in range(len(self.animals)):
                if self.matrix[an_index][at_index] == '1':
                    self.answers[an_index] += 1
        elif answer == "no":
            for an_index in range(len(self.animals)):
                if self.matrix[an_index][at_index] == '0':
                    self.answers[an_index] += 1
        else:
            raise ValueError

    def guess(self):
        # Returns a guess (the animal we think the user had in mind).
        # Returns None if we dont know yet, i.e: more questions need to be asked from the user.

        # First set answers if to zero if that particular animal has already been (incorrectly) guessed
        for past_guess in self.guesses:
            self.answers[self.animals.index(past_guess)] = 0

        # Now get the list of possible solutions (for which the answer points are maximal)
        possible_solutions = [i for i in range(len(A.answers)) if A.answers[i] == max(A.answers)]
        if len(possible_solutions) == 1:    # If there is only one then return it
            return self.animals[possible_solutions[0]]
        else:   # otherwise return None (keep guessing)
            return None

    def wrong_guess(self, guess):
        # This needs to be called when we guessed and the user said this wasn't it
        self.guesses.append(guess)

    def get_question_sentence(self, predicate):
        inx = self.attributes.index(predicate)
        return self.questions[inx]


# This is for testing but also serves as a guidance,
# as in this is the game mechanic that needs to be implemented on pepper
if __name__ == "__main__":
    A = Akin()
    while True:
        solution = A.guess()
        if solution:
            # Ask user if this was it
            yesorno = raw_input("I think you thought of " + solution + ". Was this it? (yes/no) ")
            if yesorno == "yes":
                print "I guessed it!"
                break
            elif yesorno == "no":
                A.wrong_guess(solution)
                continue
            else:
                raise ValueError
        else:
            attribute_to_ask = A.get_question()
            print attribute_to_ask
            ans = raw_input("(yes/no/dontknow) ")
            A.user_answer(attribute_to_ask, ans)
