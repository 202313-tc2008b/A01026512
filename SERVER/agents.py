import mesa
import numpy as np
import heapq
import math
import random


class Buildings(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model, 
            pos
        ):
        super().__init__(unique_id, model)
        self.pos = pos

class ParkingSpots(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model,
            pos
        ):
        super().__init__(unique_id, model)
        self.pos = pos

class RoundAbout(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model,
            pos
        ):
        super().__init__(unique_id, model)
        self.pos = pos

class TrafficLight(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model,
            pos, 
            state
        ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state   # Green | Red
        
        def sta(self):
            if self.state == "Green":
                self.state == "Red"
            else:
                self.state == "Green"

class Street(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model, 
            pos,
            direction
        ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = direction # En que dirección pueden avanzar los autos

class Car(mesa.Agent):
    def __init__(
            self, 
            unique_id, 
            model,
            pos,
            path,
            currentPathIndex, 
            goal,
            roadDirections,
            color="purple",
        ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = path
        self.currentPathIndex = currentPathIndex  # Index to track the current position in the path
        self.goal = goal
        self.roadDirections = roadDirections
        self.color = color

    def dijkstra(self, start, goal, avoid_position=None):
        print("Dk")
        print(f"({start}, {goal})")
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.neighbors(current_node, avoid_position):
                new_cost = cost_so_far[current_node] + 1
                if (
                    next_node not in cost_so_far
                    or new_cost < cost_so_far[next_node]
                ):
                    cost_so_far[next_node] = new_cost
                    heapq.heappush(frontier, (new_cost, next_node))
                    came_from[next_node] = current_node

        # Reconstruct path from goal to start
        path = []
        current = goal
        while current != start:
            if current not in came_from:
                # Path not founded, car must wait
                return []
            current = came_from[current]
            path.append(current)

        path.reverse()

        # Last coord to path
        path.append(goal)

        return path

    def neighbors(self, node, avoid_position = None):
        available_directions = self.roadDirections[node[0]][node[1]].split(',')
        neighbors = []
        for direction in available_directions:
            new_neighbor = None
            if direction == 'north':
                new_neighbor = (node[0], node[1] + 1)
            elif direction == 'south':
                new_neighbor = (node[0], node[1] - 1)
            elif direction == 'west':
                new_neighbor = (node[0] - 1, node[1])
            elif direction == 'east':
                new_neighbor = (node[0] + 1, node[1])

            if new_neighbor and new_neighbor != avoid_position:
                neighbors.append(new_neighbor)

        neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.model.width and 0 <= y < self.model.height]
        return neighbors
    
    def set_path(self):
        start = self.pos
        end = self.goal
        print(f"{start}, {end}")
        self.path = self.dijkstra(start, end)
        self.currentPathIndex = 0
        print(f"dk path: {self.path}")

    def move(self):
        # Check if the next position has a Stop agent
        next_position = self.path[0] if self.path else self.pos
        red_lights = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, TrafficLight) and agent.state == "red" and np.array_equal(agent.pos, next_position)
        ]

        if red_lights:
            return

        # car_agents = [
        #     agent for agent in self.model.schedule.agents
        #     if isinstance(agent, Car) and agent.pos == next_position and agent != self
        # ]

        # if car_agents:
        #     print(f"Car {self.unique_id} encontró otro carro en su próxima posición.")
        #     avoid_position = car_agents[0].pos if car_agents else None
        #     alternative_path = self.find_alternative_path(avoid_position)
        #     if alternative_path != []:
        #         self.path = alternative_path
        #         print(f"Car {self.unique_id} ha encontrado un camino alternativo.")
        #     else:
        #         print(f"Car {self.unique_id} está esperando a que el otro coche se mueva.")
        #         return

        # Move along the path
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)
    
    def step(self):
        print(self.pos)
        print(self.path)
        if not self.path:
            self.set_path()
        else:
            # Check if the car has reached the end of the path
            if self.currentPathIndex < len(self.path) - 1:
                # Move to the next position in the path
                # self.currentPathIndex += 1
                # new_x, new_y = self.path[self.currentPathIndex]

                # Move the car to the new position
                # self.model.grid.move_agent(self, (new_x, new_y))
                self.move()

# class Boid(mesa.Agent):
#     """
#     A Boid-style flocker agent.

#     The agent follows three behaviors to flock:
#         - Cohesion: steering towards neighboring agents.
#         - Separation: avoiding getting too close to any other agent.
#         - Alignment: try to fly in the same direction as the neighbors.

#     Boids have a vision that defines the radius in which they look for their
#     neighbors to flock with. Their speed (a scalar) and velocity (a vector)
#     define their movement. Separation is their desired minimum distance from
#     any other Boid.
#     """

#     def __init__(
#         self,
#         unique_id,
#         model,
#         pos,
#         speed,
#         velocity,
#         vision,
#         separation,
#         cohere=0.025,
#         separate=0.25,
#         match=0.04,
#     ):
#         """
#         Create a new Boid flocker agent.

#         Args:
#             unique_id: Unique agent identifyer.
#             pos: Starting position
#             speed: Distance to move per step.
#             heading: numpy vector for the Boid's direction of movement.
#             vision: Radius to look around for nearby Boids.
#             separation: Minimum distance to maintain from other Boids.
#             cohere: the relative importance of matching neighbors' positions
#             separate: the relative importance of avoiding close neighbors
#             match: the relative importance of matching neighbors' headings
#         """
#         super().__init__(unique_id, model)
#         self.pos = np.array(pos)
#         self.speed = speed
#         self.velocity = velocity
#         self.vision = vision
#         self.separation = separation
#         self.cohere_factor = cohere
#         self.separate_factor = separate
#         self.match_factor = match

#     def cohere(self, neighbors):
#         """
#         Return the vector toward the center of mass of the local neighbors.
#         """
#         cohere = np.zeros(2)
#         if neighbors:
#             for neighbor in neighbors:
#                 cohere += self.model.space.get_heading(self.pos, neighbor.pos)
#             cohere /= len(neighbors)
#         return cohere

#     def separate(self, neighbors):
#         """
#         Return a vector away from any neighbors closer than separation dist.
#         """
#         me = self.pos
#         them = (n.pos for n in neighbors)
#         separation_vector = np.zeros(2)
#         for other in them:
#             if self.model.space.get_distance(me, other) < self.separation:
#                 separation_vector -= self.model.space.get_heading(me, other)
#         return separation_vector

#     def match_heading(self, neighbors):
#         """
#         Return a vector of the neighbors' average heading.
#         """
#         match_vector = np.zeros(2)
#         if neighbors:
#             for neighbor in neighbors:
#                 match_vector += neighbor.velocity
#             match_vector /= len(neighbors)
#         return match_vector

#     def step(self):
#         """
#         Get the Boid's neighbors, compute the new vector, and move accordingly.
#         """

#         neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
#         self.velocity += (
#             self.cohere(neighbors) * self.cohere_factor
#             + self.separate(neighbors) * self.separate_factor
#             + self.match_heading(neighbors) * self.match_factor
#         ) / 2
#         self.velocity /= np.linalg.norm(self.velocity)
#         new_pos = self.pos + self.velocity * self.speed
#         self.model.space.move_agent(self, new_pos)