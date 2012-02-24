<?php
	/*
	*	@desc: PHP interface for the lvl-bubble svg 
	*/
	
	header("Content-Type: image/svg+xml");

?><!DOCTYPE html>
<html>
	<head>
	</head>

	<body>

<?php

	print ( system ("./gen-lvl-bubbles.py" ) );

?>
</body>
</html>
