import pygame #importuje modul pygame
import os # importuje system operacyjny
import random # importuje modul  losowosci
pygame.init()   # inicjalizuje okno pygame
# OPCJE OKNA
WIDTH = 600
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #ustawia rozmiar naszego okna
pygame.display.set_caption("Monkey jump") #nazwka naszego okna
#WARTOSCI GRY
ground_scroll = 0 #wartosc początkowa od której ma być przewijany ziemia
scroll_speed = 4  #szybkosc przewijania okna
clock = pygame.time.Clock()
FPS = 60
flying = False #parametr flying określa czy postac lata czy nie
pipe_gap = 170 #różnica   odległosci pomiedzy rurami
pipe_frequancy = 1500 # czestotliwosc pojawiania sie rur
last_pipe = pygame.time.get_ticks() - pipe_frequancy #zapobiega dalszemu spawnowaniu sie rur bo przegranej grze 
game_over = False #parametr game over bedzie odpowiadal za zamykanie gry
score = 0 #wynik
pass_pipe = False
font = pygame.font.SysFont("Comicsans", 40) #czcionka
WHITE = (255,255,255) #kolor
#WGRYWANIE OBIEKTÓW
BACKGROUND_image = pygame.image.load(os.path.join(r"C:\Users\gekon\Desktop\monkey jump\Background.jpg"))
BACKGROUND = pygame.transform.scale(BACKGROUND_image, (600, 500))
ground_image = pygame.image.load(os.path.join(r"C:\Users\gekon\Desktop\monkey jump\ground 1.jpg"))
ground = pygame.transform.scale(ground_image, (800, 94))
button_image = pygame.image.load(os.path.join(r"C:\Users\gekon\Desktop\monkey jump\play again button 4.png"))
def draw_text(text,font,text_col,x,y):
    image = font.render(text,True,text_col)
    WIN.blit(image,(x,y))  #renderujemy czcionke wyniku


def reset_game():#funkcja reset game bedzie odpowiadal za ponowna gre
    pipe_group.empty() #przywraca wszystkie wartosci grupy rur do 0
    monkeys.rect.x = 100 #przywraca położenie małpki do stanu z początku gry
    monkeys.rect.y = int(HEIGHT / 2)
    score = 0
    return score  #przywraca wynik do 0



