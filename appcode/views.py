"""
    appcode.views
    ===================

worker dictionary contains different workers of different region
Example worker['north']
For each worker['<region>'], it contains the following:
worker['north'][0] > Cost per year
worker['north'][1] > Health
worker['north'][2] > Skill
worker['north'][3] > Productivity
worker['north'][4] > Upgrade Cost For Health
worker['north'][5] > Upgrade Cost For Skills
worker['north'][6] > Upgrade Cost For Productivity

plant dictionary contains different plant of different region
Example plant['north']
For each plant['<region>'], it contains the following:
plant['north'][0] > Cost of the plant
plant['north'][1] > Capacity of the plant

shoeMatCost dictionary contains the cost of each unit of the material
shoeMatCost['sole'] = 0.05 cent per unit of the shoe's sole
shoeMatCost['body'] = 0.05 cent per unit of the shoe's body
shoeMatCost['color'] = 0.05 cent per unit of the shoe's color
"""

from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.http import HttpResponse
from google.appengine.api import users
from appcode.models import Account
from appcode.models import Island
from appcode.models import Player
from google.appengine.ext import db
from appcode.models import Shoe
from appcode.models import Plant
from appcode.models import DemandTransaction
from appcode.models import PayPalTransaction
from appcode.models import SupplyTransaction

import simplejson
import math
import random
import datetime

plant = {'north':[100000.0,600000], 'south':[200000.0,400000], 'east':[50000.0,1000000], 'west':[150000.0,800000]}
worker = {'north':[5000.0,30,50,80,5.0,5.0,5.0],'south':[10000.0,60,80,40,10.0,10.0,10.0],'east':[3000.0,50,30,80,3.0,3.0,3.0],'west':[8000.0,30,70,60,8.0,8.0,8.0]}
shoeMatCost = {'sole':0.05,'body':0.05,'color':0.05}
shippingCost = {}
shippingCost['north'] = {}
shippingCost['south'] = {}
shippingCost['east'] = {}
shippingCost['west'] = {}

shippingCost['north']['north'] = 1.0
shippingCost['north']['south'] = 3.0
shippingCost['north']['east'] = 2.0
shippingCost['north']['west'] = 2.0

shippingCost['south']['north'] = 3.0
shippingCost['south']['south'] = 1.0
shippingCost['south']['east'] = 2.0
shippingCost['south']['west'] = 2.0

shippingCost['east']['north'] = 2.0
shippingCost['east']['south'] = 2.0
shippingCost['east']['east'] = 1.0
shippingCost['east']['west'] = 3.0

shippingCost['west']['north'] = 2.0
shippingCost['west']['south'] = 2.0
shippingCost['west']['east'] = 3.0
shippingCost['west']['west'] = 1.0


def home(request):
    return redirect('/app/index.html');

def subscribe_login(request):
    user = users.get_current_user()
    if user:
        get_account()
    else:
        return redirect(users.create_login_url("/subscribe_login"))
    return redirect("/subscribe")
    
def login(request):
    '''
    Auth the user
    IF user is logged in to Gmail, get Account object and store in session - return "true"
    ELSE return login link
    '''
    user = users.get_current_user()
    if user:
        request.session['account'] = get_account()
        request.session.set_expiry(0)
        #return HttpResponse(s['account'].email)
        return redirect("/app/main.html#/theworld")
    return redirect(users.create_login_url("/login"))

def logout(request):
    '''
    return logout link
    '''
    return redirect(users.create_logout_url("/destroy"))

def load_account(request):
    '''
    Load Account from session
    '''
    session = request.session
    try:
        if session['account']:
            j = simplejson.dumps(session['account'].__dict__['_entity'])
            return HttpResponse(j, mimetype="application/json")
        else:
            return HttpResponse("aasdsad")
    except KeyError:
        pass
    dd = {}
    dd['error'] = "Error: cannot get session account"
    return HttpResponse(simplejson.dumps(dd),mimetype="application/json")

