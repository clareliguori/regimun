<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  // Print form
    ?>
<h1>Add a country</h1>
<b>Note:</b><br />
Please do not add delegate information for a country that has not been assigned to you by the Secretariat.<br />
To request countries, please e-mail <?php echo '<a href="mailto:' . $secretary_general_email . '">' . $secretary_general_email . '</a>';?>.<br /><br />

<form action="logcountry.php" method="POST">

<h3>Country</h3>
<select name="country">
<option value="select" selected>Select your country</option>
<?php
$file_lines = read_file($list_of_countries_location);
  $file_lines = remove_blank_entries($file_lines);
  sort($file_lines);
  foreach($file_lines as $country) {
    echo '<option>' . $country . "</option>\n";
  }
?>
</select><br /><br />

<h3>Delegates (First and Last Name):</h3>
Enter names exactly as you want them to appear on name tags. If you do not have a delegate in a certain committee, leave the box blank.<br /><br />

<?php
  foreach($committees as $committee) {
    echo $committee . ':<br /><input name="' . str_replace(" ","",$committee) . '" size="50"><br /><br />';
  }
  echo '<input type="submit" value="Submit"></form>';

  include 'footer.php';
}

?>
