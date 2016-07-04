
<?php

   function buildnode(&$a, $b, $c) {
	//$a["$b"] = array("size"=>"11K","date"=>"2016-08-19 12:00:00","type"=>"dir");
	$dev=$c["dev"];
	$ino=$c["ino"];
	$mode=$c["mode"];
	$nlink=$c["nlink"];
	$uid=$c["uid"];
	$gid=$c["gid"];
	$rdev=$c["rdev"];
	$size=$c["size"];
	$atime=$c["atime"];
	$mtime=$c["mtime"];
	$ctime=$c["ctime"];
	$blksize=$c["blksize"];
	$blocks=$c["blocks"];
	
	$a["$b"] =  array("dev"=>"$dev", "ino"=>"$ino", "mode"=>"$mode", "mode"=>"$mode", "nlink"=>"$nlink",
			"uid"=>"$uid", "gid"=>"$gid", "rdev"=>"$rdev", "size"=>"$size", "atime"=>"$atime",
			"ctime"=>"$ctime", "mtime"=>"$mtime", "blksize"=>"$blksize", "blocks"=>"$blocks");
	return 0;
   } 	
	
	#echo   $_GET['filename'];
	#echo   $_POST['filename'];
	$uid=$_GET['uid'];
	$gid=$_GET['gid'];
	$key=$_GET['key'];
	$base_dir=$_GET['filename'];
	$jj=array();
	if (empty($base_dir) || empty($uid) || empty($gid) || empty($key)) {
		$jj["error"] = array("errmsg"=>"Invalid argument", "errno"=>"22");
		echo json_encode($jj); 
                exit(1);
	}
	#$base_dir = "/root/bin/";
	#$base_dir=$_GET['filename'];
	if (file_exists($base_dir)) {
		$stat = stat($base_dir);
		//print_r($stat);
		//$jj["father_node"] = array("size"=>"$stat()","date"=>"2016-08-19 12:00:00","type"=>"dir");
		buildnode($jj, "father_node", $stat);
	} else {
		$jj["Error"] = array("errmsg"=>"No such file or directory", "errno"=>"2");
		#echo "Error: File not found $base_dir";
		echo json_encode($jj); 
		exit(1);
	}
	if (is_dir($base_dir) == FALSE) exit(1);
	$fso = opendir($base_dir);
	#echo $base_dir."<hr/>"   ;
	while($flist=readdir($fso)){
		#echo $flist."<br/>" ;
		$stat = stat("$base_dir/$flist");
		//$jj[$flist] = array("size"=>"111KB","date"=>"2016-08-19 12:00:00","type"=>"file");
		buildnode($jj, "$flist", $stat);
	}
	closedir($fso);
	#var_dump($jj);
	#echo $jj
?>
<?php 
//$json = '{"a":1,"b":2,"c":3,"d":4,"e":5}'; 
echo json_encode($jj); 
#var_dump(json_decode($json, true)); 
?> 
