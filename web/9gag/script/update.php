<?php

$data = json_decode(file_get_contents('php://input'), true);
if (isset($data['task'])) {
    require __DIR__ . '/library.php';
    $name = (isset($data['task']['name']) ? $data['task']['name'] : null);
    $description = (isset($data['task']['description']) ? $data['task']['description'] : null);
    $task_id = (isset($data['task']['id']) ? $data['task']['id'] : null);

    if ($name == null) {
        http_response_code(400);
        echo json_encode(['errors' => ["Name  required"]]);
    } else {

        // Update the Task
        $task = new Task();
        $task->Update($name, $description, $task_id);
    }
}
