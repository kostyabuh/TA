import tkinter as tk
from tkinter import ttk
from datetime import timedelta
import random

class FishingStateMachineGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Рыболовный автомат")
        self.master.geometry("800x600")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="green")
        self.canvas.pack()

        # Отрисовка озера
        self.canvas.create_rectangle(100, 0, 400, 450, fill="blue")  # вода
        self.canvas.create_rectangle(580, 0, 800, 600, fill="white")

        self.image_static = tk.PhotoImage(file="fisherman.png")
        self.image_dynamic = tk.PhotoImage(file="fisherman2.png")
        self.image_bait = tk.PhotoImage(file="food3.png")
        self.image_fish = tk.PhotoImage(file="fish.png")
        self.image_stick = tk.PhotoImage(file="stick.png")
        self.image_grass = tk.PhotoImage(file="grass33.png")
        self.image_pond = tk.PhotoImage(file="pond11.png")
        self.image_talk = tk.PhotoImage(file="talk.png")
        self.image_talk1 = tk.PhotoImage(file="talk1.png")

        # Рыбаки
        self.grass = self.canvas.create_image(180, 300, image=self.image_grass)
        self.pond = self.canvas.create_image(180, 235, image=self.image_pond)
        self.fisherman_static = self.canvas.create_image(170, 325, image=self.image_static)  # Статичный рыбак
        self.fisherman_dynamic = self.canvas.create_image(325, 355, image=self.image_dynamic)  # Динамичный рыбак
        self.bait = self.canvas.create_image(1000, 195, image=self.image_bait)
        self.stick = self.canvas.create_image(325, 300, image=self.image_stick)
        self.fish = self.canvas.create_image(1000,195, image=self.image_fish)
        self.talk = self.canvas.create_image(1300, 300, image=self.image_talk)
        self.talk1 = self.canvas.create_image(2850, 300, image=self.image_talk1)

        self.fishing_automaton = FishingStateMachine()
        self.delay = 1  # Задержка в миллисекундах (1 секунда)
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        # Добавляем текст поверх изображений
        self.state_text = self.canvas.create_text(600, 10, anchor="w", text="Состояние: Ждать поклевку", fill="black")
        self.time_text = self.canvas.create_text(600, 35, anchor="w", text="Время: 00:00", fill="black")
        self.hunger_text = self.canvas.create_text(600, 60, anchor="w", text="Голод: 0", fill="black")
        self.mood_text = self.canvas.create_text(600, 85, anchor="w", text="Настроение: 100", fill="black")
        self.catch_text = self.canvas.create_text(600, 110, anchor="w", text="Количество рыбы: 0", fill="black")
        self.bait_text = self.canvas.create_text(600, 135, anchor="w", text="Подкормка: Не брошена", fill="black")
        self.cycle_button = ttk.Button(self.master, text="Автоматический цикл", command=self.toggle_automatic_cycle)
        self.canvas.create_window(600, 160, anchor="w", window=self.cycle_button)

    def toggle_automatic_cycle(self):
        self.running = not self.running
        if self.running:
            self.reset_automaton()
            self.start_automatic_cycle()

    def reset_automaton(self):
        self.fishing_automaton = FishingStateMachine()

    def start_automatic_cycle(self):
        if self.running:
            self.run_one_tick()
            if self.fishing_automaton.state == "Уехать домой":
                self.running = False
            else:
                self.master.after(self.delay, self.start_automatic_cycle)

    def run_one_tick(self):
        self.fishing_automaton.update_bait_ticks()
        self.fishing_automaton.update_eat_ticks()
        self.fishing_automaton.update_talk_ticks()
        self.fishing_automaton.fishing_cycle()
        self.fishing_automaton.time += 1  # Увеличиваем время на 1 тик
        self.update_labels()

    def update_labels(self):
        state_text = f"Состояние: {self.fishing_automaton.state}"
        time_text = f"Время: {self.fishing_automaton.format_time()}"
        hunger_text = f"Голод: {self.fishing_automaton.hunger}"
        mood_text = f"Настроение: {self.fishing_automaton.mood}"
        catch_text = f"Количество рыбы: {self.fishing_automaton.catch_count} "
        bait_text = "Подкормка: Брошена" if self.fishing_automaton.bait_ticks > 0 else "Подкормка: Не брошена"

        self.canvas.itemconfig(self.state_text, text=state_text)
        self.canvas.itemconfig(self.time_text, text=time_text)
        self.canvas.itemconfig(self.hunger_text, text=hunger_text)
        self.canvas.itemconfig(self.mood_text, text=mood_text)
        self.canvas.itemconfig(self.catch_text, text=catch_text)
        self.canvas.itemconfig(self.bait_text, text=bait_text)

        self.canvas.coords(self.stick, 325, 300)

        if self.fishing_automaton.state == "Поговорить":
            self.canvas.coords(self.fisherman_dynamic, 235, 355)
            self.canvas.coords(self.fish, 1000, 195)
            self.canvas.coords(self.talk, 130, 300)
            self.canvas.coords(self.talk1, 285, 300)

        if self.fishing_automaton.state == "Поесть":
            self.canvas.coords(self.fisherman_dynamic, 365, 545)
            self.canvas.coords(self.fish, 1000, 195)
            self.canvas.coords(self.talk, 1300, 300)
            self.canvas.coords(self.talk1, 2850, 300)

        if self.fishing_automaton.state == "Ждать рыбу":
            self.canvas.coords(self.fisherman_dynamic, 325, 355)
            self.canvas.coords(self.fish, 1000, 195)
            self.canvas.coords(self.talk, 1300, 300)
            self.canvas.coords(self.talk1, 2850, 300)

        if self.fishing_automaton.state == "Бросить подкормку":
            self.canvas.coords(self.fisherman_dynamic, 325, 355)
            self.canvas.coords(self.bait, 315, 205)
            self.canvas.coords(self.fish, 1000, 395)
            self.canvas.coords(self.talk, 1300, 300)
            self.canvas.coords(self.talk1, 2850, 300)

        if self.fishing_automaton.bait_ticks == 0:
            self.canvas.coords(self.fish, 1000, 195)
            self.canvas.coords(self.bait, 1000, 195)

        if self.fishing_automaton.state == "Уехать домой":
            self.canvas.coords(self.fish, 1000, 195)
            self.canvas.coords(self.stick, 1000, 0)
            self.canvas.coords(self.fisherman_dynamic, 1000, 195)
            self.canvas.coords(self.talk, 1300, 300)
            self.canvas.coords(self.talk1, 2850, 300)

        if self.fishing_automaton.state == "Ловить":
            self.canvas.coords(self.fish, 320, 265)


