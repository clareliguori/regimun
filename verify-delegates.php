<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 

  echo "<h1>Verify delegate registrations</h1>";
  echo "This page checks the following for all delegate registrations:<ul>";
  echo "<li>The country is assigned to the school</li>";
  echo "<li>The committee is assigned to the country</li>";
  echo "<li>The school has an account in the system</li>";
  echo "</ul>";

  echo '<a href="remove-invalid-delegates.php">Remove all invalid delegate registrations</a><hr>';

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
  $current_school = "";
  foreach($file_lines as $line) {
	  $entries = explode('","',$line);
	  $entries[0] = str_replace('"','',$entries[0]);
	  $entries[count($entries) - 1] = str_replace('"','',$entries[count($entries) - 1]);
	 
	  $school_name = $entries[0];
	  $country_name = $entries[1];
	  $committee_name = $entries[2];
	  $delegate_name = $entries[3];

	  if($current_school != $school_name) {
		  echo '<br/><b>' . $school_name . '</b><br/>';
		  $current_school = $school_name;
	  }

	  // Check the school account
	  if(array_search($school_name, $school_list) === FALSE) {
		  echo $delegate_name . ": School (" . $school_name . ") does not have an account) ";
		  echo '<small><a href="removedelegate.php?school='.$school_name.'&country='.$country_name.'&committee='.$committee_name.'&delegate='.$delegate_name.'">(Delete)</a></small><br/>';
		  // Check the school-country assignment
	  } else if($country_school_assignments[$country_name] != $school_name) {
		  echo $delegate_name . ": School (" . $school_name . ") is not assigned the country (" . $country_name . ") ";
		  echo '<small><a href="removedelegate.php?school='.$school_name.'&country='.$country_name.'&committee='.$committee_name.'&delegate='.$delegate_name.'">(Delete)</a></small><br/>';
		  // Check the country-committee assignment
	  } else if(count($country_committee_assignments[$country_name]) < 1 || array_search($committee_name, $country_committee_assignments[$country_name]) === FALSE) {
		  echo $delegate_name . ": Committee (" . $committee_name . ") is not assigned to the country (" . $country_name . ") ";
		  echo '<small><a href="removedelegate.php?school='.$school_name.'&country='.$country_name.'&committee='.$committee_name.'&delegate='.$delegate_name.'">(Delete)</a></small><br/>';
	  }
  }
  
  include 'footer.php';
}
 ?>
