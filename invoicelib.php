<?php

function invoice_header() {
  include 'config.php';
  echo '<html>';
  echo '<head><title>Conference Invoice</title>' . "\n";
  echo '<style type="text/css" media="all">' . "\n";
  echo ' @import "'.$invoice_css_location.'";' . "\n";
  echo '</style>' . "\n";
  echo '<link rel="stylesheet" type="text/css" media="print" href="invoiceprint.css" />' . "\n";
  echo '</head>';
  echo '<body>';
}

function print_invoice($school) {
  include 'config.php';
  echo '<div id="main-content"><div id="invoice">';
  echo "<h2>INVOICE</h2>";

  echo '</div><div id="letterhead">';
  echo "<h1>" . $organization_title . "</h1>";
  echo $organization_mailing_address . " &#8226; ";
  echo $main_conference_site . "<br><br><br/>";

  echo '</div><div id="topinfo"><div id="billto">';

  echo "<h3>Bill To:</h3>";
  $file_lines = read_file($contact_file_location);
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $school_name = $entries[0];
    $school_name = str_replace('"','',$school_name);
    if($school_name == $school) {
      $entries = str_replace('"','',$entries);
      echo $entries[1] . " " . $entries[2] . "<br>";
      echo "c/o " . $school . "<br>";
      echo $entries[4] . "<br>" . $entries[5] . ", " . $entries[6] . ", " . $entries[7] . "<br>";
      break;
    }
  }

  echo '<br/><br/></div><div id="date">';
  echo "<h3>Date:</h3>";
  echo date('l, F j, Y');

  echo '<br/><br/><br/></div></div><div id="event">';

  echo "<h3>Event:</h3>";
  echo $conference_title . "<br>";
  echo $conference_location . "<br>";
  echo $conference_date . "<br><br>";

  echo '<br/></div><div id="fees">';
  echo "<h3>Conference Fees:</h3>";
  echo '<table>';
  echo "<tr><th class=\"left\">Fee</th><th>Rate</th><th>Quantity</th><th>Amount</th></tr>";
  
  $total_charge = 0;

  // School charge
  if($per_school_charge != 0) {
    $number = 1;
    $charge = $number * $per_school_charge;
    $total_charge += $charge;
    echo "<tr><td class=\"left\">School Fee</td><td>$".number_format($per_school_charge, 2, '.', '')."</td><td>".$number."</td><td>$".number_format($charge, 2, '.', '')."</td></tr>";
  }

  // Country charge
  if($per_country_charge != 0) {
    $number = 0;

    $file_lines = read_file($delegate_list_location);
    $school_lines = array();
    foreach($file_lines as $line) {
      $entries = explode(',',$line);
      if(str_replace('"','',$entries[0]) == $school) {
	array_push($school_lines,$line);
      }
    }
    sort($school_lines);
    
    $currentcountry = "";
    foreach($school_lines as $line) {
      $entries = explode(',',$line);
      $entries = str_replace('"','',$entries);
      if($current_country != $entries[1]) {
	$number++;
	$current_country = $entries[1];
      }
    }

    $charge = $number * $per_country_charge;
    $total_charge += $charge;
    echo "<tr><td class=\"left\">Country Fee</td><td>$".number_format($per_country_charge, 2, '.', '')."</td><td>".$number."</td><td>$".number_format($charge, 2, '.', '')."</td></tr>";
  }

  // Faculty Sponsor charge
  if($per_faculty_sponsor_charge != 0) {
    $number = 0;
    $file_lines = read_file($contact_file_location);
    foreach($file_lines as $line) {
      $entries = explode(',',$line);
      $school_name = $entries[0];
      $school_name = str_replace('"','',$school_name);
      if($school_name == $school) {
	$number++;
      }
    }
    
    $charge = $number * $per_faculty_sponsor_charge;
    $total_charge += $charge;
    echo "<tr><td class=\"left\">Faculty Sponsor Fee</td><td>$".number_format($per_faculty_sponsor_charge, 2, '.', '')."</td><td>".$number."</td><td>$".number_format($charge, 2, '.', '')."</td></tr>";
  }

  // delegate charge
  if($per_delegate_charge != 0) {
    $number = 0;

    $file_lines = read_file($delegate_list_location);
    $school_lines = array();
    foreach($file_lines as $line) {
      $entries = explode(',',$line);
      if(str_replace('"','',$entries[0]) == $school) {
	$number++;
      }
    }

    $charge = $number * $per_delegate_charge;
    $total_charge += $charge;
    echo "<tr><td class=\"left\">Student Delegate Fee</td><td>$".number_format($per_delegate_charge, 2, '.', '')."</td><td>".$number."</td><td>$".number_format($charge, 2, '.', '')."</td></tr>";
  }

  echo '<tr><th colspan="3">Total Amount Due</th><th>$'.number_format($total_charge, 2, '.', '').'</th></tr>';
  echo "</table>";
  echo "<br><br><br/>";

  echo "Please mail all payment to: <br>" . $payment_mailing_address . "<br>";
  echo "<i>We look forward to seeing your school at the conference!</i>";

  echo '</div></div>';
}

function invoice_footer() {
  echo '</body></html>';
}

?>
