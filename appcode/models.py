"""
    appcode.models
    ===================

"""
from google.appengine.ext import db

class Account(db.Model):
    '''
    email is gmail address of the user
    name is given by user
    payment is the real currency paid by user
    type is eigher normal user('normal') or user created through shared links('share')
    shareCount is the number of links shared by the user
    '''
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    payment = db.FloatProperty(required=True)
    acc_type = db.StringProperty(required=True)
    shareCount = db.IntegerProperty(required=True)

class Player(db.Model):
    email = db.StringProperty(required=True)
    networth = db.FloatProperty(required=True)
    #networth is calculated by money + money_spent
    money = db.FloatProperty(required=True)
    islandId = db.IntegerProperty(required=True)
    money_spent = db.FloatProperty(required=True)
    

class Island(db.Model):
    name = db.StringProperty(required=True)
    creatorEmail = db.StringProperty(required=True)
    numOfPlayer = db.IntegerProperty(required=True)
    #numOfPlants = db.IntegerProperty(required=True)
    maxNumOfPlayers = db.IntegerProperty(required=True)
    maxNumOfPlants = db.IntegerProperty(required=True)
    
class Plant(db.Model):
    playerId = db.IntegerProperty(required=True)
    islandId = db.IntegerProperty(required=True)
    region = db.StringProperty(required=True)
    cost = db.FloatProperty(required=True)
    capacity = db.IntegerProperty(required=True)
    currentCapacity = db.IntegerProperty(required=True)
    numOfWorkers = db.IntegerProperty(required=True)
    workerCost = db.FloatProperty(required=True)
    workerHealth = db.IntegerProperty(required=True)
    workerSkills = db.IntegerProperty(required=True)
    workerProductivity = db.IntegerProperty(required=True)
    #based on number of workers and formula >> ((1*Health)+(0.5*Skills)+(0.75*Productivity))*10
    productionLimit = db.IntegerProperty(required=True)
    
class Celebrity(db.Model):
    influence = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    cost = db.FloatProperty(required=True)
    
class Shoe(db.Model):
    plantId = db.IntegerProperty(required=True)
    sole = db.IntegerProperty(required=True)
    body = db.IntegerProperty(required=True)
    color = db.IntegerProperty(required=True)
    price = db.FloatProperty(required=True)
    qty = db.IntegerProperty(required=True)
    costPrice = db.FloatProperty(required=True)
    
class DemandTransaction(db.Model):
    shoeId = db.IntegerProperty(required=True)
    salePrice = db.FloatProperty(required=True)
    shippingCost = db.FloatProperty(required=True)
    qty = db.IntegerProperty(required=True)

class PayPalTransaction(db.Model):
    email = db.StringProperty(required=True)
    cashAmt = db.FloatProperty(required=True)
    money = db.FloatProperty(required=True)
    status = db.StringProperty(required=True)
    playerId = db.IntegerProperty(required=True) #the player object the user want to added money to
    
class SupplyTransaction(db.Model):
    shoeId = db.IntegerProperty(required=True)
    costPerUnit = db.FloatProperty(required=True)
    qty = db.IntegerProperty(required=True)
    totalCost = db.FloatProperty(required=True)
    trxnDate = db.DateTimeProperty(required=True)