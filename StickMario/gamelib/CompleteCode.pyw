import pygame,random,math,time,os
name=""
try:
    with open("gamelib/levels/1/1.txt","r")as F:
        folder="gamelib/"
except:
    folder=""
class Player(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy,40,50)
        self.image=p1s
        self.direction="r"
        self.animtime=0
        self.score=0
        self.hptime=0
        self.swimmingtime=0
        self.health=1
        self.lives=3
        self.firetime=0
        self.jumping=False
        self.runningright=False
        self.runningleft=False
        self.changedhp=False
        self.died=False
        self.fireballs=[]
    def move(self,dx=0,dy=0):
        if dx!=0:
            self.rect.x+=dx
        if dy!=0:
            self.rect.y+=dy
        for mushrect in mushrects:
            if self.rect.colliderect(mushrect):
                self.col_mush("MUSH")
                mushrects.remove(mushrect)
        for flower in flowers:
            if self.rect.colliderect(flower):
                self.col_mush("FLOWER")
                flowers.remove(flower)
        for coin in coins:
            if self.rect.colliderect(coin):
                self.score+=100
                coins.remove(coin)
        for question in questions:
            if question.rect.colliderect(self.rect):
                if dx>0:
                    self.rect.right=question.rect.left
                if dx<0:
                    self.rect.left=question.rect.right
                if dy>0:
                    self.rect.bottom=question.rect.top
                    self.g=0
                    self.jumping=False
                if dy<0:
                    self.rect.top=question.rect.bottom
                    if not question.hit:
                        self.score+=50
                        if question.item=="MUSH":
                            mushrects.append(pygame.Rect(question.rect.x,question.rect.y-50,50,50))
                        if question.item=="UPGRADE":
                            if self.health==1:
                                mushrects.append(pygame.Rect(question.rect.x,question.rect.y-50,50,50))
                            if self.health==2:
                                flowers.append(pygame.Rect(question.rect.x,question.rect.y-50,50,50))
                            if self.health>=3:
                                mushrects.append(pygame.Rect(question.rect.x,question.rect.y-50,50,50))
                        if question.item=="COIN":
                            coins.append(pygame.Rect(question.rect.x,question.rect.y-50,50,50))
                    question.hit=True
                    self.g=0
        for brick in bricks:
            if brick.rect.colliderect(self.rect):
                if dx>0:
                    self.rect.right=brick.rect.left
                if dx<0:
                    self.rect.left=brick.rect.right
                if dy>0:
                    self.rect.bottom=brick.rect.top
                    self.g=0
                    self.jumping=False
                if dy<0:
                    self.rect.top=brick.rect.bottom
                    if self.health>=2:
                        self.score+=50
                        bricks.remove(brick)
                    self.g=0
        for pipe in pipes:
            if pipe.rect.colliderect(self.rect):
                if dx>0:
                    self.rect.right=pipe.rect.left
                if dx<0:
                    self.rect.left=pipe.rect.right
                if dy>0:
                    self.rect.bottom=pipe.rect.top
                    self.g=0
                    self.jumping=False
                    if user_input[pygame.K_s]or user_input[pygame.K_DOWN]:
                        if pipe.type==3:
                            self.rect.y=pipe.destination[1]
                            everything(0,-900)
                            if self.rect.y>900:
                                self.rect.y-=900
                if dy<0:
                    self.rect.top=pipe.rect.bottom
                    self.g=0
                    if user_input[pygame.K_w]or user_input[pygame.K_UP]:
                        if pipe.type==4:
                            everything(0,900)
                            self.rect.y=pipe.destination[1]
                            if self.rect.y>900:
                                self.rect.y-=900
        for items in [grounds,blocks,platforms,firebars,castlebricks]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    if dx>0:
                        self.rect.right=item.rect.left
                    if dx<0:
                        self.rect.left=item.rect.right
                    if dy>0:
                        self.rect.bottom=item.rect.top
                        self.g=0
                        self.jumping=False
                    if dy<0:
                        self.rect.top=item.rect.bottom
                        self.g=0
        for movingplatform in movingplatforms:
            if movingplatform.rect.colliderect(self.rect)and dy>0:
                if (movingplatform.rect.y>self.rect.y+75 and self.health>1)or(movingplatform.rect.y>self.rect.y+25 and self.health==1):
                        self.rect.bottom=movingplatform.rect.top
                        self.g=0
                        self.jumping=False
        for simple in simples:
            if self.rect.x>simple.rect.x-30 and self.rect.x<simple.rect.x+30:
                if self.health>1:
                    if self.rect.y>simple.rect.y-(60*2)and self.rect.y<simple.rect.y-(40*2):
                        self.score+=100
                        simples.remove(simple)
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>simple.rect.y-(50*2)and self.rect.y<simple.rect.y+50:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
                if self.health==1:
                    if self.rect.y>simple.rect.y-60 and self.rect.y<simple.rect.y-40:
                        self.score+=100
                        simples.remove(simple)
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>simple.rect.y-50 and self.rect.y<simple.rect.y+50:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
        for comple in complexs:
            if self.rect.x>comple.rect.x-30 and self.rect.x<comple.rect.x+30:
                if self.health>1:
                    if self.rect.y>comple.rect.y-((60*2)+25)and self.rect.y<comple.rect.y-((40*2)+25):
                        self.score+=100
                        complexs.remove(comple)
                        shells.append(Shell(comple.rect.x,comple.rect.y+47,comple.type))
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>comple.rect.y-(50*2)and self.rect.y<comple.rect.y+75:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
                if self.health==1:
                    if self.rect.y>comple.rect.y-85 and self.rect.y<comple.rect.y-65:
                        self.score+=100
                        complexs.remove(comple)
                        shells.append(Shell(comple.rect.x,comple.rect.y+47,comple.type))
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>comple.rect.y-50 and self.rect.y<comple.rect.y+75:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
        for brother in brothers:
            if self.rect.x>brother.rect.x-30 and self.rect.x<brother.rect.x+30:
                if self.health>1:
                    if self.rect.y>brother.rect.y-((60*2)+25)and self.rect.y<brother.rect.y-((40*2)+25):
                        self.score+=100
                        brothers.remove(brother)
                        shells.append(Shell(brother.rect.x,brother.rect.y+47,"GREEN"))
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>brother.rect.y-(50*2)and self.rect.y<brother.rect.y+75:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
                if self.health==1:
                    if self.rect.y>brother.rect.y-85 and self.rect.y<brother.rect.y-65:
                        self.score+=100
                        brothers.remove(brother)
                        shells.append(Shell(brother.rect.x,brother.rect.y+47,"GREEN"))
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>brother.rect.y-50 and self.rect.y<brother.rect.y+75:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
        for blooper in bloopers:
            if self.rect.x>blooper.rect.x-30 and self.rect.x<blooper.rect.x+30:
                if self.health>1:
                    if self.rect.y>blooper.rect.y-(60*2)and self.rect.y<blooper.rect.y-(40*2):
                        self.score+=100
                        bloopers.remove(blooper)
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>blooper.rect.y-(50*2)and self.rect.y<blooper.rect.y+50:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
                if self.health==1:
                    if self.rect.y>blooper.rect.y-60 and self.rect.y<blooper.rect.y-40:
                        self.score+=100
                        bloopers.remove(blooper)
                        self.jump()
                        if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                            self.g=15
                    elif self.rect.y>blooper.rect.y-50 and self.rect.y<blooper.rect.y+50:
                        if time.time()-self.hptime>2:
                            self.col_enem()
                            self.hptime=time.time()
        for items in[plants,podoboos]:
            for item in items:
                if self.rect.colliderect(item.rect)and time.time()-self.hptime>2:
                    self.col_enem()
                    self.hptime=time.time()
        for beetle in beetles:
            if beetle.type=="SPINY":
                if self.rect.colliderect(beetle.rect)and time.time()-self.hptime>2:
                    self.col_enem()
                    self.hptime=time.time()
            if beetle.type=="BUZZY":
                if self.rect.x>beetle.rect.x-30 and self.rect.x<beetle.rect.x+30:
                    if self.health>1:
                        if self.rect.y>beetle.rect.y-(60*2)and self.rect.y<beetle.rect.y-(40*2):
                            self.score+=100
                            shells.append(Shell(beetle.rect.x,beetle.rect.y,"GREEN"))
                            beetles.remove(beetle)
                            self.jump()
                            if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                                self.g=15
                        elif self.rect.y>beetle.rect.y-(50*2)and self.rect.y<beetle.rect.y+50:
                            if time.time()-self.hptime>2:
                                self.col_enem()
                                self.hptime=time.time()
                    if self.health==1:
                        if self.rect.y>beetle.rect.y-60 and self.rect.y<beetle.rect.y-40:
                            self.score+=100
                            shells.append(Shell(beetle.rect.x,beetle.rect.y,"GREEN"))
                            beetles.remove(beetle)
                            self.jump()
                            if not pygame.key.get_pressed()[pygame.K_w]or pygame.key.get_pressed()[pygame.K_UP]:
                                self.g=15
                        elif self.rect.y>beetle.rect.y-50 and self.rect.y<beetle.rect.y+50:
                            if time.time()-self.hptime>2:
                                self.col_enem()
                                self.hptime=time.time()
        for firebar in firebars:
            for fireball in firebar.fireballs:
                if self.rect.colliderect(fireball):
                    if time.time()-self.hptime>2:
                        self.col_enem()
                        self.hptime=time.time()
        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                if time.time()-self.hptime>2:
                    self.col_enem()
                    self.hptime=time.time()
                if dx>0:
                    self.rect.right=spike.rect.left
                if dx<0:
                    self.rect.left=spike.rect.right
                if dy>0:
                    self.rect.bottom=spike.rect.top
                    self.g=0
                    self.jumping=False
                if dy<0:
                    self.rect.top=spike.rect.bottom
                    self.g=0
    def col_enem(self):
        if not breakpressed:
            self.health-=1
            if self.health==1:
                self.rect=pygame.Rect(self.rect.x,self.rect.y+50,40,50)
            if self.health==0:
                self.lives-=1
                self.died=True
            else:
                self.died=False
    def col_mush(self,item):
        if item=="MUSH"and self.health>1:
            self.lives+=1
        if self.health==1:
            self.rect=pygame.Rect(self.rect.x,self.rect.y-50,40,100)
        if item=="MUSH"and self.health<3:
            self.health=2
        if item=="FLOWER":
            self.health=3
    def jump(self):
        self.g=25
        self.jumping=True
    def animation(self,direction):
        self.direction=direction
        if self.health==3:
            if time.time()-self.animtime>0.5:
                self.animtime=time.time()
            elif time.time()-self.animtime>0.4:
                if direction=="r":
                    self.image=p35r
                else:
                    self.image=p35l
            elif time.time()-self.animtime>0.3:
                if direction=="r":
                    self.image=p34r
                else:
                    self.image=p34l
            elif time.time()-self.animtime>0.2:
                if direction=="r":
                    self.image=p33r
                else:
                    self.image=p33l
            elif time.time()-self.animtime>0.1:
                if direction=="r":
                    self.image=p32r
                else:
                    self.image=p32l
            else:
                if direction=="r":
                    self.image=p31r
                else:
                    self.image=p31l
        if self.health==2:
            if time.time()-self.animtime>0.5:
                self.animtime=time.time()
            elif time.time()-self.animtime>0.4:
                if direction=="r":
                    self.image=p25r
                else:
                    self.image=p25l
            elif time.time()-self.animtime>0.3:
                if direction=="r":
                    self.image=p24r
                else:
                    self.image=p24l
            elif time.time()-self.animtime>0.2:
                if direction=="r":
                    self.image=p23r
                else:
                    self.image=p23l
            elif time.time()-self.animtime>0.1:
                if direction=="r":
                    self.image=p22r
                else:
                    self.image=p22l
            else:
                if direction=="r":
                    self.image=p21r
                else:
                    self.image=p21l
        if self.health==1:
            if time.time()-self.animtime>0.5:
                self.animtime=time.time()
            elif time.time()-self.animtime>0.4:
                if direction=="r":
                    self.image=p15r
                else:
                    self.image=p15l
            elif time.time()-self.animtime>0.3:
                if direction=="r":
                    self.image=p14r
                else:
                    self.image=p14l
            elif time.time()-self.animtime>0.2:
                if direction=="r":
                    self.image=p13r
                else:
                    self.image=p13l
            elif time.time()-self.animtime>0.1:
                if direction=="r":
                    self.image=p12r
                else:
                    self.image=p12l
            else:
                if direction=="r":
                    self.image=p11r
                else:
                    self.image=p11l
    def stationary(self):
        if self.health==1:
            self.image=p1s
        if self.health==2:
            self.image=p2s
        if self.health==3:
            self.image=p3s
