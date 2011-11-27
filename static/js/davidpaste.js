$(document).ready(function(){
	$('#paste_view > h1 > img').click(function() {
		var star = $(this);
		var id = star.attr('_id');
		$.ajax({
			type:'POST',
			url:'/paste/favourite',
			data:'id=' + id,
			dataType:'json',
			success:function(data) {
				if (data['result'] == 'success') {
					if (data['action'] == 'add') {
						star.attr('src', '/static/images/star_on.png');
					} else {
						star.attr('src', '/static/images/star_off.png');
					}
				} else {
                    alert(data['message']);
                }
			}
		});
	});
});
