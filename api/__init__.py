def result_message(result, error_message="Error"):
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": error_message}