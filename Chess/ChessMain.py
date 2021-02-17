import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wR', 'wB', 'wQ', 'wK', 'wN', 'bR', 'bB', 'bP', 'bQ', 'bK', 'bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Chess/images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True

    selectedSq = ()
    clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selectedSq == (row, col):
                    selectedSq = ()
                    clicks = []
                else:
                    selectedSq = (row, col)
                    clicks.append(selectedSq)

                if len(clicks) == 2:
                    move = ChessEngine.Move(clicks[0], clicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    selectedSq = ()
                    clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gs)


def drawGameState(screen, gs):
    drawBoard(screen) # Draws squares
    drawPieces(screen, gs.board) # Draws pieces on squares

def drawBoard(screen):
    colors = [(235, 235, 208), (119, 148, 85)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                image = IMAGES[piece]
                screen.blit(image, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
