<?php 
include 'lib.php';

if(check_secretariat_session()) {
  $file_lines = read_file($_GET['filename']);
  echo implode("\n",$file_lines);
}
 ?>
