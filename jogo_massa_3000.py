"""
Universidade de Brasilia
Instituto de Ciencias Exatas
Departamento de Ciencia da Computacao
Algoritmos e Programação de Computadores – 2/2023
Turma: Prof. Carla Castanho e Prof. Frank Ned

Aluno(a): Giovanni Daldegan
Matricula: 232002520
Projeto Final - Parte 1
Descricao: o código a seguir apresenta um menu no terminal que dá
           acesso ao jogo do projeto. O jogo consiste em desviar
           de projéteis letais enquanto se coleta combustível pa-
           ra abastecer a nave do jogador. Atirar nos projéteis
           mortais (vermelhos) aumenta a pontuação.
"""


import os, pygame, random

clear = lambda: os.system('clear')

SETTINGS = {
	"fps":		60,
	"gridSize":	[135, 10],
	"unitSize":	14,
	"run": 		False
}

options = ["Jogar", "Configurações", "Ranking", "Instruções", "Sair"]
COLORS = {
	"vermelho": 	"#DB1515",
	"azul":			"#3755DB",
	"verde":		"#4ADA67",
	"verde-escuro":	"#2F8A4D",
	"branco":		"#FFFFFF",
	"preto":		"#000000",
}


def menu():
	clear()
	print(f"{'#'*25}\n#{'Jogo massa 3000':^23}#\n#{' '*23}#\n#{'Giovanni Daldegan':^23}#\n#{'UnB | CIC':^23}#\n#{'2023.2':^23}#\n{'#'*25}")

	input()

	while True:
		clear()

		for i in range(len(options)):
			print(f"{i+1} - {options[i]}")

		inp = input()

		clear()

		match inp:
			case "1":
				print("O jogo já está rodando!")
				game()

			case "2":
				print(f"Configurações\n\nFPS: {SETTINGS['fps']}\nTamanho da matriz: {SETTINGS['gridSize'][1]}x{SETTINGS['gridSize'][0]}\nTamanho da célula: {SETTINGS['unitSize']}x{SETTINGS['unitSize']}")
				input()
				

			case "3":
				print("Ranking\n\n\tSerá implementado em breve :)\n")
				input()

			case "4":
				print("Instruções\n\n> Controles:\n\nSeta para cima:\t\tmove para cima\nSeta para baixo:\tmove para baixo\nEspaço:\t\t\tatira\n\n> Regras do jogo:\n\nConsumo de combustível\nFicar parado:\t1\nMover:\t\t2\nAtirar:\t\t3\n\nSó é possível executar 1 ação de cada vez\n\n!! ATENÇÃO !!\nO jogo foi programado em um sistema Linux. Talvez haja problemas de compatibilidade com outros sistemas operacionais!")
				input()

			case "5":
				exit()

