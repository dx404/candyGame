<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8" >
	<title> Candy Game </title>
	<link rel="stylesheet" type="text/css" href="../CSS/body.css" >
	<link rel="stylesheet" type="text/css" href="../CSS/index.css" >
	<link rel="stylesheet" type="text/css" href="board.css" >
	<script type="text/javascript" src="jquery-2.1.0.js"></script>
	<script type="text/javascript" src="jquery.cookie.js"></script>
	<script type="text/javascript" src="board.js"></script>
</head>
<?php 
ini_set('display_errors', 'On');
$N = 6;
if (isset($_GET['size']))
	$N = $_GET['size'];
?>
<body>
	<h1>Candy Game</h1>
	<form id="boardForm" action='.' method="get">
		<p>Size: <input type="text" name="size" value="<?php echo $N;?>">
 		 <button type="submit"> Resize </button></p>
	</form>
	<fieldset>
<?php
	echo "<legend> Candy Game ($N by $N) </legend>";
?>	
	<table id="scoreBoad">
		<tr style="color:lightblue"><td>Blue:</td><td id="blueScore">0</td> 
			<td> <img id="blueToggle" alt="You Now" src="hand-point-left.jpg" width="70"></td>
			
		</tr>
		<tr style="color:lightgreen"><td>Green: </td><td id="greenScore">0 </td> 
			<td> <img id="greenToggle" alt="You Now" src="hand-point-left.jpg" width="70"></td> 
			
		</tr>
	</table>
<?php
	echo "<table class=\"candyGameBoad\" data-boardSize=\"$N\">\n";
	for ($i = 0; $i < $N + 1; $i++){
		echo "<tr>";
		for ($j = 0; $j < $N + 1; $j++){
			$category = ($i * $j == 0) ? "border" : "cell";
			echo "<td id=\"cell-$i-$j\" class=\"$category candyGameBoad\" data-status=\"V\"> $i$j</td>\t";
		}
		echo "</tr>\n";
	}
	echo "</table>";
?>
	</fieldset>
	
	<div >
		<pre id="scratch">
		
		</pre>
	</div>
	<div >
		<pre id="log">
		
		</pre>
	</div>
	

</body>