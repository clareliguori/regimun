<?php 
include 'header.php'; 
include 'lib.php';
?>

<h1>School Login</h1>
<form method="post" action="main.php">
Choose your school:<br />
<select name="schoolname">
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

<br><br>
Password:
<br>
<input TYPE="password" NAME="schoolpasswd">
<br><br>

<input TYPE="submit" NAME="submitlogin" VALUE="Submit">
<br>
</form>
<br />
Forgot your password? <a href="forgotpassword.php">Get it e-mailed to you</a><br />
School not listed? <a href="newschool.php">Register a new school</a>
<br /><br /><a href="secretariat.php">Secretariat Login</a>
<?php include 'footer.php'; ?>
