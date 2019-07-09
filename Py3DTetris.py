#==========================================
#PyTetris3D - cykim8811@snu.ac.kr
#==========================================

import pygame
import math
import random as rnd

BLACK=(0,0,0)
DKGRAY=(48,48,48)
WHITE=(255,255,255)
BLUE=(32,32,195)
YELLOW=(243,243,48)
ORANGE=(227,127,32)
GREEN=(32,159,32)
RED=(195,32,32)
PINK=(227,95,95)
PURPLE=(127,32,127)
SKYBLUE=(63,63,255)

screen=[[[-1]*16 for i in range(6)] for j in range(6)]
UIscreen=[[[-1]*5 for i in range(5)] for j in range(5)]

rectList=[]
UIrectList=[]
persp=True
color=[BLUE,YELLOW,ORANGE,GREEN,RED,PURPLE,DKGRAY,SKYBLUE,PINK,WHITE]

size=100
pad_width=1920
pad_height=1080

score=0

dT=10.0

def makeT(n,i):
	return [[[i]*n for k in range(n)] for j in range(n)]

global tileData
tileData=[]

def setTileData(loc,i):
	global tileData
	x,y,z=loc
	tileData[i][x][y][z]=i

tileData.append(makeT(5,-1))
setTileData((2,2,0),len(tileData)-1)
setTileData((2,2,1),len(tileData)-1)
setTileData((2,2,2),len(tileData)-1)
setTileData((2,2,3),len(tileData)-1)

tileData.append(makeT(3,-1))
setTileData((1,0,1),len(tileData)-1)
setTileData((1,1,1),len(tileData)-1)
setTileData((1,1,2),len(tileData)-1)
setTileData((1,2,2),len(tileData)-1)

tileData.append(makeT(3,-1))
setTileData((1,0,1),len(tileData)-1)
setTileData((1,1,1),len(tileData)-1)
setTileData((1,2,1),len(tileData)-1)
setTileData((1,1,0),len(tileData)-1)

tileData.append(makeT(4,-1))
setTileData((1,1,1),len(tileData)-1)
setTileData((1,2,1),len(tileData)-1)
setTileData((2,1,1),len(tileData)-1)
setTileData((2,2,1),len(tileData)-1)

tileData.append(makeT(3,-1))
setTileData((1,0,1),len(tileData)-1)
setTileData((1,1,1),len(tileData)-1)
setTileData((1,2,1),len(tileData)-1)
setTileData((1,2,0),len(tileData)-1)

tileData.append(makeT(3,-1))
setTileData((0,1,1),len(tileData)-1)
setTileData((1,0,1),len(tileData)-1)
setTileData((1,1,1),len(tileData)-1)
setTileData((1,1,2),len(tileData)-1)

tileData.append(makeT(2,-1))
setTileData((0,0,0),len(tileData)-1)
setTileData((1,0,0),len(tileData)-1)
setTileData((1,1,0),len(tileData)-1)
setTileData((1,1,1),len(tileData)-1)

tileData.append(makeT(2,-1))
setTileData((0,1,0),len(tileData)-1)
setTileData((1,1,0),len(tileData)-1)
setTileData((1,0,0),len(tileData)-1)
setTileData((1,0,1),len(tileData)-1)



class Rect():
	def __init__(self,p=[(0,0,0)*4],c=WHITE,s=(0,0,0)):
		self.pos=p
		self.col=c
		self.shade=(0,0,0)
		self.sideLight=s
		rectList.append(self)
	def getPointList(self,screenCenter):
		global cam
		return [sumVec2(getPointOnScreen(pt),screenCenter) for pt in self.pos]
	def destroy(self):
		rectList.remove(self)
	def getMid(self):
		mPos=(0,0,0)
		for m in self.pos:
			mPos=sumVec(mPos,m)
		return calcVec(mPos,(4,4,4),lambda x,y:x/y)
		#return tuple([i/4 for i in mPos])
	def getCol(self):
		return addCol(addCol(self.col,self.shade),self.sideLight)

