
$(document).ready(function() {
	mocha.setup('bdd');

	var expect = chai.expect;
	var array = [3,8,2,0,7,8];

	var inTitle = "my title";
	var outTitle = "My title";
	var slugTitle = "my-title";
    var outSrrSort = ["apple", "orange", "banana", "strawberry"];
	
    
    var tmstmp = 1503623508;
    var outTmstmp = "01:11:48";
    
    var ahrf = `<a
                class="resource-link"
                href="/mylink/"
                data-method="GET"
                data-schema-url=""
            >my title</a>`;
    
	const $containerControls = $('.container.controls');
	const $contentData   = $('.content-data');
	const $controlsData  = $('.controls-data');

	describe('testing init', function() {
		it('really runs', function() {
		expect(0).to.equal(0);
	  });
	});

	describe('formatTitle testing', function(){
		it('returns the formatted title', function(){
			var output = formatTitle(inTitle);
			expect(output).to.equal(outTitle);
		});
	});

    
    describe('slugify testing', function(){
		it('returns the slug of a given text', function(){
			var output = sluggify(inTitle);
			expect(output).to.equal(slugTitle);
		});
	});
    
    
    describe('array sort testing', function(){
		it('returns the sorted array', function(){
			var arlene = new Array("orange","apple","strawberry","banana");
            var output = arlene.sort(customSort);
			expect(output[0]).to.equal(outSrrSort[0]);
		});
	});
    
    describe('getCurrentHash function test', function(){
		it('returns the sorted array', function(){
			var output = getCurrentHash();
			expect(output).to.equal("");
		});
	});
    
    describe('currentLink function test', function(){
		it('returns an HTML a tag', function(){
			var output = createLink("/mylink/", "my title");
			expect(output).to.equal(ahrf);
		});
	});
    
    describe('check time function test', function(){
		it('returns the time from a timestamp', function(){
			var output = time(tmstmp);
			expect(output).to.equal(outTmstmp);
		});
	});
    
	mocha.run();

});