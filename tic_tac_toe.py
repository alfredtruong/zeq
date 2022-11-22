# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 21:48:46 2022

@author: ahkar
"""

########################################################
# imports
########################################################
from typing import Dict
import time # make cpu seem thoughtful
import random # make cpu seem thoughtful
from itertools import cycle # to zip lists of different lengths

########################################################
# TicTacToe class
########################################################
class TicTacToe:
    
    # class variables
    human_marker = 'x'
    cpu_marker   = 'o'
    empty_marker = ' '

    def __init__(self):
        # nothing to init here
        # I separate code into play_game() to make it easier to test
        pass

    def type_text(self, msg : str, await_key_press = False) -> None:
        '''
        make it seem like the cpu is typing text in real-time
        '''
        
        # choose a random talking speed
        text_speed = random.uniform(0.02, 0.08)
        
        # spit out 1 char at a time
        for char in msg:
            time.sleep(text_speed)
            print(char, end='', flush=True)
        
        # require prompt or not?
        if await_key_press:
            input()
        else:
            print('')

    def play_game(self) -> None:
        '''
        prep board
        prep cpu talking points
        play till end of game
        '''
        # init
        self.board = self.create_board() # set the board
        
        # randomise what the cpu will say and in what order
        l = list(range(10))
        random.shuffle(l) # can't shuffle a generator so shuffle a list
        self.speech_order = cycle(l) # make speak infinitely useable

        # chitchat
        self.type_text('Welcome weary traveller to `Maison du Tic Tac Toe` (hit enter)',True)
        self.type_text('I\'ve been waiting for you since time immemorial ... (hit enter)',True)
        self.type_text('Shall we jam? (hit enter)',True)
        self.type_text('I insist on the following position names ............ (hit enter)',False)
        print()
        self.show_board(show_location = True)
        input()
        self.type_text('You go first, it doesn\'t matter to me ......... I can\'t lose',False)

        # play until someone wins or until it's a draw
        turn_identifier = TicTacToe.human_marker # human goes first
        while not (
            self.is_win_for_marker(TicTacToe.human_marker) or 
            self.is_win_for_marker(TicTacToe.cpu_marker) or 
            self.no_more_moves()
        ):
            self.show_board()
        
            # take turns alternately
            if turn_identifier == TicTacToe.human_marker:
                self.human_turn()
                turn_identifier = TicTacToe.cpu_marker
            else:
                self.cpu_turn()
                turn_identifier = TicTacToe.human_marker
        
        # show final board
        self.show_board()
        
        # chit chat
        if self.is_win_for_marker(TicTacToe.human_marker):
            self.type_text('you win, how can this be?! this is literally impossible!')
        elif self.is_win_for_marker(TicTacToe.cpu_marker):
            self.type_text('I win, better luck next time')
        elif self.no_more_moves():
            self.type_text('we drew, I\'m pretty sure that\'s the best you can do')
        
    def create_board(self) -> Dict:
        '''
        represent board as integer keyed dico running with keys 1-9
        '''
        return dict(zip(range(1,10),cycle(TicTacToe.empty_marker)))

    def show_val(self,x,show_location : bool = False):
        '''
        utility function for self.show_board
        ability to show the name of a location or it's contents
        '''
        return str(x) if show_location else self.board[x]
    
    def show_board(self,show_location : bool = False) -> None:
        '''
        display the board
        print either the contents or the name of the location
        '''
        out = '\n' + \
        '\t\t' + self.show_val(1,show_location) + '|' + self.show_val(2,show_location) + '|' + self.show_val(3,show_location) + '\n' + \
        '\t\t' + '-+-+-\n' + \
        '\t\t' + self.show_val(4,show_location) + '|' + self.show_val(5,show_location) + '|' + self.show_val(6,show_location) + '\n' + \
        '\t\t' + '-+-+-\n' + \
        '\t\t' + self.show_val(7,show_location) + '|' + self.show_val(8,show_location) + '|' + self.show_val(9,show_location)
        
        print(out)
    
    def is_location_playable(self, loc : int) -> bool:
        '''
        utility function to check if location is occupied
        '''
        return self.board[loc] == TicTacToe.empty_marker
    
    def play_location(self, loc : int, player_marker : str, silent : bool = False) -> None:
        '''
        utility function to play a spot
        '''
        self.board[loc] = player_marker
        # show_board()
        
        if not silent:
            if self.is_win_for_marker(TicTacToe.human_marker): self.type_text('human wins')
            elif self.is_win_for_marker(TicTacToe.cpu_marker): self.type_text('cpu wins')
            elif self.no_more_moves():                           self.type_text('match drawn')
    
    def human_turn(self, msg = None) -> None:
        '''
        ask player to play a spot
        validate input data and check if place is occupied
        '''
        
        # say something if needed
        if msg:
            self.type_text(msg)
            self.show_board()
            
        # ensure input conversion works
        try:
            location = int(input('enter 1-9 : '))
            
            if not (0 < location < 10):
                msg = 'it\'s only 1-9, I told you already'
                self.human_turn(msg)
            else:
                if not self.is_location_playable(location):
                    msg = str(location) + ' is taken, try another spot'
                    self.human_turn(msg)
                else:
                    self.play_location(location,TicTacToe.human_marker)
        except:
            msg = 'pls try again'
            self.human_turn(msg)
    
    def cpu_turn(self):
        '''
        cpu player uses minimax algo to figure out optimal play
        '''
        # initialize
        best_score = -10000 # cpu wants to play MAX scoring position
        best_move  = None # placeholder for best position found
        
        # iterate over all board locations
        for loc in self.board.keys():
            # only consider unoccupied locations
            if self.is_location_playable(loc):
                # figure out minimax score of playing here position
                self.play_location(loc, TicTacToe.cpu_marker, silent = True) # temporarily play it
                score = self.minimax(self.board,False) # compute minimax score of this play
                self.play_location(loc, TicTacToe.empty_marker, silent = True) # roll it back as we only want to play the best position which is not necessarily this one
                
                # keep track of best playing position
                if score > best_score:
                    best_score = score
                    best_move  = loc

        # play best move
        time.sleep(random.randint(1,2)) # make it seem like cpu is thinking
        self.play_location(best_move, TicTacToe.cpu_marker, silent = True)

        # say something
        time.sleep(1) # pause before speaking
        msg_idx = next(self.speech_order)
        
        if   msg_idx == 0: self.type_text('not bad')
        elif msg_idx == 1: self.type_text('how\'d you like that?')
        elif msg_idx == 2: self.type_text('I can see the future')
        elif msg_idx == 3: self.type_text('sorry for the wait, my mum just called')
        elif msg_idx == 4: self.type_text('you really think you can win?')
        elif msg_idx == 5: self.type_text('you literally can\'t beat me')
        elif msg_idx == 6: self.type_text('Python\'s awesome')
        elif msg_idx == 7: self.type_text('nearly there')
        elif msg_idx == 8: self.type_text('you feeling lucky?')
        elif msg_idx == 9: self.type_text('I can\'t lose btw')

        time.sleep(1) # pause after speaking
        
    def minimax(self, board, is_maximising : bool):
        '''
        implement recursive minimax algo to compute score of playing this board to termination
        - cpu plays against itself
        - both (cpu) players are trying to maximize their score (a win) / minimize their score (a lose)
        '''
        
        # stopping conditions for recursion
        if self.is_win_for_marker(TicTacToe.cpu_marker):
            return 1 # like games where we win
        elif self.is_win_for_marker(TicTacToe.human_marker):
            return -1 # don't like games where we lose
        elif self.no_more_moves():
            return 0 # indifferent to games that are drawn

        # both players        
        if is_maximising:
            # cpu wants to win
            best_score = -1000
            
            for k in board.keys():
                if self.is_location_playable(k):
                    # temporarily play move
                    self.play_location(k, TicTacToe.cpu_marker, silent = True)
                    score = self.minimax(board,False)
                    
                    # roll it back
                    self.play_location(k, TicTacToe.empty_marker, silent = True)
                    if score > best_score: # "best score" needs to be maximal
                        best_score = score
                        
            return best_score
        else:
            # cpu human wants to avoid losing
            best_score = 1000
            
            for k in board.keys():
                if self.is_location_playable(k):
                    # temporarily play move
                    self.play_location(k, TicTacToe.human_marker, silent = True)
                    score = self.minimax(board,True)
                    
                    # roll it back
                    self.play_location(k, TicTacToe.empty_marker, silent = True)
                    if score < best_score: # "best score" needs to be minimal
                        best_score = score
    
            return best_score
        
    def is_win_for_marker(self,player_marker : str):
        '''
        utility function to figure out if player with marker `player_marker` won
        '''
        # check all triplets for winning condition
        if   player_marker == self.board[1] == self.board[2] == self.board[3]: return True # top row
        elif player_marker == self.board[4] == self.board[5] == self.board[6]: return True # middle row
        elif player_marker == self.board[7] == self.board[8] == self.board[9]: return True # bottom row
        elif player_marker == self.board[1] == self.board[4] == self.board[7]: return True # leftmost col
        elif player_marker == self.board[2] == self.board[5] == self.board[8]: return True # middle col
        elif player_marker == self.board[3] == self.board[6] == self.board[9]: return True # rightmost col
        elif player_marker == self.board[1] == self.board[5] == self.board[9]: return True # diag top-left to bottom-right
        elif player_marker == self.board[7] == self.board[5] == self.board[3]: return True # diag bottom-left to top-right
        else:                                                                  return False
       
    def no_more_moves(self):
        '''
        utility function to figure out if board is full, used to help identify a draw condition
        '''
        return not any(x == TicTacToe.empty_marker for x in self.board.values())

'''
requested entry point function
'''
def tic_tac_toe():
    TicTacToe().play_game()
    
'''
entry point if running file
'''
if __name__ == '__main__':
    # run TicTacToe() if script called
    tic_tac_toe()
