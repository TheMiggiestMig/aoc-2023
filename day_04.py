with open('day') as f: txt = f.read()

lines = txt.splitlines()
total = 0


# Determine the number of winning numbers on a given scratchcard.
def process_scratchcard(scratchcard):
    all_numbers = scratchcard.split(': ')[1].split(' | ')
    winning_numbers = all_numbers[0].split(' ')
    scratch_numbers = all_numbers[1].split(' ')
    wins = 0
    
    for win_number in winning_numbers:
        if win_number and win_number in scratch_numbers:
            wins += 1
    
    return wins


# Part 1
# Calculate the total score from the results.
results = [process_scratchcard(line) for line in lines]
print(sum([pow(2, result - 1) if result else 0 for result in results]))


# Part 2
# Work out how many cards get generated, starting from the end (since we already know the last card does not win / generate anything).
cards = [{'new_cards':0, 'scratchcard':scratchcard} for scratchcard in lines[::-1]]

for card_id, card in enumerate(cards):
    # Start with the number of cards we will generate with our win.
    card_wins = process_scratchcard(card['scratchcard'])
    
    if card_wins:
        # Add the number of cards that our generated cards will also win.
        card_wins += sum([next_card['new_cards'] for next_card in cards[card_id - card_wins : card_id]])
    card['new_cards'] = card_wins

# Add together all the cards generated in the game, plus the original lot of cards we started with.
print(sum([card['new_cards'] for card in cards]) + len(cards))
