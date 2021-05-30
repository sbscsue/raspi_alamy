var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;


const fs = require('fs');

var project_path = '/home/pi/project'   /*설정01:git폴더 저장해놓은 폴더로 설정해놓으시오!*/
var file_path = '/raspi_alamy/web/weblamy/public'
var link = [ ['/update_1','/alarm_update_1'], 
             ['/update_2','/alarm_update_2'], 
             ['/update_3','/alarm_update_3'], 
             ['/update_4','/alarm_update_4'], 
             ['/update_5','/alarm_update_5']];
/* 기본 알람 홈페이지 접속 */
router.get('/', function(req, res, next) {
  res.render('table', { title: 'Express' });
});


/*첫번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[0][0], function(req, res, next) {
    res.render('form', { number: '1'});
});


/* 알람 변경 값 받기 */
router.post(link[0][1],function(req,res){
  var path = project_path+file_path+'/alarm1'
  var setting_path = path + '/setting.json' 
  var img_path = path + '/img.jpg'
  
  /*코드 줄이기*/
  data = req.body
  console.log(data)
  data = {'active': data.active ,'time': data.time}
  fileFormat = JSON.stringify(data);
  fs.writeFile(setting_path,fileFormat,'utf8',function(err){
    console.log("FileSaveErr:"+err)
  })

  exec("raspistill -o "+img_path) /*설정02:파이캠 설정*/
  
  res.send("보내졌슈");
});

/*두번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[1][0], function(req, res, next) {
    res.render('form', { number: '2'});
});
/* 알람 변경 값 받기 */
router.post(link[1][1],function(req,res){
  console.log(req.body)
  data = {'확인용':"dfdfdfda"}
  fileFormat = JSON.stringify(data);
  fs.writeFile(file_path,fileFormat,'utf8',function(err){
    console.log(err)
  })
  res.send("보내졌슈");
});

/*세번째 알람*/
/* 알람 변경 홈페이지 접속 */
router.get(link[2][0], function(req, res, next) {
    res.render('form', { number: '3'});
});
/* 알람 변경 값 받기 */
router.post(link[2][1],function(req,res){
  console.log(req.body)
  data = {'확인용':"dfdfdfda"}
  fileFormat = JSON.stringify(data);
  fs.writeFile(file_path,fileFormat,'utf8',function(err){
    console.log(err)
  })
  res.send("보내졌슈");
});



module.exports = router;
