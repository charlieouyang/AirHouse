from flask import Flask, request, jsonify
import time
import json

app = Flask(__name__)

time_to_metric_data = {}

#------------------    API ENDPOINTS ------------------------

@app.route("/metric/<metric_name>/sum", methods=["GET"])
def get_metric(metric_name):
    print("Get metric for: " + metric_name)
    end_time = get_current_time_in_seconds()
    start_time = end_time - (60 * 60) #Examining the time window as 1 hour
    
    all_times = list(time_to_metric_data.keys())
    sum_of_values = 0
    
    for examine_time in reversed(all_times):
        print("Looking at time: " + str(examine_time))
        
        if examine_time <= end_time and examine_time >= start_time:
            print("Time is in range! " + str(examine_time))
            list_of_metrics = time_to_metric_data[examine_time]
            
            for metric_object in list_of_metrics:
                
                if metric_name in metric_object:
                    print("Found metric: " + metric_name)
                    print("Adding value: " + str(metric_object[metric_name]))
                    print(metric_object[metric_name])
                    sum_of_values += metric_object[metric_name]
        elif examine_time < start_time:
            print("Examine_time already out of window: " + str(examine_time))
            break
    
    print("Finished aggregating.. value: " + str(sum_of_values))
    return_obj = {
        'status': 200,
        'sum': sum_of_values
    }

    return jsonify(return_obj)


@app.route("/metric/<metric_name>", methods=["POST"])
def post_metric(metric_name):
    #Input - customer e-mail

    global time_to_metric_data

    if "value" not in request.json:
        return_obj = {
            'status': 400,
            'result': 'Please add metric_name and value to request'
        }
        return jsonify(return_obj)

    metric_value = request.json["value"]
    print("Setting key: " + metric_name)
    print("Setting value: " + str(metric_value))
    
    current_time = get_current_time_in_seconds()
    metric_object = {}
    metric_object[metric_name] = int(metric_value)
    
    print("Adding metric object: " + str(metric_object))
    #Store the metric in data
    if current_time in time_to_metric_data:
        time_to_metric_data[current_time].append(metric_object)
    else:
        time_to_metric_data[current_time] = [metric_object]
    
    print("Done.. Current state is: " + str(time_to_metric_data))

    return_obj = {
        'status': 200,
        'result': 'Metric added: ' + metric_name + ' metric_value: ' + str(metric_value)
    }

    return jsonify(return_obj)

#------------------    UTILITY FUNCTIONS ------------------------

def get_current_time_in_seconds():
    return int(time.time())

if __name__ == '__main__':
    print("Starting service")
    #app.run()
    app.run(host='0.0.0.0')
