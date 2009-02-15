<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Process form input
  $_POST = str_replace(array('"',',','\\'),"",$_POST);
  $file_lines = read_file($optional_event_list_location);
  $file_lines = remove_blank_entries($file_lines);

  if($_POST['optionaleventcount'] != "") {
    // school, country, committee, name
    $match_string = '"'.$_SESSION['school'];
    $output_str = $match_string . '","' . $_POST['optionaleventcount'].'"';
    for($i = 0; $i < sizeof($file_lines); $i++) {
	// remove current optional event registration
	if(begins_with(str_replace('"',"",$file_lines[$i]),str_replace('"',"",$match_string))) {
	  array_splice($file_lines, $i, 1);
	}
    }
    array_push($file_lines,$output_str);
  }

  write_file($optional_event_list_location,$file_lines);

  echo "<br/>Your school's registration for the " . $optional_event_name . ' has been saved!  <a href="main.php">Return to the main page</a>!';

  include 'footer.php';
}

?>
