import numpy as np
import random 
from collections import deque

def generate_puzzle():
    ''' This generates a random 9x9 sudoku puzzle'''
    puzzle_complete = False
    big_iter = 0
    while not puzzle_complete:
        big_iter = big_iter + 1
        if big_iter%10==0:print 'big_iter=',big_iter
        if big_iter > 100: break
        mat = np.zeros((9,9),dtype=np.int)
        nums = range(1,10)
        random.shuffle(nums) # random sequence of numbers 1 to 9
        mat[0,:] = nums
        for i in range(9):
            #print "ROW NUM ",i
            add_row(mat,i)
            if np.ravel(mat).tolist().count(0) == 0:
                puzzle_complete = True
    print 'Puzzle Complete --> ',puzzle_complete
    print mat
    return

def add_row(mat,row_num):
    max_iter = 0
    row_complete = False
    while (not row_complete) and (max_iter < 1000):
        max_iter = max_iter + 1
        orig_line = range(1,10)
        random.shuffle(orig_line)
        #if max_iter%100==0: 
        #    print 'max_iter=',max_iter
        #    print orig_line
        next_line = deque(orig_line)
        col_num = 0
        iter = 0
        while (len(next_line) > 0):
            iter = iter + 1
            #if iter % 1000 == 0: print 'iter=',iter
            if iter > 100: break
            # check col and square, either fails then rotate
            index = (row_num,col_num)
            new_num = next_line[0]
            if not check_column(mat,index,new_num):
            # if the number already appears in the column, then skip to next one
                next_line.rotate(1)
                continue
            if not check_square(mat,index,new_num):
                next_line.rotate(1)
                continue
            else: 
                tmp = next_line.popleft()
                mat[row_num,col_num] = tmp
                col_num = col_num + 1
                if len(next_line) == 0: row_complete = True
    return

def check_square(mat,index,new_num):
    ''' Check the 3x3 square of the particular index '''
    row_num = index[0]
    col_num = index[1]
    row_sq_begin = ((row_num)//3)*3
    row_sq_end = row_sq_begin + 3
    col_sq_begin = ((col_num)//3)*3
    col_sq_end = col_sq_begin + 3
    square = mat[row_sq_begin:row_sq_end,col_sq_begin:col_sq_end]
    num_list = np.ravel(square).tolist()
    # remove zeros
    for i in num_list:
        if i == 0: num_list.remove(i)
    return check_numlist(num_list,new_num)
    
def check_column(mat,index,new_num):
    ''' check the column that no numbers repeat '''
    row_num = index[0]
    col_num = index[1]
    num_list = mat[:row_num,col_num].tolist()
    return check_numlist(num_list,new_num)

def check_numlist(num_list,new_num):
    ''' Check to see if the new_num already exists in the num_list '''
    if num_list.count(new_num) > 0:
        return False
    return True
    
def check_nine(num_list):
    full_nine = range(1,10)
    for i in num_list:
        if full_nine.count(i) == 1:
            full_nine.remove(i)
        else: return False
    return True

def solve_main(puzzle_filename):
    # get puzzle from file
    puzzle_mat = read_puzzle(puzzle_filename)
    # make dictionary of possible options for each remaining number
    solve_puzzle(puzzle_mat)
    return 

def solve_puzzle(puzzle_mat):
    # create empty dictionary for pencil answers
    pencil = {}
    # loop through puzzle_mat and fill in pencil dictionary
    full_nine = range(1,10)
    for i in range(9):
        for j in range(9):
            if puzzle_mat[i,j] == 0:
                pencil[(i,j)]=full_nine
            else:
                pencil[(i,j)]=puzzle_mat[i,j]
    # now sweep the columns and rows
    return

def read_puzzle(puzzle_filename):
    # read puzzle sequence from file
    with open(puzzle_filename, 'r') as f:
        puzzle_data = f.read()
    # form matrix with puzzle sequence
    puzzle_string = ""
    for i in puzzle_data:
        puzzle_string = puzzle_string + i + ","
    #remove trailing comma
    puzzle_string = puzzle_string.rstrip(",")
    #convert to 1-D array
    puzzle_array = np.fromstring(puzzle_string,dtype=int,sep=',')
    #reshape 1-D array to 9x9 square array
    puzzle_mat = np.reshape(puzzle_array,(9,9))
    print puzzle_mat
    return puzzle_mat

solve_main("./puzzle01.txt")
#generate_puzzle()