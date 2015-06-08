import requests
import simplejson
import sys

# change if on prod
URL = 'http://localhost:5000/api'

# makes sure value is numeric and within range
def sanatizeDigit(option, max):
    # is int
    try:
        option = int(option)
    except ValueError:
        return None
    # is not longer than list
    if option > max:
        return None
    # isn't less than list
    elif option < 1:
        return None
    else:
        return option


# choose the task
def chooseTask():
    # get list of tasks from api
    taskListResponse = requests.get(URL)
    taskList = simplejson.loads(taskListResponse.text)['tasks']
    # prompt
    print 'Select a task:'
    # list tasks
    for i in xrange(len(taskList)):
        print str(i + 1) + ') ' + taskList[i]

    # enter task based on input
    taskOption = raw_input()
    taskOption = sanatizeDigit(taskOption, len(taskList))

    # if not None
    if taskOption:
        return taskList[taskOption-1]
    else:
        print 'Invalid option please try again'
        print
        return chooseTask()


# call this to print json with depth 0
def printJSON(obj, depth):
    # call print function for nested dict or list with higher depth
    if type(obj) == dict:
        printJSONdict(obj, depth+1)
    elif type(obj) == list:
        printJSONlist(obj, depth+1)
    # else print string or numeric
    elif type(obj) == str:
        sys.stdout.write('"' + obj + '"')
    else:
        sys.stdout.write(str(obj))

def printJSONdict(objDict, depth):
    # print surrounding brackets one depth out
    print '\t'*(depth-1) + '{'
    first = True
    # loop and print values
    for key, value in objDict.iteritems():
        # if first time don't print trailing ,
        if first == True:
            first = False
        else:
            print ','
        sys.stdout.write('\t'*depth)
        printJSON(key, depth)
        sys.stdout.write(' : ')
        printJSON(value, depth)

    print
    sys.stdout.write('\t'*(depth-1) + '}')


def printJSONlist(objList, depth):
    # print surrrounding braces one depth out
    print '['
    first = True
    # print each object in list
    for o in objList:
        # if first time don't print trailing ,
        if first == True:
            first = False
        else:
            print ','
        printJSON(o, depth)

    print
    print '\t'*(depth-1) + ']'



# class for Inventory
class Inventory():
    """Inventory interaction class"""
    # init by asking about what inventory to use
    def __init__(self):
        # get list
        invListResponse = requests.get(URL + '/inventory')
        invList = simplejson.loads(invListResponse.text)['inventories']

        # prompt
        print 'Select an inventory or select "Create New Inventory":'

        # list inventories
        for j in xrange(len(invList)):
            print str(j + 1) + ') ' + invList[j]['name']

        # get option
        invOption = raw_input()
        invOption = sanatizeDigit(invOption, len(invList))

        # if not None
        if invOption:
            self.inventory = invList[invOption-1]['name']
            self.inventoryId = invList[invOption-1]['id']
            self.url = URL + '/inventory/' + self.inventory
        else:
            print 'Invalid option'
            print
            self.__init__()

    def getAll(self):
        """gets all of the items in inventory"""
        getResponse = requests.get(self.url)
        getList = simplejson.loads(getResponse.text)
        return getList['items']


    def getItems(self):
        """get and print all items"""
        items = self.getAll()
        printJSON(items, 0)



    def getItem(self, name):
        """get and print specific item"""
        items = self.getAll()
        # look through items
        for i in items:
            if i['name'] == name:
                printJSON(i, 0)
                return

        print 'Item not found'



    def addItem(self, attrs):
        """add or update item"""

        # check for different attributes being passed in
        if len(attrs) > 0:
            name = attrs[0]
        else:
            print 'No item name found'
            return
        if len(attrs) > 1:
            quantity = attrs[1]
        else:
            quantity = None
        if len(attrs) > 2:
            purchaseDate = attrs[2]
        else:
            purchaseDate = None
        if len(attrs) > 3:
            expirationDate = attrs[3]
        else:
            expirationDate = None
        if len(attrs) > 4:
            purchasePrice = attrs[4]
        else:
            purchasePrice = None

        # format them in json
        item = simplejson.dumps({
            'inventoryId': self.inventoryId
            , 'name': name
            , 'quantity': quantity
            , 'purchaseDate': purchaseDate
            , 'expirationDate': expirationDate
            , 'purchasePrice': purchasePrice
        })

        # add/update item
        addRequest = requests.post(self.url
                                , item
                                , headers = {'content-type': 'application/json'})
        # show info about return
        if addRequest.ok:
            printJSON(simplejson.loads(addRequest.text), 0)
        else:
            printJSON(simplejson.loads(addRequest.text), 0)
            print 'Item could not be added'



    def deleteItem(self, name):
        """delete item"""
        items = self.getAll()
        # look for item
        for i in items:
            if i['name'] == name:
                # confirm delete
                print 'Are you sure you want to delete ' + name + '? (y/n)'

                conf = raw_input()

                if conf.lower() == 'y' or conf.lower == 'yes':
                    # delete
                    deleted = requests.delete(self.url + '/' + str(i['id']))
                    if deleted.ok:
                        print 'Deleted ' + name
                else:
                    print 'Item not deleted'

                return

        print 'Item not found'


# while loop

# enter one task
task = chooseTask()
print

# task: inventory
if task == 'inventory':
    # list out inventories with new as option
    # select inventory
    inv = Inventory()

    # while not exit command
    while 1:
        print '''
Please give a command
Usage:
get                             returns all items
get <item_name>                 returns item with name given if exists
add <item_name> <quantity>      add or update an item with that name and attributes
delete <item_name>              delete item with that name
exit                            exit out and choose another inventory'''

        cmd = raw_input()
        print
        # split on spaces
        cmd = cmd.split()

        # if cmd has no length
        if len(cmd) < 1:
            print 'No command given'
            continue

        # all options for get
        elif cmd[0].lower() == 'get':
            if len(cmd) < 2:
                inv.getItems()
            else:
                inv.getItem(cmd[1])

        # insert/update command
        elif cmd[0].lower() == 'add':
            if len(cmd) < 2:
                print 'Invalid Command'
                continue
            else:
                inv.addItem(cmd[1:])


        # delete command
        elif cmd[0].lower() == 'delete':
            if len(cmd) < 2:
                print 'Invalid Command'
                continue
            else:
                inv.deleteItem(cmd[1])


        # exit
        elif cmd[0].lower() == 'exit':
            print 'Leaving ' + inv.inventory
            break

        # no other valid commands
        else:
            print 'Invalid Command'
            continue
