<?php

# SITE INFORMATION
$site_title = 'Conference Registration';
$secretariat_password = "password";
$css_location = 'css/registration.css';
$invoice_css_location = 'css/invoice.css';
$logo_location = '/var/www/img/hamuntop.jpg';
$webmaster_email = 'webmaster@hamun.org';

# REGISTRATION DATA
# Store these files somewhere that is *not* accessible through the web
$password_file_location = '/home/hamun/registration/data/schoolpasswd.csv';
$contact_file_location = '/home/hamun/registration/data/schoolcontact.csv';
$delegate_list_location = '/home/hamun/registration/data/delegates.csv';
$list_of_countries_location = '/home/hamun/registration/data/countries.txt';
$backup_data_location = '/home/hamun/registration/data/backup/';

# CONFERENCE INFORMATION
$main_conference_site = 'http://www.hamun.org';
$conference_title = 'Houston Area Model United Nations XXXII';
$conference_location = 'University of Houston Main Campus';
$conference_date = 'February 9 - 10, 2007';
$organization_title = 'Houston Area Model United Nations, Inc.';
$organization_mailing_address = "P.O. Box 667049, Houston, Texas, 77266";
$secretary_general_email = "secgen@hamun.org";

# CONFERENCE FEE STRUCTURE
$per_school_charge = 10;
$per_country_charge = 20;
$per_faculty_sponsor_charge = 30;
$per_delegate_charge = 40;
$payment_mailing_address = "555 HAMUN Lane, Houston, Texas, 77777";

# SCHOOL CONTACT FILE COLUMNS
// Do not change the contact_file_columns array!!
// If needed, add columns in the more_contact_file_columns array
$contact_file_columns = array("School", 
			      "First Name",
			      "Last Name",
			      "E-mail Address",
			      "Address",
			      "City",
			      "State",
			      "Zip Code",
			      "Phone Number");
$more_contact_file_columns = array();

# CONFERENCE COMMITTEES / DELEGATE POSITIONS
// If you allow more than one delegate from countries in a committee, add multiple entries in the array for that committee that have unique names (example: GAPlenaryDelegate1, GAPlenaryDelegate2 for two delegates per country in the GA Plenary).  These names can only contain letters and numbers (no special characters).
$committees = array("GA Plenary Ambassador",
		    "GA Plenary Assistant Ambassador",
		    "GA 1",
		    "GA 3",
		    "GA 6",
		    "Security Council Delegate 1",
		    "Security Council Delegate 2",
		    "European Union",
		    "ICJ Delegate or Litigant",
		    "ICJ Second Litigant",
		    "Commission on Human Rights",
		    "ECOSOC",
		    "CSTD");
?>
