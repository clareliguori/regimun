<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_POST['sponsor'])) {
    // Remove selected sponsor
    echo 'This sponsor has been removed! <a href="main.php">Return to the main page</a>!';
    $lastname_pos = strrpos($_POST['sponsor']," ");
    $first_name = substr($_POST['sponsor'],0,$lastname_pos);
    $last_name = substr($_POST['sponsor'],$lastname_pos+1);

    // find sponsor's current information
    $match_string = $_SESSION['school'] . ',' . $first_name . ',' . $last_name;
    $file_lines = read_file($contact_file_location);
    for($i = 0; $i < sizeof($file_lines); $i++) {
      if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
	array_splice($file_lines, $i, 1);
      }
    }

    write_file($contact_file_location,$file_lines);
  } else {
    // Print choose sponsor form
    echo "<h1>Choose a sponsor to remove</h1>";
    echo '<form action="removecontact.php" method="POST">';
    echo '<select name="sponsor">';

    $file_lines = read_file($contact_file_location);
    foreach ($file_lines as $line) {
      $entries = explode(',',$line);
      $school_name = $entries[0];
      $school_name = str_replace('"','',$school_name);
      if($school_name == $_SESSION['school']) {
	$entries = str_replace('"','',$entries);
	echo "<option>" . $entries[1] . " " . $entries[2] . "</option>";
      }
    }

    echo '</select>';
    echo '<br /><br /><input type="submit" value="Submit"></form>';
    
  }

  include 'footer.php';
}

?>
