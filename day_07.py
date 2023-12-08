lines = open('day').read().splitlines()

# The scoring metric is done as follows:
# 1 instance of a card scores 0
# 2 ... (a pair) scores 1
# 3 ... (three-of-a-kind) scores 3
# 4 ... (four-of-a-kind) scores 5
# 5 ... (five-of-a-kind) scores 6
#
# What about Two Pair or Full house?
# Two Pair is just, well, two pairs (so 1 + 1, or 2).
# And a Full House is just a Pair and Three-of-a-kind (so 1 + 3, or 4)
scoring_metric = [0,1,3,5,6]
card_value = "23456789TJQKA"
card_value_joker = "J23456789TQKA"


# Calculate the value of the hand.
def hand_value(hand, jokers=False):
    cards = {}
    value = 0
    
    # Count the occurences of each card
    for card in hand:cards[card] = cards[card] + 1 if cards.get(card) else 1
    
    # If the joker rule is in place, sub it out for the card with the highest occurence.
    if jokers:
        joker_number = cards.get('J') or 0
        if joker_number and joker_number < 5:
            del cards['J']
            cards[sorted(cards.items(), key=lambda x: x[1], reverse=True)[0][0]] += joker_number
    
    # Score the hand based on the count of each card
    for card in cards.values(): value += scoring_metric[card - 1]
    
    # The hand build has far more value than the individual cards.
    value *= 10000
    
    # Add the card values at a lower level to help prevent ties.
    for card in hand:
        value *= 100
        
        if jokers:
            value += card_value_joker.index(card)
        else:
            value += card_value.index(card)
        
    return value
    
# Form the hands and calculate their value(s)
hands = []
for line in lines:
    hand, bet = line.split(' ')
    hands.append({'hand': hand,
                'bet': int(bet),
                'value': hand_value(hand),              # Part 1
                'joker_value': hand_value(hand, True)   # Part 2
    })

# Part 1
print(sum([(rank + 1) * hand['bet'] for rank, hand in enumerate(sorted(hands, key=lambda x: x['value']))]))

# Part 2
print(sum([(rank + 1) * hand['bet'] for rank, hand in enumerate(sorted(hands, key=lambda x: x['joker_value']))]))
