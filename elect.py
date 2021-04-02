import dataset
import election

num_candidates = 150
num_spots = 25
num_voters = 50

dataset.make_dataset(num_candidates, num_spots, num_voters)

elect = election.Election(num_candidates, "out.csv")
ret, extras = elect.run_election()
print(ret)
print(len(ret))
print(extras)