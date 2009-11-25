<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php';
  include 'configdata.php';

  #$_POST = str_replace(array('"',',','\\'),"",$_POST);
  if(isset($_POST['countries'])) {
	  $list_of_countries = $_POST['countries'];
	  $list_of_countries = str_replace(array('"',',','\\'),"",$list_of_countries);
	  $countries_array = split("\n", $list_of_countries);
	  $countries_array = remove_blank_entries($countries_array);
	  sort($countries_array);
	  write_file($list_of_countries_location,$countries_array);
	  
	  echo 'Updated list of countries has been saved.  Return to the <a href="secretariat.php">Secretariat Dashboard</a>.';
  } else {
?>
<style>
<!--
  p { text-indent : 50px; }
-->
</style>

<h1>Edit the countries list</h1>
<form method="POST" action="countries-list.php">

Enter all the countries and organizations that will be represented at the conference in the box below, one item per line. This list will be used for schools' country preference submission and country assignment.<br/>
These names can only contain letters and numbers (no special characters like apostrophes).<br/>
<?php
$countries_list = "";
$file_lines = read_file($list_of_countries_location);
foreach ($file_lines as $line) {
  $line = str_replace("\r\n","\n",$line);
  $countries_list .= $line . "\n";
}
?>
<p><textarea name="countries" rows="30" cols="50"><?php echo trim($countries_list); ?></textarea></p>
			       
<input type="submit" value="Submit Changes">
</form>

<?php
  }

  include 'footer.php';
}
?>