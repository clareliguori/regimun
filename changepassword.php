<?php
include 'lib.php';

if(check_session()) {
  include 'header.php';

  if(isset($_POST['password1']) && isset($_POST['password2'])) {
    // process password form
    if($_POST['password1'] != $_POST['password2'] ||
       $_POST['password1'] == "") {
      echo 'Passwords do not match or are empty.  Please try again.';
    } else {
      $allowed_chars = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,1,2,3,4,5,6,7,8,9,0";
      $allowed_chars = explode(",",$allowed_chars);
      if(str_replace($allowed_chars,"",$_POST['password1'])!="") {
	echo "Password contains special characters.  Password can only contain letters and numbers.  Please try again.  Use the back button on your browser.";
      } else {
	$file_lines = read_file($password_file_location);
	for($i = 0; $i < sizeof($file_lines); $i++) {
	  if(begins_with(str_replace('"',"",$file_lines[$i]),$_SESSION['school'])) {
	    array_splice($file_lines, $i, 1);
	  }
	}
	array_push($file_lines, '"'.$_SESSION['school'].'","'.$_POST['password1'].'"');
	write_file($password_file_location,$file_lines);
	echo 'Your password has been changed! <a href="main.php">Return to the main page</a>!';
      }
    }
  } else {
    // print password form
?>
<h1>Change password</h1>
<form method="POST" action="changepassword.php">

New password:
<br>
<input TYPE="password" NAME="password1">
<br><br>
Re-type new password:
<br>
<input TYPE="password" NAME="password2"><br><br>
Password may only contain letters and numbers.  No special characters.
<br><br>
<input TYPE="submit" NAME="submitlogin" VALUE="Submit">
<br>
</form>

<?php    
  }

  include 'footer.php';
}

?>