class UIRect():
	def __init__(self,p=[(0,0,0)*4],c=WHITE,s=(0,0,0)):
		self.pos=p
		self.col=c
		self.shade=(0,0,0)
		self.sideLight=s
		UIrectList.append(self)
	def getPointList(self,screenCenter):
		global cam
		return [sumVec2(UIgetPointOnScreen(pt),screenCenter) for pt in self.pos]
	def destroy(self):
		UIrectList.remove(self)
	def getMid(self):
		mPos=(0,0,0)
		for m in self.pos:
			mPos=sumVec(mPos,m)
		return calcVec(mPos,(4,4,4),lambda x,y:x/y)
		#return tuple([i/4 for i in mPos])
	def getCol(self):
		return addCol(addCol(self.col,self.shade),self.sideLight)


def getMidF(dL):
	mPos=(0,0,0)
	for m in dL:
		mPos=sumVec(mPos,m)
	return calcVec(mPos,(4,4,4),lambda x,y:x/y)
def dot(v1,v2):
	x1,y1,z1=v1
	x2,y2,z2=v2
	return (x1*x2)+(y1*y2)+(z1*z2)
def norm(v):
	x,y,z=v
	l=math.sqrt(dot(v,v))
	return (x/l,y/l,z/l)
def pyToVec(py,l):
	pitch,yaw=py
	return (l*math.cos(yaw)*math.cos(pitch),l*math.sin(yaw)*math.cos(pitch),l*math.sin(pitch))
def sumVec(v1,v2):
	x1,y1,z1=v1
	x2,y2,z2=v2
	return (x1+x2,y1+y2,z1+z2)
def subVec(v1,v2):
	x1,y1,z1=v1
	x2,y2,z2=v2
	return (x1-x2,y1-y2,z1-z2)
def spinOnAxis(v,axis,angle):
	return 0
	#not coded yet
def cross(v1,v2):
	x1,y1,z1=v1
	x2,y2,z2=v2
	return (y1*z2-y2*z1,z1*x2-z2*x1,x1*y2-x2*y1)
def sumVec2(v1,v2):
	x1,y1=v1
	x2,y2=v2
	return (x1+x2,y1+y2)
def getScreenBox(scr):
	return (0,0,0,len(scr),len(scr[0]),len(scr[0][0]))
def calcVec(v1,v2,f):
	x1,y1,z1=v1
	x2,y2,z2=v2
	return(f(x1,x2),f(y1,y2),f(z1,z2))
def vecToPy(v):
	v=norm(v)
	x,y,z=v
	if y>=0:
		return (math.atan(y/x),math.asin(z))
	else:
		return (math.atan(y/x)+math.pi,math.asin(z))
def dist(v1,v2):
	return math.sqrt(math.pow(v1[0]-v2[0],2)+math.pow(v1[1]-v2[1],2)+math.pow(v1[2]-v2[2],2))
def addCol(col1,col2):
	r1,g1,b1=col1
	r2,g2,b2=col2
	return (max(0,min(255,r1+r2)),max(0,min(255,g1+g2)),max(0,min(255,b1+b2)))
def getPointOnScreen(point):
	global camAngle, idep, iv, ih, cam
	dV=subVec(point,cam[0])
	l=dot(idep,dV)
	rat=camAngle/l
	dV=calcVec((rat,rat,rat),dV,lambda x,y:x*y)
	#dV=tuple(map(lambda x:x*rat,dV))
	return (dot(ih,dV),dot(iv,dV))
def UIgetPointOnScreen(point):
	global camAngle, UIidep, UIiv, UIih, UIcam
	dV=subVec(point,UIcam[0])
	l=dot(UIidep,dV)
	rat=camAngle/l
	dV=calcVec((rat,rat,rat),dV,lambda x,y:x*y)
	#dV=tuple(map(lambda x:x*rat,dV))
	return (dot(UIih,dV),dot(UIiv,dV))

