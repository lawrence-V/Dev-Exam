from flask import Blueprint, request, jsonify

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    args = request.args.to_dict()
    search_results = search_users(args)

    if not search_results:
        return jsonify({"message": "No matching users found"}), 404

    return jsonify(search_results), 200


def search_users(args):
    included_users = set()
    search_results = []

    for user in USERS:
        user_info = (user['name'], user['age'], user['occupation'])

        if user_info in included_users:
            continue

        if 'id' in args and user['id'] == args['id']:
            search_results.append({"priority": "id", "user": user})
            included_users.add(user_info)
        elif 'name' in args and args['name'].lower() in user['name'].lower():
            search_results.append({"priority": "name", "user": user})
            included_users.add(user_info)
        elif 'age' in args and (
            str(user['age']) == args['age'] or
            str(user['age'] + 1) == args['age'] or
            str(user['age'] - 1) == args['age']
        ):
            search_results.append({"priority": "age", "user": user})
            included_users.add(user_info)
        elif 'occupation' in args and args['occupation'].lower() in user['occupation'].lower():
            search_results.append({"priority": "occupation", "user": user})
            included_users.add(user_info)

    sorted_results = sorted(search_results, key=lambda x: (
        x['priority'] != 'id',
        x['priority'] != 'name',
        x['priority'] != 'age',
        x['priority'] != 'occupation'
    ))

    return [result['user'] for result in sorted_results]