def load_player(request):
    session = request.session
    dd = {}
    
    #check necessary arguments
    if session.__contains__('islandId') == False:
        dd['error'] = "missing islandId"
        return HttpResponse(simplejson.dumps(dd),mimetype="application/json")
    
    if session.__contains__('account') == False:
        dd['error'] = "Error: Not logined."
        return HttpResponse(simplejson.dumps(dd),mimetype="application/json")
    
    email = session['account'].email
    islandId = session['islandId']
    island = Island.get_by_id(islandId)
    player_q = Player.gql("WHERE email = :1 and islandId = :2",email,islandId)
    player = player_q.get()
    player_dict = player.__dict__['_entity']
    player_dict['playerId'] = player.key().id()
    #get number of factories
    plantQuery = Plant.gql("WHERE playerId = :1 and islandId = :2",player.key().id(), islandId)
    player_dict['numPlants'] = plantQuery.count()
    player_dict['numWorkers'] = 0
    plants = plantQuery.fetch(1000)
    plantIds = []
    for p in plants:
        player_dict['numWorkers'] += p.numOfWorkers
        plantIds.append(p.key().id())
    player_dict['numShoes'] = 0
    shoeQuery = Shoe.gql("WHERE plantId in :1",plantIds)
    shoes = shoeQuery.fetch(1000)
    for shoe in shoes:
        player_dict['numShoes'] += shoe.qty
    player_dict['islandName'] = island.name
    jsonString = simplejson.dumps(player_dict)
    
    return HttpResponse(jsonString,mimetype="application/json")

def play(request):
    arguments = request.GET
    if arguments.__contains__('islandId') == False:
        return redirect("/app/main.html#/theworld") #need to change to intermediate page
    try:
        request.session['account']
        request.session['islandId'] = int(arguments.__getitem__('islandId')) 
    except KeyError:
        return redirect("/")
    except ValueError:
        return redirect("/app/error.html?error=ValueError")
    return redirect("/app/main.html#/theworld")
    

def destroy(request):
    session = request.session
    try:
        del session['account']
        del session['islandId']
    except KeyError:
        pass
    return redirect("/")


def share_login(request):
    user = users.get_current_user()
    if user:
        session = request.session
        session['account'] = get_account("share")
        session.set_expiry(0)
    else:
        return redirect(users.create_login_url("/share_login"))
    return redirect("/app/main.html#/theworld")

def get_account(accountType = 'normal'):
    ''''
    This method will retrieve and return Account object.
    In the event that no Account object is associated with the email,
    a new Account object will be created with the default values
    '''
    user = users.get_current_user()
    account = None
    if user:
        uemail = user.email()
        #uemail = uemail[0:uemail.find("@")]
        query = Account.gql("WHERE email = :1",uemail)
        if query.count() == 0:
            if accountType=='normal':
                account = Account(email=uemail,name=user.nickname(),payment=0.0,acc_type='normal',shareCount=0)
            else:
                account = Account(email=uemail,name=user.nickname(),payment=0.0,acc_type='share',shareCount=0)
            account.put()
        else:
            account = query.get()
        
        return account

def track_share(request):
    session = request.session
    try:
        account = session['account']
        account.shareCount = account.shareCount + 1
        account.put()
        session['account'] = account
        return HttpResponse(str(account.shareCount),"text")
    except KeyError:
        return HttpResponse("error","text")
    
def create_island(request):
    try:
        q = request.GET
        #iCreatorEmail = q.__getitem__('creatorEmail')
        iCreatorEmail = request.session['account'].email
        iName = q.__getitem__('name')
        if iName == "":
            raise ValueError
        iMaxNumOfPlayers = int(q.__getitem__('maxNumOfPlayers'))
        iMaxNumOfPlants = int(q.__getitem__('maxNumOfPlants'))
        island = Island(name=iName,creatorEmail=iCreatorEmail,numOfPlayer=0,maxNumOfPlayers=iMaxNumOfPlayers,maxNumOfPlants=iMaxNumOfPlants)
        island.put()
        return redirect("/app/main.html#/theworld")
    except KeyError:
        return redirect("/")
    except ValueError:
        return redirect("/app/error.html?error=ValueError")