def getScreen(loc):
	global screen
	x,y,z=loc
	return screen[x][y][z]
def getListVec(lst,vec,deft):
	if (len(lst)>vec[0])&(len(lst[0])>vec[1])&(len(lst[0][0])>vec[2]):
		return lst[vec[0]][vec[1]][vec[2]]
	else:
		return deft


def isOccupied(loc,tile):
	global screen
	ret=False
	for (x,l) in enumerate(tile):
		for (y,m) in enumerate(l):
			for (z,d) in enumerate(m):
				if d!=-1:
					if (getScreen(sumVec(loc,(x,y,z)))!=-1):
						ret=True
	return ret



def isColliding(loc,dt,tile):
	global screen
	clearTile(loc,tile)
	ret=False
	for x in range(len(tile)):
		for y in range(len(tile)):
			for z in range(len(tile)):
				if getListVec(tile,(x,y,z),-1)!=-1:
					if isInBox(sumVec(sumVec(loc,dt),(x,y,z)),getScreenBox(screen)):
						if (getScreen(sumVec(sumVec(loc,(x,y,z)),dt))!=-1):
							ret=True
					else:
						ret=True
	moveTile(loc,(0,0,0),tile)
	return ret
def isCol(loc,tile,loc2,tileE):
	global screen
	clearTile(loc2,tileE)
	ret=False
	for x in range(len(tile)):
		for y in range(len(tile)):
			for z in range(len(tile)):
				if getListVec(tile,(x,y,z),-1)!=-1:
					if isInBox(sumVec(loc,(x,y,z)),getScreenBox(screen)):
						if (getScreen(sumVec(loc,(x,y,z)))!=-1):
							ret=True
					else:
						ret=True
	moveTile(loc2,(0,0,0),tileE)
	return ret
def moveTile(loc,dl,tile):
	global screen
	ret=False
	for (x,l) in enumerate(tile):
		for (y,m) in enumerate(l):
			for (z,d) in enumerate(m):
				if d!=-1:
					setBlock(sumVec(loc,(x,y,z)),-1)
	for (x,l) in enumerate(tile):
		for (y,m) in enumerate(l):
			for (z,d) in enumerate(m):
				if d!=-1:
					setBlock(sumVec(sumVec(loc,(x,y,z)),dl),d)
def clearTile(loc,tile):
	global screen
	ret=False
	for (x,l) in enumerate(tile):
		for (y,m) in enumerate(l):
			for (z,d) in enumerate(m):
				if d!=-1:
					setBlock(sumVec(loc,(x,y,z)),-1)


def isInBox(loc,box):
	res=True
	for i in range(3):
		if not (loc[i]>=box[i]):
			res=False
		if not loc[i]<=(box[i]+box[i+3]-1):
			res=False
	return res
def drawCube(loc,col):
	global gamepad, clock , cam
	p,y=cam[1]
	pi=math.pi
	pl=[
	(sumVec((0,0,-size/2),pyToVec((0,(1+2*i)*pi/4),size/2*math.sqrt(2)))) for i in range(4)]+[
	(sumVec((0,0,size/2),pyToVec((0,(1+2*i)*pi/4),size/2*math.sqrt(2)))) for i in range(4)
	]
	for (i,v) in enumerate(pl):
		pl[i]=sumVec(loc,v)

	cLoc=cam[0]
	drawRect([pl[i] for i in [0,1,2,3]],col)
	drawRect([pl[i] for i in [4,5,6,7]],col)
	drawRect([pl[i] for i in [0,1,5,4]],col)
	drawRect([pl[i] for i in [2,3,7,6]],col)
	drawRect([pl[i] for i in [1,2,6,5]],col)
	drawRect([pl[i] for i in [3,0,4,7]],col)
