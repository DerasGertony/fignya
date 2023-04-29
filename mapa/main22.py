import os
import sys
import pygame_widgets
from pygame_widgets.textbox import TextBox
import pygame as pg
import requests


def output():
  # Get text in the textbox
  print(textbox.getText())
  textbox.setText('')


class mapa:

  def __init__(self):
    self.x = 100
    self.y = 50
    self.spn = (3.0, 3.0)
    self.l = ['sat', 'map', 'skl']
    self.index = 0
    self.params = {}
    self.set_params()

  def set_params(self):
    self.params = {
      'll': str(self.x) + ',' + str(self.y),
      'l': str(self.l[self.index % 3]),
      'spn': str(self.spn[0]) + ',' + str(self.spn[1])
    }

  def request(self):
    search_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(search_api_server, params=self.params)
    if not response:
      print("Ошибка выполнения запроса:")
      print("Http статус:", response.status_code, "(", response.reason, ")")
      sys.exit(1)
    return response

  def change_spn(self, x, y):
    if 0 <= x < 20 and 0 <= y < 20:
      self.spn = (x, y)
      self.set_params()
      return self.request()
    return 0

  def change_coord(self, way):
    if way == 0 and -170 < self.x < 170:
      self.x += self.spn[0]
    if way == 1 and -170 < self.x < 170:
      self.x -= self.spn[0]
    if way == 2 and -80 < self.y < 80:
      self.y -= self.spn[1]
    if way == 3 and -80 < self.y < 80:
      self.y += self.spn[1]
      self.set_params()
    return self.request()

  def change_type(self):
    self.index += 1
    self.set_params()
    return self.request()


map1 = mapa()

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
  file.write(map1.request().content)

# Инициализируем pygame
pg.init()
screen = pg.display.set_mode((800, 600))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pg.image.load(map_file), (0, 0))

textbox = TextBox(screen,
                  50,
                  500,
                  600,
                  40,
                  fontSize=30,
                  borderColour=(255, 255, 0),
                  textColour=(0, 0, 0),
                  onSubmit=output,
                  radius=10,
                  borderThickness=5)
clock = pg.time.Clock()
running = True
while running:
  # внутри игрового цикла ещё один цикл
  # приема и обработки сообщений
  events = pg.event.get()
  for event in events:
    # при закрытии окна
    if event.type == pg.QUIT:
      running = False
    x = 0
    if event.type == pg.KEYDOWN:
      if event.key == 1073741902:
        x = map1.change_spn(map1.spn[0] - 1, map1.spn[1] - 1)
      if event.key == 1073741899:
        x = map1.change_spn(map1.spn[0] + 1, map1.spn[1] + 1)
      if event.key - 1073741903 in [0, 1, 2, 3]:
        x = map1.change_coord(event.key - 1073741903)
      if event.key == 116:
        x = map1.change_type()
    if x == 0:
      pass
    else:
      with open(map_file, "wb") as file:
        file.write(x.content)

    screen.blit(pg.image.load(map_file), (0, 0))

    pygame_widgets.update(events)
    pg.display.flip()
    clock.tick(144)
pg.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
