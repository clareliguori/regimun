<?php 
include 'lib.php';

function get_email_list() {
  include 'config.php';
  $file_lines = read_file($contact_file_location);
  $sponsor_emails = array();
  foreach($file_lines as $line) {
    $entries = explode(',',$line);
    $entries = str_replace('"','',$entries);
    $entries = str_replace(' ','',$entries);
    if(trim($entries[3]) != "")
      array_push($sponsor_emails,$entries[3]);
  }
  sort($sponsor_emails);
  return implode(",",$sponsor_emails);
}

if(check_secretariat_session()) {
  include 'secretariatheader.php'; 

  if(isset($_POST['fromemail']) && isset($_POST['subject']) && isset($_POST['body'])) {
    // send email
    $to = get_email_list();
    $header = 'From: '.$_POST['fromemail'];
    if(mail($to, $_POST['subject'], $_POST['body'], $header)) {
      echo 'Your email has been sent to the faculty sponsors!  <a href="secretariat.php">Return to the main page!</a>';
    } else {
      echo 'Your email could not be sent.  Please try again!';
    }
    
  } else {
    echo '<h1>Email faculty sponsors</h1>';
    echo '<b>Copy the following into the To: bar of your e-mail client to e-mail all registered faculty sponsors.</b><br><br>';
    echo get_email_list();
    
    echo '<br><br><b>Use the following form to send an e-mail to all the registered faculty sponsors.</b><br><br>';
?>
<form method="POST" action="sponsoremail.php">
   Your e-mail address: <br><input name="fromemail" size="50"><br><br>
   Subject line: <br><input name="subject" size="50"><br><br>
   E-mail body: <br><textarea name="body" rows="10" cols="100"></textarea><br><br>
   <input type="submit" value="Send E-mail">
</form>
<?php
  }

  include 'footer.php';
}
 ?>