def setBlock(loc,cube):
	testList=[
	(1,0,0),
	(-1,0,0),
	(0,1,0),
	(0,-1,0),
	(0,0,1),
	(0,0,-1),
	]
	dirLight=[6,-6,15,-15,9,-9]
	for i,dll in enumerate(dirLight):
		dirLight[i]=(dll,dll,dll)
	global screen
	rLoc=calcVec(loc,(size,size,size),lambda x,y:x*y)
	if cube!=-1:
		
		rp=[]
		for rt in rectList:
			if dist(rt.getMid(),rLoc)<size*0.6:
				rp.append(rt)
		rpl=len(rp)
		for i in range(rpl):
			rp[rpl-i-1].destroy()

		for (i,cb) in enumerate(testList):
			if not isInBox(sumVec(loc,cb),getScreenBox(screen)):
				Rect(tmpFnc1(cb,rLoc),color[cube],dirLight[i])
			elif getScreen(sumVec(loc,cb))==-1:
				Rect(tmpFnc1(cb,rLoc),color[cube],dirLight[i])

	elif getScreen(loc)!=-1:

		dirLight=[6,-6,15,-15,9,-9]
		for i,dll in enumerate(dirLight):
			dirLight[i]=(dll,dll,dll)
		rp=[]
		for rt in rectList:
			if dist(rt.getMid(),rLoc)<size*0.6:
				rp.append(rt)
		rpl=len(rp)
		for i in range(rpl):
			rp[rpl-i-1].destroy()

		for i,cb in enumerate(testList):
			if isInBox(sumVec(loc,cb),getScreenBox(screen)):
				if getScreen(sumVec(loc,cb))!=-1:
					Rect(tmpFnc1(cb,rLoc),color[getScreen(sumVec(loc,cb))],dirLight[i])
	screen[loc[0]][loc[1]][loc[2]]=cube

	global shouldUpdate
	shouldUpdate=True
'''
def UIsetBlock(loc,cube):
	testList=[
	(1,0,0),
	(-1,0,0),
	(0,1,0),
	(0,-1,0),
	(0,0,1),
	(0,0,-1),
	]
	dirLight=[4,-4,20,-20,12,-12]
	for i,dll in enumerate(dirLight):
		dirLight[i]=(dll,dll,dll)
	global UIscreen
	rLoc=calcVec(loc,(size,size,size),lambda x,y:x*y)
	if cube!=-1:
		
		rp=[]
		for rt in UIrectList:
			if dist(rt.getMid(),rLoc)<size*0.6:
				rp.append(rt)
		rpl=len(rp)
		for i in range(rpl):
			rp[rpl-i-1].destroy()

		for (i,cb) in enumerate(testList):
			if not isInBox(sumVec(loc,cb),getScreenBox(UIscreen)):
				UIRect(tmpFnc1(cb,rLoc),color[cube],dirLight[i])
			elif getListVec(UIscreen,sumVec(loc,cb),-1)==-1:
				UIRect(tmpFnc1(cb,rLoc),color[cube],dirLight[i])

	elif getListVec(UIscreen,loc,-1)!=-1:

		dirLight=[-4,4,-20,20,-12,12]
		for i,dll in enumerate(dirLight):
			dirLight[i]=(dll,dll,dll)
		rp=[]
		for rt in UIrectList:
			if dist(rt.getMid(),rLoc)<size*0.6:
				rp.append(rt)
		rpl=len(rp)
		for i in range(rpl):
			rp[rpl-i-1].destroy()

		for i,cb in enumerate(testList):
			if isInBox(sumVec(loc,cb),getScreenBox(UIscreen)):
				if getListVec(UIscreen,sumVec(loc,cb),-1)!=-1:
					UIRect(tmpFnc1(cb,rLoc),color[getListVec(UIscreen,sumVec(loc,cb),-1)],dirLight[i])
	UIscreen[loc[0]][loc[1]][loc[2]]=cube

	global shouldUpdate
	shouldUpdate=True
'''
def UIsetBlock(loc,cube):
	testList=[
	(1,0,0),
	(-1,0,0),
	(0,1,0),
	(0,-1,0),
	(0,0,1),
	(0,0,-1),
	]
	dirLight=[4,-4,20,-20,12,-12]
	for i,dll in enumerate(dirLight):
		dirLight[i]=(dll,dll,dll)
	global UIscreen
	rLoc=calcVec(loc,(size,size,size),lambda x,y:x*y)
	if cube!=-1:
		for (i,cb) in enumerate(testList):
			UIRect(tmpFnc1(cb,rLoc),color[cube],dirLight[i])
	UIscreen[loc[0]][loc[1]][loc[2]]=cube
