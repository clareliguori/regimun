<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 

  //Tabulate delegate and school count
  $file_lines = read_file($delegate_list_location);
  $file_lines = remove_blank_entries($file_lines);
  $school_list = array();
  foreach($file_lines as $line) {
	  $entries = explode(',',$line);
	  $school_name = $entries[0];
	  array_push($school_list, $school_name);
  }
  echo 'Total number of delegates registered for conference: ';
  echo sizeof($school_list) . '<br/>';
  echo 'Total number of schools with registered delegates: ';
  echo sizeof(array_unique($school_list)) . '<br/>';
?>

<h1>Communication</h1>
<a href="sponsoremail.php">Email all registered faculty sponsors</a>

<h1>Downloads</h1>
   These are CSV (comma separated value) files.  To view them in Excel in spreadsheet form, right click on the link and click Save Link As.  Save the file to your computer as something.csv (not showfile.php).  Then you should be able to double click on the file on your computer, and it will open up in Excel.<br><br>
<a href="showfile.php?filename=<?php echo $contact_file_location; ?>">Sponsor Contact Info Spreadsheet</a><br>
<a href="showfile.php?filename=<?php echo $delegate_list_location; ?>">Delegates Registration Spreadsheet</a><br>
<a href="showfile.php?filename=<?php echo $password_file_location; ?>">School Password Spreadsheet</a><br>
<br/>
<a href="showfile.php?filename=<?php echo $school_country_assignments_location; ?>">School-Country Assignments Spreadsheet</a><br>
<a href="showfile.php?filename=<?php echo $country_committee_assignments_location; ?>">Country-Committee Assignments Spreadsheet</a>

<h1>School Information</h1>
<form method="post" action="main.php">
Choose a school to view its information:<br>
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
  echo '</select>';
  echo '<br><br><input TYPE="submit" NAME="submitlogin" VALUE="Submit"></form>';
  echo '<a href="allinvoices.php">Generate all invoices in one document</a>';
?>

<h1>Registration Configuration</h1>
<a href="configuration.php">Configure system: conference information, registration data location, and conference fee structure</a><br/>
<a href="countries-list.php">Edit list of countries</a><br/>
<a href="committees-list.php">Edit list of committees</a><br/>
<a href="countries-committee-assign.php">Assign committees to countries</a><br/>
<a href="school-countries-assign.php">Assign countries to schools</a><br/>

<h1>System Administration</h1>
<a href="backup.php">Backup all system data</a><br/>
<a href="reset.php?type=delegates">Remove all delegates</a><br/>
<a href="reset.php?type=full">Perform a full system reset</a><br/><br/>

<form method="post" action="reset.php?type=school">
Choose a school to remove:<br>
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
  echo '</select>';
  echo '<br><br><input TYPE="submit" NAME="submitlogin" VALUE="Submit"></form>';

} else {
  include 'secretariatheader.php';
?>
<h1>Secretariat Login</h1>
<form method="post" action="secretariat.php">
Password:
<br>
<input TYPE="password" NAME="secretariatpassword">
<br><br>
<input TYPE="submit" NAME="submitlogin" VALUE="Submit">
<br>
</form>
<br />

<?php 
}
include 'footer.php'; ?>
