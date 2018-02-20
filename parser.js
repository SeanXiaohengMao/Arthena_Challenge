
var fs = require("fs")
var readline = require('readline')
var dirname ='data/2017-12-20/'

var files = fs.readdirSync('data/2017-12-20/')

fs.readdir(dirname, function(err, files) {
	if (err) {
		       return console.error(err);
		   }

	/* 
	* Define 2 object to save the data,
	* obj_list is the output JSON array,
	* obj_index saves the index of the artist in the obj_list.
	**/
	var obj_list = [];
	var obj_index = {};
	var index = 0;

	/*
	* Parse the html documents,
	* open the documents in the loop.
	**/
	const htmlFiles = files.filter(el => /\.html$/.test(el))
  	htmlFiles.forEach(file => 
  	{
    	var lines = require('fs').readFileSync(dirname+file, 'utf-8').split('\n');

    	var num = 1;
    	var artist, title, value, currency, amount;

    	/* search line by line */
    	lines.some(line => 
    	{
    		/* search the artist name in a html file */
			if (num == 1) 
			{
				reobj = /<h3 class='artist'>(.*?)( \(.*\))*<\/h3>/.exec(line);
				if (reobj) 
				{
					artist = '\''+reobj[1]+'\''
					/* initialize the object of the artist */
					if (!obj_index.hasOwnProperty(artist)) 
					{
						/* the artist's works are saved as a list */
						obj_list.push( {'artist': artist, 'totalValue': 0, 'works':[]} );
						/* saved the artist's index */
						obj_index[artist] = index;
						index++;
					}
					num++;
				}
			}
				

			/* search the title of the work in a html file */
			else if (num == 2) 
			{
				reobj = /<h3>(.*?)<\/h3>/.exec(line);
				if (reobj) 
				{
					title = '\''+reobj[1]+'\'';
					num++; 
				}
			}

			/* 
			* search the price of the work in a html file,
			* each work is saved as a object
			**/
			else if (num == 3) 
			{
				reobj = /<div><span class='currency'>(.*?)<\/span><span>(.*?)<\/span><\/div>/.exec(line);
				if (reobj) 
				{
					currency = '\''+reobj[1]+'\'';
					amount = '\''+reobj[2]+'\'';
					/* convert string to integer */
					value = parseInt(reobj[2].replace(/,/g, ''));	
					/* convert GBP to USD */
					if (currency == '\'GBP\'')	
					{
						value *= 1.34;
						currency = '\'USD\'';
					}
					/* calculate the totalValue */
					obj_list[obj_index[artist]].totalValue += value; 
					obj_list[obj_index[artist]].works.push({'title': title, 'currency': currency, 'amount': amount}) 
				}
			}
			return num === 4;
		});
  	});

  	/*
  	* Print the JSON array in the console.
  	* Structure the results into the format.
  	**/
  	obj_list.forEach(el => 
  	{
  		var value = el.totalValue.toLocaleString();
  		var value_string = '\'USD ' + value + '\'';
  		el.totalValue = value_string;
  	})
  	str = JSON.stringify(obj_list, null, 4);
	console.log(str.replace(/\"/g, ""));
})