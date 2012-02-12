<?php
	/*
	*	@desc: PHP interface for the lvl-bubble svg 
	*/
	
	header("Content-Type: image/svg+xml");

	print ( system ("./gen-lvl-bubbles.py" ) );

?>
