var N;
var player = "blue";
var URLconnector = "connector.php";
var blueScore = 0;
var greenScore = 0;
$(document).ready(function(){
	N = $("table.candyGameBoad").attr("data-boardSize");
	$("#cell-0-0").text("");
	for (var i = 1; i <= N; i++){
		$("#cell-" + i + "-0").text(i);
	}
	for (var j = 1; j <= N; j++){
		$("#cell-0-" + j).text(String.fromCharCode(64 + j));
	}
	
	if ($.cookie('boardGame') === null || $.parseJSON($.cookie('boardGame'))['N'] != N){
		refreshTurn("blue");
		randomFill();
	}
	else{
		cookieFill();
	}
	

	for (var i = 1; i <= N; i++){
		for (var j = 1; j <= N; j++){	
			$("#cell-" + i + "-" + j).on('click', function(){
				var cellStatus = $(this).attr("data-status");
				if (cellStatus == 'V'){
					var px = parseInt($(this).attr('id').substring(5,6)) - 1;
					var py = parseInt($(this).attr('id').substring(7,8)) - 1;
					var info = "N=" + N + "&";
					info +=	"player=" + player + "&";
					info += "px=" + px + "&";
					info += "py=" + py + "&";
					info += loadBoardInfo() + "end=true";
					
					$.ajax(URLconnector, {
						type: 'POST',
						data: info,
						//dataType: 'json',
						success: function (data, textStatus, jqXHR){
							// $("#scratch").text(data);
							result = $.parseJSON(data);
							$.cookie('boardGame', data);
							renderBoard(result);
						},
						error: function (jqXHR, textStatus, errorThown){
							alert('Load previous dorms failed');
						},
						cache:false
					});
					
					
					var pos = player + " : " 
					+ String.fromCharCode(65 + py) + (px+1) 
					+ " (" + blueScore + ", " + greenScore + ")";
					$("#log").append("<p>" + pos + "</p>");
				}
			});
		}
	}
	
});

var loadBoardInfo = function(){
	var info = "";
	for (var i = 1; i <= N; i++){
		for (var j = 1; j <= N; j++){
			info += "board[" + (i-1) +"][" + (j-1) + "][0]=" + $.trim($("#cell-" + i + "-" + j).text()) + "&";	
			info += "board[" + (i-1) +"][" + (j-1) + "][1]=" + $.trim($("#cell-" + i + "-" + j).attr("data-status")) + "&";	
			$.cookie("board-val-" + i + "-" + j, $.trim($("#cell-" + i + "-" + j).text()));
			
		}
	}
	return info;
};

var renderBoard = function (result){
	blueScore = parseInt(result["blueScore"]);
	greenScore = parseInt(result["greenScore"]);
	$("#blueScore").text(blueScore);
	$("#greenScore").text(greenScore);
	for (var i = 1; i <= N; i++){
		for (var j = 1; j <= N; j++){	
			var status = result["board"][i-1][j-1][1];
			$("#cell-" + i + "-" + j).attr("data-status", status);
		}
	}
	var finished = result["finished"];
	if (finished){
		if (blueScore >= greenScore){
			refreshTurn("blue");
			$("#blueToggle").attr("src", "winner.jpg");
		}
		else {
			refreshTurn("green");
			$("#greenToggle").attr("src", "winner.jpg");
		}
	}
	else
		refreshTurn(result["player"]);
};

var refreshTurn = function (newPlayer){
	player = newPlayer;
	if (player == "blue"){
		$("#blueToggle").css("visibility", "visible");		
		$("#greenToggle").css("visibility", "hidden");		
	}
	else if (player == "green"){
		$("#greenToggle").css("visibility", "visible");		
		$("#blueToggle").css("visibility", "hidden");		
	}
};

var randomFill = function(){
	for (var i = 1; i <= N; i++){
		for (var j = 1; j <= N; j++){
			var num = Math.floor(Math.random() * 100);
			$("#cell-" + i + "-" + j).text(num);
		}
	}
};

var cookieFill = function(){
	var boardState =  $.parseJSON($.cookie('boardGame'));
	for (var i = 1; i <= N; i++){
		for (var j = 1; j <= N; j++){
			$("#cell-" + i + "-" + j).attr('data-status', boardState['board'][i-1][j-1][1]);
			$("#cell-" + i + "-" + j).text(boardState['board'][i-1][j-1][0]);
//			alert($("#cell-" + i + "-" + j).attr('data-status'));
		}
	}
};

