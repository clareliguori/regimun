<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_POST['country'])) {
    // Remove selected country
    echo 'This country has been removed! <a href="main.php">Return to the main page</a>!';

    // Find country entries
    $match_string = $_SESSION['school'] . ',' . $_POST['country'];
    $file_lines = read_file($delegate_list_location);
    $new_file_lines = array();
    for($i = 0; $i < sizeof($file_lines); $i++) {
      if (!(begins_with(str_replace('"',"",$file_lines[$i]),$match_string))) {
	array_push($new_file_lines,$file_lines[$i]);
      }
    }

    write_file($delegate_list_location,$new_file_lines);

  } else {
    // Print choose country form
    echo "<h1>Choose a country to remove</h1>";
    echo '<form action="removecountry.php" method="POST">';
    echo '<select name="country">';

    $file_lines = read_file($delegate_list_location);
    $countries = array();
    foreach ($file_lines as $line) {
      $entries = explode(',',$line);
      $school_name = $entries[0];
      $school_name = str_replace('"','',$school_name);
      if($school_name == $_SESSION['school']) {
	$entries = str_replace('"','',$entries);
	array_push($countries,$entries[1]);
      }
    }
    $countries = array_unique($countries);
    sort($countries);
    foreach ($countries as $country) {
      echo '<option>' . $country . '</option>\n';
    }

    echo '</select>';
    echo '<br /><br /><input type="submit" value="Submit"></form>';
    
  }

  include 'footer.php';
}

?>
