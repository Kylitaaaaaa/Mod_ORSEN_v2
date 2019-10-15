class NRC_Emotion:

    def __init__(self, term="", fear=0, anger=0, anticip=0, trust=0, surprise=0, positive=0, negative=0, sadness=0, disgust=0, joy=0, synonyms=[]):
        self.term = term
        """Positive Emotions"""
        self.joy = joy
        self.anticip = anticip
        self.trust = trust
        self.surpise = surprise

        """Negative Emotions"""
        self.anger = anger
        self.sadness = sadness
        self.fear = fear
        self.disgust = disgust

        self.positive = positive
        self.negative = negative
        self.synonyms = synonyms

        """For OCC"""
        self.positive_sense_count = 0
        self.negative_sense_count = 0
        self.prior_valence = 0
        self.prospect_polarity = 0
        self.prospective_value = 0
        self.praiseworthy_value = 0

    def __str__(self):
        my_string = "=====================\n"
        my_string = my_string + "FETCHING TERM: %s \n" % (self.term)
        my_string =  my_string + "=====================\n"

        my_string = my_string + "Joy \t Anticip \t Trust \t Surprise \t Anger \t Sadness \t Fear \t  Disgust\n"
        my_string = my_string + "%s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \n\n" % (self.joy, self.anticip, self.trust, self.surpise, self.anger, self.sadness, self.fear, self.disgust)

        my_string = my_string + "Pos_count \t Neg_count \t Prior_val \t Pros_pol \t Pros_val \t Praise_val\n"
        my_string = my_string + "%s \t %s \t %s \t %s \t %s \t %s \n\n" % (self.positive_sense_count, self.negative_sense_count, self.prior_valence, self.prospect_polarity, self.prospective_value, self.praiseworthy_value)

        syn_string = "Synonyms:\n"
        for X in self.synonyms:
            syn_string = syn_string + "%s, " % X

        my_string = my_string + syn_string

        return my_string

    def compute_occ_values(self):
        """
        FOR OCC
        """
        self.positive_sense_count = self.joy + self.anticip + self.trust + self.surpise
        self.negative_sense_count = self.anger + self.sadness + self.fear + self.disgust

        if self.positive_sense_count + self.negative_sense_count > 0:
            self.prior_valence = ((self.positive_sense_count - self.negative_sense_count) / (
                        self.positive_sense_count + self.negative_sense_count)) * 5
            self.prospective_value = (max(self.positive_sense_count, self.negative_sense_count) / (
                    self.positive_sense_count + self.negative_sense_count)) * 5 * self.prospect_polarity
        else:
            self.prior_valence = 0
            self.prospective_value = 0

        if self.positive_sense_count > self.negative_sense_count:
            self.prospect_polarity = 1
        else:
            self.prospect_polarity = -1


        self.praiseworthy_value = self.prior_valence + self.prospective_value

    def add_values(self, to_add):
        print("Adding: ", to_add)
        self.fear = self.fear + to_add[2]
        self.anger = self.anger + to_add[3]
        self.anticip = self.anticip + to_add[4]
        self.trust = self.trust + to_add[5]
        self.surpise = self.surpise + to_add[6]
        self.positive = self.positive + to_add[7]
        self.negative = self.negative + to_add[8]
        self.sadness = self.sadness + to_add[9]
        self.disgust = self.disgust + to_add[10]
        self.joy = self.joy + to_add[11]

        for i in range(12, len(to_add)):
            self.synonyms.append(to_add[i])


