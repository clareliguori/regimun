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

  $files_to_backup = array();
  array_push($files_to_backup, $password_file_location);
  array_push($files_to_backup, $contact_file_location);
  array_push($files_to_backup, $delegate_list_location);
  array_push($files_to_backup, $optional_event_list_location);
  array_push($files_to_backup, $list_of_committees_location);
  array_push($files_to_backup, $list_of_countries_location);
  array_push($files_to_backup, $school_country_assignments_location);
  array_push($files_to_backup, $country_committee_assignments_location);

  foreach($files_to_backup as $file_name) {
	  $file_lines = read_file($file_name);
	  $backup_file = $backup_data_location . get_filename($file_name) . '.' . date("Ymd");
	  write_file($backup_file, $file_lines);
  }

  echo 'All data has been backed up to '.$backup_data_location.'. <a href="secretariat.php">Return to the main page</a>.';

  include 'footer.php';
}
 ?>