def game():
	SETTINGS["screenSize"] = [SETTINGS["gridSize"][0] * SETTINGS["unitSize"], SETTINGS["gridSize"][1] * SETTINGS["unitSize"]]
	SETTINGS["run"] = True

	grid = []
	for i in range(SETTINGS["gridSize"][1]):
		l = []
		for j in range(SETTINGS["gridSize"][0]):
			l.append(" ")

		grid.append(l)

	grid[SETTINGS["gridSize"][1] // 2][0] = "+"

	playerInfo = {
		"alive":	True,
		"posY":		SETTINGS["gridSize"][1] // 2,
		"points":	0,
		"fuel":		400,
		"action":	False,
		"cooldown":	0
	}

	# initialize pygame
	pygame.init()

	SCREEN = pygame.display.set_mode(SETTINGS["screenSize"])
	pygame.display.set_caption("Projeto APC")
	clock = pygame.time.Clock()

	path = os.path.dirname(os.path.realpath(__file__))

	fonts = {
		"font0": pygame.font.Font(os.path.join(path, "Pixeltype.ttf"), 65),
		"font1": pygame.font.Font(os.path.join(path, "Pixeltype.ttf"), 30)
	}

	lastGameTick = pygame.time.get_ticks()

	SCREEN.fill("#000000")

	while SETTINGS["run"]:
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				SETTINGS["run"] = False

			playerInfo["action"] = False

			# Input
			if event.type == pygame.KEYDOWN:

				if playerInfo["alive"]:
					match event.key:

						case pygame.K_UP:
							if playerInfo["posY"] != 0:
								grid[playerInfo["posY"]][0] = " "
								grid[playerInfo["posY"] - 1][0] = "+"

								playerInfo["posY"] -= 1

								playerInfo["fuel"] -= 2
								playerInfo["action"] = True

						case pygame.K_DOWN:
							if playerInfo["posY"] != len(grid) - 1:
								grid[playerInfo["posY"]][0] = " "
								grid[playerInfo["posY"] + 1][0] = "+"

								playerInfo["posY"] += 1

								playerInfo["fuel"] -= 2
								playerInfo["action"] = True

						case pygame.K_SPACE:
							if pygame.time.get_ticks() - playerInfo["cooldown"] > 500:
								grid[playerInfo["posY"]][1] = ">"

								playerInfo["fuel"] -= 3
								playerInfo["action"] = True
								playerInfo["cooldown"] = pygame.time.get_ticks()

		# Game tick
		if pygame.time.get_ticks() - lastGameTick > 100 and playerInfo["alive"]:
			lastGameTick = pygame.time.get_ticks()

			if not playerInfo["action"]:
				playerInfo["fuel"] -= 1

			if playerInfo["fuel"] <= 0:
				gameOver(playerInfo)

			spawn_objects(grid)
			updateGrid(grid, playerInfo)


		render(SCREEN, playerInfo, grid, fonts)

		clock.tick(SETTINGS["fps"])

	pygame.quit()
	clear()
	return


def render(SCREEN:pygame.surface, playerInfo:list, grid:list, fonts:list):
	SCREEN.fill("#000000")

	if not playerInfo["alive"]:
		game_over = fonts["font0"].render("GAME OVER", True, COLORS["branco"])
		points_text = fonts["font1"].render("Pontos:", True, COLORS["branco"])
		points_value = fonts["font1"].render(str(playerInfo["points"]), True, COLORS["branco"])

		SCREEN.blit(game_over, (845, 40))
		SCREEN.blit(points_text, (885, 75))
		SCREEN.blit(points_value, (965, 75))

		pygame.display.update()

		return

	for i in range(len(grid)):

		for j in range(len(grid[i])):
			rect = pygame.Rect(j * SETTINGS["unitSize"], i * SETTINGS["unitSize"], SETTINGS["unitSize"], SETTINGS["unitSize"])

			if grid[i][j] == "F":
				pygame.draw.rect(SCREEN, COLORS["azul"], rect)

			elif grid[i][j] == "+":
				pygame.draw.rect(SCREEN, COLORS["verde"], rect)

			elif grid[i][j] == "X":
				pygame.draw.rect(SCREEN, COLORS["vermelho"], rect)

			elif grid[i][j] == ">":
				pygame.draw.rect(SCREEN, COLORS["verde-escuro"], rect)

	fuel_text = fonts["font1"].render("Combustivel:", True, COLORS["branco"])
	fuel_value = fonts["font1"].render(str(playerInfo["fuel"]), True, COLORS["branco"])
	
	points_text = fonts["font1"].render("Pontos:", True, COLORS["branco"])
	points_value = fonts["font1"].render(str(playerInfo["points"]), True, COLORS["branco"])

	textY = 8

	SCREEN.blit(fuel_text, (15, textY))
	SCREEN.blit(fuel_value, (130, textY))
	SCREEN.blit(points_text, (1760, textY))
	SCREEN.blit(points_value, (1834, textY))

	pygame.display.update()


def spawn_objects(grid):
	if random.random() <= 0.15:
		fuelY = random.randint(0, SETTINGS["gridSize"][1] - 1)
		grid[fuelY][SETTINGS["gridSize"][0] - 1] = "F"

	enemyY = random.randint(0, SETTINGS["gridSize"][1] - 1)
	grid[enemyY][len(grid[0]) - 1] = "X"


def updateGrid(grid, playerInfo):
	shotPos = []

	for i in range(len(grid)):

		for j in range(len(grid[i])):
			if not grid[i][j] in [" ", "+"]:
				moveObject(grid, playerInfo, i, j, shotPos)
	
	for i in shotPos:
		grid[i[0]][i[1]] = ">"


def moveObject(grid:list, playerInfo:dict, i:int, j:int, shotPos:list):
	obj = grid[i][j]
	grid[i][j] = " "

	# shot update
	if obj == ">" and j < SETTINGS["gridSize"][0] - 1:
		if grid[i][j + 1] == "X" or grid[i][j + 1] == "F" :
			grid[i][j + 1] = " "
			
			playerInfo["points"] += 50

		elif grid[i][j + 2] == "X" or grid[i][j + 2] == "F" :
			grid[i][j + 2] = " "
			
			playerInfo["points"] += 50

		else:
			shotPos.append((i, j + 1))

	# enemy update
	if obj == "X" and j > 0:
		if grid[i][j - 1] == "+":
			gameOver(playerInfo)

		grid[i][j - 1] = "X"

	# fuel update
	elif obj == "F" and j > 0:
		if grid[i][j - 1] == "+":
			grid[i][j] = " "
			playerInfo["fuel"] += 40		
		else:
			grid[i][j - 1] = "F"

def gameOver(playerInfo):
	playerInfo["alive"] = False

	#SETTINGS["run"] = False


menu()
