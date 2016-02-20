import bottle
import os


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
        'color': 'red',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # THIS IS THE DATA WE RECEIVE: 
    
    # {
    #     "game": "hairy-cheese",
    #     "mode": "advanced",
    #     "turn": 0,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": [],
    #     "walls": [],  // Advanced Only
    #     "gold": []    // Advanced Only
    # }

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    # THIS IS THE DATA WE RECEIVE: 
    # {
    #     "game": "hairy-cheese",
    #     "mode": "advanced",
    #     "turn": 4,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": [
    #         [1, 2], [9, 3], ...
    #     ],
    #     "walls": [    // Advanced Only
    #         [2, 2]
    #     ],
    #     "gold": [     // Advanced Only
    #         [5, 5]
    #     ]
    # }

    return {
        'move': 'north',
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data
    
    # THIS IS THE DATA WE RECEIVE: 
    # {
    #     "game": "hairy-cheese",
    #     "mode": "advanced",
    #     "turn": 4,
    #     "height": 20,
    #     "width": 30,
    #     "snakes": [
    #         <Snake Object>, <Snake Object>, ...
    #     ],
    #     "food": [
    #         [1, 2], [9, 3], ...
    #     ],
    #     "walls": [    // Advanced Only
    #         [2, 2]
    #     ],
    #     "gold": [     // Advanced Only
    #         [5, 5]
    #     ]
    # }

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
