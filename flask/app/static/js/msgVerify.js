var InterValObj;
var count = 60;
var curCount;
function sendMessage() {
    curCount = count;
    var data = {}

    data['phone'] = $("#phone").val();
    data['username'] = $("#account").val();
    if(phone != "" && account != ""){
        $("#codeBtn").attr("disabled", "true");
        $("#codeBtn").css({'background-color':'rgba(57, 141, 238, 0.5)'});
        $("#codeBtn").text(curCount + "s");
        InterValObj = window.setInterval(SetRemainTime, 1000);
        console.log(data)
        $.ajax({
            url: "/sendSMS",
            type: "POST",
            data: data,
            error:function(XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
              },
            success: function (msg){
                console.log('success',msg)}  
        });

    }else if(phone == ""){  
        alert("手机号码不能为空！");  
    }else if(account == ""){
    	alert("账户不能为空！");
    }
}
//timer处理函数  
function SetRemainTime() { 
    if (curCount == 0) {   
        window.clearInterval(InterValObj);
        $("#codeBtn").removeAttr("disabled");
        $("#codeBtn").css({'background-color':'transparent'});
        $("#codeBtn").text("发送");
    }  
    else {  
        curCount--;
        $("#codeBtn").text(curCount + "s");  
    }  
}  
