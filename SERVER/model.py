import mesa
import csv
import random
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
        population = 1,## number of cars
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
        startendPos = [[[1, 6], [5, 3]], [[9, 22], [8, 15]]],
        streetPos = [(15, 21),(18, 17),(7, 17),(8, 0),(19, 0),(8, 9),(19, 9),(0, 5),(19, 18),(0, 14),(22, 10),(22, 19),(14, 15),(15, 7),(7, 3),(15, 16),(18, 12),(18, 21),(19, 4),(0, 0),(11, 0),(0, 9),(11, 9),(10, 22),(22, 5),(3, 1),(14, 1),(22, 14),(3, 10),(14, 19),(15, 2),(15, 11),(7, 7),(7, 16),(18, 16),(10, 8),(10, 17),(2, 22),(22, 0),(22, 9),(14, 5),(22, 18),(14, 14),(15, 6),(7, 2),(18, 11),(7, 11),(6, 15),(21, 22),(2, 8),(2, 17),(22, 4),(3, 0),(14, 0),(22, 13),(3, 9),(14, 18),(6, 10),(21, 8),(21, 17),(10, 16),(22, 8),(14, 4),(9, 11),(5, 22),(6, 5),(6, 14),(10, 11),(2, 16),(13, 13),(13, 22),(17, 1),(5, 8),(17, 10),(5, 17),(6, 0),(6, 9),(21, 16),(2, 11),(13, 8),(1, 15),(13, 17),(16, 22),(17, 5),(9, 1),(5, 12),(9, 10),(6, 4),(6, 13),(12, 20),(13, 3),(1, 10),(13, 12),(16, 8),(1, 19),(13, 21),(16, 17),(17, 0),(17, 9),(5, 16),(20, 1),(20, 10),(12, 6),(12, 15),(4, 11),(1, 5),(13, 7),(1, 14),(13, 16),(17, 4),(9, 0),(5, 11),(9, 9),(19, 13),(8, 22),(19, 22),(0, 18),(20, 5),(12, 1),(12, 10),(12, 19),(1, 0),(13, 2),(1, 9),(13, 11),(1, 18),(16, 16),(15, 20),(8, 8),(19, 8),(0, 4),(8, 17),(19, 17),(0, 13),(0, 22),(11, 22),(20, 0),(20, 9),(12, 5),(4, 1),(12, 14),(4, 10),(1, 4),(1, 13),(15, 15),(18, 20),(19, 12),(0, 8),(11, 8),(19, 21),(0, 17),(11, 17),(20, 4),(12, 0),(12, 9),(22, 22),(15, 1),(15, 10),(7, 6),(15, 19),(18, 15),(0, 3),(8, 16),(19, 16),(0, 12),(0, 21),(12, 4),(4, 0),(4, 9),(22, 17),(14, 13),(3, 22),(14, 22),(15, 5),(7, 1),(18, 1),(15, 14),(7, 10),(18, 10),(18, 19),(8, 11),(19, 11),(0, 7),(0, 16),(11, 16),(22, 3),(22, 12),(3, 8),(14, 8),(22, 21),(3, 17),(14, 17),(15, 0),(15, 9),(7, 5),(18, 5),(15, 18),(18, 14),(0, 2),(22, 7),(14, 3),(22, 16),(14, 12),(14, 21),(15, 4),(7, 0),(18, 0),(15, 13),(7, 9),(18, 9),(18, 18),(21, 11),(6, 22),(10, 1),(10, 10),(7, 8),(22, 2),(22, 11),(14, 7),(22, 20),(3, 16),(14, 16),(7, 4),(18, 4),(6, 8),(6, 17),(2, 1),(2, 10),(22, 6),(14, 2),(3, 11),(14, 11),(17, 22),(6, 3),(21, 1),(6, 12),(21, 10),(10, 0),(10, 9),(22, 1),(13, 20),(14, 6),(17, 8),(5, 15),(17, 17),(9, 22),(6, 7),(21, 5),(6, 16),(2, 0),(2, 9),(13, 6),(13, 15),(16, 11),(1, 22),(5, 1),(5, 10),(9, 8),(9, 17),(6, 2),(21, 0),(6, 11),(21, 9),(20, 22),(12, 18),(13, 1),(1, 8),(1, 17),(13, 19),(5, 14),(17, 16),(6, 6),(21, 4),(20, 8),(20, 17),(12, 13),(12, 22),(1, 3),(13, 5),(16, 1),(1, 12),(13, 14),(16, 10),(1, 21),(5, 0),(5, 9),(17, 11),(9, 16),(6, 1),(19, 20),(12, 8),(12, 17),(4, 22),(13, 0),(1, 7),(16, 5),(1, 16),(13, 18),(5, 13),(19, 15),(0, 11),(11, 11),(0, 20),(12, 3),(20, 16),(12, 12),(4, 8),(12, 21),(4, 17),(1, 2),(13, 4),(16, 0),(1, 11),(16, 9),(1, 20),(15, 22),(8, 1),(19, 1),(8, 10),(19, 10),(0, 6),(19, 19),(0, 15),(20, 11),(12, 7),(12, 16),(1, 6),(16, 4),(15, 8),(15, 17),(18, 13),(7, 22),(18, 22),(19, 5),(0, 1),(11, 1),(19, 14),(0, 10),(11, 10),(0, 19),(12, 2),(12, 11),(4, 16),(22, 15),(1, 1),(14, 20),(15, 3),(15, 12),(18, 8)]
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
        self.streetPos = streetPos if streetPos else []

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


    # def move_cars_based_on_traffic_lights(self):
    #     for agent in self.schedule.agents:
    #         if isinstance(agent, Car):
    #             if self.is_traffic_light_red(agent.pos):
    #                 # Stop the car at the red light
    #                 continue

    #             # Check if the next position is valid based on road directions
    #             next_pos = agent.path[agent.pathIndex + 1] if agent.pathIndex < len(agent.path) - 1 else agent.pos
    #             if agent.can_move(tuple(map(int, next_pos))):
    #                 agent.step()
    #             else:
    #                 # Stop the car if the next position is not valid
    #                 continue

    def make_agents(self):
        """
        Crea agentes self.population, con posiciones y direcciones iniciales aleatorias.
        """
        occupied_street = []
        # CARS
        for i in range(self.population):
            cont = True
            random_street = None
            while cont:
                random_street = random.choice(self.streetPos)
                if random_street not in occupied_street:
                    occupied_street.append(random_street)
                    cont = False

            # random_street = random.choice(self.streetPos)
            x = random_street[0]
            y = random_street[1]

            random_goal = random.choice(self.parkingSpotsPos)
            xg = random_goal[0]
            yg = random_goal[1]

            # x = self.parkingSpotsPos[r][0]
            # y = self.parkingSpotsPos[r][1]
            # x = self.startendPos[i][0][0]
            # y = self.startendPos[i][0][1]

            
            # xg = self.startendPos[i][1][0]
            # yg = self.startendPos[i][1][1]

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
            # r = self.random.randint(0, len(self.parkingSpotsPos)-1)
            # rg = self.random.randint(0, len(self.parkingSpotsPos)-1)
            # if r == rg:
            #     r = self.random.randint(0, len(self.parkingSpotsPos)-1)
            #     rg = self.random.randint(0, len(self.parkingSpotsPos)-1)
            # else:
            #     # print("Value of r: ", r)
            #     # print("Value of rg: ", rg)
                

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
        
    def update_population(self, new_population):
        current_population = len([agent for agent in self.schedule.agents if isinstance(agent, Car)])
        
        if new_population > current_population:
            additional_cars = new_population - current_population
            for i in range(additional_cars):
                self.add_car_agent()
        elif new_population < current_population:
            removed_cars = current_population - new_population
            self.remove_cars(removed_cars)

    def add_car_agent(self):
        cont = True
        random_street = None
        while cont:
            random_street = random.choice(self.streetPos)
            if random_street not in self.occupied_street:
                self.occupied_street.append(random_street)
                cont = False

        x, y = random_street[0], random_street[1]

        random_goal = random.choice(self.parkingSpotsPos)
        xg, yg = random_goal[0], random_goal[1]

        pos = (x, y)
        path = []
        goal = (xg, yg)

        car = Car(
            len([agent for agent in self.schedule.agents if isinstance(agent, Car)]),
            self,
            pos,
            path,
            self.pathIndex,
            goal,
            self.road_directions
        )

        self.grid.place_agent(car, pos)
        self.schedule.add(car)

    def remove_cars(self, num_cars):
        # Remove specified number of car agents from the model
        cars_to_remove = [agent for agent in self.schedule.agents if isinstance(agent, Car)][:num_cars]
        for car in cars_to_remove:
            self.schedule.remove(car)
            self.grid.remove_agent(car)
    
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