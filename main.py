import pygame, sys, random
from simulation_classes import Room

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Vacuum Cleaner Simulation")
clock = pygame.time.Clock()

# Function to randomly choose between True and False
def random_bool():
    return random.choice([True, False])

# Function to randomly choose 's' or 'l'
def random_s_l():
    return random.choice(['s', 'l'])

room1 = Room(random_bool(), random_s_l(), 10, 10)
if room1.status == 's':  # Check if room1 should have dirt
    room1.add_dirt()
room1.add_door()

room2 = Room(random_bool(), random_s_l(), 10, 10)
if room2.status == 's':  # Check if room2 should have dirt
    room2.add_dirt()
room2.add_door()

room3 = Room(random_bool(), random_s_l(), 10, 10)
if room3.status == 's':  # Check if room3 should have dirt
    room3.add_dirt()
room3.add_door()

room4 = Room(random_bool(), random_s_l(), 10, 10)
if room4.status == 's':  # Check if room4 should have dirt
    room4.add_dirt()
room4.add_door()

colors = {
    0: (255, 0, 0),  # Red for walls and obstacles
    1: (255, 255, 255),  # White for available spaces
    2: (0, 0, 255)  # Blue for dirt (you can choose your own color)
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Fill with a black background

    # Define the size and position of the rooms
    room_size = 35
    room_padding = 180
    room_spacing = 400  # Adjust the spacing between rooms

    for i, room in enumerate([room1, room2, room3, room4]):
        for y in range(room.height):
            for x in range(room.width):
                pygame.draw.rect(
                    screen,
                    colors[room.distribution_matrix[y][x]],
                    (x * room_size + room_padding + i * (room_size + room_spacing), y * room_size + room_padding,
                     room_size, room_size)
                )

    pygame.display.update()
    clock.tick(60)
