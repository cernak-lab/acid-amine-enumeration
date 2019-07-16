def loader():

    N = 320
    dist = int(200100/N)
    start = 9300
    c = 1

    with open("reaction_names.txt", "r") as output:
        for s in output:
            # if c % 5 == 0:
                # print("hs2", str(start), str(start+dist), c)
            if c % 2 == 0:
                print("band hs2 b1 b1 " + str(start) + " " + str(start+dist) + " black")
            else:
                print("band hs2 b2 b2 " + str(start) + " " + str(start+dist) + " grey")
            start = start + dist

            c = c + 1

loader()