def tmpFnc1(dl,loc):
	global size
	t=[
	[size/2,size/2],
	[size/2,-size/2],
	[-size/2,-size/2],
	[-size/2,size/2],
	]
	k=[]
	for i in t:
		a=0
		b=[]
		for j in list(dl):
			if j!=0:
				b.append(j*size/2)
			else:
				b.append(i[a])
				a+=1
		k.append(sumVec(loc,tuple(b)))
	return k#change (0,1,0) into [(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
def checkDone():
	global endGame
	for x in range(len(screen)):
		for y in range(len(screen[0])):
			if screen[x][y][9]!=-1:
				endGame=True
def checkFill():
	checkDone()
	again=False
	for z in range(1,len(screen[0][0])):
		if not again:
			isLineFull=True
			for x in range(len(screen)):
				for y in range(len(screen[0])):
					if screen[x][y][z]==-1:
						isLineFull=False
			if isLineFull:
				for x in range(len(screen)):
					for y in range(len(screen[0])):
						setBlock((x,y,z),-1)
						for z2 in range(z,len(screen[0][0])-1):
							setBlock((x,y,z2),getScreen((x,y,z2+1)))
							again=True
	if again:
		global score
		score+=1
		checkFill()
def updateShade():
	global shade,rectList
	srL=[]
	mz=len(screen[0][0])
	for x in range(6):
		for y in range(6):
			shaded=False
			for z in range(mz):
				if screen[x][y][mz-1-z]!=-1:
					shaded=True
				if shaded&(screen[x][y][mz-1-z]==-1):
					for rt in rectList:
						if dist(rt.getMid(),(size*x,size*y,size*(mz-1-z)))<size:
							srL.append(rt)
	for rl in rectList:
		rl.shade=(0,0,0)
	for rl in srL:
		if rl.sideLight[0]==-12:
			rl.shade=(-40,-40,-40)
		else:
			rl.shade=(-30,-30,-30)
def setNextTile():
	global nextTile,curTile
	curTile=tileData[nextTile]
	nextTile=math.floor(rnd.random()*len(tileData))
	l=len(UIrectList)
	for i in range(l):
		UIrectList[l-i-1].destroy()
	UIscreen=makeT(len(tileData[nextTile]),-1)
	for x in range(len(tileData[nextTile])):
		for y in range(len(tileData[nextTile])):
			for z in range(len(tileData[nextTile])):
				if tileData[nextTile][x][y][z]!=-1:
					UIsetBlock((x,y,z),nextTile)


def rotate(tile):
	lT=makeT(len(tile),-1)
	for (x,l) in enumerate(tile):
		for (y,m) in enumerate(l):
			for (z,d) in enumerate(m):
				lT[y][len(tile)-1-x][z]=d
	return lT
def rotateR(tile,dirI):
	lT=makeT(len(tile),-1)
	for x in range(len(tile)):
		for y in range(len(tile[0])):
			for z in range(len(tile[0][0])):
				m=len(tile)-1
				rL=[
				(x,m-z,y),
				(z,y,m-x),
				(x,z,m-y),
				(m-z,y,x)
				]
				lT[rL[dirI][0]][rL[dirI][1]][rL[dirI][2]]=tile[x][y][z]
	return lT

def done():
	global endGame
	if endGame==False:
		endGame=True

