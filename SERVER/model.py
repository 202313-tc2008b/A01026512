import mesa
from agents import *
from scheduler import RandomActivationByTypeFiltered

class StreetView(mesa.Model):

    description = "MESA Visualization of the street cross simulation."

    def __init__(
        self,
        num = 2,
        width=25,
        height=25,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
        pathIndex=0,
        buildingPos=[(2, 21), (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21),           (11, 21), (12, 21),                   (17, 21), (18, 21),                (21, 21), (22, 21),
                                     (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20),                   (17, 20),                          (21, 20), (22, 20),
                            (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19), (11, 19),                             (17, 19), (18, 19),                          (22, 19),
                            (2, 18), (3, 18), (4, 18), (5, 18), (6, 18),          (8, 18), (9, 18), (10, 18), (11, 18), (12, 18),                   (17, 18), (18, 18),                (21, 18), (22, 18),
                            
                            (2, 15), (3, 15), (4, 15),                   (7, 15),          (9, 15), (10, 15), (11, 15), (12, 15),                   (17, 15), (18, 15),                (21, 15), (22, 15),
                            (2, 14), (3, 14), (4, 14),                   (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14),                   (17, 14), (18, 14),                (21, 14),
                            (2, 13), (3, 13),                            (7, 13), (8, 13), (9, 13), (10, 13), (11, 13),                                       (18, 13),                (21, 13), (22, 13),
                            (2, 12), (3, 12), (4, 12),                   (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12),                   (17, 12), (18, 12),                (21, 12), (22, 12),
                            
                            
                            
                            
                            (2, 7), (3, 7), (4, 7), (5, 7),                           (8, 7), (9, 7), (10, 7), (11, 7), (12, 7),                    (17, 7), (18, 7), (19, 7), (20, 7), (21, 7), (22, 7),
                                    (3, 6), (4, 6), (5, 6),                           (8, 6), (9, 6), (10, 6), (11, 6), (12, 6),                    (17, 6),          (19, 6),          (21, 6), (22, 6),
                            (2, 5), (3, 5), (4, 5), (5, 5),                           (8, 5), (9, 5), (10, 5), (11, 5), (12, 5),
                            (2, 4), (3, 4), (4, 4), (5, 4),                           (8, 4), (9, 4), (10, 4), (11, 4), (12, 4),
                            (2, 3), (3, 3), (4, 3),                                           (9, 3), (10, 3), (11, 3), (12, 3),                    (17, 3), (18, 3), (19, 3),          (21, 3), (22, 3),
                            (2, 2), (3, 2), (4, 2), (5, 2),                           (8, 2), (9, 2), (10, 2), (11, 2), (12, 2),                    (17, 2), (18, 2), (19, 2), (20, 2), (21, 2), (22, 2)],

        parkingSpotsPos=[(10, 21), (2, 20), (12, 19), (7, 18), (8, 15), (4, 13), (12, 13), (2, 6), (5, 3), (8, 3), (18, 20), (17, 13), (18, 6), (21, 19), (22, 14), (20, 6), (20, 3)],
        roundAboutPos = [(14, 10), (15, 10), (14, 9), (15, 9)],
        trafficLightPos = [(15, 21), (16, 21), (5, 15), (6, 15), (0, 12), (1, 12), (23, 7), (24, 7), (13, 2), (14, 2), (15, 3), (16, 3), (17, 23), (17, 22), (8, 17), (8, 16), (2, 11), (2, 10), (22, 9), (22, 8), (17, 5), (17, 4), (12, 1), (12, 0)],
    ):
        super().__init__()
        # Set parameters
        # self.width = width
        # self.height = height

        self.population = num
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.pathIndex = pathIndex

        self.buildingPos = buildingPos if buildingPos else []
        self.parkingSpotsPos = parkingSpotsPos if parkingSpotsPos else []
        self.roundAboutPos = roundAboutPos if roundAboutPos else []
        self.trafficLightPos = trafficLightPos if trafficLightPos else []
        
        self.schedule = RandomActivationByTypeFiltered(self)
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
                print("Valor de r: ", r)
                print("Valor de rg: ", rg)

                x = self.parkingSpotsPos[r][0]
                y = self.parkingSpotsPos[r][1]

                xg = self.parkingSpotsPos[rg][0]
                yg = self.parkingSpotsPos[rg][1]
                pos = np.array((x, y))
                path = []
                goal = np.array((xg, yg))

                car = Car(
                    i,
                    self,
                    pos,
                    path,
                    self.pathIndex,
                    goal,
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
        for i in range(len(self.trafficLightPos)):
            x = self.trafficLightPos[i][0]
            y = self.trafficLightPos[i][1]

            pos = np.array((x, y))

            if i == 0 or i == 1 or i ==12 or i == 13 or i == 14 or i == 15 or i == 16 or i == 17 or i == 18 or i == 19 or i == 22 or i == 23:
                state = "green"
            else:
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
        self.schedule.step()

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

