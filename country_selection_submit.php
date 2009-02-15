<?php
include 'lib.php';

if(check_session()) {
	include 'header.php';
?>
            	<h1>Country Selection</h1>
		<p>Thank you for submitting your country preferences!  We'll be in touch with the country that has been assigned to your school. <a href="main.php">Return to the main page</a>.</p>

<?php
	$to = $country_selection_email;
	$subject = "Conference Country Preferences";
	$body = "Conference Country Preferences Form Submission:\r\n\r\n";

	$body .= "School: " . $_SESSION['school'] . "\r\n";
	$body .= "Number of countries needed: " . $_POST['number'] . "\r\n";

	$body .= "Country #1: " . $_POST['country1'] . "\r\n";
	$body .= "Country #2: " . $_POST['country2'] . "\r\n";
	$body .= "Country #3: " . $_POST['country3'] . "\r\n";
	$body .= "Country #4: " . $_POST['country4'] . "\r\n";
	$body .= "Country #5: " . $_POST['country5'] . "\r\n";
	$body .= "Country #6: " . $_POST['country6'] . "\r\n";
	$body .= "Country #7: " . $_POST['country7'] . "\r\n";
	$body .= "Country #8: " . $_POST['country8'] . "\r\n";
	$body .= "Country #9: " . $_POST['country9'] . "\r\n";
	$body .= "Country #10: " . $_POST['country10'] . "\r\n";

	$headers = "From: " . $country_selection_email . "\r\n";
	$headers .= "Reply-To: " . $country_selection_email . "\r\n";
	$headers .= "X-Mailer: PHP/".phpversion();

	mail($to,$subject,$body,$headers);

  include 'footer.php';
}

?>
