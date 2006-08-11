<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Process form input
  $_POST = str_replace(array('"',',','\\'),"",$_POST);
  $file_lines = read_file($contact_file_location);
  $file_lines = remove_blank_entries($file_lines);
  $_POST['LastName'] = str_replace(" ","",$_POST['LastName']);

  $output_str = '"' . $_SESSION['school'] . '",';
  for($i = 1; $i < sizeof($contact_file_columns); $i++) {
    $output_str .= '"' . $_POST[str_replace(" ","",$contact_file_columns[$i])].'",';
  }
  for($i = 0; $i < sizeof($more_contact_file_columns); $i++) {
    $output_str .= '"' . $_POST[str_replace(" ","",$more_contact_file_columns[$i])].'",';
  }
  $output_str = substr($output_str,0,strrpos($output_str,","));

  $match_string = $_SESSION['school'] . ',' . $_POST['FirstName'] . ',' . $_POST['LastName'];
  for($i = 0; $i < sizeof($file_lines); $i++) {
    // remove sponsor's current entry
    if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
      array_splice($file_lines, $i, 1);
    }
  }
  array_push($file_lines,$output_str);

  write_file($contact_file_location,$file_lines);

  echo 'The contact information has been saved!  <a href="main.php">Return to the main page</a>!';

  include 'footer.php';
}

?>
