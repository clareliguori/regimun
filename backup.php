<?php 
include 'lib.php';

function get_filename($fullname) {
  if(strrchr($fullname, "/") != false) {
    return substr(strrchr($fullname, "/"), 1);
  } else {
    return $fullname;
  }
}

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 
  if(!ends_with($backup_data_location,'/')) {
    $backup_data_location .= '/';
  }

  $file_lines = read_file($password_file_location);
  $backup_file = $backup_data_location . get_filename($password_file_location) . '.' . date("Ymd");
  write_file($backup_file, $file_lines);

  $file_lines = read_file($contact_file_location);
  $backup_file = $backup_data_location . get_filename($contact_file_location) . '.' . date("Ymd");
  write_file($backup_file, $file_lines);

  $file_lines = read_file($delegate_list_location);
  $backup_file = $backup_data_location . get_filename($delegate_list_location) . '.' . date("Ymd");
  write_file($backup_file, $file_lines);

  echo 'All data has been backed up to '.$backup_data_location.'. <a href="secretariat.php">Return to the main page</a>.';

  include 'footer.php';
}
 ?>
