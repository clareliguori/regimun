<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_GET['country']) && isset($_GET['committee']) && isset($_GET['delegate'])) {
    // Remove selected delegate
	  $school_name = "";
	  if(isset($_GET['school'])) {
		  $school_name = $_GET['school'];
	  } else {
		  $school_name = $_SESSION['school'];
	  }

	  if(check_secretariat_session()) {
		  echo '<br>This delegate registration has been removed! <a href="secretariat.php">Return to the secretariat dashboard page</a>!';
	  } else {
		  echo '<br>This delegate registration has been removed! <a href="main.php">Return to the main page</a>!';
	  }

    // Find country entries
    $match_string = $school_name . ',' . $_GET['country'] . ',' . $_GET['committee'] . ',' . $_GET['delegate'];
    $file_lines = read_file($delegate_list_location);
    $new_file_lines = array();
    for($i = 0; $i < sizeof($file_lines); $i++) {
      if (strcmp(str_replace('"',"",$file_lines[$i]),$match_string) != 0) {
	array_push($new_file_lines,$file_lines[$i]);
      }
    }

    write_file($delegate_list_location,$new_file_lines);

  }

  include 'footer.php';
}

?>
