<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

#print out all entries matching school in contact file
  echo "<h1>Faculty Sponsor Contact Information</h1>";
  echo "The following sponsors are currently registered for your school:<br /><br />";
  $file_lines = read_file($contact_file_location);
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    if($school_name == $_SESSION['school']) {
      $entries = str_replace('"','',$entries);
      echo "<b>Sponsor: " . $entries[1] . " " . $entries[2] . "</b><br>";
      echo "E-mail Address: " . $entries[3] . "<br>";
      echo "Mailing Address: " . $entries[4] . ", " . $entries[5] . ", " . $entries[6] . ", " . $entries[7] . "<br>";
      echo "Phone Number: " . $entries[8] . "<br>";
      for($i = 0; $i < sizeof($more_contact_file_columns); $i++) {
	echo $more_contact_file_columns[$i] . ": " . $entries[9 + $i] . "<br />";
      }
      echo "<br>";
    }
  }

?>
<a href="addcontact.php">Add Faculty Sponsor</a><br/>
<a href="editcontact.php">Edit Faculty Sponsor</a><br/>
<a href="removecontact.php">Remove Faculty Sponsor</a>
<?php

  echo "<h1>Delegate Registration</h1>";
  echo "The following delegates are currently registered for your school:<br />";
#print out all entries matching school in delegates.cvs
  $file_lines = read_file($delegate_list_location);
  $school_lines = array();
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    if(str_replace('"','',$entries[0]) == $_SESSION['school']) {
      array_push($school_lines,$line);
    }
  }
  sort($school_lines);

  $currentcountry = "";
  foreach($school_lines as $line) {
    $entries = explode(',',$line);
    $entries = str_replace('"','',$entries);
    if($current_country != $entries[1]) {
      echo "<br/><h2>" . $entries[1] . "</h2>";
      $current_country = $entries[1];
    }
    echo $entries[2] . ": " . $entries[3] . "<br>";
  }
?>

<br>
<a href="addcountry.php">Add Country</a><br />
<a href="editcountry.php">Edit Country</a><br />
<a href="removecountry.php">Remove Country</a><br />

<h1>School Invoice</h1>
If you need an invoice, click the following link.  It will generate an invoice based on your delegate registration, which you can print from your web browser.<br><br>
<a href="invoice.php">Create School Invoice</a>

<h1>Password Change</h1>
<a href="changepassword.php">Change Account Password</a>

<?php
   include 'footer.php';
}

?>
