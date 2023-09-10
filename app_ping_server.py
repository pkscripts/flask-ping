from flask import Flask, render_template, jsonify
import json
import threading
import time
import ping_tracker

app = Flask(__name__)
read_api_count = False
api_call_counts = {
    'get_data': 0,
    'home': 0,
    'api3': 0,
    'api4': 0
}


# Background function
def background_task():
    time.sleep(10)
    while True:
        try:
            ping_tracker.main()
            time.sleep(120)
        except Exception as _:
            pass


# Start the background thread when the app starts
background_thread = threading.Thread(target=background_task)
background_thread.start()


def update_call_count_json():
    global read_api_count
    if not read_api_count:
        read_api_count = True
        try:
            try:
                with open('call_count.json', 'r') as json_file:
                    data = json.load(json_file)
                    for k, v in data.items():
                        api_call_counts[k] = data[k]
            except:
                data = api_call_counts                            
        except Exception as err:
            print(str(err))

    try:
        with open('call_count.json', 'w') as json_file:
            json.dump(api_call_counts, json_file, indent=4)
    except Exception as err:
        print(str(err))


@app.route('/get_call_counts', methods=['GET'])
def get_call_counts():
    try:
        return jsonify(api_call_counts)
    except FileNotFoundError:
        return jsonify({'error': 'Call count data not found'})


@app.route('/')
def index():
    api_call_counts["home"] += 1
    data = {}
    try:
        # Load JSON data from file
        with open('ping_results.json') as json_file:
            data = json.load(json_file)
    except:
        pass
    return render_template('index.html', data=data)


@app.route('/get_data')
def get_data():
    api_call_counts["get_data"] += 1
    update_call_count_json()
    data = {}
    try:
        with open('ping_results.json') as json_file:
            data = json.load(json_file)
    except:
        pass
    return json.dumps(data, sort_keys=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