def join_island(request):
    try:
        q = request.GET
        #jEmail = q.__getitem__('email')
        jEmail = request.session['account'].email
        jIslandId = int(q.__getitem__('islandId'))
        query = Player.gql("WHERE email = :1 and islandId = :2",jEmail,jIslandId)
        if query.count() > 0:
            return redirect("/play?islandId="+str(jIslandId)) #change to play game
        else:
            
            island = Island.get_by_id(jIslandId)
            if island != None and island.numOfPlayer < island.maxNumOfPlayers:
                player = Player(email = jEmail,money_spent=0.0,money=1000000.0,islandId=jIslandId,networth=1000000.0)
                player.put()
                island.numOfPlayer = island.numOfPlayer + 1
                island.put()
                return redirect("/play?islandId="+str(island.key().id()))
            else:
                return HttpResponse("error","text")
        #dd = {}
        #return HttpResponse(simplejson.dumps(dd),mimetype="application/json")
    except KeyError:
        return redirect("/")
    except ValueError:
        return "/app/error.html?error=ValueError"



def get_all_island(request):
    #acc = request.session['account']
    session = request.session
    try:
        if session['account']:
            q = Island.all()
            f = q.fetch(1000)
            islands = []
            for i in f:
                d = i.__dict__['_entity']
                d['islandId'] = i.key().id()
                islands.append(d)
            return HttpResponse(simplejson.dumps(islands),mimetype="application/json")
    except KeyError:
        pass
    dd = {}
    dd['error'] = "Error: cannot get session account"
    return HttpResponse(simplejson.dumps(dd),mimetype="application/json")
    

def get_account_players(request):
    session = request.session
    try:
        if session['account']:
            acc = session['account']
            q = Player.gql("WHERE email = :1",acc.email)
            f = q.fetch(1000)
            players = []
            for i in f:
                islandId = i.islandId
                island = Island.get_by_id(islandId)
                dd = i.__dict__['_entity']
                dd['playerId'] = i.key().id()
                dd['islandName'] = island.name
                players.append(dd)
            return HttpResponse(simplejson.dumps(players),mimetype="application/json")
        else:
            return HttpResponse("error","text")
    except KeyError:
        pass
    dd = {}
    dd['error'] = "Error: cannot get session account"
    return HttpResponse(simplejson.dumps(dd),mimetype="application/json")

def buy_plant(request):
    '''
    Check user logged in
    Check playerId belongs to account
    Get max plant limit from island id
    Check player's plant count
    '''
    
    if request.session.__contains__('account'):
        q = request.GET
        bPlayerId = int(q.__getitem__('playerId'))
        bIslandId = int(q.__getitem__('islandId'))
        bRegion = q.__getitem__('region')
        
        player = Player.get_by_id(bPlayerId)
        if player.email == request.session['account'].email:
            island = Island.get_by_id(bIslandId)
            if island != None:
                maxNumPlants = island.maxNumOfPlants
                plants = Plant.gql("WHERE playerId = :1 and islandId = :2",bPlayerId, bIslandId)
                if plants.count() < maxNumPlants:
                    bPlant = Plant(playerId=bPlayerId,islandId=bIslandId,region=bRegion,cost=plant[bRegion][0],capacity=plant[bRegion][1],numOfWorkers = 0, workerCost=worker[bRegion][0],workerHealth = worker[bRegion][1],workerSkills=worker[bRegion][2],workerProductivity=worker[bRegion][3], currentCapacity = 0, productionLimit = 0)
                    bPlant.put()
                    player.money = player.money - plant[bRegion][0]
                    player.money_spent = player.money_spent + plant[bRegion][0]
                    player.put()
    return redirect("/app/main.html#/theworld")
    

def hire_worker(request):
    '''
    Check user login
    Check plantId, numWorker, playerId exist in querydict (request.GET)
    Check plantId belongs to account
    Get plant by plantId
    '''
    
    if request.session.__contains__('account'):
        args = request.GET
        if args.__contains__('numWorker') and args.__contains__('plantId') and args.__contains__('playerId'):
            try:
                playerId = int(args.__getitem__('playerId'))
                plantId = int(args.__getitem__('plantId'))
                numWorker = int(args.__getitem__('numWorker'))
                
                plant = Plant.get_by_id(plantId)
                if plant != None and plant.playerId == playerId:
                    player = Player.get_by_id(playerId)
                    region = plant.region
                    workerCost = worker[region][0]
                    totalHireCost = workerCost * numWorker
                    if totalHireCost <= player.money:
                        plant.numOfWorkers += numWorker
                        capProd = int((1*plant.workerHealth) + (0.5*plant.workerSkills) + (0.75 * plant.workerProductivity) * 10 * plant.numOfWorkers)
                        if capProd > plant.capacity:
                            capProd = plant.capacity
                        plant.productionLimit = capProd
                        player.money = player.money - totalHireCost
                        player.money_spent = player.money_spent + totalHireCost
                        player.networth = player.money + player.money_spent
                        plant.put()
                        player.put()
                    else:
                        return redirect("/app/error.html?error=NotEnoughMoney")
                else:
                    return redirect("/app/error.htmlerror=InvalidPlant")
            except ValueError:
                return redirect("/app/error.html?error=ValueError")
        else:
            return redirect("/app/error.html?error=NotEnoughArguments")
    else:
        return redirect("/")
    return redirect("/app/main.html#/theworld")

