$(function(){
	$('input').eq(1).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
		}else if($(this).val().length>0 && $(this).val().length<4){
			$(this).parent().next("div").text("长度只能在4-20个字符之间");
			$(this).parent().next("div").css("color",'rgba(255, 0, 0, 0.5)');
		}else{
			/*--------*/
			$(this).parent().next("div").text("");
		}		
	})
	
	$('input').eq(2).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
		}else if($(this).val().length>0 && $(this).val().length<6){
			$(this).parent().next("div").text("长度只能在6-20个字符之间");
			$(this).parent().next("div").css("color",'rgba(255, 0, 0, 0.5)');
		}else{
			$(this).parent().next("div").text("");
		}		
	})

	$('input').eq(3).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
		}else if($(this).val()!=$('input').eq(2).val()){
			$(this).parent().next("div").text("两次密码不匹配");
			$(this).parent().next("div").css("color",'rgba(255, 0, 0, 0.5)');
		}else{
			$(this).parent().next("div").text("");
		}		
	})
	
	$("#submit_btn").click(function(e){		
		for(var j=1 ;j<=10;j++){
			if($('input').eq(j).val().length==0){				
				$('input').eq(j).focus();				
				$('input').eq(j).parent().next(".tips").text("此处不能为空");
				$('input').eq(j).parent().next(".tips").css("color",'rgba(255, 0, 0, 0.5)');	
				e.preventDefault();
				return;
			}			
		}
		if($("#xieyi")[0].checked){

		}else{						
			$("#xieyi").next().next().next(".tips").text("请勾选协议");
			$("#xieyi").next().next().next(".tips").css("color",'rgba(255, 0, 0, 0.5)');
			e.preventDefault();
			return;
		}
	})
	
})