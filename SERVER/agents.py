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
            pathIndex,
            goal,
            roadDirections,
            color="purple",
        ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = path
        self.pathIndex = pathIndex  # Index to track the current position in the path
        self.goal = goal
        self.roadDirections = roadDirections
        self.color = color

    def dijkstra(self, start, end, avoid_position=None):
        print("Dijkstra")
        print(f"Setting path from {start} to {end}")
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == end:
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

        # Reconstruct path from end to start
        path = []
        current = end
        while current != start:
            if current not in came_from:
                # Path not founded, car must wait
                return []
            current = came_from[current]
            path.append(current)

        path.reverse()

        # Last coord to path
        path.append(end)

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
    
    def set_new_path(self, avoid_position):
        start = self.pos
        goal = self.goal
        return self.dijkstra(start, goal, avoid_position)
    
    def set_path(self):
        start = self.pos
        goal = self.goal
        self.path = self.dijkstra(start, goal)
        # self.pathIndex = 0
        print(f"Dijkstra path: {self.path}")

    def move(self):
        # Check if the next position has a Stop agent
        next_position = self.path[0] if self.path else self.pos

        red_lights = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, TrafficLight) and agent.state == "red" and np.array_equal(agent.pos, next_position)
        ]
        if red_lights:
            return

        cars = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, Car) and agent.pos == next_position and agent != self
        ]
        if cars:
            print(f"Setting new path")
            avoid_position = cars[0].pos if cars else None
            new_path = self.set_new_path(avoid_position)
            if new_path != []:
                self.path = new_path
                print(f"New path: {new_path}")
            else:
                print(f"New path: {new_path}")
                return

        if self.path:
            next_position = self.path.pop(0)
            # self.pathIndex += 1
            self.model.grid.move_agent(self, next_position)
    
    def step(self):
        print(f"Current position: {self.pos}")
        print(f"Current path: {self.path}")
        if not self.path:
            self.set_path()
            # if self.pathIndex > 0:
            #     next_position = self.goal
            #     self.model.grid.move_agent(self, next_position)

            # next_position = self.goal
            # self.model.grid.move_agent(self, next_position)
        else:
            if self.pathIndex < len(self.path) - 1:
                self.move()