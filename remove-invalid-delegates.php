<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 

  echo '<br>All invalid delegate registrations have been removed! <a href="secretariat.php">Return to the secretariat dashboard</a>!';

// Get the list of schools
  $file_lines = read_file($password_file_location);
  $school_list = array();
  foreach($file_lines as $line) {
	  $entries = explode('","',$line);
	  $entries[0] = str_replace('"','',$entries[0]);
	  array_push($school_list, $entries[0]);
  }

// Get the country-committee assignments
  $file_lines = read_file($country_committee_assignments_location);
  $country_committee_assignments = array();
  foreach($file_lines as $line) {
	  $entries = explode('","',$line);
	  $entries[0] = str_replace('"','',$entries[0]);
	  $entries[count($entries) - 1] = str_replace('"','',$entries[count($entries) - 1]);
	  $country_committee_assignments[$entries[0]] = array_slice($entries, 1);
  }

// Get the school-country assignments
  $file_lines = read_file($school_country_assignments_location);
  $country_school_assignments = array();
  foreach($file_lines as $line) {
	  $entries = explode('","',$line);
	  $entries[0] = str_replace('"','',$entries[0]);
	  $entries[1] = str_replace('"','',$entries[1]);
	  $country_school_assignments[$entries[0]] = $entries[1];
  }

  // Get the delegate list and verify each registration
  $file_lines = read_file($delegate_list_location);
  $file_lines = remove_blank_entries($file_lines);
  sort($file_lines);
  $new_file_lines = array();

  foreach($file_lines as $line) {
	  $entries = explode('","',$line);
	  $entries[0] = str_replace('"','',$entries[0]);
	  $entries[count($entries) - 1] = str_replace('"','',$entries[count($entries) - 1]);
	 
	  $school_name = $entries[0];
	  $country_name = $entries[1];
	  $committee_name = $entries[2];
	  $delegate_name = $entries[3];

	  // Check the school account
	  if(array_search($school_name, $school_list) !== FALSE) {
		  // Check the school-country assignment
		  if($country_school_assignments[$country_name] == $school_name) {
			  // Check the country-committee assignment
			  if(count($country_committee_assignments[$country_name]) > 0 && array_search($committee_name, $country_committee_assignments[$country_name]) !== FALSE) {
				  array_push($new_file_lines,$line);
			  }
		  }
	  }
  }

  write_file($delegate_list_location,$new_file_lines);
  
  include 'footer.php';
}
 ?>
