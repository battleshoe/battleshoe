function MainController($xhr,$route){
	var self = this;
	clearChart();
	//auth account
	var success = function(code,response){ //response contains > {"_email": "test", "_money": 1000000.0, "_parent_key": null, "_parent": null, "_entity": {"money": 1000000.0, "email": "test", "networth": 0.0}, "_app": null, "_Model__namespace": "", "_networth": 0.0}
		self.account = response;
		if (self.account.error != undefined){
			alert(self.account.error);
			window.location = "/app/index.html";
		}
	}
	var error = function(code,response){
		alert("There is error retrieving data [PlayerController]")
	}
	$xhr('get','/load_account',success,error)
	
	//load player game
	var loadSuccess = function(code,response){
		self.stats = response;
		if (self.stats.error == "missing islandId"){
			self.islandIdCheck = false;
			//alert(self.stats.error);
		}else{
			self.islandIdCheck = true;
		}
	}
	$xhr('get','/load_player',loadSuccess);
	
	//routing
	$route.when("",{template:"/app/templates/main_content.html"});
	$route.when("/construct",{template:"/app/templates/construction.html", controller:ConstructController});
	$route.when("/theworld",{template:"/app/templates/mainpage.html", controller:IslandController});
	$route.when("/theisland",{template:"/app/templates/theisland.html", controller:RankingController});
	$route.when("/produce",{template:"/app/templates/production.html", controller:ShoeController});
	$route.when("/mycompany",{template:"/app/templates/mycompany.html", controller:CompanyController});
	$route.when("/centralbank",{template:"/app/templates/centralbank.html", controller:CentralBankController})
	$route.when("/jobsmarket",{template:"/app/templates/jobsmarket.html", controller:JobsMarketController})
	$route.parent(this);
}

function IslandController($xhr){
	var self = this;
	clearChart();
	//load all player islands
	var success = function(code, response){
		if (response.error != undefined){
			alert(reponse.error);
			window.location = "/";
		}
		
		self.islands = response; //assign list of islands to array variable
		self.counter = self.islands.length; //assign number of islands
	}
	$xhr('get','/get_all_island',success)
	
	//load account's existing game
	var existSuccess = function(code,response){
		self.existingGames = response;
		self.egcounter = self.existingGames.length
	}
	$xhr('get','/get_account_players',existSuccess);
}

IslandController.prototype = {
	create: function(){
		var islandname = this.islandname,
		nplayer = this.nplayer,
		nplant = this.nplant;
		var link = "/create_island?name="+islandname+"&maxNumOfPlayers="+nplayer+"&maxNumOfPlants="+nplant
		window.location = link;
	}
}

function ConstructController($xhr){
	clearChart();
	var self = this;
	playerId = self.stats.playerId;
	var link = "/retrieve_player_plants?playerId="+playerId;
	
	var success = function(code,response){
		self.plants = response;
	}
	$xhr('get',link,success);
}

ConstructController.prototype = {
	buy_plant: function(plant_region){
		//var plant_region = this.plant_region,
		var playerId = this.stats.playerId,
		islandId = this.stats.islandId,
		link = "/buy_plant?playerId="+playerId+"&islandId="+islandId+"&region="+plant_region;
		window.location = link;
	},
	hire_worker: function(plantId){
		//alert(plantId);
		var num = $("#plantId"+plantId).val();
		link = "/hire_worker?playerId="+this.stats.playerId+"&plantId="+plantId+"&numWorker="+num;
		alert(link);
		window.location = link;
	}
}

function ShoeController($xhr){
	clearChart();
	var self = this;
	var playerId = self.stats.playerId;
	
	//load player's existing plants
	var plantSuccess = function(code,response){
		self.plants = response;
		self.plcounter = self.plants.length
	}
	$xhr('get','/retrieve_player_plants?playerId='+playerId,plantSuccess);
	
	var pastSuccess = function(code,response){
		self.pastProductions = response;
	}
	$xhr('get','/retrieve_past_production?playerId='+playerId,pastSuccess);
	
	//load all player shoe templates
	/*
	var success = function(code, response){
		if (response.error != undefined){
			alert(reponse.error);
			window.location = "/";
		}
		
		self.shoes = response; //assign list of shoes to array variable
		self.counter = self.shoes.length; //assign number of shoes
	}
	$xhr('get','/retrieve_shoe_templates?playerId='+playerId,success)
	*/
}

