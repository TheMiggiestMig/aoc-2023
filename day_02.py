import numpy

with open('day') as f: txt = f.read()

lines = txt.splitlines()
max_score = {'red':12, 'green':13, 'blue':14}

# Parse the game and calculate the power of each game (while also determining if a game was possible or not).
def score_games(game_lines):
    game_results = []
    for game_index, game_line in enumerate(game_lines):
        game_score = {'red':0, 'green':0, 'blue':0}
        game_valid_value = game_index + 1
        
        game = game_line.split(': ')[1]
        
        for game_index, game_round in enumerate(game.split('; ')):
            for pull in game_round.split(', '):
                score, cube = pull.split(' ')
                score = int(score)
                
                if score > max_score[cube]:
                    game_valid_value = 0
                
                if game_score[cube] < score:
                    game_score[cube] = score
            
        game_results.append({'value': game_valid_value, 'score': game_score})
        
    return game_results
    

game_results = score_games(lines)

# Part 1
print(sum([result['value'] for result in game_results]))

# Part 2
print(sum([numpy.prod(list(result['score'].values())) for result in game_results]))
