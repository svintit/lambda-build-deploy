import logging

from package.clients.boto.sqs import SQSMessageAttributes
from package.clients.queue import TaskQueuer
from package import Worker
from package.tasks.base import TaskResponse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    records = event.get("Records", [])
    task_queuer = TaskQueuer()
    results = []

    for record in records:
        try:
            task_name = record.get("body")
            message_attributes = SQSMessageAttributes(
                record.get("messageAttributes")
            ).decode
            message_attributes["task"] = task_name
        except Exception as e:
            logger.error(f"SQS Message Error: {str(e)}, Message: {record}")
            raise Exception("Cannot parse message attributes")

        logger.info(f"==> Starting task {task_name}")

        response: TaskResponse = Worker.execute(message_attributes)

        if response.next_tasks:
            for task in response.next_tasks:
                task_queuer.add_task(
                    task.attributes.get("task"),
                    task.attributes,
                    task.task_runner,
                )

        if response.schedule_db_update:
            task_queuer.update_status(**response.result)

        results.append(response.result)

    return {"statusCode": 200, "body": results}