class FireBall(object):
    def __init__(self,wx,wy,obj):
        self.dir=obj
        self.rect=pygame.Rect(wx,wy,8,8)
        self.g=-10
        self.time=time.time()
    def move(self,dx=0,dy=0):
        if dx>0:
            if self.dir=="r":
                self.rect.x+=dx
            else:
                self.rect.x-=dx
        if dy>0:
            self.rect.y-=self.g
            if self.g>=-10:
                self.g-=1
        for items in [grounds,bricks,blocks,spikes,questions,pipes,platforms,castlebricks,firebars]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    if dy>0:
                        if self.g>0:
                            self.g=0
                            self.rect.top=item.rect.bottom
                        if self.g<0:
                            self.g=-(self.g+1)
                            self.rect.bottom=item.rect.top
                    if dx>0:
                        if self.dir=="r":
                            self.rect.right=item.rect.left
                            self.dir="l"
                        elif self.dir=="l":
                            self.rect.left=item.rect.right
                            self.dir="r"
        for comple in complexs:
            if comple.rect.colliderect(self.rect):
                shells.append(Shell(comple.rect.x,comple.rect.y+47,comple.type))
                try:
                    player.fireballs.remove(self)
                except:
                    pass
                complexs.remove(comple)
        for items in [simples,plants]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    try:
                        player.fireballs.remove(self)
                    except:
                        pass
                    items.remove(item)
        if time.time()-self.time>3:
            try:
                player.fireballs.remove(self)
            except:
                pass
class Block(object):
    def __init__(self,wx,wy,sx=50,sy=50):
        self.rect=pygame.Rect(wx,wy,sx,sy)
        self.hit=False
class Question(object):
    def __init__(self,wx,wy,sx=50,sy=50):
        self.rect=pygame.Rect(wx,wy,sx,sy)
        self.hit=False
        self.item=random.choice(["COIN","COIN","COIN","COIN","COIN","COIN","COIN","COIN","COIN","UPGRADE"])
class MovingPlatform(object):
    def __init__(self,wx,wy,sx=150,sy=50):
        self.rect=pygame.Rect(wx,wy,sx,sy)
    def move(self,dx=0,dy=0):
        if dx!=0:
            self.rect.x+=dx
        if dy!=0:
            self.rect.y+=dy
            if self.rect.y<=-25:
                self.rect.y=899
            if self.rect.y>=900:
                self.rect.y=-24
            if self.rect.colliderect(player.rect):
                if (self.rect.y>player.rect.y+75 and player.health>1)or(self.rect.y>player.rect.y+25 and player.health==1):
                        player.rect.bottom=self.rect.top
class Simple(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy,50,50)
        self.speed=-2
        self.image=s1r
        self.animtime=0
    def move(self,dx=0,dy=0):
        if dx!=0:
            self.rect.x+=dx
            for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks,firebars]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.speed=-self.speed
                        self.rect.x-=dx
            for simple in simples:
                if simple.rect.x!=self.rect.x and simple.rect.colliderect(self.rect):
                    self.speed=-self.speed
            for comple in complexs:
                if comple.rect.colliderect(self.rect):
                    self.speed=-self.speed
            if dx>0:
                self.animation("r")
            if dx<0:
                self.animation("l")
        if dy!=0:
            self.rect.y+=dy
            self.rect.x+=self.speed*25
            self.collision=False
            self.blockcollision=False
            for block in blocks:
                if block.rect.colliderect(self.rect):
                    self.blockcollision=True
            if not self.blockcollision:
                self.collision=True
            for items in [grounds,bricks,questions,pipes,platforms,castlebricks,firebars]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.collision=True
            if not self.collision:
                self.rect.y-=dy
                self.speed=-self.speed
                self.rect.x+=self.speed*25
            else:
                self.rect.x-=self.speed*25
            for items in [grounds,blocks,bricks,questions,pipes,platforms,movingplatforms,castlebricks,firebars]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.rect.bottom=item.rect.top
    def animation(self,direction):
        if time.time()-self.animtime>0.3:
            self.animtime=time.time()
        elif time.time()-self.animtime>0.2:
            if direction=="r":
                self.image=s3r
            else:
                self.image=s3l
        elif time.time()-self.animtime>0.1:
            if direction=="r":
                self.image=s2r
            else:
                self.image=s2l
        else:
            if direction=="r":
                self.image=s1r
            else:
                self.image=s1l
