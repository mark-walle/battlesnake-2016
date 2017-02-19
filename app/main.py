## Battlesnake - Medusa

import bottle
import os

    # snake object:
    #    "id": "1234-567890-123456-7890",
    #    "name": "Well Documented Snake",
    #    "status": "alive",
    #    "message": "Moved up",
    #    "taunt": "Let's rock!",
    #    "age": 56,
    #    "health": 83,
    #    "coords": [ [1, 1], [1, 2], [2, 2] ],
    #    "kills": 4,
    #    "food": 12,
    #    "gold": 2

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00FF00',
        'head': head_url,
        'name': 'fartbox 9000',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
    }
    
# {
#   "you": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
#   "width": 20,
#   "turn": 0,
#   "snakes": [
#     {
#       "taunt": "git gud",
#       "name": "my-snake",
#       "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
#       "health_points": 93,
#       "coords": [[0,0],[0,0],[0,0]]
#     },
#     {
#       "taunt": "gotta go fast",
#       "name": "other-snake",
#       "id": "0fd33b05-37dd-419e-b44f-af9936a0a00c",
#       "health_points": 50,
#       "coords": [[1,0],[1,0],[1,0]]
#     }
#   ],  
#   "height": 20,
#   "game_id": "870d6d79-93bf-4941-8d9e-944bee131167",
#   "food": [[1,1]],
#   "dead_snakes": [{
#       "taunt": "gotta go fast",
#       "name": "other-snake",
#       "id": "c4e48602-197e-40b2-80af-8f89ba005ee9",
#       "health_points": 50,
#       "coords": [[5,0],[5,0],[5,0]]
#   }]
# }

@bottle.post('/move')
    
def move():
    data = bottle.request.json
    move_decision = ['up', 'right', 'down', 'left']

    ourSnake = findSnake(data['snakes'],data['you'])
    
    head = ourSnake['coords'][0]
    neighbours = {  'up': [head[0], head[1]-1],
                    'right': [head[0]+1, head[1]],
                    'down': [head[0], head[1]+1],
                    'left': [head[0]-1, head[1]]}
    
    # for each possible direction, check if moving there will cause collison
    # if so, remove it from the list
    for direction, coord in neighbours.items():
        if not verifyNeighbours(data, coord):
            move_decision.remove(direction)

    #returns coordinates [x, y] of nearest food
    nearestFood = findNearestFood(ourSnake, data['food'])
    #find which directions take us closer to food
    
    if nearestFood != []:
        if nearestFood[0] < head[0] and 'left' in move_decision:
            move_decision = ['left']
        if nearestFood[0] > head[0] and 'right' in move_decision:
            move_decision = ['right']
        if nearestFood[1] > head[1] and 'down' in move_decision:
            move_decision = ['down']
        if nearestFood[1] < head[1] and 'up' in move_decision:
            move_decision = ['up']
                
    if not move_decision:
        move_decision = ['up']
    
    return {
        'move': move_decision[0],
        'taunt': 'hi'
    }
    
# Input: list of snake objects
# Output: snake object that is our snake
def findSnake(snakes,you):
    for snake in snakes:
        if snake['id'] == you:
            return snake

# Return the coords [x, y] of where the nearest food is
# Distances are calculated by calculateDistance method below
def findNearestFood(snake, foodList):
    if foodList == []:
        return []
    
    headLocation = snake['coords'][0]
    nearestFood = foodList[0]
    nearestDistance = calculateDistance(nearestFood, headLocation)
    for food in foodList[1:]:
        if calculateDistance(food, headLocation) < nearestDistance:
            nearestFood = food
            nearestDistance = calculateDistance(nearestFood, headLocation)
            
    return nearestFood

# Calculate the distance between two coords [x1, y1], [x2, y2]
# Input: two coordinates as a list of [x, y]
def calculateDistance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

# Input: our data object, coordinates of desired locatioin
# Output: return TRUE if can move there, FALSE if cannot move there
def verifyNeighbours(data, coord):
    return not isWall(data, coord) and not isSnake(data, coord)

# Checks if the desired coordinate is a wall
def isWall(data, coord):
    #check if coord is out of bounds
    if coord[0] < 0 or coord[1] < 0:
        return True
    elif coord[0] >= data['width'] or coord[1] >= data['height']:
        return True
    else:
        return False

# Checks if desired coordinate is own tail
def isSnake(data, coord):
    for snake in data['snakes']:
        if coord in snake['coords']:
            return True
    return False

@bottle.post('/end')
def end():
    data = bottle.request.json
    
    return {
        'taunt': 'Good game all!'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))