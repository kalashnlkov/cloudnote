WB2.anyWhere(function (W) {
        W.widget.connectButton({
            id: "weiboLogin",
            type: '3,2',
            callback: {
                login: function (o) { //登录后的回调函数
　　　　　　　　　　　　console.log(o);
                    thirdparty(null,null,o.avatar_hd, o.name ,3, o.id);//个人方法
                    try{
                        document.getElementsByClassName('loginout')[0].click();
　　　　　　　　　　　　　　　//页面需求，当前页面登录完成之后，不进行跳转，所以模拟点击事件，让微博账号在当前域中退出。不影响下次登录。（元素为微博动态添加）
　　　　　　　　　　　　　　　//微博没有提供退出方法。下面的logout为另一种开发模式调用。

                    }catch(e){
                        console.log(e);
                    }
                },
                logout: function () { //退出后的回调函数
                }
            }
        });
    });