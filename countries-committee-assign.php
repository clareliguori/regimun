<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php';
  include 'configdata.php';

  $countries = read_file($list_of_countries_location);
  sort($countries);

  $committees = read_file($list_of_committees_location);
  sort($committees);

  if(isset($_POST['check'])) {
	  $output_array = array();
	  $assignments = array();

	  foreach ($_POST['check'] as $value) {
		  $entries = split('_assigned_', $value);
		  $country = $entries[0];
		  $country = str_replace('_',' ',$country);
		  $new_committee = $entries[1];
		  $new_committee = str_replace('_',' ',$new_committee);
		  if(array_key_exists($country, $assignments))
			  $assignments[$country] .= ',"' . $new_committee . '"';
		  else
			  $assignments[$country] = '"' . $new_committee . '"';
	  }

	  foreach ($assignments as $country => $committee_assigns) {
		  array_push($output_array, '"' . $country . '",' . $committee_assigns);
	  }

	  write_file($country_committee_assignments_location,$output_array);

	  echo 'New country-committee assignments have been saved.  Return to the <a href="secretariat.php">Secretariat Dashboard</a>.';
  } else {
?>
<style>
<!--
  p { text-indent : 50px; }
-->
</style>

<h1>Assign countries to schools</h1>
<form method="POST" action="countries-committee-assign.php">
<table style="border-spacing: 0px">

<?php
	  $file_lines = read_file($country_committee_assignments_location);
	  $assignments = array();
	  foreach($file_lines as $line) {
		  $entries = explode('","',$line, 2);
		  
		  $country_name = $entries[0];
		  $country_name = str_replace('"','',$country_name);

		  $committees_list = $entries[1];
		  $committees_list = explode('","', $committees_list);
		  for($i = 0; $i < sizeof($committees_list); $i++) {
			  $committees_list[$i] = str_replace('"','',$committees_list[$i]);
			  $committees_list[$i] = str_replace("\r\n","",$committees_list[$i]);
			  $committees_list[$i] = str_replace("\n","",$committees_list[$i]);
		  }

		  $assignments[$country_name] = $committees_list;
	  }

	  $i = 0;
	  foreach($countries as $country) {
		  $style_string = "text-align: center; border-left: thin solid; border-top: thin solid;";
		  if($i % 15 == 0) {
			  echo "<tr><td> </td>\n";
			  foreach($committees as $committee) {
				  if($i > 0)
					  echo "  <td style=\"font-weight: bold; border-top: thin solid; text-align: center;\">" . $committee . "</td>\n";
				  else
					  echo "  <td style=\"font-weight: bold; text-align: center;\">" . $committee . "</td>\n";
			  }
			  echo "</tr>\n";
		  }

		  echo "<tr><td>" . $country . "</td>\n";

		  $current_committee_assignments = array();
		  if (array_key_exists($country, $assignments)) {
			  $current_committee_assignments = $assignments[$country];
		  }

		  for($j = 0; $j < sizeof($committees); $j++) {
			  $name = $country . '_assigned_' . $committees[$j];
			  $name = str_replace(' ','_',$name);

			  if($j == sizeof($committees) - 1)
				  $style_string .= "border-right: thin solid;";
			  
			  if(in_array($committees[$j], $current_committee_assignments))
				  echo '<td style="' . $style_string . '"><input type=checkbox checked="true" name="check[]" value="' . $name . '"></td>'. "\n";
			  else
				  echo '<td style="' . $style_string . '"><input type=checkbox name="check[]" value="' . $name . '"></td>' . "\n";
		  }

		  echo "</tr style=\"border-right: thin solid;\">\n";
		  $i++;
	  }

	  echo "<tr><td> </td>\n";
	  foreach($committees as $committee) {
		  echo "  <td style=\"font-weight: bold; border-top: thin solid; text-align: center;\">" . $committee . "</td>\n";
	  }
	  echo "</tr>\n";

 
?>

</table>
			       
<input type="submit" value="Submit Changes">
</form>

<?php
  }

  include 'footer.php';
}
 ?>