class Complex(object):
    def __init__(self,wx,wy,obj,wings):
        self.rect=pygame.Rect(wx,wy-25,50,75)
        if wings and obj=="RED":
            self.speed=-1
        else:
            self.speed=-2
        self.location=wy-25
        self.wings=wings
        self.image=cr1r
        self.wingimage=wl
        self.type=obj
        self.animtime=0
        self.direction="l"
    def move(self,dx=0,dy=0):
        if dx!=0 and(not self.wings or self.type=="GREEN"):
            self.rect.x+=dx
            for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks,firebars]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.speed=-self.speed
                        self.rect.x-=dx
            for comple in complexs:
                if comple.rect.x!=self.rect.x and comple.rect.colliderect(self.rect):
                    self.speed=-self.speed
            for simple in simples:
                if simple.rect.colliderect(self.rect):
                    self.speed=-self.speed
            if dx>0:
                self.animation("r")
            if dx<0:
                self.animation("l")
        if dy!=0 and not self.wings:
            if self.type=="RED":
                self.rect.y+=dy
                self.rect.x+=self.speed*25
                self.collision=False
                for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks,firebars]:
                    for item in items:
                        if item.rect.colliderect(self.rect):
                            self.collision=True
                if not self.collision:
                    self.rect.y-=dy
                    self.speed=-self.speed
                    self.rect.x+=self.speed*25
                else:
                    self.rect.y-=dy
                    self.rect.x-=self.speed*25
            if self.type=="GREEN":
                self.rect.y+=dy
                self.rect.x+=self.speed*25
                self.collision=False
                self.blockcollision=False
                for block in blocks:
                    if block.rect.colliderect(self.rect):
                        self.blockcollision=True
                if not self.blockcollision:
                    self.collision=True
                for items in [grounds,bricks,questions,pipes,platforms,castlebricks,firebars]:
                    for item in items:
                        if item.rect.colliderect(self.rect):
                            self.collision=True
                if not self.collision:
                    self.rect.y-=dy
                    self.speed=-self.speed
                    self.rect.x+=self.speed*25
                else:
                    self.rect.x-=self.speed*25
                for items in [grounds,blocks,bricks,questions,pipes,platforms,castlebricks,firebars]:
                    for item in items:
                        if item.rect.colliderect(self.rect):
                            self.rect.bottom=item.rect.top
        if dy!=0 and self.wings and self.type=="RED":
            self.image=cr1l
            self.rect.y+=self.speed
            if self.rect.y>self.location+100 or self.rect.y<self.location-100:
                self.speed=-self.speed
            for items in [grounds,blocks,bricks,questions,pipes,platforms,castlebricks,firebars]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.speed=-self.speed
                        self.rect.y+=self.speed
    def animation(self,direction):
        self.direction=direction
        if self.type=="GREEN":
            if time.time()-self.animtime>0.6:
                self.animtime=time.time()
            elif time.time()-self.animtime>0.4:
                if direction=="r":
                    self.image=cg5r
                else:
                    self.image=cg5l
            elif time.time()-self.animtime>0.3:
                if direction=="r":
                    self.image=cg4r
                else:
                    self.image=cg4l
            elif time.time()-self.animtime>0.2:
                if direction=="r":
                    self.image=cg3r
                else:
                    self.image=cg3l
            elif time.time()-self.animtime>0.1:
                if direction=="r":
                    self.image=cg2r
                else:
                    self.image=cg2l
            else:
                if direction=="r":
                    self.image=cg1r
                else:
                    self.image=cg1l
        if self.type=="RED":
            if time.time()-self.animtime>0.6:
                self.animtime=time.time()
            elif time.time()-self.animtime>0.4:
                if direction=="r":
                    self.image=cr5r
                else:
                    self.image=cr5l
            elif time.time()-self.animtime>0.3:
                if direction=="r":
                    self.image=cr4r
                else:
                    self.image=cr4l
            elif time.time()-self.animtime>0.2:
                if direction=="r":
                    self.image=cr3r
                else:
                    self.image=cr3l
            elif time.time()-self.animtime>0.1:
                if direction=="r":
                    self.image=cr2r
                else:
                    self.image=cr2l
            else:
                if direction=="r":
                    self.image=cr1r
                else:
                    self.image=cr1l
        if self.wings:
            if direction=="r":
                self.wingimage=wr
            else:
                self.wingimage=wl
        else:
            self.wingimage=empty
class Shell(object):
    def __init__(self,wx,wy,obj):
        self.rect=pygame.Rect(wx,wy,50,28)
        self.hit=False
        if obj=="GREEN":
            self.image=shellgimg
        if obj=="RED":
            self.image=shellrimg
        self.time=0
    def move(self,dx=0,dy=0):
        if dx!=0:
            self.rect.x+=dx
            for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.speed=-self.speed
        if dy!=0:
            self.rect.y+=dy
            for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks]:
                for item in items:
                    if item.rect.colliderect(self.rect):
                        self.rect.y-=dy
class Plant(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx+25,wy+100,50,75)
        self.location=wy+100
        self.time=0
        self.open=False
        self.spawn=True
        self.player=False
    def move(self):
        if self.rect.x<=player.rect.x+100 and self.rect.x>player.rect.x-25 and self.rect.y>=self.location-25:
            self.rect.y=10000
            self.player=True
        elif self.player or self.rect.y>self.location+75:
            self.player=False
            self.rect.y=self.location
            self.time=0
        if time.time()-self.time>0.4 and not self.spawn:
            if self.open:
                self.open=False
            else:
                self.open=True
            self.time=time.time()
        else:
            self.spawn=False
        if self.open:
            self.rect.y-=5
        else:
            self.rect.y+=5
class Pipe(object):
    def __init__(self,wx,wy,obj):
        self.rect=pygame.Rect(wx,wy,100,50)
        obj=int(obj)
        self.type=obj
        if obj==1:
            self.image=p1
        if obj==2:
            self.image=p2
        if obj==3:
            self.image=p1
        if obj==4:
            self.image=p1
        if self.type==4:
            for pipe in pipes:
                if pipe.type==3 and pipe.rect.x==self.rect.x:
                    self.destination=(pipe.rect.x+25,pipe.rect.y-150)
                    pipe.destination=(self.rect.x+25,self.rect.y+100)
