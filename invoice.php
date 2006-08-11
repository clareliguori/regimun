<?php
include 'lib.php';

if(check_session()) {
  include 'invoicelib.php';
  invoice_header();
  print_invoice($_SESSION['school']);
  invoice_footer();
}

?>
