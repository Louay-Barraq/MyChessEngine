class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False


    def makeMove(self, move):
        # Making changes on the board
        self.board[move.startingRow][move.startingColumn] = "--"
        self.board[move.endingRow][move.endingColumn] = move.movedPiece
        # Making changes to the king's location if it is the moved piece
        if move.movedPiece == "wK":
            self.whiteKingLocation = (move.endingRow, move.endingColumn)
        elif move.movedPiece == "bK":
            self.blackKingLocation = (move.endingRow, move.endingColumn)
        # Logging the move
        self.moveLog.append(move)
        # Swapping between players
        self.whiteToMove = not self.whiteToMove


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            # Reverting back pieces
            self.board[move.startingRow][move.startingColumn] = move.movedPiece
            self.board[move.endingRow][move.endingColumn] = move.capturedPiece
            # Pass
            if move.movedPiece == "wK":
                self.whiteKingLocation = (move.startingRow, move.startingColumn)
            elif move.movedPiece == "bK":
                self.blackKingLocation = (move.startingRow, move.startingColumn)
            # Swapping back turns
            self.whiteToMove = not self.whiteToMove


    # Getting all the valid moves considering checks
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # makeMove switches turns, so we have to switch them back to see if that move made the king vulnerable
            self.whiteToMove = not self.whiteToMove
            if self.isInCheck():
                moves.remove(moves[i])
            # Reverting back into the initial conditions
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        # Checking for the edge cases (Checkmate or Stalemate)
        if len(moves) == 0:
            if self.isInCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate, self.stalemate = False, False

        return moves

    # Checking if player's king is in a check state
    def isInCheck(self):
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation[0], self.whiteKingLocation[1]
        else:
            kingRow, kingCol = self.blackKingLocation[0], self.blackKingLocation[1]

        return self.isUnderAttack(kingRow, kingCol)


    # Checking if the square (row, col) is under attack by any of the opponent's pieces
    def isUnderAttack(self, row, col) -> bool:
        # Switching to the opponent
        self.whiteToMove = not self.whiteToMove
        # Generating all his possible moves
        opponentMoves = self.getAllPossibleMoves()
        # Before checking, the player's turn should be reverted back
        self.whiteToMove = not self.whiteToMove
        for move in opponentMoves:
            if (move.endingRow == row) and (move.endingColumn == col):
                return True

        return False


    # Getting all the possible moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # Checking whoever turn it is
                colorMove = self.board[r][c][0]
                if (colorMove == 'w' and self.whiteToMove) or (colorMove == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # Getting all the possible moves of the corresponding piece
                    self.moveFunctions[piece](r, c, moves)
        return moves


    # Getting all the possible moves for a pawn
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--": # Advancing one square
                moves.append(Move((r, c), (r - 1, c), self.board))
                if (r == 6) and (self.board[r - 2][c] == "--"): # Advancing two squares
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if (c - 1) >= 0: # Capturing to the left
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if (c + 1) <= 7: # Capturing to the right
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--": # Advancing one square
                moves.append(Move((r, c), (r + 1, c), self.board))
                if (r == 1) and (self.board[r + 2][c] == "--"): # Advancing two squares
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if (c - 1) >= 0: # Capturing to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if (c + 1) <= 7: # Capturing to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    # Getting all the possible moves for a rook
    def getRookMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'

        # Check moves to the right
        col_idx = c + 1
        while col_idx <= 7:
            if self.board[r][col_idx] == "--":
                moves.append(Move((r, c), (r, col_idx), self.board))
                col_idx += 1
            elif self.board[r][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (r, col_idx), self.board))
                break
            else:
                break

        # Check moves to the left
        col_idx = c - 1
        while col_idx >= 0:
            if self.board[r][col_idx] == "--":
                moves.append(Move((r, c), (r, col_idx), self.board))
                col_idx -= 1
            elif self.board[r][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (r, col_idx), self.board))
                break
            else:
                break

        # Check moves upwards
        row_idx = r - 1
        while row_idx >= 0:
            if self.board[row_idx][c] == "--":
                moves.append(Move((r, c), (row_idx, c), self.board))
                row_idx -= 1
            elif self.board[row_idx][c][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, c), self.board))
                break
            else:
                break

        # Check moves downwards
        row_idx = r + 1
        while row_idx <= 7:
            if self.board[row_idx][c] == "--":
                moves.append(Move((r, c), (row_idx, c), self.board))
                row_idx += 1
            elif self.board[row_idx][c][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, c), self.board))
                break
            else:
                break


    # Getting all the possible moves for a bishop
    def getBishopMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'

        # Checking for moves : Up - Right
        row_idx, col_idx = r - 1, c + 1
        while (row_idx >= 0) and (col_idx <= 7):
            if self.board[row_idx][col_idx] == "--":
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                row_idx, col_idx = row_idx - 1, col_idx + 1
            elif self.board[row_idx][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                break
            else:
                break

        # Checking for moves : Up - Left
        row_idx, col_idx = r - 1, c - 1
        while (row_idx >= 0) and (col_idx >= 0):
            if self.board[row_idx][col_idx] == "--":
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                row_idx, col_idx = row_idx - 1, col_idx - 1
            elif self.board[row_idx][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                break
            else:
                break

        # Checking for moves : Down - Right
        row_idx, col_idx = r + 1, c + 1
        while (row_idx <= 7) and (col_idx <= 7):
            if self.board[row_idx][col_idx] == "--":
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                row_idx, col_idx = row_idx + 1, col_idx + 1
            elif self.board[row_idx][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                break
            else:
                break

        # Checking for moves : Down - Left
        row_idx, col_idx = r + 1, c - 1
        while (row_idx <= 7) and (col_idx >= 0):
            if self.board[row_idx][col_idx] == "--":
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                row_idx, col_idx = row_idx + 1, col_idx - 1
            elif self.board[row_idx][col_idx][0] == enemyColor:
                moves.append(Move((r, c), (row_idx, col_idx), self.board))
                break
            else:
                break


    # Getting all the possible moves for a knight
    def getKnightMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        knightMoves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for knightMove in knightMoves:
            row_idx, col_idx = r + knightMove[0], c + knightMove[1]
            if (0 <= row_idx <= 7) and (0 <= col_idx <= 7):
                if self.board[row_idx][col_idx] == "--":
                    moves.append(Move((r, c), (row_idx, col_idx), self.board))
                elif self.board[row_idx][col_idx][0] == enemyColor:
                    moves.append(Move((r, c), (row_idx, col_idx), self.board))


    # Getting all the possible moves for a king
    def getKingMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for kingMove in kingMoves:
            row_idx, col_idx = r + kingMove[0], c + kingMove[1]
            if (0 <= row_idx <= 7) and (0 <= col_idx <= 7):
                if self.board[row_idx][col_idx] == "--":
                    moves.append(Move((r, c), (row_idx, col_idx), self.board))
                elif self.board[row_idx][col_idx][0] == enemyColor:
                    moves.append(Move((r, c), (row_idx, col_idx), self.board))


    # Getting all the possible moves for a queen
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startingSquare, endingSquare, board):
        self.startingRow = startingSquare[0]
        self.startingColumn = startingSquare[1]
        self.endingRow = endingSquare[0]
        self.endingColumn = endingSquare[1]
        self.movedPiece = board[self.startingRow][self.startingColumn]
        self.capturedPiece = board[self.endingRow][self.endingColumn]
        # Attributes related to pawns
        # self.isPawnPromotion = (self.movedPiece == 'wp' and self.endingRow == 0) or (self.movedPiece == 'bp' and self.endingRow == 7)
        # self.isEnPassantMove = (self.movedPiece[1] == 'p')
        # Generating a unique ID for the move using a hashing function
        self.moveID = (self.startingRow * 1000) + (self.startingColumn * 100) + (self.endingRow * 10) + self.endingColumn

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True
        return False


    def __str__(self):
        return f"Move : from {self.getRankFile(self.startingRow, self.startingColumn)} to {self.getRankFile(self.endingRow, self.endingColumn)}"


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]


    def getChessNotation(self):
        # Handling the pawn's moves
        if self.movedPiece[1] == 'p':
            if self.capturedPiece != '--':  # If the pawn captures a piece
                return self.getRankFile(self.endingRow, self.endingColumn)
            else:  # If the pawn captures a piece
                return self.colsToFiles[self.startingColumn] + 'x' + self.getRankFile(self.endingRow, self.endingColumn)

        # Handling other pieces' moves
        piece = self.movedPiece[1]
        if self.capturedPiece != '--':
            return piece + 'x' + self.getRankFile(self.endingRow, self.endingColumn)
        else:
            return piece + self.getRankFile(self.endingRow, self.endingColumn)
