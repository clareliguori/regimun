<?php 
include 'header.php'; 
include 'lib.php';

if(isset($_POST['school'])) {
  $file_lines = read_file($contact_file_location);
  $sponsor_emails = array();
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    if($school_name == $_POST['school']) {
      $entries = str_replace('"','',$entries);
      array_push($sponsor_emails,$entries[3]);
    }
  }

  $file_lines = read_file($password_file_location);
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    if($school_name == $_POST['school']) {
      $entries = str_replace('"','',$entries);
      $password_match = $entries[1];
    }
  }

  $to = implode(",",$sponsor_emails);
  $subject = "Conference Registration Password Reminder";
  $body = "Someone has filled out the 'Forgotten Password' form on the ".$conference_title." conference registration system.  \nIf you did not request this e-mail, please disregard it.\n\n";
  $body .= $_POST['school'] . "'s password: " . $password_match;

  if (mail($to, $subject, $body)) {
    echo "Your school's password has been sent to: " . $to;
  } else {
    echo "E-mail delivery failed.  Please try again!";
  }
} else {
?>
<h1>E-mail Forgotten Password</h1>
Use the form below to have your school's password e-mailed to the faculty sponsors registered for the account.<br><br>
<form method="post" action="forgotpassword.php">
Choose your school:<br />
<select name="school">
<?php
$schools = array();
$file_lines = read_file($password_file_location);
foreach($file_lines as $line) {
  $entries = explode(',',$line);
  $school_name = $entries[0];
  $school_name = str_replace('"','',$school_name);
  array_push($schools,$school_name);
}
sort($schools);

foreach($schools as $school) {
  if($school != "")
    echo "<option>" . $school . "</option>";
}
?>
</select>

<br/><br/><input TYPE="submit" NAME="submitlogin" VALUE="Submit">
</form>

<?php 
}
include 'footer.php'; ?>
