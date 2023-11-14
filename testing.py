import json


def ourlist(ctx,*args):
    def responding(ctx,responce):
        if type(responce) == str:
            print(responce)
            return
        for x in responce:print(x)
    filepath = "C:\\Users\\User\\OneDrive\\Desktop\\coding\\Discord Bot\\listjson.json"
    file = open(filepath)
    data = json.load(file)
    responce = "Bro's an idiot if he sees this message"

    #This happens when there is nothing in args
    ''.join(args)
    ','.split(args)
    if len(args) == 0:
        responce = list(responce)
        responce.clear()
        for x in data:
             responce.append(x)
        responding(ctx,responce)
    #This happens when we have only one arg in which case we print everything in the list. If there is no list of that type we should then display "No valid list"
    if len(args) == 1:
        responce = list(responce)
        responce.clear()
        try:
            responce.append(args[0]+":")
            for x in data[args[0]]:
                responce.append(x)
        except KeyError:responce.append("You did not put a valid list")
        responding(ctx,responce)
    #adds everything after the list name to that list, if there is no list of that name then we make a new list and add the text to there
    if len(args) >= 2:
        responce = list(responce)
        responce.clear()
        responce.append(args[0]+":")

        if args[0] in data:
            data[args[0]].append(args[1:])
        else:
            data[args[0]] = [args[1:]]

        data[args[0]][len(data[args[0]])-1] = "\n".join(data[args[0]][len(data[args[0]])-1])
        responding(ctx,responce)

    #adds everything back to the file
    with open(filepath, "w") as json_file:
        json.dump(data, json_file)
ourlist(0,"Elias' Revenge")