import numpy as np

K_q = lambda K_mathcal , q : [idx for idx,K in enumerate(K_mathcal) if q in K]

prob_K_q = lambda K_mathcal, q, prob : sum([prob[idx] for idx in K_q(K_mathcal , q)])

# Q is the set of items
# K_mathcal is the knowledge network
# K0 is the set of items that the student understands. We use it for simulations but not for real student.
# beta_q is the probability for the student to fail to response item q despite the fact that he manages this item.

class knowledge_learning_space:

    def __init__(self,Q,K_mathcal,Xi,beta_q=None,prob_distribution = None,K0=None,student_name = None):


        if student_name != None:
            self.student_name = student_name

        if (beta_q == None) and (K0!= None):
            self.beta_q = {q : 0.0 for q in K0}
        else:
            self.beta_q = beta_q

        self.K0 = K0
        self.Xi = Xi
        self.Q = Q
        self.K_mathcal = K_mathcal
        n_K = len(K_mathcal)

        if prob_distribution == None:

            self.prob_distribution =[1/n_K for K in K_mathcal]

        else:

            self.prob_distribution = prob_distribution

        self.prob_distribution_items = {q : prob_K_q(K_mathcal, q,self.prob_distribution) for q in self.Q}
        min_half = min([np.abs(p - 0.5) for p in self.prob_distribution_items.values()])
        distance_half = [q for q in self.Q if np.abs(self.prob_distribution_items[q]  -0.5 ) \
                              == min_half]

        self.responded_items = {q : [] for q in Q}

        idx_next_item = np.random.randint(0,len(distance_half))

        self.next_item = distance_half[idx_next_item]

    def simulation(self):

        if self.K0 == None:
            raise NameError('No se puede simular sin conocer K0')

        q = self.next_item
        r = int((q in self.K0) and (np.random.rand() <= 1 - self.beta_q[q]))
        self.responded_items[q].append(r)

        for idx,K in enumerate(self.K_mathcal):

            if int(q in K) == r:

                self.prob_distribution[idx] = self.Xi[(q,r)] * self.prob_distribution[idx]

        S = np.sum(self.prob_distribution)

        for idx in range(len(self.K_mathcal)):

                self.prob_distribution[idx] = self.prob_distribution[idx] / S

        self.prob_distribution_items = {q : prob_K_q(self.K_mathcal, q,self.prob_distribution) for q in self.Q}

        min_half = min([np.abs(p - 0.5) for p in self.prob_distribution_items.values()])

        distance_half = [q for q in self.Q if np.abs(self.prob_distribution_items[q]  -0.5 ) \
                              == min_half]

        idx_next_item = np.random.randint(0,len(distance_half))

        self.next_item = distance_half[idx_next_item]

    def response_item(self,r):

        q = self.next_item
        self.responded_items[q].append(r)

        for idx,K in enumerate(self.K_mathcal):

            if int(q in K) == r:

                self.prob_distribution[idx] = self.Xi[(q,r)] * self.prob_distribution[idx]

        S = np.sum(self.prob_distribution)

        for idx in range(len(self.K_mathcal)):

                self.prob_distribution[idx] = self.prob_distribution[idx] / S

        self.prob_distribution_items = {q : prob_K_q(K_mathcal, q,self.prob_distribution) for q in Q}
        min_half = min([np.abs(p - 0.5) for p in self.prob_distribution_items.values()])
        distance_half = [q for q in self.Q if np.abs(self.prob_distribution_items[q]  -0.5 ) \
                              == min_half]

        idx_next_item = np.random.randint(0,len(distance_half))
        self.next_item = distance_half[idx_next_item]