<?php 
include 'lib.php';

if(check_secretariat_session()) {
  include 'secretariatheader.php';
  include 'configdata.php';

  if(isset($_POST['secretariat_password'])) {
    $output_string = "<?php\n";
    foreach ($_POST as $key => $value) {
      if (strstr($key,"charge") != FALSE) {
	$output_string .= '$' . $key . " = " . $value . ";\n";
      } elseif ((strstr($key,"columns") != FALSE) || (strstr($key,"committees") != FALSE)) {
	if ($value != "") {
	  $value = str_replace("\r\n",'","',$value);
	  $value = str_replace("\n",'","',$value);
	  $output_string .= '$' . $key . ' = array("' . $value . '");' . "\n";
	}
	else
	  $output_string .= '$' . $key . " = array();\n";
      } else {
	$output_string .= '$' . $key . ' = "' . $value . '";' . "\n";
      }
    }
    $output_string .= '$contact_file_columns = array("School","First Name","Last Name","E-mail Address","Address","City","State","Zip Code","Phone Number");' . "\n";
    $output_string .= "?>";
   write_file("configdata.php",array($output_string));

    echo 'New configuration has been saved.  Return to the <a href="secretariat.php">Secretariat Dashboard</a>.';
  } else {
?>
<style>
<!--
  p { text-indent : 50px; }
-->
</style>

<h1>Configure the registration system</h1>
<form method="POST" action="configuration.php">

<h2>Site Information</h2>
   <p>Site Title: <input name="site_title" size="50" value="<?php echo $site_title; ?>"></p>
   <p>Secretariat Password: <input name="secretariat_password" size="50" value="<?php echo $secretariat_password; ?>"></p>
   <p>Main CSS Location: <input name="css_location" size="50" value="<?php echo $css_location; ?>"></p>
   <p>Invoice CSS Location: <input name="invoice_css_location" size="50" value="<?php echo $invoice_css_location; ?>"></p>
   <p>Site Logo Location: <input name="logo_location" size="50" value="<?php echo $logo_location; ?>"></p>
   <p>Webmaster Email Address: <input name="webmaster_email" size="50" value="<?php echo $webmaster_email; ?>"></p>

<h2>Registration Data Locations</h2>
Store these files somewhere that is *not* accessible through the web!
   <p>Password File Location: <input name="password_file_location" size="50" value="<?php echo $password_file_location; ?>"></p>
   <p>Contact File Location: <input name="contact_file_location" size="50" value="<?php echo $contact_file_location; ?>"></p>
   <p>Delegate List Location: <input name="delegate_list_location" size="50" value="<?php echo $delegate_list_location; ?>"></p>
   <p>List of Countries File Location: <input name="list_of_countries_location" size="50" value="<?php echo $list_of_countries_location; ?>"></p>
   <p>School-Country Assignment File Location: <input name="school_country_assignments_location" size="50" value="<?php echo $school_country_assignments_location; ?>"></p>
   <p>Country-Committee Assignment File Location: <input name="country_committee_assignments_location" size="50" value="<?php echo $country_committee_assignments_location; ?>"></p>
   <p>Backup Data Location: <input name="backup_data_location" size="50" value="<?php echo $backup_data_location; ?>"></p>

<h2>Conference Information</h2>
   <p>Main Conference Website: <input name="main_conference_site" size="50" value="<?php echo $main_conference_site; ?>"></p>
   <p>Current Year's Conference Title: <input name="conference_title" size="50" value="<?php echo $conference_title; ?>"></p>
   <p>Conference Location: <input name="conference_location" size="50" value="<?php echo $conference_location; ?>"></p>
   <p>Conference Date: <input name="conference_date" size="50" value="<?php echo $conference_date; ?>"></p>
   <p>Organization Name: <input name="organization_title" size="50" value="<?php echo $organization_title; ?>"></p>
   <p>Organization Mailing Address: <input name="organization_mailing_address" size="50" value="<?php echo $organization_mailing_address; ?>"></p>
   <p>Secretary General's Email Address: <input name="secretary_general_email" size="50" value="<?php echo $secretary_general_email; ?>"></p>

<h2>Conference Fee Structure</h2>
    All fees are in dollars.  Enter only numbers into the text boxes (don't include the dollar sign).
   <p>Per School Charge: $<input name="per_school_charge" size="10" value="<?php echo $per_school_charge; ?>"></p>
   <p>Per Country Charge: $<input name="per_country_charge" size="10" value="<?php echo $per_country_charge; ?>"></p>
   <p>Per Faculty Sponsor Charge: $<input name="per_faculty_sponsor_charge" size="10" value="<?php echo $per_faculty_sponsor_charge; ?>"></p>
   <p>Per Delegate Charge: $<input name="per_delegate_charge" size="10" value="<?php echo $per_delegate_charge; ?>"></p>
   <p>Payment Mailing Address: <input name="payment_mailing_address" size="50" value="<?php echo $payment_mailing_address; ?>"></p>

<h2>Committees and Delegate Positions</h2>
Enter the conference committees in the box below, one item per line.<br/>
If you allow more than one delegate from countries in a committee, add multiple entries in the box for that committee that have unique names (example: GA Plenary Delegate 1, GA Plenary Delegate 2 for two delegates per country in the GA Plenary).  These names can only contain letters and numbers (no special characters).<br/>
<?php
$columns_value = "";
foreach ($committees as $column) {
  $columns_value .= $column . "\n";
}
?>
<p><textarea name="committees" rows="10" cols="50"><?php echo trim($columns_value); ?></textarea></p>

<h2>School Contact Information</h2>
The system will automatically ask for school name, sponsor name, sponsor email, address, city, state, zip code, and phone number.<br/>
Enter any additional contact information you want from each school faculty sponsor in the box below, one item per line.<br/>
<?php
$columns_value = "";
foreach ($more_contact_file_columns as $column) {
  $columns_value .= $column . "\n";
}
?>
<p><textarea name="more_contact_file_columns" rows="5" cols="50"><?php echo trim($columns_value); ?></textarea></p>
			       
<input type="submit" value="Submit Changes">
</form>

<?php
  }

  include 'footer.php';
}
 ?>
