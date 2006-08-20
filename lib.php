<?php

function read_file($file_path) {
  if(file_exists($file_path) && filesize($file_path) > 0) {
    $fh = fopen($file_path, 'r');
    $file_data = fread($fh, filesize($file_path));
    fclose($fh);
    return explode("\n",$file_data);
  } else {
    return array();
  }
}

function write_file($file_path,$line_array) {
  $created = false;
  if(!file_exists($file_path)) {
    $created = true;
  }
  $fh = fopen($file_path, 'w');
  $lines_string = implode("\n",$line_array);
  fwrite($fh, $lines_string);
  fclose($fh);
  if($created) {
    chmod($file_path,0777);
  }
}

function remove_file($file_path) {
  if(file_exists($file_path)) {
    unlink($file_path);
  }
}

function remove_blank_entries($arr) {
  for($i = 0; $i < sizeof($arr); $i++) {
    if(trim($arr[$i]) == "") {
      array_splice($arr, $i, 1);
    }
  }
  return $arr;
}

function begins_with( $str, $sub ) {
   return ( substr( $str, 0, strlen( $sub ) ) === $sub );
}
function ends_with( $str, $sub ) {
   return ( substr( $str, strlen( $str ) - strlen( $sub ) ) === $sub );
}

function display_page($output) {
  include 'header.php';
  echo $output;
  include 'footer.php';
}

function check_password($name, $password) {
  include 'config.php';
  $password_match = false;

  $fh = fopen($password_file_location, 'r');
  $file_data = fread($fh, filesize($password_file_location));
  fclose($fh);

  $file_lines = explode("\n",$file_data);
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    $school_passwd = $entries[1];
    $school_passwd = str_replace('"','',$school_passwd);
    if(($name == $school_name) &&($password == $school_passwd)) {
      $password_match = true;
    }
  }
  return $password_match;
}

function check_session() {
  if(isset($_POST['schoolname']) && isset($_POST['schoolpasswd'])) {
    if(check_password($_POST['schoolname'],$_POST['schoolpasswd'])){
      session_start();
      $_SESSION['school'] = $_POST['schoolname'];
      $_SESSION['password'] = $_POST['schoolpasswd'];
      return true;
    } else {
      display_page("Incorrect password.  <a href=\"index.php\">Please try again.</a>");
    }
  } else if(isset($_POST['schoolname'])){
    session_start();
    if(check_secretariat_session()) {
      $_SESSION['school'] = $_POST['schoolname'];
      return true;
    }
  } else {
    session_start();
    if(isset($_SESSION['school'])) {
      return true;
    } else {
      echo display_page("Error: <a href=\"index.php\">Click here to log in.</a>");
    }
  }
  return false;
}

function check_secretariat_session() {
  include 'config.php';
  if(isset($_POST['secretariatpassword'])) {
    if($_POST['secretariatpassword'] == $secretariat_password){
      session_start();
      $_SESSION['secretariat'] = "yes";
      return true;
    }
  } else {
    session_start();
    if(isset($_SESSION['secretariat']) && $_SESSION['secretariat'] == "yes") {
      return true;
    }
  }
  return false;
}

?>
