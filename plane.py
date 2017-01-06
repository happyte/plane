#!C:/Users/Administrator/Desktop/demo/python
#coding=utf-8

#导入pygame库
import pygame,random,sys,time   #sys模块中的exit用于退出
from pygame.locals import *

#定义导弹类
class Bullet(object):
	"""Bullet"""
	def __init__(self, planeName,x,y):
		if planeName == 'enemy':        #敌机导弹向下打
			self.imageName = 'Resources/bullet-3.png'
			self.direction = 'down'
		elif planeName == 'hero':       #英雄飞机导弹向上打
			self.imageName = 'Resources/bullet-1.png'
			self.direction = 'up'
		self.image = pygame.image.load(self.imageName).convert()
		self.x = x
		self.y = y

	def draw(self,screen):
		if self.direction == 'down':
			self.y += 8
		elif self.direction == 'up':
			self.y -= 8
		screen.blit(self.image,(self.x,self.y))
	
#定义一个飞机基类		
class Plane(object):
	"""Plane"""
	def __init__(self):
		#导弹间隔发射时间1s
		self.bulletSleepTime = 0.3
		self.lastShootTime = time.time()
		#存储导弹列表
		self.bulletList = []

	#描绘飞机
	def draw(self,screen):
		screen.blit(self.image,(self.x,self.y))

	def shoot(self):
		if time.time()-self.lastShootTime>self.bulletSleepTime:
			self.bulletList.append(Bullet(self.planeName,self.x+36,self.y))
			self.lastShootTime = time.time()

#玩家飞机类，继承基类
class Hero(Plane):
	"""Hero"""
	def __init__(self):
		Plane.__init__(self)
		planeImageName = 'Resources/hero.png'
		self.image = pygame.image.load(planeImageName).convert()
		#玩家原始位置
		self.x = 200
		self.y = 600
		self.planeName = 'hero'

	#键盘控制自己飞机
	def keyHandle(self,keyValue):
		if keyValue == 'left':
			self.x -= 50
		elif keyValue == 'right':
			self.x += 50
		elif keyValue == 'up':
			self.y -= 50
		elif keyValue == 'down':
			self.y += 50

#定义敌人飞机类
class Enemy(Plane):
	"""docstring for Enemy"""
	def __init__(self,speed):
		super(Enemy, self).__init__()
		randomImageNum = random.randint(1,3)
		planeImageName = 'Resources/enemy-' + str(randomImageNum) + '.png'
		self.image = pygame.image.load(planeImageName).convert()
		#敌人飞机原始位置
		self.x = random.randint(20,400)    #敌机出现的位置任意
		self.y = 0
		self.planeName = 'enemy'
		self.direction = 'down'     #用英文表示
		self.speed = speed          #移动速度,这个参数现在需要传入

	def move(self):
		if self.direction == 'down':
			self.y += self.speed     #飞机不断往下掉


class GameInit(object):
	"""GameInit"""
	#类属性
	gameLevel = 1       #简单模式
	g_ememyList = []    #前面加上g类似全局变量
	score = 0           #用于统计分数
	hero = object

	@classmethod
	def createEnemy(cls,speed):
		cls.g_ememyList.append(Enemy(speed))

	@classmethod
	def createHero(cls):
		cls.hero = Hero()

	@classmethod
	def gameInit(cls):
		cls.createHero()

	@classmethod
	def heroPlaneKey(cls,keyValue):
		cls.hero.keyHandle(keyValue)

	@classmethod
	def draw(cls,screen):
		delPlaneList = []
		j = 0
		for i in cls.g_ememyList:
			i.draw(screen)   #画出敌机
			#敌机超过屏幕就从列表中删除
			if i.y > 680:
				delPlaneList.append(j)
			j += 1
		for m in delPlaneList:
			del cls.g_ememyList[m]


		delBulletList = []
		j = 0
		cls.hero.draw(screen)    #画出英雄飞机位置
		for i in cls.hero.bulletList:
			#描绘英雄飞机的子弹，超出window从列表中删除
			i.draw(screen)
			if i.y < 0:
				delBulletList.append(j)
			j += 1
		#删除加入到delBulletList中的导弹索引,是同步的
		for m in delBulletList:
			del cls.hero.bulletList[m]
    
    #更新敌人飞机位置
	@classmethod
	def setXY(cls):
		for i in cls.g_ememyList:
			i.move()

	#自己飞机发射子弹
	@classmethod
	def shoot(cls):
		cls.hero.shoot()
		#子弹打到敌机让敌机从列表中消失
		ememyIndex = 0
		for i in cls.g_ememyList:
			enemyRect = pygame.Rect(i.image.get_rect())
			enemyRect.left = i.x
			enemyRect.top  = i.y
			bulletIndex = 0
			for j in cls.hero.bulletList:
				bulletRect = pygame.Rect(j.image.get_rect())
				bulletRect.left = j.x
				bulletRect.top  = j.y
				if enemyRect.colliderect(bulletRect):
					#判断敌机的宽度或者高度，来知道打中哪种类型的敌机
					if enemyRect.width == 39:
						cls.score += 1000     #小中大飞机分别100,500,1000分
					elif enemyRect.width == 60:
						cls.score += 5000
					elif enemyRect.width == 78:
						cls.score += 10000
					cls.g_ememyList.pop(ememyIndex)        #敌机删除
					cls.hero.bulletList.pop(bulletIndex)   #打中的子弹删除
				bulletIndex += 1
			ememyIndex += 1

    #判断游戏是否结束
	@classmethod
	def gameover(cls):
		heroRect = pygame.Rect(cls.hero.image.get_rect())
		heroRect.left = cls.hero.x
		heroRect.top  = cls.hero.y
		for i in cls.g_ememyList:
			enemyRect = pygame.Rect(i.image.get_rect())
			enemyRect.left = i.x
			enemyRect.top  = i.y
			if heroRect.colliderect(enemyRect):
				return True
		return False

	#游戏结束后等待玩家按键
	@classmethod
	def waitForKeyPress(cls):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					cls.terminate()
				elif event.type == pygame.KEYDOWN:
					if event.key == K_RETURN:    #Enter按键
						return

	@staticmethod
	def terminate():
		pygame.quit()
		sys.exit(0)

	@staticmethod
	def pause(surface,image):
		surface.blit(image,(0,0))
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					cls.terminate()
				elif event.type == pygame.KEYDOWN:
					if event.key == K_SPACE:
						return

	@staticmethod
	def drawText(text,font,surface,x,y):
		#参数1：显示的内容 |参数2：是否开抗锯齿，True平滑一点|参数3：字体颜色|参数4：字体背景颜色
		content = font.render(text,False,(10,100,200))
		contentRect = content.get_rect()
		contentRect.left = x
		contentRect.top  = y
		surface.blit(content,contentRect)    
           
