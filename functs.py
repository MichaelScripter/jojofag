import PIL
from PIL import Image
import requests
import random
chances = {}
num = 0

sys_random = random.SystemRandom()

def add_chance(stands, chance):
    global num
    chances[(num, chance+num)] = stands
    num += chance

def generate_stand():
    rand = random.randint(1,100)
    for chance in chances:
        if rand >= chance[0] and rand <= chance[1]:
            return sys_random.choice(chances[chance])

def add_avatar(image, user, pos, size):
    img = Image.open(requests.get(user.avatar_url, stream=True).raw)
    img = img.resize(size)
    image.paste(img, pos)