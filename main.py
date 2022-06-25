strategy = {}
optEnd = {}

def itomx(arg) :
  i = 0
  mx = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
  while arg > 0 :
    mx[i//3][i%3] = {0: ' ', 1: 'X', 2: 'O'}[arg % 3]
    arg //= 3
    i+=1
  return [''.join(x) for x in mx]

def printState(state):
  board = itomx(state)
  board = [list(x) for x in board]
  for x in range(9):
    if (board[x//3][x%3] == ' '):
      board[x//3][x%3] = str(x)
  board = [''.join(x) for x in board]
  for x in board:
    print(x)

def eval(state) :
  mx = itomx(state)
  lines = [
    *mx, 
    *[''.join([x[y] for x in mx]) for y in range(3)],
    ''.join(mx[x][x] for x in range(3)),
    ''.join(mx[2-x][x] for x in range(3)),
  ]
  if "XXX" in lines: return 1
  if "OOO" in lines: return -1
  return 0

def buildStrat(x, turn):
  if x in optEnd: return optEnd[x]
  mx = itomx(x)
  if ' ' not in ''.join(mx) or eval(x) != 0: optEnd[x] = eval(x); return optEnd[x]
  moves = [y for y in range(9) if mx[y//3][y%3] == ' ']
  choice = sorted(zip([buildStrat(x+(1+turn)*(3**y),(turn+1)%2) for y in moves],moves))[turn-1]
  strategy[x] = choice[1]
  optEnd[x] = choice[0]
  return choice[0]

def game(turn, state=0):
  res = eval(state)
  mx = itomx(state)
  if res == 0 and ' ' in ''.join(mx):
    if turn % 2 > 0:
      state += 2*3**strategy[state]
    else:
      printState(state)
      print({
        -1:" - You've already lost, the rest is just a ceremony!", 
        0 :" - ...", 
        1 :" - You are too incompetent to finish what you've started!.."
      }[optEnd[state]])
      x = "penguin"
      while not x.isnumeric(): x = input()
      state += 3**int(x)
    res = game(turn+1, state)
  else:
    printState(state)
  return res

def main():
  turn = "parrot"
  while turn not in ["0", "1"]:
    turn = input("Who starts the game? ( 0 - Human, 1 - Computer )\n")
  turn = int(turn)
  buildStrat(0, turn)
  print({ 
    -1 : "You lose, just as I've predicted!", 
    0  : "Draw..", 
    1  : "I-I.. I can't believe this! You've defeated me!" 
  }[game(turn)])

main()
