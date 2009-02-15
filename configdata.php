<?php

# SITE INFORMATION
$site_title = 'Conference Registration';
$secretariat_password = "secretariat";
$css_location = 'css/registration.css';
$invoice_css_location = 'css/invoice.css';
$logo_location = '/var/www/img/hamuntop.jpg';
$webmaster_email = 'webmaster@hamun.org';

# REGISTRATION DATA
# Store these files somewhere that is *not* accessible through the web
$password_file_location = '/home/hamun/registration/data/schoolpasswd.csv';
$contact_file_location = '/home/hamun/registration/data/schoolcontact.csv';
$delegate_list_location = '/home/hamun/registration/data/delegates.csv';
$optional_event_list_location = '/home/hamun/registration/data/optional-event-list.csv';
$list_of_committees_location = '/home/hamun/registration/data/committees.txt';
$list_of_countries_location = '/home/hamun/registration/data/countries.txt';
$school_country_assignments_location = '/home/hamun/registration/data/school-country-assignments.csv';
$country_committee_assignments_location = '/home/hamun/registration/data/country-committee-assignments.csv';
$backup_data_location = '/home/hamun/registration/data/backup/';

# CONFERENCE INFORMATION
$main_conference_site = 'http://www.hamun.org';
$conference_title = 'Houston Area Model United Nations XXXII';
$conference_location = 'University of Houston Main Campus';
$conference_date = 'February 9 - 10, 2007';
$organization_title = 'Houston Area Model United Nations, Inc.';
$organization_mailing_address = "P.O. Box 667049, Houston, Texas, 77266";
$secretary_general_email = "secgen@hamun.org";

# OPTIONAL EVENT INFORMATION
$enable_optional_event = "true";
$optional_event_name = "Delegate Social";

# COUNTRY SELECTION INFORMATION
$country_selection_enable = "true";
$country_selection_open = "true";
$country_selection_email = "secgen@hamun.org";
$number_of_selections_charge = 10;

# CONFERENCE FEE STRUCTURE
$per_school_charge = 10;
$per_country_charge = 20;
$per_faculty_sponsor_charge = 30;
$per_delegate_charge = 40;
$per_person_optional_event_charge = 5;
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
?>
