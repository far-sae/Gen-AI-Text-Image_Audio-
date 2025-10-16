class APIError(Exception):
    pass

def handle_error(e: Exception):
    import logging
    logging.exception("Error in API handler")
    raise e
