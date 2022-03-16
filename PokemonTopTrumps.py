import random

import requests

player = input("Hi there! What is your name? ")
print('Nice to meet you, {}. Welcome to the world of Pokemon! \nYour pokemon will be chosen at random'.format(player))

def random_pokemon ():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()
    return  {
    'name': pokemon['name'],
    'id': pokemon['id'],
    'height': pokemon['height'],
    'weight': pokemon['weight'],
    'hp': pokemon['stats'][0]['base_stat'],
    'attack':pokemon['stats'][1]['base_stat'],
    'defence':pokemon['stats'][2]['base_stat'],
    'special_attack': pokemon['stats'][3]['base_stat'],
    'special_defence': pokemon['stats'][4]['base_stat'],
    'speed': pokemon['stats'][5]['base_stat'],
    }

def run ():
    my_pokemon = random_pokemon()
    stats_list = ['id', 'height', 'weight', 'hp', 'attack', 'defence', 'special_attack', 'special_defence', 'speed']
    my_pokemon_list = []
    for stat in range(len(stats_list)):
        my_pokemon_list.append(my_pokemon[stats_list[stat]])
        print('The {} is {}'.format(stats_list[stat],my_pokemon_list[stat]))
    print('You were given {}'.format(my_pokemon['name']))
    stat_choice = input('Which stat do you want to use? (id, height, weight, hp, attack, speed, defence, special_attack, special_defence, speed)' + ' ').lower().strip()
    print('{}, You chose to compare the {} stat'.format(player, stat_choice))
    opponent_pokemon = random_pokemon()
    opponent_pokemon_list=[]
    for stat in range(len(stats_list)):
        opponent_pokemon_list.append(opponent_pokemon[stats_list[stat]])
        print('The {} is {}'.format(stats_list[stat], opponent_pokemon_list[stat]))
    print('Your opponent were given {}'.format(opponent_pokemon['name']))
    my_stat = my_pokemon[stat_choice]
    opponent_stat = opponent_pokemon[stat_choice]
    if my_stat > opponent_stat:
        print('You Win!')
    elif my_stat < opponent_stat:
        print('You Lose!')
    else:
        print('Draw!')

    for number in range(len(stats_list)):
        if my_stat != my_pokemon_list[number]:
            if my_pokemon_list[number] > opponent_pokemon_list[number]:
                print('{} would have won.'.format(stats_list[number]))
            elif my_pokemon_list[number] < opponent_pokemon_list[number]:
                print('{} would have lost.'.format(stats_list[number]))
            else :
                print('{} would have drawn.'.format(stats_list[number]))


run()
