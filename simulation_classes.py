import random, pygame, sys

class Room():
    def __init__(self, people,status,width, height):
        self.people = people
        self.status = status
        self.width = width
        self.height = height
        self.door = (self.height-1, self.width//2)
        self.distribution_matrix = [[0 if (i == 0 or i == width - 1  or j == 0 or j == height - 1) else 1 for i in range(width)] for j in range(height)]

    def add_door(self):
        middle = self.width // 2
        self.distribution_matrix[self.height - 1][middle] = 1

    def add_dirt(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.distribution_matrix[i][j] == 1:
                    if random.random() < 0.5:  # Adjust the probability as needed
                        self.distribution_matrix[i][j] = 2

room = Room(False,'s',10, 10)
room.add_door()
  # Adjust the width and height as needed
for row in room.distribution_matrix:
    print(row)