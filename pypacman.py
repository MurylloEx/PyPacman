import pyxel
from enum import Enum, IntEnum

#region Enumeradores do jogo.

class PACMAN_SPRITES_ID(IntEnum):
    #Pacman
    PACMAN_CLOSED           = 0x0001
    PACMAN_OPEN_RIGHT       = 0x0002
    PACMAN_OPEN_LEFT        = 0x0003
    PACMAN_OPEN_UP          = 0x0004
    PACMAN_OPEN_DOWN        = 0x0005
    #Fantasminha vermelho
    GHOST_RED_LEFT          = 0x0006
    GHOST_RED_RIGHT         = 0x0007
    GHOST_RED_DOWN          = 0x0008
    GHOST_RED_UP            = 0x0009
    #Fantasminha rosa
    GHOST_PINK_LEFT         = 0x000A
    GHOST_PINK_RIGHT        = 0x000B
    GHOST_PINK_DOWN         = 0x000C
    GHOST_PINK_UP           = 0x000D
    #Fantasminha laranja
    GHOST_ORANGE_LEFT       = 0x000E
    GHOST_ORANGE_RIGHT      = 0x000F
    GHOST_ORANGE_DOWN       = 0x0010
    GHOST_ORANGE_UP         = 0x0011
    #Fantasminha azul
    GHOST_BLUE_LEFT         = 0x0012
    GHOST_BLUE_RIGHT        = 0x0013
    GHOST_BLUE_DOWN         = 0x0014
    GHOST_BLUE_UP           = 0x0015
    #Fantasminhas comestíveis
    GHOST_EATABLE_DARK      = 0x0016
    GHOST_EATABLE_WHITE     = 0x0017
    #Olhos dos fantasminhas
    GHOST_EYES_LEFT         = 0x0018
    GHOST_EYES_RIGHT        = 0x0019
    GHOST_EYES_DOWN         = 0x001A
    GHOST_EYES_UP           = 0x001B
    #Comidas
    CHERRY_FOOD             = 0x001C
    WHITE_FOOD              = 0x001D
    BIG_WHITE_FOOD          = 0x001E
    #Pacman Logo
    PACMAN_LOGO             = 0x001F

class PACMAN_SPRITES_POS(tuple):
    #Pacman
    PACMAN_CLOSED           = (0, 0)
    PACMAN_OPEN_RIGHT       = (0, 16)
    PACMAN_OPEN_LEFT        = (0, 32)
    PACMAN_OPEN_UP          = (0, 48)
    PACMAN_OPEN_DOWN        = (0, 64)
    #Fantasminha vermelho
    GHOST_RED_LEFT          = (0,  80)
    GHOST_RED_RIGHT         = (16, 80)
    GHOST_RED_DOWN          = (32, 80)
    GHOST_RED_UP            = (48, 80)
    #Fantasminha rosa
    GHOST_PINK_LEFT         = (0,  96)
    GHOST_PINK_RIGHT        = (16, 96)
    GHOST_PINK_DOWN         = (32, 96)
    GHOST_PINK_UP           = (48, 96)
    #Fantasminha laranja
    GHOST_ORANGE_LEFT       = (0,  112)
    GHOST_ORANGE_RIGHT      = (16, 112)
    GHOST_ORANGE_DOWN       = (32, 112)
    GHOST_ORANGE_UP         = (48, 112)
    #Fantasminha azul
    GHOST_BLUE_LEFT         = (0,  128)
    GHOST_BLUE_RIGHT        = (16, 128)
    GHOST_BLUE_DOWN         = (32, 128)
    GHOST_BLUE_UP           = (48, 128)
    #Fantasminhas comestíveis
    GHOST_EATABLE_DARK      = (0, 160)
    GHOST_EATABLE_WHITE     = (0, 160)
    #Olhos dos fantasminhas
    GHOST_EYES_LEFT         = (0,  144)
    GHOST_EYES_RIGHT        = (16, 144)
    GHOST_EYES_DOWN         = (32, 144)
    GHOST_EYES_UP           = (48, 144)
    #Comidas
    CHERRY_FOOD             = (16, 0)
    WHITE_FOOD              = (16, 16)
    BIG_WHITE_FOOD          = (16, 32)
    #Pacman Logo
    PACMAN_LOGO             = (0, 0)

class PACMAN_DIRECTION(IntEnum):
    RIGHT   = 0
    LEFT    = 1
    UP      = 2
    DOWN    = 3

class GAME_STATE(IntEnum):
    PAUSED  = 0x0000
    READY   = 0x0001
    RUNNING = 0x0002

