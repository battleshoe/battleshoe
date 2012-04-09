/* jasmine-like end2end tests go here */

	
  describe('The world', function() {
	beforeEach(function() {
		browser().navigateTo('/login');
		
	});
	
    it('should display 0 island and 0 game', function() {
    	browser().navigateTo('../../app/main.html#/theworld');
    	
    	expect(repeater('.link-list1 tr').count()).toBe(1);
    	expect(binding('stats.money')).toBe("");
    	expect(binding('stats.numPlants')).toBe("");
    	expect(binding('stats.numWorkers')).toBe("");
    	expect(binding('stats.numShoes')).toBe("");
    	
    	expect(repeater('.link-list2 tr').count()).toBe(1);
    });
    it('create one island and should display no existing game but one available island to join', function() {	
    	input('islandname').enter('hahais');
    	input('nplayer').enter('50');
    	input('nplant').enter('100');   	
    	element('.link-list3 :button').click();
    	
    	browser().navigateTo('../../app/main.html#/theworld');
    	expect(repeater('.link-list1 tr').count()).toBe(1);
    	expect(repeater('.link-list2 tr').count()).toBe(2);
  
    	expect(repeater('.link-list2 tr').column('a')).
         toEqual(["hahais","0","50","100"]);
    });
    it('start playing and should display game stats', function() {
    	element('#link1').click();
    	
    	//check existing games
    	browser().navigateTo('../../app/main.html#/theworld');
    	expect(repeater('.link-list1 tr').count()).toBe(2);
    	expect(repeater('.link-list2 tr').count()).toBe(2);
    	//check money, factories, works, shoes 1000000,0,0,0
    	expect(binding('stats.money')).toBe("1000000");
    	expect(binding('stats.numPlants')).toBe("0");
    	expect(binding('stats.numWorkers')).toBe("0");
    	expect(binding('stats.numShoes')).toBe("0");
    });
    it('build 2 factories and should display updated number of factories and money', function() {
    	//build factory North 
    	browser().navigateTo('../../app/main.html#/construct');
    	element('#north').click();
    	//check money, factories, works, shoes  900000,1,0,0
    	//browser().navigateTo('../../app/main.html#/theworld');
    	expect(binding('stats.money')).toBe("800000");
    	expect(binding('stats.numPlants')).toBe("2");
    	expect(binding('stats.numWorkers')).toBe("0");
    	expect(binding('stats.numShoes')).toBe("0");
    });
    it('hire 100 workers and should display updated money and number of workers', function() {
    	//hire workers 100
    	browser().navigateTo('../../app/main.html#/jobsmarket');
    	select('hireLocation').option('Factory 4 (north)');
    	input('numHire').enter('100');
    	element('#hiring').click();
    	//check money, factories, works, shoes 400000,1,100,0
    	browser().navigateTo('../../app/main.html');
    	expect(binding('stats.money')).toBe("300000");
    	expect(binding('stats.numPlants')).toBe("2");
    	expect(binding('stats.numWorkers')).toBe("100");
    	expect(binding('stats.numShoes')).toBe("0");
    });
    it('manufacture 200 shoes and should display updated money and number of shose', function() {
    	//produce shoe 50,100,10,10,10
    	browser().navigateTo('../../app/main.html#/produce');
    	select('location').option('Factory 4');
    	input('sellprice').enter('50');
    	input('qty').enter('100');
    	input('sole').enter('10');
    	input('body').enter('10');
    	input('color').enter('10');
    	element('#produce').click();
    	//check money, factories, works, shoes 399850,1,100,100
    	browser().navigateTo('../../app/main.html');
    	expect(binding('stats.money')).toBe("299700");
    	expect(binding('stats.numPlants')).toBe("2");
    	expect(binding('stats.numWorkers')).toBe("100");
    	expect(binding('stats.numShoes')).toBe("200");
    	
    }); 
    it('should display one player only and corresponding stats', function() {
    	//check ranking and money, factories, workers, shoes
    	browser().navigateTo('../../app/main.html#/theisland');
    	expect(repeater('#ranking tr').count()).toBe(2);
    	//check money, factories, works, shoes 399850,1,100,100
    	expect(binding('player.money')).toBe("299700");
    	expect(binding('player.numPlants')).toBe("2");
    	expect(binding('player.numWorkers')).toBe("100");
    	expect(binding('player.numShoes')).toBe("200");
    	expect(binding('player.networth')).toBe("1000000");
    });
    
    
  });
  
  

