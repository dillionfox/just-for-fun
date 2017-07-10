from __future__ import division
from vpython import *
import numpy as np
import os

pbc_x = 40
pbc_y = 20
thickness = -.5
n = 15
dt = 0.01
vmax = 3

# vertical walls
wall1 = box (pos=vector(-pbc_x/2,0,0), length=thickness, height=pbc_y, width=4, color=color.blue)
wall2 = box (pos=vector(pbc_x/2,0,0),  length=thickness, height=pbc_y, width=4, color=color.blue)
# horizontal walls
wall3 = box (pos=vector(0,-pbc_y/2,0), length=pbc_x, height=thickness, width=4, color=color.blue)
wall4 = box (pos=vector(0,pbc_y/2,0),  length=pbc_x, height=thickness, width=4, color=color.blue)
# partition
partition = box (pos=vector(0,0,0),  length=0.5, height=pbc_y, width=4, color=vector(0.4,0.4,0.4), opacity=0.6)

def update(ball,old_x,i):
	ball.pos = ball.pos + ball.velocity*dt
	if ball.pos.x < wall1.pos.x+ball.radius or ball.pos.x > wall2.pos.x-ball.radius: 
		ball.velocity.x = -1*ball.velocity.x
	if ball.pos.y < wall3.pos.y+ball.radius or ball.pos.y > wall4.pos.y-ball.radius:
		ball.velocity.y = -1*ball.velocity.y
	total_velocity = (ball.velocity.x**2+ball.velocity.x**2+ball.velocity.x**2)**(1/2)
	if total_velocity < average_velocity:
		if (old_x[i] < partition.pos.x and ball.pos.x > partition.pos.x):
			ball.pos.x = old_x[i]
			ball.velocity.x = -1*ball.velocity.x
	if old_x[i] > partition.pos.x and ball.pos.x < partition.pos.x:
		ball.pos.x = old_x[i]
		ball.velocity.x = -1*ball.velocity.x
	old_x[i] = ball.pos.x
	return [ball,old_x]

particles = []
xi = []
yi = []
vxi = []
vyi = []
old_x = []

colors = [vector(1,0,0), vector(0,1,0), vector(0,0,1)]

for i in range(n):
	xi.append(np.random.uniform(-pbc_x/4+thickness,partition.pos.x-2*thickness))
	yi.append(np.random.uniform(-pbc_y/4+thickness,pbc_y/4-thickness))
	vxi.append(np.random.uniform(-vmax,vmax))
	vyi.append(np.random.uniform(-vmax,vmax))
	ball = sphere (pos=vector(xi[i],yi[i],0), radius=0.5, color=colors[0])
	ball.velocity = vector(vxi[i],vyi[i],0)
	particles.append(ball)

average_velocity = 0.3*vmax**2
old_x = xi

while 1:
	rate (500)
	i = 0
	for ball in particles:
		[ball,old_x] = update(ball,old_x,i)
		particles[i] = ball
		i+=1

