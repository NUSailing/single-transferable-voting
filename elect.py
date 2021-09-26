import election

num_candidates = 150
num_spots = 25
num_voters = 50

# dataset.make_dataset(num_candidates, num_spots, num_voters)

# name = "out.csv"
# #name = "custom.csv"

# elect = election.Election(num_candidates, name)
# ret, extras = elect.run_election()
# print(ret)
# print(len(ret))
# print(extras)



###
num_candidates = 13

elect = election.Election(num_candidates, "/Users/agdelesseps/NUGD/Responsibilities/Sailing/STV/elections_men_2.csv")
ret, extras = elect.run_election()


print(ret)
print(len(ret))
print(extras)


# elect2 = election.Election(15, "~/Desktop/tE2.csv")
# print(elect2.num_candidates)

# ret2, extras2 = elect2.run_election()
# print(ret2)
# print(len(ret2))
# print(extras2)

