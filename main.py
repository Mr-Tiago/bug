import pygame, sys, time, node, pathfinder, colors, os, time
from node import NodeTypes

from gui import *


pathfinder.on_checking_event.append(OnCheking)
pathfinder.on_finished_event.append(OnVisited)
mouse_down = False
remove_mode = False
draw_mode = NodeTypes.Start
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.VIDEORESIZE:
			if event.size == screen.get_size():
				break
			screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
			FillEmptyScreen()
			DrawNodes()
			DrawInfoPanel()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 5:
				ZoomOut()
			elif event.button == 4:
				ZoomIn()
			elif event.button == 1:
				mouse_down = True
				ModifyNode(pygame.mouse.get_pos(), draw_mode)
			elif event.button == 3:
				remove_mode = True
				ModifyNode(pygame.mouse.get_pos(), NodeTypes.Normal)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1: 
				mouse_down = False
			elif event.button == 3:
				remove_mode = False
		#Keyboard input
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				draw_mode = NodeTypes.Start
			elif event.key == pygame.K_e:
				draw_mode = NodeTypes.End
			elif event.key == pygame.K_o:
				draw_mode = NodeTypes.Obstacle
			elif event.key == pygame.K_w:
				draw_mode = NodeTypes.Weight
			elif event.key == pygame.K_r:
				Reset(True, True)
			elif event.key == pygame.K_PERIOD:
				if delay_time < maximum_delay:
					delay_time += 0.01
					print(delay_time)
			elif event.key == pygame.K_COMMA:
				if delay_time > minimum_delay:
					delay_time -= 0.01
					print(delay_time)
			elif event.key == pygame.K_F1:
				DrawInfoPanel()
			elif event.key == pygame.K_RETURN:
				currentTime=time.time()
				Reset(False, False)
				path = pathfinder.run_algorithm(node_list, GetStartNode(), GetEndNode())
				DrawFoundPath(path)
				totalseconds=time.time()-currentTime
				DrawDuringTime(totalseconds)
		#Modify nodes
		elif event.type == pygame.MOUSEMOTION:
			if remove_mode:
				ModifyNode(pygame.mouse.get_pos(), NodeTypes.Normal)
			elif mouse_down:
				ModifyNode(pygame.mouse.get_pos(), draw_mode)
	node_generator.UpdateRectSize(rect_size)
	DrawDelayTime()
	pygame.display.flip()
