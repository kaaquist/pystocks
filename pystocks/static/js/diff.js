$(document).ready(function(){

loadCompany('GOOG', null, null);
loadCompany('IBM', null, null);

function loadCompany(stockSymbol, start, end) {
	var params = '?'
	params += start != null ? 'start=' + start + '&' : '';
	params += end != null ? 'end=' + end : '';

	var url = '/demo/diff/' + stockSymbol + params;

	var iframe = "<iframe src='" + url + "'></iframe>"

	$('#content-wrapper').append(iframe);
}





});
