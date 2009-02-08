<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php';
  include 'configdata.php';

   //$_POST = str_replace(array('"',',','\\'),"",$_POST);
  if(isset($_POST['committees'])) {
	  $list_of_committees = $_POST['committees'];
	  $committees_array = split("\n", $list_of_committees);
	  $committees_array = remove_blank_entries($committees_array);
	  sort($committees_array);
	  write_file($list_of_committees_location,$committees_array);
	  
	  echo 'Updated list of committees has been saved.  Return to the <a href="secretariat.php">Secretariat Dashboard</a>.';
  } else {
?>
<style>
<!--
  p { text-indent : 50px; }
-->
</style>

<h1>Edit the committees list</h1>
<form method="POST" action="committees-list.php">

Enter the conference committees in the box below, one item per line.<br/>
If you allow more than one delegate from countries in a committee, add multiple entries in the box for that committee that have unique names (example: GA Plenary Delegate 1, GA Plenary Delegate 2 for two delegates per country in the GA Plenary).  These names can only contain letters and numbers (no special characters).<br/>
<?php
$committees_list = "";
$file_lines = read_file($list_of_committees_location);
foreach ($file_lines as $line) {
  $committees_list .= $line . "\n";
}
?>
<p><textarea name="committees" rows="30" cols="50"><?php echo trim($committees_list); ?></textarea></p>
			       
<input type="submit" value="Submit Changes">
</form>

<?php
  }

  include 'footer.php';
}
?>