task_routes = {
    "process_email_query": {
        "exchange": "notifications",
        "exchange_type": "direct",
        "routing_key": "email",
    },
    "process_websocket_query": {
        "exchange": "notifications",
        "exchange_type": "direct",
        "routing_key": "websocket",
    },
}
