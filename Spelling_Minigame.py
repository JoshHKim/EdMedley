from pydoc import render_doc
import pygame as pg
import os
pg.font.init()
import random
from Minigame import Minigame

class Spelling_Minigame(Minigame):

    def __init__(self, WIN, SCALE, NEXT_MINI, duration):
        super().__init__(WIN, SCALE, NEXT_MINI, duration);

        self.WIDTH = WIN.get_width();
        self.HEIGHT = WIN.get_height();

        #Simply list the names of the files you want to load, will auto load them for you, named after their file name sans file type
        self.imageSet = {};
        self.loadImages(['notebook_background.png', 'pencil.png']);
        self.transformImages();

        self.CURRENT_POS = 0;
        self.rumbleUp = True;
        self.rumbleDistance = 2;
        self.move_timer = 100;
        self.tutorial_timer = 0;

        if(not pg.font.get_init):
            pg.font.init;
        self.font = pg.font.Font('freesansbold.ttf', 50);
        self.tutorial_font = pg.font.Font('freesansbold.ttf', 80);

        self.createObjects();
        self.createTutorialText();
        self.createAnswerChoices();

    def transformImages(self):
        self.initScaleImage('pencil', 0.9, 1)

    def createObjects(self):
        self.pencil = self.initImageObjectRect('pencil', self.WIDTH // 2 - self.imageSet['pencil'].get_width() // 2,(int)(self.HEIGHT * .75) - self.imageSet['pencil'].get_height() // 2 - self.rumbleDistance // 2)
        self.background = pg.transform.scale(pg.image.load(os.path.join('Assets','notebook_background.png')),(1280,720))

    def startRunningMinigame(self):
        #Will need to change to event that moves the queue foward
        print("New Minigame")
        pg.time.set_timer(self.NEXT_MINI, self.duration, 1);
    
    def createTutorialText(self):
        self.tutorial_text=self.tutorial_font.render("Choose the Correct Spelling", True, (0, 0, 0))
        self.tutorial_rect=self.tutorial_text.get_rect()
        self.tutorial_rect.center = (700, 50)
        
    def run_minigame(self):
        keys_pressed = pg.key.get_pressed()
        self.handle_pencil_movement(keys_pressed)
        self.draw_window()

    def draw_window(self):
        self.move_timer+=1
        self.WIN.blit(self.background,(0,0))
        self.WIN.blit(self.imageSet['pencil'],(self.pencil.x, self.pencil.y))
        
        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_1)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_1_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_1_text, self.sign_1_text_rect)

        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_2)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_2_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_2_text, self.sign_2_text_rect)

        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_3)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_3_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_3_text, self.sign_3_text_rect)

        if self.tutorial_timer<70:
            self.tutorial_timer+=1;
            self.WIN.blit(self.tutorial_text,self.tutorial_rect)

        self.drawTimer();
        pg.display.update()

    def correctAnswer(self):
        if self.answerKey-2==self.CURRENT_POS:
            return True
        else:
            return False

    def handle_pencil_movement(self, keys_pressed):
        if self.move_timer<10:
            quit
        elif keys_pressed[pg.K_LEFT] and self.CURRENT_POS != -1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS - 1;
            self.pencil.x-= self.imageSet['pencil'].get_width()+100

        elif keys_pressed[pg.K_RIGHT] and self.CURRENT_POS != 1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS + 1;
            self.pencil.x += self.imageSet['pencil'].get_width()+100
    
    def createAnswerChoices(self):
        #the correct answer will be in the first position
        question_bank = [["spelling","speling","speeling"],["crayon","krayon","craon"],["paraphrase","paraphase","parafrase"],["rewrite","rewrit","riwrite"],["root","rott","roat"],["usage","usige","usege"],["verify","veerify","verrify"],["claim","claime","claym"],["prose","proase","prosse"],["perform","prefform","perfform"],["repetition","reptition",'wrepition'],["pitch","petch","pitsh"]]
        question=random.randint(0,len(question_bank)-1)
        self.answerKey = random.randint(1,5) % 3 + 1
        if(self.answerKey == 1):
            self.choices = [question_bank[question][0], question_bank[question][1], question_bank[question][2]];
        elif(self.answerKey == 2):
            self.choices = [question_bank[question][1], question_bank[question][0], question_bank[question][2]];
        else:
            self.choices = [question_bank[question][1], question_bank[question][2], question_bank[question][0]];

        if self.answerKey==1:
            self.createSignObject(self.getAnswer(), self.getWrong1(), self.getWrong2())
        elif self.answerKey==2:
            self.createSignObject(self.getWrong1(), self.getAnswer(), self.getWrong2())
        else:
            self.createSignObject(self.getWrong1(), self.getWrong2(), self.getAnswer())

    def createSignObject(self, sign1text, sign2text, sign3text):
        self.sign_1 = pg.Rect(80, 100, 300, 250);
        self.sign_1_border = pg.Rect(80, 100, 300, 250);
        self.sign_1_text = self.font.render(str(sign1text), True, (255, 255, 255));
        self.sign_1_text_rect = self.sign_1_text.get_rect();
        self.sign_1_text_rect.center = (200, 175);

        self.sign_2 = pg.Rect(480, 100, 300, 250);
        self.sign_2_border = pg.Rect(480, 100, 300, 250);
        self.sign_2_text = self.font.render(str(sign2text), True, (255, 255, 255));
        self.sign_2_text_rect = self.sign_1_text.get_rect();
        self.sign_2_text_rect.center = (600, 175);

        self.sign_3 = pg.Rect(880, 100, 300, 250);
        self.sign_3_border = pg.Rect(880, 100, 300, 250);
        self.sign_3_text = self.font.render(str(sign3text), True, (255, 255, 255));
        self.sign_3_text_rect = self.sign_1_text.get_rect();
        self.sign_3_text_rect.center = (1000, 175);