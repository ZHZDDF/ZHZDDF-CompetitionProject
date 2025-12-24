import random
import numpy as np

# 常量定义
Red = 1
Blue = -1
MC_CONSTANT = 1000

# 位置类
class Loc:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def set(self, a, b):
        self.x = a
        self.y = b

# 移动棋子类
class MovePiece:
    def __init__(self, loc=None, piece=0, direction=0):
        self.loc = loc if loc else Loc()
        self.piece = piece
        self.dir = direction

# 随机骰子函数
def rand_dice():
    return random.randint(1, 6)

# 棋盘类
class Board:
    def __init__(self, arr):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                self.board[i][j] = arr[i][j]
        
        self.red = [0] * 7
        self.blue = [0] * 7
        
        self.red[0] = 0
        self.blue[0] = 0
        for i in range(5):
            for j in range(5):
                if arr[i][j] > 0:
                    self.red[0] += 1
                    self.red[arr[i][j]] = 1
                elif arr[i][j] < 0:
                    self.blue[0] += 1
                    self.blue[-arr[i][j]] = 1
    
    def winner(self):
        if self.blue[0] == 0 or self.board[4][4] > 0:
            return 1  # red win
        elif self.red[0] == 0 or self.board[0][0] < 0:
            return -1  # blue win
        else:
            return 0  # 无胜负
    
    def is_alive(self, piece):
        if piece > 0:
            return self.red[piece] == 1
        else:
            return self.blue[-piece] == 1
    
    def get_piece_legality(self, ploc):
        if 0 <= ploc.x < 5 and 0 <= ploc.y < 5:
            return True
        return False
    
    def get_piece(self, piece):
        loc = Loc()
        for i in range(5):
            for j in range(5):
                if piece == self.board[i][j]:
                    loc.set(i, j)
                    return loc
        return loc
    
    # 获取阵营
    def get_piece_faction(self, piece):
        if piece > 0:
            return 1  # 红方为1
        elif piece < 0:
            return -1  # 蓝方为-1
        else:
            return 0
    
    def get_larger_piece(self, piece):
        if piece > 0:
            for i in range(piece + 1, 7):
                if self.is_alive(i):
                    return i
        elif piece < 0:
            for i in range(piece - 1, -7, -1):
                if self.is_alive(i):
                    return i
        return 0
    
    def get_smaller_piece(self, piece):
        if piece > 0:
            for i in range(piece - 1, 0, -1):
                if self.is_alive(i):
                    return i
        elif piece < 0:
            for i in range(piece + 1, 0):
                if self.is_alive(i):
                    return i
        return 0
    
    def is_waning_zone(self, loc):
        f = self.get_piece_faction(self.board[loc.x][loc.y])
        if (f * loc.x >= 2 * f + 1) and (f * loc.y >= 2 * f + 1):  # 禁区公式
            return True
        else:
            return False
    
    def move(self, nloc, piece):
        oloc = self.get_piece(piece)
        f = self.board[nloc.x][nloc.y]
        if f > 0:
            self.red[0] -= 1
            self.red[f] = 0
        if f < 0:
            self.blue[0] -= 1
            self.blue[-f] = 0
        self.board[oloc.x][oloc.y] = 0
        self.board[nloc.x][nloc.y] = piece
    
    def get_all_moves(self, piece):
        moves = []
        direction = [(0, 1), (1, 0), (1, 1)]  # 0右 1下 2右下
        f = self.get_piece_faction(piece)  # 向量(棋子阵营)
        
        if self.is_alive(piece):
            ploc = self.get_piece(piece)
            if self.is_waning_zone(ploc):
                nloc = Loc(2 + 2 * f, 2 + 2 * f)
                temp_dir = 0
                if f > 0:
                    dx = 4 - ploc.x
                    dy = 4 - ploc.y
                    if dx == 0 and dy == 1:
                        temp_dir = 0  # 右
                    if dx == 1 and dy == 0:
                        temp_dir = 1  # 下
                    if dx == 1 and dy == 1:
                        temp_dir = 2  # 右下
                elif f < 0:
                    dx = ploc.x
                    dy = ploc.y
                    if dx == 0 and dy == 1:
                        temp_dir = 0  # 左
                    if dx == 1 and dy == 0:
                        temp_dir = 1  # 上
                    if dx == 1 and dy == 1:
                        temp_dir = 2  # 左上
                moves.append(MovePiece(nloc, piece, temp_dir))
                return moves
            
            for i in range(3):
                nloc = Loc(ploc.x + f * direction[i][0], ploc.y + f * direction[i][1])
                if self.get_piece_legality(nloc):
                    moves.append(MovePiece(nloc, piece, i))
        else:
            # 获取可移动的较大和较小棋子
            L = self.get_larger_piece(piece)
            S = self.get_smaller_piece(piece)
            
            if L != 0:
                ploc = self.get_piece(L)
                if self.is_waning_zone(ploc):
                    nloc = Loc(2 + 2 * f, 2 + 2 * f)
                    td2 = 0
                    if f > 0:
                        dx = 4 - ploc.x
                        dy = 4 - ploc.y
                        if dx == 0 and dy == 1:
                            td2 = 0  # 右
                        if dx == 1 and dy == 0:
                            td2 = 1  # 下
                        if dx == 1 and dy == 1:
                            td2 = 2  # 右下
                    elif f < 0:
                        dx = ploc.x
                        dy = ploc.y
                        if dx == 0 and dy == 1:
                            td2 = 0  # 左
                        if dx == 1 and dy == 0:
                            td2 = 1  # 上
                        if dx == 1 and dy == 1:
                            td2 = 2  # 左上
                    moves.append(MovePiece(nloc, L, td2))
                    return moves
                
                for i in range(3):
                    nloc = Loc(ploc.x + f * direction[i][0], ploc.y + f * direction[i][1])
                    if self.get_piece_legality(nloc):
                        moves.append(MovePiece(nloc, L, i))
            
            if S != 0:
                ploc = self.get_piece(S)
                if self.is_waning_zone(ploc):
                    nloc = Loc(2 + 2 * f, 2 + 2 * f)
                    td3 = 0
                    if f > 0:
                        dx = 4 - ploc.x
                        dy = 4 - ploc.y
                        if dx == 0 and dy == 1:
                            td3 = 0  # 右
                        if dx == 1 and dy == 0:
                            td3 = 1  # 下
                        if dx == 1 and dy == 1:
                            td3 = 2  # 右下
                    elif f < 0:
                        dx = ploc.x
                        dy = ploc.y
                        if dx == 0 and dy == 1:
                            td3 = 0  # 左
                        if dx == 1 and dy == 0:
                            td3 = 1  # 上
                        if dx == 1 and dy == 1:
                            td3 = 2  # 左上
                    moves.append(MovePiece(nloc, S, td3))
                    return moves
                
                for i in range(3):
                    nloc = Loc(ploc.x + f * direction[i][0], ploc.y + f * direction[i][1])
                    if self.get_piece_legality(nloc):
                        moves.append(MovePiece(nloc, S, i))
        
        return moves

