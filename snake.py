import tkinter as tk
import random

class Snakegame:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake")
        self.window.columnconfigure([i for i in range(17)], minsize=20, weight=1)
        self.window.rowconfigure([i for i in range(17)], minsize=20, weight=1)
        self.set_grid()
        self.speed = 5
        self.speeds = {7: 30, 6: 50, 5: 100, 4: 150, 3: 200, 2: 250, 1: 300}
        self.score = 0
        self.scorecounter = tk.Label(text=f"SCORE: {self.score}")
        self.scorecounter.grid(row=16, column=0, columnspan=16, sticky="nsew")
        self.button = tk.Button(text="START", command= self.start)
        self.button.grid(row=0,column=0, columnspan= 5, sticky="nsew")
        self.speedbutton = tk.Button(text= f"SPEED: {self.speed}", command=self.toggle_speed)
        self.speedbutton.grid(row=0, column=12, columnspan=5, sticky="nsew")
        self.direction = "right"
        self.dirchangepending = False
        self.keybinds()
        self.window.mainloop()

    def toggle_speed(self):
        self.speed -= 1
        if self.speed < 1:
            self.speed = 7
        self.speedbutton["text"] = f"SPEED: {self.speed}"

    def keybinds(self):
        self.window.bind("w", lambda x: self.change_direction("up"))
        self.window.bind("<Up>", lambda x: self.change_direction("up"))
        self.window.bind("s", lambda x: self.change_direction("down"))
        self.window.bind("<Down>", lambda x: self.change_direction("down"))
        self.window.bind("a", lambda x: self.change_direction("left"))
        self.window.bind("<Left>", lambda x: self.change_direction("left"))
        self.window.bind("d", lambda x: self.change_direction("right"))
        self.window.bind("<Right>", lambda x: self.change_direction("right"))
    
    def start(self):
        self.score = 0
        self.button.configure(text="STOP", command=self.game_over)
        self.set_grid()
        self.init_snake()
        self.food()
        self.direction = "right"
        self.gameover = False
        self.score = 0
        self.scorecounter["text"] = f"SCORE: {self.score}"
        self.tick()

    def set_grid(self):
        # Each item in grid contains: [0]label, [1]x, [2]y, [3]snake, [4]food
        self.grid = []
        for r in range(15):
            for c in range(17):
                label = tk.Label()
                label.grid(row=r+1, column=c, sticky="nsew")
                self.grid.append([label, r, c, False, False])
        for l in self.grid:
            if l[1] % 2 == 0:
                if l[2] % 2 == 0:
                    l[0]["background"] = "#343434"
                else:
                    l[0]["background"] = "#111111"
            else:
                if l[2] % 2 == 0:
                    l[0]["background"] = "#111111"
                else:
                    l[0]["background"] = "#343434"

    def init_snake(self):
        init_pos = [(7,3),(7,2),(7,1),(7,0)]
        self.snake_pos = []
        for l in init_pos:
            for i in self.grid:
                if i[1] == l[0] and i[2] == l[1]:
                    self.snake_pos.append(i)
                    i[3] = True

    def change_direction(self, direction):
        if not self.dirchangepending:
            directions = ["left", "up", "right", "down"]
            if direction == self.direction or directions.index(direction) == directions.index(self.direction) - 2 or directions.index(direction) == directions.index(self.direction) + 2:
                return
            else:
                self.dirchangepending = True
                self.direction = direction

    def move_snake(self):
        head = self.snake_pos[0]
        self.snake_pos[-1][3] = False
        self.snake_pos.pop()
        if self.direction == "right":
            for p in self.grid:
                if head[2]+1 > 16:
                    if p[2] == 0 and p[1] == head[1]:
                        break
                elif p[2] == head[2]+1 and p[1] == head[1]:
                    break
        elif self.direction == "left":
            for p in self.grid:
                if head[2]-1 < 0:
                    if p[2] == 16 and p[1] == head[1]:
                        break
                elif p[2] == head[2]-1 and p[1] == head[1]:
                    break
        elif self.direction == "up":
            for p in self.grid:
                if head[1]-1 < 0:
                    if p[1] == 14 and p[2] == head[2]:
                        break
                elif p[1] == head[1]-1 and p[2] == head[2]:
                    break
        elif self.direction == "down":
            for p in self.grid:
                if head[1]+1 > 14:
                    if p[1] == 0 and p[2] == head[2]:
                        break
                elif p[1] == head[1]+1 and p[2] == head[2]:
                    break
        if p in self.snake_pos:
            p[0]["background"] = "red"
            self.game_over()
        else:
            p[3] = True
            self.snake_pos.insert(0, p)
            if p[4] == True:
                self.eat()

    def game_over(self):
        self.gameover = True
        for i in self.grid:
            if i not in self.snake_pos:
                i[0]["background"] = "black"
        self.button.configure(text= "START", command= self.start)

    def tick(self):
        self.move_snake()
        if self.dirchangepending:
            self.dirchangepending = False
        if self.gameover == True:
            return

        for l in self.grid:
            if l == self.snake_pos[0]:
                l[0]["background"] = "green"
            elif l[3] == True:
                l[0]["background"] = "#005A2A"
            elif l[4] == True:
                l[0]["background"] = "orange"
            elif l[1] % 2 == 0:
                if l[2] % 2 == 0:
                    l[0]["background"] = "#343434"
                else:
                    l[0]["background"] = "#111111"
            else:
                if l[2] % 2 == 0:
                    l[0]["background"] = "#111111"
                else:
                    l[0]["background"] = "#343434"
        
        self.window.after(self.speeds[self.speed], self.tick)

    def eat(self):
        self.snake_pos.append(self.snake_pos[-1])
        self.snake_pos[0][4] = False
        self.score += 1
        self.scorecounter["text"] = f"SCORE: {self.score}"
        self.food()

    def food(self):
        pos = random.choice(self.grid)
        while pos[3] == True:
            pos = random.choice(self.grid)
        pos[4] = True
                    
if __name__ == "__main__":
    Snakegame()
