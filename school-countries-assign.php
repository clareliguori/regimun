<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php';
  include 'configdata.php';

  if(isset($_POST['writeout'])) {
	  $output_array = array();
	  array_push($output_array, "Country,School");
	  foreach ($_POST as $key => $value) {
		  if($key != "writeout" and $value != "") {
			  array_push($output_array, '"' . $key . '","' . $value . '"');
		  }
	  }

	  write_file($school_country_assignments_location,$output_array);

	  echo 'New school-country assignments have been saved.  Return to the <a href="secretariat.php">Secretariat Dashboard</a>.';
  } else {
?>
<style>
<!--
  p { text-indent : 50px; }
-->
</style>

<h1>Assign countries to schools</h1>
<form method="POST" action="school-countries-assign.php">
<input type="hidden" name="writeout" value="true">
<table>

<?php
	  $file_lines = read_file($school_country_assignments_location);
	  $assignments = array();
	  foreach($file_lines as $line) {
		  $entries = explode(',',$line);
		  
		  $country_name = $entries[0];
		  $country_name = str_replace('"','',$country_name);

		  $school_name = $entries[1];
		  $school_name = str_replace('"','',$school_name);

		  $assignments[$country_name] = $school_name;
	  }

	  $schools = array();
	  $file_lines = read_file($password_file_location);
	  foreach($file_lines as $line) {
		  $entries = explode(',',$line);
		  $school_name = $entries[0];
		  $school_name = str_replace('"','',$school_name);
		  array_push($schools,$school_name);
	  }
	  sort($schools);

	  $countries = read_file($list_of_countries_location);
	  sort($countries);

	  foreach($countries as $country) {
		  $assignment = "";
		  if (array_key_exists($country, $assignments)) {
			  $assignment = $assignments[$country];
		  }

		  echo "<tr><td>" . $country . "</td><td>\n";
		  echo '<select name="' . $country . '">';
		  echo "<option></option>";
		  foreach($schools as $school) {
			  if($school != "") {
				  if(strcmp($school,$assignment) == 0)
					  echo "<option selected=\"true\">" . $school . "</option>\n";
				  else
					  echo "<option>" . $school . "</option>\n";
			  }
		  }
		  echo "</select></td></tr>\n";		  
	  }
 
?>

</table>
			       
<input type="submit" value="Submit Changes">
</form>

<?php
  }

  include 'footer.php';
}
 ?>
