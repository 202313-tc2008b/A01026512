import mesa
import csv
from agents import *
from scheduler import RandomActivationByTypeFiltered

class StreetView(mesa.Model):

    description = "MESA Visualization of the street cross simulation."

    def load_road_directions(self, filename="direcciones.csv"):
        directions = []

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            rows = list(reader)

            for col in range(1, len(rows[0])):  # Iterate over columns, starting from the second column
                direction_col = [row[col].strip() for row in rows]
                direction_col.reverse()  # Invertir el orden de los datos en cada subarray
                directions.append(direction_col)

        return directions

    def __init__(
        self,
        population = 2,## number of cars
        width=24,
        height=24,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
        pathIndex=0,
        buildingPos=[(2, 2),(2, 3), (2, 4),(2, 5),(2, 7),(3, 2),(3, 3),(3, 4),(3, 5),(3, 6),(3, 7),(4, 2),(4, 3),(4, 4),(4, 5),(4, 6),(4, 7),(5, 2),(5, 4),(5, 5),(5, 6),(5, 7),(8, 2),(8, 4),
                     (8, 5),(8, 6),(8, 7),(9, 2),(9, 3),(9, 4),(9, 5),(9, 6),(9, 7),(10, 2),(10, 3),(10, 4),(10, 5),(11, 5),(11, 2),(11, 3),(11, 4),(11, 6),(11, 7),(10, 6),(10, 7),(2, 12),
                     (2, 13),(2, 14),(2, 15),(3, 12),(3, 13),(3, 14),(3, 15),(4, 12),(4, 14),(4, 15),(7, 12),(7, 13),(7, 14),(7, 15),(8, 12),(8, 13),(8, 14),(9, 12),(9, 13),(9, 14),(9, 15),(10, 12),
                     (10, 13),(10, 14), (10, 15),(11, 12), (11, 14),(11, 15), (2, 18),(2, 19),(2, 21),(3, 18),(3, 19),(3, 20),(3, 21),(4, 18),(4, 19),(4, 20),(4, 21),(5, 18),(5, 19),(5, 20),
                     (5, 21),(6, 19),(6, 20),(6, 21),(7, 18),(7, 19),(7, 20),(7, 21),(8, 18),(8, 19),(8, 20),(8, 21),(9, 18),(9, 19),(9, 20),(10, 18),(10, 19),(10, 20),(10, 21),(11, 18),(11, 20),(11, 21),
                     (16, 2),(16, 3),(17, 2),(17, 3),(18, 2),(18, 3),(19, 2),(20, 2),(20, 3),(21, 2),(21, 3),(16, 6),(16, 7),(17, 7),(18, 6),(18, 7),(19, 7),(20, 6),(20, 7),(21, 6),(21, 7),(16, 12),
                     (16, 14),(16, 15),(17, 12),(17, 13),(17, 14),(17, 15),(20, 12),(20, 13),(20, 14),(20, 15),(21, 12),(21, 13),(21, 15),(16, 18),(16, 19),(16, 20),(16, 21),(17, 18),(17, 19),(17, 21),
                     (20, 18),(20, 20), (20, 21),(21, 18),(21, 19),(21, 20),(21, 21),(13, 9),(13, 10),(14, 9),(14, 10)],

        parkingSpotsPos=[ (9, 21),(2, 20), (17, 20),(11, 19), (20, 19),(6, 18), (8, 15),(21, 14), (4, 13),(11, 13), (16, 13),(2, 6), (17, 6),(19, 6), (5, 3),(8, 3), (19, 3)],
        roundAboutPos = [(14, 10), (13, 10), (14, 9), (13, 9)],
        trafficLightPos = [ (14, 21), (15, 21), (0, 12), (1, 12), (12, 2), (13, 2), (14, 3), (15, 3), (22, 7), (23, 7), (5, 15), (6, 15), 
                           (16, 22), (16, 23), (2, 11), (2, 10), (21, 8), (21, 9), (11, 0), (11, 1), (16, 4), (16, 5), (21, 8), (21, 9), (7, 16), (7, 17)],
        startendPos = [[[1, 6], [5, 3]], [[9, 22], [8, 15]]]
    ):
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.schedule = RandomActivationByTypeFiltered(self)
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.pathIndex = pathIndex

        self.buildingPos = buildingPos if buildingPos else []
        self.parkingSpotsPos = parkingSpotsPos if parkingSpotsPos else []
        self.roundAboutPos = roundAboutPos if roundAboutPos else []
        self.trafficLightPos = trafficLightPos if trafficLightPos else []
        self.road_directions = self.load_road_directions()
        self.startendPos = startendPos if startendPos else []

        
        
        # self.space = mesa.space.ContinuousSpace(width, height, True)
        self.factors = {"cohere": cohere, "separate": separate, "match": match}
        
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Buildings": lambda b: b.schedule.get_type_count(Buildings),
                "Parking Spots": lambda p: p.schedule.get_type_count(ParkingSpots),
                "Round About": lambda r: r.schedule.get_type_count(RoundAbout),
                "Traffic Lights": lambda t: t.schedule.get_type_count(TrafficLight),
            }
        )

        self.make_agents()
        self.running = True
        self.datacollector.collect(self)


    def move_cars_based_on_traffic_lights(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Car):
                if self.is_traffic_light_red(agent.pos):
                    # Stop the car at the red light
                    continue

                # Check if the next position is valid based on road directions
                next_pos = agent.path[agent.currentPathIndex + 1] if agent.currentPathIndex < len(agent.path) - 1 else agent.pos
                if agent.can_move(tuple(map(int, next_pos))):
                    agent.step()
                else:
                    # Stop the car if the next position is not valid
                    continue

    def make_agents(self):
        """
        Crea agentes self.population, con posiciones y direcciones iniciales aleatorias.
        """
        # CARS

        for i in range(self.population):
            r = self.random.randint(0, len(self.parkingSpotsPos)-1)
            rg = self.random.randint(0, len(self.parkingSpotsPos)-1)
            if r == rg:
                r = self.random.randint(0, len(self.parkingSpotsPos)-1)
                rg = self.random.randint(0, len(self.parkingSpotsPos)-1)
            else:
                print("Value of r: ", r)
                print("Value of rg: ", rg)

                # x = self.parkingSpotsPos[r][0]
                # y = self.parkingSpotsPos[r][1]
                x = self.startendPos[i][0][0]
                y = self.startendPos[i][0][1]

                # xg = self.parkingSpotsPos[rg][0]
                # yg = self.parkingSpotsPos[rg][1]
                xg = self.startendPos[i][1][0]
                yg = self.startendPos[i][1][1]

                pos = (x, y)
                path = []
                goal = (xg, yg)

                car = Car(
                    i,
                    self,
                    pos,
                    path,
                    self.pathIndex,
                    goal,
                    self.road_directions
                )

                self.grid.place_agent(car, pos)
                self.schedule.add(car)

        # BUILDINGS
        for i in range(len(self.buildingPos)):
            x = self.buildingPos[i][0]
            y = self.buildingPos[i][1]

            pos = np.array((x, y))

            building = Buildings(
                i + self.population,
                self,
                pos,
            )
                
            self.grid.place_agent(building, pos)
            self.schedule.add(building)

        # PARKING SPOTS
        for i in range(len(self.parkingSpotsPos)):
            x = self.parkingSpotsPos[i][0]
            y = self.parkingSpotsPos[i][1]

            pos = np.array((x, y))

            parkingSpot = ParkingSpots(
                i + self.population + len(self.buildingPos),
                self,
                pos,
            )
                
            self.grid.place_agent(parkingSpot, pos)
            self.schedule.add(parkingSpot)

        # ROUNDABOUT
        for i in range(len(self.roundAboutPos)):
            x = self.roundAboutPos[i][0]
            y = self.roundAboutPos[i][1]

            pos = np.array((x, y))

            roundabout = RoundAbout(
                i + self.population + len(self.buildingPos) + len(self.parkingSpotsPos),
                self,
                pos,
            )
                
            self.grid.place_agent(roundabout, pos)
            self.schedule.add(roundabout)

        # TRAFFIC LIGHTS

        green_traffic_light_positions = [(14, 21), (15, 21), (0, 12), (1, 12), (12, 2), (13, 2), (14, 3), (15, 3), (22, 7), (23, 7), (5, 15), (6, 15)]
        red_traffic_light_positions = [(16, 22), (16, 23), (2, 11), (2, 10), (21, 8), (21, 9), (11, 0), (11, 1), (16, 4), (16, 5), (21, 8), (21, 9), (7, 16), (7, 17)]

        for i in range(len(self.trafficLightPos)):
            x = self.trafficLightPos[i][0]
            y = self.trafficLightPos[i][1]

            pos = np.array((x, y))

            if any(np.array_equal(pos, green_pos) for green_pos in green_traffic_light_positions):
                state = "green"
            elif any(np.array_equal(pos, red_pos) for red_pos in red_traffic_light_positions):
                state = "red"
            else:
                # Set default state if not specified
                state = "red"

            trafficlight = TrafficLight(
                i + self.population + len(self.buildingPos) + len(self.parkingSpotsPos) + len(self.roundAboutPos),
                self,
                pos,
                state,
            )
            
            self.grid.place_agent(trafficlight, pos)
            self.schedule.add(trafficlight)
        

    def step(self):
        if self.schedule.steps % 5 == 0:
            for agent in self.schedule.agents:
                if isinstance(agent, TrafficLight):
                    if agent.state == "green":
                        agent.state = "red"
                    else:
                        agent.state = "green"

        self.schedule.step()
        self.datacollector.collect(self)

    def getCarPositions(self):
        car_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, Car):
                car_positions.append(agent.pos.tolist())
        return car_positions

    def getBuildingsPosition(self):
        building_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, Buildings):
                building_positions.append(agent.pos.tolist())
        return building_positions

    def getRoundAboutPositions(self):
        roundabout_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, RoundAbout):
                roundabout_positions.append(agent.pos.tolist())
        return roundabout_positions

    def getTrafficLightPositions(self):
        trafficlight_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, TrafficLight):
                trafficlight_positions.append(agent.pos.tolist())
        return trafficlight_positions