def initGame():

	global ft, endGame,fontEnd
	pygame.font.init()
	ft = pygame.font.SysFont("comicsansms", 20)
	fontEnd=pygame.font.SysFont("comicsansms", 200)
	endGame=False

	global tilePos,curTile,fallDelay,fallDelayMax
	tilePos=(1,1,10)
	curTile=tileData[math.floor(rnd.random()*8)]
	moveTile(tilePos,(0,0,0),curTile)
	fallDelayMax=100
	fallDelay=0.0
	fallDelay=fallDelayMax

	global nextTile
	nextTile=math.floor(rnd.random()*8)


	global gamepad, clock , cam ,screen ,camAngle,size,camVD,camDist,camElev,shouldUpdate
	pygame.init()
	gamepad=pygame.display.set_mode((pad_width,pad_height),pygame.FULLSCREEN)
	pygame.display.set_caption("Main")
	clock=pygame.time.Clock()
	camVD=math.pi/4
	camDist=size*25
	camElev=size*6
	shouldUpdate=False

	global UIcam,UIcamVD,UIcamDist,UIcamElev
	UIcamVD=math.pi/4
	UIcamDist=size*30
	UIcamElev=size*2

	global isKeyPressed,keyDelay,keyDelayMax,camPosDir,UIcamPosDir
	isKeyPressed=[False]*1000
	keyDelay=[-1]*1000
	keyDelayMax=8



	cam=[(size*(-4),size*(-4),size*5),(0,0)]
	camPosDir=0

	UIcam=[(size*(-4),size*(-4),size*5),(0,0)]
	UIcamPosDir=0

	global camAngle, idep, iv, ih
	camAngle=pad_width+math.tan(40*math.pi/180)
	cX,cY,cZ=cam[0]
	p,y=cam[1]
	idep=pyToVec((p,y),1)
	iv=pyToVec((p-math.pi/2,y),1)
	ih=norm(cross(idep,iv))





	for i in range(6):
		for j in range(6):
			setBlock((i,j,0),9)
	updateCam()

	UIscreen=makeT(len(tileData[nextTile]),-1)
	for x in range(len(tileData[nextTile])):
		for y in range(len(tileData[nextTile])):
			for z in range(len(tileData[nextTile])):
				if tileData[nextTile][x][y][z]!=-1:
					UIsetBlock((x,y,z),nextTile)

	global UIidep, UIiv, UIih
	cX,cY,cZ=UIcam[0]
	p,y=UIcam[1]
	UIidep=pyToVec((p,y),1)
	UIiv=pyToVec((p-math.pi/2,y),1)
	UIih=norm(cross(idep,iv))
	updateUICam()

	runGame()
def drawRect(dl,col):
	pygame.draw.polygon(gamepad,col,dl)
	pygame.draw.polygon(gamepad,addCol(col,(-64,-64,-64)),dl,4)
def updateCam():
	global camVD,camPosDir,camDist,cam,camElev,dT
	cPos=sumVec((size*2.5,size*2.5,camElev),pyToVec((camVD,camPosDir+math.pi),camDist))
	cam=(cPos,(-camVD,camPosDir))

	global idep, iv, ih
	idep=pyToVec(cam[1],1)
	iv=pyToVec((cam[1][0]-math.pi/2,cam[1][1]),1)
	ih=norm(cross(idep,iv))
def updateUICam():
	global UIcamVD,UIcamPosDir,UIcamDist,UIcam,UIcamElev,dT
	gC=size*(float(len(tileData[nextTile])-1)/2)
	UIcPos=sumVec((gC,gC,UIcamElev),pyToVec((UIcamVD,UIcamPosDir+math.pi),UIcamDist))
	UIcam=[UIcPos,(-UIcamVD,UIcamPosDir)]

	global UIidep, UIiv, UIih
	UIidep=pyToVec(UIcam[1],1)
	UIiv=pyToVec((UIcam[1][0]-math.pi/2,UIcam[1][1]),1)
	UIih=norm(cross(UIidep,UIiv))

