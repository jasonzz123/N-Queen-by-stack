#jason zhou stack version of n-queen puzzle

import random
from bitarray import bitarray

nSize = 9 #8 
st_picked=[]
st_candidate =[x for x in range(nSize)]
#random.shuffle(st_candidate) #ok!
flag_used = bitarray(nSize)
flag_used.setall(0)
nSol =0
st_back =[] #stack of backtracking,record floor,pos
nFirst =0 #count of choose 1st queen, end condition of recursion

def clear():
    global nFirst
    global st_candidate  #adjust it to keep whole solve space
    global flag_used
    
    nFirst +=1 
    head = (nFirst-1) % nSize
    st_candidate.sort() #sort candidate 2 keep solve sapce MAX
    if head >0:
        tmp = st_candidate[0]
        st_candidate[0] = st_candidate[head]
        st_candidate[head]=tmp
        st_back.clear()  #clear the backtrack stack in case of riot
    flag_used.setall(0)  #clear flag state 2 from scratch


def isSafe(qq):
    row1=len(st_picked)
    # print(row1, qq) #debug
    
    if row1==0 : #1st queen in blank space, always safe
       return True

    for row ,col in enumerate(st_picked):
       if (row1-row)==abs(qq-col):
           return False
    return True   

def myqueen(n):

    global st_picked, st_candidate
    global flag_used
    global nSol
    global st_back
    
    while len(st_candidate)>=0 and nFirst <= n :  

       n_p = len(st_picked)
                    
       if n_p==n :
          print('SOLUTION:',st_picked)
          nSol +=1
          #break
          #print('Solution backtack...') #solution backtracking, pop 2 item
                                       
          sol1 = st_picked.pop()
          st_back.append((n-1, sol1))
          st_candidate.append(sol1)
          flag_used[sol1]=1 #treat as this brach used, backtrack used, can not go through
          
          if st_back:
              #print('backtrack del',n_p, st_back) #debug
              for ele in st_back:
                  if ele[0]==n_p: #when backtrack, del deep ele
                      st_back.remove(ele)
          continue
          

       if flag_used.all() and n_p < n :  #all tested, backtack!!
          if n_p==0:  #!!!special case
             return
          
          back1= st_picked.pop()  #stack pop,flag clear          
          st_candidate.append(back1)
          flag_used.setall(0)
          for x in st_picked:
              flag_used[x]=1

          flag_used[back1] = 1 #!!!flag this brach used, backtrack used, can not go through

          
          if st_back:
              #print('backtrack del',n_p, st_back) #debug
                           
              st_back =[ele for ele in st_back if ele[0]!=n_p] #debug, use list comprehension!!!
              #print('after backtrack del', st_back)         
          st_back.append((n_p-1,back1)) #record backtrack
          
          #print('flag:', flag_used) #debug flag state before next loop
          continue   #!!!backtack!!! so continue next loop            
           
       if st_back :  #backtrack occur case,latest one,set before pick action
           #r1, p1 = st_back.pop()
           #print('st_back in:', st_back) #debug
           for r1, p1 in st_back:  #multiple backtrack in this row
               #if n_p-1 == r1 : #and n_p+1 < n:  # n_p+1 = n, next to leaf node, not set 1, or may miss solution !!!
               if n_p == r1 : # pick next row !!!! avoid dead loop!!!
                  #print('Back track in:', r1,p1)
                  flag_used[p1] =1
        
       if not st_picked: #empty stack
           clear()   #reset before a blank space, adjust order of candidate to find every solution
                   
       for it in st_candidate:  #pick next queen in the row
           
           pick_a = it
           
           if n_p+1 ==n: #debug , pick leaf, check status
              pass #print('PICK A LEAF:', pick_a, flag_used)

           if flag_used[pick_a]==1: #backtrack used or tested in this cycle
              continue

           if isSafe(pick_a):

              st_picked.append(pick_a)

              st_candidate.remove(pick_a)
              flag_used.setall(0)  #!!!
              for x in st_picked:
                  flag_used[x]=1

              break
           else:       # not safe
              flag_used[pick_a] =1


def main():
    print(st_candidate)
    myqueen(nSize)
    print('Total Solutions:', nSol)
    print('backtrack:',st_back)
    print('nFirst:', nFirst)
main()

