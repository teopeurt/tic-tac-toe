# app/__init__.py
from flask_api import FlaskAPI, status
from flask import request, jsonify, abort, make_response
import random

# local import
from instance.config import app_config

wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6))


def checkscore(board):
    for w in wins:
        b = board[w[0]]
        if b in 'xo' and all(board[i] == b for i in w):
            print('get the winning tuple_index')
            return b, [i for i in w]
    return None, None


def format_tostring(board):
    stringboard = ''
    for x in board:
        if x not in 'xo':
            stringboard += str(' ')
        else:
            stringboard += str(x)
    return stringboard


def filter_list(board, x):
    return [ch for ch in board if ch not in x]


def my_turn(board, xo):
    empty_indexes = filter_list(board, 'xo')
    choice = random.choice(empty_indexes)
    board[int(choice)] = xo
    return board


def whoseturn(board):
    diff = len(filter_list(board, 'x')) - len(filter_list(board, 'o'))
    print(diff)
    if diff == -1:
        return 'o'
    elif diff == 1:
        return 'x'
    return None


def nomovesleft(board):
    return all(ch in 'xo' for ch in board)


def emptyboard(board):
    return all(ch not in 'xo' for ch in board)


def extract(inp):
    in_list = list(str(inp))
    if len(in_list) != 9:
        return None
    new_list = []
    for idx, ch in enumerate(in_list):
        if ch in 'xo':
            new_list.append(ch)
        else:
            new_list.append(str(idx))
    return new_list


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    @app.route('/tictoc', methods=['GET'])
    def begin():
        if 'board' in request.args:
            clean_ls = extract(request.args.get('board'))

            if not clean_ls:
                return 'bad request', 400

            if nomovesleft(clean_ls):
                return 'bad request', 400

            if emptyboard(clean_ls):
                new_board = my_turn(clean_ls, 'o')
                return format_tostring(new_board)

            turn = whoseturn(clean_ls)

            if not turn:
                return 'bad request', 400

            if turn == 'x':
                return 'bad request', 400

            if turn == 'o':
                new_board = my_turn(clean_ls, 'o')
                s = checkscore(new_board)
                if s[0]:
                    print("\n%s wins across %s" % s)
                return format_tostring(new_board)

            return str(clean_ls)
        else:
            return 'bad request', 400

    return app
