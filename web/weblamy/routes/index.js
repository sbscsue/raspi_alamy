var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
const fs = require('fs');


var project_path = '/home/pi/project'   /*설정01:git폴더 저장해놓은 폴더로 설정해놓으시오!*/
var file_path = '/raspi_alamy/web/weblamy/public'
var link = [ ['/update_1','/alarm_update_1'], 
             ['/update_2','/alarm_update_2'], 
             ['/update_3','/alarm_update_3']];

function get_setting(number){           
  var path = project_path+file_path+'/alarm'+number+'/setting.json';
  var jsonFile = fs.readFileSync(path); /*의문 filesync / file 뭐가 다름 */
  var jsonData = JSON.parse(jsonFile)
  var jsonToArray = [jsonData.active,jsonData.time];
  return jsonToArray;
}
function set_setting(number,data){
  var path = project_path+file_path+'/alarm'+number+'/setting.json' 
  fileFormat = JSON.stringify(data);
  fs.writeFile(path,fileFormat,'utf8',function(err){
    if(err) {
      console.log("FileSaveErr:"+err);
    }
  })
}
function capture(number){
  var path = project_path+file_path+'/alarm'+number+'/img.jpg'; 
  exec("raspistill -o "+path) /*설정02:파이캠 설정*/
}
/* 기본 알람 홈페이지 접속 */
router.get('/', function(req, res, next) {
  var alarm = [get_setting(1),get_setting(2),get_setting(3)];
  res.render('table', { title: 'Express' ,alarm: alarm});
});


/*첫번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[0][0], function(req, res, next) {
    res.render('form', { number: '1'});
});


/* 알람 변경 값 받기 */
router.post(link[0][1],function(req,res){
  data = req.body
  console.log(data)
  data = {'active': data.active ,'time': data.time}

  set_setting(1,data);
  capture(1);
  
  res.send("보내졌슈");
});

/*두번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[1][0], function(req, res, next) {
    res.render('form', { number: '2'});
});
/* 알람 변경 값 받기 */
router.post(link[1][1],function(req,res){
  data = req.body
  console.log(data)
  data = {'active': data.active ,'time': data.time}

  set_setting(2,data);
  capture(2);
  
  res.send("보내졌슈");
});

/*세번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[2][0], function(req, res, next) {
    res.render('form', { number: '3'});
});
/* 알람 변경 값 받기 */
router.post(link[2][1],function(req,res){
  data = req.body
  console.log(data)
  data = {'active': data.active ,'time': data.time}

  set_setting(3,data);
  capture(3);
  
  res.send("보내졌슈");
});



module.exports = router;
