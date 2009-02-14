<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_GET['country']) && isset($_GET['committee']) && isset($_GET['delegate'])) {
    // Remove selected delegate
    echo '<br>This delegate registration has been removed! <a href="main.php">Return to the main page</a>!';

    // Find country entries
    $match_string = $_SESSION['school'] . ',' . $_GET['country'] . ',' . $_GET['committee'] . ',' . $_GET['delegate'];
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