class Lava(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy,50,950)
class FireBar(object):
    def __init__(self,wx,wy,direction,amount=0):
        self.rect=pygame.Rect(wx,wy,50,50)
        self.direction=direction
        self.amount=amount
        if amount==0:
            self.amount=random.randint(10,20)
        self.time=0
        self.fireballs=[]
    def move(self):
        self.fireballs=[]
        if self.direction=="c":
            if time.time()-self.time>4:
                self.time=time.time()
            elif time.time()-self.time>3.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.25*8*(1+turn),(self.rect.y+25)-0.75*8*(1+turn),8,8))
            elif time.time()-self.time>3.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.5*8*(1+turn),(self.rect.y+25)-0.5*8*(1+turn),8,8))
            elif time.time()-self.time>3.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.75*8*(1+turn),(self.rect.y+25)-0.25*8*(1+turn),8,8))
            elif time.time()-self.time>3:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-8*(1+turn),(self.rect.y+25),8,8))
            elif time.time()-self.time>2.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.75*8*(1+turn),(self.rect.y+25)+0.25*8*(1+turn),8,8))
            elif time.time()-self.time>2.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.5*8*(1+turn),(self.rect.y+25)+0.5*8*(1+turn),8,8))
            elif time.time()-self.time>2.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.25*8*(1+turn),(self.rect.y+25)+0.75*8*(1+turn),8,8))
            elif time.time()-self.time>2:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25),(self.rect.y+25)+8*(1+turn),8,8))
            elif time.time()-self.time>1.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.25*8*(1+turn),(self.rect.y+25)+0.75*8*(1+turn),8,8))
            elif time.time()-self.time>1.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.5*8*(1+turn),(self.rect.y+25)+0.5*8*(1+turn),8,8))
            elif time.time()-self.time>1.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.75*8*(1+turn),(self.rect.y+25)+0.25*8*(1+turn),8,8))
            elif time.time()-self.time>1:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+8*(1+turn),(self.rect.y+25),8,8))
            elif time.time()-self.time>0.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.75*8*(1+turn),(self.rect.y+25)-0.25*8*(1+turn),8,8))
            elif time.time()-self.time>0.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.5*8*(1+turn),(self.rect.y+25)-0.5*8*(1+turn),8,8))
            elif time.time()-self.time>0.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.25*8*(1+turn),(self.rect.y+25)-0.75*8*(1+turn),8,8))
            else:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25),(self.rect.y+25)-8*(1+turn),8,8))
        else:
            if time.time()-self.time>4:
                self.time=time.time()
            elif time.time()-self.time>3.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.25*8*(1+turn),(self.rect.y+25)-0.75*8*(1+turn),8,8))
            elif time.time()-self.time>3.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.5*8*(1+turn),(self.rect.y+25)-0.5*8*(1+turn),8,8))
            elif time.time()-self.time>3.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.75*8*(1+turn),(self.rect.y+25)-0.25*8*(1+turn),8,8))
            elif time.time()-self.time>3:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+8*(1+turn),(self.rect.y+25),8,8))
            elif time.time()-self.time>2.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.75*8*(1+turn),(self.rect.y+25)+0.25*8*(1+turn),8,8))
            elif time.time()-self.time>2.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.5*8*(1+turn),(self.rect.y+25)+0.5*8*(1+turn),8,8))
            elif time.time()-self.time>2.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)+0.25*8*(1+turn),(self.rect.y+25)+0.75*8*(1+turn),8,8))
            elif time.time()-self.time>2:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25),(self.rect.y+25)+8*(1+turn),8,8))
            elif time.time()-self.time>1.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.25*8*(1+turn),(self.rect.y+25)+0.75*8*(1+turn),8,8))
            elif time.time()-self.time>1.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.5*8*(1+turn),(self.rect.y+25)+0.5*8*(1+turn),8,8))
            elif time.time()-self.time>1.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.75*8*(1+turn),(self.rect.y+25)+0.25*8*(1+turn),8,8))
            elif time.time()-self.time>1:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-8*(1+turn),(self.rect.y+25),8,8))
            elif time.time()-self.time>0.75:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.75*8*(1+turn),(self.rect.y+25)-0.25*8*(1+turn),8,8))
            elif time.time()-self.time>0.5:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.5*8*(1+turn),(self.rect.y+25)-0.5*8*(1+turn),8,8))
            elif time.time()-self.time>0.25:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25)-0.25*8*(1+turn),(self.rect.y+25)-0.75*8*(1+turn),8,8))
            else:
                for turn in range(self.amount):
                    self.fireballs.append(pygame.Rect((self.rect.x+25),(self.rect.y+25)-8*(1+turn),8,8))
class Blooper(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy,50,50)
class Podoboo(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy,50,50)
        self.g=0
    def move(self):
        self.rect.y-=self.g
        self.g-=1
        if self.rect.y>900:
            self.g=random.randint(20,30)
class Brother(object):
    def __init__(self,wx,wy):
        self.rect=pygame.Rect(wx,wy-25,50,75)
        self.hammers=[]
        self.time=0
    def attack(self):
        if self.rect.x<player.rect.x+800 and self.rect.x>player.rect.x and time.time()-self.time>1:
            self.hammers.append(Hammer(self.rect.x,self.rect.y,"l"))
            self.image=cg1l
            self.time=time.time()
        if self.rect.x<player.rect.x and self.rect.x>player.rect.x-800 and time.time()-self.time>1:
            self.hammers.append(Hammer(self.rect.x+50,self.rect.y,"r"))
            self.image=cg1r
            self.time=time.time()
        for hammer in self.hammers:
            if hammer.rect.y>=900 or hammer.rect.x<=0 or hammer.rect.x>=1625:
                self.hammers.remove(hammer)
            hammer.move()
class Hammer(object):
    def __init__(self,wx,wy,obj):
        self.rect=pygame.Rect(wx,wy,25,25)
        self.g=10
        self.obj=obj
    def move(self):
        self.rect.y-=self.g
        self.g-=1
        if self.obj=="r":
            self.rect.x+=random.randint(8,10)
        else:
            self.rect.x-=random.randint(8,10)
        if self.rect.colliderect(player.rect)and time.time()-player.hptime>2:
            player.col_enem()
            player.hptime=time.time()
class Beetle(object):
    def __init__(self,wx,wy,obj):
        self.rect=pygame.Rect(wx,wy,50,50)
        self.type=obj
        self.speed=-2
        self.animtime=0
        self.direction="l"
    def move(self):
        self.rect.x+=self.speed
        for items in [grounds,bricks,blocks,questions,pipes,platforms,castlebricks,firebars]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    self.speed=-self.speed
                    self.rect.x+=self.speed
        for simple in simples:
            if simple.rect.colliderect(self.rect):
                self.speed=-self.speed
        for comple in complexs:
            if comple.rect.colliderect(self.rect):
                self.speed=-self.speed
        if dx>0:
            self.animation("r")
        if dx<0:
            self.animation("l")
        self.rect.y+=10
        self.rect.x+=self.speed*25
        self.collision=False
        self.blockcollision=False
        for block in blocks:
            if block.rect.colliderect(self.rect):
                self.blockcollision=True
        if not self.blockcollision:
            self.collision=True
        for items in [grounds,bricks,questions,pipes,platforms,castlebricks,firebars]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    self.collision=True
        if not self.collision:
            self.rect.y-=10
            self.speed=-self.speed
            self.rect.x+=self.speed*25
        else:
            self.rect.x-=self.speed*25
        for items in [grounds,blocks,bricks,questions,pipes,platforms,movingplatforms,castlebricks,firebars]:
            for item in items:
                if item.rect.colliderect(self.rect):
                    self.rect.bottom=item.rect.top
    def animation(self,direction):
        self.direction=direction
        if time.time()-self.animtime>0.3:
            self.animtime=time.time()
        elif time.time()-self.animtime>0.2:
            if direction=="r":
                self.image=sb3r
            else:
                self.image=sb3l
        elif time.time()-self.animtime>0.1:
            if direction=="r":
                self.image=sb2r
            else:
                self.image=sb2l
        else:
            if direction=="r":
                self.image=sb1r
            else:
                self.image=sb1l
class Bowser(object):
    def __init__(self,wx,wy,health):
        self.rect=pygame.Rect(wx,wy,100,100)
        self.health=health
        self.time=0
        self.fire=[]
    def attack(self):
        if time.time()-self.time>3:
            self.fire.append(pygame.Rect(self.rect.x,self.rect.y+random.randint(-1,5)*25,45,13))
            self.time=time.time()
        for fire in self.fire:
            fire.x-=5
            if fire.x<=-100:
                self.fire.remove(fire)
def everything(direction,otherdirection=0):
    direction=int(direction)
    otherdirection=int(otherdirection)
    if direction!=0:
        for items in [grounds,bricks,blocks,simples,complexs,shells,spikes,questions,pipes,plants,platforms,walls,movingplatforms,lavas,castlebricks,bloopers,podoboos]:
            for item in items:
                item.rect.x+=direction
        for items in [coins,mushrects,flowers]:
            for item in items:
                item.x+=direction
        try:
            flagrect.x+=direction
        except:
            axerect.x+=direction
        leveledges[0]+=direction
        leveledges[1]+=direction
        for firebar in firebars:
            firebar.rect.x+=direction
            for fireball in firebar.fireballs:
                fireball.x+=direction
        for brother in brothers:
            brother.rect.x+=direction
            for hammer in brother.hammers:
                hammer.rect.x+=direction
        for fireball in player.fireballs:
            fireball.rect.x+=direction
        player.rect.x+=direction
        try:
            bowser.rect.x+=direction
            for fire in bowser.fire:
                fire.x+=direction
        except:
            pass
    if otherdirection!=0:
        for items in [grounds,bricks,blocks,simples,complexs,shells,spikes,questions,pipes,platforms,walls,movingplatforms,lavas,castlebricks,bloopers,podoboos]:
            for item in items:
                item.rect.y+=otherdirection
        for items in [coins,mushrects,flowers]:
            for item in items:
                item.y+=otherdirection
        for plant in plants:
            plant.rect.y+=otherdirection
            plant.location+=otherdirection
        for firebar in firebars:
            firebar.rect.y+=otherdirection
            for fireball in firebar.fireballs:
                fireball.y+=otherdirection
        for brother in brothers:
            brother.rect.y+=otherdirection
            for hammer in brother.hammers:
                hammer.rect.y+=otherdirection
        try:
            bowser.rect.y+=otherdirection
            for fire in bowser.fire:
                fire.y+=otherdirection
        except:
            pass
        try:
            flagrect.y+=otherdirection
        except:
            axerect.y+=otherdirection
        player.rect.y+=otherdirection
