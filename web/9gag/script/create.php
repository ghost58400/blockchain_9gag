<?php

$data = json_decode(file_get_contents('php://input'), TRUE);
//var_dump($data);
if (isset($data['task'])) {

    require __DIR__ . '/library.php';

    $name = (isset($data['task']['name']) ? $data['task']['name'] : NULL);
    $description = (isset($data['task']['description']) ? $data['task']['description'] : NULL);

    // validated the request
    if ($name == NULL) {
        http_response_code(400);
        echo json_encode(['errors' => ["Name  required"]]);

    } else {

        // Add the task
        $task = new Task();

        echo $task->create($name, $description);
    }
}
  ?>
