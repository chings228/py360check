<?php


$output = [];
$returnCode = null;

exec('python3 loopfile.py',$output,$returnCode);

print_r($returnCode);



if ($returnCode === 0) {
    echo "Execution successful!<br>";
    // Print all lines returned from Python
    echo "<pre>" . implode("\n", $output) . "</pre>";
} else {
    echo "Error executing script. Return code: " . $returnCode;
}



?>