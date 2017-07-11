from __future__ import division
from vpython import *
import numpy as np

pbc_x = 40
pbc_y = 20

# vertical walls
wall1 = box (pos=vector(-pbc_x/2,0,0), length=0.5, height=pbc_y, width=4, color=color.blue)
wall2 = box (pos=vector(pbc_x/2,0,0),  length=0.5, height=pbc_y, width=4, color=color.blue)

# horizontal walls
wall3 = box (pos=vector(0,-pbc_y/2,0), length=pbc_x, height=0.5, width=4, color=color.blue)
wall4 = box (pos=vector(0,pbc_y/2,0),  length=pbc_x, height=0.5, width=4, color=color.blue)

# partition
partition = box (pos=vector(0,0,0),  length=0.5, height=pbc_y, width=4, color=vector(0.4,0.4,0.4), opacity=0.6)

# randomize velocity in x and y

vxi = np.random.uniform(-3,3)
vyi = np.random.uniform(-3,3)

ball = sphere (pos=vector(-pbc_x/4,0,0), radius=1, color=color.red)
old_x = -pbc_x/4

ball.velocity = vector(vxi,vyi,0)
dt = 0.01

average_velocity = 7

while 1:
	rate (500)
	ball.pos = ball.pos + ball.velocity*dt
	if ball.pos.x < wall1.pos.x+ball.radius or ball.pos.x > wall2.pos.x-ball.radius: 
		ball.velocity.x = -1*ball.velocity.x
	if ball.pos.y < wall3.pos.y+ball.radius or ball.pos.y > wall4.pos.y-ball.radius:
		ball.velocity.y = -1*ball.velocity.y
	total_velocity = (ball.velocity.x**2+ball.velocity.x**2+ball.velocity.x**2)**(1/2)
	if total_velocity < average_velocity:
		if (old_x < partition.pos.x and ball.pos.x > partition.pos.x) or (old_x > partition.pos.x and ball.pos.x < partition.pos.x):
			print("denied, bitch!")
			ball.pos.x = old_x
			ball.velocity.x = -1*ball.velocity.x

	old_x = ball.pos.x
