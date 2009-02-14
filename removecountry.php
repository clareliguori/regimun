<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_GET['country'])) {
    // Remove selected country
    echo '<br>The delegate registrations for this country have been removed! <a href="main.php">Return to the main page</a>!';

    // Find country entries
    $match_string = $_SESSION['school'] . ',' . $_GET['country'];
    $file_lines = read_file($delegate_list_location);
    $new_file_lines = array();
    for($i = 0; $i < sizeof($file_lines); $i++) {
      if (!(begins_with(str_replace('"',"",$file_lines[$i]),$match_string))) {
	array_push($new_file_lines,$file_lines[$i]);
      }
    }

    write_file($delegate_list_location,$new_file_lines);

  }

  include 'footer.php';
}

?>
