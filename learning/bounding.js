/*
$(document).mousedown(function(e){
	var x,y;
	x = e.pageX;
	y = e.pageY;
	console.log(x + "," + y);
});

$(document).mouseup(function(e){
	var x,y;
	x = e.pageX;
	y = e.pageY;
	console.log(x + "," + y);
});
*/

$(function() {
    var $container = $('#container');
    var $selection = $('<div>').addClass('selection-box');

    $container.on('mousedown', function(e) {
        var click_y = e.pageY;
        var click_x = e.pageX;

        $selection.css({
          'top':    click_y,
          'left':   click_x,
          'width':  0,
          'height': 0
        });
        $selection.appendTo($container);

        $container.on('mousemove', function(e) {
            var move_x = e.pageX,
                move_y = e.pageY,
                width  = Math.abs(move_x - click_x),
                height = Math.abs(move_y - click_y),
                new_x, new_y;

            new_x = (move_x < click_x) ? (click_x - width) : click_x;
            new_y = (move_y < click_y) ? (click_y - height) : click_y;

            $selection.css({
              'width': width,
              'height': height,
              'top': new_y,
              'left': new_x
            });
        }).on('mouseup', function(e) {
            $container.off('mousemove');
            $selection.remove();
        });
    });
});