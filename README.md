# single-transferable-voting

This is a program to run a single transferable voting (STV) process.  STV is a multi-winner voting system where each voter submits a ranked-choice ballot.  The specific use case for this program is the Northwestern University Sailing Team (NUST) yearly recruitment process.  These two links give a strong overview of the system:
- YouTube: https://www.youtube.com/watch?v=M91jraoo6t8
- Wikipedia: https://en.wikipedia.org/wiki/Single_transferable_vote

## file overview
`dataset.py`: Makes a random test dataset containing valid ranked choice votes.

`elect.py`: A workbook for configuring and running elections.

`election.py`: Code to execute a full STV process.  By function:
- `__init__`:
- `increment_round`:
- `run_election`:
- `get_threshold`:

# Structure of input csv

Row 0: i for i in range(num_spots)
Rows 1 - n_rows: voter, first choice, second choice, ... , (num_spots) choice

Voters **MUST** rank *as many candidates as there are spots*.
