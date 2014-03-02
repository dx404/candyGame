<?php 
	$N = $_POST["N"];
	$player = $_POST["player"];
	$px = $_POST["px"];
	$py = $_POST["py"];
	$info = "$N\n$player\n$px $py\n\n";
	
	$board = $_POST["board"];
	for ($i = 0; $i < $N; $i++){
		for ($j = 0; $j < $N; $j++){
			$info .= ("$i $j " . $board[$i][$j][0] . " " . $board[$i][$j][1] . "\n");
		}
	}
// 	echo $info;
// 	echo '<br>';
	$result = shell_exec("echo \"$info\" | python candyGame.py");
	echo $result;
?>