grounds=[]
bricks=[]
blocks=[]
pipes=[]
questions=[]
platforms=[]
movingplatforms=[]
walls=[]
castlebricks=[]
coins=[]
simples=[]
complexs=[]
shells=[]
plants=[]
bloopers=[]
podoboos=[]
brothers=[]
beetles=[]
mushrects=[]
flowers=[]
spikes=[]
firebars=[]
lavas=[]
leveledges=[]
width=1600
height=900
r=True
os.environ["SDL_VIDEO_WINDOW_POS"]="0,0"
pygame.init()
myfont=pygame.font.SysFont("Arial",30)
player_label=myfont.render(name,0,(0,0,155))
music=pygame.mixer.Sound(folder+"sound/music.wav")
pygame.mixer.set_num_channels(8)
channel0=pygame.mixer.Channel(0)
channel1=pygame.mixer.Channel(1)
channel2=pygame.mixer.Channel(2)
channel3=pygame.mixer.Channel(3)
channel4=pygame.mixer.Channel(4)
channel5=pygame.mixer.Channel(5)
channel6=pygame.mixer.Channel(6)
channel7=pygame.mixer.Channel(7)
empty=pygame.image.load(folder+"sprites/empty.png")
p1s=pygame.image.load(folder+"sprites/player/1/s.png")
p2s=pygame.image.load(folder+"sprites/player/2/s.png")
p3s=pygame.image.load(folder+"sprites/player/3/s.png")
p11r=pygame.image.load(folder+"sprites/player/1/right/1.png")
p12r=pygame.image.load(folder+"sprites/player/1/right/2.png")
p13r=pygame.image.load(folder+"sprites/player/1/right/3.png")
p14r=pygame.image.load(folder+"sprites/player/1/right/4.png")
p15r=pygame.image.load(folder+"sprites/player/1/right/5.png")
p11l=pygame.image.load(folder+"sprites/player/1/left/1.png")
p12l=pygame.image.load(folder+"sprites/player/1/left/2.png")
p13l=pygame.image.load(folder+"sprites/player/1/left/3.png")
p14l=pygame.image.load(folder+"sprites/player/1/left/4.png")
p15l=pygame.image.load(folder+"sprites/player/1/left/5.png")
p21r=pygame.image.load(folder+"sprites/player/2/right/1.png")
p22r=pygame.image.load(folder+"sprites/player/2/right/2.png")
p23r=pygame.image.load(folder+"sprites/player/2/right/3.png")
p24r=pygame.image.load(folder+"sprites/player/2/right/4.png")
p25r=pygame.image.load(folder+"sprites/player/2/right/5.png")
p21l=pygame.image.load(folder+"sprites/player/2/left/1.png")
p22l=pygame.image.load(folder+"sprites/player/2/left/2.png")
p23l=pygame.image.load(folder+"sprites/player/2/left/3.png")
p24l=pygame.image.load(folder+"sprites/player/2/left/4.png")
p25l=pygame.image.load(folder+"sprites/player/2/left/5.png")
p31r=pygame.image.load(folder+"sprites/player/3/right/1.png")
p32r=pygame.image.load(folder+"sprites/player/3/right/2.png")
p33r=pygame.image.load(folder+"sprites/player/3/right/3.png")
p34r=pygame.image.load(folder+"sprites/player/3/right/4.png")
p35r=pygame.image.load(folder+"sprites/player/3/right/5.png")
p31l=pygame.image.load(folder+"sprites/player/3/left/1.png")
p32l=pygame.image.load(folder+"sprites/player/3/left/2.png")
p33l=pygame.image.load(folder+"sprites/player/3/left/3.png")
p34l=pygame.image.load(folder+"sprites/player/3/left/4.png")
p35l=pygame.image.load(folder+"sprites/player/3/left/5.png")
s1r=pygame.image.load(folder+"sprites/enemies/simple/right/1.png")
s2r=pygame.image.load(folder+"sprites/enemies/simple/right/2.png")
s3r=pygame.image.load(folder+"sprites/enemies/simple/right/3.png")
s1l=pygame.image.load(folder+"sprites/enemies/simple/left/1.png")
s2l=pygame.image.load(folder+"sprites/enemies/simple/left/2.png")
s3l=pygame.image.load(folder+"sprites/enemies/simple/left/3.png")
cg1r=pygame.image.load(folder+"sprites/enemies/shell/green/right/1.png")
cg2r=pygame.image.load(folder+"sprites/enemies/shell/green/right/2.png")
cg3r=pygame.image.load(folder+"sprites/enemies/shell/green/right/3.png")
cg4r=pygame.image.load(folder+"sprites/enemies/shell/green/right/4.png")
cg5r=pygame.image.load(folder+"sprites/enemies/shell/green/right/5.png")
cg1l=pygame.image.load(folder+"sprites/enemies/shell/green/left/1.png")
cg2l=pygame.image.load(folder+"sprites/enemies/shell/green/left/2.png")
cg3l=pygame.image.load(folder+"sprites/enemies/shell/green/left/3.png")
cg4l=pygame.image.load(folder+"sprites/enemies/shell/green/left/4.png")
cg5l=pygame.image.load(folder+"sprites/enemies/shell/green/left/5.png")
cr1r=pygame.image.load(folder+"sprites/enemies/shell/red/right/1.png")
cr2r=pygame.image.load(folder+"sprites/enemies/shell/red/right/2.png")
cr3r=pygame.image.load(folder+"sprites/enemies/shell/red/right/3.png")
cr4r=pygame.image.load(folder+"sprites/enemies/shell/red/right/4.png")
cr5r=pygame.image.load(folder+"sprites/enemies/shell/red/right/5.png")
cr1l=pygame.image.load(folder+"sprites/enemies/shell/red/left/1.png")
cr2l=pygame.image.load(folder+"sprites/enemies/shell/red/left/2.png")
cr3l=pygame.image.load(folder+"sprites/enemies/shell/red/left/3.png")
cr4l=pygame.image.load(folder+"sprites/enemies/shell/red/left/4.png")
cr5l=pygame.image.load(folder+"sprites/enemies/shell/red/left/5.png")
wr=pygame.image.load(folder+"sprites/enemies/shell/right.png")
wl=pygame.image.load(folder+"sprites/enemies/shell/left.png")
fc=pygame.image.load(folder+"sprites/enemies/plant/closed.png")
fo=pygame.image.load(folder+"sprites/enemies/plant/open.png")
p1=pygame.image.load(folder+"sprites/pipe/1.png")
p2=pygame.image.load(folder+"sprites/pipe/2.png")
shellgimg=pygame.image.load(folder+"sprites/enemies/shell/green/shell.png")
shellrimg=pygame.image.load(folder+"sprites/enemies/shell/red/shell.png")
mushimg=pygame.image.load(folder+"sprites/mush.png")
flowerimg=pygame.image.load(folder+"sprites/flower.png")
groundimg=pygame.image.load(folder+"sprites/blocks/ground.png")
brickimg=pygame.image.load(folder+"sprites/blocks/brick.png")
blockimg=pygame.image.load(folder+"sprites/blocks/block.png")
questionimg=pygame.image.load(folder+"sprites/blocks/question.png")
unquestionimg=pygame.image.load(folder+"sprites/blocks/unquestion.png")
platformimg=pygame.image.load(folder+"sprites/blocks/platform.png")
wallimg=pygame.image.load(folder+"sprites/blocks/wall.png")
movingplatformimg=pygame.image.load(folder+"sprites/blocks/movingplatform.png")
coinimg=pygame.image.load(folder+"sprites/coin.png")
spikeimg=pygame.image.load(folder+"sprites/spike.png")
flagimg=pygame.image.load(folder+"sprites/flag.png")
fireballimg=pygame.image.load(folder+"sprites/player/fireball.png")
lavaimg=pygame.image.load(folder+"sprites/lava.png")
castlebrickimg=pygame.image.load(folder+"sprites/blocks/castle.png")
bowserimg=pygame.image.load(folder+"sprites/enemies/bowser/sprite.png")
fireimg=pygame.image.load(folder+"sprites/enemies/bowser/fire.png")
axeimg=pygame.image.load(folder+"sprites/axe.png")
blooperimg=pygame.image.load(folder+"sprites/enemies/blooper.png")
podobooimg=pygame.image.load(folder+"sprites/enemies/podoboo.png")
sb1l=pygame.image.load(folder+"sprites/enemies/beetle/spiny/left/1.png")
sb2l=pygame.image.load(folder+"sprites/enemies/beetle/spiny/left/2.png")
sb3l=pygame.image.load(folder+"sprites/enemies/beetle/spiny/left/2.png")
sb1r=pygame.image.load(folder+"sprites/enemies/beetle/spiny/right/1.png")
sb2r=pygame.image.load(folder+"sprites/enemies/beetle/spiny/right/2.png")
sb3r=pygame.image.load(folder+"sprites/enemies/beetle/spiny/right/3.png")
screen=pygame.display.set_mode((width,height),pygame.FULLSCREEN)
clock=pygame.time.Clock()
pygame.mouse.set_visible(False)
player=Player(0,750)
#Code to be improved :)\/
area=3
level=1
BOWSERhealth=7
charactertime=0
volume=0
breaktime=0
breakpressed=False
x=y=0
with open(folder+"levels/"+str(area)+"/"+str(level)+".txt","r")as f:
    for row in f:
        for col in row:
            if col.upper()=="0":
                questions.append(Question(x,y))
                questions[-1].item="COIN"
            if str(col)in"1234":
                pipes.append(Pipe(x,y,col))
            if str(col)=="5":
                podoboos.append(Podoboo(x,y))
            if str(col)=="6":
                brothers.append(Brother(x,y))
            if str(col)=="7":
                beetles.append(Beetle(x,y,"SPINY"))
            if str(col)=="8":
                beetles.append(Beetle(x,y,"BUZZY"))
            if col.upper()=="A":
                movingplatforms.append(MovingPlatform(x,y))
            if col.upper()=="B":
                bricks.append(Block(x,y))
            if col.upper()=="C":
                coins.append(pygame.Rect(x,y,50,50))
            if col.upper()=="D":
                complexs.append(Complex(x,y,"RED",True))
            if col.upper()=="E":
                flagrect=pygame.Rect(x,y-350,50,400)
                try:
                    del axerect
                except:
                    pass
            if col.upper()=="F":
                grounds.append(Block(x,y))
            if col.upper()=="G":
                complexs.append(Complex(x,y,"GREEN",False))
            if col.upper()=="H":
                complexs.append(Complex(x,y,"GREEN",True))
            if col.upper()=="I":
                castlebricks.append(Block(x,y))
            if col.upper()=="J":
                platforms.append(Block(x,y))
            if col.upper()=="K":
                firebars.append(FireBar(x,y,"c"))
            if col.upper()=="L":
                blocks.append(Block(x,y))
            if col.upper()=="M":
                questions.append(Question(x,y))
                questions[-1].item="MUSH"
            if col.upper()=="N":
                firebars.append(FireBar(x,y,"a"))
            if col.upper()=="O":
                bowser=Bowser(x,y,BOWSERhealth)
                BOWSERhealth+=1
            if col.upper()=="P":
                plants.append(Plant(x,y))
            if col.upper()=="Q":
                questions.append(Question(x,y))
            if col.upper()=="R":
                complexs.append(Complex(x,y,"RED",False))
            if col.upper()=="S":
                simples.append(Simple(x,y))
            if col.upper()=="T":
                axerect=pygame.Rect(x,y,50,50)
                try:
                    del flagrect
                except:
                    pass
            if col.upper()=="U":
                questions.append(Question(x,y))
                questions[-1].item="UPGRADE"
            if col.upper()=="V":
                lavas.append(Lava(x,y))
            if col.upper()=="W":
                walls.append(Block(x,y))
            if col.upper()=="X":
                spikes.append(Block(x,y))
            if col.upper()=="Y":
                bloopers.append(Blooper(x,y))
            if col.upper()=="Z":
                leveledges.append(x)
            x+=50
        y+=50
        x=0
    f.close()
