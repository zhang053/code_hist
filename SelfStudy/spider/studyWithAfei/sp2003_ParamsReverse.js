// 参数逆向

var crypto = require("crypto")
var u = {a:crypto}

function fn(t){
    var e = "293643"   //音频id
    // var t = "29413300"  //表示某一集
    // var s = /audiostream/redirect/" + e + "/" + t + (o.a.stringify(a) && "?" + o.a.stringify(a));
    var s = `/audiostream/redirect/${e}/${t}?access_token=&device_id=MOBILESITE&qingting_id=&t=${Date.now()}`
    var sign = u.a.createHmac("md5", "7l8CZ)SgZgM_bkrw").update(s).digest("hex").toString()
    return "https://audio.qtfm.cn" + s + "&sign=" + sign
}

t = process.argv[2]
url = fn(t)
console.log(url)