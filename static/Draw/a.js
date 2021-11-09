				$(function(){
					var a=($('#front').width()/2)+$('#rear').width()-5;
					var b=($('#rear').width()/2)+$('#front').width();
					$('#front').css({
						'margin-left':'-'+a+'px',
					});
					$('#rear').css('margin-right','-'+b+'px');
				})