#Code to be improved :)/\
player_label_width=player_label.get_rect().width/2
while r:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            r=False
    channel0.set_volume(volume)
    if not channel0.get_busy():
        channel0.play(music)
    screen.fill((255,255,255))
    for lava in lavas:
        if lava.rect.y>=-50 and lava.rect.y<=900 and lava.rect.x>=-50 and lava.rect.x<=1600:
            screen.blit(lavaimg,(lava.rect.x,lava.rect.y))
            pygame.draw.rect(screen,(88,88,88),pygame.Rect(lava.rect.x,lava.rect.y+10,50,940))
    user_input=pygame.key.get_pressed()
    levelChange=False
    for movingplatform in movingplatforms:
        if movingplatform.rect.x>=-150 and movingplatform.rect.x<=1600:
            movingplatform.move(dy=-7)
            if movingplatform.rect.y>=0 and movingplatform.rect.y<=900:
                screen.blit(movingplatformimg,(movingplatform.rect.x,movingplatform.rect.y))
    try:
        if player.rect.colliderect(flagrect):
            player.score+=5000
            levelChange=True
            level+=1
    except:
        if player.rect.colliderect(axerect):
            player.score+=10000
            levelChange=True
            level+=1
            try:
                del bowser
            except:
                pass
    if player.rect.y>=900:
        player.lives-=1
        levelChange=True
        if player.health>1:
            player.rect=pygame.Rect(player.rect.x,player.rect.y+50,50,50)
        player.health=1
    if player.died:
        player.died=False
        levelChange=True
        if player.health>1:
            player.rect=pygame.Rect(player.rect.x,player.rect.y+50,50,50)
        player.health=1
    if player.lives==-1:
        r=False
    #Code to be improved :)\/
    if levelChange:
        try:
            if level==5:
                level=1
                area+=1
                player.health=1
                player.rect=pygame.Rect(player.rect.x,player.rect.y,50,50)
                if area==9:
                    r=False
            grounds=[]
            bricks=[]
            blocks=[]
            pipes=[]
            questions=[]
            platforms=[]
            movingplatforms=[]
            walls=[]
            castlebricks=[]
            coins=[]
            simples=[]
            complexs=[]
            shells=[]
            plants=[]
            bloopers=[]
            podoboos=[]
            brothers=[]
            mushrects=[]
            flowers=[]
            spikes=[]
            firebars=[]
            lavas=[]
            leveledges=[]
            x=y=0
            with open(folder+"levels/"+str(area)+"/"+str(level)+".txt","r")as f:
                for row in f:
                    for col in row:
                        if col.upper()=="0":
                            questions.append(Question(x,y))
                            questions[-1].item="COIN"
                        if str(col)in"1234":
                            pipes.append(Pipe(x,y,col))
                        if str(col)=="5":
                            podoboos.append(Podoboo(x,y))
                        if str(col)=="6":
                            brothers.append(Brother(x,y))
                        if col.upper()=="A":
                            movingplatforms.append(MovingPlatform(x,y))
                        if col.upper()=="B":
                            bricks.append(Block(x,y))
                        if col.upper()=="C":
                            coins.append(pygame.Rect(x,y,50,50))
                        if col.upper()=="D":
                            complexs.append(Complex(x,y,"RED",True))
                        if col.upper()=="E":
                            flagrect=pygame.Rect(x,y-350,50,400)
                            try:
                                del axerect
                            except:
                                pass
                        if col.upper()=="F":
                            grounds.append(Block(x,y))
                        if col.upper()=="G":
                            complexs.append(Complex(x,y,"GREEN",False))
                        if col.upper()=="H":
                            complexs.append(Complex(x,y,"GREEN",True))
                        if col.upper()=="I":
                            castlebricks.append(Block(x,y))
                        if col.upper()=="J":
                            platforms.append(Block(x,y))
                        if col.upper()=="K":
                            firebars.append(FireBar(x,y,"c"))
                        if col.upper()=="L":
                            blocks.append(Block(x,y))
                        if col.upper()=="M":
                            questions.append(Question(x,y))
                            questions[-1].item="MUSH"
                        if col.upper()=="N":
                            firebars.append(FireBar(x,y,"a"))
                        if col.upper()=="O":
                            bowser=Bowser(x,y,BOWSERhealth)
                            BOWSERhealth+=1
                        if col.upper()=="P":
                            plants.append(Plant(x,y))
                        if col.upper()=="Q":
                            questions.append(Question(x,y))
                        if col.upper()=="R":
                            complexs.append(Complex(x,y,"RED",False))
                        if col.upper()=="S":
                            simples.append(Simple(x,y))
                        if col.upper()=="T":
                            axerect=pygame.Rect(x,y,50,50)
                            try:
                                del flagrect
                            except:
                                pass
                        if col.upper()=="U":
                            questions.append(Question(x,y))
                            questions[-1].item="UPGRADE"
                        if col.upper()=="V":
                            lavas.append(Lava(x,y))
                        if col.upper()=="W":
                            walls.append(Block(x,y))
                        if col.upper()=="X":
                            spikes.append(Block(x,y))
                        if col.upper()=="Y":
                            bloopers.append(Blooper(x,y))
                        if col.upper()=="Z":
                            leveledges.append(x)
                        x+=50
                    y+=50
                    x=0
                f.close()
            player.rect.y=450
            player.rect.x=0
        except:
            r=False
    #Code to be improved :)/\
    if user_input[pygame.K_ESCAPE]:
        r=False
    player.lavacollision=False
    for lava in lavas:
        if player.rect.colliderect(lava.rect)and player.rect.y>lava.rect.y+110:
            if player.g>15:
                player.g=15
            if player.g<-2:
                player.g=-2
            player.lavacollision=True
    if (user_input[pygame.K_w]or user_input[pygame.K_UP])and(not player.jumping or player.lavacollision)and time.time()-player.swimmingtime>0.3:
        player.jump()
        player.swimmingtime=time.time()
    elif player.jumping:
        player.move(dy=-player.g)
        if player.g>-25:
            player.g-=1
    else:
        player.collision=False
        for ground in grounds:
            if ground.rect.colliderect(player.rect):
                player.collision=True
        if not player.collision:
            player.g=0
            player.jumping=True
    if player.lavacollision:
        player.move(dy=-player.g)
        if player.g>-2:
            player.g-=1
    if (user_input[pygame.K_a]or user_input[pygame.K_LEFT])and not player.runningleft:
        player.runningleft=True
        player.rg=5
        if player.lavacollision:
            player.rg=4
    elif (user_input[pygame.K_a]or user_input[pygame.K_LEFT])and player.runningleft:
        player.move(-player.rg)
        if player.rg<8 and not player.lavacollision:
            player.rg+=0.1
        if player.rg<6 and not player.lavacollision:
            player.rg+=0.1
        player.animation("l")
    else:
        player.runningleft=False
    if (user_input[pygame.K_d]or user_input[pygame.K_RIGHT])and not player.runningright:
        player.runningright=True
        player.rg=5
        if player.lavacollision:
            player.rg=4
    elif (user_input[pygame.K_d]or user_input[pygame.K_RIGHT])and player.runningright:
        player.move(player.rg)
        if player.rg<8 and not player.lavacollision:
            player.rg+=0.1
        if player.rg<6 and not player.lavacollision:
            player.rg+=0.1
        player.animation("r")
    else:
        player.runningright=False
    try:
        if player.rect.x<700 and leveledges[0]<=0:
            everything((700-player.rect.x)/20)
    except:
        pass
    try:
        if player.rect.x>900 and leveledges[1]>=1550:
            everything(-(player.rect.x-900)/20)
    except:
        pass
    if player.rect.x<0:
        player.rect.x=0
    if player.rect.x>1550:
        player.rect.x=1550
    if user_input[pygame.K_SPACE]and player.health==3 and time.time()-player.firetime>0.5:
        player.fireballs.append(FireBall(player.rect.x+20,player.rect.y,player.direction))
        player.firetime=time.time()
    try:
        bowser.attack()
        if player.rect.colliderect(bowser)and time.time()-player.hptime>2:
            player.col_enem()
            player.hptime=time.time()
        for fire in bowser.fire:
            screen.blit(fireimg,(fire.x-5,fire.y))
            if player.rect.colliderect(fire)and time.time()-player.hptime>2:
                player.col_enem()
                player.hptime=time.time()
        screen.blit(bowserimg,(bowser.rect.x,bowser.rect.y))
        for fireball in player.fireballs:
            if fireball.rect.colliderect(bowser.rect):
                bowser.health-=1
                player.fireballs.remove(fireball)
        if bowser.health<=0:
            del bowser
    except:
        pass
    for fireball in player.fireballs:
        if not(fireball.rect.x>=1600 or fireball.rect.x<=-8 or fireball.rect.y>=900 or fireball.rect.y<=-8):
            fireball.move(9)
            fireball.move(dy=1)
            screen.blit(fireballimg,(fireball.rect.x,fireball.rect.y))
        else:
            player.fireballs.remove(fireball)
    for mushrect in mushrects:
        if mushrect.y>=0 and mushrect.y<=900 and mushrect.x>=-50 and mushrect.x<=1600:
            mushrect.x+=2
            for items in [blocks,bricks,questions,grounds,pipes,platforms,spikes,castlebricks]:
                for item in items:
                    if mushrect.colliderect(item.rect):
                        mushrect.x-=2
            mushrect.y+=10
            for items in [blocks,bricks,questions,grounds,pipes,platforms,spikes,castlebricks]:
                for item in items:
                    if mushrect.colliderect(item.rect):
                        mushrect.bottom=item.rect.top
            screen.blit(mushimg,(mushrect.x,mushrect.y))
    for flower in flowers:
        if flower.y>=0 and flower.y<=900 and flower.x>=-50 and flower.x<=1600:
            screen.blit(flowerimg,(flower.x,flower.y))
    if not (player.runningright or player.runningleft):
        player.stationary()
    for simple in simples:
        if simple.rect.y>=0 and simple.rect.y<=900 and simple.rect.x>=-50 and simple.rect.x<=1600:
            simple.move(simple.speed)
            simple.move(dy=10)
            screen.blit(simple.image,(simple.rect.x,simple.rect.y))
    for comple in complexs:
        if comple.rect.y>=0 and comple.rect.y<=900 and comple.rect.x>=-50 and comple.rect.x<=1600:
            comple.move(comple.speed)
            comple.move(dy=10)
            screen.blit(comple.image,(comple.rect.x,comple.rect.y))
            if comple.wings and comple.direction=="l":
                screen.blit(comple.wingimage,(comple.rect.x+30,comple.rect.y))
            elif comple.wings:
                screen.blit(comple.wingimage,(comple.rect.x+5,comple.rect.y))
    for blooper in bloopers:
        if blooper.rect.y>=0 and blooper.rect.y<=900 and blooper.rect.x>=-50 and blooper.rect.x<=1600:
            screen.blit(blooperimg,(blooper.rect.x,blooper.rect.y))
    for brother in brothers:
        brother.attack()
        for hammer in brother.hammers:
            if hammer.obj=="r":
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(hammer.rect.x+13,hammer.rect.y,12,25))
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(hammer.rect.x,hammer.rect.y+11,13,3))
            else:
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(hammer.rect.x,hammer.rect.y,12,25))
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(hammer.rect.x+12,hammer.rect.y+11,13,3))
        if brother.rect.y>=0 and brother.rect.y<=900 and brother.rect.x>=-50 and brother.rect.x<=1600:
            screen.blit(brother.image,(brother.rect.x,brother.rect.y))
    for shell in shells:
        if shell.rect.y>=0 and shell.rect.y<=900 and shell.rect.x>=-50 and shell.rect.x<=1600:
            if shell.hit and time.time()-shell.time:
                if time.time()-shell.time>0.1:
                    if player.rect.x>shell.rect.x-25 and player.rect.x<shell.rect.x+75:
                        if player.health>1:
                            if player.rect.y>shell.rect.y-110 and player.rect.y<shell.rect.y-90:
                                player.score+=100
                                player.jump()
                                if not(user_input[pygame.K_UP]or user_input[pygame.K_w]):
                                    player.g=15
                                shell.hit=False
                                shell.time=time.time()
                            if player.rect.y<shell.rect.y+110 and player.rect.y>shell.rect.y-90 and time.time()-player.hptime>2:
                                player.col_enem()
                                player.hptime=time.time()
                        if player.health==1:
                            if player.rect.y>shell.rect.y-60 and player.rect.y<shell.rect.y-40:
                                player.score+=100
                                player.jump()
                                if not(user_input[pygame.K_UP]or user_input[pygame.K_w]):
                                    player.g=15
                                shell.hit=False
                            if player.rect.y<shell.rect.y+60 and player.rect.y>shell.rect.y-40 and time.time()-player.hptime>2:
                                player.col_enem()
                                player.hptime=time.time()
                for simple in simples:
                    if simple.rect.colliderect(shell.rect):
                        player.score+=500
                        simples.remove(simple)
                for comple in complexs:
                    if comple.rect.colliderect(shell.rect):
                        player.score+=500
                        complexs.remove(comple)
                shell.move(shell.speed)
            if not shell.hit and time.time()-shell.time:
                if player.rect.colliderect(shell.rect):
                    player.score+=400
                    player.jump()
                    if not(user_input[pygame.K_UP]or user_input[pygame.K_w]):
                        player.g=15
                    if player.direction=="r":
                        shell.speed=5
                    else:
                        shell.speed=-5
                    shell.hit=True
                    shell.time=time.time()
            shell.move(dy=10)
            screen.blit(shell.image,(shell.rect.x,shell.rect.y))
        else:
            shells.remove(shell)
    for podoboo in podoboos:
        if podoboo.rect.y>=0 and podoboo.rect.y<=1800 and podoboo.rect.x>=-50 and podoboo.rect.x<=1600:
            podoboo.move()
            screen.blit(podobooimg,(podoboo.rect.x,podoboo.rect.y))
    for plant in plants:
        if plant.rect.y>=0 and plant.rect.y<=900 and plant.rect.x>=-50 and plant.rect.x<=1600:
            plant.move()
            if plant.open:
                screen.blit(fo,(plant.rect.x,plant.rect.y))
            else:
                screen.blit(fc,(plant.rect.x,plant.rect.y))
        else:
            plant.rect.y=plant.location
            plant.time=0
    for ground in grounds:
        if ground.rect.y>=0 and ground.rect.y<=900 and ground.rect.x>=-50 and ground.rect.x<=1600:
            screen.blit(groundimg,(ground.rect.x,ground.rect.y))
    for block in blocks:
        if block.rect.y>=0 and block.rect.y<=900 and block.rect.x>=-50 and block.rect.x<=1600:
            screen.blit(blockimg,(block.rect.x,block.rect.y))
    for brick in bricks:
        if brick.rect.y>=0 and brick.rect.y<=900 and brick.rect.x>=-50 and brick.rect.x<=1600:
            screen.blit(brickimg,(brick.rect.x,brick.rect.y))
    for question in questions:
        if question.rect.y>=0 and question.rect.y<=900 and question.rect.x>=-50 and question.rect.x<=1600:
            if question.hit:
                screen.blit(unquestionimg,(question.rect.x,question.rect.y))
            else:
                screen.blit(questionimg,(question.rect.x,question.rect.y))
    for pipe in pipes:
        if pipe.rect.y>=0 and pipe.rect.y<=900 and pipe.rect.x>=-100 and pipe.rect.x<=1600:
            screen.blit(pipe.image,(pipe.rect.x,pipe.rect.y))
    for platform in platforms:
        if platform.rect.y>=0 and platform.rect.y<=900 and platform.rect.x>=-100 and platform.rect.x<=1600:
            screen.blit(platformimg,(platform.rect.x,platform.rect.y))
    for wall in walls:
        if wall.rect.y>=0 and wall.rect.y<=900 and wall.rect.x>=-100 and wall.rect.x<=1600:
            screen.blit(wallimg,(wall.rect.x,wall.rect.y))
    for coin in coins:
        if coin.y>=0 and coin.y<=900 and coin.x>=-50 and coin.x<=1600:
            screen.blit(coinimg,(coin.x,coin.y))
    for spike in spikes:
        if spike.rect.y>=0 and spike.rect.y<=900 and spike.rect.x>=-50 and spike.rect.x<=1600:
            screen.blit(spikeimg,(spike.rect.x,spike.rect.y))
    for brick in castlebricks:
        if brick.rect.y>=0 and brick.rect.y<=900 and brick.rect.x>=-50 and brick.rect.x<=1600:
            screen.blit(castlebrickimg,(brick.rect.x,brick.rect.y))
    for firebar in firebars:
        if firebar.rect.y>=0 and firebar.rect.y<=900 and firebar.rect.x>=-50 and firebar.rect.x<=1600:
            screen.blit(unquestionimg,(firebar.rect.x,firebar.rect.y))
            firebar.move()
            for fireball in firebar.fireballs:
                screen.blit(fireballimg,(fireball.x,fireball.y))
    screen.blit(player_label,(player.rect.x-player_label_width+25,player.rect.y-50))
    if(time.time()-player.hptime>2)or(time.time()-player.hptime>1.8 and time.time()-player.hptime<1.9)or(time.time()-player.hptime>1.6 and time.time()-player.hptime<1.7)or(time.time()-player.hptime>1.4 and time.time()-player.hptime<1.5)or(time.time()-player.hptime>1.2 and time.time()-player.hptime<1.3)or(time.time()-player.hptime>1.0 and time.time()-player.hptime<1.1)or(time.time()-player.hptime>0.8 and time.time()-player.hptime<0.9)or(time.time()-player.hptime>0.6 and time.time()-player.hptime<0.7)or(time.time()-player.hptime>0.4 and time.time()-player.hptime<0.5)or(time.time()-player.hptime>0.2 and time.time()-player.hptime<0.3)or(time.time()-player.hptime>0.0 and time.time()-player.hptime<0.1):
        screen.blit(player.image,(player.rect.x-5,player.rect.y))
    try:
        if flagrect.x>=-50 and flagrect.x<=1600 and flagrect.y>=0 and flagrect.y<=900:
            screen.blit(flagimg,(flagrect.x,flagrect.y))
    except:
        if axerect.x>=-50 and axerect.x<=1600 and axerect.y>=0 and axerect.y<=900:
            screen.blit(axeimg,(axerect.x,axerect.y))
    screen.blit(myfont.render("Lives: "+str(player.lives),0,(0,0,0)),(1500,0))
    screen.blit(myfont.render("Score: "+"0"*(10-len(str(player.score)))+str(player.score),0,(0,0,0)),(1250,0))
    if user_input[pygame.K_0]:
        volume=0.0
    if user_input[pygame.K_1]:
        volume=0.1
    if user_input[pygame.K_2]:
        volume=0.2
    if user_input[pygame.K_3]:
        volume=0.3
    if user_input[pygame.K_4]:
        volume=0.4
    if user_input[pygame.K_5]:
        volume=0.5
    if user_input[pygame.K_6]:
        volume=0.6
    if user_input[pygame.K_7]:
        volume=0.7
    if user_input[pygame.K_8]:
        volume=0.8
    if user_input[pygame.K_9]:
        volume=0.9
    if user_input[pygame.K_KP1]:
        if player.health!=1:
            player.rect=pygame.Rect(player.rect.x,player.rect.y+50,50,50)
            player.health=1
    if user_input[pygame.K_KP2]:
        if player.health<2:
            player.rect=pygame.Rect(player.rect.x,player.rect.y-50,50,100)
        player.health=2
    if user_input[pygame.K_KP3]:
        if player.health<2:
            player.rect=pygame.Rect(player.rect.x,player.rect.y-50,50,100)
        player.health=3
    if user_input[pygame.K_KP9]and time.time()-breaktime>1:
        if breakpressed:
            breakpressed=False
        else:
            breakpressed=True
        breaktime=time.time()
    if user_input[pygame.K_RETURN]and time.time()-charactertime>1:
        running=True
        name=""
        charactertime=time.time()
        while running:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running=False
            screen.fill((0,0,0))
            user_input=pygame.key.get_pressed()
            if time.time()-charactertime>0.15:
                characterpress=False
                if user_input[pygame.K_q]:
                    name+="q"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_w]:
                    name+="w"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_e]:
                    name+="e"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_r]:
                    name+="r"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_t]:
                    name+="t"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_y]:
                    name+="y"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_u]:
                    name+="u"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_i]:
                    name+="i"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_o]:
                    name+="o"
                    characterpress=True
                    charactertime=time.time()
                    charactertime=time.time()
                if user_input[pygame.K_p]:
                    name+="p"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_a]:
                    name+="a"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_s]:
                    name+="s"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_d]:
                    name+="d"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_f]:
                    name+="f"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_g]:
                    name+="g"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_h]:
                    name+="h"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_j]:
                    name+="j"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_k]:
                    name+="k"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_l]:
                    name+="l"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_z]:
                    name+="z"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_x]:
                    name+="x"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_c]:
                    name+="c"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_v]:
                    name+="v"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_b]:
                    name+="b"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_n]:
                    name+="n"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_m]:
                    name+="m"
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_SPACE]:
                    name+=" "
                    characterpress=True
                    charactertime=time.time()
                if user_input[pygame.K_LSHIFT]and characterpress:
                    oldcharacter=name[-1].upper()
                    name=name[:-1]
                    name+=oldcharacter
                if user_input[pygame.K_BACKSPACE]:
                    name=name[:-1]
                    charactertime=time.time()
            if user_input[pygame.K_RETURN]and time.time()-charactertime>1:
                running=False
                charactertime=time.time()
            player_label=myfont.render(name,0,(0,0,155))
            player_label_width=player_label.get_rect().width/2
            player_label_height=player_label.get_rect().height/2
            screen.blit(player_label,(800-player_label_width,450-player_label_height))
            pygame.display.update()
            pygame.display.flip()
    pygame.display.update()
    pygame.display.flip()
pygame.quit()