#endregion

#region Funções de desenho VIRTUAIS (São chamadas para adicionar a imagem na fila para serem desenhados).

#Cria e inicializa um novo buffer Virtual Graphics.
def VgQueueCreateBuffer():
    return []

#Define uma tupla com as posições x, y
def VgSetPoint(x: int, y: int):
    return (x, y)

#Define uma tupla com o tamanho do objeto.
def VgSetSize(width: int, height: int):
    return (width, height)

#Obtém a estrutura de índice do objeto a ser desenhado.
def VgAcquireObjectIndex(objPos: PACMAN_SPRITES_POS, objId: PACMAN_SPRITES_ID, imgBank: int, size: tuple, transpColorKey: int = None):
    return [objPos, imgBank, objId, transpColorKey, size]

#Adiciona no buffer [objectIndex, z_Order, point, transpKey]
#Adiciona um objeto no buffer para ser desenhado na próxima vez.
def VgQueueAddObjectToDraw(pVgBuffer: list, objectIndex: list, z_Order: int, point: tuple):
    pVgBuffer.append([objectIndex, z_Order, point])

#Limpa o buffer de escrita.
def VgQueueReleaseBuffer(pVgBuffer: list):
    while (VgQueueNextObjectToDraw(pVgBuffer) != None):
        continue
    pVgBuffer = None

#Retorno [objectIndex, z_Order, point, transpKey]
#Retira o proximo objeto do buffer que será desenhado na tela.
def VgQueueNextObjectToDraw(pVgBuffer: list):
    if (len(pVgBuffer) > 0):
        bStart = True
        lowerZ = int(0)
        lastIndex = 0
        nextVgObject = []
        for VgIndex in range(len(pVgBuffer)):
            if (bStart == True):
                bStart = False
                lowerZ = pVgBuffer[VgIndex][1]
                nextVgObject = pVgBuffer[VgIndex]
                lastIndex = VgIndex
            else:
                if (lowerZ > pVgBuffer[VgIndex][1]):
                    lowerZ = pVgBuffer[VgIndex][1]
                    nextVgObject = pVgBuffer[VgIndex]
                    lastIndex = VgIndex
        pVgBuffer.pop(lastIndex)
        return nextVgObject
    else:
        return None

#Retorna um novo buffer contendo os objetos cujo ID é o objId.
#Verifique que a função retorna um buffer vazio equivalente a
#VgQueueCreateBuffer() caso nenhum objeto com o ID objId seja
#encontrado no buffer fornecido.
def VgQueueGetElementsById(pVgBuffer: list, objId: PACMAN_SPRITES_ID):
    vgElements = VgQueueCreateBuffer()
    for VgObject in pVgBuffer:
        spriteId = VgObject[0][2]
        if (spriteId == objId):
            vgElements.append(VgObject)
    return vgElements

#Move o conteúdo de um buffer VG para outro buffer VG.
#Essa função reduz o desempenho do jogo se for usada excessivamente.
def VgQueueMoveBuffer(pToVgBuffer: list, pFromVgBuffer: list):
    vgObj = VgQueueNextObjectToDraw(pFromVgBuffer)
    while (vgObj != None):
        VgQueueAddObjectToDraw(pToVgBuffer, vgObj[0], vgObj[1], vgObj[2], vgObj[3])
        vgObj = VgQueueNextObjectToDraw(pFromVgBuffer)

#Copia o conteúdo de um buffer VG para outro buffer VG.
#Essa função é mais rápida que VgQueueMoveBuffer pois não
#é feita verificação do vetor Z.
def VgQueueCopyBuffer(pToVgBuffer: list, pFromVgBuffer: list):
    for k in range(len(pFromVgBuffer)):
        pToVgBuffer.append(pFromVgBuffer[k])

#endregion

#region Funções operação de tela (Operation Screen) para desenhar o jogo.

#Escreve um texto na tela
def OpScrWriteTextInPosition(text: str, position: tuple, color: int):
    pyxel.text(position[0], position[1], text, color)

#Desenha uma imagem na tela
def OpScrDrawImageInPosition(VgObject: list):
    imgPos = VgObject[2]
    imgSize = VgObject[0][4]
    spritePos = VgObject[0][0]
    spriteId = VgObject[0][2]
    transpKey = VgObject[0][3]
    imgBank = VgObject[0][1]
    if (transpKey != None):
        pyxel.blt(imgPos[0], imgPos[1], imgBank, spritePos[0], spritePos[1], imgSize[0], imgSize[1], transpKey)
    else:
        pyxel.blt(imgPos[0], imgPos[1], imgBank, spritePos[0], spritePos[1], imgSize[0], imgSize[1])

