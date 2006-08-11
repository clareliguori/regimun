<?php
include 'lib.php';

if(check_session()) {
  include 'invoicelib.php';
  include 'config.php';

  // get school list
  $schools = array();
  $file_lines = read_file($password_file_location);
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    array_push($schools,$school_name);
  }
  sort($schools);
  
  invoice_header();
  foreach($schools as $school) {
    print_invoice($school);
  }
  invoice_footer();
}

?>
