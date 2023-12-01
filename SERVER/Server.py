# http://127.0.0.1:5000/ 

from flask_cors import CORS
from flask import Flask, request, jsonify
import threading
import mesa
import json
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from agents import *
from model import StreetView

app = Flask(__name__)
CORS(app)
current_step = 0
street = StreetView()

def street_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Car:
        portrayal["Color"] = ["#190019", "#190019", "#190019"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        
    if type(agent) is Buildings:
        portrayal["Color"] = ["#0390fc", "#0390fc", "#0390fc"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is ParkingSpots:
        portrayal["Color"] = ["#fcf803", "#fcf803", "#fcf803"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is RoundAbout:
        portrayal["Color"] = ["#5e2a03", "#5e2a03", "#5e2a03"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is TrafficLight:
        if agent.state == "green":
            portrayal["Color"] = ["#00FF00", "#00FF00", "#00FF00"]  # Green color
        elif agent.state == "red":
            portrayal["Color"] = ["#FF0000", "#FF0000", "#FF0000"]  # Red color
        else:
            portrayal["Color"] = ["#000", "#000", "#000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

# ENDPOINTS
@app.route('/start', methods = ['POST'])
def startRoute():
    global current_step
    global street

    if request.method == 'POST':
        if current_step < 1:
            if 'num' in request.form:
                num_cars = int(request.form['num'])
                if num_cars > 1:
                    street.update_population(num_cars)

            agents_info = []
            # Filter Car agents
            car_agents = [agent for agent in street.schedule.agents if isinstance(agent, Car)]
            for agent in car_agents:
                agent_data = {
                    "agent": agent.unique_id,
                    "x": agent.pos[0],
                    "z": agent.pos[1]
                }
                print(f"agent_data: {agent_data}")
                agents_info.append(agent_data)

            street.step()
            current_step += 1

            result = {"agents": agents_info}
            res = jsonify(result)
        else:
            res = "Server error"
    else:
        res = "Server error"
    print(f"Server response: {res}")
    return res

@app.route('/step', methods = ['POST', 'GET'])
def stepRoute():
    global current_step
    global street
    if request.method == 'POST':
        if 'num' in request.form:
            num_steps = int(request.form['num'])
        else:
            num_steps = 1

        for _ in range(num_steps):
            street.step()
        current_step += num_steps

        res = f'Simulation advanced by {num_steps} steps. Current step: {current_step}.'
    elif request.method == 'GET':
        res = {
            "current_step": current_step
        }
    else:
        res = "Server error"
    print(res)
    return res

@app.route('/path', methods = ['POST'])
def pathRoute():
    global current_step
    global street
    if request.method == 'POST':
        street.step()
        p = int(request.form['p'])
        car_path = [agent.path for agent in street.schedule.agents if isinstance(agent, Car) and agent.unique_id == 1]
        path = car_path[0]

        if (p >= len(path)):
            currPos = [path[len(path)-1]]
            return arrayToJSON(currPos)

        currPos = [path[p]]
        res = arrayToJSON(currPos)
    else:
        res = "Server error"
    print(res)
    return res


@app.route('/carAgents', methods = ['POST', 'GET'])
def carAgents():
    global street  # Hace referencia a la variable global boids
    if request.method == 'POST':
        cars = street.getCarPositions()
        return arrayToJSON(cars)

@app.route('/carPositions', methods = ['POST','GET'])
def carPositions():
    if request.method == 'POST':
        p = int(request.form['p'])
        path = [(12, 14), (13, 14), (13, 13), (13, 12), (12, 12), (11, 12), (10, 12), (9, 12), (8, 12), (7, 12), (7, 13), (7, 14), (6, 14), (5, 14)]
        
        if (p >= len(path)):
            currPos = [path[len(path)-1]]
            return arrayToJSON(currPos)

        currPos = [path[p]]
        return arrayToJSON(currPos)
    
def arrayToJSON(ar):
    result = []
    for i, coords in enumerate(ar):
        agent_data = {
            "agent": i + 1,
            "x": coords[0],
            "z": coords[1]
        }
        result.append(agent_data)
    return json.dumps({"agents": result})

@app.route('/buildingsPosition', methods = ['POST', 'GET'])
def buildingsPosition():
    global street  # Hace referencia a la variable global boids
    if request.method == 'POST':
        buildings = street.getBuildingsPosition()
        return arrayToJSON(buildings)

@app.route('/roundaboutPosition', methods = ['POST', 'GET'])
def roundaboutPosition():
    global street  # Hace referencia a la variable global boids

    if request.method == 'POST':
        roundabout = street.getRoundAboutPositions()
        return arrayToJSON(roundabout)

@app.route('/trafficlights-position', methods = ['POST', 'GET'])
def trafficLightsPosition():
    if request.method == 'POST':
        trafficlights = street.getTrafficLightPositions()
        return arrayToJSON(trafficlights)

@app.route('/trafficlights-state', methods=['GET'])
def get_traffic_lights_state():
    traffic_lights_state = {
        f"TrafficLight_{i}": agent.state for i, agent in enumerate(street.schedule.agents) if isinstance(agent, TrafficLight)
    }
    return jsonify(traffic_lights_state)

def arrayToJSON(ar):
    result = []
    for i, coords in enumerate(ar):
        agent_data = {
            "agent": i + 1,
            "x": coords[0],
            "z": coords[1]
        }
        result.append(agent_data)
    return json.dumps({"agents": result})

def run_flask():
    app.run(port=8522, use_reloader=False)

canvas_element = mesa.visualization.CanvasGrid(street_portrayal, 24, 24, 600, 600)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Buildings", "Color": "#0390fc"},
        {"Label": "ParkingSpots", "Color": "#fcf803"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("- Parameters -"),
    "buildings": mesa.visualization.StaticText("Buildings (Blue)"),
    "parkingSpots": mesa.visualization.StaticText("Parking Spots (Yellow)"),
}

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

server = mesa.visualization.ModularServer(
    StreetView, [canvas_element, chart_element], "Street Mesa Simulation", model_params
)
server.port = 8521
server.launch(open_browser=True)

flask_thread.join()