def drawText(pos,txt,col=(255,255,255)):
	global ft
	text=ft.render(txt,True,col)
	tt=text.get_rect()
	tt.center=sumVec2(pos,(text.get_width()/2,text.get_height()/2))
	gamepad.blit(text,tt)

def gameTick():
	global gamepad, clock , cam
	loc,py=cam
	p,y=py

	global isKeyPressed,keyDelay,keyDelayMax

	global tilePos,curTile,fallDelay,fallDelayMax,camDist,camPosDir,camElev,camAngle

	for (i,k) in enumerate([pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT]):
		keyDelay[k]=max(0,keyDelay[k]-1)
		if isKeyPressed[k]&(keyDelay[k]==0):
			keyDelay[k]=keyDelayMax

			if isColliding(tilePos,(0,0,-1),curTile):
				fallDelay=fallDelayMax
			mV=tuple(map(round,pyToVec((0,(math.pi/2)*(i+round(y/(math.pi/2)))),1)))
			if not isColliding(tilePos,mV,curTile):
				moveTile(tilePos,mV,curTile)
				tilePos=sumVec(tilePos,mV)

	drawText((0,pad_height-32*6),"A,D:Spin Camera")
	drawText((0,pad_height-32*5),"W,S:Joom In/Out")
	drawText((0,pad_height-32*4),"Arrow:Move Tetris")
	drawText((0,pad_height-32*3),"R,F:Spin Tetris")
	drawText((0,pad_height-32*2),"Space:Drop Tetris")


	spd=dT
	if isKeyPressed[pygame.K_w]:
		camDist=max(size*2,camDist-spd*4)
		updateCam()
	if isKeyPressed[pygame.K_s]:
		camDist=min(size*60,camDist+spd*4)
		updateCam()
	if isKeyPressed[pygame.K_a]:
		camPosDir+=(math.pi/4)*dT/100
		updateCam()
	if isKeyPressed[pygame.K_d]:
		camPosDir-=(math.pi/4)*dT/100
		updateCam()
	if isKeyPressed[pygame.K_e]:
		camElev+=spd
		updateCam()
	if isKeyPressed[pygame.K_q]:
		camElev-=spd
		updateCam()

	if endGame:
		camPosDir+=math.pi/300
		updateCam()

	global UIcamPosDir
	UIcamPosDir+=math.pi/500

	fallDelay-=dT/10
	if (fallDelay<=0)&(not endGame):
		fallDelay=fallDelayMax
		if not isColliding(tilePos,(0,0,-1),curTile):
			moveTile(tilePos,(0,0,-1),curTile)
			tilePos=sumVec(tilePos,(0,0,-1))
		else:
			checkFill()
			setNextTile()
			tilePos=(1,1,10)
			if (not isOccupied(tilePos,curTile))&(not endGame):
				moveTile(tilePos,(0,0,0),curTile)
			else:
				done()
	updateUICam()


def getDepth(rect):
	global cam
	mPos=rect.getMid()
	return dot(pyToVec(cam[1],1),calcVec(mPos,cam[0],lambda x,y:x-y))

def UIgetDepth(rect):
	global UIcam
	mPos=rect.getMid()
	return dot(pyToVec(UIcam[1],1),calcVec(mPos,UIcam[0],lambda x,y:x-y))

