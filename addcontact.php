<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Print form
  echo '<h1>Add a sponsor to your contact list</h1>';
  echo '<form action="logcontact.php" method="POST">';
  for($i = 1; $i < sizeof($contact_file_columns); $i++) {
    echo $contact_file_columns[$i] . ': <input name="' . str_replace(" ","",$contact_file_columns[$i]) . '"><br /><br />';
  }
  for($i = 0; $i < sizeof($more_contact_file_columns); $i++) {
    echo $more_contact_file_columns[$i] . ': <input name="' . str_replace(" ","",$more_contact_file_columns[$i]) . '"><br /><br />';
  }
  echo '<input type="submit" value="Submit"></form>';

  include 'footer.php';
}

?>
