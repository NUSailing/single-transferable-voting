import pandas as pd
import numpy as np

class Election():
    '''
    runs single transferrable voting
    takes precautions in tying scenarios - tied losers or tied winners with not enough spots left
    '''
    
    def __init__(self, num_candidates, path):
        '''
        num_candidates (int): number of total candidates
        path (str): path to csv of votes num_voters rows and num_candidates+1 columns (column 0 is names)
        '''

        # read csv
        data = pd.read_csv(path)
    
        # init internals
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

        # find all potential new winners
        new_winners = set()
        for i in range(self.num_candidates):
            if self.tallies[i] != None and self.tallies[i] >= self.threshold:
                new_winners.add(i)

        # if the new winners would be too many, return the new winners as extras
        # otherwise, make them all winners (don't make tallies None yet)
        if np.sum(self.winners) + len(new_winners) > self.num_spots:
            return list(new_winners), "potential winners"
        for w in new_winners:
            self.winners[w] = True

        # if there are no new winners, find all that have minimum tally
        if len(new_winners) == 0:

            # find minimum tally
            minimum = float("inf")
            for c in range(self.num_candidates):
                if self.tallies[c] != None and self.tallies[c] < minimum:
                    minimum = self.tallies[c]
            
            # this shouldn't ever happen, but just in case
            if minimum == float("inf"):
                return "no minimum"

            # get indices of all candidates with minimum tally
            allminidcs = [c for c in range(self.num_candidates) if self.tallies[c] != None and self.tallies[c] == minimum]

            # if removing all minimum tally candidates would leave not enough candidiates to choose from
            inv = np.invert(np.isnan(self.tallies))
            if np.sum(inv) - len(allminidcs) < self.num_spots - np.sum(self.winners):

                # potential winners are candidates who are not yet winners and are not tied for losers
                potential_winners = [c for c in range(self.num_candidates) if inv[c] and c not in allminidcs]

                if np.sum(self.winners) + len(potential_winners) <= self.num_spots:
                    if np.sum(self.winners) + len(potential_winners) == self.num_spots:
                        for w in potential_winners:
                            self.winners[w] = True
                        return "clean finish"
                    # if winners + potential winners < num_spots
                    else:
                        for w in potential_winners:
                            self.winners[w] = True
                        return allminidcs, "potential winners"
                else:
                    return potential_winners, "potential winners"

            # if there will still be enough people left to choose from after removing all minimum candidates
            for c in allminidcs:

                #set loser tallies to None
                self.tallies[c] = None

                #get who voted for them
                who_voted = set()
                for v in range(self.num_voters):
                    if self.voter_states[v] < self.num_spots and self.indicator[self.voter_states[v],v,c] != 0:
                        # only add voters who have more votes (aren't exhausted)
                        who_voted.add(v)
                        self.voter_states[v] += 1

                for v in who_voted:
                    if self.voter_states[v] < self.num_spots:
                        cand = self.indicator[self.voter_states[v],v,:].nonzero()[0][0]
                        self.tallies[cand] += 1

        # if new winners and they wouldn't be too many
        else:
            for w in new_winners:
                who_voted = set()
                for i in range(self.num_voters):
                    if self.voter_states[i] < self.num_spots and self.indicator[self.voter_states[i],i,w] != 0:
                        # only add voters who have more votes
                        who_voted.add(i)
                        self.voter_states[i] += 1
                
                #get fractional vote value
                frac = (self.tallies[w] - self.threshold) / len(who_voted)

                # set winner tallies to None
                self.tallies[w] = None

                #assign fractional votes
                for v in who_voted:
                    if self.voter_states[v] < self.num_spots:
                        cand = self.indicator[self.voter_states[v], v].nonzero()[0][0]
                        self.tallies[cand] += frac


    def run_election(self):
        '''
        runs entire election iteratively
        '''

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


    def get_threshold(self):
        return self.threshold