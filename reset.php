<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 

  if(isset($_GET['type'])) {
    // confirm reset
    if($_GET['type'] == "full") {
      echo 'Performing a full system reset will remove all schools, sponsor contacts, and delegates from the system.  You cannot get these back!';
    } elseif($_GET['type'] == "delegates") {
      echo 'Removing all delegates will delete the registered delegates spreadsheet.  You cannot get these back!';
    } elseif($_GET['type'] == "school" && isset($_POST['schoolname'])) {
      echo 'Removing ' . $_POST['schoolname'] . ' will remove all sponsor contacts and registered delegates for this school.  You cannot get these back!';
    }

    echo '<br><br>Are you sure you want perform this action?';
    echo '<form method="post" action="reset.php">';
    echo '<input type="hidden" name="type" value="'.$_GET['type'].'">';
    if($_GET['type'] == "school" && isset($_POST['schoolname'])) {
      echo '<input type="hidden" name="school" value="'.$_POST['schoolname'].'">';
    }
    echo '<input TYPE="submit" value="Yes">';
    echo '</form>';

  } else {
    // do reset
    if($_POST['type'] == "full") {
      remove_file($password_file_location);
      remove_file($contact_file_location);
      remove_file($delegate_list_location);
      remove_file($optional_event_list_location);
      remove_file($school_country_assignments_location);
      remove_file($country_committee_assignments_location);
      echo 'Your system has been fully reset!  <a href="secretariat.php">Return to the main page</a>.';
    } elseif($_POST['type'] == "delegates") {
      remove_file($delegate_list_location);
      remove_file($optional_event_list_location);
      echo 'All delegates have been removed!  <a href="secretariat.php">Return to the main page</a>.';
    } elseif($_POST['type'] == "school" && isset($_POST['school'])) {
      // find and remove school's entries in all data files
      $match_string = $_POST['school'];
      $file_lines = read_file($contact_file_location);
      for($i = 0; $i < sizeof($file_lines); $i++) {
	if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
	  array_splice($file_lines, $i, 1);
	}
      }
      write_file($contact_file_location,$file_lines);

      $file_lines = read_file($password_file_location);
      for($i = 0; $i < sizeof($file_lines); $i++) {
	if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
	  array_splice($file_lines, $i, 1);
	}
      }
      write_file($password_file_location,$file_lines);

      $file_lines = read_file($delegate_list_location);
      for($i = 0; $i < sizeof($file_lines); $i++) {
	if(begins_with(str_replace('"',"",$file_lines[$i]),$match_string)) {
	  array_splice($file_lines, $i, 1);
	}
      }
      write_file($delegate_list_location,$file_lines);

      echo $_POST['school'] . ' has been removed!  <a href="secretariat.php">Return to the main page</a>.';
    }
  }

  include 'footer.php';
}
 ?>
