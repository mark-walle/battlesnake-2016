## Battlesnake - Medusa

import bottle
import os

    # snake object:
    #    "id": "1234-567890-123456-7890",
    #    "name": "Well Documented Snake",
    #    "status": "alive",
    #    "message": "Moved north",
    #    "taunt": "Let's rock!",
    #    "age": 56,
    #    "health": 83,
    #    "coords": [ [1, 1], [1, 2], [2, 2] ],
    #    "kills": 4,
    #    "food": 12,
    #    "gold": 2

snakeid = 'f729b53e-3477-447d-b07e-c79d7e326c82'

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': 'green',
        'head': head_url
    }

@bottle.post('/start')
def start():
    data = bottle.request.json

    # THIS IS THE DATA WE RECEIVE: 
    # {
    #     "game": "hairy-cheese",
    #     "mode": "classic",
    #     "turn": 0,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": []
    # }

    return {
        'taunt': 'Medusa snake go!'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    move_decision = ['north', 'east', 'south', 'west']

    ourSnake = findSnake(data['snakes'])

    #returns coordinates [x, y] of nearest food
    nearestFood = findNearestFood(ourSnake, data['food'])
    
    #returns a list of blocked directions that won't run us into a wall
    wallAvoidance = avoidWall(ourSnake['coords'], data['height'], data['width'])
    for direction in wallAvoidance:
        if direction in move_decision:
            move_decision.remove(direction)
    
    #returns a list of directions blocked by self
    selfAvoidance = avoidSelf(ourSnake['coords'])
    for direction in selfAvoidance:
        if direction in move_decision:
            move_decision.remove(direction)
    
    # THIS IS THE DATA WE RECEIVE: 
    # {
    #     "game": "hairy-cheese",
    #     "mode": "classic",
    #     "turn": 4,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": [
    #         [1, 2], [9, 3], ...
    #     ]
    # }
    
    if not move_decision:
        move_decision = ['north']

    return {
        'move': move_decision[0],
        'taunt': 'Y\'all gonna get turned to stone!'
    }
    
def findSnake(snakes):
    for snake in snakes:
        if snake['id'] == snakeid:
            return snake

# Return the coords [x, y] of where the nearest food is
# Distances are calculated by calculateDistance method below
def findNearestFood(snake, foodList):
    if foodList == []:
        return []
    
    nearestFood = foodList[0]
    headLocation = snake['coords'][0]
    for food in foodList[1:]:
        if calculateDistance(food, headLocation) < calculateDistance(nearestFood, headLocation):
            nearestFood = food
            
    return nearestFood

# Calculate the distance between two coords [x1, y1], [x2, y2]
# Because diagonal is not allowed, distance formula is 
# deltaX + deltaY
# Input: two coordinates as a list of [x, y]
# Output: integer distance between coords
def calculateDistance(coord1, coord2):
    return abs( (coord1[0] - coord2[0]) + (coord1[1] - coord2[1]) )
    
# Input: list of coordinates corresponding to snake position
# Output: list of directions that are blocked by a wall
def avoidWall(coordinates, height, width):
    blockedDirections = []
    head = coordinates[0]
    if head[0] < 3:
        blockedDirections.append('west')
    if head[0] > width - 3:
        blockedDirections.append('east')
    if head[1] < 3: 
        blockedDirections.append('north')
    if head[1] > height - 3:
        blockedDirections.append('south')
        
    return blockedDirections
    
# This is a snake object

# {   "name": "Well Documented Snake",
#     "status": "alive",
#     "message": "Moved north",
#     "taunt": "Let's rock!",
#     "age": 56,
#     "health": 83,
#     "coords": [ [1, 1], [1, 2], [2, 2] ],
#     "kills": 4,
#     "food": 12,
#     "gold": 2
# }

# Input: list of coordinates corresponding to snake position
# Output: list of blocked directions
def avoidSelf(coordinates):
    blockedDirections = []
    head = coordinates[0]
    
    # we know where the head is, let's check surrounding tiles and remove conflicts
    
    #algorithm:
    # 1. create list of possible directions as a list of coords
    # 2. iterate through body and check if body coords is in list
    # 3. if it is in the list, add that direction to blockedDirections

    neighbours = {  'north': [head[0], head[1]+1],
                    'east': [head[0]+1, head[1]],
                    'south': [head[0], head[1]-1],
                    'west': [head[0]-1, head[1]]}
    
    for direction, neighbour in neighbours.items():
        if neighbour in coordinates[1:]:
            blockedDirections.append(direction)

    return blockedDirections

@bottle.post('/end')
def end():
    data = bottle.request.json
    
    # THIS IS THE DATA WE RECEIVE: 
    # {
    #     "game": "hairy-cheese",
    #     "mode": "classic",
    #     "turn": 4,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": [
    #         [1, 2], [9, 3], ...
    #     ]
    # }

    return {
        'taunt': 'Good game all!'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))