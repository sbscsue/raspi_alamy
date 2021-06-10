var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
const fs = require('fs');





var project_path = '/home/pi'   /*설정01:git폴더 저장해놓은 폴더로 설정해놓으시오!*/
var file_path = '/raspi_alamy/web/weblamy/public'
var process_path = '/raspi_alamy/main.py'
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

function start_process(){
    var make_process = "python3 "+project_path+process_path
    var alarm = [get_setting(1),get_setting(2),get_setting(3)];
    var instruction =  [make_process+" --number 1"+" --active "+alarm[0][0]+" --time "+alarm[0][1],
                        make_process+" --number 2"+" --active "+alarm[1][0]+" --time "+alarm[1][1],
                        make_process+" --number 3"+" --active "+alarm[2][0]+" --time "+alarm[2][1]]

    exec(instruction[0],(error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
    
    exec(instruction[1],(error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
    exec(instruction[2],(error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
}
function update_process(number,value){
  var make_process = "python3 "+project_path+process_path
  exec(make_process+" --number "+number+" --active "+value[0]+" --time "+value[1],(error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}
function kill_process(number){
  exec(" kill -9 `ps -ef | grep 'python3 /home/pi/raspi_alamy/main.py --number "+number+"' | awk '{print $2}'`",(error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}
/*알람 프로세스 시작*/

start_process()

/* 기본 알람 홈페이지 접속 */
router.get('/', function(req, res, next) {
  var alarm = [get_setting(1),get_setting(2),get_setting(3)];
  res.render('table', { title: 'WEBLAMY' ,alarm: alarm});
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
  alarm = [data.active,data.time]
  kill_process(1)
  update_process(1,alarm)
  set_setting(1,data);
  capture(1);
  
  res.send("전송완료");
 
  
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
  alarm = [data.active,data.time]
  kill_process(2)
  update_process(2,alarm)
  set_setting(2,data);
  capture(2);
  
  res.send("전송완료");
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
  alarm = [data.active,data.time]
  kill_process(3)
  update_process(3,alarm)
  set_setting(3,data);
  capture(3);
  
  res.send("전송완료");
});



module.exports = router;