def retrieve_workers(request):
    if request.session.__contains__('account'):
        args = request.GET
        if(args.__contains__('plantId')):
            plantIds = args.__getitem__('plantId').split(",");
            for i in plantIds:
                plantId = int(i)
                
        else:
            error = {}
            error['error':"Invalid Values."]
            return HttpResponse(simplejson.dumps(error),mimetype="application/json")
    else:
        error = {}
        error['error':"Unable to retrieve plants"]
        return HttpResponse(simplejson.dumps(error),mimetype="application/json")

def retrieve_player_plants(request):
    session = request.session
    ret = []
    if request.session.__contains__('account'):
        args = request.GET
        if args.__contains__('playerId'):
            try:
                playerId = int(args.__getitem__('playerId'))
                islandId = session['islandId']
                plants = Plant.gql("WHERE playerId = :1 and islandId = :2",playerId, islandId)
                for plant in plants:
                    d = plant.__dict__['_entity']
                    d['plantId'] = plant.key().id()
                    ret.append(d)
            except ValueError:
                error = {}
                error['error':"Invalid Values."]
                return HttpResponse(simplejson.dumps(error),mimetype="application/json")
    else:
        error = {}
        error['error':"Unable to retrieve plants"]
        return HttpResponse(simplejson.dumps(error),mimetype="application/json")
    return HttpResponse(simplejson.dumps(ret),mimetype="application/json")



def manufacture_shoe(request):
    '''
    Check user login
    Check plantId, playerId, sole, body, color, sellprice, qty exist in querydict (request.GET)
    Check plantId belongs to account
    Check shoeId belongs to plant
    Get plant by plantId
    '''

    if request.session.__contains__('account'):
        args = request.GET
        if args.__contains__('sole') and args.__contains__('body') and args.__contains__('color') and args.__contains__('playerId') and args.__contains__('plantId') and args.__contains__('sellprice') and args.__contains__('qty'):
            _sole = int(args.__getitem__('sole'))
            _body = int(args.__getitem__('body'))
            _color= int(args.__getitem__('color'))
            _qty= int(args.__getitem__('qty'))
            _sellprice = float(args.__getitem__('sellprice'))
            _plantId = int(args.__getitem__('plantId'))
            _playerId = int(args.__getitem__('playerId'))
            
            plant = Plant.get_by_id(_plantId)
            if plant != None and plant.playerId == _playerId:
                if _body < 10 or _sole < 10 or _color < 10:
                    return HttpResponse("Minimum shoe body, sole and color is 10")
                player = Player.get_by_id(_playerId)
                _costPrice = _body * shoeMatCost['body'] + _sole * shoeMatCost['sole'] + _color * shoeMatCost['color']
                _totalCost = _costPrice * _qty
                ##check if player has money
                hasMoney = (_totalCost <= player.money)
                ##has enough capacity
                hasCapacity = (_qty+plant.currentCapacity <= plant.productionLimit)
                if hasMoney == True and hasCapacity == True:
                    shoe = Shoe(plantId = _plantId, sole = _sole, body = _body, color = _color, price = _sellprice, qty = _qty, costPrice = _costPrice)
                    shoe.put()
                    player.money -= _totalCost
                    player.money_spent += _totalCost
                    player.networth = player.money + player.money_spent
                    player.put()
                    plant.currentCapacity += _qty
                    plant.put()
                    supTrxn = SupplyTransaction(shoeId = shoe.key().id(), costPerUnit = _costPrice, qty = _qty, totalCost = _totalCost, trxnDate = datetime.datetime.now())
                    supTrxn.put()
                    return redirect("/app/main.html#/theworld")
                elif hasMoney == False:
                    return HttpResponse("not enough money")
                else:
                    return HttpResponse("insufficient factory capacity")
            else:
                return HttpResponse("plant does not belong to player")
        else:
            return HttpResponse("value missing")
    else:
        return HttpResponse("Please Login.")


