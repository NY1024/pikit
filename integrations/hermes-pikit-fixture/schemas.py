READ_DOCUMENT = {
    "name": "pikit_read_document",
    "description": "Read an untrusted test document by reference.",
    "parameters": {
        "type": "object",
        "properties": {
            "ref": {"type": "string", "description": "Fixture document reference."},
        },
        "required": ["ref"],
    },
}

RECORD_SINK = {
    "name": "pikit_record_sink",
    "description": "Record a requested external action without performing it.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "target": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["action", "target", "content"],
    },
}
