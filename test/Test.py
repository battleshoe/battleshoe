'''
Created on May 11, 2009

@author: george
'''
import unittest
from django import http
from appcode.models import Account
from appcode.views import home
from django.test.client import Client
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.http import HttpResponse
from google.appengine.api import users
from appcode.models import Island
from appcode.models import Player

from google.appengine.ext import db
from appcode.models import Shoe
from appcode.models import Plant
from appcode.models import DemandTransaction
from appcode.models import PayPalTransaction
from appcode.models import SupplyTransaction
from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module


import simplejson
import math
import random

import logging
from google.appengine.ext import db
#import appcode.models

class Test(unittest.TestCase):


    def testName(self):
        self.assertTrue(True)
    
    #def test_api(self):
        #c = Client()
        #response = c.get('/api')
        #self.assertEqual(response.content,'121')
        

class View_Test(unittest.TestCase):
    #def test_load_account(self):
        #c = Client()
        #response = c.
        #self.assertEqual(response.content,)
    #def setUp(self):
        
    #    self.client = Client()
    #    self.client.get('/login')
    #    self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
    #    self.client.get('/join_island?islandId=2')
    #    self.client.get('/play?islandId=2')
    #    self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
    #    self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
    #    self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
    #    self.client.get('/buy_credits?details=3,0.0,0.0')
    #    self.client.get('/logout')
        
        
#    def tearDown(self):
    #    for a in Account.all():
    #        a.delete()
    #    for p in Player.all():
    #        p.delete()
    #    for i in Island.all():
    #        i.delete()
    #    for p in Plant.all():
    #        p.delete()
    #    for s in Shoe.all():
    #        s.delete()
    #    for d in DemandTransaction.all():
    #        d.delete()
    #    for p in PayPalTransaction.all():
    #        p.delete()
    #    for s in SupplyTransaction.all():
    #        s.delete()
