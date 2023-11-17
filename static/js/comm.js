jQuery(document).ready(function($){
        $('.list-com').click(function(){ 	
		var post = $(this).data('post'),
			list = $('.list-com');
        $.ajax({
            type: "POST",
            url: gidurl.url,
            data: {   
				security: gidurl.nonce,
                action: 'gid_action',   
                postId: gidurl.postId 
            },
			beforeSend: function(){
				list.fadeOut(500);
			},			
            success: function(res){             
                var j = $("#archi");
                j.html(res);
            },
            error: function(){
                alert('Error!');
            }
        });
        return false;
    });
	});