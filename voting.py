import pandas as pd
import numpy as np

#seed for testing consistency
np.random.seed(90210)


##########

class Election():
    '''
    runs single transferrable voting
    if number of new winners in final round exceeds total number of spots left, returns current winners as well as new winners to allow for revoting with new winners
    '''
    def __init__(self, num_candidates, path):
        import pandas as pd
        import numpy as np
        
        '''
        num_candidates (int): number of total candidates
        path (str): path to csv of votes num_voters rows and num_candidates+1 columns (column 0 is names)
        '''

        #read csv
        data = pd.read_csv(path)
    
        #init internals
        self.num_voters = data.shape[0]
        self.num_spots = data.shape[1]-1
        self.num_candidates = num_candidates
        self.winners = np.zeros(num_candidates, dtype = bool)
        self.threshold = (self.num_voters / (self.num_spots + 1)) + 1
        self.voter_states = np.zeros(self.num_voters, dtype = np.int64)

        # init indicator
        self.indicator = np.zeros((self.num_spots, self.num_voters, self.num_candidates), dtype=np.int64)
        for i in range(1,self.num_spots+1):
            for j in range(self.num_voters):
                self.indicator[i-1, j, data.iloc[j,i]] += 1
    
        # init tallies
        self.tallies = np.zeros(self.num_candidates)
        for c in range(self.num_candidates):
            self.tallies[c] += np.sum(self.indicator[0,:,c])




    def increment_round(self):
        '''
        increments election by a single round

        who_is_over: set of candidates for which the number of votes allocated to them has exceeded the threshold
        new_winners: set of candidates who became winners (exceeded threshold) this round
        '''

        who_is_over = set()
        new_winners = set()

        #find all who are over
        for i in range(self.num_candidates):
            if self.tallies[i] != None and self.tallies[i] > self.threshold:
                who_is_over.add(i)
        
        #fill new_winners [Can we combine these loops?^^]
        for c in who_is_over:
            if not self.winners[c]:
                new_winners.add(c)


        if len(new_winners) + np.sum(self.winners) > self.num_spots:
            return list(new_winners)
        else:
            for w in new_winners:
                self.winners[w] = True
        
        if self.num_spots >= sum(np.invert(np.isnan(self.tallies))):
            inv = np.invert(np.isnan(self.tallies))
            self.winners[np.where(inv)[0]] = True
            return "Type 1"

        # if no (new?) winners. should this be new_winners?
        elif len(who_is_over) == 0:
            minimum = float("inf")
            minidx = None
            for i in range(self.num_candidates):
                if self.tallies[i] != None and self.tallies[i] < minimum:
                    minimum = self.tallies[i]
                    minidx = i

            #set tallies to None for least voted for
            who_voted = set()
            self.tallies[minidx] = None
            if minidx == None:
                return "Type 2"

            #get who voted for them
            for j in range(self.num_voters):
                if self.voter_states[j] < self.num_spots and self.indicator[self.voter_states[j],j,minidx] != 0:
                    # only add voters who have more votes (aren't exhausted)
                    who_voted.add(j)
                    self.voter_states[j] += 1
          
            for v in who_voted:
                if self.voter_states[v] < self.num_spots:
                    cand = self.indicator[self.voter_states[v],v,:].nonzero()[0][0]
                    self.tallies[cand] += 1

        else:
            # if new winners
            for i in who_is_over:
                who_voted = set()
                for j in range(self.num_voters):
                    if self.voter_states[j] < self.num_spots and self.indicator[self.voter_states[j],j,i] != 0:
                    # only add voters who have more votes
                        who_voted.add(j)
                        self.voter_states[j] += 1
                
                #get fractional vote value
                frac = (self.tallies[i] - self.threshold) / len(who_voted)
                self.tallies[i] = self.threshold

                #assign fractional votes
                for v in who_voted:
                    if self.voter_states[v] < self.num_spots:
                        cand = self.indicator[self.voter_states[v], v].nonzero()[0][0]
                        self.tallies[cand] += frac




    def run_election(self):
        extras = None
        while np.sum(self.winners) < self.num_spots:
            extras = self.increment_round()
            if extras != None:
                break
        ret = []
        for i in range(self.num_candidates):
            if self.winners[i]:
                ret += [i]
        return ret, extras




########## TESTS ######
num_candidates = 150
num_spots = 25
num_voters = 50
np_data = [np.random.choice(np.arange(num_candidates), num_spots, replace=False)]
for i in range(num_voters-1):
    np_data = np.append(np_data, [np.random.choice(np.arange(num_candidates), num_spots, replace=False)], axis=0)

names = np.zeros((num_voters,), dtype='object')
for i in range(len(names)):
    names[i] = 'phil'
names = np.array([names]).T
info = np.concatenate((names, np_data), axis=1)
data = pd.DataFrame(data=info)

print(data.shape)

data.to_csv("out.csv", index=False)

data.head(10)


election = Election(num_candidates, 'out.csv')
ret, extras = election.run_election()
print(ret)
print(len(ret))
print(extras)
