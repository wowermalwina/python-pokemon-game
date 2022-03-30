import csv
import os.path
import random
from datetime import datetime
import pandas
import requests
import time

start_time = datetime.now()

player_name = input("Hi there! What is your name? ")
print('Nice to meet you, {}. Welcome to the world of Pokemon! \nYour pokemon will be chosen at random'.format(
    player_name))

number_of_rounds = int(input('How many rounds would you like to play? (1, 3, 5, 7, 9))'))

while number_of_rounds not in (1,3,5,7,9):
    number_of_rounds = int(input('Sorry, number of rounds must one of the following (1, 3, 5, 7, 9). Enter again.'))
stats_list_with_name = ['name', 'id', 'height', 'weight', 'hp', 'attack', 'defence', 'special_attack',
                        'special_defence', 'speed']
stats_list = ['id', 'height', 'weight', 'hp', 'attack', 'defence', 'special_attack', 'special_defence', 'speed']
if os.path.exists('pokemon_stats.csv') != True:
    open('pokemon_stats.csv', 'x')
else:
    with open('pokemon_stats.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=stats_list_with_name)
        lines = len(list(csv_reader))
        csv_pokemon = open('pokemon_stats.csv')
        csv_pokemon.close();
        if lines != 152:
            with open('pokemon_stats.csv', 'w+', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=stats_list_with_name)
                csv_writer.writeheader()
                for pokemon_id in range(1, 152):
                    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_id)
                    response = requests.get(url)
                    pokemon = response.json()
                    rows = [{
                        'name': pokemon['name'],
                        'id': pokemon['id'],
                        'height': pokemon['height'],
                        'weight': pokemon['weight'],
                        'hp': pokemon['stats'][0]['base_stat'],
                        'attack': pokemon['stats'][1]['base_stat'],
                        'defence': pokemon['stats'][2]['base_stat'],
                        'special_attack': pokemon['stats'][3]['base_stat'],
                        'special_defence': pokemon['stats'][4]['base_stat'],
                        'speed': pokemon['stats'][5]['base_stat'],
                    }]
                    csv_writer.writerows(rows)
data_from_csv = pandas.read_csv('pokemon_stats.csv')
id = data_from_csv['id'].tolist()
sorted_id = sorted(id)
height = data_from_csv['height'].tolist()
sorted_height = sorted(height)
weight = data_from_csv['weight'].tolist()
sorted_weight = sorted(weight)
hp = data_from_csv['hp'].tolist()
sorted_hp = sorted(hp)
attack = data_from_csv['attack'].tolist()
sorted_attack = sorted(attack)
defence = data_from_csv['defence'].tolist()
sorted_defence = sorted(defence)
special_attack = data_from_csv['special_attack'].tolist()
sorted_special_attack = sorted(special_attack)
special_defence = data_from_csv['special_defence'].tolist()
sorted_special_defence = sorted(special_defence)
speed = data_from_csv['speed'].tolist()
sorted_speed = sorted(speed)

sorted_stats=[sorted_id,sorted_height,sorted_weight,sorted_hp,sorted_attack,sorted_defence,special_attack,special_defence,sorted_speed]

def ranking_generation(stats):
    rankings = []
    for stat in range(len(stats)):
        ranking=0
        while stats[stat] > sorted_stats[stat][ranking]:
            ranking +=1
        rankings.append(ranking)
    return rankings

ai_choice = input('What kind of AI do you want to play against? (easy, medium, hard)').lower().strip()

def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()
    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'hp': pokemon['stats'][0]['base_stat'],
        'attack': pokemon['stats'][1]['base_stat'],
        'defence': pokemon['stats'][2]['base_stat'],
        'special_attack': pokemon['stats'][3]['base_stat'],
        'special_defence': pokemon['stats'][4]['base_stat'],
        'speed': pokemon['stats'][5]['base_stat'],
    }