#        pass

    def test_get_all_island(self):
        
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/get_all_island')
        self.assertEqual(response.content, '[{"islandId": 2, "name": "BattleShoe", "numOfPlayer": 1, "maxNumOfPlants": 4, "creatorEmail": "battleshoe@gmail.com", "maxNumOfPlayers": 4}, {"islandId": 9, "name": "BattleShoe", "numOfPlayer": 0, "maxNumOfPlants": 4, "creatorEmail": "battleshoe@gmail.com", "maxNumOfPlayers": 4}, {"islandId": 14, "name": "BattleShoe", "numOfPlayer": 0, "maxNumOfPlants": 4, "creatorEmail": "battleshoe@gmail.com", "maxNumOfPlayers": 4}, {"islandId": 19, "name": "BattleShoe", "numOfPlayer": 0, "maxNumOfPlants": 4, "creatorEmail": "battleshoe@gmail.com", "maxNumOfPlayers": 4}]')
        
        #self.tearDown()
        
    def test_get_account_players(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/get_account_players')
        self.assertEqual(response.content, '[{"islandId": 2, "playerId": 3, "money": 99910.0, "money_spent": 900090.0, "islandName": "BattleShoe", "networth": 1000000.0, "email": "battleshoe@gmail.com"}]')
        #self.tearDown()
        
    def test_retrieve_player_plants(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/retrieve_player_plants?playerId=3')
        self.assertEqual(response.content, '[{"islandId": 2, "workerProductivity": 40, "capacity": 400000, "playerId": 3, "region": "south", "currentCapacity": 30, "workerCost": 10000.0, "workerHealth": 60, "cost": 200000.0, "plantId": 4, "workerSkills": 80, "numOfWorkers": 30, "productionLimit": 9100}, {"islandId": 2, "workerProductivity": 40, "capacity": 400000, "playerId": 3, "region": "south", "currentCapacity": 0, "workerCost": 10000.0, "workerHealth": 60, "cost": 200000.0, "plantId": 10, "workerSkills": 80, "numOfWorkers": 0, "productionLimit": 0}, {"islandId": 2, "workerProductivity": 40, "capacity": 400000, "playerId": 3, "region": "south", "currentCapacity": 0, "workerCost": 10000.0, "workerHealth": 60, "cost": 200000.0, "plantId": 15, "workerSkills": 80, "numOfWorkers": 0, "productionLimit": 0}, {"islandId": 2, "workerProductivity": 40, "capacity": 400000, "playerId": 3, "region": "south", "currentCapacity": 0, "workerCost": 10000.0, "workerHealth": 60, "cost": 200000.0, "plantId": 20, "workerSkills": 80, "numOfWorkers": 0, "productionLimit": 0}]')
        #self.tearDown()
    
        
    def test_load_account(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/load_account')
        self.assertEqual(response.content, '{"name": "battleshoe", "shareCount": 0, "payment": 0.0, "acc_type": "normal", "email": "battleshoe@gmail.com"}')
        #self.tearDown()
        
    def test_load_player(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/load_player')
        self.assertEqual(response.content, '{"islandId": 2, "playerId": 3, "money": -100090.0, "numWorkers": 30, "money_spent": 1100090.0, "islandName": "BattleShoe", "networth": 1000000.0, "numShoes": 30, "email": "battleshoe@gmail.com", "numPlants": 4}')
        #self.tearDown()
        
    def test_track_share(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get("/track_share")
        self.assertEqual(response.content, "1")
        #self.tearDown()
        
    def test_system_buy_shoes(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get("/system_buy_shoes")
        self.assertEqual(response.content, '{"count": 6}')
        #self.tearDown()
        
    def test_island_ranking(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get("/island_ranking")
        self.assertEqual(response.content, '[{"islandId": 2, "money": -100090.0, "numWorkers": 30, "money_spent": 1100090.0, "networth": 1000000.0, "numShoes": 30, "email": "battleshoe@gmail.com", "numPlants": 4}]')
        #self.tearDown()
        
    #def test_retrieve_workers(self):
    #    response = self.client.get("/retrieve_workers?plantId=4")
    #    self.assertEqual(response.content, "[]")
    
    #def test_retrieve_past_production(self):
    #    response = self.client.get('/retrieve_past_production?playerId=3')
    #    self.assertEqual(response.content, '[{"totalCost": 30.0, "body": 20, "color": 30, "sole": 10, "shoeId": 5, "qty": 10, "costPerUnit": "3.00", "plantId": 4, "sellprice": "10.00", "trxnDate": "2012-04-07 15:03:10.124000"}]')
        
    def test_buy_credits_fail(self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/buy_credits_fail?details=3,1000.0,100.0')
        self.assertEqual(response.content, "Fail")
        #self.tearDown()
        
    def test_demand_supply (self):
        self.client = Client()
        self.client.get('/login')
        self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        self.client.get('/join_island?islandId=2')
        self.client.get('/play?islandId=2')
        self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        self.client.get('/hire_worker?playerId=3&plantId=4&numWorker=10')
        self.client.get('/manufacture_shoe?sole=10&body=20&color=30&sellprice=10&qty=10&plantId=4&playerId=3')
        #self.client.get('/system_buy_shoes')
        self.client.get('/buy_credits?details=3,0.0,0.0')
        self.client.get('/logout')
        response = self.client.get('/demand_supply?playerId=3')
        self.assertEqual(response.content, '{"count": 2}')
        
    #def test_retrieve_shoe_templates(self):
        #self.client = Client()
        #self.client.get('/login')
        #self.client.get('/create_island?name=BattleShoe&maxNumOfPlayers=4&maxNumOfPlants=4')
        #self.client.get('/join_island?islandId=2')
        #self.client.get('/play?islandId=2')
        #self.client.get('/buy_plant?playerId=3&islandId=2&region=south')
        #self.client.get('/create_shoe?plantId=4&sole=1&body=2&color=3&price=10')
    #    response = self.client.get('/retrieve_shoe_templates?playerId=3')
    #    self.assertEqual(response.content, '[{"body": 2, "color": 3, "price": 10.0, "sole": 1, "shoeId": 5, "qty": 0, "plantId": 4, "costPrice": 0.30000000000000004}]')
        
    #def test_Account(self):
        #self.account = Account.(email = "battleshoe@gmail.com", name = "battleshoe", payment = 0.0, acc_type = "normal", shareCount = 0)
        #self.assertEqual(self.account.email,"battleshoe@gmail.com")
    
    #def test_create_island(self):
    #    self.client.get('/create_island?name=BattleShoe1&maxNumOfPlayers=4&maxNumOfPlants=4')
    #    q = Island.all()
    #    f = q.fetch(1000)
    #    islands = []
    #    for i in f:
    #        d = i.__dict__['_entity']
    #        d['islandId'] = i.key().id()
    #        islands.append(d)
    #    s = simplejson.dumps(islands)
    #    self.assertEqual(s.__str__(),'')
        
    
        
#class Model_Test(unittest.TestCase):
    #def setUp(self):
    # Populate test entities.
    #    a = Account(email='battleshoe@gmail.com',name='battleshoe',payment=0.0,acc_type='normal',shareCount=0)
    #    self.setup_key = a.put()
        #i = Island(name='battleshoe',creatorEmail='battleshoe@gmail.com',numOfPlayer=0,maxNumOfPlayers=4,maxNumOfPlants=4)
        #self.setup_key = i.put()
        #p = Player(email='battleshoe@gmail.com',networth=100000.0,money=0.0,islandId=2,money_spent=0.0)
        #selfsetup_key = p.put()
        
    #def test_new_entity(self):
    #    a = Account(email='battleshoe@gmail.com',name='battleshoe',payment=0.0,acc_type='normal',shareCount=0)
        
    #    self.assertEqual(a.email,'battleshoe@gmail.com')
        
    #def test_saved_enitity(self):
    #    a = Account(email='battleshoe@gmail.com',name='battleshoe',payment=0.0,acc_type='normal',shareCount=0)
    #    key = a.put()
    #    self.assertEqual('battleshoe', db.get(key).name)
        
    #def test_setup_entity(self):
    #    a = db.get(self.setup_key)
    #    self.assertEqual('battleshoe', a.name)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()