$(document).ready(function(){

loadCompany('GOOG', null, null, 400, 250);
loadCompany('MSFT', null, null, 400, 250);

function loadCompany(stockSymbol, start, end, width, height) {
	var params = '?'
	params += start != null ? 'start=' + start + '&' : '';
	params += end != null ? 'end=' + end + '&' : '';
	params += width != null ? 'width=' + width + '&' : '';
	params += height != null ? 'height=' + height + '&' : '';

	var url = '/pystocks/demo/diff/' + stockSymbol + params;

	console.log('Before loading');

	$('#content-wrapper').append("<img class='loading-container' src='http://authenticate.hublot.com/interface/img/icons/loading.gif'>")

	var iframe = "<iframe style='display:none' class='async-graph' src='" + url + "'></iframe>"
	$('#content-wrapper').append(iframe);
}


/* Called when iframe content is loaded */
$('.async-graph').load(function() {
  console.log(this);
  var content = this;
  $(content).prev('img').fadeOut('slow', function() {
  	$(content).fadeIn(1000);	
  });
  
});





});