def retrieve_past_production(request):
    if request.session.__contains__('account'):
        args = request.GET
        if args.__contains__('playerId'):
            playerId = int(args.__getitem__('playerId'))
            plantQuery = db.GqlQuery("SELECT __key__ FROM Plant where playerId = :1",playerId)
            plantKeys= plantQuery.fetch(1000)
            plantIds = []
            for key in plantKeys:
                plantId = key.id()
                plantIds.append(plantId)
            shoeQuery = db.GqlQuery("SELECT * FROM Shoe WHERE plantId in :1",plantIds)
            shoes = shoeQuery.fetch(1000)
            shoeIds = []
            for shoe in shoes:
                shoeIds.append(shoe.key().id())
            supTrxnQuery = SupplyTransaction.gql("WHERE shoeId in :1 ORDER BY trxnDate DESC",shoeIds)
            supTrxns = supTrxnQuery.fetch(10)
            d = []
            for st in supTrxns:
                shoe = Shoe.get_by_id(st.shoeId)
                dd = st.__dict__['_entity']
                dd['trxnDate'] = str(dd['trxnDate'])
                dd['costPerUnit'] = "%.2f" % dd['costPerUnit']
                dd['plantId'] = shoe.plantId
                dd['sole'] = shoe.sole
                dd['body'] = shoe.body
                dd['color'] = shoe.color
                dd['sellprice'] = "%.2f" % shoe.price
                d.append(dd)
            return HttpResponse(simplejson.dumps(d),mimetype="application/json")
            #return HttpResponse(simplejson.dumps(shoeList),mimetype="application/json")
        else:
            return HttpResponse("no player id.")
    else:
        return redirect("/")

def buy_credits(request):
    
    args = request.GET
    if args.__contains__('details'):
        d = args.__getitem__('details')
        dd = d.split(",") 
        _playerId = int(dd[0])
        _money = float(dd[1])
        _cashAmt = float(dd[2])
        player = Player.get_by_id(_playerId)
        player.money += _money
        player.networth = player.money + player.money_spent
        player.put()
        email = player.email
        accQuery = Account.gql("WHERE email = :1",email)
        acc = accQuery.get()
        acc.payment += _cashAmt
        acc.put()
        ppTrxn = PayPalTransaction(email = player.email,cashAmt = _cashAmt, money = _money, status="OK",playerId = _playerId)
        ppTrxn.put()
        return redirect("/app/main.html#/theworld")
    else:
        return HttpResponse("Not enough arguments")

def buy_credits_fail(request):
    args = request.GET
    if args.__contains__('details'):
        d = args.__getitem__('details')
        dd = d.split(",") 
        _playerId = int(dd[0])
        _money = float(dd[1])
        _cashAmt = float(dd[2])
        player = Player.get_by_id(_playerId)
        ppTrxn = PayPalTransaction(email = player.email,cashAmt = _cashAmt, money = _money, status="ERROR",playerId = _playerId)
        ppTrxn.put()
        return HttpResponse("Fail")
    else:
        return HttpResponse("Not enough arguments")
#def set_shoeprice(request):
#    '''
#    Check if user logged in
#    Check if shoeId
#    '''
    