def draw():
	global gamepad,clock ,cube , cam
	cLoc,cPy=cam
	cX,cY,cZ=cLoc
	UIcLoc,UIcPy=UIcam
	rectDraw=sorted(rectList,reverse=True,key=getDepth)
	UIrectDraw=sorted(UIrectList,reverse=True,key=UIgetDepth)
	for rt in rectDraw:
		if dot(norm(subVec(rt.getMid(),cLoc)),pyToVec(cPy,10))>6:
			drawRect([sumVec2(getPointOnScreen(rt.pos[i]),(pad_width/2,pad_height/2)) for i in range(4)],rt.getCol())

	for rt in UIrectDraw:
		if dot(norm(subVec(rt.getMid(),UIcLoc)),pyToVec(UIcPy,10))>6:
			drawRect([sumVec2(UIgetPointOnScreen(rt.pos[i]),(pad_width*5/6,pad_height/4)) for i in range(4)],rt.getCol())

	drawText((0,0),"score:"+str(score))
	drawText((0,32),"fps:"+str(round(clock.get_fps())))

	if endGame:
		global fontEnd
		text=fontEnd.render("Score:"+str(score),True,(48,195,48))
		tt=text.get_rect()
		tt.center=(pad_width/2,pad_height/2)
		gamepad.blit(text,tt)

	global shouldUpdate
	if shouldUpdate:
		updateShade()
		shouldUpdate=False

	

def runGame():
	global gamepad, clock , cam, persp, cubeOnHand, camAngle,curTile,tilePos,camVD,camDist,camPosDir,dT

	crashed=False
	while not crashed:
		for event in pygame.event.get():
			#===Events=====
			evt=event.type
			if evt==pygame.QUIT:
				crashed=True
			elif evt==pygame.KEYDOWN:
				evk=event.key
				isKeyPressed[evk]=True
				if evk==pygame.K_r:
					brk=False
					for cP in [(0,0,0),(0,-1,0),(-1,0,0),(0,1,0),(1,0,0)]:
						if not brk:
							if isColliding(tilePos,(0,0,-1),curTile):
								fallDelay=fallDelayMax
							if not isCol(sumVec(cP,tilePos),rotate(curTile),tilePos,curTile):
								brk=True
								clearTile(tilePos,curTile)
								curTile=rotate(curTile)
								tilePos=sumVec(tilePos,cP)
								moveTile(tilePos,(0,0,0),curTile)
				elif evk==pygame.K_f:
					brk=False
					tLst=[(0,0,0),(0,-1,0),(-1,0,0),(0,1,0),(1,0,0)]
					for cP in [(0,0,0),(0,-1,0),(-1,0,0),(0,1,0),(1,0,0)]:
						if not brk:
							if isColliding(tilePos,(0,0,-1),curTile):
								fallDelay=fallDelayMax
							if not isCol(sumVec(cP,tilePos),rotateR(curTile,round(cam[1][1]/(math.pi/2))%4),tilePos,curTile):
								brk=True
								clearTile(tilePos,curTile)
								curTile=rotateR(curTile,round(cam[1][1]/(math.pi/2))%4)
								tilePos=sumVec(tilePos,cP)
								moveTile(tilePos,(0,0,0),curTile)

				elif evk==pygame.K_p:
					persp=not persp
				elif evk==pygame.K_SPACE:
					fallDelay=fallDelayMax
					if not endGame:
						while not isColliding(tilePos,(0,0,-1),curTile):
							moveTile(tilePos,(0,0,-1),curTile)
							tilePos=sumVec(tilePos,(0,0,-1))
						setNextTile()
						checkFill()
						tilePos=(1,1,10)
						if not isOccupied(tilePos,curTile):
							moveTile(tilePos,(0,0,0),curTile)
						else:
							done()

				elif evk==pygame.K_ESCAPE:
					crashed=True
			elif evt==pygame.KEYUP:
				evk=event.key
				isKeyPressed[evk]=False
				for k in [pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT]:
					keyDelay[k]=0
			elif event.type == pygame.MOUSEMOTION:
				if False:#(not endGame):
					global camPosDir
					camPosDir+=(event.pos[0]-(pad_width/2))*(math.pi)/pad_width
					pygame.mouse.set_pos([pad_width/2,pad_height/2])
					updateCam()
		gamepad.fill(BLACK)
		gameTick()
		draw()
		pygame.display.update()
		dT=clock.tick(100)

	pygame.quit()


#=====Start Game=====
import cProfile
#cProfile.run('initGame()')
initGame()
print("score:"+str(score))
input()