#主循环
if __name__ == '__main__':
    #初始化pygame
    pygame.init()
    #创建一个窗口与背景图片一样大
    ScreenWidth,ScreenHeight = 460,680
    easyEnemySleepTime = 1      #简单模式下每隔1s创建新的敌机
    middleEnemySleepTime = 0.5 
    hardEnemySleepTime = 0.25
    lastEnemyTime  = 0
    screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),0,32)
    pygame.display.set_caption('飞机大战')
    #参数1：字体类型，例如"arial"  参数2：字体大小
    font  = pygame.font.SysFont(None,64)
    font1 = pygame.font.SysFont("arial",24)
    #记录游戏开始的时间
    startTime = time.time()
    #背景图片加载并转换成图像
    background = pygame.image.load("Resources/bg_01.png").convert()   #背景图片
    gameover = pygame.image.load("Resources/gameover.png").convert()  #游戏结束图片
    start = pygame.image.load("Resources/startone.png")               #游戏开始图片
    gamePauseIcon = pygame.image.load("Resources/Pause.png")
    gameStartIcon = pygame.image.load("Resources/Start.png")
    screen.blit(start,(0,0))
    pygame.display.update()       #开始显示启动图片，直到有Enter键按下才会开始
    GameInit.waitForKeyPress()
    #初始化
    GameInit.gameInit()

    while True:
    	screen.blit(background,(0,0))    #不断覆盖，否则在背景上的图片会重叠
    	screen.blit(gameStartIcon,(0,0))
    	GameInit.drawText('score:%s' % (GameInit.score),font1,screen,80,15)
    	for event in pygame.event.get():
    		#print(event.type)
    		if event.type == pygame.QUIT:
    			GameInit.terminate()
    		elif event.type == KEYDOWN:
    			if event.key == K_LEFT:
    				GameInit.heroPlaneKey('left')
    			elif event.key == K_RIGHT:
    				GameInit.heroPlaneKey('right')
    			elif event.key == K_UP:
    				GameInit.heroPlaneKey('up')
    			elif event.key == K_DOWN:
    				GameInit.heroPlaneKey('down')
    			elif event.key == K_SPACE:
    				GameInit.pause(screen,gamePauseIcon) #难度选择方面有bug.因为时间一直继续
    	interval = time.time() - startTime
    	# easy模式
    	if interval < 10:
    		if time.time() - lastEnemyTime >= easyEnemySleepTime:
    			GameInit.createEnemy(5)   #传入的参数是speed
    			lastEnemyTime = time.time()
    	# middle模式
    	elif interval >= 10 and interval < 30:
    		if time.time() - lastEnemyTime >= middleEnemySleepTime:
    			GameInit.createEnemy(10)
    			lastEnemyTime = time.time()
    	# hard模式
    	elif interval >= 30:
    		if time.time() - lastEnemyTime >= hardEnemySleepTime:
    			GameInit.createEnemy(13)
    			lastEnemyTime = time.time()
    	GameInit.shoot()
    	GameInit.setXY()
    	GameInit.draw(screen)    #描绘类的位置
    	pygame.display.update()  #不断更新图片
    	if GameInit.gameover():
    		time.sleep(1)        #睡1s时间,让玩家看到与敌机相撞的画面
    		screen.blit(gameover,(0,0))
    		GameInit.drawText('%s' % (GameInit.score),font,screen,170,400)
    		pygame.display.update()
    		GameInit.waitForKeyPress()
    		break

    	

    