class Monkey(pygame.sprite.Sprite):  #Nasz kreator małpki
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] # lista naszych oobrazkow
        self.index = 0 #numer naszego obrazk z listy obrazków
        self.counter = 0 #szybkosc wyswietlania naszych obrazków
        for num in range(1, 4):
            image =pygame.image.load(os.path.join(fr"C:\Users\gekon\Desktop\NEW MONEY JUMP\monkey {num}.png"))
            self.images.append(image)
        self.image = self.images[self.index] #obrazek = obrazek o numerze np 1 wybrany z listy obrazków
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0  #prędkosc naszej małpki
        self.clicked = False #parametr clicked swiadczacy o tym czy user input zostaje odebrany

    def update(self):
        #GRAWITACJA MAŁPKI
        if flying == True:   #jezeli latanie jest prawda
            self.vel +=0.5  #predkosc zwiekszona o 0.5 ciągnaca nas w dol
            if self.vel >8: # jezeli bedzie ona wieksza od 8 to zmien ja spowrotem na 8
                self.vel = 8
            if self.rect.bottom < 768:  #jezeli dolny wymiar naszej malpki bedzie mniejszy od 768 to przyspiesz jej poruszanie w osi y czyli pociagij ja w góre
                self.rect.y += int(self.vel)
        if game_over == False:
            #SKAKANIE MAŁPKI
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True   #jezeli mysz 1 zostanie nacisnieta wtedy wartosc klikde przechodzi na kliknąles i predkosc jest obnizona o -10 czyli w naszym przypadku wartosci sa odwrocone wiec jest to +10 i malpka skacze do góry
                self.vel = -10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False #jezeli nie jest mysz 1 kliknieta wtedy wartosc clicked przechodz na nieklinoles

            self.counter +=1  #zwiększamy predkosc wyswietlania obrazkow o 1 czyli wyswietlamy o 1 obrazek wiecej
            jump_cooldown = 5 #okresla maksymlan liczbe skokow po ktory bedzie przerwa czasowa przed nastepna seria

            if self.counter > jump_cooldown:
                self.counter = 0 #jezeli predkosc wyswietlania obrazkow jest wieksza od cooldownu skoku to jej wartosc wraca na 0 i kolejne obrazki maja byc rysowane
                self.index +=1   #drukuje o 1 obrazek z listy dalej
                if self.index >=len(self.images):  #jeżeli obrazki w liscie sie skoncza to powracan do 1 obrazka i rysuje wszystko od nowa
                    self.index = 0
            self.image = self.images[self.index]

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,possition):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(r"C:\Users\gekon\Desktop\monkey jump\trees 1.png"))
        self.rect = self.image.get_rect()   #nadajemy kształt prostokata naszym obiektom aby mozna je było łatwiej ustawiac,modyfikowac
        self.rect.topleft = [x,y]

        if possition ==-1:
            self.image = pygame.transform.flip(self.image, False, True) #dzieki tej komendzie mozemy odwroci nasze obrazki i ustawic je po przeciwnej stronie 1 to dół a -1 to góra
            self.rect.bottomleft = [x,y-int(pipe_gap)/2]
        if possition ==1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed   #przepsuwa nasze rury w osi x z prędkościa scroll_speed
        if self.rect.right < 0:  #jezeli prawa strona prostokta naszej rury bedzie miala pozycje wieksza od 0 to zabij funkcje rysowania rur
            self.kill()


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):   #ustalamy kolizje myszy z przyciskiem i jezeli koliduja ze soba to wykona sie jakas okreslona akcja czyli jak wcisniemy przycisk to ma sie cos zadziac
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        WIN.blit(self.image, (self.rect.x, self.rect.y))

        return action

monkey_group = pygame.sprite.Group()
monkeys = Monkey(100, int(HEIGHT/2))
monkey_group.add(monkeys)
pipe_group = pygame.sprite.Group()


button = Button(WIDTH//2 - 50,HEIGHT // 2 -100,button_image)


run = True
while run:
    clock.tick(FPS)
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(ground, (ground_scroll, 450))

    monkey_group.draw(WIN)
    monkey_group.update()
    pipe_group.draw(WIN)

    if len(pipe_group) > 0:
        if monkey_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and monkey_group.sprites()[0].rect.right > pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
           if  monkey_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score +=1
            pass_pipe = False
#jezeli długosc prostka małpki jest  wieksza od prostakąta rury w lewej i prawej stronie to oznacza to ze małpka przeskoczyła pomiedzy rurami
#parametr pass_pipe okresla czy małpka przeszła przez obszar w którym zaliczane sa punkty
    draw_text(str(score),font,WHITE,int(WIDTH/2),20)


    if pygame.sprite.groupcollide(monkey_group,pipe_group,False,False) or monkeys.rect.top < 0:
        game_over = True   #kolizja małpki z rurami

    if monkeys.rect.bottom >= 450:
        game_over = True   #kolizja małpki z podłożem
        flying = False


    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequancy:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(WIDTH, int(HEIGHT / 2)+pipe_height, 1)
            pipe_group.add(btm_pipe, )
            pipe_group.add(top_pipe)
            last_pipe = time_now
   #Ta sekcja tworzy nowe rury o losowych wartosciach


        ground_scroll -=scroll_speed
        if abs(ground_scroll) > 35:
                    ground_scroll = 0
    #Animacja przewijania podłoza
        pipe_group.update()


    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
    #ROZPOCZECIE PONOWNEJ GRY PO NACISNIECIU PRZYCISKU PLAY


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over == False:
            flying = True
#Sekcja odpowiedzialna za wykorzystanie przycisku myszy do aktywowania skoku

    pygame.display.update()
