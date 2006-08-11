<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_POST['sponsor'])) {
    // Print contact info form
    echo "<h1>Edit this sponsor's contact information</h1>";
    echo "Sponsor: " . $_POST['sponsor'] . "<br /><br />";
    $lastname_pos = strrpos($_POST['sponsor']," ");
    $first_name = substr($_POST['sponsor'],0,$lastname_pos);
    $last_name = substr($_POST['sponsor'],$lastname_pos+1);

    // find sponsor's current information
    $match_string = $_SESSION['school'] . ',' . $first_name . ',' . $last_name;
    $file_lines = read_file($contact_file_location);
    for($i = 0; $i < sizeof($file_lines); $i++) {
      if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
	$match_string = $file_lines[$i];
      }
    }
    $match_string = str_replace('"','',$match_string);
    $sponsor_info = explode(",",$match_string);

    echo '<form action="logcontact.php" method="POST">';
    echo '<input type="hidden" name="FirstName" value="' . $first_name . '">';
    echo '<input type="hidden" name="LastName" value="' . $last_name . '">';
    for($i = 3; $i < sizeof($contact_file_columns); $i++) {
      echo $contact_file_columns[$i] . ': <input name="' . str_replace(" ","",$contact_file_columns[$i]) . '" value="' . $sponsor_info[$i] . '"><br /><br />';
    }
    for($i = 0; $i < sizeof($more_contact_file_columns); $i++) {
      echo $more_contact_file_columns[$i] . ': <input name="' . str_replace(" ","",$more_contact_file_columns[$i]) . '"><br /><br />';
    }
    echo '<input type="submit" value="Submit"></form>';
  } else {
    // Print choose sponsor form
    echo "<h1>Choose a sponsor to edit</h1>";
    echo '<form action="editcontact.php" method="POST">';
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
