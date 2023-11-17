def targetSchema(target) -> dict:
    return {
        "id": target.id,
        "category": target.category,
        "target": target.target,
        "message": target.message,
        "percentage": target.percentage
    }
    
def targetsSchema(targets) -> list:
    return [targetSchema(target) for target in targets]