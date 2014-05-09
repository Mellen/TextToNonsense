var canvas = document.getElementById('pic');
var context = canvas.getContext('2d');
var maxPixel = 810000;
var currentIndex = 0;

var socket = new WebSocket('ws://'+location.host+'/ws')

socket.onopen = function(){jQuery('#message').text('socket open');};

socket.onmessage = function(message)
{
    data = jQuery.parseJSON(message.data);
    updatePicture(data);
    jQuery('#message').text(data.text);
};

jQuery('#btnSubmit').click(function (e)
			   {
			       var result = jQuery.post('analyse', {'text':jQuery('#txtInput').val()}, 
							success = function(data, status, xhr)
							{
							    jQuery('#message').text(data.text);
							    
							    jQuery('#txtInput').val('');
							}, 
							'json');
			       result.fail(function(e)
					   {
					       jQuery('#message').text('Failure: ' + e.status + ' ' + e.statusText);
					   });
			   });

jQuery('form').submit(function (e)
		      {
			  jQuery('#btnSubmit').click();
			  e.cancelBubble = true;
			  e.returnValue = false;
			  return false;
		      });

function updatePicture(data)
{
    var picture = context.getImageData(0,0,900,900);
    var index = Math.floor(currentIndex + 36*data.ratio);
    currentIndex = index;
    if(index >= maxPixel)
    {
	index = index - maxPixel;
    }
    
    var position = index*4;
    
    for(var colourIndex in data.colours)
    {
	picture.data[position] = data.colours[colourIndex][0];
	picture.data[position+1] = data.colours[colourIndex][1];
	picture.data[position+2] = data.colours[colourIndex][2];
	picture.data[position+3] = 255;

	index++;
	if(index >= maxPixel)
	{
	    index = index - maxPixel;
	}
	position = index * 4;
    }

    context.putImageData(picture, 0,0);
}