#Desenha uma imagem sem usar o buffer Vg (Virtual graphics)
def OpScrDrawImageByObjectIndex(ObjectIndex: list, point: tuple):
    VgObject = [ObjectIndex, 0, point]
    OpScrDrawImageInPosition(VgObject)

#Limpa a tela e preenche com a cor preta.
def OpScrClearScreen():
    pyxel.cls(0)

#endregion

#Flags globais de Vida, Score e tamanho de sprites
GL_FLAG_SPRITE_SIZE: tuple      = VgSetSize(16, 16)
GL_FLAG_MAP_SPRITE_SIZE: tuple  = VgSetSize(4, 4)
GL_FLAG_SCORE: int              = 0
GL_FLAG_LIFES: int              = 3

#Flags globais de vetor profundidade
GL_DEFAULT_MAP_Z    = 0
GL_DEFAULT_FOOD_Z   = 1
GL_DEFAULT_GHOST_Z  = 2
GL_DEFAULT_PACMAN_Z = 3

#Correção do comprimento de tela
GL_SCR_WIDTH   = 255 - 1
GL_SCR_HEIGHT  = 255 - 1

#Global Map Coordinates
GL_MAP_WALLS : list = [ [(14, 0), (GL_SCR_WIDTH - 14, 2)], 
                        [(14, 0), (14 + 2, GL_SCR_HEIGHT - 20)], 
                        [(33, 19), (33 + 25, 19 + 20)],
                        [(75, 19), (75 + 35, 19 + 20)], 
                        [(127, 0), (127 + 3, 39)], 
                        [(147, 19), (147 + 35, 19 + 20)],
                        [(199, 19), (199 + 25, 19 + 20)], 
                        [(241, 0), (241 + 2, GL_SCR_HEIGHT - 20)], 
                        [(33, 56), (33 + 25, 56 + 10)],
                        [(75, 56), (75 + 2, 56 + 60)], 
                        [(94, 56), (163, 56 + 10)], 
                        [(180, 56), (180 + 2, 56 + 60)],
                        [(199, 56), (199 + 25, 56 + 10)], 
                        [(77, 83), (110, 66 + 19)], 
                        [(127, 66), (130, 66 + 19)],
                        [(147, 83), (180, 66 + 19)], 
                        [(94, 102), (163, 160)], 
                        [(75, 133), (75 + 2, 179)],
                        [(180, 133), (180 + 2, 179)], 
                        [(94, 177), (163, 179)], 
                        [(33, 66 + 17), (33 + 25, 116)],
                        [(199, 66 + 17), (199 + 25, 116)], 
                        [(33, 116 + 17), (33 + 25, 179)], 
                        [(199, 116 + 17), (199 + 25, 179)],
                        [(33, 179 + 17), (33 + 25, GL_SCR_HEIGHT - 39)], 
                        [(75, 179 + 17), (182, GL_SCR_HEIGHT - 39)], 
                        [(199, 179 + 17), (199 + 25, GL_SCR_HEIGHT - 39)],
                        [(14, GL_SCR_HEIGHT - 22), (GL_SCR_WIDTH - 14, GL_SCR_HEIGHT - 20)]]

