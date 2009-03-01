<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if($country_selection_open == 'true' && $country_selection_enable == 'true') {
?>
	<h1>Country Selection</h1>
	<p>Country selection is done by random lottery. Please submit the following form to notify us of your country preferences.</p>

	<form action="country_selection_submit.php" method="post">
	<p>
	Number of countries needed: <input type="text" name="number"/><br/><br/>
<?php
		 for($i = 1; $i <= $number_of_selections_charge; $i++) {
			 echo 'Country #' . $i . ': ';
			 echo '<select name="country' . $i . '">';
			 echo '<option value="select" selected>Select your #' . $i . ' preferred country</option>';
			 
			 $file_lines = read_file($list_of_countries_location);
			 foreach($file_lines as $country_choice) {
				 echo '<option>' . $country_choice . "</option>\n";
			 }
			 
			 echo '</select><br /><br />';
		 }
?>
	<INPUT type="submit" value="Submit"> <INPUT type="reset">
	</p>
	</form>

<?php
  }

  include 'footer.php';
}

?>
