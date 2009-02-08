<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Process form input
  $_POST = str_replace(array('"',',','\\'),"",$_POST);
  $file_lines = read_file($delegate_list_location);
  $file_lines = remove_blank_entries($file_lines);

  $committees = read_file($list_of_committees_location);
  foreach($committees as $committee) {
    if($_POST[str_replace(" ","",$committee)] != "") {
      // school, country, committee, name
      $match_string = '"'.$_SESSION['school'].'","'.$_POST['country'].'","'.$committee;
      $output_str = $match_string . '","' . $_POST[str_replace(" ","",$committee)].'"';
      for($i = 0; $i < sizeof($file_lines); $i++) {
	// remove current delegate entry
	if(begins_with(str_replace('"',"",$file_lines[$i]),str_replace('"',"",$match_string))) {
	  array_splice($file_lines, $i, 1);
	}
      }
      array_push($file_lines,$output_str);
    }
  }
  write_file($delegate_list_location,$file_lines);

  echo 'The delegate information has been saved!  <a href="main.php">Return to the main page</a>!';

  include 'footer.php';
}

?>