class Pacman:

    def __init__(self, initPos: tuple, initVel: int = 1, direction: PACMAN_DIRECTION = PACMAN_DIRECTION.LEFT):
        self.velocity: int = initVel
        self._direction: PACMAN_DIRECTION = direction
        self.position: tuple = initPos
        self.moving: bool = False
        self.SpriteId()
        self.SpritePos()

    def Move(self):
        if (self._direction == PACMAN_DIRECTION.LEFT):
            #Verificar por colisão, inserir as duas linhas debaixo em um if posteriormente.
            if (self.Collide((self.position[0] - self.velocity, self.position[1])) == False):
                self.Position((self.position[0] - self.velocity, self.position[1]))
                self.moving = True
        elif (self._direction == PACMAN_DIRECTION.RIGHT):
            if (self.Collide((self.position[0] + self.velocity, self.position[1])) == False):
                self.Position((self.position[0] + self.velocity, self.position[1]))
                self.moving = True
        elif (self._direction == PACMAN_DIRECTION.DOWN):
            if (self.Collide((self.position[0], self.position[1] + self.velocity)) == False):
                self.Position((self.position[0], self.position[1] + self.velocity))
                self.moving = True
        elif (self._direction == PACMAN_DIRECTION.UP):
            if (self.Collide((self.position[0], self.position[1] - self.velocity)) == False):
                self.Position((self.position[0], self.position[1] - self.velocity))
                self.moving = True
    
    def Position(self, newPosition: tuple = None):
        if (newPosition != None):
            self.position = newPosition
            return self.position
        else:
            return self.position
    
    def Direction(self, newDirection: PACMAN_DIRECTION = None):
        if (newDirection != None):
            if (newDirection == PACMAN_DIRECTION.LEFT):
                if (self.Collide((self.position[0] - self.velocity, self.position[1])) == False):
                    self._direction = newDirection
            elif (newDirection == PACMAN_DIRECTION.RIGHT):
                if (self.Collide((self.position[0] + self.velocity, self.position[1])) == False):
                    self._direction = newDirection
            elif (newDirection == PACMAN_DIRECTION.DOWN):
                if (self.Collide((self.position[0], self.position[1] + self.velocity)) == False):
                    self._direction = newDirection
            elif (newDirection == PACMAN_DIRECTION.UP):
                if (self.Collide((self.position[0], self.position[1] - self.velocity)) == False):
                    self._direction = newDirection
            return self._direction
        else:
            return self._direction

    def Velocity(self, newVelocity: int = None):
        if (newVelocity != None):
            self.velocity = newVelocity
            return self.velocity
        else:
            return self.velocity
    
    def SpritePos(self):
        if (self.Direction() == PACMAN_DIRECTION.LEFT):
            if (self.moving == True):
                self.moving = False
                if (pyxel.frame_count % 6 == 0 or pyxel.frame_count % 6 == 1):
                    return PACMAN_SPRITES_POS.PACMAN_CLOSED
                else:
                    return PACMAN_SPRITES_POS.PACMAN_OPEN_LEFT
            else:
                return PACMAN_SPRITES_POS.PACMAN_OPEN_LEFT

        elif (self.Direction() == PACMAN_DIRECTION.RIGHT):
            if (self.moving == True):
                self.moving = False
                if (pyxel.frame_count % 6 == 0 or pyxel.frame_count % 6 == 1):
                    return PACMAN_SPRITES_POS.PACMAN_CLOSED
                else:
                    return PACMAN_SPRITES_POS.PACMAN_OPEN_RIGHT
            else:
                return PACMAN_SPRITES_POS.PACMAN_OPEN_RIGHT

        elif (self.Direction() == PACMAN_DIRECTION.DOWN):
            if (self.moving == True):
                self.moving = False
                if (pyxel.frame_count % 6 == 0 or pyxel.frame_count % 6 == 1):
                    return PACMAN_SPRITES_POS.PACMAN_CLOSED
                else:
                    return PACMAN_SPRITES_POS.PACMAN_OPEN_DOWN
            else:
                return PACMAN_SPRITES_POS.PACMAN_OPEN_DOWN

        elif (self.Direction() == PACMAN_DIRECTION.UP):
            if (self.moving == True):
                self.moving = False
                if (pyxel.frame_count % 6 == 0 or pyxel.frame_count % 6 == 1):
                    return PACMAN_SPRITES_POS.PACMAN_CLOSED
                else:
                    return PACMAN_SPRITES_POS.PACMAN_OPEN_UP
            else:
                return PACMAN_SPRITES_POS.PACMAN_OPEN_UP

    def SpriteId(self):
        spritePos = self.SpritePos()
        if (spritePos == PACMAN_SPRITES_POS.PACMAN_CLOSED):
            return PACMAN_SPRITES_ID.PACMAN_CLOSED

        elif (spritePos == PACMAN_SPRITES_POS.PACMAN_OPEN_LEFT):
            return PACMAN_SPRITES_ID.PACMAN_OPEN_LEFT

        elif (spritePos == PACMAN_SPRITES_POS.PACMAN_OPEN_RIGHT):
            return PACMAN_SPRITES_ID.PACMAN_OPEN_RIGHT

        elif (spritePos == PACMAN_SPRITES_POS.PACMAN_OPEN_DOWN):
            return PACMAN_SPRITES_ID.PACMAN_OPEN_DOWN

        elif (spritePos == PACMAN_SPRITES_POS.PACMAN_OPEN_UP):
            return PACMAN_SPRITES_ID.PACMAN_OPEN_UP
    
    def Collide(self, nextPos: tuple):
        bCollide : bool = False
        for k in range(len(GL_MAP_WALLS)):
            map_wall = GL_MAP_WALLS[k]
            if (self.MatchPos(map_wall[0], map_wall[1], nextPos) == True):
                bCollide = True
                break
        return bCollide
    
    def MatchPos(self, startPos: tuple, endPos: tuple, nextPos: tuple):
        pacPosS = nextPos
        pacPosE = VgSetPoint(pacPosS[0] + 15, pacPosS[1] + 15)
        wallSzX : int = (endPos[0] - startPos[0]) + 0
        wallSzY : int = (endPos[1] - startPos[1]) + 0
        bCond1 : bool = (pacPosE[0] >= startPos[0] >= pacPosS[0] and pacPosE[1] >= startPos[1] >= pacPosS[1]) 
        bCond2 : bool = (pacPosE[0] >= endPos[0] >= pacPosS[0] and pacPosE[1] >= endPos[1] >= pacPosS[1])
        bCond3 : bool = (pacPosE[0] >= startPos[0] + wallSzX >= pacPosS[0] and pacPosE[1] >= startPos[1] >= pacPosS[1])
        bCond4 : bool = (pacPosE[0] >= startPos[0] >= pacPosS[0] and pacPosE[1] >= startPos[1] + wallSzY >= pacPosS[1])
        bCond5 : bool = (endPos[0] >= pacPosS[0] >= startPos[0] and endPos[1] >= pacPosS[1] >= startPos[1])
        bCond6 : bool = (endPos[0] >= pacPosE[0] >= startPos[0] and endPos[1] >= pacPosE[1] >= startPos[1])
        bCond7 : bool = (endPos[0] >= pacPosS[0] + 15 >= startPos[0] and endPos[1] >= pacPosS[1] >= startPos[1])
        bCond8 : bool = (endPos[0] >= pacPosS[0] >= startPos[0] and endPos[1] >= pacPosS[1] + 15 >= startPos[1])
        return (bCond1 or bCond2 or bCond3 or bCond4 or bCond5 or bCond6 or bCond7 or bCond8)
    
    def CheckForEat(self, pVgFoodBuffer: list):
        pacPos: tuple = VgSetPoint(self.Position()[0] + 7.5, self.Position()[1] + 7.5)
        for k in range(len(pVgFoodBuffer)):
            if (k <= len(pVgFoodBuffer) - 1):
                dx: int = abs(pacPos[0] - (pVgFoodBuffer[k][2][0] + 7.5))
                dy: int = abs(pacPos[1] - (pVgFoodBuffer[k][2][1] + 7.5))
                drel: float = abs((dx**2 + dy**2)**1/2)
                if (drel <= 20):
                    global GL_FLAG_SCORE
                    if (pVgFoodBuffer[k][0][2] == PACMAN_SPRITES_ID.WHITE_FOOD):
                        pVgFoodBuffer.remove(pVgFoodBuffer[k])
                        GL_FLAG_SCORE += 10
                        break
                    if (pVgFoodBuffer[k][0][2] == PACMAN_SPRITES_ID.BIG_WHITE_FOOD):
                        pVgFoodBuffer.remove(pVgFoodBuffer[k])
                        GL_FLAG_SCORE += 200
                        break
                    print("s")

