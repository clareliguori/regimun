<?php 
include 'header.php'; 
include 'lib.php';

if(isset($_POST['school']) && isset($_POST['password1']) && isset($_POST['password2'])) {
  // process new school form
  if($_POST['password1'] != $_POST['password2'] ||
     $_POST['password1'] == "") {
    // check matching passwords
    echo 'Passwords do not match or are empty.  Please try again.';
  } else {
    // check for special characters
    $allowed_chars = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,1,2,3,4,5,6,7,8,9,0";
    $allowed_chars = explode(",",$allowed_chars);
    if(str_replace($allowed_chars,"",$_POST['password1'])!="") {
      echo "Password contains special characters.  Password can only contain letters and numbers.  Please try again.  Use the back button on your browser.";
    } else {
      //check for existing school account
      $school_match = false;
      $file_lines = read_file($password_file_location);
      for($i = 0; $i < sizeof($file_lines); $i++) {
	$current_school = str_replace(" ","",strtolower(str_replace('"',"",$file_lines[$i])));
	$new_school = str_replace(" ","",strtolower($_POST['school']));
	if(begins_with($current_school,$new_school)) {
	  $school_match = true;
	}
      }
      
      if($school_match) {
	echo 'An account for your school already exists!';
      } else {
	array_push($file_lines, '"'.$_POST['school'].'","'.$_POST['password1'].'"');
	write_file($password_file_location,$file_lines);
	echo 'Your new school account has been created!  ';

	$to = $_POST['email'];
	$subject = "New Conference Registration Account";
	$body = "You have created a new ".$conference_title." conference registration account for ".$_POST['school'].". Your password is ".$_POST['password1'].".";
	if(mail($to,$subject,$body)) {
	  echo 'The account password has been e-mailed to the address you provided.  ';
	}
	echo '<a href="index.php">Return to the main page</a> to log into your account.';
      }
    }
  }
} else {
  // print new school form
?>
<h1>Create New School Account</h1>
Use the form below to create a new school account for conference registration.  Please check the main registration page to ensure your school account is not already created!
<br><br>
<form method="post" action="newschool.php">
      School name:<br>
      <input TYPE="text" NAME="school">
      <br><br>
      Your e-mail address:<br>
      <input TYPE="text" NAME="email">
      <br><br>
    Password:
      <br>
      <input TYPE="password" NAME="password1">
      <br><br>
    Re-type password:
      <br>
      <input TYPE="password" NAME="password2"><br>
      Password may only contain letters and numbers.  No special characters.
      <br><br>
      <input TYPE="submit" NAME="submitlogin" VALUE="Submit">
      <br>
</form>

<?php 
}
include 'footer.php'; ?>