# 随机走子
def rand_move(CB, piece):
    moves = CB.get_all_moves(piece)
    if moves:
        dice = random.randint(0, len(moves) - 1)
        CB.move(moves[dice].loc, moves[dice].piece)

# 模拟
def get_mc_winner(CB, next_player):
    NCB = Board([row[:] for row in CB.board])
    player = next_player
    while True:
        win = NCB.winner()
        if win != 0:
            return win
        player *= -1
        rand_move(NCB, player * rand_dice())

# 评估
def get_mc_evalution(CB, next_player, times):
    eva = 0
    for i in range(times):
        NCB = Board([row[:] for row in CB.board])
        if get_mc_winner(NCB, next_player) == -next_player:  # next_player输
            eva += 1
    result = eva / times
    return result

# 移子函数
def deal(CB, piece):
    """红正 蓝负   如果红色方 直接传骰子；  蓝色方 骰子*-1"""
    f = CB.get_piece_faction(piece)
    best_val = -1
    best_move = 0
    moves = CB.get_all_moves(piece)
    move_num = len(moves)
    
    for i in range(move_num):
        NCB = Board([row[:] for row in CB.board])
        NCB.move(moves[i].loc, moves[i].piece)
        val = get_mc_evalution(NCB, -f, MC_CONSTANT)
        
        if best_val < val:
            best_val = val
            best_move = i
    
    # print(moves[best_move].piece)  # 移动的棋子
    # print(moves[best_move].dir)  # 移动的方向 0右 1下 2右下
    if moves[best_move].piece > 0:
        if moves[best_move].dir == 0:
            print(moves[best_move].piece)
            print(1)
            print(0)
        elif moves[best_move].dir == 1:
            print(moves[best_move].piece)
            print(0)
            print(1)
        elif moves[best_move].dir == 2:
            print(moves[best_move].piece)
            print(1)
            print(1)
    else:
        if moves[best_move].dir == 0:
            print(moves[best_move].piece)
            print(-1)
            print(0)
        elif moves[best_move].dir == 1:
            print(moves[best_move].piece)
            print(0)
            print(-1)
        elif moves[best_move].dir == 2:
            print(moves[best_move].piece)
            print(-1)
            print(-1)
        
    # 返回最佳移动
    return moves[best_move]

import sys
import json
from pathlib import Path

def test():
	try:
		file_path=Path(sys.argv[1])
		with open(file_path,'r',encoding='utf-8') as f:
			data=json.load(f)
		print(data)
		#message={"who_is_me":自己为先手时为true，后手时为false,"table_message":5*5数组,"dice":骰子点数}
		if data["who_is_me"]:
			print("1")
			print("1")
			print("1")
		else:
			print("-1")
			print("-1")
			print("-1")
	finally:
		return 

#最后三行输出分别为
#:棋子(红的(先手)为1~6，蓝的(后手)为-1~-6)
#移动的X偏移，1为向右，-1向左，0不动
#移动的Y偏移，1为向下，-1向上，0不动
def main():
    # 初始化棋盘
    file_path=Path(sys.argv[1])
    with open(file_path,'r',encoding='utf-8') as f:
        data=json.load(f)
    arr = data["table_message"]
    dice = data["dice"]
    who_is_me = data["who_is_me"]
    test_move_num = dice if who_is_me else -1 * dice
    CB = Board(arr)  # 需要每次实例化一个   1
    
    best_move = deal(CB, test_move_num)  # deal
# def main():
    # arr = [
    #     [1, 0, 3, 0, 0],
    #     [4, 5, 0, 0, 0],
    #     [6, 0, 0, 0, -1],
    #     [0, 0, 0, 0, -3],
    #     [0, 0, -4, -5, -6]
    # ]
    # dice = 2
    # who_is_me = False
    # test_move_num = dice if who_is_me else -1 * dice
    # CB = Board(arr)  # 需要每次实例化一个   1
    
    # # 调用deal函数，例如蓝方第2个棋子
    # best_move = deal(CB, test_move_num)  # deal


if __name__ == "__main__":
    random.seed()
    main()