class MainWindow:

    def __init__(self, wndSize):
        self.gamestate: GAME_STATE = GAME_STATE.READY
        self.vgBuffer = VgQueueCreateBuffer()
        self.vgFoodBuffer = VgQueueCreateBuffer()
        self.foodLoaded: bool = False
        self.pacmanObj = None
        pyxel.init(wndSize[0], wndSize[1], fps=40)
        pyxel.mouse(True)
        pyxel.load("C:\\Users\\Murilo\\Desktop\\ZwQuerySystemInformation\\UPE Homework\\Programação 1\\Pacman\\pacman.pyxel")
        pyxel.run(self.UpdateCallback, self.DrawCallback)
    
    #Atualizando as posições e a dinâmica do jogo. Este método é IMUTÁVEL.
    def UpdateCallback(self):
        #Chama a sub-rotina de preprocessamento de tecla
        if (self.gamestate == GAME_STATE.RUNNING):
            self.BeforeKeyProcessed()
        #Chama a rotina de processamento de tecla
        if (pyxel.btn(pyxel.KEY_LEFT)):
            self.KeyPressed(pyxel.KEY_LEFT)
        elif (pyxel.btn(pyxel.KEY_RIGHT)):
            self.KeyPressed(pyxel.KEY_RIGHT)
        elif (pyxel.btn(pyxel.KEY_DOWN)):
            self.KeyPressed(pyxel.KEY_DOWN)
        elif (pyxel.btn(pyxel.KEY_UP)):
            self.KeyPressed(pyxel.KEY_UP)
        elif (pyxel.btnp(pyxel.KEY_P)):
            self.KeyPressed(pyxel.KEY_P)
        elif (pyxel.btnp(pyxel.KEY_SPACE)):
            self.KeyPressed(pyxel.KEY_SPACE)
        #Chama a sub-rotina de pós processamento de tecla
        if (self.gamestate == GAME_STATE.RUNNING):
            self.AfterKeyProcessed()

    #Desenhando na tela. Este método é IMUTÁVEL.
    def DrawCallback(self):
        if (self.gamestate == GAME_STATE.RUNNING):
            OpScrClearScreen()
            self.LoadMap()
            vgCount: int = len(self.vgBuffer)
            nextVgObj = VgQueueNextObjectToDraw(self.vgBuffer)
            while (nextVgObj != None):
                OpScrDrawImageInPosition(nextVgObj)
                nextVgObj = VgQueueNextObjectToDraw(self.vgBuffer)
            #Escreve o Score e a quantidade de vidas na tela
            OpScrWriteTextInPosition("Score:", VgSetPoint(10, pyxel.height - 10), 7)
            OpScrWriteTextInPosition(str(GL_FLAG_SCORE), VgSetPoint(40, pyxel.height - 10), 3)
            OpScrWriteTextInPosition("Vidas:", VgSetPoint(70, pyxel.height - 10), 7)
            OpScrWriteTextInPosition(str(GL_FLAG_LIFES), VgSetPoint(100, pyxel.height - 10), 3)
            #Escreve algumas informações básicas de depuração na tela
            
            OpScrWriteTextInPosition("Frame: " + str(pyxel.frame_count), VgSetPoint(150, pyxel.height - 18), 2)
            OpScrWriteTextInPosition("Objetos desenhados: " + str(vgCount), VgSetPoint(150, pyxel.height - 10), 2)
        elif (self.gamestate == GAME_STATE.READY):
            #Tela inicial do jogo
            OpScrClearScreen()
            vgObjLogo = VgAcquireObjectIndex(PACMAN_SPRITES_POS.PACMAN_LOGO, PACMAN_SPRITES_ID.PACMAN_LOGO, 1, VgSetSize(253, 51))
            OpScrDrawImageByObjectIndex(vgObjLogo, VgSetPoint(0, 50))
            OpScrWriteTextInPosition("PRESSIONE ESPACO PARA INICIAR O JOGO", VgSetPoint(pyxel.width / 2 - pyxel.width / 4 - 10, pyxel.height / 2), pyxel.frame_count % 16)
        elif (self.gamestate == GAME_STATE.PAUSED):
            OpScrClearScreen()
            vgObjLogo = VgAcquireObjectIndex(PACMAN_SPRITES_POS.PACMAN_LOGO, PACMAN_SPRITES_ID.PACMAN_LOGO, 1, VgSetSize(253, 51))
            OpScrDrawImageByObjectIndex(vgObjLogo, VgSetPoint(0, 50))
            OpScrWriteTextInPosition("PRESSIONE \"P\" PARA CONTINUAR O JOGO", VgSetPoint(pyxel.width / 2 - pyxel.width / 4 - 10, pyxel.height / 2), pyxel.frame_count % 16)



    #Antes de processar as teclas
    def BeforeKeyProcessed(self):
        if (self.gamestate == GAME_STATE.RUNNING):
            #parei aqui na animação do pacman
            if (self.pacmanObj == None):
                self.pacmanObj = Pacman(VgSetPoint(121, 40), 1, PACMAN_DIRECTION.LEFT)

            #objetoFantasma = VgAcquireObjectIndex(PACMAN_SPRITES_POS.GHOST_BLUE_UP, PACMAN_SPRITES_ID.GHOST_BLUE_UP, 0, GL_FLAG_SPRITE_SIZE, 0)
            #VgQueueAddObjectToDraw(self.vgBuffer, objetoFantasma, 0, VgSetPoint(200, 50))


    #Depois de processar as teclas
    def AfterKeyProcessed(self):
        #parei aqui também
        if (self.pacmanObj != None):
            self.pacmanObj.Move()
            self.pacmanObj.CheckForEat(self.vgFoodBuffer)
            objIndex = VgAcquireObjectIndex(self.pacmanObj.SpritePos(), self.pacmanObj.SpriteId(), 0, GL_FLAG_SPRITE_SIZE, 0)
            VgQueueAddObjectToDraw(self.vgBuffer, objIndex, GL_DEFAULT_PACMAN_Z, VgSetPoint(self.pacmanObj.Position()[0], self.pacmanObj.Position()[1]))

    #Processando as teclas
    def KeyPressed(self, keyId):
        if (keyId == pyxel.KEY_SPACE):
            if (self.gamestate == GAME_STATE.READY):
                self.gamestate = GAME_STATE.RUNNING
        elif (keyId == pyxel.KEY_P):
            if (self.gamestate == GAME_STATE.RUNNING):
                self.gamestate = GAME_STATE.PAUSED
            elif (self.gamestate == GAME_STATE.PAUSED):
                self.gamestate = GAME_STATE.RUNNING

        #Direcionamento do Pacman usando as setas do teclado
        if (self.pacmanObj != None):
            if (keyId == pyxel.KEY_LEFT):
                self.pacmanObj.Direction(PACMAN_DIRECTION.LEFT)
            elif (keyId == pyxel.KEY_RIGHT):
                self.pacmanObj.Direction(PACMAN_DIRECTION.RIGHT)
            elif (keyId == pyxel.KEY_UP):
                self.pacmanObj.Direction(PACMAN_DIRECTION.UP)
            elif (keyId == pyxel.KEY_DOWN):
                self.pacmanObj.Direction(PACMAN_DIRECTION.DOWN)

    #Carrega o mapa no frame atual
    def LoadMap(self):
        SCR_WIDTH   = pyxel.width - 1
        SCR_HEIGHT  = pyxel.height - 1
        COLOR_WALL  = 13
        #Margem superior
        pyxel.rect(14, 0, SCR_WIDTH - 14, 2, COLOR_WALL)
        #Margem lateral esquerda
        pyxel.rect(14, 0, 14 + 2, SCR_HEIGHT - 20, COLOR_WALL)
        #Bloco 1
        pyxel.rect(33, 19, 33 + 25, 19 + 20, COLOR_WALL)
        #Bloco 2
        pyxel.rect(75, 19, 75 + 35, 19 + 20, COLOR_WALL)
        #Divisória central superior
        pyxel.rect(127, 0, 127 + 3, 39, COLOR_WALL)
        #Bloco 3
        pyxel.rect(147, 19, 147 + 35, 19 + 20, COLOR_WALL)
        #Bloco 4
        pyxel.rect(199, 19, 199 + 25, 19 + 20, COLOR_WALL)
        #Margem lateral direita
        pyxel.rect(241, 0, 241 + 2, SCR_HEIGHT - 20, COLOR_WALL)
        #Bloco 5
        pyxel.rect(33, 56, 33 + 25, 56 + 10, COLOR_WALL)
        #Bloco 6
        pyxel.rect(75, 56, 75 + 2, 56 + 60, COLOR_WALL)
        #Bloco 7
        pyxel.rect(94, 56, 163, 56 + 10, COLOR_WALL)
        #Bloco 8
        pyxel.rect(180, 56, 180 + 2, 56 + 60, COLOR_WALL)
        #Bloco 9
        pyxel.rect(199, 56, 199 + 25, 56 + 10, COLOR_WALL)
        #Divisoria horizontal do bloco 6
        pyxel.rect(77, 83, 110, 66 + 19, COLOR_WALL)
        #Divisoria vertical do bloco 7
        pyxel.rect(127, 66, 130, 66 + 19, COLOR_WALL)
        #Divisoria horizontal do bloco 8
        pyxel.rect(147, 83, 180, 66 + 19, COLOR_WALL)
        #Buraco do centro
        pyxel.rectb(94, 102, 163, 160, COLOR_WALL)
        pyxel.rect(75, 133, 75 + 2, 179, COLOR_WALL)
        pyxel.rect(180, 133, 180 + 2, 179, COLOR_WALL)
        pyxel.rect(94, 177, 163, 179, COLOR_WALL)
        pyxel.rect(33, 66 + 17, 33 + 25, 116, COLOR_WALL)
        pyxel.rect(199, 66 + 17, 199 + 25, 116, COLOR_WALL)
        pyxel.rect(33, 116 + 17, 33 + 25, 179, COLOR_WALL)
        pyxel.rect(199, 116 + 17, 199 + 25, 179, COLOR_WALL)
        pyxel.rect(33, 179 + 17, 33 + 25, SCR_HEIGHT - 39, COLOR_WALL)
        pyxel.rect(75, 179 + 17, 182, SCR_HEIGHT - 39, COLOR_WALL)
        pyxel.rect(199, 179 + 17, 199 + 25, SCR_HEIGHT - 39, COLOR_WALL)
        pyxel.rect(14, SCR_HEIGHT - 22, SCR_WIDTH - 14, SCR_HEIGHT - 20, COLOR_WALL)
        if (self.foodLoaded == False):
            self.foodLoaded = True
            self.CreateFood(VgSetPoint(17, 5), 0, 10, 22)
            self.CreateFood(VgSetPoint(59, 5), 0, 10, 22)
            self.CreateFood(VgSetPoint(183, 5), 0, 10, 22)
            self.CreateFood(VgSetPoint(225, 5), 0, 10, 22)
            self.CreateFood(VgSetPoint(28, 40), 10, 0, 3)
            self.CreateFood(VgSetPoint(71, 40), 10, 0, 11)
            self.CreateFood(VgSetPoint(194, 40), 10, 0, 3)
            self.CreateFood(VgSetPoint(28, 67), 10, 0, 3)
            self.CreateFood(VgSetPoint(28, 117), 10, 0, 3)
            self.CreateFood(VgSetPoint(28, 180), 10, 0, 3)
            self.CreateFood(VgSetPoint(28, 216), 10, 0, 3)
            self.CreateFood(VgSetPoint(71, 180), 10, 0, 11)
            self.CreateFood(VgSetPoint(194, 180), 10, 0, 3)
            self.CreateFood(VgSetPoint(71, 216), 10, 0, 11)
            self.CreateFood(VgSetPoint(194, 216), 10, 0, 3)
            self.CreateFood(VgSetPoint(28, 4), 10, 0, 3)
            self.CreateFood(VgSetPoint(194, 67), 10, 0, 3)
            self.CreateFood(VgSetPoint(194, 117), 10, 0, 3)
            self.CreateFood(VgSetPoint(194, 4), 10, 0, 3)
            self.CreateFood(VgSetPoint(71, 4), 10, 0, 5)
            self.CreateFood(VgSetPoint(131, 4), 10, 0, 5)
            self.CreateFood(VgSetPoint(111, 17), 0, 10, 2)
            self.CreateFood(VgSetPoint(131, 17), 0, 10, 2)
            self.CreateBigFood(VgSetPoint(78, 87))
            self.CreateBigFood(VgSetPoint(164, 87))
            self.CreateBigFood(VgSetPoint(78, 162))
            self.CreateBigFood(VgSetPoint(164, 162))
            self.CreateFood(VgSetPoint(91, 87), 10, 0, 7)
            self.CreateFood(VgSetPoint(91, 162), 10, 0, 7)
            self.CreateFood(VgSetPoint(78, 100), 0, 10, 6)
            self.CreateFood(VgSetPoint(164, 100), 0, 10, 6)
            self.CreateFood(VgSetPoint(69, 117), 0, 0, 1)
            self.CreateFood(VgSetPoint(173, 117), 0, 0, 1)
            self.CreateFood(VgSetPoint(78, 50), 0, 10, 2)
            self.CreateFood(VgSetPoint(78, 69), 10, 0, 4)
            self.CreateFood(VgSetPoint(134, 69), 10, 0, 4)
            self.CreateFood(VgSetPoint(164, 50), 0, 10, 2)
            self.CreateFood(VgSetPoint(111, 78), 0, 10, 1)
            self.CreateFood(VgSetPoint(131, 78), 0, 10, 1)
            self.CreateFood(VgSetPoint(78, 172), 0, 10, 1)
            self.CreateFood(VgSetPoint(164, 172), 0, 10, 1)
        VgQueueCopyBuffer(self.vgBuffer, self.vgFoodBuffer)

    def CreateFood(self, point1, xspacing, yspacing, foodCount = 20):
        xInc = 0
        yInc = 0
        foodObjIndex = VgAcquireObjectIndex(PACMAN_SPRITES_POS.WHITE_FOOD, PACMAN_SPRITES_ID.WHITE_FOOD, 0, GL_FLAG_SPRITE_SIZE, 0)
        for k in range(foodCount):
            VgQueueAddObjectToDraw(self.vgFoodBuffer, foodObjIndex, GL_DEFAULT_FOOD_Z, VgSetPoint(point1[0] + xInc, point1[1] + yInc))
            xInc += xspacing
            yInc += yspacing

    def CreateBigFood(self, point):
        objIndex = VgAcquireObjectIndex(PACMAN_SPRITES_POS.BIG_WHITE_FOOD, PACMAN_SPRITES_ID.BIG_WHITE_FOOD, 0, GL_FLAG_SPRITE_SIZE, 0)
        VgQueueAddObjectToDraw(self.vgFoodBuffer, objIndex, GL_DEFAULT_FOOD_Z, point)

#Inicia o jogo com as dimensões a serem definidas:
if (__name__ == "__main__"):
    MainWindow((255, 255))