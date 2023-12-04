from collections import deque

with open('day') as f: txt = f.read()

lines = txt.splitlines()
cards = deque()
total = 0

def process_scratchcard(scratch):
    nums = scratch.split(': ')[1].split(' | ')
    win_nums = nums[0].split(' ')
    scratch_nums = nums[1].split(' ')
    wins = 0
    
    for win_num in win_nums:
        if win_num and win_num in scratch_nums:
            wins += 1
    
    return wins

# Part 1
results = [process_scratchcard(line) for line in lines]
print(sum([pow(2, result - 1) if result else 0 for result in results]))

# Part 2
cards = [[0, card] for card in lines[::-1]]
for index, card in enumerate(cards):
    card_wins = process_scratchcard(card[1])
    
    if card_wins:
        card_wins += sum([new_card[0] for new_card in cards[index - card_wins : index]])
    card[0] = card_wins

print(sum([card[0] for card in cards]) + len(cards))