def system_buy_shoes(request):
    '''
    Check the logged in user
    
    '''
    user = users.get_current_user()
    marketing = 1
    
    dd = []
    if user:
        
        islandQuery = Island.all()
        islandCount = islandQuery.count()
        islands = islandQuery.fetch(islandCount)
        
        for island in islands:
            islandId = island.key().id()
            playerQuery = Player.gql("WHERE islandId = :1",islandId)
            numPlayers = playerQuery.count()
            
            plantQuery = Plant.gql("WHERE islandId = :1",islandId)
            plantCount = plantQuery.count()
            plants = plantQuery.fetch(plantCount)
            
            for plant in plants:
                plantId = plant.key().id()
                plantRegion = plant.region
                shoeQuery = Shoe.gql("WHERE plantId = :1",plantId)
                shoeCount = shoeQuery.count()
                shoes = shoeQuery.fetch(shoeCount)
                
                for shoe in shoes:
                    body = shoe.body
                    sole = shoe.sole
                    color = shoe.color
                    qty = shoe.qty
                    attractiveness = math.fabs((0.75*sole + body + 1.25 * color) / 3)
                    saleRegion = ""
                    
                    #randomly select sale-to-region
                    i = random.randint(1,4)
                    if i == 1:
                        saleRegion = "north"
                    elif i == 2:
                        saleRegion = "east"
                    elif i == 3:
                        saleRegion = "west"
                    elif i == 4:
                        saleRegion = "south"
                    
                    _shippingcost = shippingCost[plantRegion][saleRegion]
                    price = shoe.price + _shippingcost
                    
                    salesVolume = int(math.ceil(numPlayers * math.pow((attractiveness*marketing/price),2)))
                    
                    if salesVolume > qty:
                        salesVolume = qty
                    
                    shoe.qty = shoe.qty - salesVolume
                    shoe.put()
                    dd.append(shoe.key().id())
                    dd.append(salesVolume)
                    n = {'count':len(dd)}
                    totalShippingCost = salesVolume * _shippingcost
                    totalRevenue = salesVolume * shoe.price
                     
                    player = Player.get_by_id(plant.playerId)
                    player.money = player.money - totalShippingCost + totalRevenue
                    player.money_spent = player.money_spent + totalShippingCost
                    player.networth = player.money + player.money_spent
                    player.put()
                    
                    plant.currentCapacity = plant.currentCapacity - salesVolume
                    plant.put()
                    
                    demandTransaction = DemandTransaction(shoeId = shoe.key().id(),salePrice = shoe.price,shippingCost = _shippingcost,qty = salesVolume)
                    demandTransaction.put()
    else:
        return redirect(users.create_login_url("/system_buy_shoes"))
    return HttpResponse(simplejson.dumps(n),mimetype="application/json")

def island_ranking(request):
    if request.session.__contains__('islandId') and request.session.__contains__('account'):
        islandId = int(request.session['islandId'])
        playerQuery = Player.gql("WHERE islandId = :1 ORDER BY networth DESC",islandId)
        
        players = playerQuery.fetch(10)
        results = []
        
        for player in players:
            _playerDict = player.__dict__['_entity']
            playerId = player.key().id()
            plantQuery = Plant.gql("WHERE playerId = :1",playerId)
            countPlant = plantQuery.count()
            _playerDict['numPlants'] = countPlant
            _playerDict['numShoes'] = 0
            _playerDict['numWorkers'] = 0
            plants = plantQuery.fetch(countPlant)
            for plant in plants:
                _playerDict['numWorkers'] += plant.numOfWorkers
                plantId = plant.key().id()
                shoeQuery = Shoe.gql("WHERE plantId = :1",plantId)
                shoes = shoeQuery.fetch(1000)
                for shoe in shoes:
                    _playerDict['numShoes'] += shoe.qty
            results.append(_playerDict)
        
        return HttpResponse(simplejson.dumps(results),mimetype="application/json")
        
    else:
        dd = {}
        dd['error'] = "Error: No island selected. Please join or resume your game."
        return HttpResponse(simplejson.dumps(dd),mimetype="application/json")

#########################new methods
def demand_supply(request):
    if(request.GET.__contains__('playerId')):
        results = {}
        demand = []
        supply = []
        args = request.GET
        playerId = int(args.__getitem__('playerId'))
        plantQuery = Plant.gql("WHERE playerId = :1",playerId)
        plants = plantQuery.fetch(1000)
        for plant in plants:
            plantId = plant.key().id()
            shoeQuery = Shoe.gql("WHERE plantId = :1", plantId)
            shoes = shoeQuery.fetch(1000)
            for shoe in shoes:
                shoeId = shoe.key().id()
                supplyQuery = SupplyTransaction.gql("WHERE shoeId = :1",shoeId)
                supplys = supplyQuery.fetch(20)
                for _supply in supplys:
                    _sDict = _supply.__dict__['_entity']
                    _sDict['trxnDate'] = str(_sDict['trxnDate'])
                    _sDict['totalCost'] = float("%.2f" % round(_sDict['totalCost'],2))
                    _sDict['costPerUnit'] = float("%.2f" % round(_sDict['costPerUnit'],2))
                    _sDict['salePrice'] = float("%.2f" % round(shoe.price,2))
                    supply.append(_sDict)
                demandQuery = DemandTransaction.gql("WHERE shoeId = :1",shoeId)
                demands = demandQuery.fetch(20)
                for _demand in demands:
                    _dDict = _demand.__dict__['_entity']
                    demand.append(_dDict)
        results['demand'] = demand
        results['supply'] = supply
        n = {"count": len(results)}
        return HttpResponse(simplejson.dumps(results),mimetype="application/json")
    else:
        dd = {}
        dd['error'] = "Error: No game selected."
        return HttpResponse(simplejson.dumps(dd),mimetype="application/json")
    
