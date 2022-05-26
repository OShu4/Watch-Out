import pygame
def start_window():
 
	pygame.init()
	GREEN = (0, 255, 0)
	# Text
	font = pygame.font.SysFont("Arial", 192)
	welcome = font.render("Pygame is great", 1, (GREEN))
	tw, th = welcome.get_size() # size of the text surface
	# Screen
	info = pygame.display.Info() # width and height
	w, h = info.current_w, info.current_h
	print(w, h)
	screen = pygame.display.set_mode((tw, th))
	clock = pygame.time.Clock()
 
 
	rx = 0
	forward = 1
	while True:
		screen.fill(0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (
				event.type == pygame.KEYDOWN and
				event.key == pygame.K_ESCAPE):
				pygame.quit()
		if rx < tw and forward == 1:
			rx += 10
			screen.blit(welcome, (-tw + rx, 0))
			if rx == tw -1:
				forward = 0
		elif forward == 0:
			rx -= 10
			screen.blit(welcome, (-tw + rx, 0))
			if rx == 0:
				forward = 1
 
		clock.tick(60)
		pygame.display.update()
	
	return screen
 
 
 
 
start_window()
