from flask import Flask
from config import *
from functions import *

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_media():
    try:
        request_name = request.args.get('name')
        request_type = request.args.get('type')
        request_many = request.args.get('many')

        data = []

        if request_many:
            for name, type_ in request_many.items():
                data.append({name: type_})
        else:
            data.append({request_name: request_type})

        for name, type_ in data.items():
            response = None

            if not media_collection.find_one({'name': name, 'type': type_}):
                return jsonify({'error': 'Media already exists'}), 400

            if type_ == 'anime':
                response = scrape_anime(name)
                response['watch_status'] = 'None'
            elif type_== 'manga':
                response = scrape_manga(name)
                response['read_status'] = 'None'
            response['rating'] = 0

            equal = compare_json(response, type_)
            if equal:
                media_collection.insert_one(response)

        return jsonify({'success': 'Media successfully added'}), 200

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

# Always return list
@app.route('/get', methods=['GET'])
def get_media():
    try: 
        request_type = request.args.get('type')
        request_name = request.args.get('name')
        request_json = request.json
        response = None

        if 'genres' in request_json:
            if request_type:
                response = [x for x in media_collection.find({'type': request_type, 'genres': request_json['genres']})]
                return jsonify({'media': [response]}), 200
            response = [x for x in media_collection.find({'genres': request_json['genres']})]
            return jsonify({'media': [response]}), 200
        if 'status' in request_json:
            if request_name and request_type:
                response = [x for x in media_collection.find({'name': request_name, 'type': request_type, 'status': request_json['status']})]
                return jsonify({'media': [response]}), 200
            if request_name:
                response = [x for x in media_collection.find({'name': request_name, 'status': request_json['status']})]
                return jsonify({'media': [response]}), 200
            if request_type:
                response = [x for x in media_collection.find({'type': request_type, 'status': request_json['status']})]
                return jsonify({'media': [response]}), 200
            response = [x for x in media_collection.find({'status': request_json['status']})]
            return jsonify({'media': [response]}), 200
        if 'authors' in request_json:
            response = [x for x in media_collection.find({'authors': request_json['authors']})]
            return jsonify({'media': [response]}), 200
        if 'alternate_titles' in request_json:
            if request_name and request_type:
                response = [x for x in media_collection.find({'name': request_name, 'type': request_type, 'alternate_titles': request_json['alternate_titles']})]
                return jsonify({'media': [response]}), 200
            if request_name:
                response = [x for x in media_collection.find({'name': request_name, 'alternate_titles': request_json['alternate_titles']})]
                return jsonify({'media': [response]}), 200
            if request_type:
                response = [x for x in media_collection.find({'type': request_type, 'alternate_titles': request_json['alternate_titles']})]
                return jsonify({'media': [response]}), 200
            response = [x for x in media_collection.find({'alternate_titles': request_json['alternate_titles']})]
            return jsonify({'media': [response]}), 200

        if request_type and request_name:
            response = media_collection.find_one({'name': request_name, 'type': request_type})
            return jsonify({'media': [response]}), 200
        elif request_type:
            response = [x for x in media_collection.find({'type': request_type})]
            return jsonify({'media': response}), 200
        elif request_name:
            response = [x for x in media_collection.find({'name': request_name})]
            return jsonify({'media': response}), 200
        else:
            response = [x for x in media_collection.find()]
            return jsonify({'media': response}), 200
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

# GET method for single object and POST for updating an item
# Must pass in name, type
# Pass scrape_update=true in args for auto or a json for manual update
@app.route('/update', methods=['GET', 'POST'])
def update_media():
    try:
        request_name = request.args.get('name')
        request_type = request.args.get('type')

        if not request_name or not request_type:
            return jsonify({'error': 'Must provide both name and type'}), 400
            
        # POST method requires both name and type and will either scrape for
        # update or use manually entered data
        if request.method == 'POST':
            scrape_update = request.args.get('scrape_update')

            if not media_collection.find_one({'name': request_name, 'type': request_type}):
                return jsonify({'error': 'No entry to update'}), 400

            if scrape_update:
                response = None

                item = media_collection.find_one({'name': request_name, 'type': request_type})
                if request_type == 'anime':
                    response = scrape_anime(request_name)
                    response['watch_status'] = item['watch_status']
                elif request_type == 'manga':
                    response = scrape_manga(request_name)
                    response['read_status'] = item['read_status']
                response['rating'] = item['rating']

                if not response:
                    return jsonify({'error': 'Media not found'}), 400

                # verify integrity
                equal = compare_json(response, request_type)
                if equal:
                    media_collection.remove({'name': request_name, 'type': request_type})
                    media_collection.insert_one(response)
                    return jsonify({'success': 'Media successfully added'}), 200
                return jsonify({'error': 'JSON format invalid'}), 400
            else:
                request_json = request.json

                media_collection.remove({'name': request_name, 'type': request_type})
                
                equal = compare_json(request_json, request_type)
                
                if equal:
                    media_collection.insert_one(request_json)
                    return jsonify({'success': 'Media successfully added'}), 200
                return jsonify({'error': 'JSON format invalid'}), 400

        # GET method requires both a name and type and will return one
        elif request.method == 'GET':
            response = media_collection.find_one({'name': request_name, 'type': request_type})
            if response:
                return jsonify(response), 200
            return jsonify({'error': 'Media not found'}), 400

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)