#old method
#def _retrieve_shoe_templates(request):
#    '''
#    Return a list of shoes templates of a particular player(a particular plant)
#    '''
#    ret = []
#    if request.session.__contains__('account'):
#        getQuery = request.GET
#        playerId = int(getQuery.__getitem__('playerId'))
#        
#        shoes = Shoe.all()
#        for i in shoes:
#            plant = Plant.get_by_id(i.plantId)
#            if plant.playerId == playerId:
#               d = i.__dict__['_entity']
#                d['shoeId'] = i.key().id()
#                ret.append(d)
#    else:
#        error = {}
#        error['error':"Unable to retreive shoe templates."]
#        return HttpResponse(simplejson.dumps(error),mimetype="application/json")
#    return HttpResponse(simplejson.dumps(ret),mimetype="application/json")

#old method        
#def _create_shoe(request):
#    session = request.session
#    try:
#        account = session['account']
#        if account != None:
#            q = request.GET
#            splantId = int(q.__getitem__('plantId'))
#            ssole = int(q.__getitem__('sole'))
#            sbody = int(q.__getitem__('body'))
#            scolor = int(q.__getitem__('color'))
#            sprice = float(q.__getitem__('price'))
#            _costPrice = shoeMatCost['sole'] * ssole + shoeMatCost['body'] * sbody + shoeMatCost['color'] * scolor
#            shoe = Shoe(plantId=splantId,sole=ssole,body = sbody,color = scolor,price = sprice,qty=0,costPrice=_costPrice)
#            shoe.put()
#    except KeyError:
#        return redirect("/")
#    return redirect("/app/main.html")

#old method
#def _manufacture_shoe(request):
#    if request.session.__contains__('account'):
#        args = request.GET
#        if args.__contains__('shoeId') and args.__contains__('playerId'):
#            try:
#                playerId = int(args.__getitem__('playerId'))
#                plantId = int(args.__getitem__('plantId'))
#                sshoeId = int(args.__getitem__('shoeId'))
#                
#                plant = Plant.get_by_id(plantId)
#                shoe = Shoe.get_by_id(sshoeId)
#                if plant != None and plant.playerId == playerId:
#                    player = Player.get_by_id(playerId)
#                    number = int(args.__getitem__('qty'))
#                    stotalCost = shoe.costPrice * number
#                    toBeCapacity = plant.currentCapacity + number
#                    
#                    if toBeCapacity <= plant.productionLimit and stotalCost <= player.money:
#                        supplyTransaction = SupplyTransaction(shoeId=sshoeId,costPerUnit = shoe.costPrice,qty = number,totalCost=stotalCost,trxnDate = datetime.datetime.now().date())
#                        supplyTransaction.put()
#                        shoe.qty = shoe.qty + number
#                        shoe.put()
#                        player.money = player.money - stotalCost
#                        player.money_spent = player.money_spent + stotalCost
#                        player.networth = player.money + player.money_spent
#                        player.put()
#                        plant.currentCapacity += number
#                        plant.put()
#                    else:
#                        return HttpResponse("not enough cap")
#                else:
#                    return HttpResponse("plant is none or plant does not belongs to playerId")
#            except ValueError:
#                return redirect("/error?error=ValueError")
#        else:
#            return HttpResponse("no values")
#    else:
#        #return redirect("/index")
#        return HttpResponse("error no account")
#    return redirect("/app/main.html")
#Converting Python Objects to JSON format
#use simplejson.dumps(obj.__dict__)
#the resulting JSON string for the Account class is as follows:
#{"_email": "test", "_money": 1000000.0, "_parent_key": null, "_parent": null, "_entity": {"money": 1000000.0, "email": "test", "networth": 0.0}, "_app": null, "_Model__namespace": "", "_networth": 0.0}
#in angular, use > response._entity to get the account JSON object