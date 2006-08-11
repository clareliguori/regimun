<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_POST['country'])) {
    // Print country delegate form
    echo "<h1>Edit this country's delegate list</h1>";
    echo '<form action="logcountry.php" method="POST">';
    echo '<input type="hidden" name="country" value="' . $_POST['country'] . '">';
    echo "<h3>Country</h3>";
    echo $_POST['country'] . '<br /><br />';

    echo '<h3>Delegates (First and Last Name):</h3>';
    echo 'If you do not have a delegate in a certain committee, leave the box blank.<br /><br />';

    foreach($committees as $committee) {
      // find delegate's current information
      $found_string = "";
      $match_string = '"'.$_SESSION['school'].'","'.$_POST['country'].'","'.$committee;
      $output_str = $match_string . '","' . $_POST[str_replace(" ","",$committee)].'"';
      $file_lines = read_file($delegate_list_location);
      for($i = 0; $i < sizeof($file_lines); $i++) {
	// find current delegate information
	if(begins_with(str_replace('"',"",$file_lines[$i]),str_replace('"',"",$match_string))) {
	  $found_string = $file_lines[$i];
	}
      }
      echo $committee . ':<br /><input name="' . str_replace(" ","",$committee) . '" size="50" ';
      if($found_string != "") {
	$found_string = str_replace('"','',$found_string);
	$delegate_info = explode(",",$found_string);
	echo 'value="' . $delegate_info[3] . '"';
      }
      echo "><br /><br />\n";
    }
    echo '<input type="submit" value="Submit"></form>';
  } else {
    // Print choose country form
    echo "<h1>Choose a country to edit</h1>";
    echo '<form action="editcountry.php" method="POST">';
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
