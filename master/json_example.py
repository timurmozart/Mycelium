from flask import Flask, request #import main Flask class and request object

app = Flask(__name__) #create the Flask app

@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
    example = req_data['examples'][0] #an index is needed because of the array
    boolean_test = req_data['boolean_test']
    print('**************************************')
    print(type(req_data))
    print('**************************************')
    global_data.append(req_data)
    print('**************************************')
    print(type(global_data))
    print('**************************************')
    print(global_data)
    print('**************************************')

    # return requests.post('http://0.0.0.0:5001/json-example').global_data
    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)