ShoeController.prototype = {
		produce_shoe: function(){
			var plantId = $('select[name="location"]').val(),
			sole = this.sole,
			body = this.body,
			color = this.color,
			sellprice = this.sellprice
			qty= this.qty,
			playerId = this.stats.playerId;
			
			var link = "/manufacture_shoe?playerId="+playerId+"&plantId="+plantId+"&sole="+sole+"&body="+body+"&color="+color
						+"&sellprice="+sellprice+"&qty="+qty;
			//alert(link);
			window.location = link;
		}
		/*
		_produce_shoe: function(plantId,shoeId){
			var number = $('input[name="number'+shoeId+'"]').val();
			var playerId = this.stats.playerId;
			var link = "/manufacture_shoe?playerId="+playerId+"&plantId="+plantId+"&shoeId="+shoeId+"&qty="+number;
			//alert(link);
			window.location = link;
		},
		create_shoe: function(){
			plantId = $('select[name="plantId"]').val();
			link = "/create_shoe?plantId="+plantId+"&sole="+this.sole+"&body="+this.body+"&color="+this.color+"&price="+this.price;
			window.location = link;
		}
		*/
}

function CentralBankController($xhr){
	clearChart();
	var self = this;
	//load account's existing game
	var existSuccess = function(code,response){
		self.existingGames = response;
	}
	$xhr('get','/get_account_players',existSuccess);
}

CentralBankController.prototype = {
	buy : function(a){
		var one = "0.99",two="1.99",three="2.99",amt="0",mone=1000000,mtwo=5000000,mthree=10000000,money="0";
		var playerId = $('select[name="'+a+'"]').val();
		if(a == "p099") {amt = one; money = mone;}
		if(a == "p199") {amt = two; money = mtwo;}
		if(a == "p299") {amt = three; money = mthree;}
		var args = playerId+","+money+","+amt
		var ppLink = "http://www.dotcom.sg/cloud/paypal/checkout.php?item="+a+"&amount="+amt+"&return=http://www.battleshoe.appspot.com/buy_credits?details="+args+"&cancel=http://www.battleshoe.appspot.com/buy_credits_fail?details="+args;
		//alert(ppLink);
		//$("#scratchbox").html(ppLink);
		window.location = ppLink;
	}
}

function JobsMarketController($xhr){
	clearChart();
	var self = this;
	var playerId = self.stats.playerId;
	
	var plantSuccess = function(code,response){
		self.hirePlants = response;
	}
	$xhr('get','/retrieve_player_plants?playerId='+playerId,plantSuccess);
}

JobsMarketController.prototype = {
	hire: function(){
		var playerId = this.stats.playerId;
		var numHire = $('input[name="numHire"]').val();
		var plantId = $('select[name="hireLocation"]').val();
		var link = "/hire_worker?numWorker="+numHire+"&plantId="+plantId+"&playerId="+playerId;
		window.location = link;
	}
}

function RankingController($xhr){
	clearChart();
	var self = this;
	$xhr('get','/island_ranking',function(code,response){
		self.ranking = response;
		//alert(self.ranking.length);
	});
}

function CompanyController($xhr){
	var self = this;
	var playerId = self.stats.playerId;
	$xhr('get','/demand_supply?playerId='+playerId, function(code,response){
		self.supply = response.supply;
		self.demand = response.demand;
		var supplyArray = new Array();
		var demandArray = new Array();
		//alert(self.supply);
		for(var i = 0 ; i < self.supply.length; i++){
			var s = self.supply[i];
			var a = new Array();
			a.push(s.salePrice);
			a.push(s.qty);
			supplyArray.push(a);
		}
		for(var i = 0 ; i < self.demand.length; i++){
			var d = self.demand[i];
			var a = new Array();
			a.push(d.salePrice);
			a.push(d.qty);
			demandArray.push(a);
		}
		var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];
		var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]]; //style="width:500px; height:500px"
		$("#scratchbox").css("width","500px");
		$("#scratchbox").css("height","500px");
		$.plot($("#scratchbox"),[
		       {data:supplyArray, label:"Supply"},
		       {data:demandArray, label:"Demand"},
		       {series:{
		    	   lines:{show:true},
		    	   points:{show:true}
		       		}
		       }
		]);
	});
}

function clearChart(){
	$("#scratchbox").html("");
	$("#scratchbox").css("height","0px");
}