class FishingStateMachine:
    def __init__(self):
        self.state = "Ждать рыбу"
        self.hunger = 99
        self.mood = 20
        self.time = 240
        self.food_count = 10
        self.bait_count = 10
        self.catch_count = 0
        self.bite_probability = 0.0
        self.bait_ticks = 0
        self.eat_ticks = 0
        self.talk_ticks = 0

    def format_time(self):
        formatted_time = str(timedelta(minutes=self.time))
        return formatted_time

    def wait_for_bite(self):
        self.hunger += 1
        self.mood -= 1

    def check_conditions(self):
        bite_condition = random.random()  # Вероятность поклевки - 0.6
        print(bite_condition)

        if self.bait_ticks == 0:
            self.bite_probability = 0.0
        else:
            print("Подкормка действует")
        print(self.bite_probability)

        if (bite_condition <= self.bite_probability) and (self.state != "Поесть" or self.eat_ticks == 0) \
                and (self.state != "Поговорить" or self.talk_ticks == 0):
            self.state = "Ловить"
        elif (self.hunger >= 100 and bite_condition > self.bite_probability and self.eat_ticks == 0) \
                or (self.state == "Поесть" and self.eat_ticks != 0):
            self.state = "Поесть"
        elif (self.mood <= 20 and self.hunger < 100 and bite_condition > self.bite_probability) \
                or (self.state == "Поговорить" and self.talk_ticks != 0):
            self.state = "Поговорить"
        elif (self.mood > 20 and self.hunger < 100 and bite_condition > self.bite_probability
              and self.bait_ticks == 0):
            self.state = "Бросить подкормку"
            print("test")
            print(self.hunger)
            print(self.mood)
        elif self.mood > 20 and self.hunger < 100 and bite_condition > self.bite_probability:
            self.state = "Ждать рыбу"
        elif (self.hunger >= 100 and self.food_count == 0) or (self.catch_count >= 20) or (self.time == 1380):
            self.state = "Уехать домой"

    def fish(self):
        print("ловлю рыбу")
        self.catch_count += 1
        self.mood += 1
        self.hunger += 1

    def talk_to_fellow_angler(self):
        self.state = "Поговорить"
        print("говорю")
        if self.talk_ticks == 0:
            self.talk_ticks = 5
        if self.talk_ticks > 0:
            self.mood += 10
        if self.talk_ticks == 0:
            self.state = "Ждать рыбу"

    def throw_bait(self):
        self.state = "Бросить подкормку"
        print("бросая подкормку")
        self.mood -= 1
        self.hunger += 1
        if self.bait_ticks == 0:
            self.bait_ticks = 5
            self.bait_count -= 1
        if self.bait_ticks > 0:
            self.bite_probability = 0.8
        if self.bait_ticks == 0:
            self.bite_probability = 0.0

    def eat(self):
        self.state = "Поесть"
        print("ем")
        print(self.eat_ticks)
        if self.eat_ticks == 0:
            self.eat_ticks = 5
            self.food_count -= 1
            print(f"ачал есть {self.eat_ticks}")
        if self.eat_ticks > 0:
            self.hunger -= 20
        if self.eat_ticks == 0:
            self.state = "Ждать рыбу"

    def update_talk_ticks(self):
        if self.talk_ticks > 0:
            self.talk_ticks -= 1

    def update_bait_ticks(self):
        if self.bait_ticks > 0:
            self.bait_ticks -= 1

    def update_eat_ticks(self):
        if self.eat_ticks > 0:
            self.eat_ticks -= 1

    def go_home(self):
        self.state = "Уехать домой"

    def fishing_cycle(self):
        print(self.state)

        self.check_conditions()
        print("test cond")
        print(self.state)
        if (self.hunger >= 100 and self.food_count == 0) or (self.catch_count >= 20) \
                or (self.time == 1380) or (self.state == "Уехать домой"):
            self.go_home()
        elif (self.state == "Бросить подкормку") or (self.bait_count == 0):
            self.throw_bait()
        elif self.state == "Поесть" and self.food_count > 0:
            self.eat()
        elif self.state == "Поговорить":
            self.talk_to_fellow_angler()
        elif self.state == "Ждать рыбу":
            self.wait_for_bite()
        elif self.state == "Ловить":
            self.fish()

        print("___________________________")


if __name__ == "__main__":
    root = tk.Tk()
    app = FishingStateMachineGUI(root)
    root.mainloop()
