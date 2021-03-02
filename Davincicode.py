#This program is AI of a boardgame, "Davinci Code".
#Each tile corresponds to one number. 2*tile_number+color, joker's tile_number:100

# 다빈치코드 2인게임 AI 프로그램

import re


def id_to_tilestr(tile_id):
    msg = "white "if tile_id % 2 else "black "
    msg += str(tile_id//2)
    return msg


def tilestr_to_id(tile_str):
    msg = tile_str.split()
    if len(msg) != 2:
        return -1
    if msg[0] == "white":
        id = 1
    elif msg[0] == "black":
        id = 0
    else:
        return -1
    if 0 <= int(msg[1]) <= 11:
        id += 2*int(msg[1])
        return id
    else:
        return -1


def num_of_clue(len, index):
    left = index
    right = len-index-1
    return (left if left >= right else right, 0 if left >= right else 1)


def inputf(comment, re_format):
    print(comment, end='')
    pattern = re.compile(re_format)
    while True:
        userput = input()
        if pattern.match(userput):
            return userput
        else:
            print("wrong format")


class MyTile:
    def __init__(self, tile_id):
        self.tile = int(tile_id)
        self.opened = False

    def open_tile(self, opened):
        self.opened = opened

    def __eq__(self, other):
        return self.tile == other.tile

    def colorb(self):
        return True if self.tile % 2 else False

    def colors(self):
        return "White" if self.tile % 2 else "Black"

    def number(self):
        return self.tile // 2

    def show(self):
        print("< MyTile | {0} {1} , {2} opened >".format(
            self.colors(), self.number(), "" if self.opened else "not"))

    def showall(self):
        print("< MyTile | number : {0} , color : {1} , opened : {2} , tile id : {3} >".format(
            self.number(), self.colors(), self.opened, self.tile))


class MyTiles:
    def __init__(self):
        self.mytiles = []

    def insert(self, tile):
        if len(self.mytiles):
            for t in self.mytiles:
                if t.tile > tile.tile:
                    self.mytiles.insert(self.mytiles.index(t), tile)
                    return
            self.mytiles.append(tile)
        else:
            self.mytiles.append(tile)

    def len_non_opened(self):
        num = 0
        for t in self.mytiles:
            num += int(not t.opened)
        return num

    def show(self):
        for t in self.mytiles:
            t.show()

    def showall(self):
        for t in self.mytiles:
            t.showall()


class OppTile:
    def __init__(self, color_id):
        self.tile = -1
        self.opened = False
        if color_id:
            self.cases = set(range(0, 24)[1::2])
        else:
            self.cases = set(range(0, 24)[0::2])

    def open_tile(self, opened, tile_id):
        if opened:
            self.tile = tile_id
            self.opened = opened
            self.cases.clear()
        else:
            self.opened = False

    def delete_case(self, list):
        for i in list:
            self.cases.discard(i)

    def include_case(self, list):
        for i in list:
            self.cases.add(i)

    def colorb(self):
        if self.opened:
            return True if self.tile % 2 else False
        return True if list(self.cases)[0] % 2 else False

    def colors(self):
        if self.opened:
            return "White" if self.tile % 2 else "Black"
        return "White" if list(self.cases)[0] % 2 else "Black"

    def show(self):
        if self.opened:
            print("< OppTile | {0} {1} , opened >".format(
                self.colors(), self.tile//2))
        else:
            num_cases = set([])
            for case in list(self.cases):
                num_cases.add(case//2)
            print("< OppTile | {0} , cases : {1} >".format(
                self.colors(), str(num_cases)))

    def showall(self):
        if self.opened:
            print("< OppTile | number : {0} , color : {1} , opened : {2} , tile id : {3} >".format(
                self.tile//2, self.colors(), True, self.tile))
        else:
            print("< OppTile | color : {0} , cases : {1} >".format(
                self.colors(), str(self.cases)))


class OppTiles:
    def __init__(self):
        self.opptiles = []
        self.entire_cases = set(range(0, 24))

    def insert(self, tile, index=-1):
        if index == -1:
            self.opptiles.append(tile)
        else:
            self.opptiles.insert(index, tile)
        self.opptiles[index].cases = self.opptiles[index].cases & self.entire_cases
        self.reason_case()

    def delete_case(self, list):
        for i in list:
            self.entire_cases.discard(i)
        for t in self.opptiles:
            t.cases = t.cases & self.entire_cases
        self.reason_case()

    def include_case(self, list):
        for i in list:
            self.entire_cases.add(i)

    def open_tile(self, index, tile_id):
        self.opptiles[index].open_tile(True, tile_id)
        self.reason_case()

    def len_non_opened(self):
        num = 0
        for t in self.opptiles:
            num += int(not t.opened)
        return num

    def index_non_opened(self, index):
        non_opened_index = 0
        for i in list(range(0, index)):
            non_opened_index += int(not self.opptiles[i].opened)
        return non_opened_index

    def reason_case(self):
        min_cases = set(range(0, 24))
        for t in self.opptiles:
            if t.tile == -1:
                t.cases = t.cases & min_cases
                min_cases = set(range(sorted(list(t.cases))[0]+1, 24))
            else:
                min_cases = set(range(t.tile+1, 24))
        max_cases = set(range(0, 24))
        for t in self.opptiles[::-1]:
            if t.tile == -1:
                t.cases = t.cases & max_cases
                max_cases = set(range(0, sorted(list(t.cases))[-1]))
            else:
                max_cases = set(range(0, t.tile))

    def show(self):
        print("< OppTiles >")
        for t in self.opptiles:
            t.show()

    def showall(self):
        print("< OppTiles | entire cases : {0} >".format(
            str(self.entire_cases)))
        for t in self.opptiles:
            t.showall()


class AIGamer:
    def __init__(self):
        self.mts = MyTiles()
        self.opmts = OppTiles()
        self.ots = OppTiles()
        self.num_of_pile = [12, 12]  # 남은 타일(더미)의 개수 [검정, 하양]

    def mts_insert(self, tile):
        self.mts.insert(tile)
        self.opmts.insert(OppTile(tile.colorb()), self.mts.mytiles.index(tile))
        self.ots.delete_case([tile.tile])
        self.num_of_pile[tile.colorb()] -= 1
        return self.mts.mytiles.index(tile)

    def ots_insert(self, tile, index=-1):
        self.ots.insert(tile, index)
        self.num_of_pile[tile.colorb()] -= 1

    def mts_open_tile(self, index):
        self.mts.mytiles[index].open_tile(True)
        self.opmts.open_tile(index, self.mts.mytiles[index].tile)

    def ots_open_tile(self, index, tile_id):
        self.ots.open_tile(index, tile_id)

    def mytile_value(self, index):
        if self.opmts.opptiles[index].opened:
            return 10000
        n = len(self.opmts.opptiles[index].cases)
        len_non_opened = self.opmts.len_non_opened()
        return (n-1)*(len_non_opened+1)/2

    def guessing_value(self, index):
        if self.ots.opptiles[index].opened:
            return -1
        return 1+num_of_clue(self.ots.len_non_opened(), self.ots.index_non_opened(index))[0]

    def reason(self):
        best_play = (0, -1)  # [0]=index, [1]=value
        for idx, ot in enumerate(self.ots.opptiles):
            if ot.opened == False:
                if self.guessing_value(idx) > best_play[1] or (self.guessing_value(idx) == best_play[1] and len(ot.cases) < len(self.ots.opptiles[best_play[0]].cases)):
                    best_play = (idx, self.guessing_value(idx))
        return (best_play[0], sorted(list(self.ots.opptiles[best_play[0]].cases))[num_of_clue(self.ots.len_non_opened(), self.ots.index_non_opened(best_play[0]))[1]-1], best_play[1])

    def start(self):
        while True:
            command = input("command : ")

            if command == "myturn":
                if self.num_of_pile == [0, 0]:
                    mytile_values = [self.mytile_value(
                        i) for i in range(0, len(self.opmts.opptiles))]
                    mytile_index_to_open = mytile_values.index(
                        min(mytile_values))
                else:
                    if self.num_of_pile[1] > self.num_of_pile[0]:
                        print("get white tile")
                        mytile_index_to_open = self.mts_insert(MyTile(tilestr_to_id(
                            "white "+inputf("Please write new tile's number. ex) 4\n", '^(\d|1[01])$'))))
                    else:
                        print("get black tile")
                        mytile_index_to_open = self.mts_insert(MyTile(tilestr_to_id(
                            "black "+inputf("Please write new tile's number. ex) 4\n", '^(\d|1[01])$'))))

                mytile_value_to_open = self.mytile_value(mytile_index_to_open)

                #first guess
                guess = self.reason()
                print("Guess #{0} tile : {1}".format(
                    guess[0]+1, id_to_tilestr(guess[1])))

                result = inputf(
                    "Please write the result. ex) right or wrong\n", '^(right|wrong)$')
                if result == "right":
                    self.ots.open_tile(guess[0], guess[1])
                    if self.ots.len_non_opened() == 0:
                        print("game ends")
                        print("I win")
                        return
                    #additional guess
                    while True:
                        guess = self.reason()
                        # 추가로 추측할 조건
                        if guess[2] > mytile_value_to_open or len(self.ots.opptiles[guess[0]].cases) == 1:
                            print("Guess #{0} tile : {1}".format(
                                guess[0]+1, id_to_tilestr(guess[1])))
                            result = inputf(
                                "Please write the result. ex) right or wrong\n", '^(right|wrong)$')
                            if result == "right":
                                self.ots.open_tile(guess[0], guess[1])
                                if self.ots.len_non_opened() == 0:
                                    print("game ends")
                                    print("I win")
                                    return
                            else:
                                self.ots.opptiles[guess[0]].delete_case(
                                    [guess[1]])
                                self.mts.mytiles[mytile_index_to_open].open_tile(
                                    True)
                                break
                        else:
                            print("stop guessing")
                            break
                else:
                    self.ots.opptiles[guess[0]].delete_case([guess[1]])
                    self.mts.mytiles[mytile_index_to_open].open_tile(True)
                    print("open #{0} tile".format(mytile_index_to_open+1))

            elif command == "oppturn":
                if not self.num_of_pile == [0, 0]:
                    newtile_msg = inputf(
                        "please write opponent's new tile ex) #1 black , #3 white\n", '^#\d{1,2} (black|white)$')
                    self.ots_insert(OppTile(newtile_msg.split()[1] == "white"), int(
                        newtile_msg.split()[0][1:])-1)
                #first guess
                oppguess_msg = inputf(
                    "please write opponent's guess ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                oppguess = [int(oppguess_msg.split()[0][1:])-1,
                            tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                    print("right")
                    self.mts_open_tile(oppguess[0])
                    if self.mts.len_non_opened() == 0:
                        print("game ends")
                        print("I lose")
                        return
                    #additional guess
                    while True:
                        oppguess_msg = inputf(
                            "please write opponent's guess. if opponent aren't reasoning, write 'pass' ex) #1 black 5 , #4 white 10\n", '^(pass|(#\d{1,2} (black|white) (\d|1[01])))$')
                        if oppguess_msg == 'pass':
                            break
                        oppguess = [int(oppguess_msg.split()[0][1:])-1,
                                    tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                        if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                            print("right")
                            self.mts_open_tile(oppguess[0])
                            if self.mts.len_non_opened() == 0:
                                print("game ends")
                                print("I lose")
                                return
                        else:
                            print("wrong")
                            self.opmts.opptiles[oppguess[0]
                                                ].delete_case([oppguess[1]])
                            for ot in self.ots.opptiles:
                                if not ot.opened:
                                    ot.delete_case([oppguess[1]])
                            opptile_msg = inputf(
                                "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                            opptile = [int(opptile_msg.split()[
                                           0][1:])-1, tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                            break
                else:
                    print("wrong")
                    self.opmts.opptiles[oppguess[0]].delete_case([oppguess[1]])
                    for ot in self.ots.opptiles:
                        if not ot.opened:
                            ot.delete_case([oppguess[1]])
                    opptile_msg = inputf(
                        "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                    opptile = [int(opptile_msg.split()[0][1:])-1,
                               tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                    self.ots.open_tile(opptile[0], opptile[1])

            elif command == "show":
                print("My tiles------------------------------")
                self.mts.show()
                print("My tiles the other side saw-----------")
                self.opmts.show()
                print("Opponent's tiles----------------------")
                self.ots.show()
                print("Pile----------------------------------")
                print("{0} black tiles, {1} white tiles".format(
                    self.num_of_pile[0], self.num_of_pile[1]))

            elif command == "showall":
                print("My tiles------------------------------")
                self.mts.showall()
                print("My tiles the other side saw-----------")
                self.opmts.showall()
                print("Opponent's tiles----------------------")
                self.ots.showall()
                print("Pile----------------------------------")
                print("{0} black tiles, {1} white tiles".format(
                    self.num_of_pile[0], self.num_of_pile[1]))
            elif command == "gamestart":
                start_player=inputf("Please write start player : ",'^(myturn|oppturn)$')
                #command == debug gamestart
                self.mts = MyTiles()
                self.opmts = OppTiles()
                self.ots = OppTiles()
                self.num_of_pile = [12, 12]

                print("Please enter your 4 tiles. ex) black 7 , white 2")
                for i in range(0, 4):
                    self.mts_insert(
                        MyTile(tilestr_to_id(inputf("", '^((white|black) (\d{1}|1[01]{1}))$'))))

                print(
                    "Please enter the 4 colors of the opponent's tile in order. ex) black , white")
                for i in range(0, 4):
                    self.ots_insert(OppTile(True if inputf(
                        "", '^(white|black)$') == "white" else False))

                print("The game started normally.")

                #command == show
                print("My tiles------------------------------")
                self.mts.show()
                print("My tiles the other side saw-----------")
                self.opmts.show()
                print("Opponent's tiles----------------------")
                self.ots.show()
                print("Pile----------------------------------")
                print("{0} black tiles, {1} white tiles".format(
                    self.num_of_pile[0], self.num_of_pile[1]))
                
                if start_player=="oppturn": #command == oppturn
                    if not self.num_of_pile == [0, 0]:
                        newtile_msg = inputf(
                            "please write opponent's new tile ex) #1 black , #3 white\n", '^#\d{1,2} (black|white)$')
                        self.ots_insert(OppTile(newtile_msg.split()[1] == "white"), int(
                            newtile_msg.split()[0][1:])-1)
                    #first guess
                    oppguess_msg = inputf(
                        "please write opponent's guess ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                    oppguess = [int(oppguess_msg.split()[0][1:])-1,
                                tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                    if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                        print("right")
                        self.mts_open_tile(oppguess[0])
                        if self.mts.len_non_opened() == 0:
                            print("game ends")
                            print("I lose")
                            return
                        #additional guess
                        while True:
                            oppguess_msg = inputf(
                                "please write opponent's guess. if opponent aren't reasoning, write 'pass' ex) #1 black 5 , #4 white 10\n", '^(pass|(#\d{1,2} (black|white) (\d|1[01])))$')
                            if oppguess_msg == 'pass':
                                break
                            oppguess = [int(oppguess_msg.split()[0][1:])-1,
                                        tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                            if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                                print("right")
                                self.mts_open_tile(oppguess[0])
                                if self.mts.len_non_opened() == 0:
                                    print("game ends")
                                    print("I lose")
                                    return
                            else:
                                print("wrong")
                                self.opmts.opptiles[oppguess[0]
                                                    ].delete_case([oppguess[1]])
                                for ot in self.ots.opptiles:
                                    if not ot.opened:
                                        ot.delete_case([oppguess[1]])
                                opptile_msg = inputf(
                                    "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                                opptile = [int(opptile_msg.split()[
                                            0][1:])-1, tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                                break
                    else:
                        print("wrong")
                        self.opmts.opptiles[oppguess[0]].delete_case([oppguess[1]])
                        for ot in self.ots.opptiles:
                            if not ot.opened:
                                ot.delete_case([oppguess[1]])
                        opptile_msg = inputf(
                            "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                        opptile = [int(opptile_msg.split()[0][1:])-1,
                                tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                        self.ots.open_tile(opptile[0], opptile[1])
                
                while True:
                    #command == myturn
                    print("myturn---------------------------------------------------")
                    if self.num_of_pile == [0, 0]:
                        mytile_values = [self.mytile_value(
                            i) for i in range(0, len(self.opmts.opptiles))]
                        mytile_index_to_open = mytile_values.index(
                            min(mytile_values))
                    else:
                        if self.num_of_pile[1] > self.num_of_pile[0]:
                            print("get white tile")
                            mytile_index_to_open = self.mts_insert(MyTile(tilestr_to_id(
                                "white "+inputf("Please write new tile's number. ex) 4\n", '^(\d|1[01])$'))))
                        else:
                            print("get black tile")
                            mytile_index_to_open = self.mts_insert(MyTile(tilestr_to_id(
                                "black "+inputf("Please write new tile's number. ex) 4\n", '^(\d|1[01])$'))))

                    mytile_value_to_open = self.mytile_value(mytile_index_to_open)

                    #first guess
                    guess = self.reason()
                    print("Guess #{0} tile : {1}".format(
                        guess[0]+1, id_to_tilestr(guess[1])))

                    result = inputf(
                        "Please write the result. ex) right or wrong\n", '^(right|wrong)$')
                    if result == "right":
                        self.ots.open_tile(guess[0], guess[1])
                        if self.ots.len_non_opened() == 0:
                            print("game ends")
                            print("I win")
                            return
                        #additional guess
                        while True:
                            guess = self.reason()
                            # 추가로 추측할 조건
                            if guess[2] > mytile_value_to_open or len(self.ots.opptiles[guess[0]].cases) == 1:
                                print("Guess #{0} tile : {1}".format(
                                    guess[0]+1, id_to_tilestr(guess[1])))
                                result = inputf(
                                    "Please write the result. ex) right or wrong\n", '^(right|wrong)$')
                                if result == "right":
                                    self.ots.open_tile(guess[0], guess[1])
                                    if self.ots.len_non_opened() == 0:
                                        print("game ends")
                                        print("I win")
                                        return
                                else:
                                    self.ots.opptiles[guess[0]].delete_case(
                                        [guess[1]])
                                    self.mts.mytiles[mytile_index_to_open].open_tile(
                                        True)
                                    break
                            else:
                                print("stop guessing")
                                break
                    else:
                        self.ots.opptiles[guess[0]].delete_case([guess[1]])
                        self.mts.mytiles[mytile_index_to_open].open_tile(True)
                        print("open #{0} tile".format(mytile_index_to_open+1))

                    #command == oppturn
                    print("oppturn--------------------------------------------------")
                    if not self.num_of_pile == [0, 0]:
                        newtile_msg = inputf(
                            "please write opponent's new tile ex) #1 black , #3 white\n", '^#\d{1,2} (black|white)$')
                        self.ots_insert(OppTile(newtile_msg.split()[1] == "white"), int(
                            newtile_msg.split()[0][1:])-1)
                    #first guess
                    oppguess_msg = inputf(
                        "please write opponent's guess ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                    oppguess = [int(oppguess_msg.split()[0][1:])-1,
                                tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                    if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                        print("right")
                        self.mts_open_tile(oppguess[0])
                        if self.mts.len_non_opened() == 0:
                            print("game ends")
                            print("I lose")
                            return
                        #additional guess
                        while True:
                            oppguess_msg = inputf(
                                "please write opponent's guess. if opponent aren't reasoning, write 'pass' ex) #1 black 5 , #4 white 10\n", '^(pass|(#\d{1,2} (black|white) (\d|1[01])))$')
                            if oppguess_msg == 'pass':
                                break
                            oppguess = [int(oppguess_msg.split()[0][1:])-1,
                                        tilestr_to_id(oppguess_msg[oppguess_msg.index(' ')+1:])]
                            if self.mts.mytiles[oppguess[0]].tile == oppguess[1]:
                                print("right")
                                self.mts_open_tile(oppguess[0])
                                if self.mts.len_non_opened() == 0:
                                    print("game ends")
                                    print("I lose")
                                    return
                            else:
                                print("wrong")
                                self.opmts.opptiles[oppguess[0]
                                                    ].delete_case([oppguess[1]])
                                for ot in self.ots.opptiles:
                                    if not ot.opened:
                                        ot.delete_case([oppguess[1]])
                                opptile_msg = inputf(
                                    "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                                opptile = [int(opptile_msg.split()[
                                            0][1:])-1, tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                                break
                    else:
                        print("wrong")
                        self.opmts.opptiles[oppguess[0]].delete_case([oppguess[1]])
                        for ot in self.ots.opptiles:
                            if not ot.opened:
                                ot.delete_case([oppguess[1]])
                        opptile_msg = inputf(
                            "please write the tile that opponent opened ex) #1 black 5 , #4 white 10\n", '^#\d{1,2} (black|white) (\d|1[01])$')
                        opptile = [int(opptile_msg.split()[0][1:])-1,
                                tilestr_to_id(opptile_msg[opptile_msg.index(' ')+1:])]
                        self.ots.open_tile(opptile[0], opptile[1])
                    
                    #command == show
                    print("My tiles------------------------------")
                    self.mts.show()
                    print("My tiles the other side saw-----------")
                    self.opmts.show()
                    print("Opponent's tiles----------------------")
                    self.ots.show()
                    print("Pile----------------------------------")
                    print("{0} black tiles, {1} white tiles".format(
                        self.num_of_pile[0], self.num_of_pile[1]))
            
            elif command == "debug gamestart":
                self.mts = MyTiles()
                self.opmts = OppTiles()
                self.ots = OppTiles()
                self.num_of_pile = [12, 12]

                print("Please enter your 4 tiles. ex) black 7 , white 2")
                for i in range(0, 4):
                    self.mts_insert(
                        MyTile(tilestr_to_id(inputf("", '^((white|black) (\d{1}|1[01]{1}))$'))))

                print(
                    "Please enter the 4 colors of the opponent's tile in order. ex) black , white")
                for i in range(0, 4):
                    self.ots_insert(OppTile(True if inputf(
                        "", '^(white|black)$') == "white" else False))

                print("The game started normally.")
                #command == show
                print("My tiles------------------------------")
                self.mts.show()
                print("My tiles the other side saw-----------")
                self.opmts.show()
                print("Opponent's tiles----------------------")
                self.ots.show()
                print("Pile----------------------------------")
                print("{0} black tiles, {1} white tiles".format(
                    self.num_of_pile[0], self.num_of_pile[1]))

            elif command == "quit":
                return

            else:
                print("wrong command")

my = AIGamer()
my.start()