def run(difficulty):
    outcome = 'draw'
    pokemon_options = []
    hand_size=3
    print('Your choices are ', end='')
    for options in range(hand_size):
        pokemon_options.append(random_pokemon())
        print('{},'.format(pokemon_options[options]['name']),end=' ')
    user_choice = input('\nChoose your pokemon').lower().strip()
    for pokemon in pokemon_options:
        if pokemon['name']== user_choice:
            my_pokemon=pokemon
    #my_pokemon = random_pokemon()
    my_pokemon_list = []
    print('You were given {}'.format(my_pokemon['name']))
    for stat in range(len(stats_list)):
        my_pokemon_list.append(my_pokemon[stats_list[stat]])
        print('{}: {}'.format(stats_list[stat], my_pokemon_list[stat]))
    if difficulty =='player':
        stat_choice = input('Which stat do you want to use? (id, height, weight, hp, attack, speed, defence, special_attack, special_defence, speed)').lower().strip()
        print('You chose to compare the {} stat'.format(stat_choice))
    opponent_pokemon_options=[]
    for options in range(hand_size):
        opponent_pokemon_options.append(random_pokemon())
    #opponent_pokemon = random_pokemon()
    if difficulty !='player':
        if difficulty == 'easy':
            opponent_pokemon=random.choice(opponent_pokemon_options)
        elif difficulty == 'medium':
            opponent_pokemon_options_rankings=[]
            opponent_pokemon_lists = []
            for pokemon in range(hand_size):
                opponent_pokemon_list=[]
                for stat in range(len(stats_list)):
                    opponent_pokemon_list.append(opponent_pokemon_options[pokemon][stats_list[stat]])
                opponent_pokemon_lists.append(opponent_pokemon_list)
                opponent_pokemon_options_rankings.append(sum(ranking_generation(opponent_pokemon_lists[pokemon])))
            weighted_rank = random.randint(1, sum(opponent_pokemon_options_rankings))
            rank_sum = 0
            for rank in range(len(opponent_pokemon_options_rankings)):
                rank_sum += opponent_pokemon_options_rankings[rank]
                if rank_sum >= weighted_rank:
                    opponent_pokemon = opponent_pokemon_options[rank]
                    break
        elif difficulty == 'hard':
            opponent_pokemon_options_rankings=[]
            opponent_pokemon_lists=[]
            for pokemon in range(hand_size):
                opponent_pokemon_list = []
                for stat in range(len(stats_list)):
                    opponent_pokemon_list.append(opponent_pokemon_options[pokemon][stats_list[stat]])
                opponent_pokemon_lists.append(opponent_pokemon_list)
                opponent_pokemon_options_rankings.append(sum(ranking_generation(opponent_pokemon_lists[pokemon])))
            for rank in range(len(opponent_pokemon_options_rankings)):
                if max(opponent_pokemon_options_rankings) == opponent_pokemon_options_rankings[rank]:
                    opponent_pokemon = opponent_pokemon_options[rank]
    else:
        opponent_pokemon=random_pokemon()
    opponent_pokemon_list = []
    for stat in range(len(stats_list)):
        opponent_pokemon_list.append(opponent_pokemon[stats_list[stat]])
        # print('The {} is {}'.format(stats_list[stat], opponent_pokemon_list[stat]))
    print('Your opponent chose {}'.format(opponent_pokemon['name']))

    if difficulty != 'player':
        if difficulty =='easy':
            stat_choice=random.choice(stats_list)

        elif difficulty =='medium':
            opponent_pokemon_rankings = ranking_generation(opponent_pokemon_list)
            weighted_rank = random.randint(1,sum(opponent_pokemon_rankings))
            rank_sum=0
            for rank in range(len(opponent_pokemon_rankings)):
                rank_sum +=opponent_pokemon_rankings[rank]
                if rank_sum >= weighted_rank:
                    stat_choice=stats_list[rank]
                    break

        elif difficulty =='hard':
            opponent_pokemon_rankings = ranking_generation(opponent_pokemon_list)
            for rank in range(len(stats_list)):
                if max(opponent_pokemon_rankings) == opponent_pokemon_rankings[rank]:
                    stat_choice = stats_list[rank]
        #for pokemon in opponent_pokemon_options:
        #    if pokemon['name']== opponent_choice:
        #        opponent_pokemon=pokemon
        print('Your opponent chose to compare the {} stat.'.format(stat_choice))


    my_stat = my_pokemon[stat_choice]
    opponent_stat = opponent_pokemon[stat_choice]
    print("Your opponent's {} was {}".format(stat_choice, opponent_stat))
    if my_stat > opponent_stat:
        print('You win!')
        outcome = 'win'
    elif my_stat < opponent_stat:
        print('You lose...')
        outcome = 'lose'
    else:
        print('Draw.')

#    for number in range(len(stats_list)):
#        if my_stat != my_pokemon_list[number]:
#            if my_pokemon_list[number] > opponent_pokemon_list[number]:
#                print('{} would have won.'.format(stats_list[number]))
#            elif my_pokemon_list[number] < opponent_pokemon_list[number]:
#                print('{} would have lost.'.format(stats_list[number]))
#            else:
#                print('{} would have drawn.'.format(stats_list[number]))

    time.sleep(2)
    return outcome



wins = 0
losses = 0
coin_flip = random.getrandbits(1)
if coin_flip == 0:
    print('You won the coin flip, so you go first.')
    next_round_diff = 'player'
else:
    next_round_diff = ai_choice
    print('You lost the coin flip, so your opponent goes first.')
for round in range(number_of_rounds):
    print('Round {}:'.format(round+1))
    if next_round_diff == 'player':
        print('Your turn to choose.')
    else:
        print("Opponent's turn to choose")
    outcome = run(next_round_diff)
    if outcome == 'win':
        wins += 1
        next_round_diff = 'player'
    elif outcome == 'lose':
        losses += 1
        next_round_diff = ai_choice


print('The game is over, you won {} rounds and your opponent won {}'.format(wins, losses))

if wins > losses:
    print('You won!')
elif losses > wins:
    print('You lost...')
else:
    print('You drew.')

pokemon_high_scores_field_names = ['name', 'rounds', 'wins', 'losses']
if os.path.exists('pokemon_high_scores.txt') != True:
    open('pokemon_high_scores.txt', 'x')
with open('pokemon_high_scores.txt', 'a') as text_file:
    text_file.write("\nname {}, rounds {}, wins {}, losses {} ".format(player_name,number_of_rounds,wins,losses))

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
