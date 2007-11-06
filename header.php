<?php 
include 'config.php'; 
?>

<html>
<head>
<title><?php echo $site_title; ?></title>

<link rel="stylesheet" type="text/css" charset="utf-8" media="all" href="<?php echo $css_location; ?>">
</head>
<body>

<div id="header">
<div id="logo"><a href="index.php" class="logolink"><img src="<?php echo $logo_location; ?>" alt="<?php echo $organization_title; ?>"></a></div>
<div id="pagename"><?php echo $site_title . ": " . $conference_title; ?></div>
</div>
<div id="main-content">
<?php
if(isset($_SESSION['school'])) {
  echo '<b>School:</b> ' . $_SESSION['school'] . "<br/>";
}
?>
