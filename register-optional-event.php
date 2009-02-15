<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Print form
  echo '<h1>Register for ' . $optional_event_name . '</h1>';

  $file_lines = read_file($optional_event_list_location);
  $schoolentries = array();
  foreach ($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    if($school_name == $_SESSION['school']) {
	$entries = str_replace('"','',$entries);
	array_push($schoolentries,$entries[1]);
    }
  }

  $count = 0;
  if (sizeof($schoolentries) > 0) {
    $count = $schoolentries[0];
  }

  echo 'Your school has previously registered ' . $count . ' people for the ' . $optional_event_name . '.<br/><br/>';

  echo '<form action="log-optional-event.php" method="POST">';
  echo 'Choose the total number of people who will attend the ' . $optional_event_name . ' from your school:<br/>';

  echo '<select name="optionaleventcount">';

  for($i = 0; $i <= 100; $i++) {
    echo '<option>' . $i . '</option>\n';
  }

  echo '</select><br/><br/>';

  echo '<input type="submit" value="Submit"></form>';

  include 'footer.php';
}

?>
